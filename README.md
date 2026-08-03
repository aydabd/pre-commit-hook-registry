# Pre-commit Hook Registry

A public, curated hook gateway maintained by `@aydabd`. Consumers reference only this repository,
pin its complete 40-character commit SHA, and opt into reviewed hook IDs.

```yaml
repos:
  - repo: https://github.com/aydabd/pre-commit-hook-registry
    rev: <FULL_RELEASE_COMMIT_SHA>
    hooks:
      - id: validate-registry-config
      - id: check-yaml
      - id: trailing-whitespace
```

The validator runs as `pre-commit-hook-registry validate [CONFIG]`; `CONFIG` defaults to
`.pre-commit-config.yaml`. The canonical catalog is packaged with the validator and cannot be
replaced by a consumer.

## Trust boundary

A registry commit pin makes the registry manifest, adapter definitions, source pins, and review
records immutable. Python and Go package infrastructure remains part of the installation trust
path; this project does not vendor upstream repositories or binaries. Consumer-local Ruff and
Gitleaks configuration is intentionally outside registry policy. See [the threat model](docs/THREAT_MODEL.md).

## Local verification

```bash
uv sync --all-groups --locked
make check
```

See [the generated catalog](docs/catalog.md), [contribution process](CONTRIBUTING.md), and
[security policy](SECURITY.md). Consumers pin a release's commit SHA, never its tag.
