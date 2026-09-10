# Figure 15-3 provenance

## Original book source line

Federal Bureau of Investigation 2016b. The arrow points to 2008, the last year plotted in fig. 7-4 of Pinker 2011.

## Recovered source chain

- FBI Hate Crime archive: https://ucr.fbi.gov/hate-crime
- Official annual reports: `figures/15-3/data/raw/fbi_hate_crime_1996.pdf` through `fbi_hate_crime_1999.pdf`; archived 2000 Section II table: `fbi_cius_2000_section_2.pdf`
- Official Table 1 workbooks: `figures/15-3/data/raw/fbi_hate_crime_table_1_2012.xls` through `fbi_hate_crime_table_1_2017.xls`
- Intervening 2000-2011 compilation: `figures/15-3/data/raw/adl_fbi_hate_crime_comparison_2000_2020.pdf`
- Parsed/transcribed incident rows: `figures/15-3/data/raw/fbi_incidents_transcribed_from_tables.csv`

The plotted measure is the `Incidents` column, not offenses or victims. The five series are harmonized to the book's labels: anti-black, anti-white, anti-Asian, anti-Jewish, and anti-Islamic. The source tables contain reporting-participation and category-definition changes; no values were taken from the Pinker plot. The ADL compilation initially supplied an inconsistent 2000 anti-black value (3,884); the archived FBI Section II table reports 2,904 incidents, which is the value used here.

## Transformations

Rows are filtered to the five series, split into book period 1996-2015 and successor period 2016-2017, and plotted without normalization. No population adjustment or interpolation is applied.
