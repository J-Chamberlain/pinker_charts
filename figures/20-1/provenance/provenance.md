# Figure 20-1 provenance

## Book evidence

- Title: `Populist support across generations, 2016`.
- Source note: Trump uses Edison Research exit polls reported by the New York Times (2016); Brexit uses Lord Ashcroft Polls reported by BBC News Magazine on June 24, 2016; European populist parties (2002-2014) use Inglehart & Norris 2016, Figure 8. Each birth cohort is plotted at the midpoint of its range.
- Stored reference: `references/figures/figure_20_1.png`.

## Source chain

`Enlightenment Now Figure 20-1` -> `Edison Research / National Election Pool 2016 exit poll` for Trump; `Lord Ashcroft EU Referendum poll` for Brexit; `Inglehart & Norris (2016), Figure 8` -> `ESS1-6 European Social Survey Cumulative File Rounds 1-6` for European populist-party support.

The Inglehart-Norris working paper is retained at `data/raw/inglehart_norris_2016.pdf`. Its Figure 8 source line identifies the ESS1-6 cumulative file, but the PDF does not provide the underlying cohort values in a table. ESS documentation states that the cumulative file is generated through the ESS Data Download Wizard and requires a registered user account.

The Lord Ashcroft full tables are retained at `data/raw/lord_ashcroft_eu_referendum_full_tables_2016.pdf`. The public Cornell Roper summary of the Edison/NEP exit poll is retained at `data/raw/roper_2016_exit_poll_age_table.html`.

## Blocker

The essential European series is not locally available. The paper graph is not used as numeric input. An authorized ESS account or an author-provided extract is required before any legitimate plot can be made.
# Current provenance, September 11

See ../remediation_2026_09_11.md and scripts/reconstruct_20_1.py. Two recovered
poll tables now generate 10 clean rows and a partial reconstruction. Original
reference -> source note -> Ashcroft page5/Roper AGE -> parser -> clean CSV ->
book-period plot -> real comparison. No invented European data or extension.
The earlier no-reconstruction statement below is historical.
