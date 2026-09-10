# Figure 14-4 provenance

Original supplied Supplemental Graphics PDF p24 lower, directly inspected.
Title Executions, US,1780-2016. Source: Death Penalty Information Center2017;
population estimates U.S. Census Bureau2017. Arrow identifies2010.

## Records and archives
The DPIC Espy workbook was recovered from an April19,2016 archive:
https://web.archive.org/web/20160419133009id_/http://www.deathpenaltyinfo.org/documents/ESPYFile.xls.
Current https://deathpenaltyinfo.org/documents/ESPYFile.xls has different binary
hash but an exactly equal data table,15296records1608-2002. Homepage says15269:
that count does not match the file. Some visible records repeat, including
unnamed people; do NOT deduplicate these without original case IDs. Per-record
source row/year/state and repeated-visible-field flag are preserved in clean data.
Full raw records remain saved. Source authors: M.Watt Espy and John Ortiz Smykla;
ICPSR8451. Used DPIC's public spreadsheet rather than requiring ICPSR credentials.

Modern current data: https://deathpenaltyinfo.org/query/executions.csv.
Archived export at https://web.archive.org/web/20161029141325id_/http://www.deathpenaltyinfo.org/exec-xls-export
is actually CSV despite its.xls filename. Annual counts1977-2015 match current
data exactly. Archive ends October19,2016(17executions), so it is not used as a
complete2016total. Current2016count20 agrees with Amnesty2016facts in14-3raw data.
Espy and modern counts differ in1991(2vs14) and2001(65vs66): modern series is used
from1977, not a duplicate sum of both.2026partial records excluded from all plots.
CDX search for later original export returned503, recorded, not falsely exhausted.

## Population
- Census2012Statistical Abstract Table1, released2011, supplies1790-2010decennial
resident populations (including table footnote corrections):
https://www2.census.gov/library/publications/2011/compendia/statab/131ed/tables/12s0001.xls.
- Census1960Historical Statistics colonial TableZ1,p756(PDFp14) supplies1780total:
https://www2.census.gov/library/publications/1960/compendia/hist_stats_colonial-1957/hist_stats_colonial-1957-chZ.pdf.
Extracted numeric text cell2,780,369; original table rendered and visually checked.
This is numerical table extraction, not chart digitization.
- Vintage2016annual population2010-2016:
https://www2.census.gov/programs-surveys/popest/datasets/2010-2016/national/totals/nst-est2016-alldata.csv.
- Later estimates:2019vintage for2010-2019 and2025vintage for2020-2025:
https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/national/totals/nst-est2019-alldata.csv
https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/state/totals/NST-EST2025-ALLDATA.csv.
Select unique SUMLEV10/NAMEUnitedStates, never sum states plus national total.

## Transformation and fidelity
Combine Espy through1976 with modern counts from1977. For1780-2009, total
executions per decade /10 / average of bounding census populations *100000.
Plot at decade start. For2010-2016 use annual count / vintage2016population.
This inferred averaging rule reproduces the original shape very closely, unlike
individual census-year counts; author code has NOT been located. No arbitrary
vertical shift. Minor low-rate differences remain and temporal aggregation is
not confirmed by the short source note: partial_match rather than verified.
A single positive stroke above zero in a printed chart is not permission to
add an offset to real values.

Extension: same judicial-execution definition, annual2017-2025, revised national
population vintages. Dotted2010-2016overlap and dashed subsequent years in an inset;
large-scale main plot otherwise makes modern changes almost invisible.2025is
47executions /341,784,857people.2026is incomplete and intentionally absent.
Country borders, missing historical records and legal categories are source limits.
The judicial record database does not count extrajudicial killings or all lynchings.

All URLs/date/hashes retained, raw input→script→clean→plot lineage explicit.
Reproduce: `.venv/bin/python scripts/reconstruct_14_4.py`.
Refresh: download new DPIC CSV and Census vintage to new immutable paths, compare
overlap and full-year coverage before promotion. Do not overwrite historical bytes.
Full surrounding Pinker text and independent publication acceptance remain pending.
