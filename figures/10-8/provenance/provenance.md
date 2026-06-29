# Provenance Summary: Figure 10-8

## Figure

- Title: CO2 emissions, 1960-2015
- Status: `verified_reproduction`
- Source fidelity: A/B

## Kindle Evidence

- Original figure inspected in Kindle on 2026-06-29.
- Source note: Our World in Data, Ritchie & Roser 2017, the OWID annual CO2 emissions by region grapher, CDIAC, and Le Quere et al. 2016; international air and sea corresponds to bunker fuels, and Other corresponds to statistical difference.
- Surrounding discussion: Surrounding chapter text argues that global emissions plateaued around 2014-2015, with changes in China, the EU, and the United States.

## Accepted Book-Period Source

- OWID datasets: CO2 per year by region - CDIAC (2017)
- Source URL: https://github.com/owid/owid-datasets/tree/master/datasets/CO2%20per%20year%20by%20region%20-%20CDIAC%20(2017)

## Successor Source

- OWID grapher annual-co-emissions-by-region, current Global Carbon Budget successor data through 2024.
- Data URL: https://ourworldindata.org/grapher/annual-co-emissions-by-region.csv

## Transformations

- Cleaned source CSV into figure-specific analysis-ready data under `data/clean/`.
- Generated book-period reconstruction from the book-era source.
- Generated extension using current OWID successor data only after the book-period endpoint.
- Generated side-by-side review images from Kindle reference crops and recreated plots.

## Remaining Issues

- Layer labels and font styling are approximate.
- Post-2015 extension uses current GCB/OWID successor categories, including EU-27 instead of EU-28 and no directly comparable statistical-difference layer.
