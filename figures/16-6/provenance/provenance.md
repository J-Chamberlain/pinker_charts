# Figure 16-6 provenance

Original reference: Supplemental Graphics PDF p32 lower, original pixels in
references/figures/figure_16_6.png. Caption: Global well-being, 1820-2015.
Short source line is retained verbatim in figure.json. Surrounding book text
is not supplied by this graphics-only reference and remains pending.

## Numerical evidence

1. Rijpma, A. (2014), A composite view of well-being since1820, in OECD,
   How Was Life?, pp249-269, specifically Figure13.2 p259.
   https://doi.org/10.1787/9789264214262-17-en
   https://doi.org/10.1787/888933096502 redirects to
   https://statlinks.oecdcode.org/302014041P1G054.XLS . Retained original workbook
   says Version1, last updated23-Jun-2014. Select World, 19decades1820s-2000s.
   These are population-weighted regional averages of an equal-weight composite
   standardized over country-decades. The later latent-variable model is NOT
   the same series. Decade labels are placed at decade starts, as the book does.
2. Prados de la Escosura, L. (2015), World Human Development:1870-2007,
   Review of Income and Wealth61(2),220-247, DOI10.1111/roiw.12104.
   https://www.roiw.org/2015/n2/02%20-%2012104.pdf . Table1 PanelA, printedp230,
   gives14World benchmarks1870-2007. The paper first appeared online2014 but
   the issue year is2015. Numeric table extraction is scripted with a PDF hash
   check. Printed table was rendered and visually checked. No chart digitization.
   The full paper is temporary; the extracted numerical table is retained.

## Transformations and limits

No reweighting or normalization is performed. Original distinct y-axes are
retained, -1to1 for composite and0to.5 displayed for HIHD (defined0to1).
Straight joins connect observed benchmarks, not invented annual observations.
The book has finer intermediate detail and HIHD continues to2015. The latter
update is not in the cited2015 paper's table. Archived OWID2015/2017 data are
regional only and also end2007. OWID2018 numeric data recovered via Git history
contain countries through2015 but no World aggregate; averaging them without
the original weights is rejected.

OECD2021 adds indicators and latent-variable weights. Prados2022 AHDI adds
political freedom and revised dimensions. Neither is spliced onto this chart.
The extension image explicitly repeats the partial historical result, with
no comparable extension plotted. Status partial_match, not verified.

## Reproduce

`.venv/bin/python scripts/reconstruct_16_6.py`

Optional raw-table refresh: download the exact PDF version in the download log,
then run `scripts/recover_16_6_table.py <pdf>` using the project Python runtime.
All chart inputs, the raw-table extractor, per-plot lineage, hashes, and rejected
numeric candidates are retained. The SQLite builder indexes clean observations.
