# Source Recovery Report: Figure 5-2

Run date: 2026-07-09

Figure: Child mortality, 1751-2013

Status after this run: `partial_match`

## Book Evidence

The Supplemental Graphics PDF page 3 shows Figure 5-2 as a five-country line chart:
Sweden, Canada, South Korea, Ethiopia, and Chile. The y-axis is "Percentage of
children dying before the age of 5" from 0 to 50, and the x-axis is 1750-2020.
The caption title is "Figure 5-2: Child mortality, 1751-2013."

The source note reads: "Our World in Data, Roser 2016a, based on data from the
UN Child Mortality estimates, http://www.childmortality.org/, and the Human
Mortality Database, http://www.mortality.org/."

The surrounding chapter text says child mortality fell from roughly one in four
children in sub-Saharan Africa in the 1960s to less than one in ten in 2015, and
that the global rate fell from 18 percent to 4 percent.

The bibliography entry is:

Roser, M. 2016a. Child mortality. Our World in Data.
https://ourworldindata.org/child-mortality/.

## Recovered Source Trail

1. Supplemental Graphics PDF page 3 was rendered and inspected visually.
2. Wayback CDX confirms 2016 captures of `https://ourworldindata.org/child-mortality/`.
3. The 2016-04-23 archived OWID article was downloaded to
   `data/candidates/archive_searches/owid_child_mortality_20160423.html`.
4. In that archived article, the "Country by Country Decline in Child Mortality"
   section embeds old Chart Builder view 58:
   `http://ourworldindata.org/chart-builder/public/view/58`.
5. Wayback CDX confirms captures of Chart Builder view 58 in 2015:
   2015-08-27, 2015-09-07, 2015-10-01, 2015-10-12, and 2015-12-27. The archived
   HTML shells were downloaded, but the underlying dynamic data endpoint
   `data/config/58` was not captured in the CDX results checked in this run.
6. Later Wayback playback of view 58 redirects/migrates to
   `grapher/child-mortality-around-the-world`, but that slug is a UN regional
   child-mortality chart, not the five-country book chart.
7. Current OWID grapher metadata for `child-mortality` was downloaded to
   `data/raw/owid_current_child_mortality.metadata.json`; it identifies the
   current successor as a long-run Gapminder plus UN IGME series.

## Candidate Datasets Checked

The following OWID dataset candidates were recovered from `owid/owid-datasets`
and stored under `data/candidates/owid_datasets_candidates/`:

- `Child mortality estimates - Gapminder (2015)`: Gapminder v8, uploaded
  2015-10-18. Its metadata cites CME Info estimates, the Human Mortality
  Database, estimated Gapminder infant-mortality conversion, and extrapolated
  Gapminder estimates.
- `Child Mortality Rates (Selected Gapminder, v10) (2017)`: later selected
  Gapminder series, documented as using HMD and International Historical
  Statistics before 1950 and UNIGME from 1950-2016.
- `Child Mortality Estimates - CME Info (2018)`: UN IGME/CME Info country
  estimates, largely 1950 onward.

These candidates are source-family evidence, not an exact recovery of the
Pinker/Roser book dataset. The 2015 Gapminder candidate does not include
Sweden's 1751-1799 values. The UN/CME candidate cannot supply the pre-1950
historical segment. The 2017 selected Gapminder candidate is post-book and has
different coverage than the figure. The current OWID `child-mortality` grapher
matches the book coverage more closely, but its metadata is current and its
exact 2016 Chart Builder data payload was not recovered.

## Fidelity Assessment

The current reconstruction uses `https://ourworldindata.org/grapher/child-mortality.csv`
in percent units and trims country starts to match the visible book figure.
For the book-period CSV, the tolerance is exact equality to the downloaded
current OWID successor file after filtering and no unit conversion. This is not
a tolerance against the unrecovered Roser 2016a source.

The book-period reconstruction remains a partial visual match. It reproduces
the figure concept, axis scale, country set, and broad trajectories, but exact
source vintage and some label/curve placement differences remain unresolved.

## Extension Assessment

The dashed post-2013 extension uses the same current OWID successor grapher as
the book-period proxy. This is institutionally comparable as an OWID long-run
Gapminder/UN IGME successor, but it is not proof of the Roser 2016a book-period
dataset. No separate non-comparable extension was added in this run.

## Conclusion

The exact Roser 2016a Chart Builder data payload for the five-country figure was
not recovered. The strongest citable provenance trail now is:

Supplemental Graphics PDF page 3 -> Roser 2016a bibliography entry -> archived
OWID 2016 child-mortality article -> embedded Chart Builder view 58 -> recovered
OWID/Gapminder/UN IGME/HMD source-family candidates -> current OWID successor
grapher used as a documented partial-match proxy.

Do not describe Figure 5-2 as reconstructed, extended, or verified beyond
`partial_match` unless the old Chart Builder data/config or an equivalent
book-era OWID export is recovered.
