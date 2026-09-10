# Figure 15-4 provenance

## Original book source line

US Bureau of Justice Statistics, National Crime Victimization Survey, Victimization Analysis Tool, http://www.bjs.gov/index.cfm?ty=nvat, with additional data provided by Jennifer Truman of BJS. The gray line represents intimate partner violence with female victims. The arrows point to 2005, the last year plotted in fig. 7-13, and 2008, the last year plotted in fig. 7-10, of Pinker 2011.

## Recovered source chain

- Official BJS report and machine-readable tables: `figures/15-4/data/raw/bjs_ipv_attributes_1993_2011.pdf`, `.txt`, `.zip`, and extracted CSV tables.
- Official BJS NCVS Select API: https://api.ojp.gov/bjsdataset/v1/gcuy-rt5g.csv?$limit=5000000
- Official BJS person population workbook: https://bjs.ojp.gov/document/personpop.xlsx
- Saved raw inputs: `bjs_ncvs_select_personal_victimization.csv` and `bjs_person_population.xlsx`.

## Transformations

For each year, female rape/sexual-assault victimizations are selected with `sex == 2` and `newoff == 1`; female intimate-partner violence is selected with `sex == 2`, `newcrime == 1`, and `direl == 1`. Weighted victimizations (`newwgt`) are divided by the official female population age 12 or older and multiplied by 100,000. No values were digitized from the Pinker chart. The BJS report's two-year rolling-average series is represented by the current API's published weighted estimates; the equality at the supplied reference landmarks supports the book-period match.
