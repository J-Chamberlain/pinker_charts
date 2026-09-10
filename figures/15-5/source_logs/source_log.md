# Figure 15-5 source discovery log

## Queries attempted

- `Ottosson 2006 2009 decriminalization homosexuality dates countries dataset`
- `State Sponsored Homophobia 2009 csv decriminalization`
- `Our World in Data decriminalization homosexuality historical countries 1791 2016`
- `Kenny Patel 2017 Norms and Reform Figure 2 data countries years`
- `ILGA State Sponsored Homophobia older editions 2009`

## Sources investigated

- ILGA State-Sponsored Homophobia 2009 report - accepted as an archived source-family reference, but it is not a machine-readable country-year table.
- Current OWID/Mignot country-year legal-status CSV - accepted as a transparent successor because it exposes the full historical state and supports reproducible counting.
- Archived OWID/Kenny-Patel legal-year table via Wikimedia - investigated; the tabular snapshot is preserved but its old CSV resource is empty in the archived GitHub dataset.
- CGD Kenny & Patel 2017 paper - investigated as a related published analysis, but its updated country universe does not reproduce the Pinker endpoint exactly.

## Remaining uncertainties

- Ottosson's exact country list and treatment of territories/never-criminalized countries are not recovered as a machine-readable original dataset.
- The current Mignot series reaches 91 cumulative first transitions by 2016 versus approximately 92 in the supplied reference.
- Country-year legal status can reflect re-criminalization and changes in territorial boundaries; the first-transition rule is an explicit approximation to the plotted concept.

## Recommended next steps

Recover the original Ottosson 2006/2009 country/date tables or the July 31, 2016 Wikipedia revision, then compare event-by-event before any promotion to `verified_reproduction`.
