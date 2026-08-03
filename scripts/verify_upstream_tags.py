"""Verify reviewed upstream tags still resolve to catalog commits."""

from __future__ import annotations

import shutil
import subprocess

from pre_commit_hook_registry.models import Catalog

git = shutil.which("git")
if git is None:
    raise RuntimeError("git executable is required")

for upstream in Catalog.load().upstreams:
    reference = f"refs/tags/{upstream.tag}"
    result = subprocess.run(  # noqa: S603 - fixed git subcommand and catalog-reviewed URL
        [git, "ls-remote", upstream.url, reference, f"{reference}^{{}}"],
        check=True,
        capture_output=True,
        text=True,
    )
    resolved = {line.split()[0] for line in result.stdout.splitlines()}
    if upstream.sha not in resolved:
        raise RuntimeError(f"{upstream.name} {upstream.tag} does not resolve to {upstream.sha}")
    print(f"verified {upstream.name} {upstream.tag} -> {upstream.sha}")
