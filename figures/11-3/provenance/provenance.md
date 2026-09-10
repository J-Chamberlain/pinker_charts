# Provenance

## Book citation

PITF, 1955-2008: Political Instability Task Force State Failure Problem Set, 1955-2008, Marshall, Gurr, & Harff 2009; Center for Systemic Peace 2015; calculations described in Pinker 2011, p. 338. UCDP, 1989-2016: UCDP One-Sided Violence Dataset v. 2.5-2016 (the historical download center exposes the one-sided release as v1.4-2016), Melander, Pettersson, & Themnér 2016; Uppsala Conflict Data Program 2017.

## Downloaded sources

- PITF workbook: https://www.systemicpeace.org/inscr/PITF%20GenoPoliticide%202018.xls
- PITF codebook: https://www.systemicpeace.org/inscr/PITFProbSetCodebook2018.pdf
- Historical UCDP one-sided workbook: https://ucdp.uu.se/downloads/nsos/ucdp-onesided-171.xlsx
- Current UCDP one-sided CSV archive: https://ucdp.uu.se/downloads/nsos/ucdp-onesided-261-csv.zip
- Population denominator: https://ourworldindata.org/grapher/population.csv

## Transformations

PITF DEATHMAG categories use the codebook's bounded intervals. The script uses arithmetic midpoints for 0.5 through 4.5 and 256,000, the lower bound, for open-ended 5.0. Values are summed by year and divided by the World population series. UCDP uses the high fatality estimate, summed by year, with the same denominator.

The exact Census Bureau/McEvedy denominator and Pinker's case-specific death estimates were not recovered.
