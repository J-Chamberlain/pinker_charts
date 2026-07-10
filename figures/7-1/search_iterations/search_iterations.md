# Search Iterations: Figure 7-1

- Kindle search/open for "Figure 7-1" or title
- "Calories, 1700-2013" source data
- "United States, England, and France: Our World in Data, Roser 2016d, based on Fogel 2004. China, India, and World: FAO."
- local OWID datasets mirror
- current public successor data where exact book vintage was unavailable
- 2026-07-09: Inspected Supplemental Graphics PDF page 5 with `pdftotext`
  and rendered page image. Captured figure title, source note, and surrounding
  text.
- 2026-07-09: Queried live OWID Grapher page
  `https://ourworldindata.org/grapher/daily-per-capita-caloric-supply`; live
  metadata reports a 2026 update and 1274-2023 coverage, making it a later
  successor rather than book-era evidence.
- 2026-07-09: Queried Internet Archive CDX for
  `daily-per-capita-caloric-supply.csv*`; no 2015-2018 CSV captures were found.
- 2026-07-09: Queried Internet Archive CDX for
  `daily-per-capita-caloric-supply*`; recovered archived 2017-2018 chart-page
  captures, including `daily-per-capita-caloric-supply-1961-2013`.
- 2026-07-09: Downloaded archived chart pages into
  `figures/7-1/data/candidates/archives/`. The useful 2018 capture identifies
  chart id `744`, variable id `3590`, and selected entities, but not values.
- 2026-07-09: Inspected the 2018 Grapher JavaScript bundle and found that the
  chart data were requested from `/grapher/data/variables/3590`.
- 2026-07-09: Queried CDX and direct Wayback URLs for
  `/grapher/data/variables/3590*`, `/grapher/variables/3590*`, `.csv`, and
  `.json` variants. No machine-readable 2017-2018 data capture was recovered.
- 2026-07-09: Queried GitHub API for the public `owid/owid-datasets` calories
  dataset path. API metadata shows the named dataset was added on 2022-02-14
  and updated on 2022-02-15.
- 2026-07-09: Cloned the current archived `owid/owid-datasets` repository
  under `tmp/` and verified that the local raw CSV is byte-identical to the
  named OWID dataset in that repository.
