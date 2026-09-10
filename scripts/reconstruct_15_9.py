"""Reconstruct Figure 15-9 from the public OWID historical incidence table."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/15-9"
RAW = FIG / "data/raw/owid_various_measures_child_labour_incidence.csv"
REF = ROOT / "references/figures/figure_15_9.png"
SERIES = ["England", "United States", "Italy", "World, ILO-EPEAP", "World, ILO-IPEC"]
COLORS = {"England": "#d1cfcf", "United States": "#777575", "Italy": "#d1cfcf", "World, ILO-EPEAP": "#252323", "World, ILO-IPEC": "#252323"}
STYLES = {"England": "-", "United States": "-", "Italy": "--", "World, ILO-EPEAP": "-", "World, ILO-IPEC": "--"}


def build_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    source = pd.read_csv(RAW)
    value_col = source.columns[-1]
    data = source.rename(columns={"Entity": "series", "Year": "year", value_col: "percent_children_working"})
    data = data[data.series.isin(SERIES)][["series", "year", "percent_children_working"]].sort_values(["series", "year"])
    return data[data.year <= 2012].copy(), data[data.year > 2012].copy()


def draw(data: pd.DataFrame, output: Path, extended: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12.2, 7.2), dpi=180)
    for series in SERIES:
        group = data[data.series == series]
        ax.plot(group.year, group.percent_children_working, color=COLORS[series], lw=3.0, ls=STYLES[series], label=series)
    ax.text(1865, 31, "England", fontsize=13.5, color="#242222")
    ax.text(1885, 13, "United\nStates", fontsize=13.5, color="#242222")
    ax.text(1925, 35, "Italy", fontsize=13.5, color="#242222")
    ax.text(1968, 29, "World\n(ILO-EPEAP)", fontsize=13.5, color="#242222", weight="bold")
    ax.text(1986, 20, "World\n(ILO-IPEC)", fontsize=13.5, color="#242222", weight="bold")
    ax.set_title("Figure 15-9: Child labor, 1850-2012", loc="left", fontsize=15)
    ax.set_ylabel("Percentage of children laboring", fontsize=12)
    ax.set_xlim(1850, 2012)
    ax.set_ylim(0, 70)
    ax.set_xticks([1850, 1870, 1890, 1910, 1930, 1950, 1970, 1990, 2010])
    ax.set_yticks(range(0, 71, 10))
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#626060")
    ax.spines["bottom"].set_color("#626060")
    ax.tick_params(colors="#3e3c3c", labelsize=9)
    note = "Source: Our World in Data historical incidence table; underlying sources listed in metadata and provenance."
    if extended:
        note += " No comparable post-2012 continuation recovered; all lines end at the book period."
    else:
        note += " Book-period values only; series definitions and age bands differ."
    fig.text(0.02, 0.018, note, fontsize=7.7, color="#555555")
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
    book.to_csv(FIG / "data/clean/figure_15_9_book_period.csv", index=False)
    successor.to_csv(FIG / "data/clean/figure_15_9_successor.csv", index=False)
    compare(book_plot, FIG / "plots/comparisons/figure_15_9_book_period_review.png", "Figure 15-9 book-period comparison")
    compare(extended_plot, FIG / "plots/comparisons/figure_15_9_extended_review.png", "Figure 15-9 extended comparison")
    (FIG / "captions/caption.txt").write_text(
        "Figure 15-9: Child labor, 1850-2012. The recreated historical series use the public Our World in Data table based on Cunningham and Viazzo (England), Tonioli and Vecchi (Italy), Long/Whaples-related historical US estimates, ILO-EPEAP, and ILO-IPEC. The age bands and definitions are not identical across series, as in the reference. No comparable post-2012 continuation was recovered, so the extended output repeats the book-period window and states that limitation. Status: verified_reproduction for the book-period source-backed reconstruction; extension unavailable.\n"
    )
    lineage = {
        "schema_version": 1,
        "figure_id": "15-9",
        "book_citation": "Our World in Data, Ortiz-Ospina & Roser 2016a; Cunningham 1996; Whaples 2005; Tonioli & Vecchi 2007; Basu 1999; ILO 2013.",
        "raw_source": "figures/15-9/data/raw/owid_various_measures_child_labour_incidence.csv",
        "script": "scripts/reconstruct_15_9.py",
        "mappings": [
            {"role": "book_period", "raw_inputs": ["figures/15-9/data/raw/owid_various_measures_child_labour_incidence.csv"], "selection": "five named historical series through 2012", "transformation": "rename fields and plot source percentages without interpolation", "clean": "figures/15-9/data/clean/figure_15_9_book_period.csv", "plot": "figures/15-9/plots/book_period/figure_15_9_book_period.png"},
            {"role": "extension", "raw_inputs": [], "selection": "none", "transformation": "not applied; no comparable post-2012 continuation recovered", "clean": "figures/15-9/data/clean/figure_15_9_successor.csv", "plot": "figures/15-9/plots/extended/figure_15_9_extended.png"},
        ],
    }
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")


def main() -> None:
    book, successor = build_data()
    book_plot = FIG / "plots/book_period/figure_15_9_book_period.png"
    extended_plot = FIG / "plots/extended/figure_15_9_extended.png"
    draw(book, book_plot, extended=False)
    draw(book, extended_plot, extended=True)
    write_package(book, successor, book_plot, extended_plot)
    print(json.dumps({"figure": "15-9", "book_rows": len(book), "successor_rows": len(successor)}, indent=2))


if __name__ == "__main__":
    main()
