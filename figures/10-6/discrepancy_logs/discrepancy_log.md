# Discrepancy Log: Figure 10-6

Accessed: 2026-06-28

## Current Discrepancies

- Initial recreated plot used current World Bank API data and had only 2013-2014 points inside the book range.
- Archived 2017 WDI bulk ZIP recovered the book-like anchor years 1990, 2000, and 2014 for both terrestrial and marine protected areas.
- Remaining uncertainty: the archived WDI file exposes three anchor years rather than annual observations. This appears consistent with the book figure geometry, but the book source line does not explicitly say the plot interpolates between three points.

## Search Hypotheses Resolved

- World Bank 2016h/2017 likely refers to an archived WDI release, not the current API.
- The correct indicators are `ER.LND.PTLD.ZS` and `ER.MRN.PTMR.ZS`; values match the book text/caption scale.
