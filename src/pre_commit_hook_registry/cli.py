"""Command-line interface for consumer policy validation."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from pre_commit_hook_registry.validator import validate_config


def build_parser() -> argparse.ArgumentParser:
    """Create the public command parser."""
    parser = argparse.ArgumentParser(prog="pre-commit-hook-registry")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate a consumer pre-commit config")
    validate.add_argument("config", nargs="?", type=Path, default=Path(".pre-commit-config.yaml"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI without exposing tracebacks for expected input failures."""
    args = build_parser().parse_args(argv)
    errors = validate_config(args.config)
    for error in errors:
        print(f"{error.code}: {error.message}")  # noqa: T201
    return int(bool(errors))
