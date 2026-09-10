# Source discovery - Figure16-6

Title and original citation: figure.json; source/units inspected in PDFp32lower.
All download URLs, redirects, timestamps, response failures and hashes are in
downloads.json and downloads.jsonl (the latter contains a JSON array despite its
legacy suffix). Sources below were evaluated2026-09-09Pacific/10UTC.

| Source | Decision |
| --- | --- |
| OECD2014 original reportp259 and StatLink888933096502 | Accepted original equal-weight World composite; retained XLS |
| ClioInfra CompositeMeasureofWellbeing page/compactdownload | Different latent-variable indicator; download403; not substituted |
| IISG Dataverse hdl10622/QIPFQF |2017dataset with2014production; metadata identifies latent-variable measure; API403; not necessary for equal-weight original |
| OECD2021HowWasLifeII component16, stat.link/yc1djg | Retained successor-comparison XLSX; latent-variable/new-indicator method, not continuation |
| OWID pinned Git HIHD dataset at6155d4c | Empty CSV; never treated as usable data |
| OWID Git commits API and3b27d632 snapshot | Retained2018source-vintage country data through2015, noWorld; no unsupported aggregation |
| OWID April24,2016 and January28,2017 archived topic | Accepted historical citation/path evidence; regional download retained, ends2007andnoWorld |
| Prados2015 original paper DOI10.1111/roiw.12104 | Accepted published WorldTable1,14benchmarks, numerical extraction visually checked |
| UC3M2013working paper hdl10016/16138 | Source-chain confirmation, earlier same2007horizon; not a2015update |
| Prados2015CEPR author article | Confirms original publicdatabase covers through2007andlinksEspacioInvestiga |
| EspacioInvestiga provider page and HIHD.xls current/archive | Recovery attempts logged; unresolved World2015vintage |
| Prados2022 AHDI viaOWID | Different index adds freedom, coverage1870-2020; not spliced |
| Wikimedia copy ofOWID2780 | Located but primary Git numeric release recovered instead |

Remaining uncertainties: exact2015World HIHD release, population weights and
annualization used by book, annual composite detail, missing surrounding context.
Next step: recover archived EspacioInvestiga regional/World workbook or author
release2016-2017; compare overlap to originalTable1 before accepting it. Then
inspect revisedHIHD without political freedom for possible comparable extension.

Provider retrieval detail: the current landing page timed out before receiving
an HTTP response. The current HIHD.xls request was interrupted after more than
three minutes in socket connection, with no file downloaded; interruption does
not prove the file absent. The archive-only request then returned404. The
interrupted request is recorded here because it did not reach the JSON logger.
