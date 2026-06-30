# Project State

Last update: 2026-06-30 03:45 America/Los_Angeles

Project version: `1.5-track-a-health-nutrition-branch`

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
checklist at [docs/review_checklist.md](docs/review_checklist.md). The final
publication-quality gate is [docs/editorial_review_gate.md](docs/editorial_review_gate.md).

Every figure must pass the five-phase research review protocol and every batch
must pass the Editorial Review Gate before it is considered complete. The
burden of proof is that the original underlying data exist unless substantial
evidence suggests otherwise; absence of immediate search results is not enough
to accept a proxy dataset.

A figure is complete only when reconstruction, extension, discrepancy review,
reviewer challenge, editorial review, repository updates, registry updates, and
this file are all updated. Only then may Codex begin another figure.

## Active Figures

| Figure | Title | Lifecycle stage | Status | Confidence | Current disposition |
| --- | --- | --- | --- | --- | --- |
| 5-1 | Life expectancy, 1771-2015 | Reviewed book-period reconstruction; no comparable extension plotted | `verified_reproduction` | High | OWID/Roser 2016n-style historical dataset matches the Kindle source line; the extended artifact is explicitly labeled as no comparable regional extension. |
| 5-2 | Child mortality, 1751-2013 | Visual QA remediation and source recovery | `partial_match` | Medium | PDF reference crop added and proxy coverage trimmed to better match the book; exact Roser 2016a UN/HMD assembled source remains unresolved. |
| 5-3 | Maternal mortality, 1751-2013 | Track A time-boxed reconstruction | `partial_match` | Medium | Book reference refreshed from supplemental PDF page 3; current OWID maternal-mortality successor data reproduce the broad concept but exact Roser 2016p vintage is not recovered. |
| 5-4 | Life expectancy, UK, 1701-2013 | Track A targeted source recovery needed | `needs_targeted_source_recovery` | Low | Book reference/source refreshed from supplemental PDF page 4, but exact age-specific HMD/OWID series for ages 1, 5, 10, 20, 30, 40, 50, 60, and 70 were not recovered. |
| 6-1 | Childhood deaths from infectious disease, 2000-2013 | Visual QA blocked at source recovery | `blocked_external_source` | Low | PDF reference shows a five-line annual deaths chart; misleading IHME bar proxy was removed and reconstruction is blocked until the cited CHERG/WHO Liu et al. appendix or verified equivalent annual line-series data are recovered. |
| 7-1 | Calories, 1700-2013 | Track A time-boxed reconstruction | `partial_match` | Medium | Book reference/source refreshed from supplemental PDF page 5; OWID/FAO historical calories dataset gives a plausible reconstruction but exact book-era source styling/vintage is unresolved. |
| 7-2 | Childhood stunting, 1966-2014 | Track A time-boxed reconstruction | `partial_match` | Medium-low | Book reference/source refreshed from supplemental PDF page 5; World Bank stunting prevalence proxy used because exact OWID/Roser 2016j WHO NLIS vintage was not recovered. |
| 8-4 | Extreme poverty (proportion), 1820-2015 | Reviewed book-period reconstruction; no comparable extension plotted | `verified_reproduction` | High | OWID historical Bourguignon & Morrison/PovcalNet dataset matches the Kindle source chain; comparison layout was remediated and no comparable World successor extension is plotted. |
| 10-5 | Oil spills, 1970-2016 | Source recovery and discrepancy analysis | `partial_match` | Medium | Do not label as verified until the exact historical oil-shipped-by-sea series or an exact archival copy is recovered. |
| 10-6 | Protected areas, 1990-2014 | Verified book-period reconstruction with successor-series extension | `verified_reproduction` | High | Book-period reconstruction accepted; bibliographic cleanup and publication packaging remain. |
| 10-7 | Carbon intensity (CO2 emissions per dollar of GDP), 1820-2014 | Reviewed book-period reconstruction with successor-series extension | `verified_reproduction` | High | OWID 2017 carbon-intensity dataset matches the Kindle source chain; extension uses current OWID successor data after 2014. |
| 10-8 | CO2 emissions, 1960-2015 | Reviewed book-period reconstruction with successor-series extension | `verified_reproduction` | High | OWID 2017 regional CDIAC dataset matches the Kindle source chain; extension uses current OWID/GCB successor categories after 2015. |
| 19-1 | Nuclear weapons, 1945-2015 | Source recovery and visual discrepancy analysis | `partial_match` | Medium-low | Actual Kindle chart-page crop is now included; current OWID successor line reconstruction remains a poor visual match to the original stacked-area figure and the cited HumanProgress/FAS 2016 table remains unresolved. |

