# Maintenance guide

This is the authoritative map of repository data and maintenance workflows. `AGENTS.md`, the
contribution guide, and the README link here rather than restating these instructions.

## Sources of truth

| Concern | Authoritative source | Derived or supporting files |
| --- | --- | --- |
| Registry identity, required hooks, upstream pins, licenses, adapters, and review paths | `src/pre_commit_hook_registry/catalog.yaml` | `docs/catalog.md` |
| Executable hook behavior | `.pre-commit-hooks.yaml` | Manifest drift tests |
| Consumer policy | `src/pre_commit_hook_registry/validator.py` | Consumer examples and policy tests |
| Python dependencies and supported Python versions | `pyproject.toml` and `uv.lock` | CI matrices |
| Go toolchain and module integrity | `go.mod` and `go.sum` | CI setup |
| Upstream update discovery | `upstream/.pre-commit-config.yaml` and `.github/dependabot.yml` | Dependabot pull requests |
| Upstream acceptance evidence | `reviews/*.md` | Generated catalog links |
| Review procedure | `docs/REVIEW_CHECKLIST.md` | Individual review records |
| Security reporting | `SECURITY.md` | GitHub security settings |
| Trust boundaries | `docs/THREAT_MODEL.md` | README link |
| Supply-chain control objectives | `docs/SUPPLY_CHAIN.md` | CI and repository settings |
| GitHub repository protections | `docs/GITHUB_SETTINGS.md` | GitHub settings |
| Release preparation, contents, and provenance | `release-please-config.json`, `.release-please-manifest.json`, `.github/workflows/release-please.yaml`, `.github/workflows/release.yaml`, and `scripts/release_manifest.py` | Release pull requests and artifacts |

Values may appear in executable integration points where a tool cannot consume the authoritative
source directly. Drift tests or CI checks must cover those copies. Prose documentation should link
to the source instead of repeating values.

Runtime and automation pins follow the acceptance policy in `docs/SUPPLY_CHAIN.md`.

## Routine change flow

1. Identify the authoritative source in the table above.
2. Change that source and the smallest necessary executable integration points.
3. For upstream changes, complete the review checklist and add a review record before acceptance.
4. Regenerate the catalog reference with `make docs`.
5. Reconcile locks with the package manager; never edit lockfile checksums manually.
6. Run `make check` and inspect the diff for unexpected generated changes.
7. Commit with SSH signing and publish through a pull request after the initial repository bootstrap.

## Release flow

Release Please maintains the version and changelog through a release pull request. Its workflow is
configured to skip GitHub release creation so that it cannot bypass the repository's signed-tag
gate. Review each automation-created release pull request before approving its CI workflows. After
the release pull request is squash-merged and all required checks pass on `main`, run
`make release VERSION=X.Y.Z`. The command requires a clean, current `main`, reconciles the package,
manifest, and changelog versions, repeats `make check`, then creates, verifies, and pushes the
SSH-signed annotated tag. The tag-triggered release workflow verifies that the tag targets protected
`main`, repeats `make check`, builds the artifacts and material manifest, attests their provenance,
and publishes the immutable GitHub release.

## Generated documentation

`docs/catalog.md` is generated from the packaged catalog. Do not edit it by hand. CI verifies that
it is current. Consumer examples are maintained as executable templates and tested after replacing
their release-SHA placeholder.
