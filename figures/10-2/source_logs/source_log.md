# Source Discovery Log: Figure 10-2

Figure title: Sustainability, 1955-2109

## PDF Reference

- Supplemental Graphics PDF page 13 inspected.
- Source line: Randall Munroe, XKCD, http://xkcd.com/1007/. Credit: Randall Munroe, xkcd.com.
- Surrounding text reviewed: Pinker uses the comic while discussing environmental pessimism and rebound/improvement claims.

## Sources Investigated

- xkcd comic page: https://xkcd.com/1007/ accepted as original visual/source page.
- xkcd JSON metadata: https://xkcd.com/1007/info.0.json accepted for title, image URL, transcript, and alt text.
- xkcd image: https://imgs.xkcd.com/comics/sustainable.png downloaded as original source visual.
- Google Books Ngram API, `sustainable`, corpus `en-US-2012`, smoothing 3: accepted as recovered book-era source data family named by xkcd.
- Google Books Ngram API, `sustainable`, corpus `en-US-2019`, smoothing 3: accepted only as successor extension data through 2019; 2020-2022 zero outputs were excluded as incomplete/invalid API tail values.
- Exact xkcd fitting formula: not located. The comic transcript states future anchors at 2036, 2061, and 2109, but does not publish the fitted line parameters.

## Search Queries/Checks

- xkcd 1007 sustainable Google Ngrams data sustainable
- Google Ngram Viewer API corpus 17 sustainable 1950 2008
- xkcd sustainable source Google NGrams Randall Munroe data
- Direct probes of `books.google.com/ngrams/json` with `en-US-2012`, numeric corpus `17`, and `en-US-2019`.

## Data Use Decision

No values were digitized from Pinker's plotted figure. The observed series comes from Google Ngram API responses. Future annotation anchors come from xkcd's own transcript and are labeled separately in the clean data.
