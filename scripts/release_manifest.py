"""Emit the deterministic release material manifest."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from pre_commit_hook_registry.models import Catalog
from pre_commit_hook_registry.version import get_version


def digest(path: Path) -> str:
    """Return a file SHA-256."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


catalog = Catalog.load()
git = shutil.which("git")
if git is None:
    raise RuntimeError("git executable is required")
payload = {
    "registry_version": get_version(),
    "registry_commit": subprocess.run(  # noqa: S603 - fixed git arguments
        [git, "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    ).stdout.strip(),
    "catalog_sha256": digest(Path("src/pre_commit_hook_registry/catalog.yaml")),
    "upstreams": {item.name: item.sha for item in catalog.upstreams},
    "locks": {name: digest(Path(name)) for name in ("uv.lock", "go.mod", "go.sum")},
    "artifacts": {
        path.name: digest(path)
        for path in sorted(Path("dist").iterdir())
        if path.name != "release-manifest.json"
    },
}
print(json.dumps(payload, indent=2, sort_keys=True))
