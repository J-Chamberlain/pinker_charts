# Figure 15-2 provenance

## Original book source line

Google Trends (www.google.com/trends), searches for the three terms cited in the figure, United States, 2004-2017, relative to total search volume. Data accessed Jan. 22, 2017 are by month, expressed as a percentage of the peak month for each search term, then averaged over the months of each year, and smoothed.

## Recovered source

- Google Trends: https://trends.google.com/trends/explore
- Query metadata and URLs: `figures/15-2/data/raw/google_trends_query_metadata.json`
- Raw current export: `figures/15-2/data/raw/google_trends_monthly_2026-09-09.csv`

Each term was queried separately for the United States from January 2004 through August 2026 so Google could scale each term to its own 0-100 peak. The saved response is a current export and is not an exact archival copy of the book's 2017 response.

## Transformations

Monthly 0-100 values were averaged by calendar year. A centered three-year rolling mean approximates the book's unspecified smoothing. Book-period rows are 2004-2017; 2018 onward is plotted as a dashed successor. No values were transcribed from the Pinker image.
