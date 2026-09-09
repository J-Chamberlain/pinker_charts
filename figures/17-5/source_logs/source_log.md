# Figure 17-5 Source Discovery

Figure: Spending on necessities, US, 1929-2016. Book citation: HumanProgress
dataset 1937, Mark Perry, BEA. Original supplied PDF p35 inspected. Research
date: 2026-09-09. Every query is in the search-iteration log; machine download
successes/failures and hashes are in `downloads.json`. Browser numeric exports
carry URLs and retrieval dates and are hashed in checksums/lineage.

| Source investigated | Result / decision |
| --- | --- |
| http://humanprogress.org/static/1937 | Current route unavailable; do not infer data vanished. |
| https://web.archive.org/web/20170101000000id_/http://humanprogress.org/static/1937 | Redirects to 20170117185627. Accepted archived numeric JSON, original dataset identity and September 2016 update. Baseline basket excludes energy; not itself the final book plot. |
| https://fred.stlouisfed.org/release/tables?rid=53&eid=44183#snid=44219 | Direct request timed out; public browser table worked. Retained component names, series links and current table. Authoritative BEA identities. |
| https://apps.bea.gov/national/nipaweb/DownSS2.asp | HTTP 403; legacy bulk retrieval unavailable here. |
| https://apps.bea.gov/national/Release/XLS/Survey/Section2All_xls.xlsx | Web retrieval did not resolve; no numeric input accepted. |
| https://api.db.nomics.world/v22/series/BEA/NIPA-T20305?limit=1000&observations=1 | Exploratory mirror endpoint did not resolve; not used. |
| https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGOERC1A027NBEA&vintage_date=2016-09-06 | Direct CSV timed out. No empty or error-response file accepted as data. |
| https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=A067RC1A027NBEA&vintage_date=2016-09-06 | Direct CSV timed out. |
| ALFRED series pages for DFXARC1A027NBEA, DMOTRC1A027NBEA, DFDHRC1A027NBEA, DCLORC1A027NBEA, DHUTRC1A027NBEA, DGOERC1A027NBEA, A067RC1A027NBEA | Accepted original 2016 and current 2026 numeric labels, 87 + 97 years per series. Exact URLs retained in raw JSON. Full coverage checked, not merely visually assumed. |
| ALFRED DMFLRC1A027NBEA | Accepted diagnostic narrower motor-fuels series. Historical vintage is August 3, not July 29. It does not account for the early book levels and is not used in the reconstruction. |
| Cafe Hayek November 2012, The Future Back to the Past | Linked contextual literature from archive, not a component dataset. No values taken from it. |
| Mark Perry / AEI, 2013 Washington Post and TCF commentary search results | Context indicated differing basket/aggregate-income interpretations; not accepted as numeric source or original figure reference. |

Browser download dropdown and data-table controls did not expose an export.
Numeric accessibility labels were available and retained with source vintage.
A first motor-fuels export contained only one year because the vintage update
reset the range asynchronously. It was replaced after validating 184 source
observations; the parser now rejects missing expected years. No false full
coverage claim is made from the initial export.

Remaining uncertainty: exact author energy definition; residual later-level
differences; 2016 title versus 2015 archive endpoint; later author revisions.
Next: recover Pinker's/Perry's final calculation file or later archived HP
versions, compare numeric source revisions, and preserve this audited 2016
baseline. Historical GitHub/academic supplement searches are not claimed
exhaustive: the original institutional numeric chain was already recovered.
