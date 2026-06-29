# Source Discovery Log: Figure 10-6

- Figure number: 10-6
- Figure title: Protected areas, 1990-2014
- Original book citation: Source: World Bank 2016h and 2017, based on data from the United Nations Environment Programme and the World Conservation Monitoring Centre.
- Reproduction status: partial_match
- Confidence score: 0.42

## Search Queries Attempted

- World Bank 2016h 2017 protected areas United Nations Environment Programme World Conservation Monitoring Centre data
- "Protected areas, 1990-2014" "World Bank" "World Resources Institute"
- "Terrestrial protected areas" "1990" "2014" "World" "World Bank"
- "Marine protected areas" "1990" "2014" "World" "World Bank"
- World Bank bulk download WDI protected areas 1990 2014 ER.LND.PTLD.ZS ER.MRN.PTMR.ZS
- Protected Planet WDPA historical terrestrial marine protected areas 1990 2014 csv
- World Resources Institute protected areas 1990 2014 data
- Internet Archive World Bank WDI protected areas ER.MRN.PTMR.ZS 2016

## Sources Investigated

### Kindle figure caption/source line

- URL: local Kindle app
- Decision: accepted
- Rationale: Confirmed figure title and visible source line during prior Computer Use pass.

### World Bank API: terrestrial protected areas

- URL: https://api.worldbank.org/v2/country/WLD/indicator/ER.LND.PTLD.ZS?format=json&per_page=20000
- Decision: accepted_partial
- Rationale: Right WDI concept, but World aggregate is populated only for 2013 onward in current API.

### World Bank API: marine protected areas

- URL: https://api.worldbank.org/v2/country/WLD/indicator/ER.MRN.PTMR.ZS?format=json&per_page=20000
- Decision: accepted_partial
- Rationale: Right WDI concept, but World aggregate is populated only for 2013 onward in current API.

### World Bank DataBank bulk WDI

- URL: https://databank.worldbank.org/source/world-development-indicators
- Decision: manual_review_needed
- Rationale: Likely path to historical WDI releases, but exact 2016h/2017 archived files were not integrated.

### World Bank indicator CSV ZIP downloads

- URL: https://api.worldbank.org/v2/en/indicator/ER.LND.PTLD.ZS?downloadformat=csv and https://api.worldbank.org/v2/en/indicator/ER.MRN.PTMR.ZS?downloadformat=csv
- Decision: accepted_partial
- Rationale: Downloadable ZIPs provide reproducible raw CSV files, but World rows still only cover 2013 onward.

### Protected Planet / UNEP-WCMC

- URL: https://www.protectedplanet.net/en
- Decision: manual_review_needed
- Rationale: Original institutional source named by WDI metadata; historical snapshots may require archive/API follow-up.

### World Resources Institute

- URL: https://www.wri.org/
- Decision: manual_review_needed
- Rationale: Book caption says compiled by WRI; no exact compilation file was located in this pass.

### Internet Archive

- URL: https://web.archive.org/
- Decision: manual_review_needed
- Rationale: Needed for archived WDI/Protected Planet releases before exact reproduction can be claimed.

## Automated Discovery Adapter Results

- Machine-readable bundle: `data/raw/figure_10_6_discovery_bundle.json`
- Direct probes recorded: 6
- Internet Archive CDX targets checked: 7
- GitHub repository searches recorded: 4
- GitHub code searches recorded: 2
- Archive candidates returned: none; 6 CDX probes errored or timed out under the default speed budget.
- Direct downloadable candidates:
  - https://api.worldbank.org/v2/en/indicator/ER.LND.PTLD.ZS?downloadformat=csv (application/zip)
  - https://api.worldbank.org/v2/en/indicator/ER.MRN.PTMR.ZS?downloadformat=csv (application/zip)
- GitHub repository candidates returned: none or API unavailable.

## Download URLs

- https://api.worldbank.org/v2/country/WLD/indicator/ER.LND.PTLD.ZS?format=json&per_page=20000
- https://api.worldbank.org/v2/country/WLD/indicator/ER.MRN.PTMR.ZS?format=json&per_page=20000
- https://api.worldbank.org/v2/en/indicator/ER.LND.PTLD.ZS?downloadformat=csv and https://api.worldbank.org/v2/en/indicator/ER.MRN.PTMR.ZS?downloadformat=csv

## Archive URLs

- Not yet pinned. Recommended: capture exact OWID grapher CSV, World Bank API JSON, and any located historical institutional files via Internet Archive or perma.cc before publication.

## Remaining Uncertainties

- Modern WDI endpoints locate the right concepts but not the full historical World aggregate used in the book.

## Recommended Next Steps

- Locate the World Bank 2016h/2017 bulk WDI files or archived indicator downloads.
- Check UNEP-WCMC/Protected Planet historical WDPA snapshots and WRI compilation files.
- Confirm whether the book used terrestrial percent of land area, terrestrial+inland water, or another WDI indicator variant.
- Replot only after the 1990-2014 annual series is recovered.
