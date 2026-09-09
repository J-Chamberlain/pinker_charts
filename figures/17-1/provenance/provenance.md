# Figure 17-1 provenance

Original: Work hours, Western Europe and US, 1870-2000. Supplied Supplemental Graphics PDF page 33 upper panel; inspected directly. Weekly hours, full-time production workers of both sexes, nonagricultural activities. Original linear scale 0-70, thirteen benchmark years connected by lines. Source: Roser 2016t, Huberman & Minns 2007. Surrounding Kindle prose not consulted; no unseen prose extraction claimed.

## Citation and numerical chain

Michael Huberman and Chris Minns (2007), *The times they are not changin': Days and hours of work in Old and New Worlds, 1870-2000*, Explorations in Economic History 44(4), 538-567. DOI 10.1016/j.eeh.2007.03.002. [Author-hosted paper](https://personal.lse.ac.uk/minns/huberman_minns_eeh_2007.pdf), Table 1, printed p542 (PDF p5). Full PDF retained only in ignored temporary cache; URL and SHA logged. Numeric data are retained OWID CSVs, not plot readings.

OWID dataset exports were downloaded at pinned Git SHA 6155d4ca1ea14ef30e753010a25521eeb416e8a2. The *Days and hours* export contains published totals, sex-specific 2000 estimates and Old World aggregates. Dataset 234, *Working Hours Data*, independently contains US weekly figures and documents averaging male/female values for 2000. A 2016 archived OWID chart identifies original weekly variable 348. Current OWID data retain the same US values, ending in 2000; its 2005 citation refers to the earlier working-paper version and is not silently substituted for the book's 2007 citation.

## Transformations

Run `.venv/bin/python scripts/reconstruct_17_1.py` offline. Select United States and unweighted Old World; label the latter Western Europe as in the book, with explicit provenance. The source regional series is retained as published, not reweighted by present-day population. Thirteen benchmark years from 1870 through 2000, 26 book rows. Float32 artifacts in the historical export are rounded to the original table's one-decimal precision. For 2000 only, take the equal mean of male and female published values, following OWID's documented method; this is not a labor-force-weighted sex aggregate. Two retained OWID exports are checked for US agreement. No subtraction, interpolation into extra observations, smoothing or chart digitization.

Unweighted versus population-weighted Old World is retained as a 39-row diagnostic. The latter has different shape and does not explain a common vertical difference affecting the US too. Preserve the actual source values despite that mismatch.

## Extension decision

No extension plotted. Current same-variable OWID series ends in 2000. [JRC 2024 working-time study](https://publications.jrc.ec.europa.eu/repository/bitstream/JRC139815/JRC139815_01.pdf) covers later EU-LFS observations but its long-run splice changes to all workers in 1992, not the original production-worker population. [OECD 2021 manufacturing history](https://www.oecd.org/en/publications/how-was-life-volume-ii_3d96efc5-en/full-report/component-8.html) is a promising sectoral source, not evidence of identical population, sex aggregation and regional composition. Do not divide annual hours by 52 to manufacture the required variable. Matching ILO/LABORSTA successor microdata and national definitions remain a targeted task.

Raw sources, metadata, version URLs, dates and checksums retained under data/raw and source_logs; clean observations enter the immutable SQLite library. Future refresh should preserve these book-period inputs and version a separately documented successor. Full author manuscript is linked rather than redistributed.
