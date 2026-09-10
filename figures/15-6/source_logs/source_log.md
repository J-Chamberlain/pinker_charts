# Figure 15-6 source discovery log

## Figure

- Figure: 15-6
- Title: Liberal values across time and generations, developed countries, 1980-2005
- Original source note: Welzel 2013, fig. 4.1. World Values Survey data are from Australia, Canada, France, West Germany, Italy, Japan, the Netherlands, Norway, Sweden, the United Kingdom, and the United States, each country weighted equally.

## Search queries attempted

1. `Welzel 2013 fig 4.1 liberal values across time generations data World Values Survey`
2. `Christian Welzel Freedom Rising figure 4.1 data csv`
3. `World Values Survey 2005 emancipative values index birth cohorts data`
4. `Table4.1.sav Welzel`
5. `Freedom Rising Table4.1.sav`
6. `Figure4.1.sav Welzel`
7. `World Values Survey 1981 2014 official aggregate csv download`
8. `RESEMAVAL csv WVS`
9. `emancipative values index dataset csv Welzel`

## Sources investigated

### World Values Survey index documentation

- URL: https://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=welzelidx
- Result: Accepted as the authoritative index-construction documentation. It defines the four components and the item recodes for emancipative values.
- Limitation: It is documentation, not the target cohort-level data file.

### WVS/EVS integrated time-series documentation

- URL: https://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=intinfo
- Result: Accepted as the authoritative description of the integrated WVS/EVS data family, including survey coverage and distributor information.
- Limitation: The direct licensed data download was not completed in this run.

### WVS current wave and time-series archive

- URL: https://www.worldvaluessurvey.org/AJDocumentationSmpl.jsp?CndWAVE=-1&INID=&SAID=-1
- Result: Investigated. Current and historical time-series files are listed, including older 1981-2016 files.
- Rejected for immediate reconstruction: download route requires a registration/conditions-of-use flow and the downloaded response was not a data archive.

### Public WVS mirror at Universite de Sherbrooke

- URL: https://dimension.usherbrooke.ca/donnees/
- Result: Investigated as a transformed access path for wave CSV files.
- Rejected for exact reconstruction: available wave files do not include the EVS European samples needed for the book's named developed-country set, and the figure needs cohort-level application of Welzel's index rather than simple country-wave averages.

### Welzel emancipative-values dataset, SoDaNet

- URL: https://datacatalogue.sodanet.gr/dataset.xhtml?persistentId=doi:10.17903/FK2/OBRI42
- Result: Accepted as evidence that Welzel's derived index dataset exists and that the algorithm is public.
- Limitation: the open resources are algorithm documentation and demo data, not the full historical cohort data needed here.

### Welzel replication file, GESIS ZA7470

- URL: https://search.gesis.org/research_data/ZA7470?doi=10.4232/1.12407
- Result: Accepted as the highest-priority recovery target because Leuphana identifies it as “World Values Studies key aggregates, waves 1-6 (Welzel replication file).”
- Limitation: direct download was blocked by the GESIS web access layer in this run; no file was saved or treated as recovered.

### Freedom Rising online appendix

- URL: https://www.cambridge.org/de/files/8613/8054/8416/FreedomRising_OA.pdf
- Result: Accepted as the cited methodological appendix and source for the index algorithm/replication-file names.
- Limitation: the local HTTP response was an access page rather than a valid PDF; the appendix was read through the publisher's indexed page.

## Remaining uncertainties

- Whether the chart's “1980” line uses the first WVS/EVS wave's survey-year midpoint or a fixed 1980 label.
- Whether “developed countries” is exactly the eleven countries listed in the source note or an equal-weight subset after missingness.
- Whether West Germany is kept separate from Germany in the underlying integrated file.
- Whether the cohort curves use respondent weights within country before equal country weighting.
- Which index-generation release and factor coefficients were used for the 2013 book.

## Recommended next steps

1. Obtain the licensed ZA7470 or WVS/EVS integrated data through the official archive.
2. Request Welzel's `Figure4.1` or cohort-level replication data if ZA7470 lacks the figure inputs.
3. Record the exact data version, survey-year mapping, country inclusion, and weighting sequence.
4. Only then generate a reconstruction and side-by-side comparison.
