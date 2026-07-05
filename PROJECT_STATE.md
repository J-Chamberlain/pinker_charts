# Project State

Last update: 2026-07-05 America/Los_Angeles

Project version: `1.13-remediate-figure-10-2-projection`

This file is the canonical project memory. Future Codex or ChatGPT runs should
read this file first, then update it before finishing any project-state-changing
work.

## Mission

Reconstruct selected figures from Steven Pinker's *Enlightenment Now* using
publicly inspectable data, documented provenance, reproducible code, and visual
comparison against the book figure.

The repository, not the conversation history, is the authoritative record.

## Canonical Reference Document

The canonical figure reference for all future reconstruction work is the
Supplemental Graphics PDF:

- [references/enlightenment_now_supplemental_graphics.pdf](references/enlightenment_now_supplemental_graphics.pdf)

Use this PDF as the default first reference for figure images, figure titles,
source notes, bibliography keys, and surrounding explanatory text. Kindle is now
a fallback only when the Supplemental Graphics PDF lacks necessary context or
when a legacy Kindle-derived artifact must be audited.

Default figure workflow:

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

## Current Visual QA Baseline

The continuous visual review PDF is tracked at:

- [output/pdf/recreated_figures_review_scroll.pdf](output/pdf/recreated_figures_review_scroll.pdf)

Its machine-readable manifest is:

- [output/pdf/recreated_figures_review_scroll.manifest.json](output/pdf/recreated_figures_review_scroll.manifest.json)

