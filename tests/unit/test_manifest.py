"""Public manifest and catalog drift tests."""

import json
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


def test_node_runtime_lock_matches_catalog_and_has_no_unreviewed_packages() -> None:
    catalog = Catalog.load()
    biome = next(item for item in catalog.upstreams if item.name == "biome-pre-commit")
    lock = json.loads(Path("package-lock.json").read_text(encoding="utf-8"))
    expected = {name: (version, integrity) for name, version, integrity in biome.runtime_packages}
    root = lock["packages"][""]
    assert root["dependencies"] == {"@biomejs/biome": expected["@biomejs/biome"][0]}
    assert set(lock["packages"]) - {""} == {
        "node_modules/@biomejs/biome",
        "node_modules/@biomejs/cli-darwin-arm64",
        "node_modules/@biomejs/cli-darwin-x64",
        "node_modules/@biomejs/cli-linux-arm64",
        "node_modules/@biomejs/cli-linux-arm64-musl",
        "node_modules/@biomejs/cli-linux-x64",
        "node_modules/@biomejs/cli-linux-x64-musl",
        "node_modules/@biomejs/cli-win32-arm64",
        "node_modules/@biomejs/cli-win32-x64",
    }
    for name, (version, integrity) in expected.items():
        package = lock["packages"][f"node_modules/{name}"]
        assert package["version"] == version
        assert package["integrity"] == integrity
    assert set(expected) == {path.removeprefix("node_modules/") for path in lock["packages"] if path}
    assert "scripts" not in Path("package.json").read_text(encoding="utf-8")
    assert Path(".npmrc").read_text(encoding="utf-8") == "ignore-scripts=true\n"


def test_gitleaks_uses_declared_go_module_at_reviewed_sha() -> None:
    manifest = yaml.safe_load(Path(".pre-commit-hooks.yaml").read_text(encoding="utf-8"))
    gitleaks = next(item for item in manifest if item["id"] == "gitleaks")
    dependency = "github.com/zricethezav/gitleaks/v8@83d9cd684c87d95d656c1458ef04895a7f1cbd8e"

    assert gitleaks["additional_dependencies"] == [dependency]
    assert "require github.com/zricethezav/gitleaks/v8 v8.30.1" in Path("go.mod").read_text(encoding="utf-8")


def test_biome_manifest_is_the_upstream_check_only_hook() -> None:
    manifest = yaml.safe_load(Path(".pre-commit-hooks.yaml").read_text(encoding="utf-8"))
    biome = next(item for item in manifest if item["id"] == "biome-ci")
    assert biome == {
        "id": "biome-ci",
        "name": "biome ci",
        "description": "Run Biome checks without writing files",
        "entry": "biome ci --files-ignore-unknown=true --no-errors-on-unmatched",
        "language": "node",
        "types": ["text"],
        "files": r"\.(jsx?|tsx?|c(js|ts)|m(js|ts)|d\.(ts|cts|mts)|jsonc?|css|svelte|vue|astro|graphql|gql)$",
        "require_serial": True,
    }
    assert not {item["id"] for item in manifest} & {"biome-check", "biome-format", "biome-lint"}


def test_every_review_identity_and_disposition_match_catalog_and_manifest() -> None:
    catalog = Catalog.load()
    manifest = yaml.safe_load(Path(".pre-commit-hooks.yaml").read_text(encoding="utf-8"))
    allowed_dispositions = {"Proxy upstream", "Reviewed adapter", "Consumer-local/system hook", "Exclude"}

    for upstream in catalog.upstreams:
        review = Path(upstream.review_record).read_text(encoding="utf-8")
        dispositions = [
            line.removeprefix("- Disposition: ")
            for line in review.splitlines()
            if line.startswith("- Disposition: ")
        ]

        assert f"- Upstream: `{upstream.url}`" in review
        assert f"`{upstream.tag}`" in review
        assert upstream.sha in review
        assert "- License:" in review
        assert len(dispositions) == 1
        assert dispositions[0] in allowed_dispositions
        assert {hook["id"] for hook in manifest} >= set(upstream.approved_ids)
