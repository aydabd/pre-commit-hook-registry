"""Public manifest and catalog drift tests."""

from pathlib import Path

import yaml

from pre_commit_hook_registry.models import Catalog


def test_manifest_exports_exact_catalog_ids() -> None:
    manifest = yaml.safe_load(Path(".pre-commit-hooks.yaml").read_text(encoding="utf-8"))
    assert {item["id"] for item in manifest} == Catalog.load().approved_ids
    assert len(manifest) == len(Catalog.load().approved_ids)


def test_runtime_pins_match_catalog() -> None:
    manifest = Path(".pre-commit-hooks.yaml").read_text(encoding="utf-8")
    for upstream in Catalog.load().upstreams:
        if upstream.name != "ruff-pre-commit":
            assert upstream.sha in manifest
    assert "ruff==0.15.22" in manifest


def test_public_catalog_copy_matches_packaged_canonical_resource() -> None:
    assert Catalog.load(Path("catalog/hooks.yaml")) == Catalog.load()