## Completed Figures

Completed means the book-period source has been located with enough evidence to
support a verified reconstruction.

- Figure 10-6: archived World Bank WDI bulk CSV from the Internet Archive
  reproduces the book-period land and marine protected-area trends.
- Figure 5-1: OWID/Roser 2016n-style historical life-expectancy dataset based
  on Riley 2005 plus WHO/World Bank matches the Kindle source line and visual
  trend.
- Figure 8-4: OWID historical dataset based on Bourguignon & Morrison 2002 and
  World Bank PovcalNet 2015 reproduces the book-period extreme-poverty
  proportion chart.
- Figure 10-7: OWID 2017 carbon-intensity dataset based on CDIAC, World Bank,
  and Maddison data reproduces the book-period line chart.
- Figure 10-8: OWID 2017 regional CDIAC dataset reproduces the book-period
  stacked emissions chart.

## Unresolved Figures

- Figure 10-5: the oil-spill count line is well supported, but the exact
  historical annual oil-shipped-by-sea/tanker-trade series for 1970-2016 has
  not been proven. A recovered UNCTADStat-style mirror supports a book-style
  reconstruction through 2020, but it remains an updated-equivalent or partial
  source rather than a verified book-era dataset.
- Figure 5-2: the Kindle title/source and chart page were captured, and the
  reconstruction was remediated to use the current OWID selected
  child-mortality series directly in percent units. It remains a partial match
  because the exact cited Roser 2016a UN Child Mortality/Human Mortality
  Database assembly has not been recovered.
- Figure 19-1: the actual Kindle chart-page crop was captured and included in
  the side-by-side comparison. The current reconstruction remains a partial
  match because it uses current OWID nuclear-warhead successor line data rather
  than the cited HumanProgress/FAS 2016 table and does not reproduce the
  original stacked-area encoding.
- Figure 5-3: broad visual match from current OWID maternal-mortality data, but
  exact Roser 2016p/Gapminder vintage remains unrecovered.
- Figure 5-4: Kindle chart captured, but only partial age-specific UK life
  expectancy data were recovered; source recovery for the exact HMD/OWID age
  series is required.
- Figure 6-1: Kindle chart-page capture and cited CHERG/WHO Liu et al. 2014
  supplementary appendix were not recovered in Track A; current artifact is a
  blocked proxy only.
- Figure 7-1: plausible OWID/FAO calories reconstruction, but exact book-era
  source vintage and line styling remain unresolved.
- Figure 7-2: World Bank stunting prevalence proxy approximates the book chart,
  but exact OWID/Roser 2016j WHO NLIS source vintage remains unrecovered.

## Attempted But Not Expanded

The initial Kindle List of Figures extraction captured 75 visible entries.
Figures 5-1, 5-2, 5-3, 5-4, 6-1, 7-1, 7-2, 8-4, 10-5, 10-6, 10-7, 10-8, and 19-1 have been carried
through at least one source recovery, transformation, plotting, and validation
pass. Continue processing in small batches of no more than two figures unless
explicitly directed otherwise.

## Canonical Figure Artifacts

Future runs should use these repository-relative paths to find the current
canonical visual and documentation artifacts. If a figure plot, comparison
image, caption, provenance file, anomaly review, metadata file, or status
changes, update this section in the same commit.

### Figure 5-1 - Life expectancy, 1771-2015

Status: `verified_reproduction`

Canonical visual artifacts:

- Original reference: `figures/5-1/plots/comparisons/kindle_reference_figure_5_1.png`
- Book-period reconstruction: `figures/5-1/plots/book_period/figure_5_1_book_period_reconstruction.png`
- Extended reconstruction: `figures/5-1/plots/extended/figure_5_1_extended_reconstruction.png`
- Book-period comparison: `figures/5-1/plots/comparisons/figure_5_1_book_period_comparison.png`
- Extended comparison: `figures/5-1/plots/comparisons/figure_5_1_extended_comparison.png`

Canonical documentation:

- Caption: `figures/5-1/captions/caption.txt`
- Provenance: `figures/5-1/provenance/provenance.md`
- Anomaly review: `figures/5-1/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/5-1/metadata/metadata.json`
- Review checklist: `figures/5-1/review_checklist.md`

### Figure 5-2 - Child mortality, 1751-2013

Status: `partial_match`

Canonical visual artifacts:

