# Figure 16-4 source discovery

Figure: Female literacy, 1750-2014. Original source note and interpretation:
[provenance](../provenance/provenance.md). Search date: September 9 local / 10 UTC,
2026. Numeric requests, redirects, failures and hashes: [downloads.json](downloads.json).

## Queries Attempted

- Gregory Clark 2007 Farewell Alms literacy women men England 1750 table 179 data
- site.humanprogress.org "2101" literacy
- "Schofield" "1973" "1750" "literacy" data table
- site.ourworldindata.org "England" "Schofield"
- "humanprogress" "2101" literacy
- Schofield 1973 literacy 1750 1850 table women men pdf
- "1754-1844" "1839-1914" literacy
- "Schofield" "literacy" "1755" "37"
- "humanprogress.org" "Ratio of" "literate"
- "England" "literacy" "Schofield" "csv"
- "World Bank" "WDI" "2016" "archive" download
- "literacy" "Schofield" "1750" "61" "1850"
- "illiteracy" "1841" "1871" "1901" "males"
- "Dimensions of Illiteracy" "data" "download"
- Local pinned OWID Git tree: Schofield, literacy, illiteracy, Clark.

## Investigated Sources

1. [Clark author site](https://faculty.econ.ucdavis.edu/faculty/gclark/a_farewell_to_alms.html),
   [data index](https://faculty.econ.ucdavis.edu/faculty/gclark/data.html) and
   [supplement index](https://faculty.econ.ucdavis.edu/faculty/gclark/Farewell%20to%20Alms/afta%20-%20supplement.html):
   no listed literacy numeric download. Teaching Chapter10.pdf confirms Schofield
   citation and signature definition; not a numeric input.
2. Publisher DOI 10.1016/0014-4983(73)90026-0: subscriber full text; RePEc and
   EconPapers confirm publication. Targeted recovery remains justified.
3. OWID pinned Git dataset named Literacy in England by sex: downloaded CSV,
   README and datapackage. Only Houston 1640-1740 observations; rejected period
   and population. Exact Git URLs in download log.
4. Warwick CAGE 56.2011 Broadberry working paper: literacy figure cites Houston/
   Schofield, no recovered numeric table. Chipping Campden local-history paper
   explicitly derives its national graph from another graph; rejected as data.
5. NBER Floud/Harris c7429 and h0087: source chain and combined-sex trend,
   not female/male values. CORE mirror 403. Further Registrar-General tables
   may recover the later England segment.
6. LEM 2022-28 working paper: web fetch failed, local request certificate
   validation failed. Verification was not disabled. Not used.
7. HumanProgress /f1/2101, /static/2101, www variant and /fl/2101 archived near
   January 2017: 404. Exact f1 CDX gives empty list; wildcard CDX returned 503.
   This does not prove all archives unavailable. 2016 Women's Progress article
   locates related chart but not its numeric export; never digitized.
8. WDI bulk November 2016 archive already recovered for 17-8: ACCEPT two country
   series. WLD empty. WDI_Country.Region excludes aggregate entities from
   diagnostic available-country mean; diagnostic rejects this naive World proxy.
9. WDI current public API: ACCEPT separately revised country continuation;
   metadata and complete single-page all-country payload retained. No paid
   model API is involved.
10. Search previews of copied books, regional UK/Irish literacy studies and
    Wikimedia mirrors were not numerical inputs: either wrong population,
    no original numeric table, or secondary graph transcription.

## Next Steps

Recover Clark's Figure 9.3 numeric worksheet or Schofield p.445 original table
and Registrar-General sex-specific signature tables (1839-1914). Seek a more
specific HumanProgress archive or the author's table behind dataset 2101;
document averaging/interpolation before plotting World. Consult full Pinker
context. No author contact, purchase, or claim of exhaustive search made.
