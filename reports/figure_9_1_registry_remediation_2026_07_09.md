# Figure 9-1 Registry Remediation Evidence

Date: 2026-07-09

## Scope

Figure 9-1, *International inequality, 1820-2013*, is a partial source-recovery case. The recovered source-backed data cover only the OECD/IISH *How Was Life?* 2014 Chapter 11 Table 11.4 unweighted/between-country series for 1820-2000. The Milanovic population-weighted international inequality series through 2013, including Pinker's 2012-2013 personal-communication update, remains unrecovered as inspectable data.

No digitized chart substitutes were used, and the figure must not be marked fully reconstructed or verified.

## Protected CSV Registry Exception

`data/figure_registry.csv` was intentionally not modified in this remediation pass. The run-specific operating rules state that the orchestrator updates the CSV registry row after external review and that any diff touching `data/figure_registry.csv` is automatically rejected.

Existing CSV row retained as evidence:

```csv
9-1,Enlightenment Now,9,"International inequality, 1820-2013",,1820-2013,manual_review_needed,source_recovery_blocked_no_reconstruction,economic_historical_dataset,active_high,Codex,Recover OECD Clio Infra Moatsos et al. 2014 market household income Gini data and Milanovic 2012 weighted international inequality update through 2013.,Processed in Track C on 2026-06-30. Original Clio Infra/Moatsos and Milanovic personal-communication data were not recovered as inspectable files. No digitized chart values were used.
```

## JSON Mirror Update

`data/figure_registry.json` was updated for Figure 9-1 to align with `PROJECT_STATE.md` and `data/metadata/figure_metadata.csv`:

```json
{
  "figure_id": "9-1",
  "book": "Enlightenment Now",
  "chapter": "9",
  "title": "International inequality, 1820-2013",
  "page": "",
  "year_range": "1820-2013",
  "current_status": "manual_review_needed",
  "lifecycle_stage": "partial_source_recovery_manual_review_source_blocked_no_reconstruction",
  "confidence": "0.45",
  "disposition": "partial_source_recovered_weighted_series_blocked",
  "source_type_guess": "economic_historical_dataset",
  "priority": "active_high",
  "current_owner": "Codex",
  "next_action": "Recover the Milanovic 2012 population-weighted international inequality source table, including Pinker's 2012-2013 personal-communication update, before considering reconstruction or verification.",
  "notes": "Remediation 2026-07-09: partial source recovery only. OECD/IISH How Was Life? 2014 Chapter 11 Table 11.4 unweighted/between-country values were recovered for 1820-2000 and retained as a source-recovery diagnostic. The Milanovic population-weighted international inequality series through 2013 remains unrecovered as inspectable data. No digitized chart substitutes were used, and the figure is not fully reconstructed or verified."
}
```

## Clean CSV Validation

Clean recovered values file:

`figures/9-1/data/clean/figure_9_1_oecd_table_11_4_between_country_inequality.csv`

Read-only validation command:

```sh
python3 - <<'PY'
import csv
from pathlib import Path
path = Path('figures/9-1/data/clean/figure_9_1_oecd_table_11_4_between_country_inequality.csv')
expected = [(1820,16),(1850,23),(1870,32),(1890,38),(1910,44),(1929,49),(1950,55),(1960,54),(1970,56),(1980,56),(1990,56),(2000,54)]
with path.open(newline='') as f:
    rows = list(csv.DictReader(f))
actual = [(int(r['year']), int(r['gini_points'])) for r in rows]
indexes_ok = all(abs(float(r['gini_index']) - int(r['gini_points']) / 100) < 1e-12 for r in rows)
notes_ok = all('population-weighted Milanovic 2012/2013 line not recovered' in r['notes'] for r in rows)
print(f'rows={len(rows)}')
print(f'expected_sequence_match={actual == expected}')
print(f'gini_index_scaled_from_points={indexes_ok}')
print(f'milanovic_blocker_note_present_all_rows={notes_ok}')
print('actual_sequence=' + ';'.join(f'{y}:{g}' for y,g in actual))
PY
```

Validation output:

```text
rows=12
expected_sequence_match=True
gini_index_scaled_from_points=True
milanovic_blocker_note_present_all_rows=True
actual_sequence=1820:16;1850:23;1870:32;1890:38;1910:44;1929:49;1950:55;1960:54;1970:56;1980:56;1990:56;2000:54
```

Clean CSV contents:

```csv
year,gini_index,gini_points,series,source,notes
1820,0.16,16,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
1850,0.23,23,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
1870,0.32,32,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
1890,0.38,38,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
1910,0.44,44,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
1929,0.49,49,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
1950,0.55,55,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
1960,0.54,54,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
1970,0.56,56,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
1980,0.56,56,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
1990,0.56,56,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
2000,0.54,54,International inequality (unweighted/between-country),"OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.
```
