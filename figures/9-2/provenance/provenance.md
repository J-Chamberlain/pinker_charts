# Figure 9-2 Provenance

## Evidence

- Title: Global inequality, 1820-2011
- Source line: Milanovic 2016, fig. 3.1. The left-hand curve shows 1990 international dollars of disposable income per capita; the right-hand curve shows 2005 international dollars, and combines household surveys of per capita disposable income and consumption.
- Figure/source inspected from: Supplemental Graphics PDF page 10, rendered at `figures/9-2/plots/comparisons/supplemental_pdf_page_10_figure_9_2.png`.
- Surrounding text inspected from Supplemental Graphics PDF page 10. Pinker introduces the figure as evidence that, despite anxiety about rising within-country inequality in Western countries, global inequality was declining, and immediately frames the decline as a decline in poverty.
- Claim summary: Estimated global interpersonal Gini rose into the mid-twentieth century and declined in the 2005-dollar household-survey series after about 2000.
- Bibliography resolved: Branko Milanovic, *Global Inequality: A New Approach for the Age of Globalization*, Belknap Press of Harvard University Press, 2016, ISBN 9780674737136.

## Source Recovery Result

Milanovic 2016 figure 3.1 underlying table was not recovered as an inspectable data file.

Targeted 2026-07-09 recovery checks:

- Public web searches for exact combinations of "Milanovic 2016", "figure 3.1", "Global inequality", "1820-2011", "supplementary material", "xls", and "xlsx" found references to supplementary material but no downloadable figure 3.1 table.
- Harvard University Press live ISBN page `https://www.hup.harvard.edu/books/9780674737136` returned an AWS/CloudFront challenge from this environment and did not expose inspectable data.
- LIS book page `https://www.lisdatacenter.org/books/global-inequality-a-new-approach-for-the-age-of-globalization/` confirms the book entry but exposes no supplementary files.
- Wayback CDX checks for the tested Harvard ISBN URLs returned no 200 captures; broad archived xls searches for likely HUP, author, and old World Bank paths did not recover `thepast.xls`, a figure 3.1 spreadsheet, or a publisher supplement.
- Later Milanovic material identifies a related successor working file, `History/thepast.xls`, in 2024 slides, but the file itself was not public and the slides are not an inspectable data source.

Closest verifiable successor evidence: Milanovic 2024, "The three eras of global inequality, 1820-2020 with the focus on the past thirty years," re-estimates the same broad concept through 2018 and documents that 1820-1980 is revised Bourguignon-Morrisson with Maddison Project 2017/2011 PPPs, while post-1980 estimates are based on Lakner-Milanovic, Milanovic 2021/2022, and unpublished calculations. This is not comparable enough to splice into Pinker's 2016 figure because Pinker's source note explicitly combines a 1990-international-dollar historical left-hand curve with a 2005-international-dollar household-survey right-hand curve.

## Reconstruction

No reconstruction data file was accepted. The generated comparison images include a source-reference/status panel only, not a reconstructed chart. This is intentional: the source-recovery rule forbids using digitized values from the book chart as reconstruction data.

Visual constraints from the Supplemental PDF: y-axis Gini index 0.25-0.75; x-axis labeled 1800-2000 with ticks at 1825, 1850, 1875, 1900, 1925, 1950, 1975, and 2000; a gray historical series runs from roughly 1820 through 1992/1990s; a black household-survey series runs from roughly 1988 through 2011. These constraints are documented, but no plotted values were digitized.

No extension is plotted. The 2024 Milanovic successor is methodologically revised and partly unpublished; it is useful provenance but not a verifiably comparable continuation of the book-period figure.

## Next Action

Recover the actual supplementary material for Milanovic 2016 figure 3.1, likely including the author workbook referenced in later slides as `History/thepast.xls`, or obtain publisher/author supplementary files that expose the figure 3.1 values directly.
