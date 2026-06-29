# Provenance Summary: Figure 10-6

- Best-current reconstruction: archived World Bank WDI bulk ZIP from 2017-10-12 Wayback snapshot.
- Candidate diagnostic: current WDI exports, shown separately to document why they are not adequate for exact reproduction.
- Why verified: archived WDI values reproduce the book's 1990, 2000, and 2014 land/marine protected-area trends within visual and numeric tolerance.
- Status: verified_reproduction.
- Source fidelity: A/B. The archived WDI release matches the cited institution and book-range values; exact bibliography wording still merits final bibliographic confirmation.
- Regeneration command: `/Users/alfred/Documents/MIsc/.venv/bin/python scripts/iterative_source_recovery.py`.

## Research Mode Provenance Update
- No regression to reconstruction. Archived WDI 2017 remains the accepted source.
- Current WDI and UNSD candidates remain diagnostic/rejected for exact reproduction.

## Book-Style Reconstruction Update
- Date: 2026-06-28
- Book-period reconstruction: `outputs/book_style/book_period/figure_10_6_book_period_reconstruction.png`.
- Extended reconstruction: `outputs/book_style/extended/figure_10_6_extended_reconstruction.png`.
- Original-vs-book comparison: `outputs/book_style/validation/figure_10_6_book_style_comparison.png`.
- Original-vs-extended comparison: `outputs/book_style/validation/figure_10_6_extended_comparison.png`.
- Captioned original-vs-book comparison: `outputs/book_style/validation/figure_10_6_book_style_comparison_captioned.png`.
- Captioned original-vs-extended comparison: `outputs/book_style/validation/figure_10_6_extended_comparison_captioned.png`.
- Caption: `outputs/book_style/captions/figure_10_6_caption.txt`.
- Visual anomaly review: `outputs/book_style/anomaly_reviews/figure_10_6_anomaly_review.md`.
- The book-period reconstruction preserves the archived WDI source and restyles the chart to match the book.
- Update period: book-period solid lines run through 2014; post-book dotted lines use current WDI successor values through 2025 and are dashed to avoid implying book-period provenance.
- The marine extension is visibly separated and labeled as a current WDI successor series because current WDI revises/rebases the 2014 marine value downward relative to the archived WDI book-period release.
