# Figure 17-4 provenance

## Original and source chain

Original inspected: supplied Supplemental Graphics PDF page 34, lower panel. Title: Cost of light, England, 1300-2006. Unit: constant-2000 pounds sterling per million lumen-hours; linear scale 0-45,000. Short source: Our World in Data, Roser 2016o, based on Fouquet & Pearson 2012. The PDF supplies the figure and source note, not surrounding prose; no unseen context claimed.

Bibliography resolved: Roger Fouquet and Peter J. G. Pearson (2012), *The long run demand for lighting: elasticities and rebound effects in different phases of economic development*, Economics of Energy & Environmental Policy 1(1), 83-100, DOI 10.5547/2160-5890.1.1.8. [Author manuscript at LSE](https://www.lse.ac.uk/granthaminstitute/wp-content/uploads/2014/06/DemLigEEEP2012.pdf). The paper provides the research context; the numeric source is the authors' series distributed by OWID, not values digitized from that paper.

The [2016 OWID archive](https://web.archive.org/web/20160815131249id_/https://ourworldindata.org/grapher/the-price-for-lighting-per-million-lumen-hours-in-the-uk-in-british-pound-1300-2006) identifies chart 190, indicator 250, entity 451, years 1301-2006 and constant-2000 prices. It describes a five-year moving average. The retained legacy observations are plotted directly; no second moving average is applied. That archive contains configuration, not numeric observations.

The numeric source was recovered from OWID's versioned dataset repository: dataset 187, *Price for Light - Fouquet*, first Git commit 189ffb348bbc843a29d749b6425da6c7798d8d6f (2018-09-21). The downloaded snapshot is pinned to repository SHA 6155d4ca1ea14ef30e753010a25521eeb416e8a2; file history contains only the initial add. Datapackage identifies Fouquet & Pearson 2012 and retrieval date 2017-09-27. All 706 annual values also agree exactly with retained indicator-250 API data. Source identity and visual agreement justify book-period verified_reproduction; byte-for-byte identity with Pinker's private working file is not claimed.

## Transformations and extension

Offline command: `.venv/bin/python scripts/reconstruct_17_4.py` from repository root. Raw legacy CSV -> schema/coverage checks -> rename columns and add units, geographic metadata and version -> plot unchanged values for 1301-2006. The source entity typo "Price for Lightning" is preserved in source_entity; normalized entity is United Kingdom, as the metadata states. No 1300 observation is invented, and the book's England title is retained with a geography note.

Successor: [OWID lighting indicator](https://ourworldindata.org/grapher/the-price-for-lighting-per-million-lumen-hours-in-the-uk-in-british-pound), January 2026 edition, Fouquet 2026 and Fouquet & Pearson 2006, indicator 1144138. Source uses a lighting-source-weighted average, revised historical price indices and OWID five-year smoothing. Retained CSV values already incorporate processing. Keep 1995-2023 for overlap and continuation; do not rebase or force a join. Same stated units and research family justify a comparable successor, not an exact extension of the 2012 vintage.

Clean outputs: 706 book rows, 735 combined rows including 29 successor rows, and 706 overlap-diagnostic rows. The full current 1300-2023 input remains raw. The inset uses an enlarged y scale explicitly labeled with the same units, because a ~2-pound modern value is visually indistinguishable from zero on a 45,000-pound scale.

## Preservation and refresh

Raw CSV/JSON, source metadata, archived HTML, query results, URL/time/SHA log and clean observations are retained. SQLite indexes the per-plot clean paths and immutable versions. Refresh by downloading a new dated source, comparing overlap and metadata, and adding a separate version. Never overwrite the frozen legacy table. OWID legacy metadata identifies provider; the current indicator explicitly permits redistribution (CC BY 4.0). Attribute Fouquet, Pearson and OWID; source-owner publication PDF is linked, not copied into the release.
