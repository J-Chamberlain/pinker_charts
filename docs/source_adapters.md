# Source Adapters

Reusable retrieval strategies for institution-specific source recovery.

## World Bank

Use both indicator-level API exports and historical bulk WDI ZIPs. Current
indicator APIs may revise historical values, so archived bulk releases can be
more faithful to book-period figures.

For Figure 10-6, the accepted source is an archived WDI bulk ZIP captured by
the Internet Archive on 2017-10-12.

Checks:

- Indicator codes.
- `WLD` country rows.
- Year coverage.
- Source metadata vintage.
- Revisions between archived and current WDI.

## UNCTAD

UNCTAD sources may appear as live API endpoints, web tables, annual reports,
or retired statistical products. Treat current API results as candidates until
their overlap values match the book-period scale.

Checks:

- Cargo type codes.
- Loaded versus unloaded measures.
- Geography and aggregation.
- Unit scale.
- Whether the endpoint is a successor to a retired table.

## ITOPF

ITOPF charts can combine spill incidents with tanker trade or oil shipped by
sea. Public pages may cite institutional sources while not exposing the exact
chart data. Archive ITOPF pages and source notes, then trace their cited data
institutions.

Checks:

- Spill-size threshold.
- Annual versus decadal aggregation.
- Whether the data includes tanker spills only.
- Current chart source notes versus historical source notes.

## Our World In Data

OWID can provide clean CSVs and historical grapher assets, but snapshots may
move or be replaced. Search live grapher CSVs, archived pages, GitHub mirrors,
and commit history when a chart is cited through OWID/Roser.

Checks:

- Slug history.
- Data package metadata.
- Grapher CSV vintage.
- GitHub repository history.

## Academic Literature

Academic papers are often bibliographic bridges rather than the final dataset.
Look for appendices, supplementary files, replication packages, journal data
deposits, author pages, and university repositories.

Checks:

- Supplement availability.
- DOI landing pages.
- Dataverse, OSF, Zenodo, institutional repositories.
- Whether the paper cites institutional data downstream.

## Journal Supplements

Journal websites can reorganize supplements over time. Capture landing pages,
file names, checksums, and archive URLs. Prefer original supplements over
third-party mirrors when both exist.

## Internet Archive

Use the Internet Archive for historical data releases, retired CSV endpoints,
and source pages. Record capture timestamp and whether the URL uses `id_` mode
for raw file download.

Checks:

- CDX search results.
- Capture date relative to book publication.
- File checksum.
- Whether redirects changed the downloaded content.

## GitHub Historical Repositories

GitHub can preserve historical data snapshots and generated chart assets. Search
repository history, tags, releases, and raw file paths. Do not assume the
current default branch reflects the book-period source.

Checks:

- Commit date.
- File path history.
- Release archives.
- Mirrors versus source repositories.
