"""Recover youth literacy parity from retained WDI 2016 and 2026 snapshots.

https://api.worldbank.org/v2/indicator/SE.ADT.1524.LT.FM.ZS?format=json
Original archive URL/hash: figures/17-8/source_logs/downloads.json.
England and HumanProgress's World aggregation are NOT inferred from pixels.
"""
import json
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/16-4"
ARCHIVE = ROOT / "figures/17-8/data/raw/WDI_csv_20161119172134.zip"
INDICATOR = "SE.ADT.1524.LT.FM.ZS"
COUNTRIES = {"AFG": "Afghanistan", "PAK": "Pakistan"}


def load_data():
    with zipfile.ZipFile(ARCHIVE) as archive:
        countries = pd.read_csv(archive.open("WDI_Country.csv"), encoding="cp1252")
        frames = []
        for chunk in pd.read_csv(archive.open("WDI_Data.csv"), encoding="cp1252", chunksize=20000):
            frames.append(chunk[chunk["Indicator Code"].eq(INDICATOR)])
    wide = pd.concat(frames)
    years = [c for c in wide if c.isdigit()]
    all_old = wide.melt(id_vars=["Country Name", "Country Code"], value_vars=years,
                        var_name="year", value_name="ratio").dropna(subset="ratio")
    all_old = all_old.rename(columns={"Country Name": "country", "Country Code": "code"})
    all_old["year"] = all_old.year.astype(int)
    all_old["source_version"] = "WDI archived 2016-11-19"
    book = all_old[all_old.code.isin(COUNTRIES) & all_old.year.le(2014)].copy()
    current = json.loads((FIG / "data/candidates/wdi_ratio.json").read_text())
    if current[0]["pages"] != 1 or len(current[1]) != current[0]["total"]:
        raise ValueError("Incomplete current WDI response")
    rows = []
    for item in current[1]:
        if item["indicator"]["id"] != INDICATOR:
            raise ValueError("Wrong indicator")
        if item["countryiso3code"] in COUNTRIES and item["value"] is not None:
            rows.append({"country": COUNTRIES[item["countryiso3code"]],
                         "code": item["countryiso3code"], "year": int(item["date"]),
                         "ratio": item["value"], "source_version": "WDI 2026-07-13 / UIS 2026-02"})
    successor = pd.DataFrame(rows).sort_values(["code", "year"])
    for frame in [book, successor]:
        if frame.duplicated(["code", "year"]).any() or not frame.ratio.between(0, 2).all():
            raise ValueError("Invalid parity observations")
    # This annual available-country mean is a rejected diagnostic, not the book World line.
    real_codes = countries.loc[countries.Region.notna(), "Country Code"]
    diagnostic = all_old[all_old.code.isin(real_codes) & all_old.year.between(1975, 2014)]
    diagnostic = diagnostic.groupby("year").ratio.agg(["mean", "count"]).reset_index()
    overlap = all_old[all_old.code.isin(COUNTRIES)].merge(
        successor, on=["code", "year"], suffixes=("_2016", "_2026"))
    overlap["difference"] = overlap.ratio_2026 - overlap.ratio_2016
    return book.sort_values(["code", "year"]), successor, diagnostic, overlap


def axes(ax, recent=False):
    ax.set(xlim=(1975, 2025) if recent else (1750, 2017), ylim=(0, 1.04),
           ylabel="Ratio of literate females to literate males")
    ax.set_xticks(range(1975, 2026, 10) if recent else range(1750, 2016, 25))
    ax.set_yticks(np.arange(0, 1.01, .1))
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=10, length=6)


def main():
    book, successor, diagnostic, overlap = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, frame in [("book_period", book), ("successor", successor),
                        ("rejected_world_mean", diagnostic), ("vintage_difference", overlap)]:
        frame.to_csv(clean / f"figure_16_4_{name}.csv", index=False)
    colors = {"PAK": "#777777", "AFG": "#aaaaaa"}
    for mode in ["book_period", "extended"]:
        extended = mode == "extended"
        fig = plt.figure(figsize=(8.2, 8.6 if extended else 6.4), dpi=200)
        ax = fig.add_axes([.12, .49 if extended else .30, .85, .45 if extended else .65])
        axes(ax)
        for code in COUNTRIES:
            rows = book[book.code.eq(code)]
            ax.plot(rows.year, rows.ratio, color=colors[code], lw=2.5)
            ax.text(1940, .67 if code == "PAK" else .31, COUNTRIES[code], fontsize=11)
        ax.text(1770, .84, "England: original numeric table not recovered\n"
                "World: original averaging method unresolved", fontsize=10, color="#555555")
        if extended:
            sub = fig.add_axes([.12, .16, .85, .235])
            axes(sub, recent=True)
            sub.set_title("Separate revised successor: dotted through 2014, dashed after", fontsize=9)
            sub.set_ylabel("Youth literacy parity", fontsize=10)
            for code in COUNTRIES:
                rows = successor[successor.code.eq(code)]
                color = "#157f7b" if code == "PAK" else "#99477b"
                # Clip visual segments at the cutoff without inventing a 2014 observation.
                before, = sub.plot(rows.year, rows.ratio, color=color, ls=":", lw=1.8)
                after, = sub.plot(rows.year, rows.ratio, color=color, ls="--", marker="o", ms=3,
                                  markerfacecolor="white", lw=1.8, label=COUNTRIES[code])
                before.set_clip_path(Rectangle((1975, 0), 2014 - 1975, 1.04, transform=sub.transData))
                after.set_clip_path(Rectangle((2014, 0), 2025 - 2014, 1.04, transform=sub.transData))
            sub.axvline(2014, color="#bbbbbb", lw=.7)
            sub.legend(frameon=False, loc="lower right", fontsize=9)
        fig.text(.025, .10 if extended else .19,
                 "Figure 16-4: Female literacy, 1750-2014 | Partial reconstruction", fontsize=11)
        fig.text(.025, .025 if extended else .055,
                 "Sources: UNESCO UIS / World Bank, archived November 2016 and July 2026 vintage.\n"
                 "Only Pakistan and Afghanistan recovered; England and World remain missing.\n"
                 + ("Revised successor shown separately. Survey gaps joined; no annual interpolation.\n"
                    "Afghanistan 2015 is revised downward; 2022 endpoint is not evidence of current policy effects."
                    if extended else "Lines join sparse age 15-24 observations; no digitized chart values."), fontsize=8)
        path = FIG / f"plots/{mode}/figure_16_4_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.3), dpi=180)
    axs[0].plot(diagnostic.year, diagnostic["mean"], color="#555555", marker="o", ms=3)
    axs[0].set(title="Rejected World proxy: available-country mean", xlabel="Year", ylabel="Unweighted mean parity ratio")
    for code in COUNTRIES:
        rows = overlap[overlap.code.eq(code)]
        axs[1].plot(rows.year, rows.difference, marker="o", label=COUNTRIES[code])
    axs[1].axhline(0, lw=.7, color="gray")
    axs[1].set(title="Source revision, not measured annual change", xlabel="Year", ylabel="2026 ratio minus 2016 ratio")
    axs[1].legend(frameon=False)
    fig.tight_layout(rect=(0, .06, 1, 1))
    fig.text(.03, .015, "Diagnostic only: changing country membership does not recover the book's World line. Source values unchanged.", fontsize=9)
    path = FIG / "plots/diagnostics/vintage_difference.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


if __name__ == "__main__":
    main()
