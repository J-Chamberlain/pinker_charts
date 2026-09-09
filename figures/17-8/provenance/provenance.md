# Figure 17-8 provenance

Original: Steven Pinker, *Enlightenment Now*, Figure 17-8, **International
tourism, 1995-2015**. Authorized visual reference: supplied Supplemental Graphics
PDF, page 36, lower panel. Title, source and chart inspected at full resolution.

Short original citation: "World Bank 2016e, based on data from the World Tourism
Organization, Yearbook of Tourism Statistics."

## Citation chain and versions

Book -> World Bank WDI -> World Tourism Organization Yearbook/Compendium ->
international tourist arrivals, `ST.INT.ARVL`, World aggregate `WLD`.
[Institutional metadata](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/ST.INT.ARVL)
confirms the source chain, annual frequency, and gap-filled aggregation. Arrivals
are trips, not distinct people. Countries can use different collection methods;
the metadata allows visitor arrivals when overnight tourist counts are missing.
The book's bibliography key has been resolved at institutional/indicator level,
not to an author-saved download or exact access date. Surrounding chapter prose
was not available in the supplied graphics PDF and is not fabricated here.

| Role | Retained source | Selection |
| --- | --- | --- |
| Book history | `data/raw/wdi_2016_world_row.csv` | WLD/ST.INT.ARVL, 1995-2014 |
| Book endpoint, explicitly later vintage | `data/raw/wdi_2017_october_world_row.csv` | 2015 only |
| Early successor | `data/candidates/owid_regional_arrivals_2026_09_09.csv` | Five nonoverlapping UNWTO destination regions, sum for 2015-2018 |
| Recent successor | `data/raw/un_tourism_2026_01_world_table.csv` | World row, January 2026 Barometer page 6, 2019-2025 |
| Rejected modern aggregate | `data/raw/world_bank_tourism_current_2026_09_09.json` | Diagnostic only, never a reconstruction input |

Raw WDI extracts preserve original CSV cell strings and include the full source
archive SHA-256/member/selection/series metadata in adjacent JSON. The 2016 ZIP
is retained; the previously retained October 2017 ZIP lives under Figure 10-6.
January and May 2017 snapshots were also investigated. January still lacks
2015; May contains the revised history also found in October. No located release
contains the complete book-looking 1995-2015 trajectory. A later endpoint is
therefore a disclosed substitution, not proof of exact vintage identity.

The recent seven observations are automatically extracted from an actual
numeric table using pypdf, then visually checked against the rendered page.
They are not transcribed or digitized from a graph. Full UN reports remain in
the ignored local `tmp/source_cache/` directory because the publisher prohibits
posting complete PDFs publicly. Seven attributed factual observations, source
URL, page, release date, hash and extraction code are retained for reuse.

## Transformations and refresh

`scripts/reconstruct_17_8.py` runs offline. It divides arrivals by 1e9 for the
book axis. The seven recent table values are in millions, converted to arrivals
by multiplying by 1e6. The five destination-region sum is accepted only when
each year contains all five unique regions. No country-level OWID sum is used:
that dataset lacks a World row and mixes country collection conventions.

No smoothing, normalization, interpolation, chart digitization or adjustment to
force a visual match. The 2015 WDI endpoint, 2015 successor overlap and 2019
source change remain distinct. No line connects the 2018 and 2019 vintages.

Freeze all present inputs. Refresh by downloading a **new dated release**, checking
definitions and overlap, and adding a new source version rather than replacing
these files. Rebuild the SQLite library after changing clean data. The long
clean table preserves year, units, role, source version and provisional flags.
The January 2026 release is the chosen extension vintage, not a claim that no
later 2026 revision exists. Compare a later complete table before updating.

## Limitations

The exact book-era 2015 endpoint is unresolved. Current World Bank totals are
much larger than the historical release; country visitor definitions and
aggregation revisions are plausible explanations, not a proved causal audit.
UN Tourism regional totals and World Bank gap-filled totals are not guaranteed
identical. The extension is a transparent conceptual successor, not a seamless
continuation of the original data vintage. Full rights clearance for public
book-reference images remains a project-level publication task.
