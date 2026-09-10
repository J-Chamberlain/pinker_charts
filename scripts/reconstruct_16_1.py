"""Literacy from the actual 2016 OWID CSV, with a separate revised successor.

Source URLs and archive timestamps: figures/16-1/provenance/provenance.md.
No values are read from chart pixels. Lines connect the original sparse records.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/16-1"
RAW = FIG / "data/raw"
SERIES = {"World": "World", "Netherlands": "Netherlands", "Great Britain": "England/GB/UK",
          "Germany": "Germany", "Italy": "Italy", "USA": "United States", "Chile": "Chile", "Mexico": "Mexico"}
STYLE = {"World": ("#222222", "-", 3.3), "Netherlands": ("#929292", "--", 2.3),
         "England/GB/UK": ("#222222", "--", 2.3), "Germany": ("#d0d0d0", "-", 2.3),
         "Italy": ("#cecece", "--", 2.3), "United States": ("#222222", ":", 2.3),
         "Chile": ("#666666", "-", 2.3), "Mexico": ("#a5a5a5", ":", 2.3)}


def load_data():
    table = pd.read_csv(RAW / "owid_2016_long_run.csv")
    book = table.melt(id_vars="year", value_vars=list(SERIES), var_name="source_series", value_name="value").dropna()
    book["year"] = book.year.astype(int)
    book = book[book.year.le(2010)].copy()
    book["series"] = book.source_series.map(SERIES)
    book["unit"] = "percent literate; heterogeneous historical definitions"
    book["vintage"] = "OWID CSV archived 2016-03-25"
    book = book.sort_values(["series", "year"])
    current = pd.read_csv(RAW / "owid_current.csv").rename(columns={"Entity": "series", "Year": "year", "Literacy rate": "value"})
    current = current[current.series.isin(["World", "Italy", "Chile", "Mexico"]) & current.year.ge(2000)].copy()
    current["unit"] = "percent literate, adults age 15+"
    current["vintage"] = "OWID/UNESCO UIS 2026; downloaded 2026-09-10 UTC"
    current["role"] = current.year.map(lambda year: "revised_overlap" if year <= 2010 else "post_book_successor")
    if book.duplicated(["series", "year"]).any() or not book.value.between(0, 100).all() or book.series.nunique() != 8:
        raise ValueError("Unexpected historical literacy records")
    if current.duplicated(["series", "year"]).any() or not current.value.between(0, 100).all():
        raise ValueError("Unexpected current literacy records")
    nces = pd.read_html(RAW / "nces_literacy.html")[0].iloc[:, :2].copy()
    nces.columns = ["year", "illiterate"]
    nces = nces.apply(pd.to_numeric, errors="coerce").dropna()
    nces["year"] = nces.year.astype(int)
    nces["nces_literate"] = 100 - nces.illiterate
    check = book[book.series.eq("United States")].merge(nces, on="year")
    check["difference_pp"] = check.value - check.nces_literate
    if len(check) != 14 or check.difference_pp.abs().max() > 1e-10:
        raise ValueError("Archived US series no longer agrees with original NCES table")
    return book, current.sort_values(["series", "year"]), check


def historical(ax, book):
    for series, group in book.groupby("series"):
        color, style, width = STYLE[series]
        ax.plot(group.year, group.value, color=color, ls=style, lw=width,
                solid_capstyle="round", dash_capstyle="round")
    labels = {"Netherlands": (1740, 92), "England/GB/UK": (1710, 56), "Germany": (1655, 38),
              "Italy": (1680, 25), "United States": (1825, 81), "Chile": (1882, 61),
              "Mexico": (2015, 90), "World": (1980, 43)}
    for label, (x, y) in labels.items():
        ax.text(x, y, label.replace("United States", "United\nStates"), fontsize=11,
                weight="bold" if label == "World" else "normal")
    ax.set(xlim=(1475, 2020), ylim=(0, 100), ylabel="Percent literate")
    ax.set_xticks(range(1475, 2001, 25))
    ax.set_yticks(range(0, 101, 10))
    ax.tick_params(axis="x", rotation=45)
    for label in ax.get_xticklabels():
        label.set_ha("right")
    for edge in ["top", "right"]:
        ax.spines[edge].set_visible(False)
    ax.tick_params(labelsize=10)


def main():
    book, current, check = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, data in [("book_period", book), ("successor", current), ("nces_check", check)]:
        data.to_csv(clean / f"figure_16_1_{name}.csv", index=False)
    for mode in ["book_period", "extended"]:
        fig, ax = plt.subplots(figsize=(9, 6.6 if mode == "book_period" else 10.0), dpi=200)
        if mode == "extended":
            ax.remove()
            ax = fig.add_axes([.1, .48, .82, .48])
            recent = fig.add_axes([.1, .18, .82, .20])
            for series, group in current.groupby("series"):
                color = {"World": "#222222", "Chile": "#197b87", "Italy": "#754a83", "Mexico": "#aa5533"}[series]
                overlap = group[group.year.le(2010)]
                later = group[group.year.gt(2010)]
                recent.plot(overlap.year, overlap.value, color=color, ls=":", lw=1.5, marker=".", ms=3)
                recent.plot(later.year, later.value, color=color, ls="--", lw=2, marker=".", ms=3, label=series)
            recent.axvline(2010, color="#bbbbbb", lw=.8)
            recent.set(xlim=(2000, 2025), ylim=(75, 101), xlabel="Year", ylabel="Adult literacy (%)",
                       title="Separate revised successor: dotted overlap, dashed after 2010")
            recent.legend(frameon=False, ncol=4, loc="lower right", fontsize=9)
            recent.spines[["top", "right"]].set_visible(False)
        else:
            fig.subplots_adjust(left=.1, right=.92, top=.96, bottom=.27)
        historical(ax, book)
        fig.text(.025, .105 if mode == "extended" else .12, "Figure 16-1: Literacy, 1475-2010" + (" | successor to 2024" if mode == "extended" else ""), fontsize=11)
        note = "2016 archive preserved, including disputed World 1940-1980 values. Sparse observations joined, not annual data."
        if mode == "extended":
            note += "\n2026 OWID/UIS is not a seamless continuation. Countries end in different years; no carry-forward."
        fig.text(.025, .027, "Source: Roser & Ortiz-Ospina, OWID, actual CSV archived March 25, 2016.\n" + note, fontsize=8, linespacing=1.4)
        path = FIG / f"plots/{mode}/figure_16_1_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=180)
    world = book[book.series.eq("World")]
    revised = pd.read_csv(RAW / "owid_global_2019.csv")
    ax.plot(world.year, world.value, label="2016 archived book candidate", color="#222222", marker=".")
    column = "Literate world population (OWID based on OECD & UNESCO (2019))"
    diagnostic = pd.concat([
        world[["year", "value"]].assign(vintage="2016"),
        revised[["Year", column]].rename(columns={"Year": "year", column: "value"}).assign(vintage="2019"),
        current[current.series.eq("World")][["year", "value"]].assign(vintage="2026")
    ], ignore_index=True)
    diagnostic.to_csv(clean / "figure_16_1_world_vintages.csv", index=False)
    ax.plot(revised.Year, revised[column], label="2019 revised historical World series", color="#197b87", ls="--")
    modern = current[current.series.eq("World")]
    ax.plot(modern.year, modern.value, label="2026 OWID/UIS", color="#aa5533", ls=":")
    ax.set(xlabel="Year", ylabel="Percent literate", title="World literacy: source revisions are not new progress", ylim=(0, 100))
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    path = FIG / "plots/diagnostics/world_vintages.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
