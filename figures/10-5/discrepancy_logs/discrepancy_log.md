# Discrepancy Log: Figure 10-5

Last updated: 2026-07-09

## Current Discrepancies

- Exact source version: Roser 2016r / OWID historical data snapshot was not recovered as an archived CSV or data bundle.
- Gray-line source data: the annual UNCTADStat table for total crude oil, petroleum product, and gas loaded was not recovered.
- Current reconstruction input: the gray line is digitized from an archived ITOPF chart image, so it carries image-reading/calibration tolerance and is not original tabular data.
- Live UNCTADStat route: current `US.SeaborneTrade` version 2231 gives 2000-2016 values that do not match the ITOPF/RMT/book scale on overlap and omits 1970-1999.
- Extension: no post-2016 extension is plotted because no same-method annual successor for the oil-loaded line was recovered.

## Resolved Or Improved

- The Supplemental Graphics PDF source note and surrounding text were checked directly.
- The spill-count line is supported by current OWID/ITOPF annual data and agrees with the book's black line.
- An archived ITOPF 2016 statistics page and `seaborne_16.JPG` chart image were recovered from the Internet Archive.
- The archived ITOPF image matches the book's right-axis concept and line shape and cites UNCTADStat.
- The image-derived oil-loaded series was checked against UNCTAD RMT 2020 selected-year tanker-trade values: MAE 0.058 billion metric tons; maximum absolute difference 0.194.

## Search Hypotheses Still Open

- The original gray line may come from a retired UNCTADStat export/report version not exposed through the current API.
- OWID/Roser may have stored the oil-loaded values in an unpublished or unarchived figure-preparation file.
- ITOPF may have had an internal chart source table for the archived `seaborne_16.JPG` image.

## Editorial Disposition

Keep status at `partial_match`. The current book-period artifact is useful for visual comparison and source-family documentation, but it is not a verified reproduction from original annual data.
