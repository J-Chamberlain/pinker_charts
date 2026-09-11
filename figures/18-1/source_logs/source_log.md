# Current Audit: September 11, 2026

Status: **partial_match**, blocked and publication-incomplete.
The [current recovery, provenance, visual review and checklist](../remediation_2026_09_11.md)
supersede the historical assessment below. New numeric recovery does not imply
full analytic verification or publication acceptance.

---

## Historical Assessment (Superseded)

# Figure 18-1 source discovery log

## Figure

- Figure: 18-1
- Title: Life satisfaction and income, 2006
- Original source note: Stevenson & Wolfers 2008a, fig. 11, based on data from the Gallup World Poll 2006. Credit: Betsey Stevenson and Justin Wolfers.

## Search queries attempted

1. `Stevenson Wolfers 2008a figure 11 Gallup World Poll replication data`
2. `site:nber.org/w14282 data replication Stevenson Wolfers Economic Growth Happiness`
3. `Economic Growth and Happiness Reassessing the Easterlin Paradox replication data`
4. `Stevenson Wolfers Gallup World Poll 2006 dataset life satisfaction GDP country data`
5. `Betsey Stevenson Justin Wolfers EasterlinParadox.zip`
6. `Gallup World Poll 2006 country aggregates life satisfaction ordered probit index`

## Sources investigated

### Authors’ replication archive

- URL: https://users.nber.org/~jwolfers/data/EasterlinParadox.zip
- Result: **Accepted as the exact replication package and source-chain evidence.** The archive contains the authors’ Stata driver, GDP inputs/scripts, Gallup processing documentation, and figure files.
- Limitation: the Gallup respondent data are not included. The archive’s own `readme-Gallup.txt` says they cannot be shared because they belong to Gallup.
- Local evidence: `data/raw/replication_archive/archive_manifest.txt`, `StevensonWolfers_Brookings.do`, `Complete_GDP.do`, `Gallup_processing_documentation.pdf`, and `readme-Gallup.txt`.

### Authors’ research page

- URL: https://betseystevenson.com/papers/
- Result: **Accepted as the authoritative link to the replication archive.** The 2008 Brookings paper entry links to the NBER archive.

### NBER working paper and paper PDF

- URL: https://www.nber.org/papers/w14282
- PDF: https://users.nber.org/~jwolfers/papers/EasterlinParadox.pdf
- Result: **Accepted for citation and figure-definition validation.** The PDF identifies the matching Gallup figure, 131-country sample, variables, regression, and source note. Pinker’s citation to Figure 11 matches the published-paper figure.
- Limitation: the paper is not a substitute for the underlying numeric data; plotted points were not transcribed.

### Gallup microdata repositories

- Washington University record: https://data.library.wustl.edu/record/108216?ln=en
- University of Virginia access note: https://library.virginia.edu/data/datasources/licensed/gallup-microdata
- Result: **Accepted as evidence of a legitimate access route, not as a downloaded source.** The World Poll microdata are access-controlled/licensed and are not redistributable in this project.

### World Database of Happiness

- URL: https://worlddatabaseofhappiness.eur.nl/correlational-findings/23265/
- Result: **Accepted as corroboration of the study and variable relationship.** It identifies the 2006 Gallup study and GDP-per-capita log relationship.
- Rejected for reconstruction: it is a finding catalogue, not the 131-row input table used by the figure.

### Public successor wellbeing datasets

- Candidate families considered: World Happiness Report, World Values Survey, and Our World in Data life-satisfaction series.
- Result: **Rejected for exact reconstruction.** They differ in survey instrument, sample, coverage, index construction, or GDP vintage. They may be useful only for a separately labeled updated-equivalent figure after the book-period reconstruction exists.

## Download URLs and archive URLs

- Exact replication archive: https://users.nber.org/~jwolfers/data/EasterlinParadox.zip
- Paper PDF: https://users.nber.org/~jwolfers/papers/EasterlinParadox.pdf
- Authors’ page: https://betseystevenson.com/papers/
- NBER working paper record: https://www.nber.org/papers/w14282
- Licensed access evidence: https://library.virginia.edu/data/datasources/licensed/gallup-microdata

## Remaining uncertainties

- Whether Gallup or the authors released an exact 131-country aggregate table separately from the restricted respondent file.
- The precise release/version of the Penn World Table and supplementary GDP inputs used in the archived build.
- The exact missing-income-country treatment and any respondent weighting steps in the Gallup preparation.
- Whether a current Gallup license permits export of the country aggregates needed for publication.

## Recommended next steps

1. Request the authors’ country-level aggregate extract or obtain licensed Gallup access.
2. Re-run the archived Stata workflow with the exact release identifiers recorded.
3. Export only the permitted aggregate fields needed for this figure and store a checksum plus license note.
4. Generate the plot and compare it against the stored original reference before considering a successor extension.
