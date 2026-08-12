# Supply-chain security

This document defines the project’s supply-chain control objectives. It describes alignment with
widely used guidance; it is not a claim of third-party certification.

## Dependency acceptance

- Every dependency and GitHub Action is immutable: package versions are exact, Git sources use full
  commit SHAs, Actions use full commit SHAs, and ecosystem checksums are committed.
- The registered Node mechanism uses only the repository package manifest and committed npm lockfile;
  lifecycle scripts and consumer-supplied additional dependencies are not part of the hook contract.
- Ordinary updates wait at least 14 full days after publication. A security update may bypass the
  cooling period only when its review record identifies the advisory, urgency, and compensating
  verification.
- The newest stable, supported release that has cleared those controls is preferred. Mutable
  `latest` references, branches, and floating major-version Action tags are prohibited.
- Dependabot discovers candidates but never merges them. Acceptance requires reconciliation of the
  authoritative source, adapter, lockfiles, review evidence, generated documentation, and tests.
- Upstream tag-to-commit resolution, Action SHA pinning, manifest/catalog parity, lock integrity,
  installed-hook behavior, and platform compatibility are enforced in CI.

## Build and release controls

- Workflows default to read-only permissions and grant narrower write permissions only to the
  Release Please and publication jobs that need them. Release Please uses the workflow-scoped token,
  is prohibited from creating tags or releases, and requires maintainer approval before CI runs on
  its pull requests.
- Third-party Actions are limited to verified creators; all Actions are SHA pinned.
- Release tags and commits are SSH signed. Releases are built by CI from protected `main`, include a
  material manifest and digests, and receive GitHub OIDC-backed artifact attestations.
- No upstream repository or executable artifact is vendored. Package indexes, GitHub, runner images,
  and language toolchains remain explicit trust dependencies documented in the threat model.

## Standards alignment

| Guidance | Project controls |
| --- | --- |
| NIST SSDF | Reviewed dependencies, protected changes, least privilege, provenance, vulnerability reporting, and repeatable verification |
| SLSA | Version-controlled build definition, isolated GitHub-hosted builders, immutable inputs, artifact digests, and signed provenance attestations |
| OpenSSF Scorecard practices | Pinned dependencies, token permissions, branch protection, code review, signed releases, security policy, and dependency updates |
| OpenSSF Best Practices | Public license, contribution/security processes, automated testing, warnings-as-failures, and documented security assumptions |

The authoritative locations for each control are listed in the maintenance guide. Review this file
when a new ecosystem, build service, package registry, or release channel enters the trust boundary.