- Original reference: `figures/5-2/plots/comparisons/kindle_reference_figure_5_2.png`
- Book-period reconstruction: `figures/5-2/plots/book_period/figure_5_2_book_period_reconstruction.png`
- Extended reconstruction: `figures/5-2/plots/extended/figure_5_2_extended_reconstruction.png`
- Book-period comparison: `figures/5-2/plots/comparisons/figure_5_2_book_period_comparison.png`
- Extended comparison: `figures/5-2/plots/comparisons/figure_5_2_extended_comparison.png`

Canonical documentation:

- Caption: `figures/5-2/captions/caption.txt`
- Provenance: `figures/5-2/provenance/provenance.md`
- Anomaly review: `figures/5-2/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/5-2/metadata/metadata.json`
- Review checklist: `figures/5-2/review_checklist.md`

### Figure 5-3 - Maternal mortality, 1751-2013

Status: `partial_match`

Canonical visual artifacts:

- Original reference: `figures/5-3/plots/comparisons/kindle_reference_figure_5_3.png`
- Book-period reconstruction: `figures/5-3/plots/book_period/figure_5_3_book_period_reconstruction.png`
- Extended reconstruction: `figures/5-3/plots/extended/figure_5_3_extended_reconstruction.png`
- Book-period comparison: `figures/5-3/plots/comparisons/figure_5_3_book_period_comparison.png`
- Extended comparison: `figures/5-3/plots/comparisons/figure_5_3_extended_comparison.png`

Canonical documentation:

- Caption: `figures/5-3/captions/caption.txt`
- Provenance: `figures/5-3/provenance/provenance.md`
- Anomaly review: `figures/5-3/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/5-3/metadata/metadata.json`
- Review checklist: `figures/5-3/review_checklist.md`

### Figure 5-4 - Life expectancy, UK, 1701-2013

Status: `needs_targeted_source_recovery`

Canonical visual artifacts:

- Original reference: `figures/5-4/plots/comparisons/kindle_reference_figure_5_4.png`
- Book-period reconstruction: `figures/5-4/plots/book_period/figure_5_4_book_period_reconstruction.png`
- Extended reconstruction: `figures/5-4/plots/extended/figure_5_4_extended_reconstruction.png`
- Book-period comparison: `figures/5-4/plots/comparisons/figure_5_4_book_period_comparison.png`
- Extended comparison: `figures/5-4/plots/comparisons/figure_5_4_extended_comparison.png`

Canonical documentation:

- Caption: `figures/5-4/captions/caption.txt`
- Provenance: `figures/5-4/provenance/provenance.md`
- Anomaly review: `figures/5-4/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/5-4/metadata/metadata.json`
- Review checklist: `figures/5-4/review_checklist.md`

### Figure 6-1 - Childhood deaths from infectious disease, 2000-2013

Status: `blocked_external_source`

Canonical visual artifacts:

- Original reference: `figures/6-1/plots/comparisons/kindle_reference_figure_6_1.png`
- Book-period reconstruction: `figures/6-1/plots/book_period/figure_6_1_book_period_reconstruction.png`
- Extended reconstruction: `figures/6-1/plots/extended/figure_6_1_extended_reconstruction.png`
- Book-period comparison: `figures/6-1/plots/comparisons/figure_6_1_book_period_comparison.png`
- Extended comparison: `figures/6-1/plots/comparisons/figure_6_1_extended_comparison.png`

Canonical documentation:

- Caption: `figures/6-1/captions/caption.txt`
- Provenance: `figures/6-1/provenance/provenance.md`
- Anomaly review: `figures/6-1/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/6-1/metadata/metadata.json`
- Review checklist: `figures/6-1/review_checklist.md`

### Figure 7-1 - Calories, 1700-2013

Status: `partial_match`

Canonical visual artifacts:

- Original reference: `figures/7-1/plots/comparisons/kindle_reference_figure_7_1.png`
- Book-period reconstruction: `figures/7-1/plots/book_period/figure_7_1_book_period_reconstruction.png`
- Extended reconstruction: `figures/7-1/plots/extended/figure_7_1_extended_reconstruction.png`
- Book-period comparison: `figures/7-1/plots/comparisons/figure_7_1_book_period_comparison.png`
- Extended comparison: `figures/7-1/plots/comparisons/figure_7_1_extended_comparison.png`

Canonical documentation:

- Caption: `figures/7-1/captions/caption.txt`
- Provenance: `figures/7-1/provenance/provenance.md`
- Anomaly review: `figures/7-1/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/7-1/metadata/metadata.json`
- Review checklist: `figures/7-1/review_checklist.md`

### Figure 7-2 - Childhood stunting, 1966-2014

Status: `partial_match`

Canonical visual artifacts:

