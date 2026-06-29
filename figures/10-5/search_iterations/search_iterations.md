# Search Iteration Log: Figure 10-5

Accessed: 2026-06-28

| Iteration | Query or URL | Result | Accepted or Rejected | Resolved discrepancy |
| --- | --- | --- | --- | --- |
| 1 | `https://ourworldindata.org/grapher/number-oil-spills.csv` | Downloaded spill-count CSV for World, 1970-2016. | Accepted partial | Reproduces black spill-count line. |
| 2 | `https://unctadstat.unctad.org/datacentre/dataviewer/us.seabornetrade` | Browser/network inspection found report `US.SeaborneTrade` version 2231 and cargo types 11/12. | Accepted partial | Identifies oil-shipped-by-sea source family. |
| 3 | `https://unctadstat-api.unctad.org/datamart-api/US.SeaborneTrade/2231/Facts` | POST returned World crude oil loaded + other tanker trade loaded for 2000-2016. | Accepted as diagnostic only | Documents candidate source family but is excluded from validation plot. |
| 4 | `US.SeaborneTrade` old report versions 584, 585, 586, 580, 600, 1000, 1500, 2000 | Current API returned 404 for those versions. | Rejected | Did not recover 1970-1999. |
| 5 | Wayback CDX for OWID grapher CSVs `number-oil-spills.csv` and `oil-shipped-by-sea.csv` | No 200 snapshots found for those exact CSV URLs. | Rejected | Did not recover Roser 2016r data. |
| 6 | Wayback CDX for OWID `oil-spills` page | Archived pages exist from 2016 onward, but this pass did not recover an embedded table/CSV with oil-shipping values. | Accepted context | Confirms historical page availability, not full data. |
| 7 | Wayback CDX for UNCTAD data viewer and wildcard `US.SeaborneTrade` CSVs | Viewer snapshots exist only from 2024 onward; wildcard CSV search returned no captures. | Rejected for plotting | Did not recover 1970-1999. |
| 8 | ITOPF 2017 statistics PDF | Found chart title and source note naming UNCTADStat but no data table. | Accepted context | Confirms source family, not full data. |
| 9 | Web/GitHub mirror searches for `US.SeaborneTrade_585`, `CargoType_Label`, `Metric_tons_in_millions_Value` | Found evidence of old UNCTAD export naming, not a downloadable full historical file. | Rejected for plotting | Did not recover 1970-1999. |

## Stop Reason

The required `oil shipped by sea` series is only partially recovered. The remaining gap appears to require an archived UNCTADStat export, an OWID/Roser historical data bundle, institutional follow-up, or manual digitization from the ITOPF chart.

## Research Mode Iterations
| Iteration | Query or URL | Result | Accepted or Rejected | Resolved discrepancy |
| --- | --- | --- | --- | --- |
| 10 | `https://unctad.org/system/files/official-document/rmt2020_en.pdf` | Downloaded and extracted RMT 2020 Table 1.1 selected-year tanker trade, 1970-2019. | Accepted diagnostic | Recovers historical source concept back to 1970, but not annual series. |
| 11 | RMT 2016/2019/2020 PDF text searches | Confirmed table/source wording and footnotes for tanker trade. | Accepted context | Strengthens UNCTAD/Clarksons evidence chain. |
| 12 | RMT-vs-live-UNCTAD numeric comparison | RMT 2000/2016 = 2.163/3.058 billion tons; live UNCTAD cargo sum = 2.984/4.086 billion tons. | Accepted diagnostic | Shows live v2231 is not a faithful substitute for the book line. |
| 13 | OWID `owid-datasets` clone and file search | Found ITOPF oil-spills dataset, no oil-shipping series. | Rejected for missing series | Negative evidence for OWID dataset trail. |
| 14 | OWID `owid-grapher-svgs` clone and file search | Found modern oil-spill grapher artifacts, no matching oil-shipping series. | Rejected for missing series | Negative evidence for public grapher artifact trail. |
| 15 | GitHub code search API | Returned 401 authentication requirement. | Incomplete | Requires authenticated GitHub code search for further automation. |
| 16 | UNCTAD legacy WDS/export endpoint probes | Version 585 not addressable; legacy WDS URLs redirect or 404. | Rejected | Retired export route not recovered. |
