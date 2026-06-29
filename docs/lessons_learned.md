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
