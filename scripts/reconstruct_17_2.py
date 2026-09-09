"""Offline reconstruction from Costa, Short and original BLS tables.

Exact source URLs and browser-table retrieval: figures/17-2/source_logs/.
Historical gainful employment and CPS participation are not identical measures.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/17-2"
RAW = FIG / "data/raw"


def load_data():
    costa = pd.read_csv(RAW / "costa_1998_table_2a1.csv")
    short = pd.read_html(RAW / "short_2002_page.html")[0]
    short.columns = ["year", "lfpr_percent"]
    short = short.apply(pd.to_numeric, errors="coerce").dropna()
    short.year = short.year.astype(int)
    historic = costa[costa.year.ge(1880)].rename(columns={"gainful_percent": "lfpr_percent"})
    crosscheck = historic.merge(short, on="year", suffixes=("_costa", "_short"))
    if len(crosscheck) != 12 or not np.array_equal(crosscheck.lfpr_percent_costa, crosscheck.lfpr_percent_short):
        raise ValueError("Costa/Short historic numeric tables disagree")
    book = historic[["year", "lfpr_percent"]].copy()
    book["source_version"] = "Costa 1998 Table 2A.1"
    book["definition"] = "gainful employment (occupation in preceding year)"
    y2000 = short[short.year.eq(2000)].copy()
    y2000["source_version"] = "Short 2002 Table 1 citing BLS"
    y2000["definition"] = "labor-force participation; original release not established"
    y2010 = pd.read_csv(RAW / "bls_2010_men65.csv")[["year", "lfpr_percent"]]
    y2010["source_version"] = "BLS 2010 annual Table 3"
    y2010["definition"] = "CPS survey-week labor-force participation"
    book = pd.concat([book, y2000, y2010], ignore_index=True)
    bls = pd.read_html(RAW / "bls_2025_table.html")[0]
    bls = bls.apply(pd.to_numeric, errors="coerce").dropna()
    bls.columns = ["year", "total", "lfpr_percent", "women"]
    bls.year = bls.year.astype(int)
    if bls.year.tolist() != list(range(1948, 2025)):
        raise ValueError("Unexpected BLS continuation coverage")
    extension = bls[bls.year.ge(2010)][["year", "lfpr_percent"]].copy()
    extension["source_version"] = "BLS May 2025 Chart 2 numeric table"
    extension["definition"] = "CPS survey-week labor-force participation"
    if extension.iloc[0].lfpr_percent != y2010.iloc[0].lfpr_percent:
        raise ValueError("BLS 2010 vintage mismatch: do not join silently")
    extended = pd.concat([book.assign(segment="book"), extension.assign(segment="extension")], ignore_index=True)
    for frame in [book, extended]:
        frame["entity"] = "United States"
        frame["sex"] = "men"
        frame["age"] = "65+"
        frame["unit"] = "percent"
        if not frame.lfpr_percent.between(0, 100).all():
            raise ValueError("Invalid participation percent")
    diagnostic = historic[["year", "lfpr_percent", "current_definition_percent"]].merge(
        bls[["year", "lfpr_percent"]], on="year", how="left", suffixes=("_gainful", "_cps_2025"))
    return book, extended, diagnostic


def main():
    book, extended, diagnostic = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, frame in [("book_period", book), ("extended", extended), ("definitions", diagnostic)]:
        frame.to_csv(clean / f"figure_17_2_{name}.csv", index=False)
    for mode in ["book_period", "extended"]:
        fig, ax = plt.subplots(figsize=(8.2, 5.9), dpi=200)
        fig.subplots_adjust(left=.115, right=.975, top=.96, bottom=.235)
        ax.plot(book.year, book.lfpr_percent, color="#252525", lw=2.5)
        if mode == "extended":
            later = extended[extended.segment.eq("extension")]
            ax.plot(later.year, later.lfpr_percent, color="#187f7b", ls="--", lw=2.2,
                    label="BLS continuation, 2011-2024")
            ax.legend(loc="upper right", frameon=False, fontsize=10)
        ax.set(xlim=(1880, 2030 if mode == "extended" else 2020), ylim=(0, 100),
               ylabel="Percentage of men 65+ participating in the labor force")
        ax.set_xticks(range(1880, 2021, 20))
        ax.set_yticks(range(0, 101, 10))
        ax.tick_params(length=6, labelsize=11)
        ax.spines[["top", "right"]].set_visible(False)
        for side in ["left", "bottom"]:
            ax.spines[side].set_color("#666666")
        fig.text(.025, .13, "Figure 17-2: Retirement, US, 1880-2010" + ("; continuation to 2024" if mode == "extended" else ""), fontsize=11)
        fig.text(.025, .03, "Sources: Costa (1998), Table 2A.1; Short (2002); BLS 2010 Table 3 / May 2025.\n"
                 "1880-1990: gainful employment; 2000 onward: labor-force participation. Definitions differ.\n"
                 "Source-table values retained; small book-level differences are unresolved. Not a retirement-rate estimate.",
                 fontsize=7.5, linespacing=1.4)
        path = FIG / f"plots/{mode}/figure_17_2_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(8.2, 4.9), dpi=180)
    for column, label, style in [("lfpr_percent_gainful", "Costa: gainful employment", "-"),
                                  ("current_definition_percent", "Costa: current definition", "--"),
                                  ("lfpr_percent_cps_2025", "BLS May 2025 CPS table", ":")]:
        subset = diagnostic[diagnostic.year.ge(1940)]
        ax.plot(subset.year, subset[column], style, label=label, lw=2)
    ax.set(xlabel="Year", ylabel="Men 65+ participating (%)", title="Figure 17-2: definitions are not interchangeable")
    ax.legend(frameon=False)
    fig.tight_layout()
    path = FIG / "plots/diagnostics/definitions.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
