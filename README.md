# Pre-commit Hook Registry

A public gateway for a small, reviewed set of pre-commit hooks. Consumer repositories use one
registry URL, pin a complete registry commit SHA, and opt into the hooks they need.

## Use the registry

Start with a tested template:

- [`consumer-examples/minimal.yaml`](consumer-examples/minimal.yaml)
- [`consumer-examples/python.yaml`](consumer-examples/python.yaml)
- [`consumer-examples/security.yaml`](consumer-examples/security.yaml)

Replace `<FULL_RELEASE_COMMIT_SHA>` with the commit behind a published release. Pin the commit, not
the release tag. Run policy validation with:

```bash
pre-commit-hook-registry validate
```

An alternate configuration path may be supplied as the final argument.

## Understand and maintain the project

- [Catalog reference](docs/catalog.md) lists the generated, reviewed hook inventory.
- [Threat model](docs/THREAT_MODEL.md) explains what a registry pin does and does not protect.
- [Supply-chain security](docs/SUPPLY_CHAIN.md) defines dependency and provenance controls.
- [Maintenance guide](docs/MAINTENANCE.md) identifies every authoritative source and update flow.
- [GitHub settings](docs/GITHUB_SETTINGS.md) records repository protections that live outside Git.
- [Contributing](CONTRIBUTING.md) describes the contribution entry point.
- [Security policy](SECURITY.md) explains private vulnerability reporting.

Local verification starts with `uv sync --all-groups --locked`, followed by `make check`.
