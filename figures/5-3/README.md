<!-- canonical-state:start -->
# Figure 5-3: Maternal mortality, 1751-2013

Scientific status: `partial_match`. Execution: `accepted`.
Publication: `not_reviewed`. Artifact kind: `reconstruction`.

This generated summary and [figure.json](figure.json) supersede historical status claims below.
A historical verified classification is not a fresh publication review.

- Original reference: [plots/comparisons/kindle_reference_figure_5_3.png](plots/comparisons/kindle_reference_figure_5_3.png)
- Book period reconstruction: [plots/book_period/figure_5_3_book_period_reconstruction.png](plots/book_period/figure_5_3_book_period_reconstruction.png)
- Extended reconstruction: [plots/extended/figure_5_3_same_source_continuation.png](plots/extended/figure_5_3_same_source_continuation.png)
- Book period comparison: [plots/comparisons/figure_5_3_book_period_comparison.png](plots/comparisons/figure_5_3_book_period_comparison.png)
- Extended comparison: [plots/comparisons/figure_5_3_extended_comparison.png](plots/comparisons/figure_5_3_extended_comparison.png)
- Caption: [captions/caption.txt](captions/caption.txt)
- Provenance: [provenance/provenance.md](provenance/provenance.md)
- Anomaly review: [anomaly_reviews/anomaly_review.md](anomaly_reviews/anomaly_review.md)
- Review checklist: [review_checklist.md](review_checklist.md)
- Source log: [source_logs/source_log.md](source_logs/source_log.md)
- Search log: [search_iterations/search_iterations.md](search_iterations/search_iterations.md)
- Discrepancy log: [discrepancy_logs/discrepancy_log.md](discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [metadata/metadata.json](metadata/metadata.json)
- Metadata: [figure.json](figure.json)

<!-- canonical-state:end -->

# Figure 5-3: Maternal mortality, 1751-2013

Status: `partial_match` -- strong book-period data reconstruction (exact conversion validation); visual comparison uses a disclosed facsimile reference, not original book pixels.

The reconstruction uses the preserved Our World in Data dataset 522, which
combines Gapminder's 2010 historical compilation with World Bank 2015 values
without adjustment. The supplemental PDF was located through its indexed
College Sidekick record, but its original pixels could not be downloaded in
this run because the host returned a Cloudflare denial. The reference image in
this package is therefore explicitly labeled as an evidence-based facsimile,
not an original page capture.

Run with:

```sh
PYTHONPATH=tmp/pydeps python3 scripts/reconstruct_5_3.py
```

The script assumes `matplotlib` and `Pillow` are available. It never uses
digitized chart values.