The current baseline contains 25 figure comparison items plus a summary page.
Source-recovery-only figures without real reconstructed comparisons are
excluded.

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
| 4-1 | Tone of the news, 1945-2010 | Source recovery blocked; Supplemental PDF reference captured | `manual_review_needed` | Low | Deeper First Monday/GDELT/archive/repository recovery found only article images and mirrored PNGs; underlying monthly NYT/SWB tone data were not found; no digitized reconstruction was made. |
| 5-1 | Life expectancy, 1771-2015 | Reviewed book-period reconstruction; no comparable extension plotted | `verified_reproduction` | High | OWID/Roser 2016n-style historical dataset matches the Kindle source line; the extended artifact is explicitly labeled as no comparable regional extension. |
| 5-2 | Child mortality, 1751-2013 | Visual QA remediation and source recovery | `partial_match` | Medium | PDF reference crop added and proxy coverage trimmed to better match the book; exact Roser 2016a UN/HMD assembled source remains unresolved. |
| 5-3 | Maternal mortality, 1751-2013 | Track A time-boxed reconstruction | `partial_match` | Medium | Book reference refreshed from supplemental PDF page 3; current OWID maternal-mortality successor data reproduce the broad concept but exact Roser 2016p vintage is not recovered. |
| 5-4 | Life expectancy, UK, 1701-2013 | Track A targeted source recovery needed | `needs_targeted_source_recovery` | Low | Book reference/source refreshed from supplemental PDF page 4, but exact age-specific HMD/OWID series for ages 1, 5, 10, 20, 30, 40, 50, 60, and 70 were not recovered. |
| 6-1 | Childhood deaths from infectious disease, 2000-2013 | Visual QA blocked at source recovery | `blocked_external_source` | Low | PDF reference shows a five-line annual deaths chart; misleading IHME bar proxy was removed and reconstruction is blocked until the cited CHERG/WHO Liu et al. appendix or verified equivalent annual line-series data are recovered. |
| 7-1 | Calories, 1700-2013 | Track A time-boxed reconstruction | `partial_match` | Medium | Book reference/source refreshed from supplemental PDF page 5; OWID/FAO historical calories dataset gives a plausible reconstruction but exact book-era source styling/vintage is unresolved. |
| 7-2 | Childhood stunting, 1966-2014 | Track A time-boxed reconstruction | `partial_match` | Medium-low | Book reference/source refreshed from supplemental PDF page 5; World Bank stunting prevalence proxy used because exact OWID/Roser 2016j WHO NLIS vintage was not recovered. |
| 8-4 | Extreme poverty (proportion), 1820-2015 | Reviewed book-period reconstruction; no comparable extension plotted | `verified_reproduction` | High | OWID historical Bourguignon & Morrison/PovcalNet dataset matches the Kindle source chain; comparison layout was remediated and no comparable World successor extension is plotted. |
| 9-1 | International inequality, 1820-2013 | Source recovery blocked; reference captured | `manual_review_needed` | Low | Source line captured from Chapter 9 preview PDF; original OECD Clio Infra/Moatsos and Milanovic weighted data not recovered, so no digitized reconstruction was made. |
| 9-2 | Global inequality, 1820-2011 | Source recovery blocked; reference captured | `manual_review_needed` | Low | Source line captured; Milanovic 2016 fig. 3.1 underlying table not recovered, so no digitized reconstruction was made. |
| 9-3 | Inequality, UK and US, 1688-2013 | Source recovery blocked; reference captured | `manual_review_needed` | Low | Source line captured; Milanovic 2016 fig. 2.1 underlying UK/US table not recovered, so no digitized reconstruction was made. |
| 9-4 | Social spending, OECD countries, 1880-2016 | Updated-equivalent reconstruction with successor extension | `updated_equivalent` | Medium | Current OWID social-spending-oecd-longrun successor reconstructs the figure concept through 2016 and extends after 2016; exact Ortiz-Ospina & Roser 2016b/2017 source snapshot remains unrecovered. |
| 9-5 | Income gains, 1988-2008 | Source recovery blocked; reference captured | `manual_review_needed` | Low | Source line captured; Milanovic 2016 fig. 1.3 growth-incidence data not recovered, so no digitized reconstruction was made. |
| 9-6 | Poverty, US, 1960-2016 | Verified reconstruction from Meyer & Sullivan 2017 Table 1 | `verified_reproduction` | High | Source report table recovered; book-period two-series chart is reconstructed from source table values, with 2017 dotted only in extended artifact. |
| 10-1 | Population and population growth, 1750-2015 and projected to 2100 | Updated-equivalent current OWID/UN successor reconstruction | `updated_equivalent` | Medium-high | Current OWID population/growth/projection grapher data reproduce the dual-axis concept, but exact 2016 OWID/HYDE/IIASA source vintage remains unrecovered. |
| 10-2 | Sustainability, 1955-2109 | Updated-equivalent XKCD/Google Ngram reconstruction with calibrated projection audit | `updated_equivalent` | Medium | Official XKCD image, Supplemental PDF crop, and Ngram source-family data are recovered; future markers now derive from one XKCD-label visual projection, while Ngram-candidate threshold mismatches are quantified. |
| 10-5 | Oil spills, 1970-2016 | Source recovery and discrepancy analysis | `partial_match` | Medium | Do not label as verified until the exact historical oil-shipped-by-sea series or an exact archival copy is recovered. |
| 10-6 | Protected areas, 1990-2014 | Verified book-period reconstruction with successor-series extension | `verified_reproduction` | High | Book-period reconstruction accepted; bibliographic cleanup and publication packaging remain. |
| 10-7 | Carbon intensity (CO2 emissions per dollar of GDP), 1820-2014 | Reviewed book-period reconstruction with successor-series extension | `verified_reproduction` | High | OWID 2017 carbon-intensity dataset matches the Kindle source chain; extension uses current OWID successor data after 2014. |
| 10-8 | CO2 emissions, 1960-2015 | Reviewed book-period reconstruction with successor-series extension | `verified_reproduction` | High | OWID 2017 regional CDIAC dataset matches the Kindle source chain; extension uses current OWID/GCB successor categories after 2015. |
| 12-3 | Motor vehicle accident deaths, US, 1921-2015 | Kindle evidence and source-chain recovery | `source_chain_recovered` | Medium-low | Kindle cites NHTSA, informedforlife TRAFFICFATALITIES(1899-2005).pdf, FARS, and CrashStats 812384. NHTSA 2015 PDF was recovered; the pre-1966 cited mirror is 404/no 200 CDX hit. |
| 12-4 | Pedestrian deaths, US, 1927-2015 | Kindle evidence and source-chain recovery | `source_chain_recovered` | Medium-low | Kindle source chain is clear (FHWA 2003; NCSA 1995, 2006, 2016, 2017), but exact historical tables were not recovered in this pass. |
| 12-5 | Plane crash deaths, 1970-2015 | Source-family reconstruction and discrepancy analysis | `partial_match` | Medium | Reconstruction uses OWID-hosted ASN 2019 successor fatality data by flight phase and World Bank passenger counts; early-1970s peak under-matches the Kindle chart, so do not call verified. |
| 12-8 | Natural disaster deaths, 1900-2015 | Reviewed book-period reconstruction with successor extension | `updated_equivalent` | Medium-high | OWID datasets repo EM-DAT death-rate data reproduce the main decadal shape; current OWID successor data provide a dashed post-2015 decadal extension. |
| 12-9 | Lightning strike deaths, US, 1900-2015 | Reviewed book-period reconstruction; no comparable extension plotted | `verified_reproduction` | High | OWID NOAA/Lopez-Holle lightning fatality-rate dataset visually reproduces the Kindle chart; no methodologically identical post-2015 rate extension was recovered. |
| 19-1 | Nuclear weapons, 1945-2015 | Source recovery and visual discrepancy analysis | `partial_match` | Medium-low | Actual Kindle chart-page crop is now included; current OWID successor line reconstruction remains a poor visual match to the original stacked-area figure and the cited HumanProgress/FAS 2016 table remains unresolved. |


