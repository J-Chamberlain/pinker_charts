"""Reconstruct Figure 15-3 from FBI hate-crime incident tables."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/15-3"
RAW = FIG / "data/raw/fbi_incidents_transcribed_from_tables.csv"
REF = ROOT / "references/figures/figure_15_3.png"
SERIES = ["Anti-black", "Anti-Jewish", "Anti-white", "Anti-Asian", "Anti-Islamic"]
COLORS = {"Anti-black": "#8e8c8c", "Anti-Jewish": "#898787", "Anti-white": "#242222", "Anti-Asian": "#d5d3d3", "Anti-Islamic": "#e5e3e3"}


def build_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    data = pd.read_csv(RAW)
    data = data[data.series.isin(SERIES)].sort_values(["series", "year"]).reset_index(drop=True)
    book = data[data.year.between(1996, 2015)].copy()
    successor = data[data.year >= 2016].copy()
    return book, successor


def draw(book: pd.DataFrame, successor: pd.DataFrame, output: Path, extended: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12.2, 7.2), dpi=180)
    for series in SERIES:
        group = book[book.series == series]
        ax.plot(group.year, group.incidents, color=COLORS[series], lw=3.0, label=series)
        if extended:
            ext = successor[successor.series == series]
            ax.plot(ext.year, ext.incidents, color=COLORS[series], lw=3.0, ls="--", label=f"{series} successor")
    if extended:
        ax.axvline(2015, color="#c6c6c6", lw=1.0, ls=":")
    ax.annotate("", xy=(2008, 2900), xytext=(2008, 3400), arrowprops={"arrowstyle": "-|>", "color": "#d1cfcf", "lw": 1.8})
    ax.text(1998.2, 3200, "Anti-black", fontsize=13.5, color="#242222")
    ax.text(1997.6, 1350, "Anti-Jewish", fontsize=13.5, color="#242222")
    ax.text(2005.2, 500, "Anti-white", fontsize=13.5, color="#242222")
    ax.text(1996.35, 430, "Anti-Asian", fontsize=13.5, color="#242222")
    ax.text(1996.3, 70, "Anti-Islamic", fontsize=13.5, color="#242222")
    ax.set_title("Figure 15-3: Hate crimes, US, 1996-2015", loc="left", fontsize=15)
    ax.set_xlabel("")
    ax.set_ylabel("Number of hate crime incidents", fontsize=12)
    ax.set_xlim(1996, 2017 if extended else 2015)
    ax.set_ylim(0, 4000)
    ax.set_xticks(range(1996, 2018 if extended else 2016))
    ax.set_yticks(range(0, 4001, 500))
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#626060")
    ax.spines["bottom"].set_color("#626060")
    ax.tick_params(colors="#3e3c3c", labelsize=9)
    note = "Source: FBI Hate Crime Statistics annual incident tables; 1996-2015 book period."
    if extended:
        note += " Dashed: official FBI successor tables for 2016-2017."
    else:
        note += " Labels and colors approximate the Supplemental PDF reference."
    fig.text(0.02, 0.018, note, fontsize=7.8, color="#555555")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def compare(recreated: Path, output: Path, title: str) -> None:
    ref, rec = mpimg.imread(REF), mpimg.imread(recreated)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=180)
    for axis, image, label in zip(axes, [ref, rec], ["Supplemental PDF reference", "Recreated"]):
        axis.imshow(image)
        axis.set_title(label, fontsize=10)
        axis.axis("off")
    fig.suptitle(title, fontsize=12)
    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_package(book: pd.DataFrame, successor: pd.DataFrame, book_plot: Path, extended_plot: Path) -> None:
    book.to_csv(FIG / "data/clean/figure_15_3_book_period.csv", index=False)
    successor.to_csv(FIG / "data/clean/figure_15_3_successor.csv", index=False)
    compare(book_plot, FIG / "plots/comparisons/figure_15_3_book_period_review.png", "Figure 15-3 book-period comparison")
    compare(extended_plot, FIG / "plots/comparisons/figure_15_3_extended_review.png", "Figure 15-3 extended comparison")
    (FIG / "README.md").write_text("""# Figure 15-3 - Hate crimes

