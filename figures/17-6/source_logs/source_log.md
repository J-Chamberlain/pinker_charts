# Figure 17-6 Source Discovery

Date: 2026-09-09. Figure: Leisure time, US, 1965-2015. Book citation:
Aguiar/Hurst 2007 Table III and BLS 2016c ATUS 2015. Exact searches are in
`search_iterations/search_iterations.md`; actual download failures and hashes
are in `downloads.json`. Do not confuse a successful source chain with a
verified visual reconstruction.

| Investigated source | Decision |
| --- | --- |
| https://www.markaguiar.com/files/leisuretrends.pdf | Accepted author copy of published QJE paper, Table III. Numeric extract only in Git. |
| https://markaguiar.com/papers/timeuse_data/aguiar_hurst_leisure_revision_9_06.pdf | Accepted manuscript cross-check; all ten Measure 1 sex/year entries agree. |
| https://academic.oup.com/qje/article-abstract/122/3/969/1879557 | Confirms DOI, publication date and bibliographic identity. Not a separate dataset. |
| https://www.bls.gov/news.release/archives/atus_06242016.htm | Original 2015 release; direct request 403, browser Table 1 retained. Accepted endpoint source, cross-checked against A-1 PDF. |
| https://www.bls.gov/news.release/atus.htm | Current direct HTML 403; use official annual PDFs instead. |
| https://www.bls.gov/tus/tables.htm | Accepted official successor index. Ten annual A-1 PDFs 2015-2025 downloaded; 2020 is explicitly unavailable. URLs in retained manifest. |
| https://www.bls.gov/tus/database/labstattips.htm | Evaluated time-series method/weighting guidance. Bulk 110 MB database unnecessary after original annual PDFs recovered. |
| http://troi.cc.rochester.edu/~maguiar/timeuse_data/datapage.html | Obsolete paper data link unavailable. |
| https://markaguiar.com/papers/timeuse_data/datapage.html and www variant | Web retrieval failed. Do not interpret as lost underlying data. |
| https://web.archive.org/web/20070101000000id_/http://troi.cc.rochester.edu/~maguiar/timeuse_data/datapage.html | Archive query did not resolve through web tool. No archive bytes accepted. |
| https://www.markaguiar.com/ | Accepted current author research index; found relocated original data, paper, supplement and DOI. |
| Author-linked Dropbox replication archive (full URL in provenance and raw manifest) | Accepted source analysis cells and compact merged data. Hash every archive member; retain numeric data unchanged. Original Stata code inspected to reproduce weighting, not executed. |
| https://markaguiar.github.io/files/robustness_appendix.pdf | Reviewed robustness design; alternative demographic/day/season controls are diagnostics, not the cited Table III substitution. |
| https://github.com/markaguiar/Time-Use-Great-Recession | Different 2013 paper, useful possible future adapter, not original 2007 source. |
| https://econweb.ucsd.edu/~vramey/research/How_Much_Has_Leisure_Really_Increased.pdf | Scholarly critique identified as follow-up context, not substituted for source values. |

Remaining: exact Pinker final assembly; matched-population 2015/continuation;
publication rights for author microdata. Original data unavailability is NOT
claimed: the analysis data and code were recovered. Reasonable next steps
are author-file reconciliation and a separate microdata harmonization exercise,
not moving the line to make a screenshot match.
