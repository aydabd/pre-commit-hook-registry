---
name: manage-github-roadmaps
description: Audit, design, create, repair, and govern GitHub Projects roadmaps using Projects v2, issues, parent/sub-issues, labels, milestones, fields, and views. Use when Codex or Copilot must move planning out of repository Markdown, establish a roadmap for a repository, normalize an existing project, create high-quality epics and research or implementation issues, configure readable views, recommend release scope, or report roadmap health without duplicating transient status in source files.
---

# Manage GitHub roadmaps

Treat GitHub Projects as the operational roadmap and GitHub issues as the actionable requirements. Keep repository Markdown limited to durable policies, specifications, architecture, maintenance procedures, and source-of-truth declarations.

Read repository instructions and referenced governance documents completely before inspecting or changing live GitHub state.

## Select the operating mode

- For audit, explanation, or recommendation requests, remain read-only.
- For creation or repair requests, audit and present the proposed structure before mutating GitHub.
- For implementation requests, first require a coherent project and a Ready issue with testable acceptance criteria.
- Never infer permission to change repository security settings, publish releases, move tags, merge pull requests, or implement roadmap items.

## Execute the workflow

1. Resolve the repository, owner, default branch, local checkout, and applicable instruction files.
2. Inventory live Projects, issues, parent/sub-issues, labels, milestones, views, discussions, pull requests, releases, permissions, and authentication scopes.
3. Identify duplicates, reusable objects, stale planning documents, missing source-of-truth boundaries, and authorization gaps.
4. Read [project-model.md](references/project-model.md) to design the fields, minimal labels, milestone use, views, and release scope.
5. Read [issue-design.md](references/issue-design.md) before drafting or reviewing epics, research issues, or admission issues.
6. Present the proposed project, hierarchy, labels, milestones, views, initial release scope, and first Ready issue. State assumptions and unresolved material decisions.
7. Proceed only when the user authorized creation and no material product decision or permission gap remains.
8. Create or update objects idempotently: re-query immediately before writes, reuse matching objects, and retain returned node IDs and URLs.
9. Establish real parent/sub-issue relationships; do not simulate hierarchy only with task-list links.
10. Add issues to the Project and populate every field needed for triage. Leave unknown values explicit rather than invented.
11. Configure views through supported tools. Read [github-operations.md](references/github-operations.md) when Projects v2 fields, items, or views require GraphQL.
12. Verify live state after writes, including field options, filters, hierarchy, milestone membership, item counts, visibility, and repository linkage.
13. Report what existed, what changed, links, release scope, blockers, research questions, and the recommended first Ready issue.

## Apply safety gates

- Prefer the GitHub connector for supported issue operations and `gh`/GraphQL for Projects v2 gaps.
- Verify token scopes before mutation. Request the narrow missing permission and provide the exact command; never request a broader token without necessity.
- Treat view filters, field option names, issue titles, and milestone titles as identifiers that require exact matching.
- Batch GraphQL conservatively. Retry idempotent updates in smaller batches after resource-limit errors.
- Keep release milestones limited to committed scope. Use a Project target-release field for broader planning.
- Do not create many speculative implementation issues. Start with epics and focused research/admission issues when suitability is unresolved.
- Do not create ROADMAP.md, TODO.md, or issue-status mirrors.
- Preserve unrelated local and live GitHub state.

## Require a usable handoff

End with:

- the audited live state;
- the Project and milestone links;
- created or updated issues grouped by epic;
- the prioritized release scope and rationale;
- blockers, permissions, and research questions;
- the first issue recommended for Ready;
- any Project-view settings that the API could not configure.

Do not call the roadmap complete until another human or agent can select the Ready issue and understand its outcome, boundaries, dependencies, risks, tests, and completion evidence without consulting private context.
