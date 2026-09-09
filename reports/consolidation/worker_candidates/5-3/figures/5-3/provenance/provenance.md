# Provenance: Figure 5-3

Book figure -> Supplemental Graphics PDF page 3 crop -> Roser 2016p (*Maternal Mortality*, Our World in Data) -> Gapminder GD010 source files -> `scripts/reconstruct_5_3.py` -> generated plots.

## Book Evidence

- Title: "Maternal mortality, 1751-2013".
- Source note: "Our World in Data, Roser 2016p, based partly on data from Claudia Hanson of Gapminder, https://www.gapminder.org/data/documentation/gd010/."
- Surrounding text says the chart shows maternal mortality since 1751 in four representative countries and notes a decline from about 1.2 percent to 0.004 percent in Europe.
- Visible figure axes: 1750-2010 tick range, 0-1.5 percent y-axis, countries Sweden, United States, Malaysia, and Ethiopia.

## Source Recovery

- Recovered original cited Gapminder source component:
  - `figures/5-3/data/raw/gapminder_gd010_gapdata010.xls`
  - `figures/5-3/data/raw/gapminder_gd010_gapdoc010.pdf`
- Gapminder documentation identifies Claudia Hanson, "Data on Maternal Mortality", Gapminder Documentation 010, uploaded 2010-07-01, and says the companion Excel file contains observations and detailed metadata.
- The recovered workbook contains Sweden (1751-2007), United States (1900-2003), and Malaysia (1933-1997), matching three of the four long-run book lines after converting maternal mortality ratio per 100,000 live births to percent by dividing by 1000.

## Unrecovered Source Vintage

The exact book-era OWID machine-readable dataset behind Roser 2016p was not recovered. Internet Archive checks found the 2018 OWID article page and an archived SVG export, but not a 2016/2017 archived `maternal-mortality.csv`. The archived OWID export cites "Gapminder (2010) and World Bank (2015)", while the recovered Gapminder workbook does not include Ethiopia. Therefore Ethiopia and the post-Gapminder tails are plotted from current OWID successor/equivalent data and labeled in the clean data as not verified book-era Roser 2016p/World Bank 2015 values.

## Reconstruction Decision

The current reconstruction is a source-improved `partial_match`, not a verified reproduction. It uses recovered Gapminder observations wherever available for Sweden, United States, and Malaysia; it uses current OWID successor/equivalent values for Ethiopia and short post-Gapminder tails only where the book-era OWID/World Bank supplement remains unrecovered. No extension beyond the book period is asserted because no same-vintage, methodologically identical successor segment was verified in this run.
