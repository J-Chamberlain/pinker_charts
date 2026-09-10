"""Reconstruct Figure 15-2 from a current Google Trends historical export.

Google Trends is sampled and revised over time.  The raw response is saved
under the figure package; this script performs only the documented annual
aggregation and smoothing and never uses values digitized from Pinker's plot.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/15-2"
RAW = FIG / "data/raw/google_trends_monthly_2026-09-09.csv"
REF = ROOT / "references/figures/figure_15_2.png"

TERMS = {
    "Racist jokes": "nigger jokes",
    "Sexist jokes": "bitch jokes",
    "Homophobic jokes": "fag jokes",
}
COLORS = {"Racist jokes": "#8a8888", "Sexist jokes": "#d1cfcf", "Homophobic jokes": "#242222"}


def build_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(RAW, parse_dates=["date"])
    annual = raw.assign(year=raw.date.dt.year).groupby(["year", "term"], as_index=False).value.mean()
    annual["series"] = annual.term.map({v: k for k, v in TERMS.items()})
    # Pinker's note says monthly values were averaged by year and smoothed.
    # A centered 3-year mean is a transparent approximation of that smoothing.
    annual["percentage_of_peak"] = annual.groupby("series")["value"].transform(lambda s: s.rolling(3, center=True, min_periods=1).mean())
    data = annual[["year", "series", "term", "percentage_of_peak", "value"]].sort_values(["series", "year"]).reset_index(drop=True)
    book = data[data.year.between(2004, 2017)].copy()
    successor = data[data.year >= 2018].copy()
    return book, successor


def draw(book: pd.DataFrame, successor: pd.DataFrame, output: Path, extended: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12.2, 7.2), dpi=180)
    for series in TERMS:
        group = book[book.series == series]
        ax.plot(group.year, group.percentage_of_peak, color=COLORS[series], lw=3.0, label=series)
        if extended:
            ext = successor[successor.series == series]
            ax.plot(ext.year, ext.percentage_of_peak, color=COLORS[series], lw=3.0, ls="--", label=f"{series} successor")
    if extended:
        ax.axvline(2017, color="#c6c6c6", lw=1.0, ls=":")
    ax.text(2014.9, 37 if not extended else 34, "Sexist\njokes", fontsize=13.5, color="#242222")
    ax.text(2013.0, 15 if not extended else 13, "Racist jokes", fontsize=13.5, color="#242222")
    ax.text(2012.0, 5 if not extended else 5, "Homophobic jokes", fontsize=13.5, color="#242222")
    ax.set_title("Figure 15-2: Racist, sexist, and homophobic Web searches, US, 2004-2017", loc="left", fontsize=15)
    ax.set_xlabel("")
    ax.set_ylabel("Frequency of searches (percentage of peak month)", fontsize=12)
    ax.set_xlim(2004, 2026 if extended else 2017)
    ax.set_ylim(0, 90)
    ax.set_xticks(range(2004, 2027 if extended else 2018, 1))
    ax.set_yticks(range(0, 91, 10))
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#626060")
    ax.spines["bottom"].set_color("#626060")
    ax.tick_params(colors="#3e3c3c", labelsize=9)
    note = "Source: Google Trends exact-term US export; annual means of monthly 0-100 series, centered 3-year smoothing."
    if extended:
        note += " Dashed: current successor observations after 2017; Trends sampling and term availability changed."
    else:
        note += " Current export accessed 2026-09-09, not the book's 2017-01-22 export."
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
    for sub in ["data/clean", "plots/comparisons", "captions", "provenance", "source_logs", "search_iterations", "anomaly_reviews", "discrepancy_logs", "lineage", "checksums"]:
        (FIG / sub).mkdir(parents=True, exist_ok=True)
    book.to_csv(FIG / "data/clean/figure_15_2_book_period.csv", index=False)
    successor.to_csv(FIG / "data/clean/figure_15_2_successor.csv", index=False)
    compare(book_plot, FIG / "plots/comparisons/figure_15_2_book_period_review.png", "Figure 15-2 book-period comparison")
    compare(extended_plot, FIG / "plots/comparisons/figure_15_2_extended_review.png", "Figure 15-2 extended comparison")
    (FIG / "README.md").write_text("""# Figure 15-2 - Racist, sexist, and homophobic Web searches

Status: `partial_match`. A current Google Trends export is available and the annual aggregation/smoothing pipeline is reproducible, but the original January 22, 2017 Trends response cannot be recreated exactly. The two low-volume terms now have different historical availability and do not visually match the book-era curves closely enough for verification.

