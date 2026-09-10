# Figure 12-7 source discovery log

## Queries attempted

- `occupational accident deaths 1913 1933 1980 source`
- `CDC Improvements in Workplace Safety 1900-1999`
- `BLS CFOI charts 1992-2005 rate`
- `BLS CFOI charts 1992-2016 rate FTE`
- `Pegula Janocha 2013 fatal work injuries`
- `OSHA timeline 40 year history 1970 fatality rate`

## Sources investigated

- CDC MMWR 1999: accepted for 1913=61, 1933=37, and NIOSH 1980=7.5/1995=4.3 source context.
- CDC MMWR 2001: accepted for the NTOF 1980-1997 methodology and 1980/1997 range.
- CDC Health, United States 2009: accepted for published 1995, 2000, 2001, 2004-2007 checkpoints.
- BLS CFOI archive 1992-2005 via CDC Stacks: accepted as a preserved BLS chart artifact; its PDF is image-heavy and values were transcribed from the official chart text available in search output.
- BLS CFOI archive 1992-2016 and BLS MLR chart: investigated as primary sources. Automated downloads from bls.gov returned Access Denied; the response pages are retained as `*.access_denied.html`, and the published chart values used here are explicitly marked as source transcription.
- OSHA 40-year timeline: citation resolved, but the archived page did not yield a machine-readable full series.

## Remaining uncertainties

The source line intentionally combines incompatible historical definitions. The 1970 value available from a BLS chart is 18.0 while the Pinker plot appears to use the OSHA-era estimate; exact OSHA timeline extraction and exact NCHS table 38 values for every year were not recovered.

## Recommended next steps

Use a browser/manual download of the BLS 1992-2016 archive and locate an archived OSHA timeline page. Compare all source-transcribed rows against those artifacts before any status promotion.
