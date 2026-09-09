# Consolidated Research History: Figure 5-2

These are historical search records, not the current acceptance decision.

## Local Work At efca1264944eabab2f733bc399027e22b8df6381

# Search Iterations: Figure 5-2

- "Figure 5-2" Kindle search
- "Child mortality, 1751-2013" Our World in Data dataset
- "Child mortality, 1751-2013" historical CSV
- "Our World in Data, Roser 2016a, based on UN Child Mortality Estimates and the Human Mortality Database."
- Internet Archive and successor dataset checks
- 2026-07-09: Wayback CDX for `ourworldindata.org/child-mortality/` found 2016
  captures; 2016-04-23 article downloaded.
- 2026-07-09: Archived 2016 article showed old Chart Builder
  `public/view/58` for the country-by-country long-run chart.
- 2026-07-09: Wayback CDX for Chart Builder view 58 found 2015 HTML shells, but
  no captured `data/config/58` payload in the checked CDX results.
- 2026-07-09: Current playback/migration of view 58 led to
  `grapher/child-mortality-around-the-world`, which is a UN regional chart and
  not the five-country book figure.
- 2026-07-09: Recovered OWID dataset candidates from `owid/owid-datasets`:
  Gapminder 2015, selected Gapminder v10 2017, and CME Info 2018.


## GitHub Recovery At 9a19519494ec20f45b3ac3e6b3122d38a2bc0892

# Search Iterations: Figure 5-2

- "Figure 5-2" Kindle search
- "Child mortality, 1751-2013" Our World in Data dataset
- "Child mortality, 1751-2013" historical CSV
- "Our World in Data, Roser 2016a, based on UN Child Mortality Estimates and the Human Mortality Database."
- Internet Archive and successor dataset checks

## 2026-07-10 source-recovery run

- Searched the live OWID grapher and metadata endpoints.
- Queried Wayback CDX for `ourworldindata.org/grapher/child-mortality.csv` and
  wildcard variants; no usable archived CSV capture was returned.
- Cloned the complete `owid/owid-datasets` Git history (3,292 commits) and
  searched current and deleted paths for child mortality and HMD material.
- Recovered immutable commit `b6746f923dd64ca0fad7de1b1f2f78bebe25205f`,
  dataset 161, “Child Mortality Estimates - CME Info (2016).”
- Inspected Gapminder 2013, Gapminder 2015, selected Gapminder v10 (2017), CME
  Info 2016, and the current selected OWID export at representative years.
- Rejected Gapminder files as the book source: their early country coverage
  produces lines absent from the figure.
- Retained current OWID only as the closest verifiable successor proxy; its
  metadata names changed source vintages.
