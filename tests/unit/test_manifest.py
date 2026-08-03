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


def test_gitleaks_uses_declared_go_module_at_reviewed_sha() -> None:
    manifest = yaml.safe_load(Path(".pre-commit-hooks.yaml").read_text(encoding="utf-8"))
    gitleaks = next(item for item in manifest if item["id"] == "gitleaks")
    dependency = "github.com/zricethezav/gitleaks/v8@83d9cd684c87d95d656c1458ef04895a7f1cbd8e"

    assert gitleaks["additional_dependencies"] == [dependency]
    assert "require github.com/zricethezav/gitleaks/v8 v8.30.1" in Path("go.mod").read_text(encoding="utf-8")