### Figure 4-1 - Tone of the news, 1945-2010

Status: `manual_review_needed`

Canonical visual artifacts:

- Supplemental PDF reference: `figures/4-1/plots/comparisons/supplemental_pdf_reference_figure_4_1.png`
- Book-period source-recovery status panel: `figures/4-1/plots/book_period/figure_4_1_book_period_source_recovery_status.png`
- Extended source-recovery status panel: `figures/4-1/plots/extended/figure_4_1_extended_source_recovery_status.png`
- Book-period status comparison: `figures/4-1/plots/comparisons/figure_4_1_book_period_status_comparison.png`
- Extended status comparison: `figures/4-1/plots/comparisons/figure_4_1_extended_status_comparison.png`

Source status: Supplemental Graphics PDF source line captured; Leetaru 2011 article, GDELT high-resolution figure mirror, First Monday snapshots, old Culturomics20 archive captures, GDELT sidecar candidates, GitHub search endpoint, Dataverse, and targeted web searches checked. Original monthly data remain unrecovered, and no plotted values were digitized. Status panels are not reconstructions.


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
- Figure 12-9: OWID NOAA/Lopez-Holle lightning fatality-rate dataset
  reproduces the book-period lightning deaths chart.

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
- Figure 12-3: Kindle source chain is captured, but the pre-1966 historical
  NHTSA/informedforlife traffic-fatality-rate PDF was not recovered.
- Figure 12-4: Kindle source chain is captured, but the stitched FHWA/NCSA
  pedestrian-rate source tables were not recovered.
- Figure 12-5: source-family reconstruction exists, but the exact ASN 2017
  extraction was not recovered and the early-1970s peak under-matches.
- Figure 12-8: OWID/EM-DAT source-family reconstruction exists and matches the
  main shape; keep as `updated_equivalent` until the exact Roser 2016q snapshot
  is version-pinned.
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


### Figure 8-3 - World income distribution, 1800, 1975, and 2015

Status: `updated_equivalent`

Canonical visual artifacts:

- Original reference: `figures/8-3/plots/comparisons/kindle_reference_figure_8_3.png`
- Book-period reconstruction: `figures/8-3/plots/book_period/figure_8_3_book_period_reconstruction.png`
- Extended reconstruction: `figures/8-3/plots/extended/figure_8_3_extended_reconstruction.png`
- Book-period comparison: `figures/8-3/plots/comparisons/figure_8_3_book_period_comparison.png`
- Extended comparison: `figures/8-3/plots/comparisons/figure_8_3_extended_comparison.png`

Canonical documentation:

- Caption: `figures/8-3/captions/caption.txt`
- Provenance: `figures/8-3/provenance/provenance.md`
- Anomaly review: `figures/8-3/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/8-3/metadata/metadata.json`
- Review checklist: `figures/8-3/review_checklist.md`

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


### Figure 9-1 - International inequality, 1820-2013

Status: `manual_review_needed`

Canonical visual artifacts:

- Original reference: `figures/9-1/plots/comparisons/kindle_reference_figure_9_1.png`
- Book-period status panel: `figures/9-1/plots/book_period/figure_9_1_book_period_reconstruction.png`
- Extended status panel: `figures/9-1/plots/extended/figure_9_1_extended_reconstruction.png`
- Book-period comparison: `figures/9-1/plots/comparisons/figure_9_1_book_period_comparison.png`
- Extended comparison: `figures/9-1/plots/comparisons/figure_9_1_extended_comparison.png`

Canonical documentation:

- Caption: `figures/9-1/captions/caption.txt`
- Provenance: `figures/9-1/provenance/provenance.md`
- Anomaly review: `figures/9-1/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/9-1/metadata/metadata.json`
- Review checklist: `figures/9-1/review_checklist.md`

### Figure 9-2 - Global inequality, 1820-2011

Status: `manual_review_needed`

Canonical visual artifacts:

