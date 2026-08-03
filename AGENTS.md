# Repository guide

This file is the entry point for automated agents and human maintainers. Read
[`docs/MAINTENANCE.md`](docs/MAINTENANCE.md) before changing policy, dependencies, generated files,
or release automation.

## Working rules

- Preserve the source-of-truth boundaries documented in `docs/MAINTENANCE.md`; reference an
  authoritative file instead of copying its values or instructions elsewhere.
- Treat upstream changes as security reviews, not routine version bumps. Follow
  [`docs/REVIEW_CHECKLIST.md`](docs/REVIEW_CHECKLIST.md).
- Keep changes focused, retain unrelated work, and use signed commits.
- Run `make check` before publishing. If a required platform tool is unavailable, run every
  available check and state exactly what remains for CI.
- Do not publish a release or change GitHub security settings unless explicitly requested.

There are no repository-specific agent skills. Tool-specific operating instructions belong to the
tooling environment, not this repository.
