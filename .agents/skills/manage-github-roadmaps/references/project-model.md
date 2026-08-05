# Project model

Use this model as a starting point, then simplify or extend it from repository evidence.

## Fields

Prefer single-select fields with stable, small option sets:

| Field | Suggested options | Purpose |
| --- | --- | --- |
| Status | Backlog, Ready, In progress, In review, Blocked, Done | Workflow state |
| Priority | P0, P1, P2, P3 | Relative urgency |
| Area | Repository-specific capability or ecosystem areas | Ownership and filtering |
| Work type | Epic, Feature, Security, Research, Maintenance | Work shape |
| Target release | Unscheduled, next release, Future | Release intent |
| Risk | Low, Medium, High | Trust and delivery risk |
| Effort | XS, S, M, L, XL | Relative size |

Keep built-in Title, Assignees, Labels, Milestone, Parent issue, and Sub-issues progress fields. Do not duplicate every Project field as a label.

## Status contract

- **Backlog:** valuable but not ready to start.
- **Ready:** outcome and acceptance criteria are testable; dependencies and material decisions are resolved.
- **In progress:** active work exists and has an owner.
- **In review:** a decision record or pull request is under review.
- **Blocked:** progress requires an external decision, dependency, authorization, or state change.
- **Done:** acceptance criteria and required evidence are complete.

## Labels

Reuse existing labels. Add only labels that remain useful outside the Project, normally:

- a small `type:*` set;
- durable `area:*` labels;
- `priority:p0` through `priority:p3` only when issue-list triage needs them;
- exceptional workflow flags such as `blocked` or `cooling-period`.

Avoid status, effort, risk, and release labels when Project fields cover them.

## Milestones

Create a milestone only for a coherent committed release outcome. Do not add Future or merely investigative ecosystems to the next-release milestone. A milestone should not copy the full Project backlog.

## Views

Start with three or four views:

1. **Delivery board:** board filtered to the next target release and grouped by Status.
2. **Roadmap:** table grouped by Target release, with Status, Priority, Area, Risk, and Effort visible.
3. **Research backlog:** table filtered to Work type = Research, grouped by Area, sorted by Priority.
4. **Epics:** table filtered to Work type = Epic, showing Target release and Sub-issues progress.

Avoid one view per ecosystem until item volume justifies it. Record any grouping or sorting that requires manual UI configuration.

## Scope selection

Prefer the smallest release that produces a coherent consumer outcome. Rank candidates using:

- consumer value;
- reuse of existing toolchains and controls;
- number and quality of new upstream trust relationships;
- package registries and runtimes introduced;
- adapter complexity;
- platform test burden;
- performance at commit versus push/manual stages;
- maintainer and release health;
- documentation and example burden.

Research is a valid release deliverable only when it resolves a blocking decision and produces independently actionable follow-up criteria.
