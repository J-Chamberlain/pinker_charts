# Provenance Summary: Figure 10-5

Last updated: 2026-07-09

## Status

- Current status: `partial_match`
- Lifecycle stage: source recovery and discrepancy analysis
- Do not describe as verified, reconstructed from original annual data, or extended.

## What This Run Recovered

- The Supplemental Graphics PDF source note and explanatory text were checked directly.
- The Roser 2016r bibliography mapping remains a candidate entry, not a fully recovered OWID 2016 dataset.
- The OWID/ITOPF annual spill-count CSV supports the black line.
- The Internet Archive preserved the ITOPF 2016 statistics page and source chart image `seaborne_16.JPG`.
- The archived ITOPF chart image identifies the gray-line source family as UNCTADStat seaborne oil trade / total crude oil, petroleum product and gas loaded.
- The 2017 ITOPF statistics PDF confirms the same chart concept and UNCTADStat label.

## Derived Data

- `figures/10-5/data/clean/figure_10_5_oil_spills_clean.csv`: annual ITOPF/OWID spill counts, 1970-2016.
- `figures/10-5/data/candidates/itopf_archived_seaborne_16_digitized_oil_loaded.csv`: oil-loaded values digitized from the archived ITOPF chart image.
- `figures/10-5/data/candidates/itopf_digitized_vs_unctad_rmt2020_selected_year_validation.csv`: selected-year validation against UNCTAD Review of Maritime Transport 2020.

The digitized oil-loaded line is calibrated to the archived chart's printed axes. It is a diagnostic reconstruction input, not original tabular UNCTADStat data. Selected-year validation against RMT 2020 gives mean absolute difference 0.058 billion metric tons and maximum absolute difference 0.194.

## Current Visual Artifacts

- Book-period reconstruction: `figures/10-5/plots/book_period/figure_10_5_book_period_reconstruction.png`
- Book-period comparison: `figures/10-5/plots/comparisons/figure_10_5_book_style_comparison_captioned.png`
- Extended artifact: `figures/10-5/plots/extended/figure_10_5_extended_reconstruction.png`
- Extended comparison: `figures/10-5/plots/comparisons/figure_10_5_extended_comparison_captioned.png`

The extended artifact is intentionally a no-extension status panel. No post-2016 line is plotted.

## Remaining Blocker

The original annual UNCTADStat oil-loaded table behind Roser 2016r / ITOPF Figure 10-5 has not been recovered. The archive trail supports the source family and visual shape, but the gray-line values remain image-derived. A future verification run needs either:

- an archived OWID/Roser 2016r data bundle containing both series,
- a legacy UNCTADStat export for the total crude oil, petroleum product, and gas loaded series, or
- an ITOPF/UNCTAD source table corresponding to the archived chart.

## Regeneration

Run:

```bash
/Users/alfred/Documents/MIsc/.venv/bin/python scripts/reconstruct_10_5.py
```
