# Provenance

## Book evidence

Title: *Figure 5-4: Life expectancy, UK, 1701-2013*.

Exact source note recovered from the book text/searchable copy: "Sources: Our World
in Data, Roser 2016n. Data before 1845 are for England and Wales and come from OECD
Clio Infra, van Zanden et al. 2014. Data from 1845 on are for mid-decade years only,
and come from the Human Mortality Database, http://www.mortality.org/."

The surrounding paragraph says the figure shows life expectancy at birth and at
different attained ages from 1 to 70. It gives checks: age 1 reaches about 47 (1845),
57 (1905), 72 (1955), and 81 (2011); age 30 has 33, 36, 43, and 52 remaining years;
age 70 has 9, 10, and 16 remaining years in 1905, 1955, and 2011; age 80 has 5 and 9
remaining years in 1845 and 2011.

## Bibliography resolution

- `Roser 2016n`: Max Roser, *Life Expectancy*, Our World in Data (2016). Exact
  bibliography wording remains unconfirmed because the repository bibliography does
  not contain this key.
- van Zanden et al. (2014): Jan Luiten van Zanden et al., *How Was Life? Global
  Well-being since 1820*, OECD Publishing, 2014, DOI 10.1787/9789264214262-en.
- Human Mortality Database: University of California, Berkeley (USA), and Max Planck
  Institute for Demographic Research (Germany), available at mortality.org.

## Recovered files

- `data/raw/owid_clio_infra_life_expectancy_at_birth.csv`: OWID datasets repository,
  dataset "Life Expectancy at Birth (both genders) - Clio Infra," authored by Richard
  Zijdeman. Repository commit `0ac52a43cddef6661787f6cedbb5483b7079f9ed`
  (2018-09-21). This is a close public successor to the cited Clio component, not proof
  of the exact 2016 snapshot.
- `data/raw/ons_expected_age_to_reach_males.csv`: ONS, "How has life expectancy
  changed over time?", data download `expected_age_to_reach2.csv`, published
  2015-09-09. It reports expected age reached for England and Wales males by attained
  age and decennial life table. It is a diagnostic only because sex and year-selection
  differ from the book series.

Retrieved 2026-07-10. Checksums are in `checksums/sha256sums.txt`.

## Fidelity conclusion

No source-value tolerance is asserted for the book series because the exact OWID/HMD
table was not recovered. The clean CSV preserves source values without interpolation;
the Clio rows are cited-source-component values and all ONS rows are explicitly marked
`diagnostic_proxy_not_book_data`. No extension is supplied.
