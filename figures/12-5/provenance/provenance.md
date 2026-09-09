# Figure 12-5 Provenance

Title: Plane crash deaths, 1970-2015

Canonical reference: Supplemental Graphics PDF page 20. The source note cites Aviation Safety Network 2017 and says passenger counts come from World Bank 2016b.

Recovered source trail:

- Supplemental PDF: `references/enlightenment_now_supplemental_graphics.pdf`, page 20.
- ASN archived source page: 2017-10-07 Wayback capture of `https://aviation-safety.net/statistics/`, stored as `data/raw/asn_statistics_wayback_20171007141946.html`.
  - Capture URL: `https://web.archive.org/web/20171007141946/https://aviation-safety.net/statistics/`
  - CDX query used for the local capture index: `https://web.archive.org/cdx?url=https://aviation-safety.net/statistics/&from=2017&to=2018&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200`
- Current ASN successor data: public Google Sheet export linked by OWID indicator metadata, stored as `data/raw/asn_accidents_and_fatalities_per_year_google_sheet_2026-07-09.csv`.
  - ASN current statistics page: `https://aviation-safety.net/statistics/`
  - Google Sheet CSV export: `https://docs.google.com/spreadsheets/d/1SDp7p1y6m7N5xD5_fpOkYOrJvd68V7iy6etXy2cetb8/gviz/tq?tqx=out:csv&sheet=Accidents+and+fatalities+per+year`
- Current processed successor: OWID grapher CSV `aviation-fatalities-per-million-passengers`, stored as `data/raw/aviation-fatalities-per-million-passengers_owid_2024.csv`.
  - Grapher CSV: `https://ourworldindata.org/grapher/aviation-fatalities-per-million-passengers.csv?v=1&csvType=full&useColumnShortNames=false`
  - Grapher metadata: `https://ourworldindata.org/grapher/aviation-fatalities-per-million-passengers.metadata.json`
  - Indicator metadata: `https://api.ourworldindata.org/v1/indicators/930564.metadata.json`
- Current World Bank passenger provenance: OWID metadata cites WDI indicator `IS.AIR.PSGR`.
  - Indicator page: `https://data.worldbank.org/indicator/IS.AIR.PSGR`
  - Current WDI bulk download cited in OWID metadata: `https://databankfiles.worldbank.org/public/ddpext_download/WDI_CSV.zip`

Supplemental PDF cites Aviation Safety Network 2017, with passengers from World Bank 2016b. The exact 2017 ASN extraction has not been recovered. This run replaces the prior flight-phase proxy with OWID's processed aviation-fatalities-per-million-passengers indicator, which uses ASN annual airliner fatalities and World Bank passenger counts and documents the same calculation.

Current OWID successor values used directly: 1970=4.76741, 1973=5.65279, 2015=0.152335. Tolerance to recovered successor CSV is exact to CSV precision because the clean data are a column rename/filter. Tolerance to the unrecovered 2017 book source is not asserted.

The early-1970s discrepancy in the previous artifact is explained by source substitution: the prior reconstruction used the ASN 2019 flight-phase table, which includes corporate jet and military transport accidents. OWID's processed indicator uses ASN annual airliner fatalities, including passenger and cargo flights with sabotage/hijacking events, and gives the book-consistent 1970 value just below five deaths per million passengers.

The current successor rate series omits 1972 because the successor World-level passenger series lacks a 1972 observation. Local evidence: `data/raw/aviation-fatalities-per-million-passengers_owid_2024.csv` has World rows for 1971 and 1973 but not 1972, and `data/raw/air-passengers-carried.csv` has World passenger rows for 1971 and 1973 but not 1972. This limitation is retained as a successor-data caveat only; it is not treated as verification of the unrecovered ASN 2017 / World Bank 2016b book vintage.

No digitized chart values were used as reconstruction data.
