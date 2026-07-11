# Provenance: Figure 5-2

Book figure -> supplemental/Kindle evidence -> archival source search ->
current OWID successor proxy -> `scripts/reconstruct_figure_5_2.py` ->
documented partial-match plots.

Source note: Our World in Data, Roser 2016a, based on UN Child Mortality Estimates and the Human Mortality Database.

## Book evidence

- Figure title and range: “Child mortality, 1751–2013.”
- Y-axis: percentage of children dying before age 5, linear 0–50 percent.
- Lines: Sweden, Canada, South Korea, Chile, and Ethiopia.
- Source line: “Our World in Data, Roser 2016a, based on data from the UN
  Child Mortality estimates, http://www.childmortality.org/, and the Human
  Mortality Database, http://www.mortality.org/.”
- Surrounding chapter text says child mortality has fallen in rich and poor
  countries and uses the long-run decline as evidence of health progress. The
  local evidence retained for this run is the chart-page crop; the complete
  supplemental PDF and surrounding prose are not stored in this checkout, so
  no additional wording is claimed.

## Bibliography resolution

The book bibliography entry is resolved as: Max Roser, “Child Mortality,”
*Our World in Data* (2016), `https://ourworldindata.org/child-mortality/`.
The figure’s `2016a` suffix is the book’s disambiguation key. This resolution
is supported by the title/author/year combination and later citations of the
same OWID page; the current page is a successor, not proof of an unchanged
2016 dataset.

## Recovered archival source

OWID commit `b6746f923dd64ca0fad7de1b1f2f78bebe25205f` preserves “Child
Mortality Estimates - CME Info (2016),” dataset ID 161. Its metadata says OWID
retrieved it from `http://childmortality.org/` on 2016-01-29 and identifies the
UN Inter-agency Group for Child Mortality Estimation. The immutable CSV and
metadata are stored in `data/candidates/`. It runs from 1970 through 2015, so
it is a recovered contemporaneous component, not the missing UN/HMD assembly.

No HMD-derived chart export was found in the complete history of the public
`owid/owid-datasets` repository. Wayback CDX queries for
`ourworldindata.org/grapher/child-mortality.csv` returned no captures. The HMD
source also historically required controlled access, preventing a defensible
fresh reconstruction of the exact 2016 input without the assembly rules.

## Closest verifiable successor and transformation

The stored current OWID `child-mortality.csv` export is used only as a
successor proxy. Its metadata endpoint (retrieved 2026-07-10 local time and
reporting `dateDownloaded` 2026-07-11 UTC) identifies a changed
source chain: Gapminder (2015) plus UN IGME (2025), processed by OWID. The
distinctive Sweden trajectory and the later country trajectories visually
track the book, but the live file contains earlier Gapminder segments absent
from the figure and later source revisions.

The script:

1. retains only the five visible countries and values through 2013;
2. keeps percent units unchanged;
3. clips each line to its book-visible start (Sweden 1751, Canada 1921, South
   Korea 1950, Chile 1955, Ethiopia 1966); and
4. records every clean row as `current_owid_successor_proxy`.

Those cutovers are visual layout constraints, not recovered source facts. The
clean values match the stored successor CSV exactly (floating-point parsing
only); this proves transformation fidelity to the proxy, not fidelity to the
unrecovered 2016 assembly.

## Extension decision

No post-2013 segment is plotted. The current OWID series has different named
sources and a 2025 UN-IGME vintage, so comparability to the cited 2016 UN/HMD
assembly is not established. The “extended” artifact repeats the documented
book-window approximation and explicitly states that no comparable extension
is available.
