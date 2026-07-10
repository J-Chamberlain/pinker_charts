# Discrepancy Log: Figure 5-4

Visual review date: 2026-07-09

Reference: `plots/comparisons/supplemental_pdf_reference_figure_5_4.png`

Comparison reviewed: `plots/comparisons/figure_5_4_book_period_comparison.png`

## Major Discrepancies

- The printed figure has ten series; the current artifact has three.
- Missing printed series: age 1, 5, 10, 20, 30, 40, 50, 60, and 70.
- Current partial age series are age 15 and age 45, which are available in the local OWID/HMD file but are not the printed labels.
- The printed post-1845 age-specific lines use mid-decade HMD-style values through 2013; the recovered local age-specific file stops at 2011 for the United Kingdom.
- The current artifact therefore cannot be judged visually faithful to the book figure.

## Resolved / Improved In This Run

- Replaced the comparison reference with a Supplemental PDF crop rather than relying only on the older Kindle-named reference.
- Rebuilt the at-birth line so values from 1845 onward use the recovered HMD-style mid-decade subset instead of annual successor values.
- Added source-recovery status text directly under the recreated plot.
- Added source-audit tables documenting HMD access and current OWID successor incompatibility.

## Final Classification

`needs_targeted_source_recovery`. The current artifact is useful for documenting partial recovery only; it is not a reconstructed, extended, or verified reproduction of the printed figure.
