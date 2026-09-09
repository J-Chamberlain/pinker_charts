"""Offline Figure 17-8 reconstruction from retained, versioned source tables.

Sources/URLs/hashes: figures/17-8/data/raw/*metadata.json and source_logs/.
2016 WDI history is frozen. The missing 2015 endpoint uses the 2017 WDI
release and is visibly marked. Later UN Tourism vintages are separate segments.
No interpolation, rescaling, smoothing, or digitized chart observations.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/17-8"
REGIONS = {"Africa", "Americas", "Asia & Pacific", "Europe", "Middle East"}


def wdi_long(path):
    row = pd.read_csv(path).iloc[0]
    return pd.DataFrame([{"year": int(k), "arrivals": float(v)} for k, v in row.items()
                         if str(k).isdigit() and pd.notna(v)]).sort_values("year")


def load_data():
    raw = FIG / "data/raw"
    early = wdi_long(raw / "wdi_2016_world_row.csv")
    later = wdi_long(raw / "wdi_2017_october_world_row.csv")
    early = early[early.year.between(1995, 2014)].assign(source_version="WDI 2016-11-17", role="book_period")
    if early.year.tolist() != list(range(1995, 2015)):
        raise ValueError("Expected complete 1995-2014 archived history")
    endpoint = later[later.year.eq(2015)].assign(source_version="WDI 2017-10", role="revised_endpoint")
    if len(endpoint) != 1:
        raise ValueError("Missing 2015 successor endpoint")
    book = pd.concat([early, endpoint], ignore_index=True)
    regional = pd.read_csv(FIG / "data/candidates/owid_regional_arrivals_2026_09_09.csv")
    selected = regional[regional.Year.between(2015, 2018)]
    for year, group in selected.groupby("Year"):
        if set(group.Entity) != REGIONS or group.Entity.duplicated().any():
            raise ValueError(f"Incomplete/nonexclusive regional coverage: {year}")
    if set(selected.Year) != set(range(2015, 2019)):
        raise ValueError("Missing successor years")
    extension1 = selected.groupby("Year")["International Tourist Arrivals"].sum().reset_index()
    extension1.columns = ["year", "arrivals"]
    extension1 = extension1.assign(source_version="UNWTO 2019 via OWID", role="successor")
    extension2 = pd.read_csv(raw / "un_tourism_2026_01_world_table.csv")
    extension2["arrivals"] = extension2.arrivals_millions * 1e6
    extension2 = extension2.assign(source_version="UN Tourism January 2026", role="successor")
    if extension2.year.tolist() != list(range(2019, 2026)):
        raise ValueError("Missing recent successor years")
    extended = pd.concat([book, extension1, extension2], ignore_index=True)
    for table in [book, extended]:
        table["arrivals_billions"] = table.arrivals / 1e9
        if table[["source_version", "year"]].duplicated().any() or not np.isfinite(table.arrivals).all() or (table.arrivals < 0).any():
            raise ValueError("Duplicate, missing or invalid source observations")
    current = json.loads((raw / "world_bank_tourism_current_2026_09_09.json").read_text())
    current = pd.DataFrame([{"year": int(r["date"]), "arrivals": r["value"]} for r in current[1] if r["value"] is not None])
    diagnostic = early[["year", "arrivals"]].merge(later, on="year", suffixes=("_2016", "_2017"))
    diagnostic = diagnostic.merge(current.rename(columns={"arrivals": "arrivals_current"}), on="year")
    diagnostic["current_to_2016_ratio"] = diagnostic.arrivals_current / diagnostic.arrivals_2016
    return book, extended, diagnostic


def plot(book, extended, output, extension=False):
    fig, ax = plt.subplots(figsize=(8.2, 5.75), dpi=200)
    fig.subplots_adjust(left=.13, right=.975, top=.91, bottom=.21)
    historic = book[book.role.eq("book_period")]
    ax.plot(historic.year, historic.arrivals_billions, color="#252525", lw=2.2)
    endpoint = book[book.year.ge(2014)]
    ax.plot(endpoint.year, endpoint.arrivals_billions, color="#252525", lw=2.2, ls=":")
    ax.plot(endpoint.year.iloc[-1], endpoint.arrivals_billions.iloc[-1], marker="o", ms=5, mfc="white", mec="#252525", clip_on=False)
    if extension:
        colors = ["#888888", "#246b79"]
        for version, color in zip(["UNWTO 2019 via OWID", "UN Tourism January 2026"], colors):
            series = extended[extended.source_version.eq(version)]
            ax.plot(series.year, series.arrivals_billions, ls="--", color=color, lw=2, marker="o", ms=2.5, label=version)
        ax.axvline(2015, color="#999999", lw=.8, ls=":")
        ax.set_xlim(1995, 2025.3)
        ax.set_ylim(.3, 1.6)
        ax.set_xticks(range(1995, 2026, 5))
        ax.set_yticks(np.arange(.4, 1.61, .2))
        ax.legend(frameon=False, fontsize=8, loc="upper left")
        ax.annotate("Pandemic", (2020, .409), xytext=(2015.8, .57), fontsize=9,
                    arrowprops={"arrowstyle": "-", "lw": .7})
    else:
        ax.set_xlim(1995, 2015.05)
        ax.set_ylim(.5, 1.3)
        ax.set_xticks(range(1995, 2016, 5))
        ax.set_yticks(np.arange(.5, 1.31, .1))
    ax.set_ylabel("Number of arrivals (billions)", fontsize=11)
    ax.tick_params(labelsize=10, length=6, color="#666666")
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color("#666666")
    title = "Figure 17-8: International tourism, 1995-2015"
    fig.text(.035, .11, title + ("; extension to 2025" if extension else ""), fontsize=11)
    footer = "Source: archived World Bank WDI. Hollow 2015 point: later WDI release."
    if extension:
        footer += "\nDashed: UN Tourism successor vintages; gaps at source changes. 2025 provisional."
    else:
        footer += "\n2016 archive lacks 2015; dotted join is not an exact historical reproduction."
    fig.text(.035, .038, footer, fontsize=8, linespacing=1.5)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, facecolor="white")
    plt.close(fig)


def main():
    book, extended, diagnostic = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, frame in [("book_period", book), ("extended", extended), ("source_version_diagnostic", diagnostic)]:
        frame.to_csv(clean / f"figure_17_8_{name}.csv", index=False)
    plot(book, extended, FIG / "plots/book_period/figure_17_8_book_period.png")
    plot(book, extended, FIG / "plots/extended/figure_17_8_extended.png", True)
    fig, ax = plt.subplots(figsize=(8.2, 4.8), dpi=160)
    for column, label in [("arrivals_2016", "WDI November 2016"), ("arrivals_2017", "WDI October 2017"),
                          ("arrivals_current", "Current WDI API (rejected)")]:
        ax.plot(diagnostic.year, diagnostic[column]/1e9, label=label)
    ax.set(xlabel="Year", ylabel="International arrivals (billions)", title="Figure 17-8: why source vintage cannot be ignored")
    ax.set_xticks([1995, 2000, 2005, 2010, 2014])
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    directory = FIG / "plots/diagnostics"
    directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(directory / "source_versions.png", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
