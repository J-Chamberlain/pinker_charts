# Figure 14-1 provenance

Original: Supplemental Graphics PDF p23 upper, original crop and hash in
figure.json. Title: Democracy versus autocracy, 1800-2015. Source line names
HumanProgress /f1/2560 and Polity IV Annual Time-Series, Marshall, Gurr and
Jaggers (2016). The reference's arrow marks 2008. Its note says scores are
summed, but the cited provider explicitly defines its aggregation as Average.
Full surrounding book discussion is not present in the graphics PDF.

## Recovered original

https://web.archive.org/web/20170427220920id_/http://humanprogress.org/f1/2560
contains numerical JSON, not values digitized from a chart. Dataset ID2560,
source update July18,2016, World216 annual records, 1800-2015. The raw subset
and source metadata are saved in data/raw. Provider-generated flags are retained:
132 of the216 World records have that flag. We do not relabel them observed.

The original institutional release is also recovered:
https://www.systemicpeace.org/inscr/p4v2015.xls . Numeric means over all valid
Polity or polity2 rows do not exactly reproduce the HP World aggregate. For
example, HP1800 uses a different historical-country set. Its generated country
values and changing coverage affect mid-century estimates. Simply including
Polity's -66/-77/-88 special codes in a mean is invalid. Our diagnostic exports
both valid(-10 to10) Polity means and the source's polity2 means.

The archived provider World curve is the closest directly cited numeric source,
but visible deviations remain around the 1940s. No data are altered to force a
match; scientific status remains partial_match.

## Later data

https://www.systemicpeace.org/inscr/p4v2018.xls and
https://www.systemicpeace.org/inscr/p5v2018.xls provide broad coverage through
2018. The current latter file also contains isolated US1776-1799 and2019-2020
rows; these are NOT global coverage. The plotting input restricts to1800-2018
and tests at least150 contributing countries at/after2015. Polity5 revises
historical scores; it is not an append-only update. Both successor trajectories
are shown in a separate recent-period panel, dotted overlap through2015 and
dashed later. No offset alignment or hidden splice.

Manual: https://www.systemicpeace.org/inscr/p5manualv2018.pdf . polity2 treats
foreign interruptions as missing, interregnum as0, and transitions by prorating.
This is not identical to dropping all three special codes. The full source
manual was read locally; short methodological summaries only are published.

## Data retention and reproduction

The source explicitly restricts redistribution of whole datasets:
https://www.systemicpeace.org/inscrdata.html . Full source workbooks and the
archived all-country HTML remain locally in ignored `.private_sources/14-1/`,
not in Git. `data/raw/source_manifest.json` preserves exact URLs, hashes and
cache locations. The source log originally names pre-relocation paths; the
manifest records their current location. No original downloaded bytes changed.
Only the small World subset, derived global aggregates and metadata are included
in the public research package. Obtain permission before releasing full datasets;
this is a publication-rights flag, not a claim that numerical facts are secret.

Offline plots rebuild with `.venv/bin/python scripts/reconstruct_14_1.py`.
Full recovery/recalculation: `.venv/bin/python scripts/recover_14_1.py --download`.
It checks exact release hashes and stops for review if a provider changes bytes.
No API key needed. The local-only full data remain available for future analysis;
the SQLite library retains the clean global observations and source manifest.