- Original: [../../references/figures/figure_15_2.png](../../references/figures/figure_15_2.png)
- Script: [../../scripts/reconstruct_15_2.py](../../scripts/reconstruct_15_2.py)
- Book comparison: [plots/comparisons/figure_15_2_book_period_review.png](plots/comparisons/figure_15_2_book_period_review.png)
- Extended comparison: [plots/comparisons/figure_15_2_extended_review.png](plots/comparisons/figure_15_2_extended_review.png)
""")
    (FIG / "captions/caption.txt").write_text("Figure 15-2: Racist, sexist, and homophobic Web searches, US, 2004-2017. Current Google Trends exact-term exports for the three cited search strings are averaged over each year and smoothed with a centered three-year mean. The extended panel shows the current export after 2017 as dashed. Google Trends is sampled and revised, and this current response is not the book's January 22, 2017 response; the low-volume sexist and homophobic series therefore remain a partial match. No Pinker chart values were digitized.")
    (FIG / "provenance/provenance.md").write_text("""# Figure 15-2 provenance

## Original book source line

Google Trends (www.google.com/trends), searches for the three terms cited in the figure, United States, 2004-2017, relative to total search volume. Data accessed Jan. 22, 2017 are by month, expressed as a percentage of the peak month for each search term, then averaged over the months of each year, and smoothed.

## Recovered source

- Google Trends: https://trends.google.com/trends/explore
- Query metadata and URLs: `figures/15-2/data/raw/google_trends_query_metadata.json`
- Raw current export: `figures/15-2/data/raw/google_trends_monthly_2026-09-09.csv`

Each term was queried separately for the United States from January 2004 through August 2026 so Google could scale each term to its own 0-100 peak. The saved response is a current export and is not an exact archival copy of the book's 2017 response.

## Transformations

Monthly 0-100 values were averaged by calendar year. A centered three-year rolling mean approximates the book's unspecified smoothing. Book-period rows are 2004-2017; 2018 onward is plotted as a dashed successor. No values were transcribed from the Pinker image.
""")
    (FIG / "source_logs/source_log.md").write_text("""# Figure 15-2 source discovery log

## Queries attempted

- `Google Trends nigger jokes bitch jokes fag jokes US 2004 2017`
- `Pinker Figure 15-2 Google Trends data`
- `Google Trends historical CSV export exact search term`
- `GitHub Google Trends nigger jokes bitch jokes fag jokes`
- `Google Trends post-2017 continuation exact terms`

## Sources investigated

- Google Trends Explore UI/API - accepted as the cited source family; current exact-term exports were retrieved separately for all three terms.
- Google Trends help documentation - accepted for the interpretation of 0-100 relative interest and comparison behavior.
- Academic and commentary references discussing Pinker's use of Google data - accepted only for context; rejected as data sources.
- GitHub search and public mirrors - no archival copy of the January 2017 three-series response was found.

## Remaining uncertainties

- Google Trends samples and revises historical results; current low-volume zeros are not evidence that the 2017 response contained zeros.
- The book's exact smoothing algorithm is unspecified.
- The original export may have used a different Trends data product, term interpretation, or query session.

## Recommended next steps

Search Internet Archive or a researcher-held export for the January 22, 2017 response. Compare the raw monthly values and reproduce the exact smoothing before promotion beyond `partial_match`.
""")
    (FIG / "search_iterations/search_iterations.md").write_text("""# Search iterations

1. Inspected the Supplemental Graphics PDF and extracted the exact three terms, geography, date range, access date, and transformation note.
2. Tested combined-term Trends retrieval; low-volume terms collapsed toward zero, so combined output was rejected.
3. Queried each exact term separately to preserve term-specific peak normalization.
4. Saved 2004-2026 monthly current export and query metadata.
5. Aggregated annual means and applied a transparent centered three-year smoothing approximation.
6. Inspected book-period and extended comparisons; racist trajectory is broadly similar, while sexist and homophobic trajectories differ materially from the original response.
""")
    (FIG / "anomaly_reviews/anomaly_review.md").write_text("""# Anomaly review

Major: current Trends data do not reproduce the original sexist and homophobic trajectories; both have zeros or low values in early years where the book shows substantial nonzero interest. This is consistent with a changed historical sample, query interpretation, or unavailable 2017 export, not with a reason to invent values.

Major: exact smoothing parameters are not specified in the book. Minor: annotation positions are approximated. The dashed extension is clearly separated after 2017 but is a modern Trends series, not a continuation of the original measurement vintage.

Status remains `partial_match`.
""")
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text("""# Discrepancy log

