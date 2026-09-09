# Figure 17-5 Search Iterations

2026-09-09; queries attempted in sequence (some batched). Results and accepted
URLs are in the source log. Search-engine snippets were not used as data.

1. `site.humanprogress.org "1937" necessities`
2. `Mark Perry 2016 necessities disposable income food home cars clothing housing 1929`
3. `site.aei.org "necessities" "2016" "Perry"`
4. `site.humanprogress.org "spending" "necessities"`
5. `site.aei.org "disposable" "gasoline" "2015"`
6. `Mark Perry "basics" "gasoline" spending income`
7. `"humanprogress.org/static/1937" gasoline`
8. `site.fred.stlouisfed.org/series "Personal consumption expenditures: Nondurable goods: Gasoline" annual`
9. `site.fred.stlouisfed.org/series "Disposable Personal Income" "Annual" "A067"`
10. `site.alfred.stlouisfed.org "vintage_date" "graph" csv`
11. `site.bea.gov "Section2All" xlsx`
12. `site.fred.stlouisfed.org/series/A067RC1A027NBEA`
13. `site.fred.stlouisfed.org/series/DGOERC1A027NBEA`

Direct source recovery then followed the actual FRED component table links.
2016 vintage selection and full-range browser export recovered eight series.
Five components reproduce the archive's baseline to its eight-decimal
precision. Comparing broad/narrow fuel definitions explains why baseline-only
or motor-fuels-only plots would visibly miss early book levels. Both candidate
definitions are retained; the broader definition remains explicitly inferred.
No numerical values were measured from the book image.
