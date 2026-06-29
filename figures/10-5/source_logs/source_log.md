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
- Decision: rejected
- Rationale: Probe returned HTTP 400 without the report parameters/authentication needed for a CSV download.

### GitHub/OWID historical mirrors

- URL: https://github.com/owid/owid-grapher-svgs
- Decision: manual_review_needed
- Rationale: Likely useful for historical commits, but no exact Roser 2016r data snapshot was integrated in this pass.

### Internet Archive

- URL: https://web.archive.org/
- Decision: manual_review_needed
- Rationale: Should be checked for archived OWID grapher CSV/UNCTAD tables before claiming exact reproduction.

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

- Spill-count data is available from current OWID/ITOPF sources. The historical UNCTAD oil-shipped-by-sea series remains unresolved.

## Recommended Next Steps

- Search Internet Archive CDX for historical OWID grapher CSV snapshots around 2016-2018.
- Inspect OWID historical commits or grapher metadata for `Roser 2016r` and oil-shipped-by-sea source data.
- Locate UNCTAD seaborne trade oil cargo table or archived CSV used by the book.
- Replot with dual axes only after the oil-shipped-by-sea series is independently downloaded.
