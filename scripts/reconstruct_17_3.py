"""Offline partial reconstruction; unresolved housework values are not invented.

Data and source URLs: figures/17-3/provenance/provenance.md.
No graph digitization, extrapolation, or hidden source substitution.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/17-3"
RAW = FIG / "data/raw"


def load_data():
    rows = []
    for sheet, pairs in {"Basic Facilities": {2: "Running water", 4: "Electricity"},
                         "Appliances": {0: "Refrigerator", 4: "Vacuum", 6: "Washing machine", 10: "Dishwasher", 14: "Microwave", 16: "Stove"}}.items():
        table = pd.read_excel(RAW / "Engines.xls", sheet_name=sheet, header=None)
        for col, series in pairs.items():
            for index, row in table.iterrows():
                year = pd.to_numeric(row[col], errors="coerce")
                value = pd.to_numeric(row[col+1], errors="coerce")
                if pd.notna(year) and pd.notna(value):
                    rows.append({"year": int(year), "series": series, "value": value,
                                 "source": "Greenwood et al. author workbook", "source_cell": f"{sheet}: row {index+1}, columns {col+1}-{col+2}",
                                 "definition": "electric range only" if series == "Stove" else series,
                                 "unit": "percent of households"})
    historical = pd.DataFrame(rows)
    census = pd.read_csv(RAW / "census_2013_table3.csv")
    census["definition"] = census.series
    census["series"] = census.series.replace({"Gas or electric stove": "Stove"})
    book = pd.concat([historical, census[census.year.isin([2005, 2011])]], ignore_index=True).sort_values(["series", "year"])
    if book.duplicated(["series", "year"]).any() or not book.value.between(0, 100).all() or book.series.nunique() != 8:
        raise ValueError("Malformed appliance observations")
    anchors = pd.read_csv(RAW / "housework_published_anchors.csv")
    if anchors.year.tolist() != [1900, 1975] or anchors.value.tolist() != [58, 18]:
        raise ValueError("Original published housework anchors changed")
    bls = pd.read_csv(RAW / "bls_housework_candidates.csv")
    candidates = bls.pivot(index=["year", "sex"], columns="activity", values="hours_per_day").reset_index()
    candidates["broad_household_weekly"] = candidates["Household activities"] * 7
    candidates["core_housework_weekly"] = (candidates.Housework + candidates["Food preparation and cleanup"]) * 7
    candidates["role"] = "diagnostic only; not identified as book endpoint"
    return book, anchors, census, candidates


def main():
    book, anchors, census, candidates = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, frame in [("book_period", book), ("housework_anchors", anchors), ("census_detail", census), ("bls_candidates", candidates)]:
        frame.to_csv(clean / f"figure_17_3_{name}.csv", index=False)
    colors = {"Electricity": "#d5d5d5", "Running water": "#999999", "Refrigerator": "#949494", "Vacuum": "#333333",
              "Washing machine": "#d2d2d2", "Stove": "#666666", "Dishwasher": "#898989", "Microwave": "#b2b2b2"}
    styles = {"Running water": ":", "Refrigerator": "--", "Vacuum": ":", "Microwave": ":"}
    labels = {"Electricity": (1915, 94), "Running water": (1897, 43), "Refrigerator": (1976, 105), "Vacuum": (1972, 91),
              "Washing machine": (1982, 66), "Stove": (1954, 20), "Dishwasher": (1991, 49), "Microwave": (1982, 10)}
    for mode in ["book_period", "extended"]:
        fig, ax = plt.subplots(figsize=(8.6, 6.0), dpi=200)
        fig.subplots_adjust(left=.11, right=.9, top=.96, bottom=.28)
        right = ax.twinx()
        for series, group in book.groupby("series"):
            if series == "Stove":
                for _, segment in group.groupby("definition"):
                    right.plot(segment.year, segment.value, color=colors[series], lw=2.2)
                # Never join electric-only history to gas-or-electric endpoints.
                right.scatter(group[group.year.ge(2005)].year, group[group.year.ge(2005)].value, color=colors[series], s=15)
            else:
                right.plot(group.year, group.value, color=colors[series], lw=2.2, ls=styles.get(series, "-"))
            x, y = labels[series]
            right.text(x, y, "Electric range" if series == "Stove" else series, fontsize=9.5, color="#333333")
        ax.scatter(anchors.year, anchors.value, color="black", s=30, zorder=5)
        ax.text(1894, 51, "Housework: two anchors only", fontsize=9)
        ax.text(1986, 20, "18 h (1975)", fontsize=9)
        right.annotate("Gas/electric stove", xy=(2008, 98.7), xytext=(1994, 87), fontsize=8,
                       arrowprops={"arrowstyle": "-", "color": "#666666", "lw": .6})
        ax.set(xlim=(1890, 2015), ylim=(0, 70), ylabel="Housework hours per week")
        right.set(ylim=(0, 110), ylabel="Households with utility or appliance (%)")
        ax.set_xticks([1890, 1915, 1940, 1965, 1990, 2015])
        ax.set_yticks(range(0, 71, 10))
        right.set_yticks(range(0, 101, 10))
        for axis in [ax, right]:
            axis.spines["top"].set_visible(False)
            axis.tick_params(labelsize=10, length=5)
            for spine in axis.spines.values():
                spine.set_color("#777777")
        title = "Figure 17-3: Utilities, appliances, and housework, US, 1900-2015"
        fig.text(.025, .17, title, fontsize=10.5)
        note = "No verified post-publication extension plotted." if mode == "extended" else "Partial: housework trajectory and 2015 endpoint not recovered."
        fig.text(.025, .035, "Sources: Greenwood et al. (2005) author workbook; Siebens (2013), Table 3.\n"
                 "Housework: two numeric statements in Greenwood et al., not a reconstructed intervening curve.\n"
                 "Stove is electric-only before 1987; gas-or-electric in 2005/2011. Gap prevents a false join.\n" + note, fontsize=7.6, linespacing=1.35)
        path = FIG / f"plots/{mode}/figure_17_3_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(8.6, 4.8), dpi=180)
    for sex, color in {"total": "#707070", "men": "#246b79", "women": "#292929"}.items():
        group = candidates[candidates.sex.eq(sex)].set_index("year").reindex(range(2015, 2026))
        ax.plot(group.index, group.broad_household_weekly, ls="--", color=color, label=sex.title() + ": broad household activities")
        ax.plot(group.index, group.core_housework_weekly, color=color, label=sex.title() + ": cleaning/laundry + meals")
    ax.set(xlabel="Year", ylabel="Hours per week, age 15+", title="17-3: BLS candidates are NOT an identified book extension")
    ax.legend(frameon=False, fontsize=8, loc="center left", bbox_to_anchor=(1.01, .5))
    fig.tight_layout(rect=(0, .05, 1, 1))
    fig.text(.05, .02, "Source: BLS original annual A-1 tables. No annual 2020 estimate; gaps are intentional.", fontsize=8)
    path = FIG / "plots/diagnostics/housework_definition_candidates.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
