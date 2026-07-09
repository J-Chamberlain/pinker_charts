# Source Discovery Log: Figure 5-2

Figure title: Child mortality, 1751-2013

Original book citation: Our World in Data, Roser 2016a, based on UN Child Mortality Estimates and the Human Mortality Database.

## Search Queries Attempted
- "Figure 5-2" Kindle search
- "Child mortality, 1751-2013" Our World in Data dataset
- "Child mortality, 1751-2013" historical CSV
- "Our World in Data, Roser 2016a, based on UN Child Mortality Estimates and the Human Mortality Database."
- Internet Archive and successor dataset checks
- 2026-07-09 targeted Wayback checks for `ourworldindata.org/child-mortality/`,
  old Chart Builder view 58, and related Grapher migrations.
- 2026-07-09 targeted `owid/owid-datasets` recovery for Gapminder 2015,
  selected Gapminder 2017, and CME Info/UN IGME candidates.

## Sources Investigated
- Kindle search/page capture: accepted for title, citation, and visual reference where captured.
- Supplemental Graphics PDF page 3: accepted as canonical figure image and
  source note evidence.
- Local OWID datasets mirror: accepted where it matched the named source chain or as a documented proxy.
- Current OWID grapher downloads: accepted only as successor/extension evidence.
- Internet Archive/GitHub/source mirrors: logged as required next searches where exact archival source remains unresolved.
- Prior Gapminder 2013 proxy: rejected for current canonical reconstruction because it visibly diverged from the Kindle figure.
- Current OWID selected child-mortality grapher: accepted as an improved proxy after confirming that the downloaded values are already percent units.
- Archived OWID child-mortality article, 2016-04-23: recovered. Its long-run
  country section embeds `http://ourworldindata.org/chart-builder/public/view/58`.
- Archived Chart Builder view 58 shells, 2015: recovered, but the dynamic
  `data/config/58` payload was not recovered from Wayback in this run.
- `Child mortality estimates - Gapminder (2015)`: recovered from
  `owid/owid-datasets`; source-family candidate only.
- `Child Mortality Rates (Selected Gapminder, v10) (2017)`: recovered from
  `owid/owid-datasets`; post-book successor/source-family candidate only.
- `Child Mortality Estimates - CME Info (2018)`: recovered from
  `owid/owid-datasets`; UN IGME candidate only, mostly 1950 onward.

## Remaining Uncertainties
- Status is `partial_match`. The exact Roser 2016a assembly based on UN Child Mortality Estimates and the Human Mortality Database remains unrecovered.
- Remaining visual differences are most likely source-vintage/country-series construction rather than only styling.
- The 2015 Gapminder candidate cites CME Info and HMD but does not include the
  1751-1799 Sweden segment visible in the book. The UN/CME candidate does not
  cover the pre-1950 historical segment. The current OWID successor has the
  visible coverage but is a current migrated dataset, not a pinned 2016 export.

## Recommended Next Steps
- Continue targeted recovery for old Chart Builder view 58, especially
  `data/config/58` or the corresponding downloaded dimensions CSV.
- Search Max Roser/OWID backups, old WordPress uploads, and possible direct
  Chart Builder database dumps for the 2015-2016 view 58 payload.
- Do not upgrade the figure until the exact historical dataset or an archival equivalent is recovered.

See also: `source_recovery_report_2026-07-09.md`.
