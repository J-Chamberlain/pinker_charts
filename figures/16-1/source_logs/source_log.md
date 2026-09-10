# Source discovery: 16-1

Title and book citation: see provenance. Research date: September 9, 2026 Pacific
(downloads September 10 UTC). Every request, redirect, success/failure and SHA is
retained in `downloads.json`; these are the exact download/archive URLs.

1. Search `site.ourworldindata.org literacy 1475 Buringh van Zanden 2009 dataset`.
   Current OWID chart and historical literacy explanation found. Current download
   accepted only as successor: historical coverage and values changed.
2. Search existing OWID repository tree for `literacy`. Pinned cross-country CSV
   and metadata found, but retrieval date April 2018 is later than the cited 2016
   version. Reject as exact book input; retain as revision evidence.
3. GitHub commits API for that dataset path returned 2018/2019 history, not 2016.
   Per-country 2018 source-map CSV accepted as later provenance aid, not proof of
   book-era identities.
4. Wayback CDX for `ourworldindata.org/grapher/cross-country-literacy-rates*`,
   2015-2017, returned empty. This was the wrong historical URL structure, not
   evidence that the data were unavailable.
5. Archived OWID literacy topic redirected to January 1, 2017. Followed its old
   static chart HTML; recovered November 2016 HTML and March 2016 actual CSV.
   Accept as canonical book-period input: all eight series, distinctive World and
   Chile features, and sparse European trajectories match the authorized reference.
6. Retrieved separate April 2016 OxLAD illiteracy CSV. Auxiliary original-source
   evidence, not digitization and not needed to replace the long-run input.
7. Direct NCES historical table: accepted independent cross-check of all fourteen
   US 1870-1979 points. Exact complement agreement, including 1950 dip.
8. Retrieved 2019 OWID global literacy CSV and metadata from pinned repository.
   Reject as exact reproduction: large historical revisions. Retain diagnostic.
9. CDX for old static CSV with digest collapse found distinct 2014/2015 digests;
   March 2016 is the captured version actually used here. No evidence of a later
   different book-era file from this query; collapse removes duplicate captures.

Remaining uncertainties: underlying cause of World historical revisions; direct
CIA 2016 endpoint audit; complete book prose/bibliography not in supplied graphic
PDF. Recommended next steps: audit original OECD literacy chapter and archived CIA
tables; preserve the recovered assembly regardless. Researcher can rerun entirely
offline using raw files, download log and explicit script column selection.
