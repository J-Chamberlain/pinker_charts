# Anomaly Review: Figure 10-2

## Data Fidelity
- Observed values come from Google Ngram API output, not from digitizing the book figure.
- The source-family data are recovered, but XKCD's exact hand-drawn regression and projection geometry are not published.
- Classification: `updated_equivalent`, not `verified_reproduction`. This status is justified by recovered official XKCD/PDF references plus Ngram source-family data, with the projection mismatch explicitly quantified.

## Visual Fidelity
- The recreated chart preserves the log y-scale, year range, Ngram data dots, extrapolated future line, and XKCD-style annotations.
- The solid future line and open-circle markers now come from the same XKCD-label visual calibration. The 2036 marker is approximately 0.097% from that calibration, not an independently placed 0.1% point.
- Remaining differences are expected: handwritten typography, exact line wobble, and annotation placement are approximate. The three labeled future points are not exactly collinear on a log scale, so the calibrated straight line has small residuals at the labels.

## Quantitative Candidate Review
- `figure_10_2_ngram_candidate_comparison.csv` compares available Google Ngram candidates by 2008 frequency, fitted slope, and implied threshold years for once per page, once per sentence, and 100%.
- The 2009/v1 corpus gives the closest 100% year to XKCD's 2109 label, but its data-only fit implies once per page around 2044.7, not 2036.
- The 2012/v2 and current en-US-2019 candidates imply still later threshold years, so they are poorer matches to the XKCD label geometry.

## Extension Clarity
- The extended comparison separates current Ngram successor observations with open circles and a dashed gray fit.
- The current corpus revises the slope and should not be read as the original XKCD data vintage.

## Editorial Review Gate
- Critical issues: none.
- Major issues: none unexplained.
- Minor issues: hand-drawn styling, exact projection geometry, and small residuals against XKCD's non-collinear labels remain documented.

Overall confidence:
- Book reconstruction: medium-high for source-family data, medium for exact XKCD projection geometry
- Extension: medium; current Ngram corpus is a successor, not the original source vintage
- Source provenance: high for XKCD and Google Ngram source chain
- Outstanding risks: no author-supplied regression parameters or raw XKCD plotting file recovered
- Recommended next action: archive the live Google Ngram responses or locate an archived Ngram endpoint capture from January 2012
