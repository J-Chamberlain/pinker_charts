# Figure 13-1 provenance

## Book source line

Global Terrorism Database, START 2016. World rate excludes Afghanistan after 2001, Iraq after 2003, Pakistan after 2004, Nigeria after 2009, Syria after 2011, and Libya after 2014. Population estimates are from the European Union's 2015 World Population Prospects revision for world/Western Europe and US Census Bureau 2017 for the United States.

## Recovered source

- START GTD download page: https://www.start.umd.edu/gtd-download
- Public GTD-derived OWID CSV: https://ourworldindata.org/grapher/terrorism-deaths.csv?v=1&csvType=full&useColumnShortNames=false
- Public OWID population CSV: https://ourworldindata.org/grapher/population.csv
- Raw files: `figures/13-1/data/raw/owid_terrorism_deaths.csv`, `figures/13-1/data/raw/owid_population.csv`

The export is event-derived and not the exact 2016 release. Western Europe is reconstructed by summing the listed OWID country rows; the world exclusions are applied before dividing by population. No values were digitized from the Pinker chart.
