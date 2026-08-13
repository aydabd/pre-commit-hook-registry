# Review: ruff-pre-commit v0.15.22

- Upstream: `https://github.com/astral-sh/ruff-pre-commit`
- Tag resolution: `v0.15.22` → `2700fd5671c633760d912769c041bfcde2b9a01b`
- Release/cooling period: passed; v0.16.0 deferred due to breaking default-rule changes
- License: MIT
- Security advisories: reviewed; no blocking advisory identified at review time
- Upstream diff: reviewed for both exported hooks
- Manifest deviations: install exact `ruff==0.15.22` rather than the wrapper repository; entries,
  types, forced exclusion, and serial execution are preserved
- Tests: check, fix, formatting, policy-safe arguments, and manifest parity required by release gate
- Reviewer: aydabd
- Review date: 2026-08-03
- Disposition: Reviewed adapter
- Integration: exact Python package instead of the wrapper repository
- Decision: accepted for v0.1.0
