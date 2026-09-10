# Figure 17-3 provenance

Reviewed 2026-09-09 (America/Los_Angeles). Status: partial_match. Not publication-ready.

## Reference and citation chain

Original supplied Supplemental Graphics PDF, page 34 upper panel, visually inspected.
Title: Utilities, appliances, and housework, US, 1900-2015.
Short source note: Before 2005: Greenwood, Seshadri, & Yorukoglu 2005. Appliances,
2005 and 2011: US Census Bureau, Siebens 2013. Housework, 2015: Our World in Data,
Roser 2016t, based on American Time Use Survey, Bureau of Labor Statistics 2016b.
Surrounding book discussion is not in the graphics supplement; not claimed reviewed.

- Greenwood, Jeremy, Ananth Seshadri, and Mehmet Yorukoglu (2005), Engines of
  Liberation, Review of Economic Studies 72(1), 109-133.
  https://www.jeremygreenwood.net/papers/engines.pdf
- Original author dataset deposited at University of Rochester in 2004, linked by
  https://jeremygreenwood.net/research.htm and https://hdl.handle.net/1802/206.
  Download: https://urresearch.rochester.edu/fileDownloadForInstitutionalItem.action?itemFileId=152&itemId=127
  Retained byte-for-byte as data/raw/Engines.xls. Source sheet/row/columns retained in clean data.
- Its underlying sources (paper footnote 3): Vanek 1973 Table 1.1 (electricity);
  Lebergott 1993 Tables II.14/II.15 (water/toilets), II.20 (washer);
  Electrical Merchandising 1947 (dishwashers/refrigerators/vacuums);
  Burwell and Sweezy 1990 (microwaves). These underlying originals are not all recovered.
- Housework: Lebergott (1993), Pursuing Happiness: American Consumers in the
  Twentieth Century, Table 8.1, via paper p113/footnote 8. Numeric prose yields
  1900=58, 1975=18 hours/week. Intermediate data absent from Engines.xls.
  Extracted by regex from the original author's PDF, not manually read off a line.
- Julie Siebens (September 2013), Extended Measures of Well-Being: Living Conditions
  in the United States: 2011, P70-136, Table 3 p10.
  https://www2.census.gov/library/publications/2013/demo/p70-136.pdf
  Table extraction retains percentages and margins of error for all six listed years.
  Only 2005/2011 append to the author dataset, as in the book's source note.
- OWID working-hours 2016 source page archived in April 2016 and January 2017;
  its housework panel is a static image, not a numeric dataset. No pixel extraction.

## Reproduction and data reuse

Run `python scripts/reconstruct_17_3.py` offline from the repository root.
`recover_17_3_tables.py` regenerates retained numeric extracts with Poppler/pypdf;
it additionally needs the original paper in tmp/source_cache/greenwood_engines.pdf.
The full copyrighted paper is not redistributed. Its URL and SHA are in downloads.json.
All clean data retain original source numbers, units, and source identity.
No smoothing, extrapolation, forward-fill or rebasing. Straight plot segments between
observed appliance years are visual connectors, not annual estimated rows.
Housework has markers only; no invented trajectory.

## Source discrepancies

The original electric-range series stops at 1986; the Census series includes gas.
They must not be joined even though the book draws a continuous stove line.
The Census web page titled 2005 has 2011 link labels but its actual XLS contains
only 1992-2005. It also gives washer 84.0 in 2005 versus 84.2 in cited 2013 Table 3.
The cited publication takes precedence. Original workbook and Census last points
are not forced to 100 or moved to the book's approximate positions.

The original published housework level 58 is below the book's apparent initial
level; it is not shifted. Ramey (2009), Time Spent in Home Production in the
Twentieth-Century United States, JEH 69(1), 1-47, challenges Lebergott's early
estimation and describes a broader activity definition. This is a substantive
source dispute, not grounds to substitute her series silently.
https://econweb.ucsd.edu/~vramey/research/Home_Production_published.pdf
Web text inspected; direct download failed TLS validation (recorded, not disabled).

## Extension

Original BLS A-1 PDFs already retained by Figure 17-6 were reused, not downloaded again.
URLs/dates/checksums are in that figure's source log. Extracted three activities,
three sex categories, 2015-2025 except unavailable annual 2020. Weekly = daily * 7.
Women age 15+ broad household activities gives 15.61 hours in 2015; this is a
plausible book endpoint, not a proven identification. The core cleaning/laundry
plus meals definition is different again. Candidates appear only in the diagnostic.
No comparable extension is claimed, and no cross-population join is made.

Current OWID technology CSV redirects to a mixed-source series. Washer/dishwasher/
stove have no post-2011 update; some refrigerator/microwave series reach 2017 but
are not yet version-harmonized. AHS 2023 definitions also differ (private equipment,
restricted microwave questions, no countertop dishwashers). Not appended blindly.
https://www2.census.gov/programs-surveys/ahs/2023/2023%20AHS%20Definitions.pdf

## Rights and remaining work

US-government tables are retained; author workbooks contain factual numeric data
but no clear general redistribution license. Check publication rights before a
public download site; this research retention does not declare a license.
Recover Lebergott Table 8.1 and Pinker's final assembly, resolve the ATUS population
and activity basket, then replace markers with legitimate observed history.
