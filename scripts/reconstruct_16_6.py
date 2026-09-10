"""Reconstruct two distinct well-being indices from original numerical tables.

OECD: https://doi.org/10.1787/888933096502
Prados: https://doi.org/10.1111/roiw.12104, Table 1 (2015).
No annual observations or post-2007 HIHD values are invented.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/16-6"


def load_data():
    raw = pd.read_excel(FIG / "data/raw/oecd_figure13_2.xls", header=None)
    composite = raw.loc[raw[7].eq("World"), [8, 9]].copy()
    composite.columns = ["decade", "value"]
    composite["year"] = composite.decade.str.rstrip("s").astype(int)
    composite["value"] = composite.value.astype(float)
    composite["series"] = "Well-Being Composite"
    composite["unit"] = "standardized country-decade scale; population-weighted World"
    composite["source"] = "Rijpma 2014 Figure13.2 June23,2014 spreadsheet"
    hihd = pd.read_csv(FIG / "data/raw/prados_2015_table1.csv")[["year", "hihd"]].rename(columns={"hihd": "value"})
    hihd["series"] = "Historical Index of Human Development"
    hihd["unit"] = "0-1 index"
    hihd["source"] = "Prados de la Escosura 2015 Table1 PanelA"
    if len(composite) != 19 or len(hihd) != 14 or hihd.year.max() != 2007:
        raise ValueError("Unexpected original table coverage")
    return pd.concat([composite, hihd], ignore_index=True)


def main():
    data = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    data.to_csv(clean / "figure_16_6_book_period.csv", index=False)
    for mode in ["book_period", "extended"]:
        fig, ax = plt.subplots(figsize=(8.7, 6.6), dpi=200)
        fig.subplots_adjust(left=.12, right=.875, top=.95, bottom=.29)
        right = ax.twinx()
        left_data = data[data.series.eq("Well-Being Composite")]
        right_data = data[data.series.eq("Historical Index of Human Development")]
        ax.plot(left_data.year, left_data.value, color="#929292", lw=2.8)
        right.plot(right_data.year, right_data.value, color="#222222", lw=2.8)
        ax.set(xlim=(1820, 2020), ylim=(-1, 1), ylabel="Well-Being Composite")
        right.set(ylim=(0, .5), ylabel="Historical Index of Human Development")
        ax.set_xticks(range(1820, 2021, 10))
        ax.set_yticks([-1, -.5, 0, .5, 1])
        right.set_yticks([0, .1, .2, .3, .4, .5])
        ax.tick_params(axis="x", labelrotation=50, labelsize=10)
        ax.tick_params(axis="y", labelsize=11)
        right.tick_params(labelsize=11)
        ax.spines["top"].set_visible(False)
        right.spines["top"].set_visible(False)
        ax.text(1844, -.21, "Well-Being Composite", fontsize=12)
        ax.text(1936, -.61, "Historical Index of\nHuman Development", fontsize=12, ha="left")
        fig.text(.025, .155, "Figure 16-6: Global well-being, 1820-2015 (partial reconstruction)", fontsize=11)
        fig.text(.025, .035, "Sources: Rijpma (2014), OECD Figure 13.2; Prados de la Escosura (2015), Table 1.\n"
                 "Original tables: composite decadal, HIHD benchmarks through 2007. Book's 2015 HIHD update missing.\n"
                 + ("Extension NOT plotted: newer indices change definition. Historical reconstruction repeated."
                    if mode == "extended" else "Straight lines connect published benchmarks, not recovered annual observations."), fontsize=8.1)
        path = FIG / f"plots/{mode}/figure_16_6_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)


if __name__ == "__main__":
    main()
