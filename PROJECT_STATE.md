# Project State

Last update: 2026-06-29 00:00 America/Los_Angeles

Project version: `0.1.0-repository-bootstrap`

This file is the canonical project memory. Future Codex or ChatGPT runs should
read this file first, then update it before finishing any project-state-changing
work.

## Mission

Reconstruct selected figures from Steven Pinker's *Enlightenment Now* using
publicly inspectable data, documented provenance, reproducible code, and visual
comparison against the book figure.

The repository, not the conversation history, is the authoritative record.

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
| `0.1.0-repository-bootstrap` | 2026-06-29 | Imported two-figure proof of concept, provenance, source logs, data references, plots, comparisons, scripts, and canonical project documentation into GitHub layout. |

## Rule For Future Sessions

Before doing new reconstruction work:

1. Read this file.
2. Read [docs/pipeline.md](docs/pipeline.md) and [docs/workflow.md](docs/workflow.md).
3. Read the target figure directory, especially `metadata/metadata.json`,
   `provenance/provenance.md`, `source_logs/source_log.md`, and
   `discrepancy_logs/discrepancy_log.md`.
4. Update this file and [docs/lessons_learned.md](docs/lessons_learned.md)
   before finishing.
