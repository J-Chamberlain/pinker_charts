# Consolidated Research History: Figure 10-5

These are historical search records, not the current acceptance decision.

## Local Work At efca1264944eabab2f733bc399027e22b8df6381

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

## 2026-07-09 Targeted Archive Recovery
| Iteration | Query or URL | Result | Accepted or Rejected | Resolved discrepancy |
| --- | --- | --- | --- | --- |
| 17 | Supplemental Graphics PDF text search for Figure 10-5 | Confirmed title, Roser 2016r/ITOPF source note, spill threshold, and oil-loaded definition. | Accepted reference | Anchors the book figure and source note to the canonical PDF. |
| 18 | Wayback CDX for ITOPF statistics page, 2016-2018 | Found multiple 200 snapshots, including 2017-01-19 for the 2016 statistics page. | Accepted archive | Recovered contemporaneous ITOPF context. |
| 19 | Wayback ITOPF 2016 statistics page | Found `seaborne_16.JPG`, captioned as seaborne oil trade and tanker spills, data source UNCTADStat. | Accepted source-family evidence | Recovers closest source image for the gray oil-loaded line. |
| 20 | Digitized archived ITOPF `seaborne_16.JPG` and compared selected years to UNCTAD RMT 2020 | Selected-year MAE 0.058 billion metric tons; max absolute difference 0.194. | Accepted diagnostic only | Supports visual reconstruction but does not recover original annual table. |
| 21 | ITOPF Oil Tanker Spill Statistics 2017 PDF | Confirmed same chart concept and UNCTADStat label; PDF text exposes spill tables but not oil-loaded annual table. | Accepted context | Confirms source family and continued publication format. |

## Updated Stop Reason

The closest recovered source for the oil-shipped-by-sea line is an archived ITOPF chart image, not the original annual UNCTADStat table. The book-period plot is therefore image-digitized and remains a `partial_match`. No extension is plotted.


## GitHub Recovery At 9a19519494ec20f45b3ac3e6b3122d38a2bc0892

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
| 17 | Web search for `US.SeaborneTrade_585_20231104_101924.csv` | Found a 2023 Medium replication article naming that local export file and stating UNCTADStat provided 1970-2021 data, but no downloadable copy of the CSV was found. | Accepted as clue only | Confirms a plausible retired export name; does not recover data. |
| 18 | Current UNCTADStat metadata endpoint `api/reportMetadata/US.SeaborneTrade/en` | Returned title, defaults, and current dataset metadata. | Accepted context | Confirms current source family and default metric-ton units. |
| 19 | Current UNCTADStat bulkfiles endpoint `api/reportMetadata/US.SeaborneTrade/bulkfiles/en` | Returned one public bulk file, `US_SeaborneTrade`, labeled `From 2000 to 2024`. | Accepted rejection evidence | Confirms the public live bulk file cannot cover 1970-1999. |
| 20 | Current UNCTADStat bulk download `bulkdownload/US.SeaborneTrade/US_SeaborneTrade` | Downloaded archive named by response header as `US_SeaborneTrade.csv.7z`; extracted CSV saved under `data/candidates/`. | Accepted diagnostic only | Provides current source-family data but not the book-period gray line. |
| 21 | Current UNCTAD bulk cargo 11+12 vs RMT 2020 selected-year scale check | Overlap differences are approximately 31-48 percent for 2000, 2005-2019. | Rejected for plotting | Shows the current bulk cargo sum is not a comparable replacement for the book/RMT tanker-trade line. |
| 22 | Current UNCTAD metadata endpoints for report version `585` | `titleAndPublicationDate` and `bulkfiles` requests returned invalid report/version combination. | Rejected | Current UNCTAD API does not expose the 2023 `585` export as a valid historical version. |
