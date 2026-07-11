# Source Discovery Log: Figure 5-3

## Accepted

- Indexed Supplemental Graphics record: title, four country labels, axes,
  scale, source line, and nearby prose recovered.
- Wikimedia Commons Data namespace preservation of OWID dataset 522:
  https://commons.wikimedia.org/wiki/Data:Maternal_Mortality_Ratio_-_Gapminder_(2010)_and_World_Bank_(2015)_(OWID_522).tab
- Raw Data namespace JSON (`action=raw`), stored locally with embedded
  provenance and retrieval date.
- Gapminder GD010 live documentation:
  https://www.gapminder.org/data/documentation/gd010/
- Gapminder GD010 Google Spreadsheet export, stored as
  `data/raw/gapminder_gd010_2010.xlsx`.
- Gapminder Documentation 010 PDF, indexed at
  https://www.gapminder.org/documentation/documentation/gapdoc010.pdf.
- Current OWID maternal-mortality CSV and metadata, accepted only for successor
  evaluation and archived locally.

## Archive/search checks

- The Supplemental Graphics PDF record was located, but direct page and common
  download endpoints returned a Cloudflare 403 response.
- Steven Pinker's 2019 ECOSOC lecture PDF was located and indexed; slide 32
  repeats the title/source family, while direct retrieval returned 403.
- The live Gapminder binary `gapdata010.xls` link stalled, but the documentation
  page's public Google Spreadsheet export succeeded and preserved the workbook.
- A Wikimedia Data page created in 2020 preserved OWID dataset 522 and its
  2017-06-04 retrieval metadata, supplying the citable book-era archive.

## Rejected for the book line

- Current OWID grapher `maternal-mortality`: rejected as the book dataset
  because its 2024-2025 source releases and processing differ from OWID 522.
- Any chart digitization: rejected by protocol and not performed.
