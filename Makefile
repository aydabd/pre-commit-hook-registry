UV ?= uv

.PHONY: bootstrap check lint typecheck test build docs docs-check locks-check release clean

bootstrap:
	$(UV) sync --all-groups --locked

lint:
	$(UV) run ruff check .
	$(UV) run ruff format --check .

typecheck:
	$(UV) run pyright

test:
	$(UV) run pytest

build:
	$(UV) build

docs:
	$(UV) run python -c 'from pathlib import Path; from pre_commit_hook_registry.documentation import generate_catalog_document; generate_catalog_document(Path("docs/catalog.md"))'

docs-check:
	$(UV) run python -c 'from pathlib import Path; from pre_commit_hook_registry.documentation import render_catalog; from pre_commit_hook_registry.models import Catalog; assert Path("docs/catalog.md").read_text() == render_catalog(Catalog.load())'

locks-check:
	$(UV) lock --check
	@if command -v go >/dev/null; then go mod verify; else echo "go is required for go mod verify"; exit 1; fi
	$(UV) run python scripts/verify_upstream_tags.py

check: lint typecheck test docs-check locks-check build

release:
	@test -n "$(VERSION)" || { echo "usage: make release VERSION=X.Y.Z"; exit 2; }
	$(UV) run python scripts/release.py "$(VERSION)"

clean:
	rm -rf .venv .coverage .pytest_cache .ruff_cache .pyright build dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
