#!/usr/bin/env python3
"""Reconstruct Figure 5-3 from preserved OWID dataset 522.

The preserved table combines Gapminder (2010) historical observations with
World Bank (2015) estimates without adjustment. Values are ratios per 100,000
live births; the book axis is percent, so percent = ratio / 1,000.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from build_review_baseline import render_comparison


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "5-3"
RAW = FIG / "data" / "raw"
CLEAN = FIG / "data" / "clean"
PLOTS = FIG / "plots"
COUNTRIES = ["Malaysia", "Sweden", "United States", "Ethiopia"]
COLORS = {
    "Malaysia": "#aaaaaa",
    "Sweden": "#111111",
    "United States": "#888888",
    "Ethiopia": "#cccccc",
}


def load_preserved() -> tuple[dict, list[dict]]:
    payload = json.loads((RAW / "owid_522_maternal_mortality.tab").read_text())
    rows = [
        {"Entity": entity, "Year": int(year), "mmr_per_100000": float(value)}
        for entity, year, value in payload["data"]
        if entity in COUNTRIES
    ]
    return payload, rows


def recover_early_sweden(rows: list[dict]) -> tuple[list[dict], dict]:
    # Source table, not chart digitization: Hanson GD010, Tabellverket counts.
    # https://www.gapminder.org/documentation/documentation/gapdata010.xls
    path = RAW / "gapminder_gd010_gapdata010.xls"
    frame = pd.read_excel(path, sheet_name="Tabelle1")
    sweden = frame[frame["Country"].eq("Sweden")].copy()
    for col in ["year", "MMR", "Live Births", "Maternal deaths"]:
        sweden[col] = pd.to_numeric(sweden[col], errors="raise")
    early = sweden[sweden.year.between(1751, 1799)]
    if set(early.year) != set(range(1751, 1800)) or len(early) != 49:
        raise ValueError("Early Sweden source must have exactly 49 unique years")
    count_error = (early.MMR - 100000 * early["Maternal deaths"] / early["Live Births"]).abs().max()
    if count_error > 1e-8:
        raise ValueError("Maternal mortality ratios do not reproduce independent birth/death columns")
    observed = {r["Year"]: r["mmr_per_100000"] for r in rows if r["Entity"] == "Sweden"}
    overlap = sweden[sweden.year.between(1800, 1949) & sweden.year.isin(observed)]
    overlap_error = max(abs(r.MMR - observed[int(r.year)]) for r in overlap.itertuples())
    if overlap_error > .051:
        raise ValueError("Historical overlap exceeds OWID one-decimal rounding tolerance")
    new = [{"Entity": "Sweden", "Year": int(r.year), "mmr_per_100000": r.MMR} for r in early.itertuples()]
    if any(r["Year"] in observed for r in new):
        raise ValueError("Recovered rows must not replace preserved OWID values")
    audit = {"source_path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
             "source_url": "https://www.gapminder.org/documentation/documentation/gapdata010.xls",
             "rows_added": len(new), "year_range": [1751, 1799], "count_ratio_max_error": count_error,
             "overlap_year_range": [1800, 1949], "overlap_rows": len(overlap), "overlap_max_mmr_error": overlap_error,
             "policy": "Add missing early Sweden only. Keep OWID 522 for all existing rows; later source versions differ and are not overwritten."}
    return rows + new, audit


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["Entity", "Year", "mmr_per_100000", "maternal_mortality_percent"],
            lineterminator="\n",
        )
        writer.writeheader()
        for row in sorted(rows, key=lambda item: (item["Entity"], item["Year"])):
            writer.writerow(
                {
                    **row,
                    "maternal_mortality_percent": f'{row["mmr_per_100000"] / 1000:.6f}',
                }
            )


def validate_clean(path: Path, source_rows: list[dict], tolerance: float = 5e-7) -> None:
    expected = {(row["Entity"], row["Year"]): row["mmr_per_100000"] / 1000 for row in source_rows}
    with path.open(newline="") as handle:
        observed = {
            (row["Entity"], int(row["Year"])): float(row["maternal_mortality_percent"])
            for row in csv.DictReader(handle)
        }
    if set(observed) != set(expected):
        raise ValueError(f"Row keys differ for {path}")
    max_error = max(abs(observed[key] - expected[key]) for key in expected)
    if max_error > tolerance:
        raise ValueError(f"Maximum error {max_error} exceeds {tolerance} for {path}")


def draw_chart(rows: list[dict], output: Path, end_year: int, extension: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.7), dpi=200)
    for country in COUNTRIES:
        series = sorted(
            (row for row in rows if row["Entity"] == country and row["Year"] <= end_year),
            key=lambda row: row["Year"],
        )
        x = [row["Year"] for row in series]
        y = [row["mmr_per_100000"] / 1000 for row in series]
        historical = [i for i, year in enumerate(x) if year <= 2013]
        if historical:
            last = historical[-1] + 1
            ax.plot(x[:last], y[:last], color=COLORS[country], linewidth=2.1)
        later = [i for i, year in enumerate(x) if year >= 2013]
        if extension and len(later) > 1:
            first = later[0]
            ax.plot(x[first:], y[first:], color=COLORS[country], linewidth=2.1, linestyle="--")

    labels = {
        "Malaysia": (1935, 1.10),
        "Sweden": (1848, 0.25),
        "United States": (1888, 0.53),
        "Ethiopia": (1961, 1.23),
    }
    for country, (x, y) in labels.items():
        ax.text(x, y, country, color="#222222", fontsize=11)
    ax.set_xlim(1750, 2020)
    ax.set_ylim(0, 1.5)
    ax.set_xticks(list(range(1750, 2011, 20)))
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5])
    ax.set_yticklabels(["0", "0.25", "0.5", "0.75", "1.0", "1.25", "1.5"])
    ax.set_ylabel("Percentage of mothers dying in childbirth")
    ax.set_title(
        "Figure 5-3: Maternal mortality, 1751-2013"
        + (" (same-source continuation to 2015)" if extension else ""),
        loc="left",
        fontsize=12,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.tick_params(labelsize=8)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    if extension:
        ax.axvline(2013, color="#777777", linewidth=0.8, linestyle=":")
        ax.text(.99, .98, "Dashed: 2014-15", transform=ax.transAxes, ha="right", va="top", fontsize=8, color="#555555")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)




def write_checksums() -> None:
    paths = [path for path in FIG.rglob("*") if path.is_file() and "checksums" not in path.parts]
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(FIG)}" for path in sorted(paths)]
    (FIG / "checksums" / "sha256sums.txt").write_text("\n".join(lines) + "\n")


def main() -> None:
    _, rows = load_preserved()
    rows, audit = recover_early_sweden(rows)
    (FIG / "provenance/early_sweden_validation.json").write_text(json.dumps(audit, indent=2) + "\n")
    book = [row for row in rows if 1751 <= row["Year"] <= 2013]
    continuation = [row for row in rows if 1751 <= row["Year"] <= 2015]
    book_csv = CLEAN / "figure_5_3_book_period_clean.csv"
    extension_csv = CLEAN / "figure_5_3_same_source_continuation_clean.csv"
    write_csv(book_csv, book)
    write_csv(extension_csv, continuation)
    validate_clean(book_csv, book)
    validate_clean(extension_csv, continuation)
    book_plot = PLOTS / "book_period" / "figure_5_3_book_period_reconstruction.png"
    ext_plot = PLOTS / "extended" / "figure_5_3_same_source_continuation.png"
    draw_chart(book, book_plot, 2013)
    draw_chart(continuation, ext_plot, 2015, extension=True)
    reference = ROOT / "references/figures/figure_5_3.png"
    caption = (FIG / "captions/caption.txt").read_text()
    render_comparison(reference, book_plot, PLOTS / "comparisons" / "figure_5_3_book_period_review.png", "Figure 5-3: Maternal mortality", "Recovered-data reconstruction", caption)
    render_comparison(reference, ext_plot, PLOTS / "comparisons" / "figure_5_3_extended_review.png", "Figure 5-3: Maternal mortality", "Same-source continuation", caption)
    write_checksums()


if __name__ == "__main__":
    main()
