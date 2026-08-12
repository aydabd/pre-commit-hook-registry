"""Templated consumer examples."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import pytest

from pre_commit_hook_registry.validator import validate_config

_EXAMPLE_DIRECTORY = Path("consumer-examples")
_PLACEHOLDER = "<FULL_RELEASE_COMMIT_SHA>"
_FULL_SHA = re.compile(r"[0-9a-f]{40}")


@dataclass(frozen=True, slots=True)
class ExampleFixture:
    """Deterministic clean and failing inputs for one consumer template."""

    clean_files: dict[str, str]
    failing_file: tuple[str, str]
    failure_hook_name: str
    forbidden_output: str | None = None


_FAKE_PRIVATE_KEY_BODY = "definitely-not-a-real-private-key"
_EXAMPLES = {
    "minimal.yaml": ExampleFixture(
        clean_files={"data.yaml": "key: value\n", "notes.txt": "clean text\n"},
        failing_file=("broken.yaml", "key: [\n"),
        failure_hook_name="check yaml",
    ),
    "python.yaml": ExampleFixture(
        clean_files={"example.py": "answer = 42\n", "data.yaml": "key: value\n"},
        failing_file=("broken.py", "def broken(:\n"),
        failure_hook_name="ruff check",
    ),
    "security.yaml": ExampleFixture(
        clean_files={"notes.txt": "synthetic fixture with no credentials\n"},
        failing_file=(
            "synthetic-test-key.pem",
            f"-----BEGIN RSA PRIVATE KEY-----\n{_FAKE_PRIVATE_KEY_BODY}\n-----END RSA PRIVATE KEY-----\n",
        ),
        failure_hook_name="detect private key",
        forbidden_output=_FAKE_PRIVATE_KEY_BODY,
    ),
    "node.yaml": ExampleFixture(
        clean_files={"src/good.js": "const answer = 42;\n", "notes.txt": "ignored by Biome\n"},
        failing_file=("src/bad.js", "const answer = ;\n"),
        failure_hook_name="biome ci",
    ),
}


def render_example(source: str, revision: str) -> str:
    """Render exactly one release placeholder with a lowercase full commit SHA."""
    if source.count(_PLACEHOLDER) != 1:
        raise ValueError("consumer example must contain exactly one release commit placeholder")
    if _FULL_SHA.fullmatch(revision) is None:
        raise ValueError("consumer example revision must be a lowercase full commit SHA")
    rendered = source.replace(_PLACEHOLDER, revision)
    if _PLACEHOLDER in rendered:
        raise ValueError("consumer example release commit placeholder was not fully rendered")
    return rendered


def _executable(name: str) -> str:
    executable = shutil.which(name)
    if executable is None:
        raise RuntimeError(f"required executable is unavailable: {name}")
    return executable


def _run(command: list[str], *, cwd: Path, environment: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        command,
        cwd=cwd,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


def _write_files(root: Path, files: dict[str, str]) -> None:
    for name, contents in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding="utf-8")


def _snapshot_consumer_files(root: Path) -> dict[str, bytes]:
    """Capture consumer files while excluding Git's mutable administrative directory."""
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }


def test_every_consumer_example_has_an_execution_fixture() -> None:
    assert {path.name for path in _EXAMPLE_DIRECTORY.glob("*.yaml")} == set(_EXAMPLES)


def test_readme_identifies_the_template_release_placeholder() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert readme.count(_PLACEHOLDER) == 1
    assert f"Replace `{_PLACEHOLDER}` with the commit behind a published release." in readme


