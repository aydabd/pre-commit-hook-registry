"""Consumer policy tests."""

from pathlib import Path

import pytest

from pre_commit_hook_registry.validator import validate_config


def _write(tmp_path: Path, body: str) -> Path:
    path = tmp_path / ".pre-commit-config.yaml"
    path.write_text(body, encoding="utf-8")
    return path


def _config(
    rev: str = "a" * 40,
    hooks: str = "      - id: validate-registry-config\n",
    repo: str = "https://github.com/aydabd/pre-commit-hook-registry",
) -> str:
    return f"repos:\n  - repo: {repo}\n    rev: {rev}\n    hooks:\n{hooks}"


def test_valid_opt_in_and_safe_ruff_args(tmp_path: Path) -> None:
    body = _config(
        hooks="      - id: validate-registry-config\n      - id: ruff-check\n        args: [--fix, --show-fixes]\n"
    )
    assert validate_config(_write(tmp_path, body)) == ()


@pytest.mark.parametrize(
    ("body", "code"),
    [
        ("repos: [\n", "PCHR002"),
        ("repos: []\n", "PCHR004"),
        (_config(repo="local"), "PCHR007"),
        (_config(repo="git@github.com:aydabd/pre-commit-hook-registry"), "PCHR007"),
        (_config(rev="v0.1.0"), "PCHR008"),
        (_config(rev="A" * 40), "PCHR008"),
        (_config(hooks="      - id: check-yaml\n"), "PCHR015"),
        (_config(hooks="      - id: validate-registry-config\n      - id: unknown\n"), "PCHR012"),
        (
            _config(hooks="      - id: validate-registry-config\n      - id: validate-registry-config\n"),
            "PCHR013",
        ),
        (_config(hooks="      - id: validate-registry-config\n        stages: [manual]\n"), "PCHR011"),
        (
            _config(
                hooks="      - id: check-yaml\n        args: [--unsafe]\n      - id: validate-registry-config\n"
            ),
            "PCHR014",
        ),
        ("repos:\n  - repo: local\n    repo: meta\n    rev: x\n    hooks: []\n", "PCHR002"),
    ],
)
def test_rejections(tmp_path: Path, body: str, code: str) -> None:
    assert code in {item.code for item in validate_config(_write(tmp_path, body))}


def test_missing_file_is_stable_diagnostic(tmp_path: Path) -> None:
    assert validate_config(tmp_path / "missing")[0].code == "PCHR001"
