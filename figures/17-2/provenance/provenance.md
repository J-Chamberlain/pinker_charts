# Figure 17-2 provenance

Original: Supplemental Graphics PDF p33 lower panel, visually inspected 2026-09-09.
Title: Retirement, US, 1880-2010. Source: Housel 2013, based on data from the Bureau of Labor Statistics, and Costa 1998.
The reference measures labor-force participation, not retirement status or retirement income.

## Citation and numeric chain

1. Morgan Housel, [The Biggest Retirement Myth Ever Told](https://www.fool.com/investing/general/2013/05/02/the-biggest-retirement-myth-ever-told.aspx), May 2, 2013. Article credits Economic History Association and BLS; no author spreadsheet recovered. Its charts were NOT digitized or used as the book reference.
2. Dora L. Costa, *The Evolution of Retirement: An American Economic History, 1880-1990*, University of Chicago Press, 1998. [Chapter 2, Appendix Table 2A.1, printed p29](https://www.nber.org/system/files/chapters/c6108/c6108.pdf). Numeric gainful-employment column, 1880-1990, extracted from the PDF text by `scripts/recover_17_2_tables.py`. Full chapter remains in ignored temporary storage; download hash and deterministic extraction are retained. The chapter identifies Moen (1987), extended using integrated public-use Census samples (Ruggles and Sobek 1995).
3. Joanna Short, [Economic History of Retirement in the United States](https://eh.net/encyclopedia/economic-history-of-retirement-in-the-united-states/), EH.Net, September 30, 2002. Table 1 agrees with all 12 Costa historical observations; its 2000 entry is 17.5%, used unchanged. Original BLS release behind this entry remains unidentified.
4. [BLS 2010 annual Table 3](https://www.bls.gov/cps/aa2010/cpsaat3.pdf), first page, all-races Men 65 years and over: 22.1% participating. Machine-extracted published percent; not recomputed from rounded population counts. Original government PDF is retained.
5. Megan Wilkins, [Golden years: older Americans at work and play](https://www.bls.gov/opub/btn/volume-14/golden-years-older-americans-at-work-and-play.htm), BLS, May 29, 2025, Chart 2 numeric table. Requests returned 403, but normal Computer Use loaded the public page. The visible table was exposed with View Chart Data, and its exact DOM HTML saved. No values transcribed from plotted geometry. The 2010 anchor agrees exactly with the original BLS release; annual 2011-2024 continuation is dashed.

## Definitions and vintage

Costa's historical measure is having an occupation during the preceding year, not the CPS survey-week measure. The original source discusses this difference. The main plot preserves the book's apparent historical assembly, not a newly harmonized series. A diagnostic compares the definitions. Modern CPS values must NOT replace historical Costa values simply because both are called participation.

The 2017 OWID/Short/OECD export is retained as an independent cross-check only, not a plotted input. Its 2000 value is 17.73170905 rather than Short's 17.5. Plotting uses the older cited institutional path instead.

## Reproduce and refresh

Run `.venv/bin/python scripts/reconstruct_17_2.py` offline from retained inputs. To re-extract Costa, download the linked chapter to ignored temporary storage and run `.venv/bin/python scripts/recover_17_2_tables.py --costa-pdf tmp/source_cache/costa_1998_chapter2.pdf` (hash pinned).
For refresh, retrieve a new BLS annual-average release into a NEW dated raw file, compare the overlapping years, and update extension input only after review. Preserve the 2010 release and historical table. Do not use incomplete-year monthly observations as annual averages.

Status: `partial_match`. Sources and variables are strong, but small historical level differences and the exact Housel assembly remain unresolved. No offset was fitted to book pixels. Surrounding Kindle prose was not reviewed; the supplied graphics PDF is the authorized visual/source reference.
