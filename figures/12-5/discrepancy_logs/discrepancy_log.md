# Figure 12-5 Discrepancy Log

Status: `partial_match`

Resolved discrepancy from the prior baseline:

- The earlier reconstruction under-matched the early-1970s peak because it used `Aviation accidents and fatalities by flight phase (ASN, 2019)`, a different ASN table whose metadata includes corporate jet and military transport accidents.
- The current reconstruction uses OWID's processed `Fatalities per million passengers` indicator, whose metadata documents the book formula: ASN annual fatalities divided by World Bank passengers, multiplied by 1,000,000.
- The current successor gives 1970 = 4.767405, consistent with the chapter text's `less than five in a million`.

Remaining discrepancy/blocker:

- Exact ASN 2017 data extraction and World Bank 2016b passenger vintage were not recovered. Current ASN/OWID/World Bank successor values are not silently treated as the book vintage.
- The 1972 ASN fatality spike is visible in the ASN annual sheet, but the World Bank passenger series used by OWID has no 1972 World observation, so the processed rate series jumps from 1971 to 1973. The book figure visually has a sharp early-1970s peak; current successor data reproduce that shape with a missing 1972 point.

Visual fidelity:

- Axis range and y-scale match the book: 1970-2015 and 0-7 deaths per million passengers per year.
- Typography and exact point placement are approximate; source-vintage uncertainty prevents verified reproduction.
