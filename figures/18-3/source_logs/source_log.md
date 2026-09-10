# Figure 18-3 source discovery log

## Figure

- Figure: 18-3
- Title: Suicide, England, Switzerland, and US, 1860-2014
- Original source note: England (including Wales): Thomas & Gunnell 2010, fig. 1, average of male and female rates, provided by Kylie Thomas. The series has not been extended because the data are not commensurable with current records. Switzerland, 1880-1959: Ajdacic-Gross et al. 2006, fig. 1. Switzerland, 1960-2013: WHO Mortality Database, OECD 2015b. United States, 1900-1998: Centers for Disease Control, Carter et al. 2000, table Abg50. United States, 1999-2014: Centers for Disease Control 2015.

## Search queries attempted

1. `Thomas Gunnell 2010 figure 1 suicide England Wales data 1860 2009`
2. `Ajdacic-Gross 2006 figure 1 Switzerland suicide 1880 1959 data`
3. `Carter 2000 table Abg50 suicide United States 1900 1998`
4. `Suicide in England and Wales 1861 2007 supplementary data csv`
5. `10.1093/ije/dyq094 data supplement`
6. `Thomas Gunnell 1861 2007 suicide data xls`
7. `WHO Mortality Database Switzerland suicide 1960 2013 OECD 2015`
8. `CDC data brief 241 suicide 1999 2014 data table`

## Sources investigated

### Thomas and Gunnell (2010)

- PubMed: https://pubmed.ncbi.nlm.nih.gov/20519333/
- DOI: https://doi.org/10.1093/ije/dyq094
- Result: **Accepted as the authoritative England/Wales source.** The methods state that 1861-2007 mortality and population data came from ONS, with pre-1911 data transcribed from paper records; rates are age-standardized for ages 15+ and smoothed with centered three-year moving averages.
- Limitation: no public numeric table for the exact Figure 1 series was recovered; Pinker’s line is an author-provided average of male and female rates.

### University of Bristol / ONS research route

- URL: https://research-information.bris.ac.uk/en/publications/suicide-in-england-and-wales-1861-2007-a-time-trends-analysis/
- Result: **Accepted as an institutional citation route.**
- Limitation: the author-supplied figure data were not attached as a downloadable table.

### Ajdacic-Gross et al. (2006)

- PubMed: https://pubmed.ncbi.nlm.nih.gov/16283596/
- DOI: https://doi.org/10.1007/s00406-005-0627-1
- Result: **Accepted as the historical Swiss source.** It covers Swiss suicide mortality from 1881-2000 and describes official historical registration.
- Limitation: the article’s Figure 1 is not an acceptable numeric input source; no accompanying downloadable table was found.

### WHO Mortality Database and OECD

- WHO: https://www.who.int/data/data-collection-tools/who-mortality-database
- OECD data: https://data-explorer.oecd.org/
- Result: **Accepted as the later Swiss source family.**
- Limitation: current access/data vintages and coding changes require a documented extraction; they do not solve the historical 1880-1959 segment.

### CDC historical mortality tables

- URL: https://www.cdc.gov/nchs/nvss/mortality_historical_data.htm
- Result: **Accepted as the US 1900-1998 recovery route.** The CDC provides historical mortality tables and population/rate documentation.
- Limitation: a US-only recovery does not complete the three-country figure, and Carter et al. table Abg50 must be matched to the same rate definition.

### CDC 2015

- Data Brief 241: https://www.cdc.gov/nchs/products/databriefs/db241.htm
- Result: **Accepted as the US 1999-2014 source route.**
- Limitation: the successor table is a modern official series and must be checked for continuity against the Carter historical segment.

### Modern successor suicide series

- Candidate families: OWID/WHO grapher series and current national statistics.
- Result: **Rejected for exact reconstruction.** They use different age standardization, cause-of-death coding, boundaries, or time coverage and cannot silently replace the cited historical components.

## Download URLs and archive URLs

- Thomas/Gunnell DOI: https://doi.org/10.1093/ije/dyq094
- Ajdacic-Gross DOI: https://doi.org/10.1007/s00406-005-0627-1
- WHO mortality database: https://www.who.int/data/data-collection-tools/who-mortality-database
- CDC historical mortality: https://www.cdc.gov/nchs/nvss/mortality_historical_data.htm
- CDC 2015 Data Brief 241: https://www.cdc.gov/nchs/products/databriefs/db241.htm
- OECD data explorer: https://data-explorer.oecd.org/

## Remaining uncertainties

- Exact author-provided England/Wales average-rate data and the centering convention for the three-year moving averages.
- Age standard population and sex averaging details at the boundaries of the England/Wales series.
- Numeric Swiss values and the precise break between Ajdacic-Gross and WHO/OECD data.
- US table Abg50 definition versus CDC 2015 definition and coding continuity.
- Whether Pinker’s displayed England endpoint is 2007, 2010, or an author-updated series ending before 2014.

## Recommended next steps

1. Request the England/Wales series from Kylie Thomas or obtain the ONS historical table under a reproducible license.
2. Recover the Swiss historical table from the authors or Swiss statistical archive.
3. Download and document CDC/WHO data vintages and harmonize only where definitions match.
4. Generate a three-panel source diagnostic before the combined reconstruction and inspect it against the reference.
