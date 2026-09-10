# Figure 12-6 source discovery log

## Queries attempted

- `National Safety Council 2016 Injury Facts deaths falls fire drowning poison 1903 2014`
- `site:nsc.org historical deaths by cause data table`
- `National Safety Council Injury Facts historical rate table 1903 1998`
- `Injury Facts deaths by cause download Excel`

## Sources investigated

- NSC current Historical Trends: Deaths by Cause page (https://injuryfacts.nsc.org/all-injuries/historical-preventable-fatality-trends/deaths-by-cause/) - accepted as the canonical same-institution successor because it exposes a downloadable workbook with both historical and current rate tables.
- Public NSC Google Sheets workbook (https://docs.google.com/spreadsheets/d/e/2PACX-1vTb9UjML1Yir8rH9mAenZMkOzjWF1RVcaUQHMgbF1p8DnbR_XCoj7yarNpAiV-C7dWOtacstCqg9v5Y/pub?output=xlsx) - accepted and saved under `data/raw/`; it contains the needed categories and year ranges.
- Search result reproducing an Injury Facts 2016 table - rejected as a secondary mirror because the official NSC workbook was available.

## Remaining uncertainties

The exact 2016 workbook binary was not recovered, so historical values are accepted as same-institution continuation rather than an exact archival copy. ICD and category breaks are present in the workbook and are not harmonized. The original figure's line-rendering choices and the source's reporting-artifact rationale are followed where documented.

## Recommended next steps

Locate an archived NSC 2016 workbook or scan and byte-compare its rate sheets against the current historical rows. Confirm the exact 2016 values for the 1999-2014 segment before considering promotion to `verified_reproduction`.
