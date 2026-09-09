# Anomaly Review: Figure 5-3

## Visible Differences
- Styling, typography, label placement, and crop geometry are approximate.
- The reconstructed Malaysia line now follows the book's 1930s-1990s trajectory, but the 1998-2013 tail comes from current OWID successor data because the exact book-era OWID/World Bank supplement was not recovered.
- Ethiopia is visually plausible but not source-verified to the book vintage; it is not present in Gapminder GD010.

## Cause Assessment
- Current status: `partial_match`.
- Source fidelity: recovered original Gapminder component for Sweden, United States, and Malaysia; unresolved OWID/World Bank 2015 component for Ethiopia and short country tails.

## Reviewer Challenge
- Pinker would likely ask whether the exact OWID chart dataset used for the book was recovered. Answer: partly; the cited Gapminder workbook was recovered, but the complete OWID/World Bank 2015 vintage was not.
- A data journalist would ask for archival URLs and machine-readable source files. Answer: Gapminder source files and archived OWID article/SVG are stored with checksums; the archived OWID CSV remains missing.
- A peer reviewer would ask whether successor data are separated from recovered data. Answer: yes, every clean row has `source_component` and `provenance_url`.
- A skeptical reader would notice that Ethiopia and late tails have weaker provenance than the long-run Gapminder lines. This remains documented rather than hidden.

Overall confidence:
- Book reconstruction: 0.78
- Extension: N/A; no verified comparable extension is asserted in this run.
- Source provenance: medium-high for recovered Gapminder component, medium-low for Ethiopia and post-Gapminder tails.
- Outstanding risks: exact Roser 2016p/World Bank 2015 machine-readable source vintage remains incomplete.
- Recommended next action: targeted source recovery before status promotion.
