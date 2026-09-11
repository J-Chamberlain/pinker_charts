# Figure 20-1 source discovery log

September 11 update: [targeted recovery and decisions](../remediation_2026_09_11.md).
Two components now have clean data and a real comparison. The third remains
unresolved. Older all-or-nothing recommended sequencing below is superseded.

## Figure

- Figure: 20-1
- Title: Populist support across generations, 2016
- Book sources: Edison Research/NYT; Lord Ashcroft/BBC; Inglehart & Norris 2016 Figure 8.

## Searches and sources

| Query or route | Source investigated | Result |
|---|---|---|
| `Inglehart Norris 2016 fig. 8 European populist parties data` | Harvard Kennedy School working paper, RWP16-026 | Accepted for citation and source-line confirmation; graph values not tabulated. |
| `ESS1-6 cumulative file download` | ESS documentation and Data Download Wizard | Accepted as the authoritative data route; registered access required. |
| `European Social Survey cumulative file GitHub mirror` | `sophieehill/ess-cumulative` | Accepted as a reproducible build guide; it contains code, not the restricted input data. |
| `Lord Ashcroft 24 June 2016 full data tables` | Lord Ashcroft Polls PDF | Accepted and downloaded; age-group Brexit percentages are available. |
| `2016 Trump exit poll age table Edison` | Cornell Roper Center public summary | Accepted as an accessible mirror of the Edison/NEP age table; exact NYT presentation remains a citation detail. |
| `New York Times 2016 exit polls` | NYT interactive | Citation identified, but direct access is unavailable to this environment. |

## Acceptance and rejection

The paper and two exit-poll sources were accepted as evidence for the source chain. The Inglehart-Norris Figure 8 image was rejected as numeric input because it would be digitization of a plotted source value. Modern ESS rounds were not substituted because the book cites the ESS1-6 cumulative file and the variable construction/classification is not interchangeable without review.

## URLs

- Working paper: https://appext.hks.harvard.edu/publications/getFile.aspx?Id=1401
- ESS data portal: https://www.europeansocialsurvey.org/data-portal
- ESS cumulative documentation: https://www.utsc.utoronto.ca/~butler/d29/ess-codebook
- ESS build guide: https://github.com/sophieehill/ess-cumulative
- Brexit full tables: https://lordashcroftpolls.com/wp-content/uploads/2016/06/How-the-UK-voted-Full-tables-1.pdf
- Trump age-table mirror: https://ropercenter.cornell.edu/how-groups-voted-2016

## Remaining uncertainty

The ESS dependent variable is a party-vote indicator classified by the authors, and the exact country/round weighting and birth-cohort bins used for the five-point line must be recovered from the data or author code. Trump and Brexit age categories also need explicit midpoint mapping to match the Pinker x-axis.

## Recommended next step

Register for ESS access, download ESS1-6 or the closest archived edition, locate the authors' party classification and cohort coding, and reproduce the European line before combining it with the independently sourced exit-poll series.
