# Track A Health And Nutrition Summary

Branch: `track-a-health-nutrition`

Date: 2026-06-30

Figures processed:

- Figure 5-3: Maternal mortality, 1751-2013
- Figure 5-4: Life expectancy, UK, 1701-2013
- Figure 6-1: Childhood deaths from infectious disease, 2000-2013
- Figure 7-1: Calories, 1700-2013
- Figure 7-2: Childhood stunting, 1966-2014

## Summary

This was a time-boxed five-figure batch. It produced reproducible figure
directories, raw and clean data files, book-period and extended plots,
side-by-side comparison images, source logs, provenance files, anomaly reviews,
lineage files, review checklists, metadata, and checksums. A supplemental PDF
reference was later used to refresh the book-reference crops for all five
figures, including Figure 6-1.

No Track A figure was promoted to `verified_reproduction`.

## Figure Outcomes

### Figure 5-3

Status: `partial_match`

Book evidence: supplemental PDF page 3 crop; Kindle page had previously been
inspected.

Dataset used: current OWID maternal mortality ratio dataset, including
Gapminder/World Bank/WHO/OECD successor columns.

Result: broad visual match after converting maternal mortality ratio per
100,000 live births to percent of mothers dying in childbirth. The exact Roser
2016p/Gapminder source vintage was not recovered, so the figure remains a
partial match.

### Figure 5-4

Status: `needs_targeted_source_recovery`

Book evidence: supplemental PDF page 4 crop with full source line.

Dataset used: partial OWID/HMD-derived age-specific life-expectancy sources.

Result: not visually adequate. The original chart contains many age-specific
series; the reconstruction only includes at-birth, age-15, and age-45 proxy
series. This needs targeted recovery of the exact HMD/OWID age-specific data.

### Figure 6-1

Status: `blocked_external_source`

Book evidence: supplemental PDF page 4 crop with full source line. Kindle
navigation had failed during the original time-box, but the PDF reference now
allows visual side-by-side review.

Dataset used: IHME 2017 causes of child mortality proxy.

Result: side-by-side comparison now uses the book figure reference, but the
reconstruction remains blocked as a source-data reproduction because the cited
CHERG/WHO Liu et al. 2014 supplementary appendix has not been recovered. The
current plot is an IHME proxy and visibly does not match the book's line chart.

### Figure 7-1

Status: `partial_match`

Book evidence: supplemental PDF page 5 crop; Kindle page had previously been
inspected.

Dataset used: OWID daily calorie supply dataset based on FAO and historical
sources.

Result: plausible book-period reconstruction and successor extension, but line
geometry and source vintage/styling differ enough that this should remain a
partial match.

### Figure 7-2

Status: `partial_match`

Book evidence: supplemental PDF page 5 crop; Kindle page had previously been
inspected.

Dataset used: World Bank stunting prevalence indicator
`SH.STA.STNT.ZS` as a proxy.

Result: visually plausible for several series, but it is not the exact
OWID/Roser 2016j WHO Nutrition Landscape Information System vintage cited in
the book.

## Editorial Review Summary

Critical issues found:

- None remain after the supplemental PDF reference refresh.

Major issues found:

- Figure 5-4 is visibly incomplete because the exact age-specific source series
  were not recovered.
- Figure 6-1 uses a proxy source and remains a major visible mismatch to the
  book line chart.
- Figures 5-3, 7-1, and 7-2 use updated or proxy source vintages rather than
  proven exact book-era datasets.

Minor issues found:

- Label placement and typography are approximate across the batch.
- Some endpoint labels crowd the plot edges.

Issues automatically corrected:

- Corrected Figure 6-1 proxy values after noticing the first reconstruction had
  multiplied already-percent IHME values by 100.
- Replaced the Figure 6-1 placeholder reference with the supplied supplemental
  PDF crop and regenerated both side-by-side comparisons.
- Refreshed all five Track A book-reference crops from the supplemental PDF for
  consistent side-by-side review.

Issues remaining:

- Exact source-vintage recovery is still needed for all five figures before any
  can be considered verified.
- Figure 6-1 still needs the cited external appendix or an archival equivalent;
  the book-reference image is now available from the supplemental PDF.

Publication decision:

- The batch is acceptable as a documented branch-local partial/blocked Track A
  pass. It is not publication-ready as verified reconstruction work.