- Original reference: `figures/9-2/plots/comparisons/kindle_reference_figure_9_2.png`
- Book-period status panel: `figures/9-2/plots/book_period/figure_9_2_book_period_reconstruction.png`
- Extended status panel: `figures/9-2/plots/extended/figure_9_2_extended_reconstruction.png`
- Book-period comparison: `figures/9-2/plots/comparisons/figure_9_2_book_period_comparison.png`
- Extended comparison: `figures/9-2/plots/comparisons/figure_9_2_extended_comparison.png`

Canonical documentation:

- Caption: `figures/9-2/captions/caption.txt`
- Provenance: `figures/9-2/provenance/provenance.md`
- Anomaly review: `figures/9-2/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/9-2/metadata/metadata.json`
- Review checklist: `figures/9-2/review_checklist.md`

### Figure 9-3 - Inequality, UK and US, 1688-2013

Status: `manual_review_needed`

Canonical visual artifacts:

- Original reference: `figures/9-3/plots/comparisons/kindle_reference_figure_9_3.png`
- Book-period status panel: `figures/9-3/plots/book_period/figure_9_3_book_period_reconstruction.png`
- Extended status panel: `figures/9-3/plots/extended/figure_9_3_extended_reconstruction.png`
- Book-period comparison: `figures/9-3/plots/comparisons/figure_9_3_book_period_comparison.png`
- Extended comparison: `figures/9-3/plots/comparisons/figure_9_3_extended_comparison.png`

Canonical documentation:

- Caption: `figures/9-3/captions/caption.txt`
- Provenance: `figures/9-3/provenance/provenance.md`
- Anomaly review: `figures/9-3/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/9-3/metadata/metadata.json`
- Review checklist: `figures/9-3/review_checklist.md`

### Figure 9-4 - Social spending, OECD countries, 1880-2016

Status: `updated_equivalent`

Canonical visual artifacts:

- Original reference: `figures/9-4/plots/comparisons/kindle_reference_figure_9_4.png`
- Book-period reconstruction: `figures/9-4/plots/book_period/figure_9_4_book_period_reconstruction.png`
- Extended reconstruction: `figures/9-4/plots/extended/figure_9_4_extended_reconstruction.png`
- Book-period comparison: `figures/9-4/plots/comparisons/figure_9_4_book_period_comparison.png`
- Extended comparison: `figures/9-4/plots/comparisons/figure_9_4_extended_comparison.png`

Canonical documentation:

- Caption: `figures/9-4/captions/caption.txt`
- Provenance: `figures/9-4/provenance/provenance.md`
- Anomaly review: `figures/9-4/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/9-4/metadata/metadata.json`
- Review checklist: `figures/9-4/review_checklist.md`

### Figure 9-5 - Income gains, 1988-2008

Status: `manual_review_needed`

Canonical visual artifacts:

- Original reference: `figures/9-5/plots/comparisons/kindle_reference_figure_9_5.png`
- Book-period status panel: `figures/9-5/plots/book_period/figure_9_5_book_period_reconstruction.png`
- Extended status panel: `figures/9-5/plots/extended/figure_9_5_extended_reconstruction.png`
- Book-period comparison: `figures/9-5/plots/comparisons/figure_9_5_book_period_comparison.png`
- Extended comparison: `figures/9-5/plots/comparisons/figure_9_5_extended_comparison.png`

Canonical documentation:

- Caption: `figures/9-5/captions/caption.txt`
- Provenance: `figures/9-5/provenance/provenance.md`
- Anomaly review: `figures/9-5/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/9-5/metadata/metadata.json`
- Review checklist: `figures/9-5/review_checklist.md`

### Figure 9-6 - Poverty, US, 1960-2016

Status: `verified_reproduction`

Canonical visual artifacts:
- Original reference: `figures/9-6/plots/comparisons/pdf_reference_figure_9_6.png`
- Book-period reconstruction: `figures/9-6/plots/book_period/figure_9_6_book_period_reconstruction.png`
- Extended reconstruction: `figures/9-6/plots/extended/figure_9_6_extended_reconstruction.png`
- Book-period comparison: `figures/9-6/plots/comparisons/figure_9_6_book_period_comparison.png`
- Extended comparison: `figures/9-6/plots/comparisons/figure_9_6_extended_comparison.png`
Canonical documentation:
- Caption: `figures/9-6/captions/caption.txt`
- Provenance: `figures/9-6/provenance/provenance.md`
- Anomaly review: `figures/9-6/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/9-6/metadata/metadata.json`
- Review checklist: `figures/9-6/review_checklist.md`

