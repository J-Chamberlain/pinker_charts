# Current Audit: September 11, 2026

Status: **partial_match**, blocked and publication-incomplete.
The [current recovery, provenance, visual review and checklist](../remediation_2026_09_11.md)
supersede the historical assessment below. New numeric recovery does not imply
full analytic verification or publication acceptance.

---

## Historical Assessment (Superseded)

# Figure 18-2 source discovery log

## Figure

- Figure: 18-2
- Title: Loneliness, US students, 1978-2011
- Original source note: Clark, Loxton, & Tobin 2015. College students (left axis): Revised UCLA Loneliness Scale, trend line across many samples, taken from their fig. 1. High school students (right axis): Mean rating of six loneliness items from the Monitoring the Future survey, triennial means, taken from their fig. 4. Each axis spans half a standard deviation, so the slopes of the college and high school curves are commensurable, but their relative heights are not.

## Search queries attempted

1. `Clark Loxton Tobin 2015 loneliness college students figure 1 Monitoring the Future figure 4`
2. `Declining loneliness over time evidence American colleges high schools data`
3. `10.1177/0146167214557007 supplementary data`
4. `site:monitoringthefuture.org loneliness 8th 10th 12th grade data 1991 2012`
5. `Monitoring the Future dataset loneliness items 1991 2012 ICPSR`
6. `six loneliness items Monitoring the Future Clark Loxton Tobin`
7. `ICPSR 34574 loneliness 2012 8th 10th grade`

## Sources investigated

### Clark, Loxton, and Tobin paper

- PubMed: https://pubmed.ncbi.nlm.nih.gov/25422313/
- Publisher page: https://journals.sagepub.com/doi/10.1177/0146167214557007
- Result: **Accepted as the authoritative source and citation resolution.** It confirms Study 1 (48 college samples, Revised UCLA scale, 1978-2009) and Study 2 (MTF high-school sample, 1991-2012).
- Limitation: the accessible article record does not provide the numeric series behind Figures 1 and 4.

### Publisher supplementary files

- URLs identified on the publisher page:
  - https://journals.sagepub.com/doi/suppl/10.1177/0146167214557007/suppl_file/10.1177_0146167214557007_online_appendix_2.pdf
  - https://journals.sagepub.com/doi/suppl/10.1177/0146167214557007/suppl_file/10.1177_0146167214557007_online_supplementary_material_1.pdf
- Result: **Accepted as a targeted recovery route.** The publisher lists both files, including a 184.99 KB supplementary PDF.
- Limitation: direct retrieval returned HTTP 403 in this run; no file was treated as recovered.

### Monitoring the Future official site

- URL: https://monitoringthefuture.org/data/data.html
- Result: **Accepted as the authoritative study and distribution route.** It states that public-use cross-sectional microdata are available through NAHDAP/ICPSR.

### ICPSR MTF public-use collection

- URL: https://www.icpsr.umich.edu/sites/icpsr/view/collections/35
- Result: **Accepted as the public data family.** The collection covers annual 12th-grade surveys from 1975 and 8th/10th-grade surveys from 1991, with public-use data and documentation.
- Limitation: a collection landing page is not yet the clean six-item triennial table used in Clark et al.

### ICPSR 2012 8th/10th-grade study

- URL: https://www.icpsr.umich.edu/web/NAHDAP/studies/34574
- Result: **Accepted as a year-specific recovery target.** It documents the public-use 2012 8th/10th-grade survey, four questionnaire forms, weights, and access terms.
- Limitation: the exact loneliness item names/forms and earlier-year harmonization still need to be resolved.

### ICPSR 2011 12th-grade study

- URL: https://www.icpsr.umich.edu/web/NAHDAP/studies/34409/variables
- Result: **Accepted as a year-specific recovery target** for the 12th-grade portion of the MTF series.
- Limitation: study variables are not the final Clark et al. six-item aggregate.

### MTF documentation and cross-time indexes

- URL: https://monitoringthefuture.org/results/publications/reference-volumes/
- Result: **Accepted as documentation route** for historical questionnaire wording and item continuity.

### Modern loneliness series and later studies

- Candidates included newer MTF analyses and general population loneliness surveys.
- Result: **Rejected for exact reconstruction.** They use different items, populations, periods, or transformations, and cannot replace the two Clark et al. source components.

## Download URLs and archive URLs

- Clark et al. DOI: https://doi.org/10.1177/0146167214557007
- MTF public-use collection: https://www.icpsr.umich.edu/sites/icpsr/view/collections/35
- MTF data tables: https://monitoringthefuture.org/data/data.html
- 2012 8th/10th-grade MTF study: https://doi.org/10.3886/ICPSR34574.v2
- 2011 12th-grade MTF study: https://doi.org/10.3886/ICPSR34409.v2

## Remaining uncertainties

- The exact six MTF loneliness item identifiers and response recoding used by Clark et al.
- Which grades/forms contribute to each triennial mean and how missing items are handled.
- Whether the college-study sample-level data are in the blocked supplementary PDF, an author-held file, or a separate repository.
- The exact normalization used to give each axis a half-standard-deviation span.
- Whether the book’s 2011 endpoint label reflects the paper’s 2012 source endpoint or an intermediate plotting convention.

## Recommended next steps

1. Acquire the supplementary PDFs through an institutional SAGE route or contact the authors for the Study 1/Study 2 data.
2. Recover the ICPSR files and codebooks for the relevant years and forms.
3. Write a source-backed harmonization script with explicit item, grade, weight, and triennial rules.
4. Only after both curves are recovered, generate and visually inspect the reconstruction.
