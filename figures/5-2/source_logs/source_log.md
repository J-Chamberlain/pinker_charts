# Source Discovery Log: Figure 5-2

Figure title: Child mortality, 1751-2013

Original book citation: Our World in Data, Roser 2016a, based on UN Child Mortality Estimates and the Human Mortality Database.

## Search Queries Attempted
- "Figure 5-2" Kindle search
- "Child mortality, 1751-2013" Our World in Data dataset
- "Child mortality, 1751-2013" historical CSV
- "Our World in Data, Roser 2016a, based on UN Child Mortality Estimates and the Human Mortality Database."
- Internet Archive and successor dataset checks

## Sources Investigated
- Kindle search/page capture: accepted for title, citation, and visual reference where captured.
- Local OWID datasets mirror: accepted where it matched the named source chain or as a documented proxy.
- Current OWID grapher downloads: accepted only as successor/extension evidence.
- Internet Archive/GitHub/source mirrors: logged as required next searches where exact archival source remains unresolved.
- Prior Gapminder 2013 proxy: rejected for current canonical reconstruction because it visibly diverged from the Kindle figure.
- Current OWID selected child-mortality grapher: accepted as an improved proxy after confirming that the downloaded values are already percent units.
- OWID Git history, commit `b6746f923dd64ca0fad7de1b1f2f78bebe25205f`:
  accepted as an immutable archival recovery of dataset 161, “Child Mortality
  Estimates - CME Info (2016).” The metadata records retrieval from CME Info on
  2016-01-29. Rejected as a complete reconstruction source because it begins in
  1970 and contains no HMD historical segment.
- Complete public `owid/owid-datasets` history: searched for current/deleted
  child-mortality and Human Mortality Database paths. No assembled Figure 5-2
  export was found.
- Wayback CDX for the OWID grapher CSV and wildcard URL: no usable archived CSV
  capture returned.
- Live OWID metadata (retrieved 2026-07-10 local time; endpoint reports
  2026-07-11 UTC): accepted for successor classification. It
  names Gapminder (2015) and UN IGME (2025), proving that the live source chain
  is not the cited 2016 UN/HMD chain.

## Remaining Uncertainties
- Status is `partial_match`. The exact Roser 2016a assembly based on UN Child Mortality Estimates and the Human Mortality Database remains unrecovered.
- Remaining visual differences are most likely source-vintage/country-series construction rather than only styling.
- The exact chart assembly cannot presently be regenerated from the recovered
  CME component because the HMD input and OWID's 2016 merge/cutover rules are
  absent. HMD controlled-access history further limits independent recovery.

## Recommended Next Steps
- Seek an author-held export, OWID database backup/chart revision, or an archive
  outside the public grapher and `owid-datasets` repository.
- Do not upgrade the figure until the exact historical dataset or an archival equivalent is recovered.
