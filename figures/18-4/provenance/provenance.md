# Figure 18-4 provenance

Current transformations and report-table extraction are in
[the September 11 remediation](../remediation_2026_09_11.md), superseding the
vintage-only explanation below. Book candidate: unweighted. Successor: WTSSPS.

## Book evidence

- Title: `Happiness and excitement, US, 1972-2016`.
- Book source line: “General Social Survey,” Smith, Son, & Schapiro 2015, figs. 1 and 5, updated for 2016 from the NORC GSS Data Explorer variable page. Data exclude nonresponses.
- Stored reference: `references/figures/figure_18_4.png`, cropped from the Supplemental Graphics PDF.

## Recovered source chain

`Enlightenment Now Figure 18-4` -> `Smith, Son, & Schapiro (2015), Trends in Psychological Well-Being, 1972-2014, figs. 1 and 5` -> `NORC General Social Survey` -> `current cumulative Stata release GSS_stata.zip` -> `scripts/reconstruct_18_4.py` -> clean summary CSV -> plots and comparisons.

The official NORC report was recovered at https://www.norc.org/content/dam/norc-org/pdfs/GSS_PsyWellBeing15_final_formatted.pdf. The current raw release was downloaded from https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_stata.zip on 2026-09-10.

## Transformations

The script reads only `year`, `happy`, and `life` from the Stata file. For each year it drops missing responses and calculates `100 * mean(variable == 1)`. No values were transcribed from the Pinker chart, interpolated, or digitized.

## Fidelity assessment

The source family, variables, broad magnitudes, and long-run shape agree with the reference. The current-release values differ modestly from the 2015 report tables, and the LIFE series has survey-year gaps. Those differences prevent `verified_reproduction`; the result is classified `updated_equivalent`.
