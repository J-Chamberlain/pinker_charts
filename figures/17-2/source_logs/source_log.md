# Figure 17-2 source discovery

Book title and citation: see provenance; discovery 2026-09-09. Every download attempt, URL, status and SHA256 is in downloads.json. Browser retrieval is separately recorded in browser_retrieval.json. Search queries are in search_iterations/search_iterations.md.

| Source investigated | Decision |
| --- | --- |
| Pinned OWID Git export, dataset 425 (2017 Short/OECD assembly) | Retain cross-check. Reject as main input because 2000 is replaced by OECD and book cites Housel/BLS/Costa. |
| EH.Net Short (2002), Table 1 | Accept 2000 and historical cross-check; BLS release behind 2000 remains uncertain. |
| NBER book and chapter pages | Accept bibliography; web search tool 403, normal Python retrieval successful. |
| NBER original Costa chapter PDF, Appendix 2A.1 | Accept original 1880-1990 numeric table. Table 2A.2 has inconsistent 1980 text extraction and is not selected; use uniquely labeled 2A.1. |
| Motley Fool author index and related article | Resolve exact Housel title/date/link. No numeric worksheet supplied. |
| AOL syndicated May 3, 2013 article | Confirms Housel attribution; original Motley Fool preferred. May 2 AOL variant failed. |
| Goodreads indexed J.D. Roth quotation | Discovery lead only; not data or evidence for numeric accuracy. |
| BLS May 2025 article, numeric Chart 2 table | Accept modern continuation and definition diagnostic. Requests 403, ordinary browser table extraction succeeded. |
| BLS archive, 2010 annual Table 3 PDF | Accept original 2010 endpoint; matches modern BLS table's 2010 value. |
| FRED LNU01300199 candidate / EconStats series directory / academic BLS series reference | Series identity leads only; no downloaded FRED numeric input. Official BLS table recovered instead. |

Archive recovery was successful via the original Costa publication, pinned OWID release and BLS 2010 annual PDF. No claim of an exhaustive Internet Archive search: the remaining targeted task is Housel's assembly or original release behind Short's 2000 entry. Broader current-data substitution cannot resolve the book-level differences.

Next: resolve small visual level differences with the author/source assembly; preserve the definition break. Obtain a later complete annual release for extension refresh when available, never overwrite this snapshot.
