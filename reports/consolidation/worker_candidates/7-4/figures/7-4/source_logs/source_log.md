# Source Discovery Log: Figure 7-4

- Read Supplemental Graphics PDF page 6: title `Famine deaths, 1860-2016`; y-axis `Famine deaths per 100,000 people per decade`; source note cites OWID Hasell & Roser 2017.
- Recovered live OWID preservation page for `The Our World in Data Dataset of Famines`, which says the old dataset covers famine deaths from the 1860s through 2016 and is now outdated relative to WPF successor data.
- Recovered the linked Google Sheet event table with parsed `year_start` and `year_end` fields.
- Recovered 2018 Wayback page text for the original OWID famines topic page. The rate-chart footnote says to use the table, average upper/lower estimates, split straddling famines proportionately by years in each decade, and exclude missing/sub-1,000 death events.
- Recovered the archived static chart image `Famine-death-rate-since-1860s.png`.
- CDX searches for `death-rate-from-famines-by-decade` found captures only from 2025 onward; wildcard 2017-2018 grapher searches for famine charts found no decadal-rate grapher CSV.
- Transcribed the printed decadal-rate values from the archived static chart image for the canonical book-period clean data.
- Audited the transcription as exact integer label transcription from the static image; expected tolerance is 0 label units for transcription, with +/-0.5 only as the implied rounding tolerance against unrecovered continuous rates.
- Conclusion: the original source family, calculation rules, and plotted values are recovered from the static chart, but not a machine-readable 2017 decadal-rate output with denominator metadata.
