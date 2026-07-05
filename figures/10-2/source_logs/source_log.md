# Source Discovery Log: Figure 10-2

Figure title: Sustainability, 1955-2109

## Source Line
- Supplemental Graphics PDF page 13: Source: Randall Munroe, XKCD, http://xkcd.com/1007/. Credit: Randall Munroe, xkcd.com.
- XKCD page text identifies the internal source as Google Ngrams and describes the measure as the frequency of use of the word 'sustainable' in US English text, as a percentage of all words, by year.

## Search and Recovery
- Official XKCD page: https://xkcd.com/1007/
- Official XKCD image: https://imgs.xkcd.com/comics/sustainable.png
- Google Ngram American English 2009/v1 corpus query: https://books.google.com/ngrams/json?content=sustainable&year_start=1955&year_end=2008&corpus=5&smoothing=0
- Google Ngram American English 2012/v2 cross-check query: https://books.google.com/ngrams/json?content=sustainable&year_start=1955&year_end=2008&corpus=17&smoothing=0
- Google Ngram current en-US-2019 successor query: https://books.google.com/ngrams/json?content=sustainable&year_start=1955&year_end=2019&corpus=en-US-2019&smoothing=0

## Source Decision
- Accepted primary visual/source reference: Supplemental Graphics PDF page 13.
- Accepted original publication reference: official XKCD 1007 page and image.
- Accepted data source for reconstruction: Google Ngram American English 2009/v1 corpus (`corpus=5`), because the 2012 XKCD comic predates later Ngram revisions and the series matches the panel's order of magnitude.
- Accepted projection display method: a log-linear visual calibration fitted to the three XKCD labeled future points (2036, 2061, 2109). This keeps the projected line and future open circles internally consistent. The separate Ngram-data-only fit is retained only for quantitative comparison.
- Current successor data are used only in the extended artifact.

## Quantitative Candidate Comparison
- CSV: `figures/10-2/data/clean/figure_10_2_ngram_candidate_comparison.csv`
- Markdown: `figures/10-2/data/clean/figure_10_2_ngram_candidate_comparison.md`
- Marker audit: `figures/10-2/data/clean/figure_10_2_xkcd_calibrated_marker_values.csv`

## Blockers and Uncertainties
- XKCD does not publish a separate spreadsheet or the exact regression method for the hand-drawn extrapolation.
- The future points are satirical extrapolation labels, not observed data.
- The 2009/v1 Ngram data-only fit implies the once-per-page threshold in the mid-2040s, later than XKCD's 2036 label; this is documented in the candidate table rather than hidden in the recreated geometry.
- No plotted values were digitized from the Pinker/Supplemental PDF figure.
