# Anomaly Review: Figure 8-3

## Visible Differences
- The recreated plot captures the log-scaled income distribution, the 1800/1975/2015 ordering, relative population-weighted curve heights, and the poverty cutoff.
- The exact curve smoothing and arrow/label placement differ from the book.
- The 1975 camel-shape is source-family similar but not pixel-identical, and its left peak is lower relative to 2015 than in the PDF reference.

## Cause Assessment
- Status: `updated_equivalent`.
- Main limitation is source vintage: Gapminder Income Mountains v2 is a successor workbook, not a proven book-era export.
- An initial normalized-share rendering made the 1800 curve visibly too tall; the pipeline corrected this by multiplying income-bin shares by workbook population.

## Reviewer Challenge
- Pinker would likely ask whether the exact Ola Rosling mountain snapshot was recovered.
- A data journalist would ask for the workbook and transformation script, both included.
- A peer reviewer would ask whether the y-axis normalization matches the mountain tool rendering.
- A skeptical reader would notice small differences in curve smoothing and label geometry.

Overall confidence:
- Book reconstruction: medium-high
- Extension: none plotted
- Source provenance: medium-high source-family match, not exact snapshot
- Outstanding risks: exact 2017 data/rendering snapshot unrecovered
- Recommended next action: archive search for the original mountain tool data snapshot