@pytest.mark.parametrize(
    ("source", "revision", "message"),
    [
        ("repos: []\n", "a" * 40, "exactly one"),
        (f"{_PLACEHOLDER}\n{_PLACEHOLDER}\n", "a" * 40, "exactly one"),
        (_PLACEHOLDER, "a" * 39, "lowercase full"),
        (_PLACEHOLDER, "A" * 40, "lowercase full"),
        (_PLACEHOLDER, "v0.1.0", "lowercase full"),
    ],
)
def test_release_sha_rendering_rejects_ambiguous_input(source: str, revision: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        render_example(source, revision)


@pytest.mark.parametrize("path", sorted(_EXAMPLE_DIRECTORY.glob("*.yaml")))
def test_example_after_release_sha_substitution(path: Path, tmp_path: Path) -> None:
    rendered = render_example(path.read_text(encoding="utf-8"), "a" * 40)
    target = tmp_path / path.name
    target.write_text(rendered, encoding="utf-8")
    assert validate_config(target) == ()


@pytest.mark.installed_examples
@pytest.mark.parametrize(("example_name", "fixture"), sorted(_EXAMPLES.items()))
def test_installed_consumer_example(
    example_name: str,
    fixture: ExampleFixture,
    tmp_path: Path,
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    revision = os.environ.get("CONSUMER_EXAMPLE_REV")
    if revision is None:
        pytest.skip("CONSUMER_EXAMPLE_REV selects the immutable registry commit for installed tests")

    source = (_EXAMPLE_DIRECTORY / example_name).read_text(encoding="utf-8")
    rendered = render_example(source, revision)
    config = tmp_path / ".pre-commit-config.yaml"
    config.write_text(rendered, encoding="utf-8")
    assert validate_config(config) == ()

    environment = os.environ.copy()
    environment["PRE_COMMIT_HOME"] = str(tmp_path_factory.mktemp("pre-commit-cache"))
    git = _executable("git")
    pre_commit = _executable("pre-commit")

    for command in (
        [git, "init", "--quiet"],
        [git, "config", "user.name", "Consumer example test"],
        [git, "config", "user.email", "consumer-example@example.invalid"],
    ):
        result = _run(command, cwd=tmp_path, environment=environment)
        assert result.returncode == 0, result.stderr

    _write_files(tmp_path, fixture.clean_files)
    if example_name == "node.yaml":
        _write_files(
            tmp_path,
            {f"src/large/file-{index:03d}.js": "const value = 42;\n" for index in range(500)},
        )
    result = _run([git, "add", "."], cwd=tmp_path, environment=environment)
    assert result.returncode == 0, result.stderr

    install_started = time.perf_counter()
    install = _run([pre_commit, "install-hooks"], cwd=tmp_path, environment=environment)
    install_elapsed = time.perf_counter() - install_started
    assert install.returncode == 0, install.stdout + install.stderr
    clean = _run(
        [pre_commit, "run", "--all-files", "--color", "never"],
        cwd=tmp_path,
        environment={
            **environment,
            "HTTP_PROXY": "http://127.0.0.1:9",
            "HTTPS_PROXY": "http://127.0.0.1:9",
            "ALL_PROXY": "http://127.0.0.1:9",
            "NO_PROXY": "",
        },
    )
    cold_elapsed = install_elapsed + (time.perf_counter() - install_started)
    assert clean.returncode == 0, clean.stdout + clean.stderr
    clean_snapshot = _snapshot_consumer_files(tmp_path)
    if example_name == "node.yaml":
        warm_elapsed = []
        for _ in range(5):
            started = time.perf_counter()
            warm = _run(
                [pre_commit, "run", "--all-files", "--color", "never"],
                cwd=tmp_path,
                environment=environment,
            )
            warm_elapsed.append(time.perf_counter() - started)
            assert warm.returncode == 0, warm.stdout + warm.stderr
        print(
            f"biome performance: cold={cold_elapsed:.3f}s warm={[round(value, 3) for value in warm_elapsed]}"
        )
        assert cold_elapsed <= 5
        assert max(warm_elapsed) <= 2

    result = _run(
        [git, "commit", "--quiet", "--no-verify", "-m", "clean fixture"],
        cwd=tmp_path,
        environment=environment,
    )
    assert result.returncode == 0, result.stderr
    failing_name, failing_contents = fixture.failing_file
    _write_files(tmp_path, {failing_name: failing_contents})
    result = _run([git, "add", "."], cwd=tmp_path, environment=environment)
    assert result.returncode == 0, result.stderr

    failing = _run(
        [pre_commit, "run", "--all-files", "--color", "never"],
        cwd=tmp_path,
        environment={
            **environment,
            "HTTP_PROXY": "http://127.0.0.1:9",
            "HTTPS_PROXY": "http://127.0.0.1:9",
            "ALL_PROXY": "http://127.0.0.1:9",
            "NO_PROXY": "",
        },
    )
    output = failing.stdout + failing.stderr
    assert failing.returncode != 0, output
    # pre-commit reports the manifest's human-readable hook name, not its hook id.
    assert fixture.failure_hook_name in output.lower(), output
    if fixture.forbidden_output is not None:
        assert fixture.forbidden_output not in output
    assert _snapshot_consumer_files(tmp_path) == clean_snapshot
