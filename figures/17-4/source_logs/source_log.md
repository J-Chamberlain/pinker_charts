# Figure 17-4 source log

Research date: 2026-09-09. Original title/source and bibliography: ../provenance/provenance.md. Exact URLs, times, HTTP outcomes and SHA256 values: downloads.json.

## Investigated sources

1. Current OWID lighting page: accepted as a successor only. Downloaded CSV, chart metadata and full indicator metadata; revised historical values differ from legacy data. Five-year averaging is explicit.
2. OWID historical dataset repository: full tree queried, not truncated; discovered dataset Price for Light - Fouquet. Downloaded pinned CSV and datapackage. Git path history contains one initial 2018 commit; publisher metadata cites 2012 paper and 2017 retrieval. Accepted as the original source series, corroborated by 2016 chart identity and visual match.
3. Wayback CDX, 2014-2018 grapher URL prefix: recovered the old slug ending -1300-2006 and August 2016 page. Accepted as book-era source identity and processing evidence, not numeric data. Numeric-variable wildcard query for 2015-2017 returned no captures.
4. Legacy OWID indicator 250: downloaded metadata/data, created 2016-02-27; exact numerical agreement with retained Git CSV on all 706 observations. Accepted cross-check, not an independently measured dataset.
5. LSE author manuscript of Fouquet & Pearson 2012: opened to resolve bibliography and research context. No figure values digitized, no full copyrighted manuscript redistributed.
6. Current OWID catalog table metadata: retained to document units and revisions. Direct .csv probe returned 404; grapher CSV already provides the required successor data, so no invented export endpoint was used as evidence.
7. Search leads included a 2006 Energy Journal paper, a third-party old OWID mirror, Wikimedia lighting-source shares and a university visualization article. These are not the numeric input; the original OWID repository is more direct. Lighting shares are a different variable.

## Uncertainties / next steps

The 2016 page stores configuration, not values. We recovered the same identified original dataset from a later immutable repository snapshot, not Pinker's own source file. The observed full-line match is strong. Source says UK while book says England; original time series starts 1301, not 1300. Preserve both facts. Current prices revise history and must remain version-separated. Future refresh should inspect price-index and smoothing changes before extending. Direct author contact is unnecessary for the present source-supported reconstruction but could resolve exact private-vintage identity.
