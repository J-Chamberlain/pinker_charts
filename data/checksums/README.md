# Checksums

- `repository_import_sha256sums.txt` covers imported repository artifacts,
  excluding itself.
- Per-figure checksum files live in `figures/<id>/checksums/`.
- `raw_file_checksums.*` are legacy checksum exports from the local proof of
  concept and may reference files that were intentionally not imported.

## Intentionally Not Imported

The local proof-of-concept directory contained transient caches, nested cloned
repositories, and very large bulk downloads. These were not imported as Git
objects:

- `data/repositories/`: nested repository mirrors and generated thumbnails.
- Python bytecode caches.
- `current_WDI_CSV.zip`: large current World Bank bulk download used as a
  diagnostic candidate. The accepted Figure 10-6 book-period source is the
  archived WDI ZIP stored under `figures/10-6/data/raw/`.

When a non-imported artifact is needed, recover it from the URL, archive URL,
or notes in the relevant source log.
