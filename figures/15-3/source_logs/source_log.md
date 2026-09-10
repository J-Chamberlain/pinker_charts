# Figure 15-3 source discovery log

## Queries attempted

- `FBI 2016b hate crime 1996 2015 anti-black anti-white anti-jewish anti-asian anti-islamic incidents`
- `FBI hate crime annual table 1 1996 1997 1998 1999`
- `FBI hate crime table 1 2010 2011 2012 2013 2014 2015 download`
- `FBI hate crime successor data 2016 2017 table 1`
- `ADL FBI Hate Crime Statistics Comparison 2000-2020`
- `FBI Crime in the United States 2000 Section II Anti-Black 2904`

## Sources investigated

- FBI 1996-1999 annual PDFs - accepted as official historical source files.
- FBI 2012-2017 Table 1 workbooks - accepted as official machine-readable tables; 2016-2017 are used only as successor extension.
- ADL 2000-2020 comparison - accepted only as a transparent compilation for the 2000-2011 gap; official FBI endpoint years are preferred where available. Its 2000 anti-black value (3,884) was rejected after comparison with the archived FBI Section II table.
- FBI Crime in the United States 2000 Section II - accepted for the 2000 anti-black incident count (2,904), which removes the source-induced spike seen in the first visual pass.
- FBI Crime Data Explorer - investigated as a modern source, but the historical table archive was more directly aligned with the book's incident measure.

## Remaining uncertainties

- Exact source file/version used by Pinker is not byte-verified.
- 2000-2011 rows rely on an ADL compilation rather than separately archived FBI files in this package, except for the corrected 2000 anti-black row.
- FBI reporting participation and category names changed; apparent trend changes may partly reflect coverage.

## Recommended next steps

Recover the 2000-2011 FBI annual files individually and compare each incident count with the ADL compilation before promotion to `verified_reproduction`.
