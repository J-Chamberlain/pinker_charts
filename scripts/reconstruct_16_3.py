"""Seven-country schooling reconstruction with exact archived author cross-check.

Sources and URLs: figures/16-3/provenance/provenance.md.
2015 successor estimates are distinct from OWID's older projections.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/16-3"
RAW = FIG / "data/raw"
COUNTRIES = ["United States", "Japan", "Chile", "China", "India", "Cambodia", "Sierra Leone"]
COLUMN = "Total years of schooling (Lee-Lee (2016))"
STYLES = {"United States": ("#222222", "-"), "Japan": ("#aaaaaa", ":"), "Chile": ("#cccccc", "--"),
          "China": ("#666666", "-"), "India": ("#cccccc", "-"), "Cambodia": ("#222222", "--"), "Sierra Leone": ("#222222", ":")}


def author_table(path):
    raw = pd.read_excel(path, header=None)
    frame = raw.iloc[14:, [0, 1, 2, 3, 11]].copy()
    frame.columns = ["series", "year", "agefrom", "ageto", "author_value"]
    frame["series"] = frame.series.ffill().replace({"USA": "United States"})
    for column in frame.columns[1:]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame[frame.series.isin(COUNTRIES)].dropna()


def load_data():
    book = pd.read_csv(RAW / "owid_legacy.csv")[["Entity", "Year", COLUMN]].rename(columns={"Entity": "series", "Year": "year", COLUMN: "value"})
    book = book[book.series.isin(COUNTRIES)].dropna().sort_values(["series", "year"])
    book["unit"] = "mean years of schooling, both sexes age15-64"
    original = author_table(RAW / "author_2016_archive.xls")
    check = book.merge(original, on=["series", "year"], validate="one_to_one")
    check["difference"] = check.value - check.author_value
    if len(check) != 203 or check.difference.abs().max() > 1e-10 or not check.agefrom.eq(15).all() or not check.ageto.eq(64).all():
        raise ValueError("Original author archive and OWID no longer match")
    successor = pd.read_csv(RAW / "barro_lee_v3.csv").rename(columns={"country": "series", "yr_sch": "value"})
    successor["series"] = successor.series.replace({"USA": "United States"})
    successor = successor[successor.series.isin(COUNTRIES) & successor.sex.eq("MF") & successor.agefrom.eq(15) & successor.ageto.eq(64)].copy()
    successor["role"] = successor.year.map(lambda y: "updated_estimate" if y > 2010 else "revised_overlap")
    if successor.groupby("series").year.max().to_dict() != dict.fromkeys(COUNTRIES, 2015):
        raise ValueError("Unexpected successor country/year coverage")
    if book.duplicated(["series", "year"]).any() or successor.duplicated(["series", "year"]).any():
        raise ValueError("Duplicate observations")
    overlap = book.merge(successor[["series", "year", "value"]], on=["series", "year"], suffixes=("_book", "_successor"))
    overlap["difference"] = overlap.value_successor - overlap.value_book
    return book, successor.sort_values(["series", "year"]), check, overlap


def main():
    book, successor, check, overlap = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, frame in [("book_period", book), ("successor", successor), ("archive_check", check), ("vintage_difference", overlap)]:
        frame.to_csv(clean / f"figure_16_3_{name}.csv", index=False)
    for mode in ["book_period", "extended"]:
        fig, ax = plt.subplots(figsize=(9, 6.6), dpi=200)
        fig.subplots_adjust(left=.1, right=.95, top=.96, bottom=.28)
        labels = {"United States": (1987, 13.5), "Japan": (1980, 10.7), "Chile": (1988, 9.25),
                  "China": (2000, 8.7), "India": (2001, 6.85), "Cambodia": (2005, 5.35), "Sierra Leone": (2001, 1.65)}
        for series, group in book.groupby("series"):
            color, style = STYLES[series]
            ax.plot(group.year, group.value, color=color, ls=style, lw=2.3, solid_capstyle="round", dash_capstyle="round")
            if mode == "extended":
                updated = successor[successor.series.eq(series) & successor.year.ge(2000)]
                ax.plot(updated[updated.year.le(2010)].year, updated[updated.year.le(2010)].value, color=color, ls=":", lw=1.2)
                segment = updated[updated.year.ge(2010)]
                ax.plot(segment.year, segment.value, color=color, ls="--", lw=2.1, marker="o", ms=3, markerfacecolor="white")
            x, y = labels[series]
            ax.text(x, y, series.replace("Sierra Leone", "Sierra\nLeone"), fontsize=11)
        ax.set(xlim=(1865, 2020 if mode == "extended" else 2015), ylim=(0, 14), ylabel="Years of schooling")
        ax.set_xticks(range(1875, 2016, 10))
        ax.set_yticks(range(0, 15, 2))
        ax.tick_params(axis="x", rotation=45)
        ax.spines[["top", "right"]].set_visible(False)
        fig.text(.025, .145, "Figure 16-3: Years of schooling, 1870-2010" + (" | updated estimates to 2015" if mode == "extended" else ""), fontsize=11)
        note = "Original 2016 authors' workbook agrees with all 203 selected OWID observations." if mode == "book_period" else "Dashed 2010-2015: Barro-Lee v3 estimates (not older projections); dotted 2000-2010 revised overlap."
        fig.text(.025, .035, "Source: Lee & Lee (2016), via OWID's August 2016 data retrieval. Both sexes, age 15-64.\n"
                 + note + "\nSource estimates, not direct annual surveys. No digitization, artificial level shifts or smoothing.", fontsize=8, linespacing=1.4)
        path = FIG / f"plots/{mode}/figure_16_3_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=180)
    for series, group in overlap.groupby("series"):
        ax.plot(group.year, group.difference, label=series, marker=".", lw=1)
    ax.axhline(0, color="black", lw=.6)
    ax.set(xlabel="Year", ylabel="Successor minus book source (years)", title="16-3: revised historical overlap, not new schooling")
    ax.legend(frameon=False, fontsize=8, loc="center left", bbox_to_anchor=(1.01, .5))
    fig.tight_layout()
    path = FIG / "plots/diagnostics/vintage_difference.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
