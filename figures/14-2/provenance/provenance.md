# Figure 14-2 provenance

Original: authorized Supplemental Graphics PDF p23 lower; title Human rights,
1949-2014. Short source: OWID, Roser2016i, Fariss2014. Measures protection from
physical-integrity abuses, not all human rights. Original inspected directly.

## Evidence chain
1. Fariss2014, *Respect for Human Rights has Improved Over Time: Modeling the
Changing Standard of Accountability*, APSR108(2)297-318,
https://doi.org/10.1017/S0003055414000070.
2. Schnakenberg/Fariss2014, *Dynamic Patterns of Human Rights Practices*,
PSRM2(1)1-31, https://doi.org/10.1017/psrm.2013.15.
3. OWID2016 topic https://web.archive.org/web/20170128041222id_/https://ourworldindata.org/human-rights/
and chart259 configuration https://web.archive.org/web/20170201012735id_/https://ourworldindata.org/grapher/config/259.js
identify numerical variable358, World plus countries,1949-2014.
4. Archived chart payload https://web.archive.org/web/20180913134846id_/https://ourworldindata.org/grapher/data/variables/358.json?v=3
has June21,2016 upload metadata, dataset241, all330 selected observations.
This is a numerical source payload, not a downloaded book-figure image.
5. `scripts/reconstruct_14_2.py` parses aligned arrays/entity keys and selects
Norway,World,South Korea,China,North Korea. No interpolation, visual rescaling,
digitization, or fabricated World average.

## Rejected first candidate
The pinned OWID Git dataset239, singular "Score", reports author email June6,2016
and has all202 country entities but no World. The330 selected chart observations
come from dataset241, plural "Scores", NOT a derived mean of239.
Common country values match exactly.2014 unweighted mean is0.323206 versus
provider World0.844099. World aggregation remains undocumented; numeric
diagnostic retains this evidence. No weighted-average guessing is substituted.

## Successor
Fariss/Kenwick/Reuning2020, *Estimating one-sided-killings from a robust
measurement model of human rights*, JPR57(6)801-814,
https://doi.org/10.1177/0022343320965670.
Harvard dataset https://doi.org/10.7910/DVN/RQ85GK, CC0,
file7209241 `LHRS-v4.02-2021.csv`:
https://dataverse.harvard.edu/api/access/datafile/7209241.
Raw columns and posterior intervals retained; COW385/710/731/732 select
countries. Dates1946-2021 retained,2000-2021 displayed in separate panel.
Historical estimates/latent scale and input indicators changed, including new
report sources and killing indicators. Never splice as an unchanged index.
The v4.01 README describes2019, whereas actual v4.02 data extend to2021;
the README is contextual, not a claim that its endpoint matches v4.02.

V2.04 https://doi.org/10.7910/DVN/24872 and v3.01
https://doi.org/10.7910/DVN/TADPGE were also recovered and retained to examine
vintages; neither replaces the book-era OWID payload. Raw bytes, request dates,
hashes, clean tables and explicit per-plot lineage are preserved. Public
presigned redirect credentials are removed from download diagnostics.

Reproduce offline: `.venv/bin/python scripts/reconstruct_14_2.py`.
Refresh into a NEW versioned raw filename using `scripts/source_cache.py`,
then review source-method differences before changing the successor mapping.
Full surrounding Pinker discussion and independent publication approval remain
pending. Small common apparent vertical offset remains; no fit-to-image values.
