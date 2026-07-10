# Anomaly Review: Figure 5-4

Review date: 2026-07-09

Status: `needs_targeted_source_recovery`

## Evidence Recovered

- Supplemental PDF page 4 figure image, source note, and surrounding discussion.
- Local OWID/Roser-era at-birth data file.
- Local OWID/HMD partial age-specific file with at-birth, age-15, and age-45 series.
- Current HMD public catalog page for England & Wales total population (`GBRTENW`).
- HMD public background documentation and country-code table.
- Current OWID successor chart data and metadata for `life-expectancy-at-different-ages`.

## Evidence Not Recovered

- Exact OWID/Roser 2016n book-era export containing the printed age set.
- Direct HMD `GBRTENW` both-sex period life-table raw file values for ages 1, 5, 10, 20, 30, 40, 50, 60, and 70.
- Archived 2015-2018 OWID grapher CSV for the printed figure.

## Why The Current Artifact Is Still Partial

The printed figure is a ten-line chart. The recovered local age-specific OWID/HMD file contains only at-birth, age-15, and age-45 series for the United Kingdom / England & Wales. The current OWID successor was not used as an extension because it omits several printed ages and uses a different post-1950 source construction.

## Reviewer Challenge

- Steven Pinker would likely ask whether the figure uses the same age-specific HMD values shown in the book. It does not; those values remain unrecovered.
- A data journalist would ask for archived raw HMD or OWID CSV URLs. The HMD catalog URLs are documented, but raw data access redirects to login; no archived CSV was recovered.
- A peer reviewer would ask whether missing age lines were interpolated. They were not; missing ages are left out.
- A skeptical reader would immediately notice the current artifact has three lines rather than ten. The caption and plot footer now state that explicitly.

## Editorial Decision

Do not promote. Keep as `needs_targeted_source_recovery` until either the exact OWID/Roser 2016n export or an authenticated/archived HMD period life-table file is recovered and the ten printed series can be rebuilt.
