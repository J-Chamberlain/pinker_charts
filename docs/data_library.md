# Reusable Data And Refreshes

The [Pinker Data Library](../data/database/README.md) is the single entry point
for finding and reusing saved data. Its SQLite file holds clean observations,
versioned snapshots, provenance metadata and references to raw downloads.
The JSON catalog reports coverage without equating archived files with accepted
reconstruction inputs.

Every future figure package must preserve:

- The exact original source download, with URL, provider, date, license and hash.
- Clean data for the book-period reconstruction and any distinct extension.
- A machine-readable mapping from each plot to its exact clean-data version,
  transformation script and raw-source versions.
- Units, geography, variable definitions, missing-value rules and transformations.
- A refresh policy: frozen historical release, comparable continuation, revised
  successor or unavailable. Record the retrieval adapter when one is implemented.

For older figures, backfill these fields from code and provenance evidence.
Do not infer use solely from filenames; wrong vintage, unused proxies and
diagnostic tables must remain identifiable. Reconcile the known Figure 10-6
clean-table/anchor discrepancy before claiming complete per-plot lineage.

After a data or canonical metadata change, run the database builder and checker,
review differences, then commit the files together. Data updates never overwrite
the frozen book reconstruction automatically. The database builder itself is
offline; source-download automation is a separate adapter responsibility.

## API Review Is Optional Infrastructure

"Paid calibration" referred to testing whether a separately invoked model reviewer
catches known scientific/visual mistakes. It is not model training, buying data,
or a prerequisite for local data preservation, reconstruction or visual inspection.
The unattended orchestrator uses an API to invoke a reviewer programmatically;
working directly in this Codex task does not require that additional API path.

Use deterministic data checks and actual visual inspection throughout the project.
Independent scientific review remains an acceptance requirement, but the API-based
reviewer is one implementation option, not the objective of the project. An API
budget gates only paid orchestration, not in-session research or the data library.
