# Source Discovery Log: Figure 5-3

Figure title: Maternal mortality, 1751-2013

Original book citation: Our World in Data, Roser 2016p, based partly on data from Claudia Hanson of Gapminder.

## Search Queries and Targets Checked

- Supplemental Graphics PDF page 3, including figure image, source note, and surrounding text.
- "Roser 2016p" and "Maternal mortality, 1751-2013".
- Gapminder GD010 documentation page: `https://www.gapminder.org/data/documentation/gd010/`.
- Gapminder source files:
  - `https://www.gapminder.org/documentation/documentation/gapdoc010.pdf`
  - `https://www.gapminder.org/documentation/documentation/gapdata010.xls`
- Google spreadsheet link exposed by Gapminder GD010. Direct CSV export returned HTTP 400/401 in this run.
- Current OWID grapher data and metadata:
  - `https://ourworldindata.org/grapher/maternal-mortality.csv?v=1&csvType=full&useColumnShortNames=false`
  - `https://ourworldindata.org/grapher/maternal-mortality.metadata.json?v=1&csvType=full&useColumnShortNames=false`
- Internet Archive:
  - 2018 OWID article page: `https://web.archive.org/web/20180202002318/https://ourworldindata.org/maternal-mortality`
  - 2018 OWID SVG export recovered from the archived article.
  - CDX/available checks for `ourworldindata.org/grapher/maternal-mortality.csv` found no archived CSV capture for the book-era target checked in this run.

## Sources Recovered

- `gapminder_gd010_gapdata010.xls`: original Gapminder Excel workbook, downloaded from Gapminder. File metadata identifies Microsoft Excel and author/last-saved-by "claudia"; sha256 `b92cd2e764309ace943b3646bf90c5bb148774e945ccecfddb4c387eed275ad6`.
- `gapminder_gd010_gapdoc010.pdf`: Claudia Hanson, Gapminder Documentation 010, uploaded 2010-07-01; sha256 `4239d4a1ad722e76a783a05ce223ea4230d2a77edaa1d98e80c5be870c032bb2`.
- `owid_maternal_mortality_2018_archived_export.svg`: archived OWID chart export citing "Gapminder (2010) and World Bank (2015)".
- Current OWID grapher successor CSV and metadata, downloaded 2026-07-09.

## Data Fidelity Findings

- Recovered Gapminder observations reproduce the book's long-run Sweden, United States, and Malaysia line levels after conversion from maternal mortality ratio per 100,000 live births to percent (`percent = MMR / 1000`).
- `figure_5_3_gapminder_vs_owid_current_audit.csv` compares recovered Gapminder values to current OWID successor values where years overlap. Most differences are rounding or OWID processing/source-switching differences; the audit keeps them visible rather than silently substituting values.
- Ethiopia is not present in the recovered Gapminder workbook. The book-era OWID/World Bank 2015 supplement that supplied Ethiopia was not recovered as machine-readable data.

## Current Status

Status remains `partial_match`. The source recovery is improved because the cited Gapminder source component is recovered, but the exact Roser 2016p OWID dataset vintage is still incomplete.

## Recommended Next Steps

Search for a 2015/2016 OWID grapher data dump or World Bank 2015 WDI snapshot containing the `maternal-mortality` grapher values, especially Ethiopia 1985-2013 and the post-2003/post-2007 tails for the United States and Sweden.
