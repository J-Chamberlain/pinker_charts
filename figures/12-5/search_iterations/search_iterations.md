# Figure 12-5 Search Iterations

- Kindle first: captured title, source note, caption context, and chart page.
- Institutional/source-family search: followed the source family named by Kindle.
- Result: partial_match.


## Worker Recovery At 25c7c29c073b324709ed3d9669ae9d284266e7e2

# Figure 12-5 Search Iterations

- Supplemental PDF inspection: located figure on page 20 with surrounding text saying the passenger fatality risk fell from less than five in a million in 1970 to about one hundredth of that risk by 2015.
- Bibliography resolution: the figure's source line is the operative bibliographic evidence available in this repository: Aviation Safety Network 2017 and World Bank 2016b. No separate bibliography row for these keys exists in `data/bibliography/`.
- Live successor search: found OWID grapher `aviation-fatalities-per-million-passengers`, whose metadata names ASN annual fatalities and World Bank WDI passenger counts and documents the same formula.
- ASN source search: downloaded current ASN annual accidents/fatalities Google Sheet through the URL exposed in OWID indicator metadata.
- Archive search: checked Wayback CDX for `aviation-safety.net/statistics/` in 2017-2018 and saved the 2017-10-07 capture. The page confirms the ASN statistics section and `Last updated: 7 March 2017`, but does not expose a CSV or table equivalent to the current Google Sheet.
- Discrepancy analysis: prior baseline used ASN 2019 flight-phase casualties. The replacement source uses the annual airliner fatality series that OWID now uses for this exact derived indicator.
- Outcome: closest verifiable successor recovered; exact ASN 2017 extraction remains unrecovered, so status remains `partial_match`.
