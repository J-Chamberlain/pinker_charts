# Consolidated Research History: Figure 5-4

These are historical search records, not the current acceptance decision.

## Local Work At efca1264944eabab2f733bc399027e22b8df6381

# Search Iterations: Figure 5-4

## 2026-07-09 Targeted Source Recovery

- Rendered Supplemental Graphics PDF page 4 and visually inspected Figure 5-4.
- Extracted page text with `pdftotext` to verify the surrounding discussion and source note.
- Searched local repository for `5-4`, `Life expectancy, UK`, `Roser 2016n`, `Human Mortality Database`, `Clio Infra`, and related terms.
- Read existing local OWID/HMD partial files and confirmed that only at-birth, age-15, and age-45 values are present for the United Kingdom / England & Wales.
- Queried current OWID grapher endpoints:
  - `https://ourworldindata.org/grapher/life-expectancy-at-different-ages.csv`
  - `https://ourworldindata.org/grapher/life-expectancy-at-different-ages.metadata.json`
  - `https://ourworldindata.org/grapher/life-expectancy-at-different-ages.config.json`
  - `https://ourworldindata.org/grapher/remaining-life-expectancy-at-different-ages.*`
- Queried adjacent OWID indicator metadata IDs around the current HMD/UN age-specific variables. The public set found in this run did not include the book's age-1, 5, 20, 30, 40, 50, 60, or 70 variables.
- Opened HMD England & Wales total population page at `https://www.mortality.org/Country/Country?cntr=GBRTENW`; the page documents the relevant period life-table files and country code.
- Downloaded public HMD background documentation and country-code table.
- Probed direct HMD raw data paths under `/File/GetDocument/hmd.v6/GBRTENW/STATS/`; data paths redirect to the HMD login page in this environment.
- Queried Wayback CDX for 2015-2018 captures of:
  - `ourworldindata.org/grapher/life-expectancy-at-different-ages*`
  - `ourworldindata.org/grapher/remaining-life-expectancy-at-different-ages*`
  - `ourworldindata.org/grapher/life-expectancy-by-age*`
  These returned no usable 200-status CSV capture in this run.

## Outcome

The source family is identified and citable, but the exact book-era OWID/Roser 2016n export or authenticated/archive HMD `GBRTENW` period life table was not recovered. Status remains `needs_targeted_source_recovery`.


## GitHub Recovery At 9a19519494ec20f45b3ac3e6b3122d38a2bc0892

# Search iterations

- Exact title/source-note searches: recovered source note and narrative anchors.
- Supplemental Graphics searches: located indexed document record, not an accessible
  Figure 5-4 page image.
- OWID Git history: full-history filename and commit search; exact 2016n multi-age data
  absent.
- HMD endpoints: confirmed login barrier for the England-and-Wales life-table files.
- Internet Archive CDX: no matching OWID grapher CSV capture.
- Institutional successor search: recovered ONS 2015 decennial male data; retained only
  as a labeled diagnostic.
