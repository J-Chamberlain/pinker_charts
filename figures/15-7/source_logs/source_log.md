# Figure 15-7 source discovery log

## Figure

- Figure number: 15-7
- Title: Liberal values across time (extrapolated), world's culture zones, 1960-2006
- Original citation: World Values Survey, as analyzed in Welzel 2013, Figure 4.4,
  updated with data provided by Welzel.

## Search queries attempted

1. `Welzel Freedom Rising Figure 4.4 data emancipative values culture zones download`
2. `Christian Welzel Freedom Rising replication data Figure 4.4 download`
3. `"Liberal values across time" Welzel 4.4 data`
4. `site:worldvaluessurvey.org/welzel "Table4.2.sav"`
5. `"Table4.2.sav" Welzel`
6. `"Figure4.4.sav" Welzel`
7. `GESIS ZA7470 download data zip`
8. `"World Values Studies key aggregates, waves 1-6" download`

## Sources investigated

### Accepted as source documentation

- [World Values Survey publication page](https://www.worldvaluessurvey.org/AJPublications.jsp?CndPUTYPE=3&PUID=131)
  lists Welzel's *Freedom Rising* materials, including the online appendix and book
  presentation. It establishes the official WVS-hosted source family, but no direct
  Figure 4.4 data file was exposed by the page.
- [Welzel online appendix](https://www.cambridge.org/de/files/8613/8054/8416/FreedomRising_OA.pdf)
  documents the index, the estimates used in Figures 4.3-4.8, the backward-estimation
  assumptions, and `Table4.2.sav`. It is the authoritative methodological source, not
  the missing chart-specific export.
- [GESIS ZA7470 catalogue](https://search.gesis.org/research_data/ZA7470?doi=10.4232/1.12407)
  identifies Welzel's "World Values Studies key aggregates, waves 1-6" replication
  file. It is a legitimate archive lead, but it is an aggregate wave file and does not
  by itself establish the author-updated fixed-age extrapolation plotted here.
- [Leuphana dataset listing](https://fis.leuphana.de/en/publications/freedom-rising-human-empowerment-and-the-quest-for-emancipation/datasets/)
  confirms both the GESIS replication file and the emancipative-values index dataset.

### Rejected as insufficient for reconstruction

- [WVS index documentation](https://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=welzelidx)
  provides the EVI definition and item coding, but not the author-updated Figure 4.4
  series or its zone-level predictions.
- [GESIS variable description](https://access.gesis.org/dbk/57970)
  describes EVI and culture-zone variables. It does not provide the plotted fixed-age
  extrapolation or a verified download of the missing series.
- WVS wave CSV mirrors found through the University of Sherbrooke repository were
  rejected because they do not contain the integrated EVS/WVS coverage, Welzel's
  predicted period values, or the exact named zone aggregation. They are not committed.
- ResearchGate and secondary reproductions were rejected as evidence for numeric data;
  they either reproduce the visual chart or cite the source without supplying the
  underlying series.

## Download URLs and archive URLs

- Method appendix: `https://www.cambridge.org/de/files/8613/8054/8416/FreedomRising_OA.pdf`
- GESIS archive record: `https://search.gesis.org/research_data/ZA7470?doi=10.4232/1.12407`
- WVS index documentation: `https://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=welzelidx`
- Leuphana dataset landing page:
  `https://fis.leuphana.de/en/publications/freedom-rising-human-empowerment-and-the-quest-for-emancipation/datasets/`

## Remaining uncertainties

- The exact filename and location of the updated Figure 4.4 export are unresolved.
- It is not known whether Pinker received a private spreadsheet, a later Welzel
  revision, or a derived file from the Figure 4.4 replication materials.
- The reference describes fixed-age hypothetical samples and a country-specific period
  effect; the coefficients and complete country membership by year are unavailable.

## Recommended next steps

1. Request or recover the author-supplied Figure 4.4 data from the Welzel replication
   archive or author contact.
2. Inspect any recovered file for country, culture-zone, birth-cohort, test-year,
   fixed-age, and period-effect fields.
3. Recreate the zone means from the recovered country-level series and compare against
   the original crop before attempting an extension.
