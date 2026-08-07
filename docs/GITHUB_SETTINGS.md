# GitHub repository settings

This file is the authoritative declaration of protections that cannot be stored directly in the
repository. Check these settings after initial publication and periodically thereafter.

## Repository

- Public visibility and `main` as the default branch.
- Features enabled only when actively used; vulnerability reporting remains private.
- Dependabot alerts and security updates enabled.
- Secret scanning and push protection enabled.
- Releases immutable.
- Repository auto-merge disabled.
- GitHub Actions may create pull requests so Release Please can maintain the release candidate.
  The repository-level capability for Actions to approve pull requests remains enabled, but no
  repository workflow approves or merges pull requests. Release Please does neither. CI runs created
  for its pull requests remain blocked until a maintainer reviews the changes and approves the
  workflows to run.

## Branch and tag rules

Protect `main` with required pull requests, one approval, code-owner review, last-push approval,
required CI, signed commits, linear history, resolved conversations, squash-only merging, and blocks
on force-push and deletion. The repository-role bypass remains available for sole-maintainer
continuity; ordinary changes, including dependency updates, still use the reviewed pull-request flow
and require a manual maintainer merge.

Protect release tags from updates and deletion. Releases must originate from the signed-tag workflow
defined in `.github/workflows/release.yaml`.
