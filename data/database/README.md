# Pinker Data Library

The data are a reusable research asset, not disposable chart inputs.

- **pinker_data.sqlite**: queryable clean CSV data, version history, per-figure
  metadata and a catalog of all retained per-figure data/supporting files.
- **catalog.json**: readable coverage counts for every figure, including gaps.
- Original downloads remain in `figures/<id>/data/raw/`; recovered/rejected
  candidates remain in `figures/<id>/data/candidates/`. Those folders and the
  plotting CSVs are not moved, overwritten or modified by this database builder.

Initial inventory: **75 figures, 321 retained files, 65 clean CSV tables,
34,968 rows**. These are file/row counts, not counts of accepted datasets or
completed figures. Some older tables are unused successors, diagnostics or
superseded outputs. No scientific status changed during this import.

## What Is In The Database?

| Table or view | Contents |
| --- | --- |
| `snapshots` | Import fingerprint, import time and repository HEAD at import |
| `figures` | Canonical figure metadata for each snapshot |
| `file_versions` | Repository path, SHA256, byte size, format, parse status, row count; exact compressed bytes for clean CSVs |
| `figure_files` | Figure/file links, storage category and declared use for each snapshot |
| `clean_rows` | Every clean CSV row, retaining its original column names and cell strings |
| `references_metadata` | Existing metadata/lineage JSON with citations, URLs and provenance where recorded |
| `current_files` | Files present at the most recent import |
| `current_clean_rows` | Queryable rows from the most recent import |

Source Excel, Stata, JSON, ZIP, PDF and raw CSV files are cataloged and remain
available in the repository; they are **not all converted into database rows**.
The database therefore supplements, rather than replaces, the original archive.
The compressed original clean CSVs permit exact exports, including their original
precision and missing-value encoding. No chart was digitized to populate it.

The builder deliberately does not guess units, normalize country definitions,
collapse source revisions or treat missing cells as zero. `values_json` retains
strings such as `001.250`, empty values and censored thresholds. Cast numeric
fields explicitly only after checking the field's meaning and missingness.

## Find And Query Data

No server, OpenAI API key or external service is required. Python includes SQLite.
From the repository root:

```bash
python scripts/build_data_database.py build
python scripts/build_data_database.py check
sqlite3 data/database/pinker_data.sqlite
```

Inside SQLite, list available clean data:

```sql
SELECT figure_id, repository_path, row_count, usage_status
FROM current_files
WHERE table_status = 'rows_imported'
ORDER BY figure_id, repository_path;
```

Example: query the preserved Figure 5-3 book-period table:

```sql
SELECT json_extract(values_json, '$.Entity') AS country,
       CAST(json_extract(values_json, '$.Year') AS INTEGER) AS year,
       CAST(NULLIF(json_extract(values_json, '$.maternal_mortality_percent'), '')
            AS REAL) AS maternal_mortality_percent
FROM current_clean_rows
WHERE repository_path = 'figures/5-3/data/clean/figure_5_3_book_period_clean.csv'
ORDER BY country, year;
```

Python/pandas users can run the same SQL with `pd.read_sql_query(sql, connection)`.
For an exact CSV copy, the existing CSV path is usually simplest. Historical
versions remain in `file_versions.original_csv_gzip`, decompressible with Python
`gzip.decompress`, with a checksum to verify the recovered bytes.

## Important Usage Labels

- `canonical_declared`: the current figure record explicitly lists this file.
  This is a declared link, not proof of scientific correctness or actual execution.
- `historical_or_unverified`: retained raw/clean data without an explicit canonical
  link. Do not silently assume it generated the current plot.
- `candidate_unverified`: retained candidate material, not approved by folder
  membership. Some historically used files also live here; that requires an
  explicit mapping rather than a blanket rejection or promotion.

Per-plot input mapping is still incomplete across older packages. In particular,
Figure 10-6 has legacy paths and a two-row clean table while historical metadata
describes three anchors. The database preserves and exposes that inconsistency;
it does not invent the missing row or certify the chart's lineage. Figure 5-3
has explicit canonical data/script links and separately retained old tables.

## Refresh Without Losing History

1. Keep book-era raw files and clean plotting data frozen. Do not overwrite a
   historical reconstruction with today's API response.
2. Save a new provider release at a new dated path under the figure's `data/raw/`
   directory. Record its exact URL, provider, indicator, release/retrieval date,
   license, checksum and any revised definitions in provenance/metadata.
3. Transform it into a separately versioned clean CSV. Record series, units,
   geography, denominator, source vintage and revision notes. Compare overlapping
   years before deciding whether it is a continuous extension or successor.
4. Update canonical input links only after the data and resulting plots pass
   review. Historical files remain available. Then regenerate project views.
5. Run `build` and `check` above and commit the new source, clean files, metadata,
   database and catalog together. A changed input creates a new snapshot;
   unchanged builds are idempotent. Previous clean rows/CSV bytes remain queryable.

`build` refreshes the **local database from saved files**. It does not download
new releases, alter plots or promote candidates. Automated provider refreshes
still need source-specific retrieval adapters and verified per-dataset mappings.
Some original datasets are static historical releases, not refreshable services.

## Integrity And Scope

The importer uses a single-writer lock, builds a temporary SQLite copy, validates
foreign keys and database integrity, rechecks source hashes, then atomically
replaces the database. Failed imports preserve the previous database. Validation
round-trips every imported clean row against its archived CSV bytes. Duplicate
headers and malformed rows are explicit parse errors, not silent truncation.

The repository commit records HEAD at import; hashes identify exact inputs even
when newly saved files have not yet been committed. Git plus dated source files
preserves raw-source history; raw bytes are not duplicated in this database.
Consolidation quarantine directories are intentionally outside the live-data
inventory. The database is a derivative index; original files and canonical
figure records remain authoritative. To preserve database snapshot history,
update the existing database rather than deleting it before a rebuild.
