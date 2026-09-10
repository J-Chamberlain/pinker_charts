# Figure 15-9 provenance

## Source chain

The original crop is `references/figures/figure_15_9.png`. Pinker's source note names
Our World in Data / Ortiz-Ospina and Roser (2016a), with underlying historical sources:

- England: children aged 10-14 recorded as working, Cunningham 1996.
- United States: Whaples 2005.
- Italy: children aged 10-14, Tonioli and Vecchi 2007.
- World ILO-EPEAP: ages 10-14, Basu 1999 and the ILO estimates/projections program.
- World ILO-IPEC: ages 5-17, ILO 2013.

## Recovered data

`figures/15-9/data/raw/owid_various_measures_child_labour_incidence.csv` is the public
OWID historical table. Its metadata identifies the source citation and contains the
five series shown by the reference: England, United States, Italy, World ILO-EPEAP,
and World ILO-IPEC. The reconstruction only renames fields and filters to those five
series; values are not digitized, interpolated, or smoothed.

The OWID metadata describes the historical chart's US source as Long (1958), while
Pinker cites Whaples (2005), likely reflecting a secondary source or source-version
difference. This is documented rather than hidden. The reference itself also warns
that the age bands and definitions differ across series.

## Extension disposition

The recovered historical table ends in 2012. Current ILO indicators use revised
definitions and estimation frameworks, so no post-2012 continuation was accepted as
comparable. The extended output therefore retains the book-period data and explicitly
states that no extension was recovered.
