# Figure 18-1 provenance

## Original source note

`Stevenson & Wolfers 2008a, fig. 11, based on data from the Gallup World Poll 2006. Credit: Betsey Stevenson and Justin Wolfers.`

The figure plots 131 country aggregates. The vertical axis is an ordered-probit life-satisfaction index. The horizontal axis is real GDP per capita in thousands of dollars on a log scale, using purchasing-power-parity values in constant 2000 international dollars. The figure also shows the cross-country regression and country-specific within-country income gradients.

## Resolved source chain

1. Pinker, *Enlightenment Now*, Figure 18-1.
2. Stevenson and Wolfers, “Economic Growth and Happiness: Reassessing the Easterlin Paradox,” *Brookings Papers on Economic Activity* (2008), Figure 11.
3. Gallup World Poll, 2006, for the respondent-level life-satisfaction and household-income data.
4. Authors’ GDP construction from Penn World Table and other macroeconomic inputs, documented in the replication archive.
5. Authors’ regressions and country aggregation, documented in the archived Stata do-files.

The exact paper and its official replication archive were located. The archive is linked from the authors’ research page and is available at `https://users.nber.org/~jwolfers/data/EasterlinParadox.zip`. Its Gallup directory explicitly states that the 2006 Gallup World Poll cannot be shared because the data belong to Gallup.

## Current recovery state

The original reference is stored at `references/figures/figure_18_1.png`. The redistributable replication materials are preserved under `data/raw/replication_archive/`, including the archive manifest, checksum, master driver, GDP build script, and Gallup processing documentation. No values were digitized from the Pinker or paper figure, and no proxy data were used to draw a reconstruction.

The figure is therefore classified `needs_targeted_source_recovery`: provenance is strong, but the exact Gallup respondent file or a legitimate country-aggregate release is still required for a reproducible plot.

## Required continuation

Obtain authorized access to the 2006 Gallup World Poll or an exact author-provided aggregate extract. Re-run the archived data preparation and regression steps, record the data version and any license restrictions, export a clean country-level table, and then reproduce both the book-period plot and any clearly distinguished extension.
