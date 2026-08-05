# GitHub repository settings

This file is the authoritative declaration of protections that cannot be stored directly in the
repository. Check these settings after initial publication and periodically thereafter.

## Repository

- Public visibility and `main` as the default branch.
- Features enabled only when actively used; vulnerability reporting remains private.
- Dependabot alerts and security updates enabled.
- Secret scanning and push protection enabled.
- Releases immutable.
- GitHub Actions may create pull requests so Release Please can maintain the release candidate.
  Release Please does not approve pull requests. CI runs created for its pull requests remain
  blocked until a maintainer reviews the changes and approves the workflows to run.

## Branch and tag rules

Protect `main` with required pull requests, required CI, signed commits, linear history, resolved
conversations, and blocks on force-push and deletion. A sole-maintainer repository uses no mandatory
approval count, avoiding deadlock on owner-authored changes. Dependency updates still require a
manual maintainer merge.

Protect release tags from updates and deletion. Releases must originate from the signed-tag workflow
defined in `.github/workflows/release.yaml`.
