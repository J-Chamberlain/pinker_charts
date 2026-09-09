# Figure 17-7 provenance

Original: **Cost of air travel, US, 1979-2015**, Supplemental Graphics PDF page 36, upper panel. Original crop inspected directly on 2026-09-09. Variables: annual US domestic travel cost per mile, constant 2015 dollars; checked baggage fees excluded. No plotted values digitized.

Citation chain: Pinker -> Derek Thompson, "How Airline Ticket Prices Fell 50 Percent in 30 Years (And Why Nobody Noticed)," The Atlantic, February 28, 2013 -> Airlines for America, annual domestic round-trip fares and fees -> US DOT DB1B ticket sample and Form 41 fee returns.

[Thompson article](https://www.theatlantic.com/business/archive/2013/02/how-airline-ticket-prices-fell-50-in-30-years-and-why-nobody-noticed/273506/) resolves the bibliography key. [A4A page](https://www.airlines.org/dataset/annual-round-trip-fares-and-fees-domestic/) is the cited institution, not a substitute source. Its 2017 archive and 2023 archive are retained in data/raw; they embed different Tableau workbook names, not static numeric tables. The 2017 page describes constant-2000 dollars, so reconstructing constant-2015 dollars requires documented CPI rebasing. Whether change fees enter the book series also needs confirmation.

No clean observations, transformation script or plot are claimed. Retained raw files are source-discovery evidence, not the underlying numerical dataset. See source_log and machine-readable downloads for exact responses, dates and hashes. Future numeric files must be preserved and ingested into the shared SQLite data library.
