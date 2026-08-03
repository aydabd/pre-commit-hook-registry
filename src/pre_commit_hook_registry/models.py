"""Validated models for the registry's packaged provenance catalog."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, ClassVar, cast

import yaml
from typing_extensions import Self


class UniqueKeyLoader(yaml.SafeLoader):
    """YAML loader which rejects duplicate mapping keys."""


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def load_unique_yaml(text: str) -> object:
    """Parse YAML while rejecting duplicate keys."""
    try:
        return yaml.load(text, Loader=UniqueKeyLoader)  # noqa: S506
    except yaml.YAMLError as error:
        raise ValueError(f"malformed YAML: {error}") from error


def _string(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"'{key}' must be a non-empty string")
    return value


@dataclass(frozen=True, slots=True)
class Upstream:
    """One reviewed, immutable upstream source."""

    name: str
    url: str
    tag: str
    sha: str
    license: str
    runtime_adapter: str
    approved_ids: tuple[str, ...]
    review_record: str

    FIELDS: ClassVar[frozenset[str]] = frozenset(
        {"url", "tag", "sha", "license", "runtime_adapter", "approved_ids", "review_record"}
    )

    @classmethod
    def from_mapping(cls, name: str, value: object) -> Self:
        """Build an upstream after strict schema validation."""
        if not isinstance(value, dict) or set(value) != cls.FIELDS:
            raise ValueError(f"upstream '{name}' has missing or unknown fields")
        value = cast("dict[str, Any]", value)
        ids = value["approved_ids"]
        if not isinstance(ids, list) or not ids or not all(isinstance(item, str) and item for item in ids):
            raise ValueError(f"upstream '{name}' approved_ids must be non-empty strings")
        if len(ids) != len(set(ids)):
            raise ValueError(f"upstream '{name}' approved_ids must be unique")
        sha = _string(value, "sha")
        if len(sha) != 40 or any(character not in "0123456789abcdef" for character in sha):
            raise ValueError(f"upstream '{name}' sha must be a lowercase full SHA")
        return cls(
            name=name,
            url=_string(value, "url"),
            tag=_string(value, "tag"),
            sha=sha,
            license=_string(value, "license"),
            runtime_adapter=_string(value, "runtime_adapter"),
            approved_ids=tuple(ids),
            review_record=_string(value, "review_record"),
        )


@dataclass(frozen=True, slots=True)
class Catalog:
    """Canonical registry identity and reviewed upstreams."""

    schema_version: int
    registry_url: str
    upstreams: tuple[Upstream, ...]

    @classmethod
    def from_text(cls, text: str) -> Self:
        """Load a catalog from YAML text."""
        raw = load_unique_yaml(text)
        if not isinstance(raw, dict) or set(raw) != {"schema_version", "registry", "upstreams"}:
            raise ValueError("catalog root has missing or unknown fields")
        raw = cast("dict[str, Any]", raw)
        if raw["schema_version"] != 1:
            raise ValueError("unsupported catalog schema_version")
        registry = raw["registry"]
        if not isinstance(registry, dict) or set(registry) != {"url"}:
            raise ValueError("registry must contain only url")
        upstreams = raw["upstreams"]
        if not isinstance(upstreams, dict) or not upstreams:
            raise ValueError("upstreams must be a non-empty mapping")
        parsed = tuple(Upstream.from_mapping(str(name), value) for name, value in upstreams.items())
        all_ids = [hook_id for upstream in parsed for hook_id in upstream.approved_ids]
        if len(all_ids) != len(set(all_ids)):
            raise ValueError("approved hook ids must be globally unique")
        return cls(1, _string(registry, "url"), parsed)

    @classmethod
    def load(cls, path: Path | None = None) -> Self:
        """Load the canonical package resource, or an explicit path for tooling/tests."""
        if path is not None:
            return cls.from_text(path.read_text(encoding="utf-8"))
        resource = resources.files("pre_commit_hook_registry").joinpath("catalog.yaml")
        return cls.from_text(resource.read_text(encoding="utf-8"))

    @property
    def approved_ids(self) -> frozenset[str]:
        """Return every approved public hook id, including the policy validator."""
        upstream_ids = (item for upstream in self.upstreams for item in upstream.approved_ids)
        return frozenset({"validate-registry-config", *upstream_ids})
