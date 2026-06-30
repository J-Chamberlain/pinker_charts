# Track D Safety And Mortality Summary

Date: 2026-06-30

Branch: `track-d-safety-mortality`

## Figures Processed

| Figure | Status | Source fidelity | Editorial review finding |
| --- | --- | --- | --- |
| 12-3 | `source_chain_recovered` | Kindle source chain captured; NHTSA 2015 PDF recovered; cited pre-1966 informedforlife PDF unavailable in this pass. | Non-validation only. No reconstruction generated because the book-period source table is missing. |
| 12-4 | `source_chain_recovered` | Kindle source chain captured; exact FHWA/NCSA pedestrian tables not recovered. | Non-validation only. No reconstruction generated because the stitched source tables are missing. |
| 12-5 | `partial_match` | ASN/World Bank source family recovered through OWID-hosted successor data, not exact ASN 2017 extraction. | Major visual/source issue documented: early-1970s peak under-matches Kindle chart. |
| 12-8 | `updated_equivalent` | OWID/EM-DAT source-family data recovered; exact Roser 2016q snapshot still needs version pinning. | Main visual shape matches after sum-then-decade-average correction; residual low-end differences documented. |
| 12-9 | `verified_reproduction` | OWID NOAA/Lopez-Holle source data recovered and visually match Kindle chart. | No critical or major publication blocker found; no comparable post-2015 extension recovered. |

## Editorial Review Summary

Critical issues found: none for generated comparison packages; 12-3 and 12-4 are explicitly non-validation packages.

Major issues found: Figure 12-5 does not fully match the early-1970s Kindle peak and remains `partial_match`; 12-3 and 12-4 require exact source-table recovery before validation.

Minor issues found: Typography and crop framing differ from Kindle style across reconstructed figures.

Issues automatically corrected: Figure 12-8 initially averaged category rows directly; it was corrected to sum disaster categories by year before decade averaging. Figure 12-9 x-axis tick overlap was removed.

Issues remaining: exact informedforlife/NHTSA pre-1966 traffic fatality table; exact FHWA/NCSA pedestrian historical tables; exact ASN 2017 plane-crash extraction; exact Roser 2016q version pin for natural disasters.

Batch disposition: documented partial/blocked batch. Figure 12-9 is verified; Figures 12-5 and 12-8 have useful but conservatively labeled reconstructions; Figures 12-3 and 12-4 stop at source-reference evidence.
