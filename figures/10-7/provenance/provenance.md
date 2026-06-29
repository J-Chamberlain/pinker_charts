# Provenance Summary: Figure 10-7

## Figure

- Title: Carbon intensity (CO2 emissions per dollar of GDP), 1820-2014
- Status: `verified_reproduction`
- Source fidelity: A/B

## Kindle Evidence

- Original figure inspected in Kindle on 2026-06-29.
- Source note: Ritchie & Roser 2017, based on data from CDIAC; GDP in 2011 international dollars with pre-1990 GDP from Maddison Project 2014.
- Surrounding discussion: Surrounding chapter text discusses decarbonization, carbon intensity, and the claim that rich countries can reduce carbon emissions per dollar of GDP after industrialization.

## Accepted Book-Period Source

- OWID datasets: Carbon intensity (kgCO2/$) - Madisson, World Bank, CDIAC
- Source URL: https://github.com/owid/owid-datasets/tree/master/datasets/Carbon%20intensity%20(kgCO2!$)%20-%20Madisson,%20World%20Bank,%20CDIAC

## Successor Source

- OWID grapher co2-intensity, current successor data through 2022.
- Data URL: https://ourworldindata.org/grapher/co2-intensity.csv

## Transformations

- Cleaned source CSV into figure-specific analysis-ready data under `data/clean/`.
- Generated book-period reconstruction from the book-era source.
- Generated extension using current OWID successor data only after the book-period endpoint.
- Generated side-by-side review images from Kindle reference crops and recreated plots.

## Remaining Issues

- Minor typography and label-placement differences remain.
- Current OWID successor data revise historical values substantially, so only post-2014 dashed segments are used in the extension.
