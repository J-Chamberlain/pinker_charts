# Project State

Last update: 2026-06-29 00:00 America/Los_Angeles

Project version: `1.0-review-protocol`

This file is the canonical project memory. Future Codex or ChatGPT runs should
read this file first, then update it before finishing any project-state-changing
work.

## Mission

Reconstruct selected figures from Steven Pinker's *Enlightenment Now* using
publicly inspectable data, documented provenance, reproducible code, and visual
comparison against the book figure.

The repository, not the conversation history, is the authoritative record.

## Figure Registry

The canonical project-wide figure queue is
[data/figure_registry.csv](data/figure_registry.csv), with a JSON mirror at
[data/figure_registry.json](data/figure_registry.json). Registry rules are
documented in [docs/figure_registry.md](docs/figure_registry.md).

Future Codex runs must consult the registry before selecting or continuing
figure work, then update the relevant registry rows before finishing.

## Review Protocol

The permanent figure quality gate is
[docs/review_protocol.md](docs/review_protocol.md), with the operational
checklist at [docs/review_checklist.md](docs/review_checklist.md).

Every figure must pass the five-phase review protocol before it is considered
complete. The burden of proof is that the original underlying data exist unless
substantial evidence suggests otherwise; absence of immediate search results is
not enough to accept a proxy dataset.

A figure is complete only when reconstruction, extension, discrepancy review,
reviewer challenge, repository updates, registry updates, and this file are all
updated. Only then may Codex begin another figure.

## Active Figures

| Figure | Title | Lifecycle stage | Status | Confidence | Current disposition |
| --- | --- | --- | --- | --- | --- |
| 10-5 | Oil spills, 1970-2016 | Source recovery and discrepancy analysis | `partial_match` | Medium | Do not label as verified until the exact historical oil-shipped-by-sea series or an exact archival copy is recovered. |
| 10-6 | Protected areas, 1990-2014 | Verified book-period reconstruction with successor-series extension | `verified_reproduction` | High | Book-period reconstruction accepted; bibliographic cleanup and publication packaging remain. |

## Completed Figures

Completed means the book-period source has been located with enough evidence to
support a verified reconstruction.

- Figure 10-6: archived World Bank WDI bulk CSV from the Internet Archive
  reproduces the book-period land and marine protected-area trends.

## Unresolved Figures

- Figure 10-5: the oil-spill count line is well supported, but the exact
  historical annual oil-shipped-by-sea/tanker-trade series for 1970-2016 has
  not been proven. A recovered UNCTADStat-style mirror supports a book-style
  reconstruction through 2020, but it remains an updated-equivalent or partial
  source rather than a verified book-era dataset.

## Attempted But Not Expanded

The initial Kindle List of Figures extraction captured 75 visible entries.
Only figures 10-5 and 10-6 have been carried through source recovery,
transformation, plotting, and validation. Do not start chapter-scale expansion
until this repository's metadata and workflow documents remain clean after a
fresh-contributor review.

## Canonical Figure Artifacts

Future runs should use these repository-relative paths to find the current
canonical visual and documentation artifacts. If a figure plot, comparison
image, caption, provenance file, anomaly review, metadata file, or status
changes, update this section in the same commit.

### Figure 10-5 - Oil spills, 1970-2016

Status: `partial_match`

Canonical visual artifacts:

- Original reference: `figures/10-5/plots/comparisons/corrected_figure_10_5_book_crop.png`
- Book-period reconstruction: `figures/10-5/plots/book_period/figure_10_5_book_period_reconstruction.png`
- Extended reconstruction: `figures/10-5/plots/extended/figure_10_5_extended_reconstruction.png`
- Book-period comparison: `figures/10-5/plots/comparisons/figure_10_5_book_style_comparison_captioned.png`
- Extended comparison: `figures/10-5/plots/comparisons/figure_10_5_extended_comparison_captioned.png`
- Diagnostic plot: `figures/10-5/plots/diagnostics/figure_10_5_unctad_partial_oil_shipping_diagnostic.png`
- Diagnostic plot: `figures/10-5/plots/diagnostics/figure_10_5_rmt_tanker_trade_selected_years_diagnostic.png`

Canonical documentation:

- Caption: `figures/10-5/captions/caption.txt`
- Provenance: `figures/10-5/provenance/provenance.md`
- Anomaly review: `figures/10-5/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/10-5/metadata/metadata.json`

### Figure 10-6 - Protected areas, 1990-2014

Status: `verified_reproduction`

Canonical visual artifacts:

- Original reference: `figures/10-6/plots/comparisons/corrected_figure_10_6_book_crop.png`
- Book-period reconstruction: `figures/10-6/plots/book_period/figure_10_6_book_period_reconstruction.png`
- Extended reconstruction: `figures/10-6/plots/extended/figure_10_6_extended_reconstruction.png`
- Book-period comparison: `figures/10-6/plots/comparisons/figure_10_6_book_style_comparison_captioned.png`
- Extended comparison: `figures/10-6/plots/comparisons/figure_10_6_extended_comparison_captioned.png`
- Diagnostic plot: `figures/10-6/plots/diagnostics/figure_10_6_current_vs_archived_wdi_diagnostic.png`