Status: `updated_equivalent`. The FBI annual incident tables recover the five visible bias-motivation series for 1996-2015, with official FBI 2016-2017 successor tables shown dashed. Terminology and reporting participation changed over time, so this is not promoted to verified reproduction.

- Original: [../../references/figures/figure_15_3.png](../../references/figures/figure_15_3.png)
- Script: [../../scripts/reconstruct_15_3.py](../../scripts/reconstruct_15_3.py)
- Book comparison: [plots/comparisons/figure_15_3_book_period_review.png](plots/comparisons/figure_15_3_book_period_review.png)
- Extended comparison: [plots/comparisons/figure_15_3_extended_review.png](plots/comparisons/figure_15_3_extended_review.png)
""")
    (FIG / "captions/caption.txt").write_text("Figure 15-3: Hate crimes, US, 1996-2015. Counts are reported FBI hate-crime incidents by bias motivation. The book-period reconstruction uses official FBI annual reports for 1996-1999 and 2012-2015, with 2000-2011 counts from an ADL compilation of FBI tables; the 2000 anti-black value is corrected to 2,904 from the archived FBI Section II table because the ADL value of 3,884 created a false spike. Dashed lines in the extended panel use official FBI successor tables for 2016-2017. Reporting coverage and category terminology vary; these are reported incidents, not population-adjusted rates. Status: updated_equivalent.")
    (FIG / "provenance/provenance.md").write_text("""# Figure 15-3 provenance

## Original book source line

Federal Bureau of Investigation 2016b. The arrow points to 2008, the last year plotted in fig. 7-4 of Pinker 2011.

## Recovered source chain

- FBI Hate Crime archive: https://ucr.fbi.gov/hate-crime
- Official annual reports: `figures/15-3/data/raw/fbi_hate_crime_1996.pdf` through `fbi_hate_crime_1999.pdf`; archived 2000 Section II table: `fbi_cius_2000_section_2.pdf`
- Official Table 1 workbooks: `figures/15-3/data/raw/fbi_hate_crime_table_1_2012.xls` through `fbi_hate_crime_table_1_2017.xls`
- Intervening 2000-2011 compilation: `figures/15-3/data/raw/adl_fbi_hate_crime_comparison_2000_2020.pdf`
- Parsed/transcribed incident rows: `figures/15-3/data/raw/fbi_incidents_transcribed_from_tables.csv`

The plotted measure is the `Incidents` column, not offenses or victims. The five series are harmonized to the book's labels: anti-black, anti-white, anti-Asian, anti-Jewish, and anti-Islamic. The source tables contain reporting-participation and category-definition changes; no values were taken from the Pinker plot. The ADL compilation initially supplied an inconsistent 2000 anti-black value (3,884); the archived FBI Section II table reports 2,904 incidents, which is the value used here.

## Transformations

Rows are filtered to the five series, split into book period 1996-2015 and successor period 2016-2017, and plotted without normalization. No population adjustment or interpolation is applied.
""")
    (FIG / "source_logs/source_log.md").write_text("""# Figure 15-3 source discovery log

## Queries attempted

- `FBI 2016b hate crime 1996 2015 anti-black anti-white anti-jewish anti-asian anti-islamic incidents`
- `FBI hate crime annual table 1 1996 1997 1998 1999`
- `FBI hate crime table 1 2010 2011 2012 2013 2014 2015 download`
- `FBI hate crime successor data 2016 2017 table 1`
- `ADL FBI Hate Crime Statistics Comparison 2000-2020`
- `FBI Crime in the United States 2000 Section II Anti-Black 2904`

## Sources investigated

