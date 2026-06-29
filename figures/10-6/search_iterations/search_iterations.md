# Search Iteration Log: Figure 10-6

Accessed: 2026-06-28

| Iteration | Query or URL | Result | Accepted or Rejected | Resolved discrepancy |
| --- | --- | --- | --- | --- |
| 1 | `https://api.worldbank.org/v2/en/indicator/ER.LND.PTLD.ZS?downloadformat=csv` and `https://api.worldbank.org/v2/en/indicator/ER.MRN.PTMR.ZS?downloadformat=csv` | Current individual indicator ZIPs contain World values only from 2013 onward. | Rejected as exact reproduction | Confirms current API limitation. |
| 2 | `https://databankfiles.worldbank.org/public/ddpext_download/WDI_CSV.zip` | Current full WDI bulk also begins World values in 2013 for the target indicators. | Rejected as exact reproduction | Confirms limitation is not API-specific. |
| 3 | Wayback CDX for `databank.worldbank.org/data/download/WDI_csv.zip` | Found archived WDI bulk snapshots including 2017-10-12. | Accepted context | Identifies historical release path. |
| 4 | `https://web.archive.org/web/20171012170642id_/http://databank.worldbank.org/data/download/WDI_csv.zip` | Downloaded archived WDI ZIP; extracted WLD rows for land, marine, and combined protected areas. | Accepted | Recovers 1990, 2000, 2014 anchor values matching the book range. |
| 5 | `Combined Protected Areas.xls` from UNSD/MDG candidate | Contains country-level combined protected-area values for 1990/2000/2008, not global land/marine annual series. | Rejected for this figure | Useful provenance only. |
| 6 | Protected Planet Report 2014 PDF | Confirms UNEP-WCMC/WDPA source family and 2014 protected-area context. | Accepted context | Supports institutional chain but not the exact chart table. |

## Stop Reason

The archived 2017 WDI file resolves the main discrepancy and supplies the book-range values. Further work should verify whether Pinker plotted only the WDI anchor years or obtained an annual/interpolated WRI table.