Canonical documentation:

- Caption: `figures/10-6/captions/caption.txt`
- Provenance: `figures/10-6/provenance/provenance.md`
- Anomaly review: `figures/10-6/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/10-6/metadata/metadata.json`

## Current Blockers

- Figure 10-5 needs the exact Roser 2016r/ITOPF source snapshot or a documented
  archival equivalent for the full 1970-2016 oil-shipped-by-sea series.
- The legacy file [data/metadata/figure_metadata_legacy.csv](data/metadata/figure_metadata_legacy.csv)
  is stale and kept only as an imported historical artifact. The canonical
  metadata is [data/metadata/figure_metadata.csv](data/metadata/figure_metadata.csv)
  plus the per-figure JSON files.
- Some imported scripts still contain local absolute paths from the original
  Mac Mini proof of concept.
- Visual comparison images include cropped book-reference material and should
  be reviewed before public website publication.

## Outstanding Research Questions

- Was Figure 10-5's gray line sourced from a retired UNCTADStat export,
  ITOPF-internal chart data, an Our World in Data/Roser snapshot, or a manually
  assembled institutional series?
- Can 2021-2023 tanker-trade values be recovered on the same scale as the
  book-period Figure 10-5 right-axis series?
- Did Figure 10-6 plot WDI anchor years directly or use an intermediate WRI
  table derived from the same WDI/Protected Planet source chain?
- What is the minimum evidence threshold required before calling future figures
  `verified_reproduction`?

## Next Recommended Tasks

1. Run a fresh-clone review of this repository and verify that all relative
   links resolve.
2. Update scripts to use repository-relative paths and regenerate outputs from
   the imported data without Mac-specific paths.
3. Keep Figure 10-5 open for targeted source recovery only; do not expand to
   new figures until its status language is settled.
4. For Figure 10-6, complete bibliographic cleanup and document the WDI archive
   capture as the accepted source.
5. Add a small validation command that checks metadata consistency, checksums,
   and required files for every figure directory.

## Repository Version History

| Version | Date | Summary |
| --- | --- | --- |
| `1.0-review-protocol` | 2026-06-29 | Added permanent five-phase figure review protocol, acceptance checklist, burden-of-proof rule, reviewer confidence standard, and batch completion rule. |
| `0.1.1-figure-registry` | 2026-06-29 | Added canonical figure registry, registry documentation, and stronger iterative QA/stopping rules for future batches. |
| `0.1.0-repository-bootstrap` | 2026-06-29 | Imported two-figure proof of concept, provenance, source logs, data references, plots, comparisons, scripts, and canonical project documentation into GitHub layout. |

## Rule For Future Sessions

Before doing new reconstruction work:

1. Read this file.
2. Read [docs/figure_registry.md](docs/figure_registry.md) and consult
   [data/figure_registry.csv](data/figure_registry.csv).
3. Read [docs/review_protocol.md](docs/review_protocol.md) and
   [docs/review_checklist.md](docs/review_checklist.md).
4. Read [docs/pipeline.md](docs/pipeline.md) and [docs/workflow.md](docs/workflow.md).
5. Read the target figure directory, especially `metadata/metadata.json`,
   `provenance/provenance.md`, `source_logs/source_log.md`, and
   `discrepancy_logs/discrepancy_log.md`.
6. Update the relevant figure registry rows, this file, and
   [docs/lessons_learned.md](docs/lessons_learned.md)
   before finishing.
7. Whenever a figure plot, comparison image, caption, provenance file, anomaly
   review, metadata file, or status changes, update the corresponding paths and
   status in the `Canonical Figure Artifacts` section above.
8. Whenever Codex updates or reviews a figure, the final response must render
   the latest side-by-side comparison images inline, including both
   book-period and extended comparisons where available. GitHub remains the
   canonical archive, but rendered images in the Codex response are required
   for ChatGPT visual QA.
9. Codex must not stop after producing a side-by-side comparison if visible
   discrepancies remain that could plausibly be addressed through additional
   source recovery, transformation correction, styling correction, scaling
   correction, or extension-data review.

After each side-by-side comparison, Codex must self-review:

1. What visibly differs from the original?
2. Is the discrepancy due to missing data, wrong data, styling, scaling,
   source-version change, or post-publication extension?
3. Can the issue be addressed automatically?
4. If yes, continue iterating.
5. If no, document why not and classify the unresolved issue.

Codex may stop only when the figure is visually and evidentially satisfactory,
remaining discrepancies are explained in the caption and anomaly review, the
source search space has been exhaustively documented, or manual input is
genuinely required. Codex should not stop merely because it found a plausible
source or generated a plot.
