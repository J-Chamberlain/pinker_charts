# Figure 17-7 source discovery

Figure: Cost of air travel, US, 1979-2015. Original citation and variables: ../provenance/provenance.md. Research date: 2026-09-09.

## Sources and decisions

- Thompson 2013 Atlantic article (URL in provenance): accepted as bibliography resolution and A4A source chain, not numeric data.
- Current A4A page: accepted source identity. Saved data/raw/a4a_domestic_fares_page_2026_09_09.html; April 16, 2026 release. Base fare, baggage and change fees are distinct; government taxes excluded.
- Wayback exact 2016 queries returned no rows. Broader CDX found 2017, 2018 and later captures. Full results retained in data/candidates; no inference that the original data never existed.
- [April 2017 archive](https://web.archive.org/web/20170401223135id_/http://airlines.org:80/dataset/annual-round-trip-fares-and-fees-domestic/): accepted historical page, embeds AnnualDomesticRTAirfares/Dashboard1. CSV export returned 404. No numeric values extracted.
- [January 2023 archive](https://web.archive.org/web/20230130141950id_/https://www.airlines.org/dataset/annual-round-trip-fares-and-fees-domestic/): accepted later institutional page; AverageDomesticAirfareTimeSeries/Dashboard_DomesticTimeSeries export returned 404.
- Current Tableau workbook AverageDomesticAirfareTimeSeries_16855689739630: CSV and workbook probes returned 404. Browser opened the public workbook and dismissed its announcement; the visualization stayed blank and clicking Download did not yield an export dialog. This is an access/delivery failure in this environment, not proof of data unavailability. No login or paywall bypass attempted.
- [BTS passenger revenue per mile](https://www.bts.gov/content/average-passenger-revenue-passenger-mile): plausible successor, not accepted input. Source explicitly warns that revised estimates are not comparable to pre-2021 table versions; fee coverage requires review. Linked table_03_20_092625.xlsx returned 403 via both official hostnames. Browser download remains a reasonable next step.
- MIT Airline Data Project domestic passenger yield (1995 onward), NBER DB1A/DB1B microdata (1979 onward): targeted leads, not downloaded or accepted. Underlying fare/distance weighting and taxes require verification before substitution.
- AEI Mark Perry article linked by Thompson: old link failed; secondary quoted numbers were not used.

## Next steps

1. Obtain a working numeric A4A export, ideally a 2016 saved workbook. Compare source's cost-per-mile definition, distances, weighting, CPI and fees with the book.
2. Try the BTS official spreadsheet in an ordinary browser and inspect revision documentation; keep successor separate from book-era data.
3. If needed, recover archived A4A workbook assets or request the historical table from A4A; DB1B microdata aggregation is a specialized fallback, not a quick equivalent.
4. Plot only legitimate retained observations; do not digitize the published line or fit a multiplier to make a proxy resemble it.

Every HTTP attempt and download URL is recorded in downloads.json. Retained raw HTML and CDX files contain no chart-derived observations. Search is substantial but not exhaustive; status is needs_targeted_source_recovery, not source_unavailable.
