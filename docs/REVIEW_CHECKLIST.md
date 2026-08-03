# Upstream review checklist

- Resolve the release tag independently to a full commit SHA.
- Confirm the release has passed the 14-day cooling period (security fixes may be expedited).
- Verify license compatibility and security-advisory status.
- Review the diff from the previously accepted release.
- Compare upstream hook definitions with the adapter and record every deviation.
- Reconcile catalog, runtime dependencies, lockfiles, watchlist, tests, and generated docs.
- Run Linux and macOS installed-hook tests; record reviewer and date.
- Block the candidate when any required check fails.
