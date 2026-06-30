# Workflow

## Start Of Work

1. Read [../PROJECT_STATE.md](../PROJECT_STATE.md).
2. Open the canonical
   [Supplemental Graphics PDF](../references/enlightenment_now_supplemental_graphics.pdf).
3. Read [figure registry documentation](figure_registry.md).
4. Check [the figure registry](../data/figure_registry.csv) before selecting
   or continuing figure work.
5. Read the [review protocol](review_protocol.md) and
   [review checklist](review_checklist.md).
6. Read the [editorial review gate](editorial_review_gate.md).
7. Read the relevant figure directory.
8. Check [figure metadata](../data/metadata/figure_metadata.csv) for canonical
   status.
9. Inspect the source log before running new searches.
10. Confirm whether the task is architecture, research, reconstruction, or
   publication packaging.

## Canonical Reference Workflow

The default first reference is now the Supplemental Graphics PDF:
[../references/enlightenment_now_supplemental_graphics.pdf](../references/enlightenment_now_supplemental_graphics.pdf).
Use it for figure images, figure titles, source notes, bibliography keys, and
surrounding explanatory text. Kindle is a fallback only when the PDF lacks
necessary context.

For each figure, use this order:

1. Open Supplemental Graphics PDF.
2. Locate figure.
3. Read figure image.
4. Read source note.
5. Read surrounding explanatory text.
6. Resolve bibliography.
7. Recover original dataset.
8. Search archived versions.
9. Reconstruct.
10. Extend.
11. Editorial review.

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

## Review Protocol

Every figure must pass the five-phase
[Figure Review Protocol](review_protocol.md) before it is considered complete:

1. Evidence Review.
2. Source Review.
3. Reconstruction Review.
4. Extension Review.
5. Reviewer Challenge.

Use [review_checklist.md](review_checklist.md) as the operational checklist.
Each active figure directory should eventually include a completed copy or
equivalent figure-specific review file.

The burden of proof is that the original underlying data exist unless
substantial evidence suggests otherwise. Codex must attempt to prove or
disprove that assumption before accepting a proxy dataset.

A figure is complete only when reconstruction, extension, discrepancy review,
reviewer questions, editorial review, repository updates, registry updates, and
`PROJECT_STATE.md` updates are all done. Only then may Codex begin another
figure.

## Editorial Review Gate

After reconstruction, extension, captions, anomaly review, and the review
checklist, run the [Editorial Review Gate](editorial_review_gate.md) before
final commit, `PROJECT_STATE.md` completion language, or marking the batch
complete.

This gate is a publication-quality scan, not a source-recovery analysis. Imagine
the batch has already been published, open every comparison image, and ask:

> If I opened this report for the first time, what would immediately catch my
> eye?

For every figure, answer:

- Completeness: is anything obviously missing, such as a Supplemental Graphics
  PDF reference crop, reconstruction, extension, caption, or labels?
- Layout: does anything look visually wrong, such as tiny plots, poor scaling,
  poor cropping, excessive whitespace, inconsistent margins, awkward label
  placement, or overlapping labels?
- Visual similarity: would a human immediately say the original and recreated
  figures look like the same figure?
- Extensions: is any extension visually clear, visibly separated when
  successor data are used, and not misleadingly continuous?
- Captions: does the caption explain every obvious visual discrepancy before a
  reader has to ask?

Any issue obvious within approximately ten seconds of viewing the page must be
corrected automatically or explicitly explained. Classify each issue as
`Critical`, `Major`, or `Minor`.

A batch may not complete while any `Critical` issue exists or any unexplained
`Major` issue exists. Minor issues may remain only if documented.

After per-figure review, perform a cross-figure review:

- Which figure looks weakest?
- Which figure would most concern a reviewer?
- Is the weakest figure good enough to publish?

If the weakest figure is not good enough to publish, continue improving it or
document why manual input or further source recovery is genuinely required.

Every batch final response must include an Editorial Review Summary:

- Critical issues found.
- Major issues found.
- Minor issues found.
- Issues automatically corrected.
- Issues remaining.
- Why the batch is acceptable for publication or remains a documented
  partial/blocked batch.

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
- Editorial Review Summary.

## Commit Practice

Use logical commits:

1. Import or reorganize artifacts.
2. Add or update documentation.
3. Update metadata/state.
4. Add reproducibility or validation tooling.

Avoid mixing new figure reconstruction with repository maintenance.

Do not create the final commit for a reconstruction batch until the Editorial
Review Gate has passed or its blockers have been explicitly documented.

## Fresh-Contributor Review

Before finishing a repository architecture task, ask:

Could another researcher understand the project, reproduce the figures, and
continue work without reading the chat history?

If the answer is no, improve the repository before stopping.