- Original reference: `figures/7-2/plots/comparisons/kindle_reference_figure_7_2.png`
- Book-period reconstruction: `figures/7-2/plots/book_period/figure_7_2_book_period_reconstruction.png`
- Extended reconstruction: `figures/7-2/plots/extended/figure_7_2_extended_reconstruction.png`
- Book-period comparison: `figures/7-2/plots/comparisons/figure_7_2_book_period_comparison.png`
- Extended comparison: `figures/7-2/plots/comparisons/figure_7_2_extended_comparison.png`

Canonical documentation:

- Caption: `figures/7-2/captions/caption.txt`
- Provenance: `figures/7-2/provenance/provenance.md`
- Anomaly review: `figures/7-2/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/7-2/metadata/metadata.json`
- Review checklist: `figures/7-2/review_checklist.md`

### Figure 8-4 - Extreme poverty (proportion), 1820-2015

Status: `verified_reproduction`

Canonical visual artifacts:

- Original reference: `figures/8-4/plots/comparisons/kindle_reference_figure_8_4.png`
- Book-period reconstruction: `figures/8-4/plots/book_period/figure_8_4_book_period_reconstruction.png`
- Extended reconstruction: `figures/8-4/plots/extended/figure_8_4_extended_reconstruction.png`
- Book-period comparison: `figures/8-4/plots/comparisons/figure_8_4_book_period_comparison.png`
- Extended comparison: `figures/8-4/plots/comparisons/figure_8_4_extended_comparison.png`

Canonical documentation:

- Caption: `figures/8-4/captions/caption.txt`
- Provenance: `figures/8-4/provenance/provenance.md`
- Anomaly review: `figures/8-4/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/8-4/metadata/metadata.json`
- Review checklist: `figures/8-4/review_checklist.md`

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

### Figure 10-7 - Carbon intensity (CO2 emissions per dollar of GDP), 1820-2014

Status: `verified_reproduction`

Canonical visual artifacts:

- Original reference: `figures/10-7/plots/comparisons/kindle_reference_figure_10_7.png`
- Book-period reconstruction: `figures/10-7/plots/book_period/figure_10_7_book_period_reconstruction.png`
- Extended reconstruction: `figures/10-7/plots/extended/figure_10_7_extended_reconstruction.png`
- Book-period comparison: `figures/10-7/plots/comparisons/figure_10_7_book_period_comparison.png`
- Extended comparison: `figures/10-7/plots/comparisons/figure_10_7_extended_comparison.png`

Canonical documentation:

- Caption: `figures/10-7/captions/caption.txt`
- Provenance: `figures/10-7/provenance/provenance.md`
- Anomaly review: `figures/10-7/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/10-7/metadata/metadata.json`
- Review checklist: `figures/10-7/review_checklist.md`

### Figure 10-8 - CO2 emissions, 1960-2015

Status: `verified_reproduction`

Canonical visual artifacts:

- Original reference: `figures/10-8/plots/comparisons/kindle_reference_figure_10_8.png`
- Book-period reconstruction: `figures/10-8/plots/book_period/figure_10_8_book_period_reconstruction.png`
- Extended reconstruction: `figures/10-8/plots/extended/figure_10_8_extended_reconstruction.png`
- Book-period comparison: `figures/10-8/plots/comparisons/figure_10_8_book_period_comparison.png`
- Extended comparison: `figures/10-8/plots/comparisons/figure_10_8_extended_comparison.png`

Canonical documentation:

- Caption: `figures/10-8/captions/caption.txt`
- Provenance: `figures/10-8/provenance/provenance.md`
- Anomaly review: `figures/10-8/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/10-8/metadata/metadata.json`
- Review checklist: `figures/10-8/review_checklist.md`

### Figure 19-1 - Nuclear weapons, 1945-2015

Status: `partial_match`

Canonical visual artifacts:

- Original reference: `figures/19-1/plots/comparisons/kindle_reference_figure_19_1.png`
- Book-period reconstruction: `figures/19-1/plots/book_period/figure_19_1_book_period_reconstruction.png`
- Extended reconstruction: `figures/19-1/plots/extended/figure_19_1_extended_reconstruction.png`
- Book-period comparison: `figures/19-1/plots/comparisons/figure_19_1_book_period_comparison.png`
- Extended comparison: `figures/19-1/plots/comparisons/figure_19_1_extended_comparison.png`

Canonical documentation:

- Caption: `figures/19-1/captions/caption.txt`
- Provenance: `figures/19-1/provenance/provenance.md`
- Anomaly review: `figures/19-1/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/19-1/metadata/metadata.json`
- Review checklist: `figures/19-1/review_checklist.md`

## Current Blockers

