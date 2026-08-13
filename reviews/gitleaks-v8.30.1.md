# Review: Gitleaks v8.30.1

- Upstream: `https://github.com/gitleaks/gitleaks`
- Tag resolution: `v8.30.1` → `83d9cd684c87d95d656c1458ef04895a7f1cbd8e`
- Release/cooling period: passed before initial selection
- License: MIT
- Security advisories: reviewed; no blocking advisory identified at review time
- Upstream diff: reviewed for the CLI and pre-commit definition
- Manifest deviations: installed through pre-commit Go support at the full Git SHA using the
  upstream module's historical `github.com/zricethezav/gitleaks/v8` identity; the reviewed source
  remains `github.com/gitleaks/gitleaks`. Go toolchain 1.26.5,
  `git --pre-commit --redact --staged --verbose`, and no filename passing are preserved.
- Tests: redacted synthetic-secret and clean-repository execution required by the release gate
- Reviewer: aydabd
- Review date: 2026-08-03
- Disposition: Reviewed adapter
- Integration: pre-commit's isolated Go dependency mechanism
- Decision: accepted for v0.1.0
