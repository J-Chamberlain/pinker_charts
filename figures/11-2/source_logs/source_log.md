# Figure 11-2 source discovery log

- Figure: 11-2
- Title: Battle deaths, 1946-2016
- Original citation: Human Security Report Project 2007; PRIO/UCDP; Census and McEvedy & Jones.

## Queries and investigations

- `Battle deaths 1946-2016 Pinker UCDP data`
- `Battle-related deaths 1946-1988 Lacina Gleditsch CSV`
- `Human Security Report Project 2007 battle deaths download`
- UCDP historical download center and version-history pages.
- PRIO Battle Deaths dataset and its versioned secondary downloads.
- Library of Congress Battle Deaths Dataset record and current OWID/UCDP pages.

## Sources investigated

1. PRIO Battle Deaths Dataset 3.1: https://cdn.cloud.prio.org/files/d21ef702-a546-45a8-b3c9-5b520dcc1239/PRIO%20Battle%20Deaths%20Dataset%2031.xls?inline=true. Accepted for the 1946-1988 numeric series; its `bdeadbes` field is the best estimate and is aggregated by year.
2. UCDP v5.0-2016 conflict CSV: https://ucdp.uu.se/downloads/brd/ucdp-brd-conf-50-2016.csv. Accepted for 1989-2015, exactly matching the book's source vintage family.
3. UCDP v26.1 current conflict ZIP: https://ucdp.uu.se/downloads/brd/ucdp-brd-conf-261-csv.zip. Accepted only as a dashed successor from 2016-2023.
4. OWID population series: https://ourworldindata.org/grapher/population.csv. Accepted as denominator substitute; rejected as proof of the cited Census vintage.
5. PRIO 2.0 yearly aggregate ZIP. Retained candidate for historical comparison, but not used because PRIO 3.1 is the later institutional release in the cited family and exposes the underlying conflict rows.
6. Human Security Report and McEvedy/Jones publications. Context confirmed, but a machine-readable exact population denominator was not recovered.

## Uncertainties and next steps

The denominator vintage and the exact HSRP transformation/adjustments remain unresolved. Compare the clean rates against a recovered Census IDB table or HSRP workbook before considering verification. Preserve PRIO/UCDP source seams; do not silently splice current UCDP into the historical source.