- FBI 1996-1999 annual PDFs - accepted as official historical source files.
- FBI 2012-2017 Table 1 workbooks - accepted as official machine-readable tables; 2016-2017 are used only as successor extension.
- ADL 2000-2020 comparison - accepted only as a transparent compilation for the 2000-2011 gap; official FBI endpoint years are preferred where available. Its 2000 anti-black value (3,884) was rejected after comparison with the archived FBI Section II table.
- FBI Crime in the United States 2000 Section II - accepted for the 2000 anti-black incident count (2,904), which removes the source-induced spike seen in the first visual pass.
- FBI Crime Data Explorer - investigated as a modern source, but the historical table archive was more directly aligned with the book's incident measure.

## Remaining uncertainties

- Exact source file/version used by Pinker is not byte-verified.
- 2000-2011 rows rely on an ADL compilation rather than separately archived FBI files in this package, except for the corrected 2000 anti-black row.
- FBI reporting participation and category names changed; apparent trend changes may partly reflect coverage.

## Recommended next steps

Recover the 2000-2011 FBI annual files individually and compare each incident count with the ADL compilation before promotion to `verified_reproduction`.
""")
    (FIG / "search_iterations/search_iterations.md").write_text("""# Search iterations

1. Inspected the Supplemental PDF and extracted the incident measure, five bias labels, and 2008 arrow.
2. Located official FBI annual PDFs for 1996-1999 and verified Table 1 incident rows.
3. Located official FBI Table 1 workbooks for 2012-2017.
4. Located an ADL compilation of FBI incident counts for 2000-2020 and transcribed the 2000-2011 gap.
5. Compared the ADL 2000 anti-black value with the archived FBI Section II table; rejected the inconsistent ADL value and substituted the official 2,904 incident count.
6. Combined the five series without normalization, generated book-period and dashed successor plots, and inspected both comparisons.
""")
    (FIG / "anomaly_reviews/anomaly_review.md").write_text("""# Anomaly review

Minor: line colors, labels, and annotation placement are approximated from the reference. Major: 2000-2011 values are from an ADL compilation of FBI tables rather than individually archived FBI files in this package; the ADL 2000 anti-black value was rejected in favor of the official archived FBI value of 2,904 after the first visual pass exposed a false spike. Major: participation and bias-category reporting changed over time, so the apparent trend is not a controlled population rate. The official FBI 2016-2017 extension is clearly dashed and separated.

Status: `updated_equivalent`.
""")
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text("""# Discrepancy log

The recreated lines match the reference's large anti-black series, roughly stable anti-Jewish series, lower anti-white/anti-Asian series, and 2001 anti-Islamic spike. The first pass showed an artificial anti-black spike in 2000 because the ADL compilation reported 3,884; the archived FBI Section II table reports 2,904 and is now used. The remaining unresolved discrepancy is source coverage: the package still mixes official FBI tables with an ADL compilation for most of 2000-2011, and reporting participation/category definitions are not constant. The 2016-2017 successor is dashed rather than visually merged into the book period.
""")
    (FIG / "review_checklist.md").write_text("""# Review checklist

