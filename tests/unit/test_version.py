"""Tests for package version resolution."""

from importlib.metadata import PackageNotFoundError

import pytest

from pre_commit_hook_registry import version


def test_get_version_uses_installed_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    """Return installed package metadata when available."""
    monkeypatch.setattr(version, "version", lambda _: "1.2.3")

    assert version.get_version() == "1.2.3"


def test_get_version_has_local_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """Return a deterministic fallback outside an installed package."""

    def missing(_: str) -> str:
        raise PackageNotFoundError

    monkeypatch.setattr(version, "version", missing)

    assert version.get_version() == "0.0.0+local"
