# Issue design

## Epic requirements

Every epic must state:

- user outcome and golden-path goal;
- supported project and toolchain boundaries;
- security and trust boundaries;
- commit versus push/manual performance expectations;
- compatibility targets;
- upstream ownership and maintenance health;
- candidates and alternatives;
- dependency and execution model;
- acceptance criteria;
- documentation and consumer-example requirements;
- test requirements;
- explicit non-goals.

Create one epic per ecosystem or major capability. Use real sub-issues for independently reviewable work.

## Research issue requirements

State the decision question, candidates, evidence to collect, comparison criteria, output format, acceptance criteria, and what implementation must wait for the conclusion. Require an explicit disposition for each candidate:

- proxy an existing upstream integration;
- expose a reviewed adapter;
- document a consumer-local/system integration;
- exclude it with a reason.

Research conclusions belong in the issue unless they establish a durable architecture, policy, security boundary, or maintenance rule that must become authoritative in the repository.

## Admission issue requirements

Adapt these gates to repository policy without weakening stricter local requirements:

- complete the authoritative review checklist;
- add a dedicated acceptance record;
- use immutable full-SHA or checksum-backed pins;
- independently resolve release tags to commits;
- review license and advisory status;
- review maintainer ownership and release health;
- review threat and execution model;
- satisfy the repository cooling period;
- add representative installed-hook or end-to-end tests;
- test every claimed platform;
- reconcile catalogs, manifests, dependencies, locks, watchlists, tests, and generated artifacts;
- achieve zero-warning CI and run the repository's full check command;
- use the protected feature-branch, signed-commit, reviewed-PR, resolved-comment, and merge process.

## Ready checklist

Move an issue to Ready only when:

- its outcome is observable;
- acceptance criteria are binary or demonstrably testable;
- scope and non-goals are explicit;
- dependencies and parent relationship are correct;
- risk and execution boundaries are understood;
- required evidence and tests are named;
- no material product decision remains hidden in implementation;
- the issue can be completed without copying transient roadmap state into repository documentation.