The current nigger-jokes series follows the reference's broad decline. The current bitch-jokes and fag-jokes series do not: current historical responses show zeros at the beginning of the period and later peaks, whereas the book's 2017 response shows nonzero early values and declining curves. This difference is source-version/availability related, not a plotting-scale issue. The extension is dashed after 2017 and is explicitly labeled as a current successor.
""")
    (FIG / "review_checklist.md").write_text("""# Review checklist

- [x] Original Supplemental PDF figure inspected
- [x] Title, source note, terms, access date, and transformation note extracted
- [x] Google Trends source family resolved
- [x] Current raw monthly exports saved
- [x] Query metadata and URLs saved
- [x] Annual aggregation and smoothing script written
- [x] Book-period reconstruction generated
- [x] Post-2017 successor extension generated and dashed
- [x] Both comparisons generated and inspected
- [x] No Pinker plotted values digitized
- [x] Source-version discrepancy documented
- [ ] January 22, 2017 raw export recovered
- [ ] Exact smoothing algorithm verified
- [ ] Sexist and homophobic trajectories reconciled
""")
    lineage = {
        "schema_version": 1,
        "figure_id": "15-2",
        "book_citation": "Google Trends, accessed Jan. 22, 2017",
        "raw_source": "figures/15-2/data/raw/google_trends_monthly_2026-09-09.csv",
        "script": "scripts/reconstruct_15_2.py",
        "mappings": [
            {"role": "book_period", "raw_inputs": ["figures/15-2/data/raw/google_trends_monthly_2026-09-09.csv"], "selection": "US exact-term monthly responses 2004-2017", "transformation": "annual mean then centered three-year rolling mean", "clean": "figures/15-2/data/clean/figure_15_2_book_period.csv", "plot": "figures/15-2/plots/figure_15_2_book_period.png"},
            {"role": "extension", "raw_inputs": ["figures/15-2/data/raw/google_trends_monthly_2026-09-09.csv"], "selection": "US exact-term monthly responses 2018-2026", "transformation": "same annual mean and smoothing; render dashed", "clean": "figures/15-2/data/clean/figure_15_2_successor.csv", "plot": "figures/15-2/plots/figure_15_2_extended.png"},
        ],
    }
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    record = {
        "figure_id": "15-2", "title": "Racist, sexist, and homophobic Web searches, US, 2004-2017", "scientific_status": "partial_match", "artifact_kind": "reconstruction", "publication_status": "not_reviewed", "execution_status": "processed", "lifecycle_stage": "visual_review", "next_action": "Recover the January 22, 2017 Google Trends export and exact smoothing method.", "notes": "Current separate exact-term export; low-volume series do not match original early values.", "extension": {"status": "successor", "label": "Current Google Trends export 2018-2026"}, "visual_review": {"status": "pending", "reference_basis": "original", "issues": ["source-version mismatch", "unspecified smoothing", "low-volume zeros"]}, "artifacts": {
            "metadata": {"path": "figures/15-2/figure.json", "self": True}, "original_reference": {"path": "references/figures/figure_15_2.png"}, "book_period_reconstruction": {"path": "figures/15-2/plots/figure_15_2_book_period.png"}, "extended_reconstruction": {"path": "figures/15-2/plots/figure_15_2_extended.png"}, "book_period_clean": {"path": "figures/15-2/data/clean/figure_15_2_book_period.csv"}, "successor_clean": {"path": "figures/15-2/data/clean/figure_15_2_successor.csv"}, "book_period_comparison": {"path": "figures/15-2/plots/comparisons/figure_15_2_book_period_review.png"}, "extended_comparison": {"path": "figures/15-2/plots/comparisons/figure_15_2_extended_review.png"}, "caption": {"path": "figures/15-2/captions/caption.txt"}, "provenance": {"path": "figures/15-2/provenance/provenance.md"}, "source_log": {"path": "figures/15-2/source_logs/source_log.md"}, "anomaly_review": {"path": "figures/15-2/anomaly_reviews/anomaly_review.md"}, "discrepancy_log": {"path": "figures/15-2/discrepancy_logs/discrepancy_log.md"}, "review_checklist": {"path": "figures/15-2/review_checklist.md"}, "lineage": {"path": "figures/15-2/lineage/lineage.json"}, "reconstruction_script": {"path": "scripts/reconstruct_15_2.py"}
        }
    }
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")


def main() -> None:
    book, successor = build_data()
    book_plot = FIG / "plots/figure_15_2_book_period.png"
    extended_plot = FIG / "plots/figure_15_2_extended.png"
    draw(book, successor, book_plot, extended=False)
    draw(book, successor, extended_plot, extended=True)
    write_package(book, successor, book_plot, extended_plot)
    print(json.dumps({"figure": "15-2", "book_rows": len(book), "successor_rows": len(successor)}, indent=2))


if __name__ == "__main__":
    main()