- [x] Original Supplemental PDF figure inspected
- [x] Title, source note, measure, labels, and arrow year extracted
- [x] Official FBI source family resolved
- [x] Historical and successor raw files saved
- [x] Five incident series reconstructed without digitization
- [x] Book-period plot generated
- [x] Official successor extension generated and dashed
- [x] Both comparisons generated and inspected
- [x] Source gap and reporting coverage caveats documented
- [ ] Individually recover FBI annual files for 2000-2011
- [ ] Byte-verify the exact FBI 2016b release used by the book
""")
    lineage = {"schema_version": 1, "figure_id": "15-3", "book_citation": "Federal Bureau of Investigation 2016b", "raw_source": "figures/15-3/data/raw/fbi_incidents_transcribed_from_tables.csv", "script": "scripts/reconstruct_15_3.py", "mappings": [{"role": "book_period", "raw_inputs": ["figures/15-3/data/raw/fbi_hate_crime_1996.pdf", "figures/15-3/data/raw/fbi_hate_crime_1997.pdf", "figures/15-3/data/raw/fbi_hate_crime_1998.pdf", "figures/15-3/data/raw/fbi_hate_crime_1999.pdf", "figures/15-3/data/raw/fbi_cius_2000_section_2.pdf", "figures/15-3/data/raw/adl_fbi_hate_crime_comparison_2000_2020.pdf", "figures/15-3/data/raw/fbi_hate_crime_table_1_2012.xls", "figures/15-3/data/raw/fbi_hate_crime_table_1_2013.xls", "figures/15-3/data/raw/fbi_hate_crime_table_1_2014.xls", "figures/15-3/data/raw/fbi_hate_crime_table_1_2015.xls"], "selection": "Incidents by five bias motivations, 1996-2015", "transformation": "harmonize labels; retain incident counts", "clean": "figures/15-3/data/clean/figure_15_3_book_period.csv", "plot": "figures/15-3/plots/figure_15_3_book_period.png"}, {"role": "extension", "raw_inputs": ["figures/15-3/data/raw/fbi_hate_crime_table_1_2016.xls", "figures/15-3/data/raw/fbi_hate_crime_table_1_2017.xls"], "selection": "Same five incident categories, 2016-2017", "transformation": "plot official successor rows as dashed", "clean": "figures/15-3/data/clean/figure_15_3_successor.csv", "plot": "figures/15-3/plots/figure_15_3_extended.png"}]}
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    record = {"figure_id": "15-3", "title": "Hate crimes, US, 1996-2015", "scientific_status": "updated_equivalent", "artifact_kind": "reconstruction", "publication_status": "not_reviewed", "execution_status": "processed", "lifecycle_stage": "visual_review", "next_action": "Recover official FBI annual files for 2000-2011 and compare against the ADL compilation.", "notes": "Incident counts; official FBI endpoints and successor, ADL compilation for 2000-2011.", "extension": {"status": "successor", "label": "Official FBI successor tables 2016-2017"}, "visual_review": {"status": "pending", "reference_basis": "original", "issues": ["mixed source packaging", "reporting coverage changes", "category terminology changes"]}, "artifacts": {"metadata": {"path": "figures/15-3/figure.json", "self": True}, "original_reference": {"path": "references/figures/figure_15_3.png"}, "book_period_reconstruction": {"path": "figures/15-3/plots/figure_15_3_book_period.png"}, "extended_reconstruction": {"path": "figures/15-3/plots/figure_15_3_extended.png"}, "book_period_clean": {"path": "figures/15-3/data/clean/figure_15_3_book_period.csv"}, "successor_clean": {"path": "figures/15-3/data/clean/figure_15_3_successor.csv"}, "book_period_comparison": {"path": "figures/15-3/plots/comparisons/figure_15_3_book_period_review.png"}, "extended_comparison": {"path": "figures/15-3/plots/comparisons/figure_15_3_extended_review.png"}, "caption": {"path": "figures/15-3/captions/caption.txt"}, "provenance": {"path": "figures/15-3/provenance/provenance.md"}, "source_log": {"path": "figures/15-3/source_logs/source_log.md"}, "anomaly_review": {"path": "figures/15-3/anomaly_reviews/anomaly_review.md"}, "discrepancy_log": {"path": "figures/15-3/discrepancy_logs/discrepancy_log.md"}, "review_checklist": {"path": "figures/15-3/review_checklist.md"}, "lineage": {"path": "figures/15-3/lineage/lineage.json"}, "reconstruction_script": {"path": "scripts/reconstruct_15_3.py"}}}
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")


def main() -> None:
    book, successor = build_data()
    book_plot = FIG / "plots/figure_15_3_book_period.png"
    extended_plot = FIG / "plots/figure_15_3_extended.png"
    draw(book, successor, book_plot, extended=False)
    draw(book, successor, extended_plot, extended=True)
    write_package(book, successor, book_plot, extended_plot)
    print(json.dumps({"figure": "15-3", "book_rows": len(book), "successor_rows": len(successor)}, indent=2))


if __name__ == "__main__":
    main()
