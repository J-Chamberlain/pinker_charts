# Provenance: Figure 5-4

Figure: Life expectancy, UK, 1701-2013

Source note from Supplemental Graphics PDF page 4:

> Our World in Data, Roser 2016n. Data before 1845 are for England and Wales and come from OECD Clio Infra, van Zanden et al. 2014. Data from 1845 on are for mid-decade years only, and come from the Human Mortality Database.

## Recovery Trail

1. Rendered `references/enlightenment_now_supplemental_graphics.pdf` page 4 and cropped the full Figure 5-4 image, title, and source note to `plots/comparisons/supplemental_pdf_reference_figure_5_4.png`.
2. Confirmed the visible printed chart requires ten total-life-expectancy series: at birth and for ages 1, 5, 10, 20, 30, 40, 50, 60, and 70.
3. Reused the local OWID/Roser-era files already present in `data/raw/`:
   - `owid_life_expectancy_riley_clio_un_2019.csv`
   - `owid_hmd_age_specific_life_expectancy_partial.csv`
4. Recovered HMD public catalog evidence for England & Wales total population:
   - `hmd_gbrtenw_country_page.html`
   - `hmd_gbrtenw_background_documentation.pdf`
   - `hmd_country_codes.csv`
5. Probed the direct HMD both-sex period life-table raw file path:
   - `https://www.mortality.org/File/GetDocument/hmd.v6/GBRTENW/STATS/bltper_1x1.txt`
   - Result: redirects to `https://www.mortality.org/Account/Login` and returns login HTML, not raw data.
6. Downloaded current OWID successor files for `life-expectancy-at-different-ages`:
   - `owid_current_life_expectancy_at_different_ages.csv`
   - `owid_current_life_expectancy_at_different_ages.metadata.json`
   - `owid_current_life_expectancy_at_different_ages.config.json`

## Current Reconstruction Status

The exact OWID/Roser 2016n book-era age-specific dataset was not recovered. The current artifact is a partial source-recovery visualization only. It combines:

- at-birth life expectancy before 1845 from the local OWID/Clio/Riley/UN file,
- at-birth, age-15, and age-45 mid-decade style series from the local OWID/HMD partial file.

This does not satisfy the printed chart's ten-series data requirement. No successor extension is plotted because the current OWID successor omits several printed ages and is methodologically discontinuous after 1950.