- Future reconstruction batches must run the Editorial Review Gate before final
  commit. Any ten-second-obvious issue must be corrected or explicitly
  explained; batches may not complete with any Critical issue or unexplained
  Major issue.
- Figure 10-5 needs the exact Roser 2016r/ITOPF source snapshot or a documented
  archival equivalent for the full 1970-2016 oil-shipped-by-sea series.
- Figure 5-2 needs the exact Roser 2016a UN/HMD assembled dataset or an
  archival copy before it can be promoted beyond `partial_match`.
- Figure 19-1 needs the cited HumanProgress/FAS 2016 table or archival
  equivalent and a stacked-area reconstruction before visual validation can
  pass.
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
3. Keep Figures 5-2, 5-3, 5-4, 6-1, 7-1, 7-2, 10-5, and 19-1 open for targeted source recovery before
   promoting their statuses.
4. For Figure 10-6, complete bibliographic cleanup and document the WDI archive
   capture as the accepted source.
5. Build reusable source adapters for OWID/GitHub datasets, World Bank bulk
   archives, UNCTAD, and academic literature before larger batches.
6. Add a small validation command that checks metadata consistency, checksums,
   and required files for every figure directory.

## Repository Version History

| Version | Date | Summary |
| --- | --- | --- |
| `1.5.1-ch5-7-visual-qa-remediation` | 2026-06-30 | Re-reviewed chapter 5-7 side-by-side comparisons visually; switched 5-1 and 5-2 to PDF chart references, corrected the 5-1 crop, trimmed 5-2 proxy coverage, and replaced the misleading 6-1 bar proxy with a source-blocked reconstruction panel. |
| `1.5-track-a-health-nutrition-branch` | 2026-06-30 | Track A branch processed Figures 5-3, 5-4, 6-1, 7-1, and 7-2 in a time-boxed health/nutrition batch. No figures were promoted to verified; statuses document partial matches, targeted source recovery, and blocked external-source evidence. |
| `1.4-four-figure-remediation` | 2026-06-29 | Remediated the latest four-figure batch: clarified no-extension artifacts for Figures 5-1 and 8-4, improved Figure 5-2 source/units while retaining partial-match status, captured the actual Figure 19-1 Kindle chart crop, and marked Figure 19-1 visual validation as poor until the cited FAS/HumanProgress stacked source is recovered. |
| `1.3-editorial-review-gate` | 2026-06-29 | Added a permanent Editorial Review Gate for publication-quality batch review before final commit, `PROJECT_STATE.md` completion language, or batch completion. |
| `1.2-four-figure-batch-5-1-5-2-8-4-19-1` | 2026-06-29 | Processed Figures 5-1, 5-2, 8-4, and 19-1. Figures 5-1 and 8-4 reached verified book-period reconstructions; Figures 5-2 and 19-1 remain partial matches with documented source/capture blockers. |
| `1.1-two-figure-batch-10-7-10-8` | 2026-06-29 | Processed Figures 10-7 and 10-8 through the full workflow, including Kindle evidence, OWID source recovery, book-period reconstruction, successor extension, review checklist, registry update, and canonical artifact paths. |
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
4. Read [docs/editorial_review_gate.md](docs/editorial_review_gate.md).
5. Read [docs/pipeline.md](docs/pipeline.md) and [docs/workflow.md](docs/workflow.md).
6. Read the target figure directory, especially `metadata/metadata.json`,
   `provenance/provenance.md`, `source_logs/source_log.md`, and
   `discrepancy_logs/discrepancy_log.md`.
7. Update the relevant figure registry rows, this file, and
   [docs/lessons_learned.md](docs/lessons_learned.md)
   before finishing.
8. Whenever a figure plot, comparison image, caption, provenance file, anomaly
   review, metadata file, or status changes, update the corresponding paths and
   status in the `Canonical Figure Artifacts` section above.
9. Whenever Codex updates or reviews a figure, the final response must render
   the latest side-by-side comparison images inline, including both
   book-period and extended comparisons where available. GitHub remains the
   canonical archive, but rendered images in the Codex response are required
   for ChatGPT visual QA.
10. Codex must not stop after producing a side-by-side comparison if visible
   discrepancies remain that could plausibly be addressed through additional
   source recovery, transformation correction, styling correction, scaling
   correction, or extension-data review.
11. Codex must run the Editorial Review Gate before final commit and include an
    Editorial Review Summary in the final response for every reconstruction
    batch.

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

For reconstruction batches, Codex may commit and mark the batch complete only
after the Editorial Review Gate finds no Critical issues and no unexplained
Major issues. Minor issues may remain only if documented.
