"""Create and push a verified SSH-signed release tag from protected main."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

_VERSION = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
_PROJECT = re.compile(r"(?ms)^\[project\]\s*$\n(?P<body>.*?)(?=^\[|\Z)")
_PROJECT_VERSION = re.compile(r'^version\s*=\s*"([^"]+)"\s*$', re.MULTILINE)


def run(*args: str, capture: bool = False) -> str:
    """Run a fixed-argument command and optionally return stripped stdout."""
    executable = shutil.which(args[0])
    if executable is None:
        raise RuntimeError(f"{args[0]} executable is required")
    result = subprocess.run(  # noqa: S603 - arguments are validated and shell=False
        [executable, *args[1:]], check=True, capture_output=capture, text=True
    )
    return result.stdout.strip() if capture else ""


def fail(message: str) -> None:
    """Stop before creating a tag with an actionable error."""
    raise SystemExit(message)


def project_version(document: str) -> str:
    """Read the version from the top-level project table without extra dependencies."""
    project = _PROJECT.search(document)
    version = _PROJECT_VERSION.search(project.group("body")) if project else None
    if version is None:
        fail("pyproject.toml must contain project.version")
    return version.group(1)


def main(version: str) -> None:
    """Validate the release candidate, sign its tag, verify it, and push it."""
    if _VERSION.fullmatch(version) is None:
        fail("VERSION must be a stable X.Y.Z version")
    tag = f"v{version}"

    if run("git", "status", "--porcelain", capture=True):
        fail("working tree must be clean")
    if run("git", "branch", "--show-current", capture=True) != "main":
        fail("release tags must be created from main")

    run("git", "fetch", "--prune", "origin", "main", "--tags")
    head = run("git", "rev-parse", "HEAD", capture=True)
    if head != run("git", "rev-parse", "origin/main", capture=True):
        fail("local main must exactly match origin/main")
    if (
        subprocess.run(  # noqa: S603 - fixed git arguments and validated tag
            [shutil.which("git") or "git", "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}"],
            check=False,
        ).returncode
        == 0
    ):
        fail(f"tag {tag} already exists")

    package_version = project_version(Path("pyproject.toml").read_text(encoding="utf-8"))
    manifest = json.loads(Path(".release-please-manifest.json").read_text(encoding="utf-8"))
    if package_version != version or manifest.get(".") != version:
        fail("VERSION must match pyproject.toml and .release-please-manifest.json")
    headings = re.findall(r"^## ([^\n]+)$", Path("CHANGELOG.md").read_text(encoding="utf-8"), re.MULTILINE)
    if sum(heading.startswith(version) for heading in headings) != 1:
        fail(f"CHANGELOG.md must contain exactly one {version} release heading")

    run("make", "check")
    signing = (
        "-c",
        "gpg.format=ssh",
        "-c",
        "gpg.ssh.allowedSignersFile=.github/allowed_signers",
    )
    run("git", *signing, "tag", "-s", tag, "-m", f"Release {tag}")
    run("git", *signing, "tag", "-v", tag)
    run("git", "push", "origin", tag)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("usage: make release VERSION=X.Y.Z")
    main(sys.argv[1])
