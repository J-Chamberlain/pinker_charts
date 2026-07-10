# Figure 10-5

Title: Oil spills, 1970-2016

Current status: `partial_match`

## Summary

Figure 10-5 has been attempted through source recovery, book-style plotting,
extension plotting, visual comparison, and discrepancy analysis. The oil-spill
count series is well supported. The exact historical oil-shipped-by-sea or
tanker-trade annual series used for the book-period gray line has not been
recovered, so the current book-period artifact plots the verified spill-count
line only and labels the missing gray line explicitly.

Do not classify this figure as `verified_reproduction` until the full
1970-2016 oil-shipping source is recovered or an exact archival equivalent is
located.

## Key Files

- [metadata/metadata.json](metadata/metadata.json)
- [provenance/provenance.md](provenance/provenance.md)
- [source_logs/source_log.md](source_logs/source_log.md)
- [search_iterations/search_iterations.md](search_iterations/search_iterations.md)
- [discrepancy_logs/discrepancy_log.md](discrepancy_logs/discrepancy_log.md)
- [anomaly_reviews/anomaly_review.md](anomaly_reviews/anomaly_review.md)
- [captions/caption.txt](captions/caption.txt)
- [plots/book_period/](plots/book_period/)
- [plots/extended/](plots/extended/)
- [plots/comparisons/](plots/comparisons/)
- [plots/diagnostics/](plots/diagnostics/)
- [checksums/](checksums/)

## Main Blocker

The public evidence has not yet established the exact annual right-axis series
for oil shipped by sea from 1970 through 2016.

## Latest Source-Recovery Result

This run recovered the current UNCTADStat `US.SeaborneTrade` public bulk file
and metadata. The live bulk file is labeled `From 2000 to 2024`, so it cannot
cover 1970-1999. Its World cargo 11+12 values also differ from UNCTAD Review
of Maritime Transport 2020 selected-year tanker-trade values by about 31-48
percent on overlap. It is therefore retained as rejected successor/source-family
evidence, not as reconstruction input.

## Canonical Artifacts

These paths must match the Figure 10-5 entry in
[../../PROJECT_STATE.md](../../PROJECT_STATE.md).

Canonical visual artifacts:

- Original reference: [plots/comparisons/corrected_figure_10_5_book_crop.png](plots/comparisons/corrected_figure_10_5_book_crop.png)
- Book-period reconstruction: [plots/book_period/figure_10_5_book_period_reconstruction.png](plots/book_period/figure_10_5_book_period_reconstruction.png)
- Extended reconstruction: [plots/extended/figure_10_5_extended_reconstruction.png](plots/extended/figure_10_5_extended_reconstruction.png)
- Book-period comparison: [plots/comparisons/figure_10_5_book_style_comparison_captioned.png](plots/comparisons/figure_10_5_book_style_comparison_captioned.png)
- Extended comparison: [plots/comparisons/figure_10_5_extended_comparison_captioned.png](plots/comparisons/figure_10_5_extended_comparison_captioned.png)
- Diagnostic plot: [plots/diagnostics/figure_10_5_unctad_partial_oil_shipping_diagnostic.png](plots/diagnostics/figure_10_5_unctad_partial_oil_shipping_diagnostic.png)
- Diagnostic plot: [plots/diagnostics/figure_10_5_rmt_tanker_trade_selected_years_diagnostic.png](plots/diagnostics/figure_10_5_rmt_tanker_trade_selected_years_diagnostic.png)

Canonical documentation:

- Caption: [captions/caption.txt](captions/caption.txt)
- Provenance: [provenance/provenance.md](provenance/provenance.md)
- Anomaly review: [anomaly_reviews/anomaly_review.md](anomaly_reviews/anomaly_review.md)
- Metadata: [metadata/metadata.json](metadata/metadata.json)
