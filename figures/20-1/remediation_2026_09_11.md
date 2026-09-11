# Figure 20-1 partial recovery, September 11

## Data recovered

scripts/reconstruct_20_1.py parses the saved Roper HTML AGE table (Edison/NEP)
and the Ashcroft PDF page 5, Table 2, Leave percentage row. Ten observations
are retained with original age labels, source URLs, table locators, percentages
and explicit coordinate methods. No values originate in chart pixels.

Closed bins use 2016 minus the mean of age limits. Both sources have an open
65+ bin: its midpoint is undefined. We do not invent an upper age to imitate
Pinker. A hollow point at the latest birth-year boundary (1951) retains the
legitimate percentage without pretending it is a mean birth year. It is not
connected to the younger bins. Day/month of birth is not resolved by age bins.

## Targeted source search

- Query: Inglehart Norris 2016 replication data populist Figure 8 ESS.
  Harvard RWP16-026 remains the exact paper; no numeric European table recovered.
- Inspected https://www.pippanorris.com/data. No exact 2016 figure-data download
  is listed. GPS2019 and later books are different classifications/vintages.
- Harvard Dataverse API search, q="Cultural Backlash", returned four datasets.
  Schafer's 2021 critique, doi:10.7910/DVN/FVZ8TR, uses ESS1-9 and is NOT the
  original authors' replication. It is not accepted as original figure data.
- ESS https://www.europeansocialsurvey.org/data-portal distributes public data.
  Registered workflow is an access step, not evidence of permanent unavailability.
- The previously cited sophieehill/ess-cumulative guide is independent code,
  not Inglehart/Norris author code. Do not attribute it to those authors.

Next: recover exact ESS1-6 edition and party/country/round coding, denominator,
poststratification/design weights and cohort bins. Author aggregate table/code
would be preferable; no outreach was sent in this run.

## Visual and editorial review

Opened original reference and real book-period comparison. Trump and Brexit
closed-bin levels and slopes resemble the corresponding book curves. Oldest
segments differ visibly because the source does not define an open-bin midpoint.
The European curve and its right axis are absent and prominently disclosed.
Critical completeness issue remains: third series missing. Major oldest-cohort
coordinate issue remains documented. No certification as publication-ready.
No extended image is created: later elections would be distinct events, and a
birth-year x-axis must not be mistaken for a calendar-year time series.

Pinker would ask for his precise cohort coordinates; unresolved. A journalist
would notice the absent European line; disclosed. A peer reviewer would ask for
ESS weights/party codes; unresolved. A skeptical reader would question detached
points; the caption explains the open-ended bins.

Overall confidence: high in recovered percentages, low in complete reconstruction.
Book reconstruction: partial_match. Extension: not a direct continuation.
Source provenance: two original poll families; ESS missing.
Outstanding risks: incomplete third series, original coordinate convention.
Next action: targeted ESS recovery; preserve useful two-component data meanwhile.
