"""Offline work-hours reconstruction; never offset data to fit book pixels.

Source: https://personal.lse.ac.uk/minns/huberman_minns_eeh_2007.pdf Table 1.
Retained OWID Git exports and precise URLs: figures/17-1/source_logs/downloads.json.
No comparable successor is plotted. The extended artifact explicitly says so.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/17-1"
YEARS = [1870, 1880, 1890, 1900, 1913, 1929, 1938, 1950, 1960, 1970, 1980, 1990, 2000]


def load_data():
    raw = pd.read_csv(FIG / "data/raw/days_hours.csv")
    total, male, female = raw.columns[2:5]
    if "(total)" not in total or "(male)" not in male or "(female)" not in female:
        raise ValueError("Source schema changed")
    selected = raw[raw.Entity.isin(["Old World", "United States", "Old World (weighted)"])].copy()
    rows = []
    for entity, group in selected.groupby("Entity"):
        if group.Year.tolist() != YEARS:
            raise ValueError("Source year coverage changed")
        for _, row in group.iterrows():
            year = int(row.Year)
            if year == 2000:
                if pd.notna(row[total]) or not np.isfinite([row[male], row[female]]).all():
                    raise ValueError("Unexpected 2000 sex/total structure")
                # Source table precision is one decimal; CSV contains float32 noise.
                value = (round(row[male], 1) + round(row[female], 1)) / 2
                method = "equal mean of male and female source-table values"
            else:
                value = round(row[total], 1)
                method = "published total, source-table precision (one decimal)"
            rows.append({"source_entity": entity, "entity": "Western Europe" if entity == "Old World" else entity,
                         "year": year, "weekly_hours": value, "unit": "hours_per_week",
                         "source_version": "Huberman-Minns 2007 / OWID archived export", "transformation": method})
    all_series = pd.DataFrame(rows)
    if not np.isfinite(all_series.weekly_hours).all() or not all_series.weekly_hours.between(0, 168).all():
        raise ValueError("Invalid weekly hours")
    book = all_series[~all_series.source_entity.eq("Old World (weighted)")].reset_index(drop=True)
    weekly = pd.read_csv(FIG / "data/raw/working_hours.csv")
    usa = weekly[weekly.Entity.eq("United States")]
    if usa.Year.tolist() != YEARS or not np.allclose(usa.iloc[:, 2], book[book.entity.eq("United States")].weekly_hours):
        raise ValueError("Independent OWID source exports disagree for US")
    return book, all_series


def main():
    book, diagnostic = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    book.to_csv(clean / "figure_17_1_book_period.csv", index=False)
    diagnostic.to_csv(clean / "figure_17_1_weighting_diagnostic.csv", index=False)
    for mode in ["book_period", "extended"]:
        fig, ax = plt.subplots(figsize=(8.2, 5.9), dpi=200)
        fig.subplots_adjust(left=.11, right=.975, top=.96, bottom=.225)
        for entity, color in [("Western Europe", "#a0a0a0"), ("United States", "#252525")]:
            series = book[book.entity.eq(entity)]
            ax.plot(series.year, series.weekly_hours, color=color, lw=2.2)
        ax.set(xlim=(1870, 2000), ylim=(0, 70), ylabel="Weekly work hours")
        ax.set_xticks(range(1870, 2001, 10))
        ax.set_yticks(range(0, 71, 10))
        ax.text(1960, 49, "Western Europe", fontsize=12)
        ax.text(1949, 33, "United States", fontsize=12)
        ax.spines[["top", "right"]].set_visible(False)
        for spine in ["left", "bottom"]:
            ax.spines[spine].set_color("#666666")
        ax.tick_params(length=6, labelsize=9)
        fig.text(.025, .12, "Figure 17-1: Work hours, Western Europe and US, 1870-2000", fontsize=11)
        note = "Source: Huberman & Minns (2007), Table 1, via retained OWID exports."
        note += "\nFull-time production workers; Western Europe = unweighted Old World source aggregate."
        note += "\n2000: equal-sex mean. No comparable post-2000 extension plotted."
        fig.text(.025, .033, note, fontsize=7.6, linespacing=1.4)
        path = FIG / f"plots/{mode}/figure_17_1_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(8.2, 4.7), dpi=180)
    for entity, style in [("Western Europe", "-"), ("Old World (weighted)", "--")]:
        group = diagnostic[diagnostic.entity.eq(entity)]
        ax.plot(group.year, group.weekly_hours, ls=style, label=entity)
    ax.set(xlabel="Year", ylabel="Weekly hours", title="Figure 17-1: alternative regional weighting, not a fitted correction")
    ax.legend(frameon=False)
    fig.tight_layout()
    path = FIG / "plots/diagnostics/weighting.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
