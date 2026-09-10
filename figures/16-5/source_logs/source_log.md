# Figure 16-5 discovery log

Original figure and citation: [provenance](../provenance/provenance.md).
September 9 local / 10 UTC, 2026. Download successes/failures and exact URLs:
[downloads.json](downloads.json).

Queries:
- Pietschnig Voracek 2015 One Century Global IQ gains supplemental material data
- site:sage.figshare.com "One Century" "IQ"
- "Pietschnig" "Voracek" "2015" "supplement" data xls
- "Pietschnig" "Voracek" "Supplemental Material" filetype:pdf
- "1745691615577701" "suppl"
- "Pietschnig" "Voracek" "Flynn" "2025" meta analysis data
- Local pinned OWID tree: Pietschnig, Voracek, IQ gains.
- Public Figshare GET /v2/articles?resource_doi=10.1177/1745691615577701
  and POST /v2/articles/search with title and limit 10: both 200, empty arrays.

Investigated:
1. [Sage article](https://journals.sagepub.com/doi/abs/10.1177/1745691615577701)
   and [APS record](https://www.psychologicalscience.org/journals/perspectives/1745691615577701/):
   accept bibliographic identification. Local publisher retrieval 403. No bypass.
2. Sage supplemental URL and original Highwire /content/10/3/282/suppl/DC1:
   archived September 5, 2015 HTML retrieved but is access/login page. Reject as
   data. Wildcard CDX for current supplement path: 503, not proof of absence.
3. OWID numeric Git dataset and metadata: ACCEPT fullscale regional column,
   July 2015 provider retrieval. Current topic redirects to homepage; April 2016
   archive confirms source association, retained with exact URL/hash.
4. SSRN author manuscript identifier 2404239 and ResearchGate author record:
   paper located, original supplemental numeric files not recovered. CiteSeer
   paper mirror web retrieval failed. None substituted for original supplement.
5. [2023 SPM meta-analysis](https://www.sciencedirect.com/science/article/abs/pii/S0160289623000314):
   different test/domain, not a compatible fullscale six-region extension.
6. [2025 Austrian pilot study](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1547520/full):
   selected occupational population, not compatible regional continuation.
7. University Vienna author records and 2025 conference abstract identify a
   new CHC-based 1909-2025 analysis. Promising targeted follow-up, but conference
   title alone is not a usable numeric release. No later values fabricated.

Next: original supplement S1-S5/sample weights and regional aggregation; obtain
the newer study's numeric release if published. Search is not claimed exhaustive.
