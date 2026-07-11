# Source Discovery Log: Figure 19-1

Figure title: Nuclear weapons, 1945-2015

Original book citation: HumanProgress static 2927, based on Federation of Atomic Scientists, Kristensen & Norris 2016a, updated in Kristensen 2016.

The repository does not contain the Supplemental Graphics PDF, and targeted web search did not locate a public copy. The canonical Kindle chart-page crop was therefore inspected directly. It supplies the full figure, source note, and note that counts include deployed and stockpiled weapons but exclude retired weapons awaiting dismantlement. No additional surrounding book prose is present in the crop; the archived FAS page supplies corroborating explanation of the Cold War peak and subsequent decline.

## Search Queries Attempted
- "Figure 19-1" Kindle search
- "Nuclear weapons, 1945-2015" Our World in Data dataset
- "Nuclear weapons, 1945-2015" historical CSV
- "HumanProgress static 2927, based on Federation of Atomic Scientists, Kristensen & Norris 2016a, updated in Kristensen 2016."
- Internet Archive and successor dataset checks

## Sources Investigated
- Kindle search/page capture: accepted for title, citation, and visual reference where captured.
- Local OWID datasets mirror: accepted where it matched the named source chain or as a documented proxy.
- Current OWID grapher downloads: accepted only as successor/extension evidence.
- Internet Archive CDX returned captures of `humanprogress.org/static/2927` from 2015-2018. The 2016-08-14 replay was recovered and accepted.
- Actual Kindle chart-page crop: accepted during remediation as the visual reference for side-by-side review.
- Archived HumanProgress 2927 embedded `gon.countries` payload: accepted as the primary table for United States and USSR/Russia; 138 observations, all marked `generated: false`.
- Archived 2016 FAS “Status of World Nuclear Forces” and `warheadhistory.jpg`: accepted as corroboration of the institution, vintage, total-inventory context, and 2016 update, but not digitized as data.
- Current OWID nuclear-warhead grapher: accepted only for the six small-country layers. Its metadata attributes the series to FAS, but it remains a later revisable vintage.

## Remaining Uncertainties
- Status is `partial_match`.
- The exact minor-country values used for the Kindle cap are not exposed in the archived 2927 payload.
- No comparable post-2015 extension has been established, so none is plotted.

## Recommended Next Steps
- Search for a machine-readable 2016 FAS all-country history to replace the disclosed successor-vintage cap.
- Retain `partial_match` until that narrow vintage issue is resolved.
