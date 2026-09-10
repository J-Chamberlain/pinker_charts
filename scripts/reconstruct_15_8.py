"""Build an evidence reconstruction for Figure 15-8 from public BJS/OWID data.

The physical- and sexual-abuse NCANDS series remain unavailable without the
NDACAN ordering step. The script therefore plots only the legitimately downloaded
school-victimization subset and marks the result as a partial match.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/15-8"
RAW = FIG / "data/raw/owid_bjs_school_victimization.csv"
REF = ROOT / "references/figures/figure_15_8.png"


def build_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    source = pd.read_csv(RAW)
    value_col = next(column for column in source.columns if column.startswith("US Violent"))
    data = source.rename(columns={"Year": "year", value_col: "rate_per_1000"})[["year", "rate_per_1000"]]
    data["rate_per_100000"] = data["rate_per_1000"] * 100
    data["series"] = "Violent victimization at school"
    book = data[data.year.between(1993, 2012)].copy()
    successor = data[data.year >= 2013].copy()
    return book, successor


def draw(book: pd.DataFrame, successor: pd.DataFrame, output: Path, extended: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12.2, 7.2), dpi=180)
    ax.plot(book.year, book.rate_per_100000, color="#aaa8a8", lw=3.0, label="School victimization subset")
    if extended:
        ax.plot(successor.year, successor.rate_per_100000, color="#aaa8a8", lw=3.0, ls="--", label="BJS/OWID successor")
        ax.axvline(2012, color="#c6c6c6", lw=1.0, ls=":")
    ax.text(1995.2, 1120, "Violent victimization at school (public subset)", fontsize=13.5, color="#242222")
    ax.set_title("Figure 15-8: Victimization of children, US, 1993-2012", loc="left", fontsize=15)
    ax.set_ylabel("Rate per 100,000 people aged 12+ (converted from per 1,000)", fontsize=11)
    ax.set_xlim(1993, 2015 if extended else 2012)
    ax.set_ylim(0, 1400)
    ax.set_xticks(range(1993, 2016 if extended else 2013, 2))
    ax.set_yticks(range(0, 1401, 200))
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#626060")
    ax.spines["bottom"].set_color("#626060")
    ax.tick_params(colors="#3e3c3c", labelsize=9)
    note = "Source: BJS NCVS series as distributed by Our World in Data; converted from rates per 1,000 to per 100,000."
    if extended:
        note += " Dashed: 2013-2015 continuation."
    note += " Physical and sexual NCANDS series are not included; see the figure review files."
    fig.text(0.02, 0.018, note, fontsize=7.5, color="#555555")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def compare(recreated: Path, output: Path, title: str) -> None:
    ref, rec = mpimg.imread(REF), mpimg.imread(recreated)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=180)
    for axis, image, label in zip(axes, [ref, rec], ["Supplemental PDF reference", "Recreated subset"]):
        axis.imshow(image)
        axis.set_title(label, fontsize=10)
        axis.axis("off")
    fig.suptitle(title, fontsize=12)
    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_package(book: pd.DataFrame, successor: pd.DataFrame, book_plot: Path, extended_plot: Path) -> None:
    book.to_csv(FIG / "data/clean/figure_15_8_book_period.csv", index=False)
    successor.to_csv(FIG / "data/clean/figure_15_8_successor.csv", index=False)
    compare(book_plot, FIG / "plots/comparisons/figure_15_8_book_period_review.png", "Figure 15-8 book-period comparison")
    compare(extended_plot, FIG / "plots/comparisons/figure_15_8_extended_review.png", "Figure 15-8 extended comparison")
    (FIG / "captions/caption.txt").write_text(
        "Figure 15-8: Victimization of children, US, 1993-2012. The reference combines physical abuse, sexual abuse, and violent victimization at school. This evidence reconstruction plots only the publicly downloadable BJS/NCVS school series distributed by Our World in Data, converted from rates per 1,000 to rates per 100,000 for a common visual scale; physical and sexual abuse rates from NCANDS are omitted pending NDACAN access. Dashed values extend the public BJS/OWID series through 2015. Status: partial_match.\n"
    )
    lineage = {
        "schema_version": 1,
        "figure_id": "15-8",
        "book_citation": "Physical and sexual abuse: NCANDS, analyzed by Finkelhor 2014; violent victimization at school: BJS NCVS NVAT.",
        "raw_source": "figures/15-8/data/raw/owid_bjs_school_victimization.csv",
        "script": "scripts/reconstruct_15_8.py",
        "mappings": [
            {
                "role": "book_period_subset",
                "raw_inputs": ["figures/15-8/data/raw/owid_bjs_school_victimization.csv"],
                "selection": "United States, 1993-2012 school victimization series",
                "transformation": "convert per-1,000 values to per-100,000 by multiplying by 100",
                "clean": "figures/15-8/data/clean/figure_15_8_book_period.csv",
                "plot": "figures/15-8/plots/book_period/figure_15_8_book_period.png",
            },
            {
                "role": "successor_subset",
                "raw_inputs": ["figures/15-8/data/raw/owid_bjs_school_victimization.csv"],
                "selection": "United States, 2013-2015 school victimization series",
                "transformation": "same unit conversion, plotted dashed",
                "clean": "figures/15-8/data/clean/figure_15_8_successor.csv",
                "plot": "figures/15-8/plots/extended/figure_15_8_extended.png",
            },
        ],
    }
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")


def main() -> None:
    book, successor = build_data()
    book_plot = FIG / "plots/book_period/figure_15_8_book_period.png"
    extended_plot = FIG / "plots/extended/figure_15_8_extended.png"
    draw(book, successor, book_plot, extended=False)
    draw(book, successor, extended_plot, extended=True)
    write_package(book, successor, book_plot, extended_plot)
    print(json.dumps({"figure": "15-8", "book_rows": len(book), "successor_rows": len(successor)}, indent=2))


if __name__ == "__main__":
    main()
