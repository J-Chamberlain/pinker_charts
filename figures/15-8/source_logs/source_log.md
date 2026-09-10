# Figure 15-8 source discovery log

## Search queries attempted

- `Finkelhor 2014 child physical sexual abuse rates 1993 2012 data`
- `site:ndacan.cornell.edu Finkelhor 2014 physical abuse sexual abuse 1993 2012`
- `BJS NCVS Victimization Analysis Tool school violent victimization 1993 2012 download`
- `Finkelhor 2014 NCANDS physical abuse sexual abuse 1993 2012 chart data csv`
- `Finkelhor Jones Trends in Child Maltreatment 1990 2012 data table`
- `site:ourworldindata.org/grapher child physical abuse rate United States NCANDS`
- `site:ourworldindata.org/grapher child sexual abuse rate United States NCANDS`

## Sources investigated

- [NDACAN NCANDS dataset list](https://www.ndacan.acf.hhs.gov/datasets/datasets-list-ncands-state-agency-file.cfm)
  was accepted as the authoritative route for the missing NCANDS files. The page lists
  historical aggregate and agency datasets, but the data require an ordering/access
  step that was not completed here.
- [UNH Crimes against Children Research Center](https://www.unh.edu/ccrc/trends-child-victimization)
  was accepted as institutional context for the Finkelhor series and its reported
  decline, but did not expose the exact annual numeric table needed for reconstruction.
- [BJS NCVS data user page](https://bjs.ojp.gov/ncvs-data-user-page) was accepted as the
  official description of current NCVS access and public-use files.
- [BJS N-DASH / NCVS dashboard](https://ncvs.bjs.ojp.gov/multi-year-trends/crimeType?hl=en-US)
  was accepted as the successor access path, but it does not expose the historical NVAT
  school subset in a simple static download through this run.
- [OWID BJS school series](https://ourworldindata.org/grapher/rate-of-violent-victimizations-at-school-us)
  was accepted for the recovered school subset because its CSV is public and identifies
  BJS NCVS as the original source.
- Finkelhor and Jones publications and secondary reproductions were retained as
  bibliography leads only; values were not manually transcribed from their figures.

## Rejected or insufficient sources

- Current NCANDS summaries were rejected as substitutes for the exact Finkelhor annual
  series because definitions, duplicate-victim treatment, and reporting years differ.
- Current BJS dashboards were rejected as an exact book-period match because the series
  definition and denominator do not establish identity with the old NVAT output.
- Search-result snippets, secondary charts, and the Pinker reference image were rejected
  as numeric data sources.

## Download URLs

- `https://ourworldindata.org/grapher/rate-of-violent-victimizations-at-school-us.csv`
- `https://ourworldindata.org/grapher/rate-of-violent-victimizations-at-school-us.metadata.json`

## Archive and access URLs

- `https://www.ndacan.acf.hhs.gov/datasets/datasets-list-ncands-state-agency-file.cfm`
- `https://bjs.ojp.gov/ncvs-data-user-page`
- `https://ncvs.bjs.ojp.gov/multi-year-trends/crimeType?hl=en-US`

## Remaining uncertainties and next steps

- Obtain the NCANDS aggregate/agency files or an exact Finkelhor 2014 annual export.
- Recover the original NVAT school definition and denominator, rather than assuming the
  current BJS/OWID series is identical.
- Rebuild all three lines and inspect both comparisons before promoting the status.
