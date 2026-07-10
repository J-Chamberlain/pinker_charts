# Source Discovery Log: Figure 7-1

Figure title: Calories, 1700-2013

Original book citation: United States, England, and France: Our World in Data, Roser 2016d, based on Fogel 2004. China, India, and World: FAO.

## Search Queries Attempted
- Kindle search/open for "Figure 7-1" or title
- "Calories, 1700-2013" source data
- "United States, England, and France: Our World in Data, Roser 2016d, based on Fogel 2004. China, India, and World: FAO."
- local OWID datasets mirror
- current public successor data where exact book vintage was unavailable
- 2026-07-09: OWID live data page and Grapher CSV/metadata for `daily-per-capita-caloric-supply`
- 2026-07-09: Internet Archive CDX for `ourworldindata.org/grapher/daily-per-capita-caloric-supply*`
- 2026-07-09: Internet Archive CDX for `daily-per-capita-caloric-supply-1961-2013*`
- 2026-07-09: Internet Archive CDX/direct Wayback checks for old Grapher data endpoints `/grapher/data/variables/3590`, `/grapher/variables/3590*`, and CSV/JSON variants
- 2026-07-09: GitHub API/repository checks for `owid/owid-datasets` named calories dataset history

## Sources Investigated
- Reference image: Supplemental PDF page 5 crop accepted for chart reference/source line.
- Supplemental PDF page 5 text and visual reference. It identifies the figure,
  title, source note, and surrounding explanatory text.
- Internet Archive recovered a 2018 OWID Grapher page for
  `daily-per-capita-caloric-supply`. This page embeds chart id `744`, variable
  id `3590`, six selected entities, and target year `2013`; it supports the
  source family and chart identity but does not expose the underlying data.
- Internet Archive also had 2017-2018 page captures for the older slug
  `daily-per-capita-caloric-supply-1961-2013`, but the captures redirect/embed
  the canonical chart page and do not provide data values.
- Direct Wayback attempts for CSV, JSON, `/grapher/variables/3590*`, and
  `/grapher/data/variables/3590*` returned only Wayback wrapper pages or empty
  CDX results; no old machine-readable variable data were recovered.
- The local raw file exactly matches the public archived `owid/owid-datasets`
  named dataset added in 2022, after publication. It is therefore a successor
  dataset, not the original Roser 2016d vintage.
- The live OWID data page for "Daily supply of calories per person" is a newer
  successor updated in 2026 with coverage through 2023 and revised values.

## Remaining Uncertainties
- Status: `partial_match`.
- Exact Roser 2016d / book-era OWID variable data were not recovered.
- The current/successor OWID file contains `United Kingdom`, not `England`.
  This run includes that source series as `England/UK` and documents the
  substitution.
- The reconstructed historical shapes, especially France, United States, and
  England/UK, visibly differ from the book figure and should not be promoted
  without recovering the old variable data or a documented transformation.

## Recommended Next Steps
- Recover old OWID Grapher variable id `3590` data or a book-era export of
  `daily-per-capita-caloric-supply`.
- If the old endpoint cannot be recovered, consult OWID source history or
  contact OWID for the 2016 `Roser 2016d` export before promotion.
