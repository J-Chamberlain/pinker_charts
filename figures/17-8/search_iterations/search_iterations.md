# Search iterations, 2026-09-09

Queries attempted (verbatim; results inspected selectively):

1. `site.data.worldbank.org indicator ST.INT.ARVL international tourism arrivals`
2. `site.unwto.org 2025 international tourist arrivals 1.52 billion 2024`
3. `World Bank WDI 2016 international tourism arrivals 1995 541000000`
4. `site.untourism.int 2026 barometer statistical annex international arrivals 2010 2025 excel`
5. `site.ourworldindata.org/grapher international tourist arrivals UNWTO 2025`
6. `site.ourworldindata.org/grapher "World" "tourist arrivals"`
7. `site.e-unwto.org "2024" "2019" "2016" world arrivals 2025 barometer statistical annex`
8. `"world tourism barometer" "January 2026" filetype:pdf "World" "2019"`
9. `"World Bank 2016e" "Pinker" tourism`

Archive queries, direct URLs and their complete responses are in
`source_logs/downloads.json` and `data/candidates/wdi_*cdx.json`.

Iteration 1: current WDI endpoint returned a materially different World series.
Iteration 2: relaxed an incorrect archive MIME filter; recovered 2016 WDI and
confirmed book-looking history, but no 2015 endpoint.
Iteration 3: January 2017 still missing 2015; May and October 2017 contain a
revised history. Preserve 2016 history and disclose later endpoint, partial status.
Iteration 4: rejected modern OWID country sum; found complete regional successor
data and an official recent World numeric table. Keep source breaks visible.
Iteration 5: actual visual comparison, source-version diagnostic, and reviewer
challenge documented in the anomaly review. No data fitted to the image.
