# Hook admission and adapter contract

This document is the authoritative decision contract for placing a candidate hook in this registry.
The catalog records only admitted upstreams; research evidence and rejected candidates remain in GitHub
issues, while acceptance evidence belongs in `reviews/*.md`.

## Required evidence

Before choosing a disposition, record the candidate's maintained upstream and release health, license,
advisory status, immutable version source, dependency acquisition, configuration and plugin loading,
file and working-directory behavior, caches, network and subprocess behavior, supported toolchains and
platforms, update owner, and measured runtime. Admission also requires every gate in
[`REVIEW_CHECKLIST.md`](REVIEW_CHECKLIST.md) and the controls in
[`SUPPLY_CHAIN.md`](SUPPLY_CHAIN.md).

Linux and macOS support may be claimed only after an installed-hook test passes on each claimed platform
using both a clean fixture and a fixture that must fail. Platform-specific behavior must be documented or
the narrower platform set must be stated. Windows is not admitted by this contract.

## Dispositions

Evaluate the following outcomes in order. A candidate exits an outcome as soon as any required criterion
cannot be met.

| Disposition | Entry criteria | Required result | Exit criteria |
| --- | --- | --- | --- |
| Proxy upstream | The upstream publishes a maintained pre-commit hook whose reviewed definition, immutable revision, dependency model, and claimed platforms satisfy repository policy without a semantic change. | Add the upstream to the catalog and faithfully reproduce the selected definition in this registry's manifest, changing only the immutable acquisition path needed to install the reviewed revision. Record and test that integration detail. | Use a reviewed adapter if entry, arguments, file passing, types, stages, isolation, or other behavior must change; exclude if the revision cannot be pinned and tested. |
| Reviewed adapter | The tool is suitable, but the upstream pre-commit integration is absent or requires a bounded change. The adapter can use one registered mechanism, preserve the tool's intended semantics, and improve reproducibility or safety. | Add the upstream and adapter mechanism to the catalog, reproduce the reviewed behavior in the manifest, record every deviation, and test catalog/manifest parity plus installed behavior. | Use a consumer-local/system hook if isolation cannot safely represent the project environment; exclude if the adapter needs prohibited behavior. |
| Consumer-local/system hook | Correct execution depends on a consumer-owned toolchain, build graph, credentials, platform facility, or configuration that the registry cannot isolate or pin without changing semantics. | Keep it out of the catalog and manifest. Publish tested guidance only when the executable, version/checksum verification, arguments, stages, and ownership boundary are explicit. | Re-evaluate for proxy or adapter only after a maintained, immutable, isolatable integration exists; exclude if safe bounded guidance is impossible. |
| Exclude | The candidate is redundant, unmaintained, unverifiable, license-incompatible, unsafe by default, outside supported platforms, or unable to meet the evidence, performance, or test gates. | Do not expose or recommend it. Record the reason and the condition, if any, that would permit reconsideration. | Re-enter research only when objective evidence changes the recorded exclusion condition. |

A proxy preserves the reviewed upstream hook's semantics while presenting it through this registry. An
adapter changes or supplies integration behavior and is admitted only when that change provides a security
or reproducibility property that faithful proxying cannot. A system hook is never presented as registry-
managed or isolated.

## Adapter invariants

Registered adapter mechanisms are enforced by the catalog model. An adapter must:

- acquire only immutable, reviewed dependencies through the declared pre-commit language environment;
- run the reviewed executable directly without a shell, installer, bootstrap download, or mutable lookup;
- preserve reviewed file passing, working directory, stages, types, arguments, and serial execution unless
  the acceptance record explains and tests a deviation;
- avoid implicit network access after environment installation and never request consumer credentials;
- keep caches within the tool or pre-commit's documented cache boundary and never share mutable build
  outputs with the consumer project by default;
- fail closed when a pin, checksum, configuration, platform, or required executable is invalid; and
- reconcile the catalog, public manifest, lockfiles, generated catalog, review record, and installed-hook
  tests in one reviewed change.

The currently registered mechanisms are `python-git-dependency`, `python-package`,
`golang-additional-dependency`, and `node-package`. The Node mechanism uses the repository's exact
`package.json` plus committed `package-lock.json`; it installs only the lock-declared graph during
pre-commit environment preparation, with no consumer `additional_dependencies` and no lifecycle
script or package-manager activity during hook execution. Adding a mechanism is an architecture change: update this contract, the
catalog model, threat analysis when its boundary changes, and tests before using it.

## Stage and performance classification

Measure a cold run and five warm runs on a representative smallest supported project and a documented
larger fixture. Record the runner operating system, CPU architecture, tool and toolchain versions, fixture
size, cache state, network state, command, and wall-clock results. Use the slowest warm run for the stage
decision; a timeout or network requirement fails that stage.

| Default stage | Measured budget and execution boundary |
| --- | --- |
| Commit | No network or credential access; file-local or bounded deterministic work; cold run at most 5 seconds and every warm run at most 2 seconds. |
| Push | No credentials unless the consumer explicitly owns the integration; repository-wide work; cold run at most 60 seconds and every warm run at most 30 seconds. |
| Manual | Work exceeding the push budget, requiring intentionally enabled network access, executing project build/test code, or performing broad security analysis. Document a finite timeout and side effects. |

Hooks may be assigned to a later stage than their measurements require. They may not be assigned earlier.
An adapter admission issue must name its fixtures and installed-hook tests so another reviewer can reproduce
the compatibility and performance evidence without private context.

## Applied examples

- `pre-commit-hooks` is a proxy: this registry faithfully reproduces selected upstream definitions and
  installs their implementation from the reviewed full SHA using `python-git-dependency`. The acquisition
  path is an integration detail, while entries, filename handling, types, and stages retain upstream
  semantics.
- `ruff-pre-commit` is a reviewed adapter: the manifest installs the exact `ruff` package instead of the
  wrapper repository while preserving reviewed entries, types, exclusion behavior, and serial execution.
  The acceptance record and installed tests must continue to cover those deviations.
- `go vet` resolves to consumer-local/system guidance under this framework, not registry admission. The
  official command analyzes named packages through the consumer's `go` command, and the consumer's
  `go.mod` controls the module graph and minimum toolchain. A registry-isolated Go hook would therefore
  replace or decouple the project-owned execution environment rather than reproduce it. Any future
  guidance must use a repository-local hook, require `pass_filenames: false`, pin the consumer's Go
  toolchain, disable automatic toolchain and network acquisition, name the package pattern, and measure
  the project before assigning push or manual stage. See the official [`go vet`](https://pkg.go.dev/cmd/vet),
  [`go.mod`](https://go.dev/doc/modules/gomod-ref), and
  [repository-local hook](https://pre-commit.com/#repository-local-hooks) documentation.

These examples validate three different branches of the framework; they do not grandfather future
versions or admit `go vet` to the registry.