### Figure 10-1 - Population and population growth, 1750-2015 and projected to 2100

Status: `updated_equivalent`

Canonical visual artifacts:
- Original reference: `figures/10-1/plots/comparisons/pdf_reference_figure_10_1.png`
- Book-period reconstruction: `figures/10-1/plots/book_period/figure_10_1_book_period_reconstruction.png`
- Extended reconstruction: `figures/10-1/plots/extended/figure_10_1_extended_reconstruction.png`
- Book-period comparison: `figures/10-1/plots/comparisons/figure_10_1_book_period_comparison.png`
- Extended comparison: `figures/10-1/plots/comparisons/figure_10_1_extended_comparison.png`
Canonical documentation:
- Caption: `figures/10-1/captions/caption.txt`
- Provenance: `figures/10-1/provenance/provenance.md`
- Anomaly review: `figures/10-1/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/10-1/metadata/metadata.json`
- Review checklist: `figures/10-1/review_checklist.md`

### Figure 10-2 - Sustainability, 1955-2109

Status: `updated_equivalent`

Canonical visual artifacts:
- Original reference: `figures/10-2/plots/comparisons/pdf_reference_figure_10_2.png`
- XKCD source image: `figures/10-2/plots/comparisons/xkcd_source_figure_10_2.png`
- Book-period reconstruction: `figures/10-2/plots/book_period/figure_10_2_book_period_reconstruction.png`
- Extended reconstruction: `figures/10-2/plots/extended/figure_10_2_extended_reconstruction.png`
- Book-period comparison: `figures/10-2/plots/comparisons/figure_10_2_book_period_comparison.png`
- Extended comparison: `figures/10-2/plots/comparisons/figure_10_2_extended_comparison.png`
- Visual reference comparison: `figures/10-2/plots/comparisons/figure_10_2_visual_reference_comparison.png`
- Candidate-corpus comparison: `figures/10-2/data/clean/figure_10_2_ngram_candidate_comparison.csv`
- Calibrated marker values: `figures/10-2/data/clean/figure_10_2_xkcd_calibrated_marker_values.csv`
Canonical documentation:
- Caption: `figures/10-2/captions/caption.txt`
- Provenance: `figures/10-2/provenance/provenance.md`
- Source log: `figures/10-2/source_logs/source_log.md`
- Anomaly review: `figures/10-2/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/10-2/metadata/metadata.json`
- Review checklist: `figures/10-2/review_checklist.md`


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

### Figure 12-3 - Motor vehicle accident deaths, US, 1921-2015

Status: `source_chain_recovered`

Canonical visual artifacts:

- Original reference: `figures/12-3/plots/comparisons/kindle_reference_figure_12_3.png`

Canonical documentation:

- Caption: `figures/12-3/captions/caption.txt`
- Provenance: `figures/12-3/provenance/provenance.md`
- Anomaly review: `figures/12-3/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/12-3/metadata/metadata.json`
- Review checklist: `figures/12-3/review_checklist.md`

### Figure 12-4 - Pedestrian deaths, US, 1927-2015

Status: `source_chain_recovered`

Canonical visual artifacts:

- Original reference: `figures/12-4/plots/comparisons/kindle_reference_figure_12_4.png`

Canonical documentation:

- Caption: `figures/12-4/captions/caption.txt`
- Provenance: `figures/12-4/provenance/provenance.md`
- Anomaly review: `figures/12-4/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/12-4/metadata/metadata.json`
- Review checklist: `figures/12-4/review_checklist.md`

### Figure 12-5 - Plane crash deaths, 1970-2015

Status: `partial_match`

Canonical visual artifacts:

- Original reference: `figures/12-5/plots/comparisons/kindle_reference_figure_12_5.png`
- Book-period reconstruction: `figures/12-5/plots/book_period/figure_12_5_book_period_reconstruction.png`
- Extended reconstruction: `figures/12-5/plots/extended/figure_12_5_extended_reconstruction.png`
- Book-period comparison: `figures/12-5/plots/comparisons/figure_12_5_book_period_comparison.png`
- Extended comparison: `figures/12-5/plots/comparisons/figure_12_5_extended_comparison.png`

Canonical documentation:

- Caption: `figures/12-5/captions/caption.txt`
- Provenance: `figures/12-5/provenance/provenance.md`
- Anomaly review: `figures/12-5/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/12-5/metadata/metadata.json`
- Review checklist: `figures/12-5/review_checklist.md`

### Figure 12-8 - Natural disaster deaths, 1900-2015

