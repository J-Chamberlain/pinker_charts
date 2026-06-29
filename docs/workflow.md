# Workflow

## Start Of Work

1. Read [../PROJECT_STATE.md](../PROJECT_STATE.md).
2. Read [figure registry documentation](figure_registry.md).
3. Check [the figure registry](../data/figure_registry.csv) before selecting
   or continuing figure work.
4. Read the relevant figure directory.
5. Check [figure metadata](../data/metadata/figure_metadata.csv) for canonical
   status.
6. Inspect the source log before running new searches.
7. Confirm whether the task is architecture, research, reconstruction, or
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

## Iterative QA Loop

Codex must not stop after producing a side-by-side comparison if visible
discrepancies remain that could plausibly be addressed through additional source
recovery, transformation correction, styling correction, scaling correction, or
extension-data review.

After each side-by-side comparison, perform a self-review:

1. What visibly differs from the original?
2. Is the discrepancy due to missing data, wrong data, styling, scaling,
   source-version change, or post-publication extension?
3. Can the issue be addressed automatically?
4. If yes, continue iterating.
5. If no, document why not and classify the unresolved issue.

Codex may stop only when one of the following is true:

- The figure is visually and evidentially satisfactory.
- Remaining discrepancies are explained in the caption and anomaly review.
- The source search space has been exhaustively documented.
- Manual input is genuinely required.

Codex should not stop merely because it found a plausible source or generated a
plot.

## Visual QA Responses

Whenever Codex updates or reviews a figure, the final response must render the
latest side-by-side comparison images inline, including both book-period and
extended comparisons where available. Use the canonical repository-relative
paths listed in [../PROJECT_STATE.md](../PROJECT_STATE.md) to identify the
images. GitHub remains the canonical archive, but inline rendered images are
required so ChatGPT can perform visual QA from the response.

Every future Codex figure run must include:

- Updated registry rows.
- Updated `PROJECT_STATE.md`.
- Rendered book-period side-by-side images.
- Rendered extended side-by-side images where available.
- A short self-review of visible discrepancies.
- What Codex did to address the discrepancies.
- What remains unresolved.

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
