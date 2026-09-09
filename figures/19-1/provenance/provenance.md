# Provenance: Figure 19-1

Book figure -> Kindle chart/source line -> archived HumanProgress payload and FAS successor evidence -> `scripts/reconstruct_5_1_5_2_8_4_19_1.py` -> generated plots.

Source note: HumanProgress static 2927, based on Federation of Atomic Scientists, Kristensen & Norris 2016a, updated in Kristensen 2016.

## Recovered primary source

- Archived page: `https://web.archive.org/web/20160814144251id_/http://humanprogress.org/static/2927`
- Local capture: `data/raw/humanprogress_static_2927_20160814.html`
- Extracted table: `data/raw/humanprogress_static_2927_recovered.csv`
- Archive capture date: 2016-08-14; recovered 2026-07-10.
- Embedded metadata identifies dataset `_id` 2927, title “Nuclear weapons stockpiles, United States and USSR/Russia,” source Hans Kristensen/Federation of American Scientists, update date 2015-08-07, and years 1945-2015.
- The embedded `gon.countries` object contains 138 non-generated observations: United States (1945-2015) and USSR/Russia (1949-2015). The reconstruction preserves all 138 values exactly; missing pre-1949 USSR/Russia years are structural zeros.

## Small-country layers and limitation

The Kindle figure also labels France, China, UK, Pakistan, India, and Israel. Those series are not present in the recovered HumanProgress payload. Their plotted values come from the current OWID grapher file, whose source is the same institution (FAS) but a later, revisable vintage. Missing years before each country first appears are treated as structural zeros. North Korea is excluded, matching the HumanProgress description and the Kindle labels. This disclosed hybrid cap is why status remains `partial_match`.

No post-2015 extension is plotted. A later FAS series is not assumed to be vintage-continuous with the recovered 2015 HumanProgress table.

## Bibliography resolution

The book source line resolves “Kristensen & Norris 2016a” to Hans M. Kristensen and Robert S. Norris, “Russian nuclear forces, 2016,” *Bulletin of the Atomic Scientists* 72(3), 125-134, DOI `10.1080/00963402.2016.1170359`. “Kristensen 2016” is the FAS “Status of World Nuclear Forces” web update by Hans M. Kristensen (with Robert S. Norris), archived in 2016; its `warheadhistory.jpg` is retained as corroborating visual evidence in the source log.