Status: `updated_equivalent`

Canonical visual artifacts:

- Original reference: `figures/12-8/plots/comparisons/kindle_reference_figure_12_8.png`
- Book-period reconstruction: `figures/12-8/plots/book_period/figure_12_8_book_period_reconstruction.png`
- Extended reconstruction: `figures/12-8/plots/extended/figure_12_8_extended_reconstruction.png`
- Book-period comparison: `figures/12-8/plots/comparisons/figure_12_8_book_period_comparison.png`
- Extended comparison: `figures/12-8/plots/comparisons/figure_12_8_extended_comparison.png`

Canonical documentation:

- Caption: `figures/12-8/captions/caption.txt`
- Provenance: `figures/12-8/provenance/provenance.md`
- Anomaly review: `figures/12-8/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/12-8/metadata/metadata.json`
- Review checklist: `figures/12-8/review_checklist.md`

### Figure 12-9 - Lightning strike deaths, US, 1900-2015

Status: `verified_reproduction`

Canonical visual artifacts:

- Original reference: `figures/12-9/plots/comparisons/kindle_reference_figure_12_9.png`
- Book-period reconstruction: `figures/12-9/plots/book_period/figure_12_9_book_period_reconstruction.png`
- Extended reconstruction: `figures/12-9/plots/extended/figure_12_9_extended_reconstruction.png`
- Book-period comparison: `figures/12-9/plots/comparisons/figure_12_9_book_period_comparison.png`
- Extended comparison: `figures/12-9/plots/comparisons/figure_12_9_extended_comparison.png`

Canonical documentation:

- Caption: `figures/12-9/captions/caption.txt`
- Provenance: `figures/12-9/provenance/provenance.md`
- Anomaly review: `figures/12-9/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/12-9/metadata/metadata.json`
- Review checklist: `figures/12-9/review_checklist.md`

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
| `1.13-remediate-figure-10-2-projection` | 2026-07-05 | Remediated Figure 10-2 projection consistency, candidate-corpus table, visual reference comparison, and status justification. |
| `1.12-production-loop-figure-10-2` | 2026-07-05 | Added Figure 10-2 as an updated-equivalent XKCD/Google Ngram reconstruction with current Ngram successor extension. |
| `1.11-source-recovery-figure-4-1` | 2026-07-05 | Processed Figure 4-1 as a documented source-recovery-blocked artifact; recovered Supplemental PDF source line and Leetaru/GDELT candidate visual evidence, but no underlying monthly data table. |
| `1.10-production-loop-figure-10-1` | 2026-07-01 | Added Figure 10-1 as an updated-equivalent current OWID/UN population and growth reconstruction. |
| `1.9-production-loop-figure-9-6` | 2026-07-01 | Added Figure 9-6 as a verified reconstruction from Meyer & Sullivan 2017 Table 1 with a dotted 2017 extension. |
| `1.8-production-loop-figure-8-3` | 2026-07-01 | Added Figure 8-3 as an updated-equivalent Gapminder Income Mountains v2 reconstruction with PDF side-by-side comparisons and full provenance package. |
| `1.7-production-loop-consolidation` | 2026-07-01 | Consolidated fragmented Track A, B, C, and D work onto the production-loop branch and normalized canonical status state against the latest visual review baseline. |
| `1.6-supplemental-graphics-reference` | 2026-06-30 | Added the Enlightenment Now Supplemental Graphics PDF as the canonical figure reference and updated README, workflow, review protocol, and project state to use it before Kindle. |
| `1.5-track-d-safety-mortality` | 2026-06-30 | Processed Track D figures 12-3, 12-4, 12-5, 12-8, and 12-9. Figures 12-8 and 12-9 received OWID/EM-DAT and NOAA/Lopez-Holle reconstructions; Figure 12-5 received a partial ASN/World Bank successor reconstruction; Figures 12-3 and 12-4 remain source-chain recovered pending exact historical NHTSA/FHWA/NCSA source tables. |
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
2. Open the canonical Supplemental Graphics PDF:
   [references/enlightenment_now_supplemental_graphics.pdf](references/enlightenment_now_supplemental_graphics.pdf).
3. Read [docs/figure_registry.md](docs/figure_registry.md) and consult
   [data/figure_registry.csv](data/figure_registry.csv).
4. Read [docs/review_protocol.md](docs/review_protocol.md) and
   [docs/review_checklist.md](docs/review_checklist.md).
