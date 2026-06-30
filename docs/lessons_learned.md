# Lessons Learned

Future runs should append to this document as the project grows.

## Repository Memory

The repository must be the authoritative project memory. Chat history is useful
context, but it is not a reproducible audit trail.

## Institutional Data Is Different From Academic Literature

Institutional datasets require source-specific retrieval strategies. A paper
citation may point to a chart, a public portal, an archived ZIP, a retired API,
or a dataset that has been silently revised.

## Side-By-Side Validation Is Mandatory

A plausible dataset is not enough. The recreated figure must be compared
visually against the book figure because mismatches reveal missing variables,
wrong units, source revisions, or an incorrect data vintage.

## Discrepancies Drive Source Recovery

Visual and numeric discrepancies should become search prompts. Figure 10-5
showed that a correct spill-count series did not solve the full chart because
the second oil-shipping series remained unresolved.

## Successor Datasets Need Explicit Explanation

Modern institutional data can be useful for post-publication extensions, but it
must not be treated as the original data without evidence. Figure 10-6's current
WDI marine protected-area series is visibly discontinuous with the archived WDI
book-period release.

## Digitized Figure Values Are Not Reconstruction Data

Digitizing the book figure can help visual validation, but it is not acceptable
as the underlying reconstruction dataset. Reproductions should be sourced from
public data releases, archives, supplements, or institutional tables.

## Status Labels Protect The Project

Use `verified_reproduction` sparingly. `partial_match` and
`updated_equivalent` are not failures; they are honest descriptions of the
evidence chain.

## Keep Large Raw Data Accountable

Large bulk downloads should be included only when GitHub can reasonably host
them and they are central to the audit trail. Otherwise, preserve URLs,
archive URLs, checksums, and retrieval notes.

## Separate Book-Era OWID Datasets From Current Grapher Data

Figures 10-7 and 10-8 showed that OWID/GitHub book-era datasets can match a
Pinker figure closely while current OWID grapher exports use revised source
versions or category definitions. For extensions, keep the book-era series
solid through the book endpoint and show current successor data only after that
endpoint with explicit caveats.

## Source-Line Capture Is Not Chart Capture

Figure 19-1 showed that a Kindle search result can confirm the title and source
line without providing a usable chart-page visual reference. Treat this as
evidence for citation extraction only; visual validation requires the actual
figure page or a documented reason that manual recapture is required.

## Do Not Let Missing Temporary Captures Overwrite Canonical References

Regeneration scripts should reuse an existing committed Kindle reference image
when a temporary local capture is unavailable. A rerun should never replace a
real reference image with a placeholder simply because the temporary screenshot
directory is absent.

## OWID Proxies Still Need Exact Vintage Proof

Figure 5-2 showed that a plausible OWID/Gapminder country series can reproduce
the concept while still diverging visibly from the book's chart. Do not upgrade
such figures until the exact named source assembly, archival grapher snapshot,
or data vintage is recovered.

## Current OWID Grapher Units Must Be Verified

Figure 5-2 also showed that successor grapher exports may already be in the
book's display units. Inspect column names and values before applying unit
conversions; otherwise an extension can be wrong even when the source is
reasonable.

## An Extended Artifact Is Not Always An Extension

If no methodologically comparable post-publication data are plotted, the image
should say so visibly and the caption should explain why. Do not let a filename
containing `extended` imply that a true extension exists.

## Chart Type Is Part Of Visual Fidelity

Figure 19-1's actual Kindle capture revealed that a line chart proxy cannot
pass visual validation for a stacked-area original even if the broad trend is
similar. Source recovery and transformation must reproduce the visual encoding,
not just the topic.
