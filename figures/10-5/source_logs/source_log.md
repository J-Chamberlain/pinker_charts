# Source Discovery Log: Figure 10-5

- Figure number: 10-5
- Figure title: Oil spills, 1970-2016
- Original book citation: Source: Our World in Data, Roser 2016r, based on data (updated) from the International Tanker Owners Pollution Federation.
- Reproduction status: partial_match
- Confidence score: 0.58

## Search Queries Attempted

- Our World in Data oil spills Roser 2016r International Tanker Owners Pollution Federation oil shipped by sea data
- Our World in Data oil spills from tankers csv oil shipped by sea csv
- site:ourworldindata.org/grapher oil shipped by sea billion metric tons grapher
- "Oil shipped by sea" "Our World in Data" grapher
- "Oil shipped by sea" "billion metric tons" data
- Internet Archive Our World in Data number-oil-spills csv Roser 2016
- github ourworldindata grapher number-oil-spills csv historical commit
- UNCTAD seaborne trade oil loaded total crude petroleum gas 1970 2016 csv
- UNCTADstat API seaborne trade US.SeaborneTrade CSV download

## Sources Investigated

### Kindle figure caption/source line

- URL: local Kindle app
- Decision: accepted
- Rationale: Confirmed figure title and visible source line during prior Computer Use pass.

### Our World in Data grapher: number-oil-spills

- URL: https://ourworldindata.org/grapher/number-oil-spills.csv
- Decision: accepted_partial
- Rationale: Provides annual medium and large tanker oil-spill counts; current metadata cites ITOPF.

### OWID grapher metadata

- URL: https://ourworldindata.org/grapher/number-oil-spills.metadata.json
- Decision: accepted_context
- Rationale: Documents current variable definitions and source citation; not the exact Roser 2016r archive.

### ITOPF oil tanker spill statistics

- URL: https://www.itopf.org/knowledge-resources/data-statistics/oil-tanker-spill-statistics-2025/
- Decision: accepted_context
- Rationale: Institutional source behind the spill counts; current public page/PDF is a modern release.

### UNCTADStat seaborne trade data viewer

- URL: https://unctadstat.unctad.org/datacentre/dataviewer/us.seabornetrade
- Decision: rejected_for_now
- Rationale: Current viewer is public, but the exact oil-shipped-by-sea export route was not located.

### UNCTADStat unauthenticated Facts endpoint

- URL: https://unctadstat-api.unctad.org/datamart-api/US.SeaborneTrade/cur/Facts?culture=en
- Decision: accepted_diagnostic_only
- Rationale: Corrected POST form with `culture=en` in the body returns current World cargo rows for 2000 onward. It does not return 1970-1999 and its cargo 11+12 values fail the RMT scale check for the book gray line.

### GitHub/OWID historical mirrors

- URL: https://github.com/owid/owid-grapher-svgs
- Decision: manual_review_needed
- Rationale: Likely useful for historical commits, but no exact Roser 2016r data snapshot was integrated in this pass.

### Internet Archive

- URL: https://web.archive.org/
- Decision: manual_review_needed
- Rationale: Should be checked for archived OWID grapher CSV/UNCTAD tables before claiming exact reproduction.

### UNCTADStat current bulk file

- URL: https://unctadstat-api.unctad.org/bulkdownload/US.SeaborneTrade/US_SeaborneTrade
- Decision: accepted_rejection_evidence
- Rationale: Current bulk-file metadata lists a single file `US_SeaborneTrade` labeled `From 2000 to 2024`. The archive was downloaded and extracted, but it lacks 1970-1999 and differs from RMT selected-year tanker trade by about 31-48 percent on overlapping years. It is retained as a verifiable successor/source-family file, not as reconstruction input.

### 2023 independent replication clue

- URL: https://medium.com/@vannairea/update-of-a-chart-from-enlightenment-now-by-steven-pinker-python-4ba9aca5eae9
- Decision: accepted_context
- Rationale: The article names a local UNCTAD export `US.SeaborneTrade_585_20231104_101924.csv` and describes UNCTADStat data from 1970 to 2021. This run did not recover that CSV or an archived equivalent; current UNCTAD metadata rejects version `585`.

## Automated Discovery Adapter Results

- Machine-readable bundle: `data/raw/figure_10_5_discovery_bundle.json`
- Direct probes recorded: 4
- Internet Archive CDX targets checked: 6
- GitHub repository searches recorded: 3
- GitHub code searches recorded: 2
- Archive candidates returned: none; 6 CDX probes errored or timed out under the default speed budget.
- Direct downloadable candidates:
  - https://www.itopf.org/fileadmin/uploads/itopf/data/Stats/Oil_Spill_Stats_brochure_2025_lo.pdf (application/pdf)
- GitHub repository candidates returned: none or API unavailable.

## Download URLs

- https://ourworldindata.org/grapher/number-oil-spills.csv
- https://ourworldindata.org/grapher/number-oil-spills.metadata.json
- https://www.itopf.org/knowledge-resources/data-statistics/oil-tanker-spill-statistics-2025/

## Archive URLs

- Not yet pinned. Recommended: capture exact OWID grapher CSV, World Bank API JSON, and any located historical institutional files via Internet Archive or perma.cc before publication.

## Remaining Uncertainties

- Spill-count data is available from current OWID/ITOPF sources. The historical annual UNCTAD/ITOPF/Roser oil-shipped-by-sea series remains unresolved.
- The live UNCTADStat successor source is verifiable but is not comparable enough to plot for the book-period gray line.

## Recommended Next Steps

- Search Internet Archive/CDX and broader web caches for `US.SeaborneTrade_585_20231104_101924.csv` or adjacent `US.SeaborneTrade_585_*` exports.
- Inspect authenticated GitHub/code search results for old UNCTADStat export mirrors and OWID/Roser source bundles.
- Contact UNCTAD/ITOPF or locate archived chart-data tables for the annual 1970-2016 oil-shipped-by-sea series.
- Replot the gray dual-axis series only after the annual book-period source is independently downloaded and scale-validated.
