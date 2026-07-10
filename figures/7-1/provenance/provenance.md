# Provenance: Figure 7-1

Book figure -> Supplemental PDF page 5 crop -> archived OWID Grapher
configuration and current OWID successor datasets -> `scripts/reconstruct_7_1.py`
-> generated plots.

Source note from Supplemental Graphics PDF page 5:

> United States, England, and France: Our World in Data, Roser 2016d, based on data from Fogel 2004. China, India, and the World: Food and Agriculture Organization of the United Nations, http://www.fao.org/faostat/en/#data.

## Source Recovery

- The Supplemental Graphics PDF was rendered/inspected for page 5. The figure
  has y-axis 1,000-4,000 calories per person per day and x-axis 1700-2030,
  with a labeled book range of 1700-2013.
- The bibliography key resolves to Max Roser's 2016 OWID "Food Supply"/food
  per person material. The book source line cites Fogel 2004 for United
  States, England, and France, and FAO/FAOSTAT for China, India, and World.
- Internet Archive CDX checks found archived OWID Grapher pages for
  `daily-per-capita-caloric-supply` and
  `daily-per-capita-caloric-supply-1961-2013` in 2017-2018. The recovered
  2018 page embeds chart id `744`, variable id `3590`, target year `2013`,
  and six selected entities.
- The 2018 chart page's JavaScript bundle shows that the chart would request
  `/grapher/data/variables/3590`, but CDX and direct Wayback checks did not
  recover a machine-readable capture of that endpoint or its CSV equivalent.
- The local raw file is byte-identical to the archived public OWID dataset
  repository's named dataset
  `Daily supply of calories per person (OWID based on UN FAO & historical sources)`.
  GitHub API metadata shows that named dataset was added to `owid/owid-datasets`
  on 2022-02-14 and updated on 2022-02-15, after the book was published.
- The live OWID Grapher data page is a later successor updated in 2026 with
  coverage through 2023 and revised values/methodology. It is not used as the
  plotted source for this run.

## Reconstruction Input

The plotted data are from `figures/7-1/data/raw/owid_daily_calories_fao_historical.csv`
with SHA-256 `0b8d54b048d74c95fa95edd142be957fb83c8c30f5206ecda3a50638d8ed1398`.

Book-period series used:

- United States: 1800-2013, n=71.
- United Kingdom displayed as `England/UK`: 1700-2013, n=64.
- France: 1705-2013, n=68.
- China: 1934-2013, n=65.
- India: 1934-2013, n=57.
- World: 1961-2013, n=53.

The exact Roser 2016d book-era dataset was not recovered. The United Kingdom
series is included because the current OWID data page states that pre-1961 UK
data may correspond to England or England and Wales; it is labeled as
`England/UK` rather than silently substituted for the book's England series.

## Extension

The extension uses the same local OWID 2022 dataset after 2013, through 2018.
It is comparable as a same-named OWID/FAO/historical-source continuation, but
it is not a verified continuation of the exact Roser 2016d vintage.
