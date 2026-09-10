# Figure 15-5 provenance

## Original book source line

Ottosson 2006, 2009. Dates for an additional sixteen countries were obtained from “LGBT Rights by Country or Territory,” Wikipedia, retrieved July 31, 2016. Dates for an additional thirty-six countries that currently allow homosexuality are not listed in either source. The arrow points to 2009, the last year plotted in fig. 7-23 of Pinker 2011.

## Recovered source chain

- Archived ILGA report: `figures/15-5/data/raw/ilga_state_sponsored_homophobia_2009.pdf`.
- Public current historical series: `figures/15-5/data/raw/owid_same_sex_sexual_acts_legal_mignot.csv`.
- Current series metadata: `owid_same_sex_sexual_acts_legal_mignot.metadata.json`.
- Archived OWID legal-year snapshot: `wikimedia_owid_4910_snapshot.json`.
- Data URL: https://ourworldindata.org/grapher/same-sex-sexual-acts-legal-mignot.csv

## Transformations

For each country, the first year in which the series changes from `Illegal` to `Legal` is retained. Counts of those transition years are cumulatively summed by year. The 1791-2016 interval is the book-period comparison; 2017 onward is plotted as a dashed current-source continuation. No values were digitized from the Pinker chart.
