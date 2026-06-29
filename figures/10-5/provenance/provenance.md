# Provenance Summary: Figure 10-5

- Best-current reconstruction: spill counts only.
- Candidate diagnostic: partial UNCTAD oil-shipped-by-sea series, 2000-2016.
- Why separated: the partial UNCTAD series does not cover 1970-1999 and worsens the visual comparison if presented as faithful reconstruction.
- Status: partial_match.
- Source fidelity: B/C. Spill-count source is an exact-publication candidate; oil-shipping source is an institutional successor/partial candidate.
- Regeneration command: `/Users/alfred/Documents/MIsc/.venv/bin/python scripts/iterative_source_recovery.py`.

## Research Mode Provenance Update
- Added `data/candidates/unctad_rmt2020_tanker_trade_selected_years.csv`.
- Added `outputs/diagnostics/figure_10_5_rmt_tanker_trade_selected_years_diagnostic.png`.
- RMT selected-year values are diagnostic evidence only and are not used in the side-by-side validation plot.

## Book-Style Reconstruction Update
- Date: 2026-06-28
- Book-period reconstruction: `outputs/book_style/book_period/figure_10_5_book_period_reconstruction.png`.
- Extended reconstruction: `outputs/book_style/extended/figure_10_5_extended_reconstruction.png`.
- Original-vs-book comparison: `outputs/book_style/validation/figure_10_5_book_style_comparison.png`.
- Original-vs-extended comparison: `outputs/book_style/validation/figure_10_5_extended_comparison.png`.
- Captioned original-vs-book comparison: `outputs/book_style/validation/figure_10_5_book_style_comparison_captioned.png`.
- Captioned original-vs-extended comparison: `outputs/book_style/validation/figure_10_5_extended_comparison_captioned.png`.
- Caption: `outputs/book_style/captions/figure_10_5_caption.txt`.
- Visual anomaly review: `outputs/book_style/anomaly_reviews/figure_10_5_anomaly_review.md`.
- The main reconstruction now uses ITOPF/OWID spill counts and an annual UNCTADStat mirror for World crude oil loaded plus other tanker trade loaded.
- Update period: book-period solid lines run through 2016; post-book dotted lines show tanker trade through 2020 and spill counts through 2025.
- ITOPF's current Figure 4 source trail says 1970-1999 tanker trade comes from UNCTADStat updated 2022 and 2000-2023 from UNCTADStat updated 2025. The public mirror recovers annual values through 2020. The accessible live UNCTAD API was investigated for 2021-2023 but rejected from the main plot because overlap values are not on the same scale as ITOPF/RMT/book values.
