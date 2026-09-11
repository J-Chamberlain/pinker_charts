# September 11 recovery and review

This audit supersedes earlier statements that no numerical reconstruction is possible.
Status: **partial_match**. Execution remains blocked for full analytic verification;
publication remains incomplete. The original author plotting inputs are recovered.

## Evidence and discovery

The authorized supplemental-PDF Figure 18-1 was inspected against both render iterations.
The cited source is Stevenson and Wolfers (2008), Figure 11, Gallup World Poll 2006.
The official archive at https://users.nber.org/~jwolfers/data/EasterlinParadox.zip
contains `Figures/fig11.gph`. Its serialized numerical sersets contain the country
estimates, GDP values, fitted values, and arrow endpoints used by the authors.
These are original numerical inputs, NOT digitized figure coordinates.

The earlier investigation stopped at the archive's notice that Gallup respondent data
cannot be shared. That restriction does not mean its graph caches lack aggregate data.
This pass inventoried every archive member and investigated the native graph payload.
The GPH identifies `gallup_work_inc.dta` and an August 8, 2008 generation date.
Stata's documentation describes data-bearing GPH files:
https://www.stata.com/manuals15/g-4conceptgphfiles.pdf .
No Stata executable was installed locally, so native-render verification is still needed.
Download URLs, actual timestamps and checksums are in `data/raw/recovery_downloads_2026_09_11.json`.
`archive_inventory.json` records the full archive's 97 members and SHA256.
The 111 MB ZIP remains local (GitHub's ordinary file limit); the exact 16 KB GPH is committed.

## Transformation and validation

Run `.venv/bin/python scripts/reconstruct_18_1.py` from the repository root.
The narrow parser rejects unknown version, byte order, type, dimensions, record length,
or mismatched names. Numeric extrema are checked against both binary and text metadata.
Stata missing values become CSV blanks, not extreme observations.
The cache contains 132 country identifiers, 129 visible points and 112 complete arrows.
These counts must not be silently replaced by the paper's commonly cited 131-country count.
Arrow centers equal the country estimates, and log income span equals 0.5.
The saved fitted equation is linear in log GDP, residual below 2.3e-7.
Its display-only extrapolation reaches the axes; it does not add observations.
GDP is in constant-2000 international dollars, PPP; the vertical variable is an
ordered-probit life-satisfaction index, not a 0-10 ladder score.

## Visual and editorial review

Original and final book comparison opened and inspected. Major country clusters,
outliers, arrow directions, axes and fitted line closely resemble the source.
Iteration 1 had undersized labels/points and thin arrows. Iteration 2 increased those
elements without changing values. Minor font and panel alignment differences remain;
crowding of country labels is intrinsic to the original design.
No extended image is generated: a later cross-section requires a separate compatible
Gallup analysis, not extending the GDP axis or relabeling the 2006 graph.

Critical publication issue: redistribution terms for the original aggregate cache and
reference crop have not been established. Major scientific issue: respondent-level
ordered-probit and income regressions cannot yet be independently rerun. This is a
strong rendering recovery, not a fully verified analytic reproduction.

## Reviewer challenge and next action

- Book author: are the arrow endpoints original? Yes, recovered directly; cached
  country counts and any sample exclusions still require confirmation.
- Data journalist: are these survey observations? No, original author estimates.
- Peer reviewer: can the estimators be rerun? Not without licensed Gallup inputs.
- Skeptical reader: why no recent curve? A cross-section needs a new analysis.

Overall confidence: medium. Book rendering: high. Extension: unavailable.
Source provenance: high for original author cache; moderate for analytic reproducibility.
Outstanding risks: cache decoder not independently checked in Stata; reuse permissions.
Recommended next action: native Stata numerical comparison and a narrowly scoped request
for aggregate-data reuse permission/sample exclusions. No request has been sent.

## Acceptance checklist

- [x] Original reference, source and bibliography inspected.
- [x] Original numerical plotting inputs recovered and preserved with hashes.
- [x] Reproducible extraction and comparison visually inspected twice.
- [x] Discrepancies investigated; no pixel digitization or proxy data.
- [ ] Full microdata analysis independently reproduced.
- [ ] Independent native-format validation and publication rights resolved.
- [ ] Comparable post-publication cross-section available.
- [ ] Publication acceptance (not claimed).
