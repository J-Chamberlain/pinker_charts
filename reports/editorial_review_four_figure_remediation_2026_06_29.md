# Editorial Review: Four-Figure Remediation

Date: 2026-06-29

Target figures: 5-1, 5-2, 8-4, 19-1.

This review remediates the latest four-figure batch without starting any new
figures.

## Figure 5-1 - Life expectancy

Status after remediation: `verified_reproduction`

Critical issues found:

- None.

Major issues found:

- The extended comparison previously risked implying a true post-2015 regional
  extension even though no comparable regional successor series was plotted.

Issues corrected:

- The extended reconstruction now visibly states that no comparable extension is
  plotted.
- Caption, anomaly review, registry row, and project state now describe the
  extended image as a review artifact rather than a true extension.

Remaining issues:

- Minor styling and label-placement differences.

Publication decision:

- Acceptable for book-period reconstruction. Do not describe the extended image
  as a true extension unless comparable regional successor data are recovered.

## Figure 5-2 - Child mortality

Status after remediation: `partial_match`

Critical issues found:

- None.

Major issues found:

- The previous reconstruction visibly failed to match the Kindle figure closely
  enough.
- The previous extension divided the current OWID selected child-mortality
  values by 10 even though the downloaded grapher reports percent units.

Issues corrected:

- Replaced the plotted proxy with the current OWID selected child-mortality
  grapher values in percent units.
- Regenerated book-period, extended, and side-by-side comparison images.
- Updated caption, anomaly review, registry row, and metadata to preserve
  `partial_match` status and identify the exact Roser 2016a UN/HMD assembly as
  unresolved.

Remaining issues:

- Exact book-era Roser 2016a dataset remains unrecovered.
- Some country trajectories and endpoint labels still differ visibly from the
  Kindle figure.

Publication decision:

- Not verified. Acceptable only as a documented partial match and source
  recovery target.

## Figure 8-4 - Extreme poverty

Status after remediation: `verified_reproduction`

Critical issues found:

- None.

Major issues found:

- The recreated plot area appeared too small in the previous comparison image.
- The extended segment needed clearer handling and explanation.

Issues corrected:

- Regenerated side-by-side comparisons with equal-sized image panels and trimmed
  whitespace.
- Removed the implied successor extension when no directly comparable World
  row was available in the local successor source.
- Caption and anomaly review now state that no comparable extension is plotted.

Remaining issues:

- Minor styling difference: the book separates historical and World Bank
  segments more distinctly than the single-line reconstruction.

Publication decision:

- Acceptable for book-period reconstruction. Extension remains absent and
  explicitly documented.

## Figure 19-1 - Nuclear weapons

Status after remediation: `partial_match`

Critical issues found:

- The prior comparison did not include the actual Kindle chart image, so visual
  validation could not pass.

Issues corrected:

- Captured the actual Kindle chart-page crop and regenerated both side-by-side
  comparisons.
- Removed placeholder-capture language from the review checklist and anomaly
  review.
- Downgraded visual validation to `poor` because the current reconstruction is
  a line chart while the Kindle figure is a stacked-area chart.

Remaining issues:

- The cited HumanProgress static 2927/FAS 2016 table remains unrecovered.
- The current OWID successor line reconstruction captures the broad trend but
  does not reproduce the original visual encoding.

Publication decision:

- Not verified. It remains a documented partial match; recover the cited source
  and reconstruct as stacked area before visual validation can pass.

## Cross-Figure Editorial Review

Weakest figure: Figure 19-1, because the actual Kindle chart now reveals a
major chart-type mismatch.

Most concerning figure for a reviewer: Figure 5-2, because it improved
materially but still depends on a modern/current OWID proxy rather than the
exact book-era Roser 2016a source.

Batch acceptance:

- No Critical issues remain.
- Major issues that remain are explicitly documented as source or chart-type
  blockers.
- The batch is acceptable as a remediated repository state, but not all figures
  are publication-ready verified reproductions.
