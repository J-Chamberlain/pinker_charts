# Figure 15-7 provenance

## Book evidence

- Figure: 15-7
- Title: Liberal values across time (extrapolated), world's culture zones, 1960-2006
- Reference: `references/figures/figure_15_7.png`, extracted from the supplied
  Enlightenment Now Supplemental Graphics PDF.
- Book source line: World Values Survey, as analyzed in Welzel 2013, Figure 4.4,
  updated with data provided by Welzel. Emancipative value estimates are calculated
  for a hypothetical fixed-age sample using respondent birth cohort, test year, and
  a country-specific period effect. Countries in each culture zone are weighted equally.

## Resolved source chain

Book figure -> Pinker's source note -> Christian Welzel, *Freedom Rising* (2013),
Figure 4.4 -> WVS/EVS country survey data plus Welzel's emancipative-values index ->
Welzel's backward-estimation and culture-zone aggregation procedure -> author-supplied
updated series used by Pinker.

The official Welzel appendix explains the backward estimates: cohort differences,
decennial trend assumptions, and an outcome-level adjustment are combined to estimate
historical country values. The appendix states that replication data for the related
analyses are provided in `Table4.2.sav`, but the exact Figure 4.4 time-series export was
not obtained in this run.

## Data disposition

No clean data file is committed for this figure. The public WVS pages and the GESIS
ZA7470 catalogue document the index and aggregated survey archive, but do not provide
the exact author-updated, fixed-age, culture-zone series used in Pinker's plot through
2006. A proxy or values transcribed from the chart would not be an acceptable
reconstruction dataset.

## Recommended recovery

Obtain the author-supplied Figure 4.4 replication file or a valid archive of Welzel's
updated data, then implement the documented fixed-age prediction, period adjustment,
equal-country zone aggregation, and the 1960-2006 plotting window.
