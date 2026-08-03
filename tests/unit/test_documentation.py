"""Generated documentation tests."""

from pathlib import Path

from pre_commit_hook_registry.documentation import generate_catalog_document, render_catalog
from pre_commit_hook_registry.models import Catalog


def test_catalog_reference_is_current() -> None:
    assert Path("docs/catalog.md").read_text(encoding="utf-8") == render_catalog(Catalog.load())


def test_generate_catalog_document(tmp_path: Path) -> None:
    destination = tmp_path / "nested" / "catalog.md"
    generate_catalog_document(destination)
    assert "Gitleaks" not in destination.read_text(encoding="utf-8")
    assert "gitleaks" in destination.read_text(encoding="utf-8")
