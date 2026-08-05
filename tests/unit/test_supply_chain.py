"""Security invariants for executable automation boundaries."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any

import yaml

_ACTION_PIN = re.compile(r"^[^@]+@[0-9a-f]{40}$")


def _walk_steps(value: object) -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = []
    if isinstance(value, dict):
        mapping = value
        if "uses" in mapping or "run" in mapping:
            steps.append(mapping)
        for child in mapping.values():
            steps.extend(_walk_steps(child))
    elif isinstance(value, list):
        for child in value:
            steps.extend(_walk_steps(child))
    return steps


def test_actions_are_sha_pinned_and_shells_exclude_untrusted_expressions() -> None:
    for workflow_path in Path(".github/workflows").glob("*.yaml"):
        workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        for step in _walk_steps(workflow):
            if "uses" in step:
                assert _ACTION_PIN.fullmatch(step["uses"]), (workflow_path, step["uses"])
            script = step.get("run", "")
            assert "${{ github.event" not in script
            assert "${{ inputs." not in script


def test_python_subprocesses_never_enable_a_shell() -> None:
    for script_path in Path("scripts").glob("*.py"):
        tree = ast.parse(script_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Attribute) and node.func.attr in {"run", "call", "Popen"}:
                shell_keywords = [item for item in node.keywords if item.arg == "shell"]
                assert not shell_keywords or all(
                    isinstance(item.value, ast.Constant) and item.value.value is False
                    for item in shell_keywords
                )


def test_go_toolchain_is_exact_and_consistent_across_workflows() -> None:
    toolchain = "1.26.5"
    assert f"toolchain go{toolchain}" in Path("go.mod").read_text(encoding="utf-8")
    for workflow_path in Path(".github/workflows").glob("*.yaml"):
        workflow = workflow_path.read_text(encoding="utf-8")
        if "actions/setup-go@" in workflow:
            assert f"go-version: {toolchain}" in workflow


def test_dependabot_applies_cooling_period_to_every_ecosystem() -> None:
    config = yaml.safe_load(Path(".github/dependabot.yml").read_text(encoding="utf-8"))
    assert config["updates"]
    for update in config["updates"]:
        assert update["cooldown"]["default-days"] == 14


def test_release_please_only_prepares_release_pull_requests() -> None:
    workflow = yaml.safe_load(Path(".github/workflows/release-please.yaml").read_text(encoding="utf-8"))
    steps = workflow["jobs"]["release-please"]["steps"]

    assert len(steps) == 1
    step = steps[0]
    options = step.get("with", {})
    assert step.get("uses", "").startswith("googleapis/release-please-action@")
    assert options.get("skip-github-release") is True
    assert "skip-labeling" not in options


def test_release_publication_requires_a_version_tag() -> None:
    workflow = yaml.safe_load(Path(".github/workflows/release.yaml").read_text(encoding="utf-8"))
    triggers = workflow.get("on", workflow.get(True))
    config = json.loads(Path("release-please-config.json").read_text(encoding="utf-8"))
    package = config["packages"]["."]

    assert triggers == {"push": {"tags": ["v*.*.*"]}}
    assert package["include-component-in-tag"] is False
    assert package["include-v-in-tag"] is True
