# Track B Economic History Summary

Date: 2026-06-30

Branch: `track-b-economic-history`

## Figures

### Figure 7-3 - Undernourishment, 1970-2015

- Status: `partial_match`
- Source note: Our World in Data, Roser 2016j, based on data from the Food and Agriculture Organization 2014, also reported in FAOSTAT.
- Disposition: Main developing-world line is source-supported; regional lines use available FAO/SOFI successor coverage with shorter time span.
- Next action: Recover the exact Roser 2016j regional FAO 2014 vintage before promoting.

### Figure 7-4 - Famine deaths, 1860-2016

- Status: `partial_match`
- Source note: Our World in Data, Hasell & Roser 2017, based on data from Devereux 2000; O Grada 2009; White 2011; EM-DAT; and other sources.
- Disposition: The event table is recovered from OWID's famine dataset article; the decadal rate denominator uses current OWID world population interpolation.
- Next action: Recover archived 2017 OWID grapher/table and denominator notes for exact visual verification.

### Figure 8-1 - Gross World Product, 1-2015

- Status: `updated_equivalent`
- Source note: Our World in Data, Roser 2016c, based on data from the World Bank and from Angus Maddison and Maddison Project 2014.
- Disposition: Live OWID successor reproduces the same shape and source family but extends past 2015 and may include revisions.
- Next action: Recover the exact 2017 OWID CSV if archival precision is required.

### Figure 8-2 - GDP per capita, 1600-2015

- Status: `updated_equivalent`
- Source note: Our World in Data, Roser 2016c, based on data from the World Bank and from Maddison Project 2014.
- Disposition: Current Maddison 2020/OWID successor data match the broad visual pattern but not the exact book-era source vintage.
- Next action: Recover the exact Maddison Project 2014/World Bank 2016 vintage before promoting.

### Figure 8-5 - Extreme poverty (number), 1820-2015

- Status: `verified_reproduction`
- Source note: Our World in Data, Roser & Ortiz-Ospina 2017, based on data from Bourguignon & Morrison 2002 (1820-1992) and the World Bank 2016g (1981-2015).
- Disposition: Book-period source family and visual encoding are reproduced; no comparable post-2015 extension is plotted.
- Next action: Publication review; add extension only if a comparable successor world count is recovered.

## Editorial Review Summary

- Critical issues found: none after generating PDF-derived references, reconstructions, and comparison images for all five figures.
- Major issues found: source-vintage caveats remain for 7-3, 7-4, 8-1, and 8-2; these are explained in captions, discrepancy logs, and anomaly reviews.
- Minor issues found: Matplotlib styling, label placement, and PDF crop geometry differ from the printed figures.
- Issues automatically corrected: replaced missing Kindle-reference placeholders with rendered PDF reference crops; generated all side-by-side book-period and extended comparisons.
- Issues remaining: exact archival source vintage recovery for several figures, as documented per figure.
- Batch disposition: acceptable as a documented mixed-status batch, with 8-5 verified and the others classified as partial or updated equivalents rather than over-promoted.
