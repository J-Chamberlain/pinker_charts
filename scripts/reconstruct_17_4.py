"""Rebuild Figure 17-4 offline from retained OWID source observations.

Historical source: https://github.com/owid/owid-datasets/tree/189ffb348bbc843a29d749b6425da6c7798d8d6f/datasets/Price%20for%20Light%20%E2%80%93%20Fouquet
Successor: https://ourworldindata.org/grapher/the-price-for-lighting-per-million-lumen-hours-in-the-uk-in-british-pound
Exact requests, source metadata and checksums are in figures/17-4/source_logs/.
No digitization, interpolation, rebasing, or additional smoothing is applied.
"""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/17-4"
UNIT = "GBP_2000_per_million_lumen_hours"


def load_data():
    raw = FIG / "data/raw"
    historic = pd.read_csv(raw / "owid_legacy.csv")
    if historic.columns.tolist() != ["Entity", "Year", "Price for Light \u2013 Fouquet and Pearson (2012)"]:
        raise ValueError("Historical source schema changed")
    if set(historic.Entity) != {"Price for Lightning"}:
        raise ValueError("Unexpected historical entity")
    book = historic.rename(columns={historic.columns[-1]: "value", "Year": "year", "Entity": "source_entity"})
    book = book.assign(entity="United Kingdom", unit=UNIT, source_version="Fouquet-Pearson 2012 / OWID legacy 187", role="book_period")
    if book.year.tolist() != list(range(1301, 2007)):
        raise ValueError("Historical years missing or duplicated")
    indicator = json.loads((raw / "legacy_indicator_data.json").read_text())
    if (indicator["years"] != book.year.tolist() or set(indicator["entities"]) != {451}
            or not np.array_equal(indicator["values"], book.value.to_numpy())):
        raise ValueError("Retained legacy export disagrees with indicator 250")
    current = pd.read_csv(raw / "owid_current.csv")
    if current.columns.tolist() != ["Entity", "Code", "Year", "Price of lighting (average)"] or set(current.Entity) != {"United Kingdom"}:
        raise ValueError("Successor schema or geography changed")
    current = current.rename(columns={"Year": "year", "Price of lighting (average)": "value", "Entity": "source_entity"})
    current = current.drop(columns="Code").assign(entity="United Kingdom", unit=UNIT, source_version="Fouquet 2026 / OWID five-year average", role="successor")
    if current.year.tolist() != list(range(1300, 2024)):
        raise ValueError("Successor years missing or duplicated")
    for table in [book, current]:
        if not np.isfinite(table.value).all() or (table.value <= 0).any():
            raise ValueError("Invalid source values")
    # Keep the overlap to reveal source revisions instead of forcing a join.
    extended = pd.concat([book, current[current.year.ge(1995)]], ignore_index=True)
    diagnostic = book[["year", "value"]].merge(current[["year", "value"]], on="year", suffixes=("_legacy", "_2026"))
    diagnostic["relative_revision"] = diagnostic.value_2026 / diagnostic.value_legacy - 1
    return book, extended, diagnostic


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color("#666666")
    ax.tick_params(length=6, labelsize=10, color="#666666")


def plot(book, extended, extension=False):
    fig, ax = plt.subplots(figsize=(8.2, 6.0), dpi=200)
    fig.subplots_adjust(left=.15, right=.985, top=.965, bottom=.235)
    ax.plot(book.year, book.value, lw=2.2, color="#282828")
    ax.set_xlim(1300, 2025 if extension else 2020)
    ax.set_ylim(0, 45000)
    ax.set_xticks(range(1300, 2001, 50))
    ax.set_yticks(range(0, 45001, 5000))
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.set_ylabel("Price in pounds (year 2000)", fontsize=11)
    ax.tick_params(axis="x", labelrotation=48)
    style(ax)
    if extension:
        successor = extended[extended.role.eq("successor")]
        later = successor[successor.year.ge(2007)]
        ax.plot(later.year, later.value, lw=2, ls="--", color="#246b79")
        inset = ax.inset_axes([.54, .49, .43, .43])
        recent = book[book.year.ge(1995)]
        inset.plot(recent.year, recent.value, lw=1.6, color="#282828", label="Legacy")
        inset.plot(successor.year, successor.value, lw=1.6, ls="--", color="#246b79", label="2026 revision")
        inset.axvline(2006, color="#999999", lw=.8, ls=":")
        inset.set(xlim=(1995, 2024), ylim=(1.5, 5), title="Recent years: same units, enlarged scale")
        inset.set_xticks([1995, 2006, 2023])
        inset.set_yticks([2, 3, 4, 5])
        inset.tick_params(labelsize=8, length=3)
        inset.title.set_fontsize(8)
        inset.spines[["top", "right"]].set_visible(False)
        inset.legend(frameon=False, fontsize=7, loc="upper right")
    fig.text(.025, .12, "Figure 17-4: Cost of light, England, 1300-2006" + ("; to 2023" if extension else ""), fontsize=11)
    footer = "Source: Fouquet & Pearson (2012), retained OWID dataset 187. One million lumen-hours."
    footer += "\nOriginal source observations begin in 1301; no year-1300 value invented. Source geography: UK."
    if extension:
        footer += "\nDashed: revised Fouquet (2026) / OWID five-year average; not joined or rescaled to legacy data."
    fig.text(.025, .027, footer, fontsize=7.5, linespacing=1.4)
    mode = "extended" if extension else "book_period"
    path = FIG / f"plots/{mode}/figure_17_4_{mode}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


def main():
    book, extended, diagnostic = load_data()
    directory = FIG / "data/clean"
    directory.mkdir(parents=True, exist_ok=True)
    for name, table in [("book_period", book), ("extended", extended), ("source_versions", diagnostic)]:
        table.to_csv(directory / f"figure_17_4_{name}.csv", index=False)
    plot(book, extended)
    plot(book, extended, True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), dpi=180)
    for ax, limits in zip(axes, [(1300, 1800), (1995, 2006)]):
        subset = diagnostic[diagnostic.year.between(*limits)]
        ax.plot(subset.year, subset.value_legacy, color="#282828", label="Legacy 2012 source")
        ax.plot(subset.year, subset.value_2026, color="#246b79", ls="--", label="2026 revised / 5-year average")
        ax.set(xlabel="Year", ylabel="GBP 2000 per million lumen-hours", title=f"Overlap: {limits[0]}-{limits[1]}")
        style(ax)
        ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    path = FIG / "plots/diagnostics/source_versions.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
