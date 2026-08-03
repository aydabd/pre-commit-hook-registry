# Threat model and trust boundaries

The registry defends consumers from mutable revisions, unreviewed hook repositories and IDs,
dangerous hook overrides, accidental duplicate YAML keys, and unnoticed divergence between the
public manifest and reviewed catalog. A registry commit SHA does not protect against a compromised
Git host, package index, developer workstation, toolchain, or consumer-local Ruff/Gitleaks config.

Upstream source and dependency pins, lock verification, cooling periods, manual review, protected
branches/tags, signed changes, and release attestations provide layered controls. Secrets must not
be included in fixtures; Gitleaks integration data uses an obvious synthetic test value and redacted
output. Windows and unreviewed ecosystems are outside v1 support.
