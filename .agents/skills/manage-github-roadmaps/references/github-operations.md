# GitHub operations

## Authentication

Start with `gh auth status`. Projects v2 writes require the `project` OAuth scope. For a stored GitHub CLI credential, request only the missing scope:

```shell
gh auth refresh -h github.com -s project
```

If `GH_TOKEN` overrides the stored credential, either supply a token with the required permissions or deliberately run the relevant command with `env -u GH_TOKEN`. Never print a token.

Fine-grained tokens need repository Issues write access and account or organization Projects write access appropriate to the Project owner.

## Tool routing

- Use the GitHub connector for repository, issue, label, comment, and pull-request operations it supports.
- Use `gh project` for project, field, item, link, and visibility operations it supports.
- Use `gh api graphql` for parent/sub-issues and Projects v2 view operations absent from the CLI.
- Re-query node IDs immediately before GraphQL mutations.

## Read-only inventory

Inventory both repository objects and owner-level Projects. At minimum inspect:

- repository metadata, permissions, features, and default branch;
- all issues and pull requests;
- labels and milestones;
- releases and tags;
- rulesets or branch/tag protection;
- discussions;
- owner Projects, fields, views, repository links, and items;
- authenticated identity and scopes.

Treat an inaccessible endpoint as unknown, not empty.

## Mutation order

1. Create or reuse the Project.
2. Link it to the repository and set intended visibility.
3. Configure fields and exact options.
4. Create minimal labels and any committed-release milestone.
5. Create epics, then child issues.
6. Add real sub-issue relationships.
7. Add issues to the Project and populate fields.
8. Create and filter views.
9. Verify all live state.

GitHub's built-in Status field cannot be deleted. Update its single-select options through `updateProjectV2Field` when the CLI cannot configure it.

## Views

The GraphQL schema may expose `createProjectV2View` and `updateProjectV2View` before `gh project` exposes equivalent commands. Discover the live schema rather than assuming support. View mutations commonly support:

- name;
- `TABLE_LAYOUT`, `BOARD_LAYOUT`, or `ROADMAP_LAYOUT`;
- filter text;
- visible field IDs.

Grouping and sorting may remain UI-only. If so, create the view, layout, filter, and columns through the API, then report exact manual group/sort steps.

## Reliability

- Use exact owner, repository, Project number, issue number, node ID, field ID, and option ID values returned by GitHub.
- Make retries idempotent and re-inventory after partial failure.
- Split large aliased GraphQL mutations when GitHub reports resource-limit errors.
- Confirm item counts, field values, hierarchy, view filters, milestone membership, and links after writes.
- Never treat a successful HTTP response as sufficient verification of the final roadmap.
