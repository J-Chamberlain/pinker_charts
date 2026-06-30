# Editorial Remediation Review: Figure 7-3

Status decision: `partial_match` (medium-low).

Fresh review found that the prior reconstruction substituted broad Africa/Asia/World curves for several book regional curves. The remediation replaces those with current FAO successor regional entities where available, but the exact Roser 2016j/FAO 2014 regional vintage and 1991-1999 regional segments remain unrecovered.

## Series Audit

| Series | Original | Recreated | Match |
| --- | --- | --- | --- |
| Developing world | Present, 1970-2015 main black line. | Recovered from OWID/FAO developing-country dataset, 1970-2015. | Good source-family match. |
| Sub-Saharan Africa | Present, early-1990s-2015 regional line. | Current FAO successor entity `Sub-Saharan Africa (FAO)`, 2000-2015 book-period subset. | Partial; early years missing and vintage differs. |
| Southeast Asia | Present, early-1990s-2015 regional line. | Current FAO successor entity `South-eastern Asia (FAO)`, 2000-2015 book-period subset. | Partial; early years missing and naming/vintage differ. |
| South Asia | Present, early-1990s-2015 regional line. | Current FAO successor entity `Southern Asia (FAO)`, 2000-2015 book-period subset. | Partial; source-family curve only. |
| East Asia | Present, early-1990s-2015 regional line. | Current FAO successor entity `Eastern Asia (FAO)`, 2000-2015 book-period subset. | Weak partial; levels/trend are revised and early years missing. |
| Latin America | Present, early-1990s-2015 regional line. | Current FAO successor entity `Latin America and the Caribbean (FAO)`, 2000-2015 book-period subset. | Partial; early years missing and regional definition is broader label. |
| World | Absent from original. | Removed from book-period recreation; retained only as a documented successor diagnostic if needed. | Prior substitution corrected. |

## Reviewer Challenge

- **What would Steven Pinker question?** Whether each book regional curve is present and named correctly. Resolved partly: labels now target the right FAO successor regions; documented blocker: exact 1991-2015 regional vintage missing.
- **What would a skeptical data journalist question?** Whether Africa/Asia/World substitutions hid missing series. Resolved: World substitution removed; broad-region substitutions replaced with specific successor region entities.
- **What would another researcher question?** Whether current FAO 2000-2024 values can stand in for FAO 2014. Documented as a research task, not treated as verified.

## Scorecard

| Criterion | Score (1-5) | Justification |
| --- | ---: | --- |
| Source recovery | 2 | Main developing-world line is recovered; regional book vintage is not. |
| Citation chain | 3 | FAO/OWID chain is documented, but Roser 2016j regional file remains missing. |
| Visual similarity | 2 | Improved regional labels and removed World substitution, but regional curves start at 2000 rather than the book's early-1990s coverage. |
| Extension quality | 3 | Current FAO successor extends to 2024 and is clearly separated as successor evidence. |
| Caption quality | 4 | Caption now states the substitution risk and missing vintage. |
| Editorial quality | 4 | Status is not over-promoted and discrepancies are explicit. |
| Overall confidence | 2 | Useful source-family partial match only. |