5. Read [docs/editorial_review_gate.md](docs/editorial_review_gate.md).
6. Read [docs/pipeline.md](docs/pipeline.md) and [docs/workflow.md](docs/workflow.md).
7. Read the target figure directory, especially `metadata/metadata.json`,
   `provenance/provenance.md`, `source_logs/source_log.md`, and
   `discrepancy_logs/discrepancy_log.md`.
8. Update the relevant figure registry rows, this file, and
   [docs/lessons_learned.md](docs/lessons_learned.md)
   before finishing.
9. Whenever a figure plot, comparison image, caption, provenance file, anomaly
   review, metadata file, or status changes, update the corresponding paths and
   status in the `Canonical Figure Artifacts` section above.
10. Whenever Codex updates or reviews a figure, the final response must render
   the latest side-by-side comparison images inline, including both
   book-period and extended comparisons where available. GitHub remains the
   canonical archive, but rendered images in the Codex response are required
   for ChatGPT visual QA.
11. Codex must not stop after producing a side-by-side comparison if visible
   discrepancies remain that could plausibly be addressed through additional
   source recovery, transformation correction, styling correction, scaling
   correction, or extension-data review.
12. Codex must run the Editorial Review Gate before final commit and include an
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
## Track B Economic History Addendum

Last Track B update: 2026-06-30 America/Los_Angeles

Track B processed five food, poverty, and economic-history figures on branch `track-b-economic-history`.

| Figure | Title | Lifecycle stage | Status | Confidence | Current disposition |
| --- | --- | --- | --- | --- | --- |
| 7-3 | Undernourishment, 1970-2015 | source recovery and partial book period reconstruction | `partial_match` | Medium | Main developing-world line is source-supported; regional lines use available FAO/SOFI successor coverage with shorter time span. |
| 7-4 | Famine deaths, 1860-2016 | source supported reconstruction with denominator caveat | `partial_match` | Medium | The event table is recovered from OWID's famine dataset article; the decadal rate denominator uses current OWID world population interpolation. |
| 8-1 | Gross World Product, 1-2015 | book period reconstruction with successor extension | `updated_equivalent` | Medium-high | Live OWID successor reproduces the same shape and source family but extends past 2015 and may include revisions. |
| 8-2 | GDP per capita, 1600-2015 | book period reconstruction with successor extension | `updated_equivalent` | Medium | Current Maddison 2020/OWID successor data match the broad visual pattern but not the exact book-era source vintage. |
| 8-3 | World income distribution, 1800, 1975, and 2015 | Gapminder successor workbook reconstruction | `updated_equivalent` | Medium-high | Gapminder Income Mountains v2 source-family workbook reproduces the concept and shape, but exact book-era mountain tool snapshot remains unrecovered. |
| 8-5 | Extreme poverty (number), 1820-2015 | reviewed book period reconstruction no comparable extension | `verified_reproduction` | High | Book-period source family and visual encoding are reproduced; no comparable post-2015 extension is plotted. |

### Track B Completed/Verified

- Figure 8-5: verified book-period reconstruction of extreme-poverty counts from OWID/Roser & Ortiz-Ospina historical counts.

### Track B Unresolved Caveats

- Figure 7-3: exact Roser 2016j regional FAO 2014 vintage remains unresolved; current reconstruction is a partial source-family match.
- Figure 7-4: exact archived OWID 2017 decadal-rate output and denominator notes remain unresolved; event table is recovered.
- Figure 8-1 and 8-2: use live/current OWID successor series rather than exact 2016c/Maddison Project 2014 vintage.

### Track B Canonical Figure Artifacts

### Figure 7-3 - Undernourishment, 1970-2015

Status: `partial_match`

Canonical visual artifacts:

- Original reference: `figures/7-3/plots/comparisons/kindle_reference_figure_7_3.png`
- Book-period reconstruction: `figures/7-3/plots/book_period/figure_7_3_book_period_reconstruction.png`
- Extended reconstruction: `figures/7-3/plots/extended/figure_7_3_extended_reconstruction.png`
- Book-period comparison: `figures/7-3/plots/comparisons/figure_7_3_book_period_comparison.png`
- Extended comparison: `figures/7-3/plots/comparisons/figure_7_3_extended_comparison.png`

Canonical documentation:

- Caption: `figures/7-3/captions/caption.txt`
- Provenance: `figures/7-3/provenance/provenance.md`
- Anomaly review: `figures/7-3/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/7-3/metadata/metadata.json`
- Review checklist: `figures/7-3/review_checklist.md`


### Figure 7-4 - Famine deaths, 1860-2016

Status: `partial_match`

Canonical visual artifacts:

