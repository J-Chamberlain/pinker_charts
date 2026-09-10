# Figure 15-9 source discovery log

## Queries attempted

- `site:ourworldindata.org/grapher child labor England 1850 Cunningham 1996`
- `Our World in Data child labor Ortiz-Ospina Roser 2016 data`
- `ILO ILO-EPEAP child labor ages 10-14 Basu 1999 dataset`
- `ILO ILO-IPEC child labor ages 5-17 2013 data`
- `various measures of child labour incidence OWID csv`

## Sources investigated

- [Our World in Data Child Labor](https://ourworldindata.org/child-labor) was accepted
  as the primary public source because it describes the historical comparison and
  provides the matching five-series grapher.
- [OWID historical grapher CSV](https://ourworldindata.org/grapher/various-measures-of-child-labour-incidence.csv)
  was accepted and downloaded as the reconstruction input.
- [OWID grapher metadata](https://ourworldindata.org/grapher/various-measures-of-child-labour-incidence.metadata.json)
  was accepted for source citations, units, selection, and data vintage.
- [ILO child labour facts and figures](https://www.ilo.org/publications/child-labour-facts-and-figures)
  was accepted as institutional confirmation of the 2013 ILO-IPEC endpoint and global
  2000-2012 estimates.
- [ILO child labour statistics](https://ilostat.ilo.org/data/) was investigated as a
  possible successor source, but current tables use changed definitions and coverage.
- Basu (1999), Cunningham/Viazzo (1996), and Tonioli/Vecchi (2007) were retained as
  bibliography leads through the OWID metadata and book source note.

## Rejected sources

- Current ILOSTAT indicators were rejected for automatic extension because their
  definitions and modeled coverage are not demonstrated to continue the heterogeneous
  historical series.
- Secondary charts and the Pinker reference image were rejected as numeric sources.

## Downloads and archives

- `https://ourworldindata.org/grapher/various-measures-of-child-labour-incidence.csv`
- `https://ourworldindata.org/grapher/various-measures-of-child-labour-incidence.metadata.json`
- `https://ourworldindata.org/child-labor`
- `https://www.ilo.org/publications/child-labour-facts-and-figures`

## Remaining uncertainties

- The OWID metadata's US attribution (Long 1958) differs from Pinker's Whaples 2005
  citation; exact archival handoff between the two is not byte-verified.
- Historical source definitions and age bands are not harmonized, as disclosed in the
  reference and caption.
- A comparable extension after 2012 remains unresolved.

## Recommended next step

Resolve the Long/Whaples source-version difference, then evaluate a post-2012 ILO
continuation only after a documented definition bridge is available.
