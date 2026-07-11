# Anomaly Review: Figure 5-2

## Visible Differences
- Axes, five series, percent scale, and labeled 1751–2013 range match the book.
- Removing predecessor segments from Canada, Chile, and Ethiopia materially
  improves the ten-second visual match.
- Ethiopia's 1966–1980 shape and small country endpoints remain visibly
  different, consistent with revision of the successor data.
- Typography, line shades, and label placement remain approximate.
## Cause Assessment
- Current status: `partial_match`.
- Major issue, explained but unresolved: the exact Roser 2016a UN/HMD assembly
  is absent. The plot uses a changed-source successor proxy and visually
  inferred start cutovers.
- Minor issues: typography, grayscale, and exact label geometry.
- No extension is shown because comparability is unverified.

## Reviewer Challenge
- Pinker would likely ask whether the cited source chain has been reconstructed
  exactly: no; that limitation is explicit in the plot and caption.
- A data journalist would ask for immutable evidence: the recovered CME 2016
  component, metadata, checksums, URLs, and dedicated script are retained.
- A peer reviewer would ask whether successor data are distinguished: every
  clean row is labeled `current_owid_successor_proxy`, and no extension is
  plotted.
- A skeptical reader would notice Ethiopia and label differences: both are
  documented rather than presented as verified fidelity.

## Editorial Review Summary

- Critical issues found: none; the reference, partial-match plot, caption, and
  source evidence are present.
- Major issues found: unrecovered exact source vintage; prior plot included
  conspicuous extra historical segments and implied a comparable extension.
- Automatically corrected: extra segments removed, labels repositioned, and
  the extended artifact changed to an explicit no-extension review view.
- Minor issues remaining: typeface, gray shades, line weight, and exact labels.
- Publication decision: acceptable only as a documented partial/source-
  recovery package. It is not acceptable as a verified reproduction.

Overall confidence:
- Book approximation: medium; close broad trajectories, unrecovered vintage.
- Extension: not plotted; comparability not established.
- Source provenance: medium; contemporaneous UN component recovered, complete
  assembly missing.
- Outstanding risks: exact HMD input, merge rules, and 2016 endpoint values.
- Recommended next action: request an OWID chart revision/database export or
  author-held Roser 2016a assembled file before promoting status.
