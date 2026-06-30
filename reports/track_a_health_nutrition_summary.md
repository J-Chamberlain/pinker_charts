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
lineage files, review checklists, metadata, and checksums.

No Track A figure was promoted to `verified_reproduction`.

## Figure Outcomes

### Figure 5-3

Status: `partial_match`

Kindle evidence: chart page and source line captured.

Dataset used: current OWID maternal mortality ratio dataset, including
Gapminder/World Bank/WHO/OECD successor columns.

Result: broad visual match after converting maternal mortality ratio per
100,000 live births to percent of mothers dying in childbirth. The exact Roser
2016p/Gapminder source vintage was not recovered, so the figure remains a
partial match.

### Figure 5-4

Status: `needs_targeted_source_recovery`

Kindle evidence: chart page captured, but full source line was not visible in
the screenshot.

Dataset used: partial OWID/HMD-derived age-specific life-expectancy sources.

Result: not visually adequate. The original chart contains many age-specific
series; the reconstruction only includes at-birth, age-15, and age-45 proxy
series. This needs targeted recovery of the exact HMD/OWID age-specific data.

### Figure 6-1

Status: `blocked_external_source`

Kindle evidence: chart-page capture failed during the time-box.

Dataset used: IHME 2017 causes of child mortality proxy.

Result: generated only as a blocked proxy artifact. The cited CHERG/WHO Liu et
al. 2014 supplementary appendix and the Kindle chart reference are still
required before visual validation can begin.

### Figure 7-1

Status: `partial_match`

Kindle evidence: chart page and source line captured.

Dataset used: OWID daily calorie supply dataset based on FAO and historical
sources.

Result: plausible book-period reconstruction and successor extension, but line
geometry and source vintage/styling differ enough that this should remain a
partial match.

### Figure 7-2

Status: `partial_match`

Kindle evidence: chart page and source line captured.

Dataset used: World Bank stunting prevalence indicator
`SH.STA.STNT.ZS` as a proxy.

Result: visually plausible for several series, but it is not the exact
OWID/Roser 2016j WHO Nutrition Landscape Information System vintage cited in
the book.

## Editorial Review Summary

Critical issues found:

- Figure 6-1 is missing a Kindle chart-page reference.

Major issues found:

- Figure 5-4 is visibly incomplete because the exact age-specific source series
  were not recovered.
- Figure 6-1 uses a proxy source and a placeholder reference.
- Figures 5-3, 7-1, and 7-2 use updated or proxy source vintages rather than
  proven exact book-era datasets.

Minor issues found:

- Label placement and typography are approximate across the batch.
- Some endpoint labels crowd the plot edges.

Issues automatically corrected:

- Corrected Figure 6-1 proxy values after noticing the first reconstruction had
  multiplied already-percent IHME values by 100.

Issues remaining:

- Exact source-vintage recovery is still needed for all five figures before any
  can be considered verified.
- Figure 6-1 needs the Kindle chart capture and cited external appendix.

Publication decision:

- The batch is acceptable as a documented branch-local partial/blocked Track A
  pass. It is not publication-ready as verified reconstruction work.
