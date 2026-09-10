# Figure 15-8 provenance

## Original book source

The reference crop is `references/figures/figure_15_8.png`, extracted from the
Supplemental Graphics PDF. Pinker's source note names two source families:

- Physical and sexual abuse: National Child Abuse and Neglect Data System (NCANDS),
  analyzed by Finkelhor 2014 and Finkelhor et al. 2014.
- Violent victimization at school: U.S. Bureau of Justice Statistics, National Crime
  Victimization Survey, Victimization Analysis Tool (NVAT).

The reference uses rates per 100,000 children under 18 for the abuse series and rates
per 10,000 children aged 12-17 for school victimization. The figure's y-axis combines
those denominators in one label.

## Recovered data

The committed raw source is:

`figures/15-8/data/raw/owid_bjs_school_victimization.csv`

It is the public Our World in Data CSV for the BJS school-victimization series, sourced
from BJS (2017). The file reports rates per 1,000 people aged 12+, for 1993-2015.
The clean tables retain the original rate and add a `rate_per_100000` column by
multiplying by 100. This allows the public subset to be viewed against the reference's
combined visual scale, but it does not make the denominator or population definition
identical to the book's stated school measure.

## Missing data

The NCANDS physical- and sexual-abuse series were not downloaded. NDACAN lists the
historical NCANDS aggregate and agency files, but distribution requires its ordering
process. No values were transcribed from the Pinker plot, and no unrelated maltreatment
proxy was substituted.

## Extension

The 2013-2015 BJS/OWID values are plotted dashed as a continuation of the recovered
school subset only. They are not presented as an extension of the complete three-series
figure.
