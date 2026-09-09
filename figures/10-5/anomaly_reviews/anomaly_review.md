Visual review date: 2026-07-09

## Reviewer-visible issues

- The book reference has two lines: black oil-spill counts and gray oil shipped by sea. The regenerated reconstruction plots only the black oil-spill line.
- The right y-axis is retained to preserve the book figure structure, but the gray series is explicitly labeled as not plotted because the annual 1970-2016 source was not recovered.
- The extended artifact carries forward only the OWID/ITOPF spill-count series through 2025. It does not plot a UNCTAD oil-shipping successor.
- This means visual fidelity is intentionally incomplete. The artifact should not be described as a verified reproduction, reconstructed dual-axis figure, or verified extension.

## Evidence review

- Accepted: OWID `number-oil-spills.csv` gives annual World large and medium tanker spills. The plotted spill-count line is the exact row-level sum of those two columns.
- Accepted as context: the book/Breakthrough figure note defines oil shipped as total crude oil, petroleum product, and gas loaded.
- Accepted as diagnostic only: UNCTAD RMT 2020 Table 1.1 provides selected-year tanker-trade values for 1970, 1980, 1990, 2000, and 2005-2019.
- Rejected for plotting: current UNCTADStat `US.SeaborneTrade` bulk data start in 2000 and cargo 11+12 values differ from RMT selected-year tanker-trade values by about 31-48 percent on overlap.
- Not recovered: the exact Roser 2016r/ITOPF/UNCTADStat annual oil-shipped-by-sea source or archived equivalent.

## Disposition

- Keep status at `partial_match`.
- Keep source-recovery stage open.
- Do not add a post-book oil-shipping extension until a same-definition, same-scale institutional series is recovered.
- Do not update `data/figure_registry.csv` in this run; the orchestrator owns registry updates after external review.

## Editorial Review Summary

- Critical issues found: none for a documented partial artifact; reference image, reconstruction image, captions, and source notes are present.
- Major issues found: the reconstruction does not visually reproduce the book figure because the gray oil-shipped-by-sea line is absent.
- Issues automatically corrected: removed unsupported annual-mirror language; regenerated comparison artifacts so the missing gray line is visibly labeled; documented the current UNCTAD bulk file as rejected successor evidence.
- Minor issues remaining: typography and plot proportions are approximate; the side-by-side comparison has substantial whitespace because it preserves the existing reference crop and current reconstruction dimensions.
- Publication disposition: acceptable only as a documented partial/source-recovery artifact, not as a verified reproduction or verified extension.
