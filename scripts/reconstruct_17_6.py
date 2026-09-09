"""Offline leisure reconstruction from original published numeric tables.

Sources: https://www.markaguiar.com/files/leisuretrends.pdf (Table III)
and https://www.bls.gov/tus/tables.htm (original annual A-1 tables).
The book's 2015 population differs from the paper's; do not harmonize silently.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/17-6"
RAW = FIG / "data/raw"
ACTIVITIES = ["Leisure and sports", "Lawn and garden care", "Volunteering (organizational and civic activities)"]


def load_data():
    old = pd.read_csv(RAW / "aguiar_hurst_2007_table_iii.csv")
    earlier = pd.read_csv(RAW / "aguiar_hurst_2006_table3.csv")
    if not old[["year", "sex", "hours_per_week"]].equals(earlier[["year", "sex", "hours_per_week"]]):
        raise ValueError("Historical paper versions differ")
    cells = pd.read_stata(RAW / "cells.dta", convert_categoricals=False)
    if cells.shape != (360, 53) or cells.duplicated(["dataset", "cells"]).any() or not cells.cell_weight.gt(0).all():
        raise ValueError("Unexpected author analysis-cell dataset")
    aggregates = []
    for (year, male), group in cells.groupby(["dataset", "male"]):
        aggregates.append({"year": int(year), "sex": "men" if male == 1 else "women",
                           "unrounded_hours_per_week": np.average(group.leisure_1.astype(float), weights=group.cell_weight.astype(float))})
    old = old.merge(pd.DataFrame(aggregates), on=["year", "sex"], validate="one_to_one")
    if not np.array_equal(old.unrounded_hours_per_week.round(2), old.hours_per_week):
        raise ValueError("Original analysis cells fail published Table III cross-check")
    old["hours_per_week"] = old.unrounded_hours_per_week.round(2)
    activities = pd.read_csv(RAW / "bls_activity_tables.csv")
    for _, group in activities.groupby(["year", "sex"]):
        if sorted(group.activity.tolist()) != sorted(ACTIVITIES + ["Animals and pets"]):
            raise ValueError("Incomplete or duplicate BLS basket")
    # Verify the original 2015 news-release table independently of the A-1 PDFs.
    release = pd.read_html(RAW / "bls_2015_table1.html")[0]
    labels = release[("Activity", "Activity")].astype(str).str.strip()
    for activity in ACTIVITIES:
        for sex in ["men", "women"]:
            actual = float(release.loc[labels.eq(activity), ("Average hours per day, civilian population", sex.title())].item())
            retained = activities.loc[activities.year.eq(2015) & activities.sex.eq(sex) & activities.activity.eq(activity), "hours_per_day"].item()
            if actual != retained:
                raise ValueError("2015 release and retained A-1 table disagree")
    current = activities[activities.sex.ne("total")].pivot(index=["year", "sex"], columns="activity", values="hours_per_day").reset_index()
    current["hours_per_week"] = (current[ACTIVITIES].sum(axis=1) * 7).round(2)
    current["with_pet_care_hours_per_week"] = (current.hours_per_week + current["Animals and pets"] * 7).round(2)
    current["population"] = "civilian noninstitutional population 15+; not fixed-demographic reweighted"
    current["version"] = "BLS annual A-1 tables, retrieved 2026-09-09"
    current["measure"] = "leisure/sports + lawn/garden + volunteering; book endpoint definition"
    for sex, group in old.groupby("sex"):
        if group.year.tolist() != [1965, 1975, 1985, 1993, 2003]:
            raise ValueError("Unexpected historical years")
    if sorted(current.year.unique()) != [2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025]:
        raise ValueError("BLS coverage changed; inspect unavailable 2020 explicitly")
    book = pd.concat([old, current[current.year.eq(2015)]], ignore_index=True)
    book["unit"] = "hours per week"
    current["unit"] = "hours per week"
    return old, book, current, activities


def main():
    old, book, current, activities = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, frame in [("book_period", book), ("extended", current), ("activities", activities)]:
        frame.to_csv(clean / f"figure_17_6_{name}.csv", index=False)
    pd.read_stata(RAW / "cells.dta", convert_categoricals=False).to_csv(clean / "figure_17_6_author_cells.csv", index=False)
    colors = {"men": "#aaaaaa", "women": "#252525"}
    for mode in ["book_period", "extended"]:
        fig, ax = plt.subplots(figsize=(8.2, 6.0), dpi=200)
        fig.subplots_adjust(left=.105, right=.97, top=.96, bottom=.28)
        for sex, color in colors.items():
            historic = old[old.sex.eq(sex)]
            endpoint = book[book.sex.eq(sex) & book.year.eq(2015)]
            ax.plot(historic.year, historic.hours_per_week, color=color, lw=2.6)
            bridge = pd.concat([historic.tail(1), endpoint])
            ax.plot(bridge.year, bridge.hours_per_week, color=color, lw=2.3, ls=":")
            ax.scatter(endpoint.year, endpoint.hours_per_week, color=color, s=18, zorder=3, clip_on=False)
            if mode == "extended":
                later = current[current.sex.eq(sex)].set_index("year").reindex(range(2015, 2026))
                ax.plot(later.index, later.hours_per_week, color=color, ls="--", lw=2.3)
            ax.text((2004 if mode == "book_period" else 1998) if sex == "men" else 2004,
                    40.8 if sex == "men" else 36.2,
                    sex.title(), fontsize=12, color="#252525")
        ax.set(xlim=(1965, 2026 if mode == "extended" else 2015), ylim=(29, 43), ylabel="Leisure hours per week")
        ax.set_xticks(range(1965, 2026 if mode == "extended" else 2016, 10))
        ax.set_yticks(range(29, 44, 2))
        ax.yaxis.label.set_size(12)
        ax.tick_params(length=6, labelsize=11)
        ax.spines[["top", "right"]].set_visible(False)
        for side in ["left", "bottom"]:
            ax.spines[side].set_color("#666666")
            ax.spines[side].set_linewidth(1.2)
        fig.text(.025, .155, "Figure 17-6: Leisure time, US, 1965-2015" + ("; BLS continuation to 2025" if mode == "extended" else ""), fontsize=11)
        continuation_note = ("Dashed later BLS data: age 15+; no annual 2020 estimate." if mode == "extended" else
                             "2015 endpoint follows the cited BLS basket; source values are not shifted to match book.")
        fig.text(.025, .035, "Sources: Aguiar & Hurst (2007), Table III; BLS ATUS original annual tables.\n"
                 "Dotted 2003-2015 connector marks a population/definition change, not a comparable trend.\n"
                 + continuation_note + "\n"
                 "Paper: nonretired nonstudents 21-65, fixed demographics; BLS basket does not add pet care.", fontsize=7.5, linespacing=1.4)
        path = FIG / f"plots/{mode}/figure_17_6_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(8.2, 4.8), dpi=180)
    for sex, color in colors.items():
        group = current[current.sex.eq(sex)].set_index("year").reindex(range(2015, 2026))
        ax.plot(group.index, group.hours_per_week, color=color, label=sex.title() + ": book BLS basket", lw=2)
        ax.plot(group.index, group.with_pet_care_hours_per_week, color=color, ls="--", label=sex.title() + ": adding pet care", lw=2)
    ax.set(xlabel="Year", ylabel="Hours per week", title="Figure 17-6: activity-definition sensitivity (age 15+)")
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    path = FIG / "plots/diagnostics/pet_care_sensitivity.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
