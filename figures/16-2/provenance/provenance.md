# Figure 16-2: Basic education, 1820-2010

## Evidence and original data
Original supplied Supplemental Graphics PDF p30 lower panel inspected directly.
Source note: Roser & Nagdy 2016c, OWID, based on van Zanden et al. 2014;
van Leeuwen & van Leeuwen-Li 2014, pp88-93. Basic education means some schooling
among adults 15+, not completion of a modern primary curriculum or a learning test.
Full surrounding Pinker prose is absent from the supplemental reference.

The [archived OWID topic](https://web.archive.org/web/20171001063038id_/https://ourworldindata.org/primary-and-secondary-education)
links the actual [regional CSV](https://web.archive.org/web/20150921004145id_/http://www.ourworldindata.org/roser/graphs/SchoolAttended_byWorldRegion_Since1870/SchoolAttended_byWorldRegion_Since1870.csv).
The requested December2016 archive redirected to September21,2015. Retained bytes:
SHA256 `0d9c8a15df708bfb4beda60f627ce634bfb8e74d2e85c23efc7f5d7eba2408dc`.
Nine series, 133 regional/World decadal observations plus World1820 backcast.
No numerical value was digitized from a plotted curve.

## Original publication and independent numeric cross-check
Bas van Leeuwen and Jieli van Leeuwen-Li, Education since 1820, in van Zanden
et al. (eds), How Was Life? Global Well-being since 1820, OECD/IISH2014, pp87-100.
[Publication](https://www.oecd-ilibrary.org/how-was-life_5jz41pwdz5zn.pdf), chapter
methodology inspected with web PDF reader. Direct requests download returned403,
recorded honestly; local plotting does not depend on that PDF.

[Table5.3 original XLS](https://doi.org/10.1787/888933095742) redirects to
`https://statlinks.oecdcode.org/302014041P1G014.XLS`, version1 June23,2014.
The XLS incorrectly labels row24 as2010 and row25 as2000. Printed Table5.3 p94
(PDF95 zero-indexed) and archived OWID agree those rows mean2000 then2010.
Cross-check preserves `source_year` and corrected `year`; all133 values agree
exactly, after this explicitly documented label correction. The untouched XLS is
retained. It is not used as an unacknowledged alternate chronology.

[Figure5.1 original XLS](https://doi.org/10.1787/888933095666) redirects to
`https://statlinks.oecdcode.org/302014041P1G010.XLS`. This independently gives the
World1820 backcast17.189273...; archived OWID rounds to17.2. The plot uses the
archived value, not a hand-entered anchor. The separate OWID1870 best-guess24 is
not duplicated over the actual regional table World23.9. Eastern Europe ends1990;
no carry-forward invented. World and regions are the source aggregates, not new
unweighted averages of countries.

The source combines historical estimates with modified Cohen/Soto, Barro/Lee and
Morrisson/Murtin material. Early estimates use inventory/back-projection methods;
World1820 is regression backcasting, not a population survey. Definitions,
geography and measurement quality vary over time. The chapter discusses these limits.

## Successor decision
Current [OWID export](https://ourworldindata.org/grapher/population-having-attained-at-least-basic-education.csv)
and metadata retained. It now cites Barro/Lee2015 and Lee/Lee2016 rather than the
original Clio/OECD regional assembly. Metadata says 2015 onward are projections.
Continental regions differ from the book's groups; chart subtitle says15+ while
its variable long title says15-64. This is not an observed comparable extension.
Retain seven World/continental candidate series in a diagnostic only; do not show
their projections as realized educational progress. The extended comparison repeats
the book reconstruction and explicitly says no observed extension is plotted.
The separate current world basic-education CSV is also retained as a candidate,
not accepted as the old OECD World series.

## Reproducibility and status
`python scripts/reconstruct_16_2.py` runs offline from three retained inputs.
Book long-form CSV, explicit OECD year-error cross-check, and rejected successor
CSV are saved with row roles. Lineage JSON/CSV and database hashes preserve which
inputs generate which plot. Refresh must retain old versions and re-evaluate
definitions, geography and projection/observation flags; never overwrite history.

Status partial_match: original assembly is recovered but several curves appear
roughly one percentage point below the source in the book. No arbitrary offset
applied. No comparable observed extension accepted. Review draft is useful but
not independently publication-approved. Next: seek author plotting assembly and
comparable adult-attainment regional observations, not net child enrollment.
