# Provenance: Figure 5-3

## Book evidence

The indexed *Enlightenment Now: Supplemental Graphics* record identifies the
figure as **Maternal mortality, 1751-2013**, with four series (Malaysia,
Sweden, United States, and Ethiopia), an x-axis from 1750 through 2020, and a
y-axis from 0 to 1.5 labeled "Percentage of mothers dying in childbirth."
The source line is:

> Our World in Data, Roser 2016p, based partly on data from Claudia Hanson of Gapminder, https://www.gapminder.org/data/documentation/gd010/.

The surrounding chapter text says the chart shows the trajectory since 1751 in
four countries representative of their regions, after noting that until
recently roughly one percent of mothers died in childbirth.

The indexed supplemental record is at
https://www.collegesidekick.com/study-docs/4585898. Direct retrieval was
blocked by Cloudflare in this run. A 2019 Steven Pinker ECOSOC lecture PDF also
indexes the same title and the shorter source line "Our World in Data, based
partly on Gapminder" on slide 32. Because original supplemental pixels were not
recoverable, the comparison uses a conspicuously labeled facsimile based on the
indexed layout; it is not represented as a page capture.

## Bibliography resolution

`Roser 2016p` resolves to Max Roser's Our World in Data maternal-mortality
publication/data page. The current page credits Max Roser and Hannah Ritchie,
states that it was first published in November 2013, and cites the historical
Gapminder source. The underlying historical publication is Claudia Hanson,
*Data on Maternal Mortality: Historical information compiled for 14 countries
(up to 200 years)*, Gapminder Documentation 010, version 1, 2010.

## Recovered dataset

Accepted raw source:
`data/raw/owid_522_maternal_mortality.tab`.

This preserved OWID table is published on Wikimedia Commons as
"Maternal Mortality Ratio - Gapminder (2010) and World Bank (2015) (OWID
522)." Its embedded metadata says:

- historical data through 1979 are Gapminder;
- recent data from 1990 through 2015 are World Bank;
- the World Bank source is WHO, UNICEF, UNFPA, World Bank Group, and UN
  Population Division, *Trends in Maternal Mortality: 1990 to 2015*;
- the two datasets were combined without adjustment; and
- OWID retrieved the data on 2017-06-04.

That source composition, date, countries, plotted axis range, and values match
the book-era Roser/Gapminder chain. Although the title and x-axis begin in
1751/1750, the earliest observation in recovered OWID 522 is Sweden in 1800;
no 1751-1799 values are invented or imported from the revised current series.
The separate Gapminder workbook
`data/raw/gapminder_gd010_2010.xlsx` was recovered from the public Google
Spreadsheet linked by the live GD010 documentation page. It provides an
independent copy of the historical source family.

## Transformation and fidelity

The source variable is the maternal mortality ratio: maternal deaths per
100,000 live births. The book displays a percentage. The sole numeric
transformation is therefore:

`maternal_mortality_percent = mmr_per_100000 / 1,000`

This is exact apart from six-decimal CSV serialization. Validation reloads the
clean CSV and requires an absolute difference no greater than `5e-7` percentage
points from the source-derived value. No values are interpolated, smoothed,
digitized, or invented. All 398 rows for the four countries through 2013 pass.

## Extension decision

The preserved dataset contains 2014 and 2015 values from the same World Bank
2015 source. Those eight values are shown only in the dashed same-source
continuation artifact. The current OWID series through 2020 is archived as
source evidence but is not appended: its metadata documents a new combination
of UN MMEIG 2023, WHO Mortality Database 2025, UN WPP 2024, and Gapminder 2010
with major OWID processing. That is not a like-for-like continuation of OWID
522.
