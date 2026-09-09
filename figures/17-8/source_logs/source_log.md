# Figure 17-8 source discovery

Title: International tourism, 1995-2015. Original citation: World Bank 2016e,
based on World Tourism Organization, Yearbook of Tourism Statistics.
Research date: 2026-09-09. Full download URLs, responses and hashes are in
`downloads.json`; archive search responses are retained in `data/candidates/`.

| Investigated source | Outcome and decision |
| --- | --- |
| Supplied graphics PDF p36, lower panel | Accepted original visual/source reference; actual pixels inspected, never used for numeric data |
| World Bank ST.INT.ARVL indicator and metadata | Accepted source-chain identification; no author access date established |
| Current WDI API WLD/ST.INT.ARVL | Downloaded; rejected as historical/extension input because much larger historical totals; retained for diagnostic |
| Internet Archive CDX, 2016, ZIP MIME filter | Empty response; recognized overrestrictive filter, not evidence of unavailability |
| CDX 2015-2017 annual and 2016/2017 monthly queries | Located November 2016, January/May/October 2017 archives; archive URLs and query parameters retained |
| November 2016 WDI ZIP | Accepted 1995-2014 source; no 2015 World observation |
| January 2017 WDI ZIP | Same book-era World history and missing endpoint; rejected as a solution to 2015 |
| May 2017 WDI ZIP | Revised 1995-2014 series and 2015 endpoint; confirms transition occurred by May, not a complete original-vintage solution |
| October 2017 WDI ZIP, already retained under 10-6 | Only 2015 endpoint used in book reconstruction, explicitly marked; revised full history shown diagnostically |
| OWID international-tourist-trips, UN Tourism 2025 source | Downloaded CSV and metadata; no World aggregate, heterogeneous collection caveats; not summed for reconstruction |
| OWID international-tourist-arrivals-by-world-region | Redirects to international-tourist-trips-by-destination-region; UNWTO 2019 data, complete five-region annual observations for 2015-2018; accepted short successor segment, not current data |
| UN Tourism January 2026 news webpage | Web access returned 403; search located official public PDF rather than treating this as source unavailable |
| UN Tourism January 2026 news PDF/search result | Useful latest annual context; rejected as input in favor of a complete source table |
| November 2025 UN Tourism Barometer via CzechTourism institutional mirror | Downloaded, numeric World table found; superseded by January 2026 table, retained locally not republished |
| January 2026 official UN Tourism Barometer excerpt, p6 | Accepted seven World annual table observations, 2019-2025; 2025 provisional; pypdf extraction visually confirmed |
| World Bank 2016 update blog, WDI 2011 PDF search results | Background/archive leads only, not graph inputs |
| Scribd, secondary tourism reports and search-result aggregators | Not used for data; official/institutional documents obtained instead |

## Remaining uncertainties / next targeted recovery

Locate Pinker's saved WDI download or a 2016/early-2017 indicator-specific capture
with a 2015 World total. The located ZIP snapshots do not establish that endpoint.
An author supplement or archived indicator API response would be stronger than
mixing vintages. Do not alter the first 20 values simply to use a single modern
table. Investigate the current WDI aggregate's collection/aggregation change
before any future automatic refresh. Search is substantial but not exhaustive.

The download cache initially lost two concurrently appended OWID log entries;
both retained files were re-registered by URL/hash without another download.
The cache writer now locks the log and rereads it before appending. Their
original HTTP-200 retrievals occurred on this date; re-registration timestamps
are not claimed to be first-download times. The November 2025 PDF's original
download path was subsequently moved to `tmp/source_cache/` for rights reasons.
