# Figure16-3: Years of schooling,1870-2010

## Original reference and citation
Authorized supplemental PDF p31 upper panel directly inspected. Seven countries:
US,Japan,Chile,China,India,Cambodia,Sierra Leone. Mean years, both sexes age15-64.
Source note: Roser & Ortiz-Ospina2016a, OWID, Lee & Lee2016.
Lee,Jong-Wha and Hanol Lee(2016), Human Capital in the Long Run, Journal of
Development Economics122,147-169, https://doi.org/10.1016/j.jdeveco.2016.05.006.
Publisher abstract/method description reviewed. Full surrounding Pinker prose is
not in the supplied graphics PDF; publication-context review remains open.

## Original numeric recovery
Pinned OWID dataset `Human Capital in Long-Run - Lee-Lee (2016)` from commit
`6155d4ca1ea14ef30e753010a25521eeb416e8a2`; exact download URL and hash in
`source_logs/downloads.json`. Metadata records original retrieval August29,2016.
Use `Total years of schooling (Lee-Lee (2016))`, not enrollment or human capital
index. All seven countries have29 five-year observations,1870-2010:203 rows.

The authors' [August25,2016 download page](https://web.archive.org/web/20160825210444id_/http://www.barrolee.com/Lee_Lee_LRdata_dn.htm)
links their v1.0 age15-64 workbook. The actual retrieved
[archive](https://web.archive.org/web/20170713032259id_/http://barrolee.com/data/Lee_Lee_v1.0/LeeLee_attain_MF1564.xls)
is July13,2017, not the requested August2016 timestamp. Workbook v1.0 January2016;
SHA256 `cd41669d0eab8e82aadf6fa074bf94f8e69befbbe022bdb7e133a3881428259e`.
All203 selected source observations agree EXACTLY with the pinned OWID records.
Country names fill down within the source's merged-cell groups; select ages15-64
and numeric year. No chart digitization, smoothing, interpolation records or scaling.

The [current author workbook](https://barrolee.github.io/BarroLeeDataSet/LeeLee/LeeLee_attain_MF1564.xls)
has the same apparent version label but different cells, so is retained only as
candidate. Version labels alone are inadequate; actual archive and cross-check matter.
These are historical estimates, partly reconstructed from census/enrollment and
school-foundation evidence. They are not direct annual observations or measures
of learning quality. Contemporary and historical estimation uncertainty persists.

## Genuine successor rather than projection
The current OWID chart adds older Barro-Lee2015 projections from2015 onward.
Those CSV/metadata files are retained but NOT used as the observed extension.
Instead, [Barro-Lee v3 methodology](https://barrolee.github.io/BarroLeeDataSet/BLv3.html)
documents a2021 release using new census/survey inputs near2015 plus estimation,
including subsequent US CPS2015 correction. Its
[CSV](https://barrolee.github.io/BarroLeeDataSet/BLData/BL_v3_MF1564.csv) gives the
same both-sex age15-64 concept for all seven countries through2015.
All source columns retained: attainment categories,population,age,sex and years.
Use `yr_sch`, not sum of attainment shares. Select MF,agefrom15,ageto64.

The1950-2010 overlap differs by at most0.005years, consistent with the original
two-decimal rounding. Do not force exact joins: plot revised2000-2010 dotted and
successor2010-2015 dashed with hollow endpoints. Original book line stays frozen.
There are no post2015 observations in this accepted source.2015 is an updated
estimate, not a directly observed census result for every country. The source uses
new observations for96 of146 countries and fills gaps via documented estimation;
age grouping changes from five- to ten-year categories. Cambodia slightly declines
in2015; do not smooth it away or substitute the more optimistic old projection.

## Reproducibility and refresh
`python scripts/reconstruct_16_3.py` runs offline.203 book rows,203 archive-check
rows, full selected successor history and overlap differences are saved. Lineage
specifies exact used files; raw current candidates are not promoted by presence.
Database retains these rows, source references and immutable versions/checksums.
Refresh: retain new author version separately, check age/sex, overlap and source
methods, distinguish new estimates from projections, then update only successor.

Scientific status: verified_reproduction based on original source identity and
close seven-curve visual agreement, not pixel equality or upstream truth guarantee.
Minor line/label and small displayed-level differences remain within visual
tolerance; no fitted adjustments. Extension is comparable successor through2015.
Publication still incomplete until independent/context review. Overall confidence:
high book/source, medium extension inference. Next: independent review and monitor
new author estimates; never silently append the OWID forecast as observation.
