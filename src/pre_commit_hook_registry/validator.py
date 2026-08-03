"""Strict consumer configuration policy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from pre_commit_hook_registry.models import Catalog, load_unique_yaml


@dataclass(frozen=True, slots=True)
class ValidationError:
    """Stable machine-readable policy diagnostic."""

    code: str
    message: str


_REPOSITORY_FIELDS = frozenset({"repo", "rev", "hooks"})
_HOOK_FIELDS = frozenset({"id", "args"})
_SAFE_ARGS = {
    "ruff-check": frozenset({"--fix", "--exit-non-zero-on-fix", "--show-fixes"}),
    "ruff-format": frozenset({"--check", "--diff"}),
}


def _error(code: str, message: str) -> ValidationError:
    return ValidationError(code, message)


def validate_config(config_path: Path, catalog: Catalog | None = None) -> tuple[ValidationError, ...]:
    """Validate a consumer config against the immutable packaged policy."""
    try:
        raw = load_unique_yaml(config_path.read_text(encoding="utf-8"))
    except OSError as error:
        return (_error("PCHR001", f"cannot read config: {error}"),)
    except ValueError as error:
        return (_error("PCHR002", str(error)),)
    try:
        policy = catalog if catalog is not None else Catalog.load()
    except (OSError, ValueError) as error:
        return (_error("PCHR900", f"internal catalog error: {error}"),)
    if not isinstance(raw, dict) or set(raw) != {"repos"} or not isinstance(raw.get("repos"), list):
        return (_error("PCHR003", "config must contain only a repos list"),)
    raw = cast("dict[str, Any]", raw)
    repos = raw["repos"]
    if len(repos) != 1:
        return (_error("PCHR004", "config must contain exactly one registry repository"),)
    repository = repos[0]
    if not isinstance(repository, dict):
        return (_error("PCHR005", "repository entry must be a mapping"),)
    repository = cast("dict[str, Any]", repository)
    unknown = set(repository) - _REPOSITORY_FIELDS
    missing = _REPOSITORY_FIELDS - set(repository)
    errors: list[ValidationError] = []
    if unknown or missing:
        message = f"repository fields invalid; unknown={sorted(unknown)}, missing={sorted(missing)}"
        errors.append(_error("PCHR006", message))
    url = repository.get("repo")
    if url != policy.registry_url:
        errors.append(_error("PCHR007", f"repository must be {policy.registry_url}"))
    revision = repository.get("rev")
    valid_revision = isinstance(revision, str) and len(revision) == 40
    if isinstance(revision, str):
        valid_revision = valid_revision and all(c in "0123456789abcdef" for c in revision)
    if not valid_revision:
        errors.append(_error("PCHR008", "revision must be a lowercase full 40-character commit SHA"))
    hooks = repository.get("hooks")
    if not isinstance(hooks, list) or not hooks:
        errors.append(_error("PCHR009", "hooks must be a non-empty list"))
        return tuple(errors)
    seen: set[str] = set()
    for index, hook in enumerate(hooks):
        if not isinstance(hook, dict):
            errors.append(_error("PCHR010", f"hook {index} must be a mapping"))
            continue
        hook = cast("dict[str, Any]", hook)
        unknown_hook = set(hook) - _HOOK_FIELDS
        if unknown_hook:
            errors.append(_error("PCHR011", f"hook {index} has forbidden fields: {sorted(unknown_hook)}"))
        hook_id = hook.get("id")
        if not isinstance(hook_id, str) or hook_id not in policy.approved_ids:
            errors.append(_error("PCHR012", f"unapproved hook id: {hook_id!r}"))
            continue
        if hook_id in seen:
            errors.append(_error("PCHR013", f"duplicate hook id: {hook_id}"))
        seen.add(hook_id)
        args: Any = hook.get("args")
        if args is not None:
            allowed = _SAFE_ARGS.get(hook_id, frozenset())
            valid_args = isinstance(args, list) and all(isinstance(arg, str) for arg in args)
            valid_args = valid_args and all(arg in allowed for arg in args)
            if not valid_args:
                errors.append(_error("PCHR014", f"forbidden args for {hook_id}"))
    if "validate-registry-config" not in seen:
        errors.append(_error("PCHR015", "validate-registry-config is required"))
    return tuple(errors)