- Original reference: `figures/7-4/plots/comparisons/kindle_reference_figure_7_4.png`
- Book-period reconstruction: `figures/7-4/plots/book_period/figure_7_4_book_period_reconstruction.png`
- Extended reconstruction: `figures/7-4/plots/extended/figure_7_4_extended_reconstruction.png`
- Book-period comparison: `figures/7-4/plots/comparisons/figure_7_4_book_period_comparison.png`
- Extended comparison: `figures/7-4/plots/comparisons/figure_7_4_extended_comparison.png`

Canonical documentation:

- Caption: `figures/7-4/captions/caption.txt`
- Provenance: `figures/7-4/provenance/provenance.md`
- Anomaly review: `figures/7-4/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/7-4/metadata/metadata.json`
- Review checklist: `figures/7-4/review_checklist.md`


### Figure 8-1 - Gross World Product, 1-2015

Status: `updated_equivalent`

Canonical visual artifacts:

- Original reference: `figures/8-1/plots/comparisons/kindle_reference_figure_8_1.png`
- Book-period reconstruction: `figures/8-1/plots/book_period/figure_8_1_book_period_reconstruction.png`
- Extended reconstruction: `figures/8-1/plots/extended/figure_8_1_extended_reconstruction.png`
- Book-period comparison: `figures/8-1/plots/comparisons/figure_8_1_book_period_comparison.png`
- Extended comparison: `figures/8-1/plots/comparisons/figure_8_1_extended_comparison.png`

Canonical documentation:

- Caption: `figures/8-1/captions/caption.txt`
- Provenance: `figures/8-1/provenance/provenance.md`
- Anomaly review: `figures/8-1/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/8-1/metadata/metadata.json`
- Review checklist: `figures/8-1/review_checklist.md`


### Figure 8-2 - GDP per capita, 1600-2015

Status: `updated_equivalent`

Canonical visual artifacts:

- Original reference: `figures/8-2/plots/comparisons/kindle_reference_figure_8_2.png`
- Book-period reconstruction: `figures/8-2/plots/book_period/figure_8_2_book_period_reconstruction.png`
- Extended reconstruction: `figures/8-2/plots/extended/figure_8_2_extended_reconstruction.png`
- Book-period comparison: `figures/8-2/plots/comparisons/figure_8_2_book_period_comparison.png`
- Extended comparison: `figures/8-2/plots/comparisons/figure_8_2_extended_comparison.png`

Canonical documentation:

- Caption: `figures/8-2/captions/caption.txt`
- Provenance: `figures/8-2/provenance/provenance.md`
- Anomaly review: `figures/8-2/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/8-2/metadata/metadata.json`
- Review checklist: `figures/8-2/review_checklist.md`


### Figure 8-5 - Extreme poverty (number), 1820-2015

Status: `verified_reproduction`

Canonical visual artifacts:

- Original reference: `figures/8-5/plots/comparisons/kindle_reference_figure_8_5.png`
- Book-period reconstruction: `figures/8-5/plots/book_period/figure_8_5_book_period_reconstruction.png`
- Extended reconstruction: `figures/8-5/plots/extended/figure_8_5_extended_reconstruction.png`
- Book-period comparison: `figures/8-5/plots/comparisons/figure_8_5_book_period_comparison.png`
- Extended comparison: `figures/8-5/plots/comparisons/figure_8_5_extended_comparison.png`

Canonical documentation:

- Caption: `figures/8-5/captions/caption.txt`
- Provenance: `figures/8-5/provenance/provenance.md`
- Anomaly review: `figures/8-5/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/8-5/metadata/metadata.json`
- Review checklist: `figures/8-5/review_checklist.md`
## Track B Editorial Remediation Addendum

Date: 2026-06-30

| Figure | Prior status | Remediated status | Confidence | Editorial decision |
| --- | --- | --- | --- | --- |
| 7-3 | `partial_match` | `partial_match` | medium-low | Retain partial_match and lower confidence. |
| 7-4 | `partial_match` | `partial_match` | medium-low | Retain partial_match and lower confidence. |
| 8-1 | `updated_equivalent` | `updated_equivalent` | medium | Do not promote to verified_reproduction. |
| 8-2 | `updated_equivalent` | `updated_equivalent` | medium | Retain updated_equivalent. |
| 8-5 | `verified_reproduction` | `verified_reproduction` | high | Retain verified_reproduction. |

See `reports/track_b_editorial_remediation.md` for the full reviewer challenge, scorecards, comparison images, and remaining blockers.
