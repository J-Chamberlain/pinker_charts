# Figure 12-5 Anomaly Review

Status: `partial_match`

Editorial self-review:

- Source recovery: partial. The closest verifiable successor is identified and preserved, but the exact ASN 2017 extraction is not.
- Data fidelity: clean data are a direct filter/rename of the recovered OWID successor CSV. No values are invented or digitized.
- Visual fidelity: the new plot matches the book axes and early-1970s magnitude better than the previous flight-phase proxy, but cannot be labeled verified because the source vintage differs.
- Extension quality: a dashed 2016-2022 segment is included only in the extended artifact because OWID metadata documents the same ASN/World Bank source family. It is labeled successor, not book-period evidence.
- Status calibration: keep `partial_match`; do not promote to `verified_reproduction`.

Reviewer challenge:

- Pinker would likely ask for the 2017 ASN export used at production time.
- A data journalist would ask why 1972 is missing in the rate series; the answer is absent World Bank passenger data for 1972 in the OWID/WDI series.
- A peer reviewer would ask whether current ASN revisions changed 1970-2015 values; this remains possible and is why the figure is not verified.
