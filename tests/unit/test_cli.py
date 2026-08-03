"""CLI contract tests."""

from pathlib import Path

from pre_commit_hook_registry.cli import build_parser, main


def test_default_config() -> None:
    assert build_parser().parse_args(["validate"]).config == Path(".pre-commit-config.yaml")


def test_cli_reports_diagnostics(tmp_path: Path, capsys: object) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("repos: []\n", encoding="utf-8")
    assert main(["validate", str(path)]) == 1
    assert "PCHR004" in capsys.readouterr().out  # type: ignore[attr-defined]
