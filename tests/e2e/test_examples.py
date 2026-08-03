"""Templated consumer examples."""

from pathlib import Path

import pytest

from pre_commit_hook_registry.validator import validate_config


@pytest.mark.parametrize("path", sorted(Path("consumer-examples").glob("*.yaml")))
def test_example_after_release_sha_substitution(path: Path, tmp_path: Path) -> None:
    rendered = path.read_text(encoding="utf-8").replace("<FULL_RELEASE_COMMIT_SHA>", "a" * 40)
    target = tmp_path / path.name
    target.write_text(rendered, encoding="utf-8")
    assert validate_config(target) == ()
