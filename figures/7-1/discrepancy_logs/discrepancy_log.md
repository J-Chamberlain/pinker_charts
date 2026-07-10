# Discrepancy Log: Figure 7-1

- Side-by-side comparisons regenerated on 2026-07-09 with
  `scripts/reconstruct_7_1.py`.
- The prior clean/recreated figure omitted the book's England line because the
  current OWID successor file contains `United Kingdom` and no `England`
  entity. This run adds the source `United Kingdom` series and displays it as
  `England/UK`.
- Current status remains `partial_match`.

## Visible Discrepancies

- The book labels a dotted `England` line that rises smoothly from about 2,200
  to 3,400 calories. The current reconstruction uses the OWID `United Kingdom`
  source series; it broadly occupies the same role but is not proven to be the
  exact England series used by Pinker.
- The reconstructed France and United States long-run lines have sharper
  mid-nineteenth and mid-twentieth-century movements than the book figure.
- China, India, and World broadly match the post-1960 layout but the exact
  annual shapes and label positions differ.
- The extended comparison is visually clear after note wrapping, but the
  extension stops in 2018 because the local same-named OWID successor file ends
  there. The newer live OWID 2026 series through 2023 was not merged because it
  has changed values/methodology.

## Cause Assessment

The main unresolved cause is source vintage: the exact 2016 OWID/FAO variable
data were not recovered. The current artifact is a documented updated-equivalent
reconstruction package, not a verified reproduction.
