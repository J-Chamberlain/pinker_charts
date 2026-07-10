# Figure 5-4: Life expectancy, UK, 1701-2013

Status: `needs_targeted_source_recovery`
Lifecycle stage: `track_a_timeboxed_reconstruction`

Targeted recovery update, 2026-07-09:

- Supplemental PDF page 4 was rendered and cropped to `plots/comparisons/supplemental_pdf_reference_figure_5_4.png`.
- The HMD England & Wales total-population country page, background documentation, and country-code table were recovered.
- Direct HMD raw life-table files such as `bltper_1x1.txt` redirect to the HMD login page in this run, so the exact book-age HMD values could not be independently recovered from HMD.
- Current OWID successor data were downloaded and audited, but they expose only at-birth, age-10, age-25, age-45, age-65, and age-80 total life expectancy and switch to UN WPP after 1950. They are not a comparable extension for the printed age set.
- The canonical comparison images are refreshed as partial source-recovery artifacts, not verified reproductions.

## Documentation / Status Evidence

The protected registry row and JSON registry row both record `current_status=needs_targeted_source_recovery` and `lifecycle_stage=track_a_timeboxed_reconstruction`. `PROJECT_STATE.md` and `metadata/metadata.json` now carry the same status evidence. The figure is not promoted because the exact OWID/Roser 2016n age-specific export or an authenticated/archived HMD vintage with the printed age set remains unrecovered.

Current clean CSV outputs:

- `data/clean/figure_5_4_book_period_clean.csv`
- `data/clean/figure_5_4_extended_clean.csv`
- `data/clean/figure_5_4_source_recovery_audit.csv`
- `data/clean/figure_5_4_current_owid_successor_availability.csv`

Current comparison/reference images:

- `plots/comparisons/supplemental_pdf_reference_figure_5_4.png`
- `plots/comparisons/kindle_reference_figure_5_4.png`
- `plots/comparisons/figure_5_4_book_period_comparison.png`
- `plots/comparisons/figure_5_4_extended_comparison.png`

## Canonical Artifacts

- Supplemental PDF reference: `plots/comparisons/supplemental_pdf_reference_figure_5_4.png`
- Original reference: `plots/comparisons/kindle_reference_figure_5_4.png`
- Book-period reconstruction: `plots/book_period/figure_5_4_book_period_reconstruction.png`
- Extended reconstruction: `plots/extended/figure_5_4_extended_reconstruction.png`
- Book-period comparison: `plots/comparisons/figure_5_4_book_period_comparison.png`
- Extended comparison: `plots/comparisons/figure_5_4_extended_comparison.png`
- Caption: `captions/caption.txt`
- Provenance: `provenance/provenance.md`
- Anomaly review: `anomaly_reviews/anomaly_review.md`
- Metadata: `metadata/metadata.json`
