# Editorial Remediation Review: Figure 7-3

Status decision: `partial_match` (medium).

This run recovered an archived FAO Food Security Indicators workbook with the named regional series. The current reconstruction no longer uses broad Africa/Asia/World substitutions and no longer omits 1991-1999 regional segments.

The remaining caveat is source vintage: the complete regional file used for the 1991-2015 reconstruction is the March 17, 2016 archived FAO workbook, sheet `V_2.6`. The book's source note cites Roser 2016j based on FAO 2014; the recovered November 2014 FAO workbook is citable provenance but ends at the 2012-14 window.

## Series Audit

| Series | Original | Recreated | Match |
| --- | --- | --- | --- |
| Developing world | Present, 1970-2015 main black line. | 1970/1980 from OWID long-run FAO chart; 1991-2015 from archived FAO workbook `V_2.6`. | Good source-family match; chart styling differs. |
| Sub-Saharan Africa | Present, early-1990s-2015 regional line. | Archived FAO workbook `Sub-Saharan Africa`, 1991-2015. | Good source-family match; vintage caveat remains. |
| Southeast Asia | Present, early-1990s-2015 regional line. | Archived FAO workbook `South-Eastern Asia`, 1991-2015. | Good source-family match; source label capitalization differs. |
| South Asia | Present, early-1990s-2015 regional line. | Archived FAO workbook `Southern Asia`, 1991-2015. | Good source-family match; book label is shortened. |
| East Asia | Present, early-1990s-2015 regional line. | Archived FAO workbook `Eastern Asia`, 1991-2015. | Good source-family match; book label is shortened. |
| Latin America | Present, early-1990s-2015 regional line. | Archived FAO workbook `Latin America`, 1991-2015. | Good source-family match; values below 5 are plotted at FAO threshold. |
| World | Absent from original. | Removed from book-period recreation; retained only as a documented successor diagnostic if needed. | Prior substitution corrected. |

## Reviewer Challenge

- **What would Steven Pinker question?** Whether each book regional curve is present and named correctly. Resolved: all named regional curves are present from 1991-2015.
- **What would a skeptical data journalist question?** Whether a later archived workbook is being silently substituted for the cited FAO 2014 vintage. Documented: yes, the full endpoint uses a March 2016 archived workbook; this is why status remains `partial_match`.
- **What would another researcher question?** Whether current FAO post-2015 data can be appended. Decision: no extension is plotted because OWID documents a methodology change and discontinuation of the long-term 1970s series.

## Scorecard

| Criterion | Score (1-5) | Justification |
| --- | ---: | --- |
| Source recovery | 4 | Archived FAO workbook recovers all named regional curves and early-1990s coverage; exact Roser 2016j/FAO 2014 endpoint file remains unresolved. |
| Citation chain | 4 | Supplemental PDF, archived FAO page, archived FAO workbook, and OWID long-run metadata are documented. |
| Visual similarity | 4 | Axes, scale, series inventory, and year range now match closely; production styling and some label placement differ. |
| Extension quality | 5 | No post-2015 extension is plotted because comparability is not proven. |
| Caption quality | 4 | Caption states archived workbook use and remaining vintage caveat. |
| Editorial quality | 4 | Status is not over-promoted and discrepancies are explicit. |
| Overall confidence | 4 | Strong partial source-family reconstruction, still below verified reproduction. |
