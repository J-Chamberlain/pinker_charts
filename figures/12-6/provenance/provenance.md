# Figure 12-6 provenance

## Original book source

National Safety Council 2016. The caption states that fire, drowning, and poison solid/liquid are joined across the 1903-1998 and 1999-2014 datasets, that post-1992 falls are excluded because of reporting artifacts, and that 1999-2014 poisoning includes gas or vapor.

## Recovered data

- Current NSC historical trends page: https://injuryfacts.nsc.org/all-injuries/historical-preventable-fatality-trends/deaths-by-cause/
- Public workbook downloaded from the page: https://docs.google.com/spreadsheets/d/e/2PACX-1vTb9UjML1Yir8rH9mAenZMkOzjWF1RVcaUQHMgbF1p8DnbR_XCoj7yarNpAiV-C7dWOtacstCqg9v5Y/pub?output=xlsx
- Raw file: `figures/12-6/data/raw/nsc_injury_facts_historical_rates_2026-09-09.xlsx`

## Transformations

The workbook's two rate sheets were read with pandas. The second 1948 ICD-revision row was retained. Historical columns were reshaped to long form, falls were cut at 1992, and the 1999-2024 sheet was mapped from `Poisoning` to the book's solid/liquid label. Book-period data end in 2014; 2015-2024 current NSC rows are plotted as a dashed successor. No values were transcribed from the Pinker chart.

The current workbook is a same-institution successor, not a cryptographically verified copy of the NSC 2016 edition; therefore the status is `updated_equivalent`, despite the strong visual and category match.
