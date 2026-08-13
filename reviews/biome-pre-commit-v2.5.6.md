# Review: biomejs/pre-commit v2.5.6

- Upstream: `https://github.com/biomejs/pre-commit`
- Tag resolution: `v2.5.6` annotated tag `d1ce4972fb5ad09afd33b432bca71e8c5dfbb2b5` → peeled commit `cd5d6ed44598e228e214b704d673541d9675f8e4`
- Tag signature: the inspected annotated tag is unsigned. Admission relies on the independently resolved full commit SHA, exact npm versions, committed npm lockfile, and SHA-512 package integrity; a signed upstream tag is not claimed.
- Release/cooling period: published 2026-07-28; review date 2026-08-12; 15 full days elapsed.
- Ownership/release health: Biome maintains the upstream hook and the `@biomejs/biome` package in the Biome organization; v2.5.6 is the exact release selected for this admission. Newer releases require a new review.
- License: upstream hook MIT; Biome runtime and platform packages are `MIT OR Apache-2.0`; both are compatible with this Apache-2.0 registry.
- Security advisories: npm/GitHub advisory review at admission time found no applicable blocking advisory for the exact package graph. Recheck on every update.
- Package provenance/integrity: `@biomejs/biome@2.5.6` and its platform optional dependencies are exact in `package-lock.json`; the lock records registry tarball URLs and SHA-512 integrity. Linux x64 and macOS arm64 are the exercised platform packages; all lock entries are checked for exact version and integrity.
- Configuration/plugins: Biome discovers consumer-owned `biome.json`/`biome.jsonc`; no external plugin is installed or resolved. Consumer configuration and local GritQL plugin files remain consumer trust inputs.
- Cache/network: npm installation occurs only during pre-commit environment preparation through its cache boundary; the checked-in `.npmrc` sets `ignore-scripts=true`, and the lock/install test verifies lifecycle scripts are disabled. Hook execution uses the installed binary, is tested with network disabled, and performs no package-manager, installer, daemon, migration, upgrade, or download operation.
- Upstream comparison: `biome-ci` is reproduced exactly as `biome ci --files-ignore-unknown=true --no-errors-on-unmatched`, `types: [text]`, the upstream filename filter, and `require_serial: true`. The writing `biome-check`, `biome-format`, and `biome-lint` hooks are deliberately not exported. The only integration difference is acquisition through this repository's checked-in Node package manifest and lock.
- Tests/evidence: installed clean/failing fixtures, config discovery, filenames with spaces, ignored/unmatched files, malformed configuration, corrupted package failure, no-write assertions, network isolation, and cold/five-warm performance evidence are covered by the admission test suite and PR report. CI claims only Linux/macOS and Node 22/24 after the complete matrix passes.
- Reviewer: aydabd
- Review date: 2026-08-12
- Disposition: Proxy upstream
- Integration: exact reviewed hook definition with a lock-backed Node package environment
- Decision: accepted only after all issue #36 gates and required CI pass
