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
