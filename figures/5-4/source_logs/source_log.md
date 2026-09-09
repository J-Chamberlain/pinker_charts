# Consolidated Research History: Figure 5-4

These are historical search records, not the current acceptance decision.

## Local Work At efca1264944eabab2f733bc399027e22b8df6381

# Source Discovery Log: Figure 5-4

Figure title: Life expectancy, UK, 1701-2013

Original source note: Our World in Data, Roser 2016n. Data before 1845 are for England and Wales and come from OECD Clio Infra, van Zanden et al. 2014. Data from 1845 on are for mid-decade years only, and come from the Human Mortality Database.

## Supplemental PDF Evidence

- Rendered Supplemental Graphics PDF page 4 with Poppler.
- Cropped reference image: `figures/5-4/plots/comparisons/supplemental_pdf_reference_figure_5_4.png`.
- Surrounding text says the figure shows life expectancy in the United Kingdom at birth and at different ages from 1 to 70 over the past three centuries.
- The printed figure visibly contains ten lines: at birth and ages 1, 5, 10, 20, 30, 40, 50, 60, and 70.

## Bibliography / Source Resolution

- The per-figure source note resolves the pre-1845 source family to OECD Clio Infra / van Zanden et al. 2014.
- The post-1845 source family resolves to the Human Mortality Database, England & Wales total population (`GBRTENW` on the current HMD site).
- No separate `Roser 2016n` entry was found in the local bibliography database during this run; this remains a bibliographic cleanup task, not evidence that the source note is unknown.

## Sources Recovered

- Local OWID/Roser-era at-birth file: `data/raw/owid_life_expectancy_riley_clio_un_2019.csv`.
- Local OWID/HMD partial age-specific file: `data/raw/owid_hmd_age_specific_life_expectancy_partial.csv`.
- HMD public country page: `data/raw/hmd_gbrtenw_country_page.html`.
- HMD country code table: `data/raw/hmd_country_codes.csv`.
- HMD England & Wales background documentation: `data/raw/hmd_gbrtenw_background_documentation.pdf`.
- Current OWID successor chart data and metadata for `life-expectancy-at-different-ages`.

## Source Blockers

- Direct HMD raw data path `https://www.mortality.org/File/GetDocument/hmd.v6/GBRTENW/STATS/bltper_1x1.txt` redirects to `https://www.mortality.org/Account/Login` and returns login HTML. The endpoint is documented on the public country page, but the raw data were not anonymously recoverable in this run.
- The local OWID/HMD file exposes only at-birth, age-15, and age-45 series for United Kingdom / England & Wales, not the printed age set.
- The current public OWID successor exposes at-birth, age-10, age-25, age-45, age-65, and age-80, and uses UN WPP after 1950. It is not accepted as a comparable extension for the book figure.
- Wayback/CDX searches for the old OWID grapher slug `life-expectancy-at-different-ages` returned no usable 2015-2018 CSV capture in this run.

## Data Fidelity Statement

The refreshed artifact does not claim data fidelity to all printed values. It uses only recovered machine-readable values for the three available local series and explicitly leaves out unrecovered ages rather than inventing or interpolating them. The visual mismatch is therefore expected and documented.

## Recommended Next Steps

- Recover an authenticated or archived HMD `GBRTENW/STATS/bltper_1x1.txt` vintage close to 2016-2018, or an archived OWID/Roser 2016n export containing the exact printed age set.
- If HMD raw data are recovered, rebuild the book-period chart from total-population period life-table `ex` values at ages 1, 5, 10, 20, 30, 40, 50, 60, and 70 and compare against the Supplemental PDF crop before promotion.


## GitHub Recovery At 9a19519494ec20f45b3ac3e6b3122d38a2bc0892

# Source log

1. Checkout/PDF audit: no Supplemental Graphics PDF was present; only an unrelated
   Figure 10-6 report PDF was found. Web search located a searchable 39-page
   Supplemental Graphics record whose indexed first page stops at Figure 5-3, so the
   Figure 5-4 image could not be visually inspected.
2. Book text audit: recovered the exact title, source note, and surrounding explanatory
   paragraph from searchable book copies. These establish the source split and numeric
   anchor values.
3. Bibliography: resolved van Zanden et al. 2014 to OECD's *How Was Life?*; classified
   Roser 2016n wording as not fully resolved.
4. OWID archive: cloned full `owid/owid-datasets` history and searched filenames/logs.
   Recovered Clio birth data and later 2018 HMD datasets, but not the cited multi-age
   Roser 2016n assembly.
5. HMD: tested England-and-Wales period life-table endpoints (`bltper`, `fltper`, and
   `mltper`); all redirected to the HMD account login. No credentials were available.
6. Wayback: wildcard CDX search for OWID grapher age/life-expectancy CSVs returned no
   captures. Current OWID datasets found were methodologically different.
7. Closest public diagnostic: recovered the ONS 2015 England-and-Wales male decennial
   expected-age table. Rejected it as a substitute because the book series is not
   identified as male-only and uses mid-decade years.

Accepted: Clio component only. Rejected as reconstruction input: ONS male table and
OWID 2018 age-15/45 successor. Outstanding: reference image and exact HMD/OWID vintage.
