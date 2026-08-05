"""Tests for the guarded release helper."""

from __future__ import annotations

import runpy
from collections.abc import Callable
from pathlib import Path
from typing import cast

import pytest


def release_function() -> Callable[[str], str]:
    """Load the release parser without executing its command-line entry point."""
    namespace = runpy.run_path(str(Path("scripts/release.py")))
    return cast(Callable[[str], str], namespace["project_version"])


def test_project_version_reads_only_the_project_table() -> None:
    """Return the package version rather than a similarly named tool field."""
    document = '[tool.example]\nversion = "9.9.9"\n\n[project]\nname = "example"\nversion = "1.2.3"\n'

    assert release_function()(document) == "1.2.3"


def test_project_version_requires_a_version() -> None:
    """Fail clearly when release metadata is incomplete."""
    with pytest.raises(SystemExit, match="pyproject.toml must contain project.version"):
        release_function()('[project]\nname = "example"\n')
