# Figure 5-2 Candidate Source Files

These files were recovered during the 2026-07-09 source-recovery run.

## `archive_searches/`

- `owid_child_mortality_20160423.html`: Wayback copy of the OWID Roser 2016a
  child-mortality article. Its country-by-country section embeds old Chart
  Builder view 58.
- `chart_builder_view_58_*.html`: Wayback HTML shells for old Chart Builder
  view 58. These identify the chart view but do not contain the underlying data
  payload.
- `chart_builder_public_cdx_2015_2016.json` and
  `chart_builder_all_cdx_2015_2016.json`: CDX results used to check whether
  the old dynamic `data/config/58` or equivalent dimensions endpoint had been
  archived. No captured view-58 data payload was found in this run.
- `js/`: small archived Chart Builder JavaScript files used to identify the old
  endpoint pattern.

## `owid_datasets_candidates/`

Recovered from `https://github.com/owid/owid-datasets`:

- `Child mortality estimates - Gapminder (2015)`: source-family candidate;
  cites CME Info and HMD but lacks the visible 1751-1799 Sweden segment.
- `Child Mortality Rates (Selected Gapminder, v10) (2017)`: later
  source-family successor; post-book vintage.
- `Child Mortality Estimates - CME Info (2018)`: UN IGME/CME Info candidate,
  mostly 1950 onward and therefore insufficient for the long-run figure.

None of these candidate datasets is treated as the exact Pinker/Roser book
dataset.
