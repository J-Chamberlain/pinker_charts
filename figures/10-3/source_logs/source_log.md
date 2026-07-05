# Source Discovery Log: Figure 10-3

Figure title: Pollution, energy, and growth, US, 1970-2015

## Primary Reference
- Supplemental Graphics PDF page 13: figure image and source line inspected. Kindle was not needed because the PDF contains the source note and surrounding text.

## Source Line Captured
- Sources: US Environmental Protection Agency 2016, based on BEA GDP, FHWA vehicle miles traveled, US Census population, US Department of Energy energy consumption, US Greenhouse Gas Inventory CO2, and EPA air-pollutant emissions trends data.

## Source Recovery
- Located EPA Our Nation's Air 2016 live report: `https://gispub.epa.gov/air/trendsreport/2016/`.
- The report text states that by 2015 aggregate emissions of six common pollutants dropped 71 percent since 1970 while growth indicators rose.
- Located `dist/js/etrends.js`; the source code labels the chart block `Growth Chart - manual data entry (not csv load); custom markers` and contains the plotted series arrays.
- Copied the source JS and extracted those EPA-authored arrays to `data/raw/epa_2016_growth_chart_manual_values.csv`.
- Located EPA Our Nation's Air 2025 successor CSV at `data/naaqs/emissions/growth_chart_data.csv` for post-2015 extension.

## Search Queries / Checks
- EPA 2016 GDP vehicle miles traveled population energy consumption CO2 emissions 1970 2015 air pollutant emissions trends data.
- EPA Our Nation's Air 2016 Comparison of Growth Areas and Emissions.
- Searched 2016 EPA source code for `GrowthAndEmissions`, `growthChart`, `GDP`, and CSV references.
- Checked direct CSV path candidates before confirming the 2016 chart is manual-data-entry in JavaScript.

## Rejected / Not Used
- Pinker/Supplemental PDF plotted values: not digitized and not used as data.
- Separate BEA/FHWA/Census/DOE/EPA recomputation: unnecessary for book-period reconstruction because the EPA 2016 chart data were recovered directly.

## Remaining Uncertainties
- The PDF's visible label says five pollutants, but the recovered EPA chart labels the line as six common pollutants. The source note's parenthetical list omits lead while EPA's source chart includes lead.
- The 2025 extension is a successor source with revised values and `NA` CO2 for 2023-2024; it is not a continuation of the 2016 embedded table.
