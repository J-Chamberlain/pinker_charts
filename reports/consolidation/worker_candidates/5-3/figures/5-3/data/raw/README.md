# Figure 5-3 Raw Data

## Recovered Book Source Component

- `gapminder_gd010_gapdata010.xls`: Gapminder Documentation 010 companion Excel workbook, downloaded from `https://www.gapminder.org/documentation/documentation/gapdata010.xls`.
- `gapminder_gd010_gapdoc010.pdf`: Claudia Hanson, *Data on Maternal Mortality*, Gapminder Documentation 010, downloaded from `https://www.gapminder.org/documentation/documentation/gapdoc010.pdf`.

The workbook contains historical maternal mortality ratio observations for 14 countries. For the book's selected countries, it covers Sweden, United States, and Malaysia, but not Ethiopia.

## OWID Evidence and Successor Files

- `owid_maternal_mortality_2018_archived_export.svg`: archived OWID export from the 2018 Internet Archive capture of the OWID maternal mortality article. It documents the source family as "Gapminder (2010) and World Bank (2015)".
- `owid_maternal_mortality_ratio_current_2026_07_09.csv` and `.metadata.json`: current OWID grapher successor data downloaded on 2026-07-09.
- `owid_maternal_mortality_ratio_current.csv`, `datapackage.json`: prior Track A local OWID mirror files retained for continuity.

## Use in Reconstruction

`scripts/reconstruct_5_3.py` uses recovered Gapminder values wherever available and labels all current OWID fill rows with `source_component` in the clean CSV. The exact book-era OWID/World Bank 2015 machine-readable dataset was not recovered in this run.
