"""Catalog schema and packaged resource tests."""

from pathlib import Path

import pytest

from pre_commit_hook_registry.models import Catalog, load_unique_yaml


def test_packaged_catalog_is_complete() -> None:
    catalog = Catalog.load()
    assert catalog.registry_url == "https://github.com/aydabd/pre-commit-hook-registry"
    assert len(catalog.upstreams) == 3
    assert {"gitleaks", "ruff-check", "check-yaml"} <= catalog.approved_ids


def test_explicit_catalog_path(tmp_path: Path) -> None:
    source = Path("src/pre_commit_hook_registry/catalog.yaml")
    copy = tmp_path / "catalog.yaml"
    copy.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    assert Catalog.load(copy) == Catalog.load()


@pytest.mark.parametrize(
    "text",
    [
        "key: one\nkey: two\n",
        "schema_version: 2\nregistry: {url: x}\nupstreams: {}\n",
        "schema_version: 1\nregistry: {url: x, extra: y}\nupstreams: {}\n",
        "[]",
    ],
)
def test_invalid_catalog_or_yaml_is_rejected(text: str) -> None:
    with pytest.raises(ValueError):
        if text.startswith("key"):
            load_unique_yaml(text)
        else:
            Catalog.from_text(text)
