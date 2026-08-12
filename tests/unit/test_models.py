"""Catalog schema and packaged resource tests."""

import re
from pathlib import Path

import pytest

from pre_commit_hook_registry.models import Catalog, Upstream, load_unique_yaml


def test_packaged_catalog_is_complete() -> None:
    catalog = Catalog.load()
    assert catalog.registry_url == "https://github.com/aydabd/pre-commit-hook-registry"
    assert len(catalog.upstreams) == 4
    assert {"gitleaks", "ruff-check", "check-yaml"} <= catalog.approved_ids


def test_explicit_catalog_path(tmp_path: Path) -> None:
    source = Path("src/pre_commit_hook_registry/catalog.yaml")
    copy = tmp_path / "catalog.yaml"
    copy.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    assert Catalog.load(copy) == Catalog.load()


def test_catalog_uses_only_registered_adapter_mechanisms() -> None:
    assert {upstream.runtime_adapter for upstream in Catalog.load().upstreams} <= Upstream.RUNTIME_ADAPTERS


def test_every_admitted_upstream_records_a_disposition() -> None:
    allowed = {"Proxy upstream", "Reviewed adapter", "Consumer-local/system hook", "Exclude"}
    prefix = "- Disposition: "
    for upstream in Catalog.load().upstreams:
        review = Path(upstream.review_record).read_text(encoding="utf-8")
        dispositions = [line.removeprefix(prefix) for line in review.splitlines() if line.startswith(prefix)]
        assert len(dispositions) == 1, upstream.name
        assert dispositions[0] in allowed, upstream.name


def test_unregistered_adapter_mechanism_is_rejected() -> None:
    text = Path("src/pre_commit_hook_registry/catalog.yaml").read_text(encoding="utf-8")
    text = text.replace("python-git-dependency", "shell-installer", 1)
    message = (
        "upstream 'pre-commit-hooks' uses unregistered runtime_adapter 'shell-installer'; "
        "registered adapters: golang-additional-dependency, node-package, python-git-dependency, python-package"
    )
    with pytest.raises(ValueError, match=re.escape(message)):
        Catalog.from_text(text)


def _valid_upstream_mapping() -> dict[str, object]:
    return {
        "url": "https://example.invalid/upstream",
        "tag": "v1.0.0",
        "sha": "a" * 40,
        "license": "MIT",
        "runtime_adapter": "node-package",
        "runtime_packages": [],
        "approved_ids": ["example"],
        "review_record": "reviews/example.md",
    }


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: value.update(runtime_packages="not-a-list"),
        lambda value: value.update(runtime_packages=[{"name": "pkg", "version": "1.0.0"}]),
        lambda value: value.update(
            runtime_packages=[{"name": "pkg", "version": "1.0.0", "integrity": "sha256-nope"}]
        ),
        lambda value: value.update(
            runtime_packages=[
                {"name": "pkg", "version": "1.0.0", "integrity": "sha512-one"},
                {"name": "pkg", "version": "1.0.0", "integrity": "sha512-two"},
            ]
        ),
    ],
    ids=["packages-not-list", "package-fields", "package-integrity", "duplicate-package"],
)
def test_invalid_runtime_packages_are_rejected(mutate: object) -> None:
    value = _valid_upstream_mapping()
    mutate(value)  # type: ignore[operator]
    with pytest.raises(ValueError):
        Upstream.from_mapping("example", value)


@pytest.mark.parametrize(
    "text",
    [
        "key: one\nkey: two\n",
        "schema_version: 2\nregistry: {url: x, required_ids: [x]}\nupstreams: {}\n",
        "schema_version: 1\nregistry: {url: x, required_ids: [x], extra: y}\nupstreams: {}\n",
        "[]",
    ],
)
def test_invalid_catalog_or_yaml_is_rejected(text: str) -> None:
    with pytest.raises(ValueError):
        if text.startswith("key"):
            load_unique_yaml(text)
        else:
            Catalog.from_text(text)
