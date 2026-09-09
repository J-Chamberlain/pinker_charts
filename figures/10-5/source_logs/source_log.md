# Consolidated Research History: Figure 10-5

These are historical search records, not the current acceptance decision.

## Local Work At efca1264944eabab2f733bc399027e22b8df6381

# Source Discovery Log: Figure 10-5

- Figure number: 10-5
- Figure title: Oil spills, 1970-2016
- Current status: partial_match
- Last updated: 2026-07-09

## Supplemental Graphics PDF

- Reference: `references/enlightenment_now_supplemental_graphics.pdf`
- Located text: Figure 10-5, "Oil spills, 1970-2016"
- Source note: Our World in Data, Roser 2016r, based on updated data from the International Tanker Owners Pollution Federation.
- Definition note: oil spills include losses of at least 7 metric tons; oil shipped is total crude oil, petroleum product, and gas loaded.
- Surrounding text states that annual oil spills fell from more than 100 in 1973 to five in 2016, while seaborne oil transport became safer.

## Bibliography Resolution

- Bibliography key: Roser 2016r
- Repository mapping: `data/bibliography/figure_bibliography_mapping.csv`
- Candidate entry: Max Roser, "Oil spills / Global number of oil spills from tankers," Our World in Data, 2016.
- Resolution status: candidate. The current OWID grapher is a public successor/candidate for the spill-count series, but the exact 2016r OWID data snapshot was not recovered.

## Recovered Source-Family Evidence

### OWID / ITOPF spill counts

- URL: `https://ourworldindata.org/grapher/number-oil-spills.csv`
- Local file: `figures/10-5/data/raw/owid_number_oil_spills.csv`
- Role: accepted for annual medium and large tanker spill counts.
- Transformation: `oil_spills_7_plus_tonnes = medium spills (7-700 tonnes) + large spills (>700 tonnes)`.

### Archived ITOPF 2016 statistics page

- URL: `https://web.archive.org/web/20170119015939/http://www.itopf.com:80/knowledge-resources/data-statistics/statistics/`
- Local file: `figures/10-5/data/candidates/itopf_statistics_20170119_wayback.html`
- Role: accepted context and source-family evidence.
- Relevant page caption: "Seaborne oil trade and number of tanker spills 7 tonnes and over, 1970 to 2015 (Crude and Oil Product*) Data source: UNCTADStat".
- Limitation: the page publishes a chart image, not the annual UNCTADStat table.

### Archived ITOPF seaborne chart image

- URL: `https://web.archive.org/web/20170119015939im_/http://www.itopf.com/fileadmin/data/Photos/Statistics/seaborne_16.JPG`
- Local file: `figures/10-5/data/candidates/itopf_archived_seaborne_16.JPG`
- Role: accepted diagnostic source image for the oil-loaded line.
- Derived data: `figures/10-5/data/candidates/itopf_archived_seaborne_16_digitized_oil_loaded.csv`
- Method: color-mask digitization of the navy oil-loaded line, calibrated to the chart axes 1970-2016 and 0-3500 million metric tons.
- Validation: selected-year comparison with UNCTAD Review of Maritime Transport 2020 gives MAE 0.058 billion metric tons and maximum absolute difference 0.194; see `figures/10-5/data/candidates/itopf_digitized_vs_unctad_rmt2020_selected_year_validation.csv`.
- Limitation: image-derived values are not the original annual dataset.

### ITOPF Oil Tanker Spill Statistics 2017 PDF

- URL: `https://tcrsudestuairemoyen.org/wp-content/uploads/2018/12/oil_spill_stats_2017.pdf`
- Local files: `figures/10-5/data/candidates/oil_spill_stats_2017.pdf`, `figures/10-5/data/candidates/oil_spill_stats_2017.txt`
- Role: accepted context.
- Relevant figure: "Tanker Spills versus Seaborne Oil Trade"; chart label says total crude oil, petroleum product and gas loaded, data source UNCTADStat.
- Limitation: the PDF exposes annual spill tables but not an annual oil-loaded table.

### UNCTAD Review of Maritime Transport 2020

- Local file: `figures/10-5/data/candidates/unctad_rmt2020_tanker_trade_selected_years.csv`
- Role: selected-year validation for the digitized oil-loaded line.
- Limitation: selected years only; not enough to reconstruct the annual 1970-2016 gray line by itself.

## Rejected Or Incomplete Routes

- Current UNCTADStat `US.SeaborneTrade` version 2231: recovered 2000-2016 values, but overlap values are inconsistent with the ITOPF/RMT/book scale and it omits 1970-1999.
- Wayback exact OWID grapher CSV snapshots for `number-oil-spills.csv`: no exact 2016/2017 CSV snapshot recovered in prior probes.
- Wayback wildcard searches for legacy UNCTADStat CSV exports: no usable annual table recovered.
- OWID public repository searches: found spill-count artifacts, not the oil-loaded companion series.

## Current Finding

The closest recovered source for the gray line is an archived ITOPF chart image whose caption cites UNCTADStat. The annual UNCTADStat table behind that line remains unrecovered, so the book-period plot is a source-family, image-digitized partial reconstruction, not a verified reproduction from original tabular data. No extension is plotted because a same-method annual successor for the oil-loaded line has not been recovered.


## GitHub Recovery At 9a19519494ec20f45b3ac3e6b3122d38a2bc0892

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
