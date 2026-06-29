# Workflow

## Start Of Work

1. Read [../PROJECT_STATE.md](../PROJECT_STATE.md).
2. Read the relevant figure directory.
3. Check [figure metadata](../data/metadata/figure_metadata.csv) for canonical
   status.
4. Inspect the source log before running new searches.
5. Confirm whether the task is architecture, research, reconstruction, or
   publication packaging.

## Figure Directory Contract

Each figure directory is an independent review package:

- `metadata/metadata.json`: detailed figure-level status.
- `provenance/provenance.md`: current source and reconstruction narrative.
- `source_logs/source_log.md`: source discovery and acceptance/rejection log.
- `search_iterations/search_iterations.md`: chronological search record.
- `discrepancy_logs/discrepancy_log.md`: unresolved mismatches.
- `anomaly_reviews/anomaly_review.md`: visual caveats.
- `captions/caption.txt`: publication-facing caption draft.
- `lineage/`: machine-readable data lineage.
- `plots/`: book-period, extended, comparison, and diagnostic images.
- `data/`: raw, clean, and candidate data files.
- `checksums/`: SHA-256 checksums for audit.

## Status Update Rules

When changing a figure status, update all of the following:

- Per-figure `metadata/metadata.json`.
- [../data/metadata/figure_metadata.csv](../data/metadata/figure_metadata.csv).
- [../PROJECT_STATE.md](../PROJECT_STATE.md).
- The relevant provenance and discrepancy logs.

Do not promote a figure to `verified_reproduction` unless the source chain and
visual validation both support that classification.

## Commit Practice

Use logical commits:

1. Import or reorganize artifacts.
2. Add or update documentation.
3. Update metadata/state.
4. Add reproducibility or validation tooling.

Avoid mixing new figure reconstruction with repository maintenance.

## Fresh-Contributor Review

Before finishing a repository architecture task, ask:

Could another researcher understand the project, reproduce the figures, and
continue work without reading the chat history?

If the answer is no, improve the repository before stopping.
