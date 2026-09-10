"""Basic education from archived OWID/OECD numeric records, never chart pixels.

Sources: figures/16-2/provenance/provenance.md and source_logs/downloads.json.
Current OWID's post-2015 projections are diagnostic, not an observed extension.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/16-2"
RAW = FIG / "data/raw"
NAMES = {"World": "World", "Western Europe": "Western Europe", "Eastern Europe": "Eastern Europe",
         "Western Offshoots": "US, Canada, Australia, NZ", "Latin America and Caribbean": "Latin America",
         "East Asia": "East Asia", "South and South-East Asia": "South and Southeast Asia",
         "Middle East and North Africa": "Middle East", "Sub-Sahara Africa": "Sub-Saharan Africa"}


def load_data():
    archive = pd.read_csv(RAW / "owid_regional_archive.csv")
    data = archive.melt(id_vars="year", value_vars=list(NAMES), var_name="source_series", value_name="value").dropna()
    early = archive.loc[archive.year.eq(1820), "World ('Best Guess')"].item()
    data = pd.concat([data, pd.DataFrame([{"year": 1820, "source_series": "World", "value": early}])], ignore_index=True)
    data["series"] = data.source_series.map(NAMES)
    data["unit"] = "percent of adults age 15+ with basic education; historical estimates"
    data["method"] = data.year.map(lambda year: "OECD regression-based backcast" if year == 1820 else "OECD decadal estimate")
    data = data.sort_values(["series", "year"])
    if data.duplicated(["series", "year"]).any() or data.series.nunique() != 9 or not data.value.between(0, 100).all():
        raise ValueError("Malformed education observations")
    # Original workbook labels its final two rows in reverse chronological order.
    # Preserve both source and interpreted years; printed Table 5.3 + OWID agree.
    table = pd.read_excel(RAW / "oecd_table_5_3.xls", header=None).iloc[10:25, :10].copy()
    table.columns = ["source_year", "Western Europe", "Eastern Europe", "Western Offshoots", "Latin America and Caribbean",
                     "East Asia", "South and South-East Asia", "Middle East and North Africa", "Sub-Sahara Africa", "World"]
    if table.source_year.tolist() != list(range(1870, 2000, 10)) + [2010, 2000]:
        raise ValueError("OECD workbook layout/version changed; reassess year correction")
    table["year"] = list(range(1870, 2011, 10))
    check = table.melt(id_vars=["year", "source_year"], var_name="source_series", value_name="oecd_value")
    check["oecd_value"] = pd.to_numeric(check.oecd_value, errors="coerce")
    check = check.dropna().merge(data, on=["year", "source_series"], validate="one_to_one")
    check["difference_pp"] = check.value - check.oecd_value
    if len(check) != 133 or check.difference_pp.abs().max() > 1e-10:
        raise ValueError("Archived CSV fails original OECD table cross-check")
    current = pd.read_csv(RAW / "owid_current.csv")
    current = current[current.Entity.isin(["World", "Africa", "Asia", "Europe", "Oceania", "North America", "South America"])].copy()
    current = current.rename(columns={"Entity": "series", "Year": "year", "Share of population with some formal education": "value"})
    current["role"] = current.year.map(lambda year: "projection_not_observed_extension" if year >= 2015 else "different_source_historical_candidate")
    current["age_warning"] = "chart subtitle says15+; variable title says15-64; unresolved"
    return data, check, current


def main():
    data, check, current = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, frame in [("book_period", data), ("oecd_crosscheck", check), ("rejected_successor", current)]:
        frame.to_csv(clean / f"figure_16_2_{name}.csv", index=False)
    styles = {"World": ("#222222", "-", 3.3), "US, Canada, Australia, NZ": ("#909090", "--", 2.2),
              "Western Europe": ("#aaaaaa", "-", 2.2), "Eastern Europe": ("#222222", ":", 2.2),
              "Latin America": ("#d0d0d0", "-", 2.2), "East Asia": ("#222222", "--", 2.2),
              "South and Southeast Asia": ("#666666", "-", 2.2), "Middle East": ("#d0d0d0", "--", 2.2),
              "Sub-Saharan Africa": ("#aaaaaa", ":", 2.2)}
    labels = {"World": (1827, 23), "US, Canada, Australia, NZ": (1847, 92), "Western Europe": (1836, 65),
              "Eastern Europe": (1890, 65), "Latin America": (1956, 84), "East Asia": (1945, 65),
              "South and Southeast Asia": (1910, 21), "Middle East": (1878, 8), "Sub-Saharan Africa": (1970, 17)}
    for mode in ["book_period", "extended"]:
        fig, ax = plt.subplots(figsize=(9, 6.8), dpi=200)
        fig.subplots_adjust(left=.12, right=.97, top=.94, bottom=.28)
        for series, group in data.groupby("series"):
            color, style, width = styles[series]
            ax.plot(group.year, group.value, color=color, ls=style, lw=width, solid_capstyle="round", dash_capstyle="round")
            x, y = labels[series]
            label = series.replace("US, Canada, Australia, NZ", "US, Canada,\nAustralia, NZ").replace("South and Southeast Asia", "South and\nSoutheast Asia").replace("Sub-Saharan Africa", "Sub-Saharan\nAfrica")
            ax.text(x, y, label, fontsize=11, weight="bold" if series == "World" else "normal")
        ax.set(xlim=(1819, 2011), ylim=(0, 102), ylabel="Adults (15+) with basic education (%)")
        ax.set_xticks(range(1820, 2011, 10))
        ax.set_yticks(range(0, 101, 20))
        ax.tick_params(axis="x", rotation=45)
        for label in ax.get_xticklabels():
            label.set_ha("right")
        ax.spines[["top", "right"]].set_visible(False)
        fig.text(.025, .15, "Figure 16-2: Basic education, 1820-2010", fontsize=11)
        note = "No observed extension: current successor contains projections and different regions/age metadata." if mode == "extended" else "1820 World is a model-based best guess. Sparse decadal estimates, not annual observations."
        fig.text(.025, .035, "Sources: OWID archived September 2015; van Leeuwen & van Leeuwen-Li, OECD (2014), Table 5.3.\n"
                 "Original regional table cross-checked; no values digitized. Small book-level offsets remain.\n" + note, fontsize=8, linespacing=1.4)
        path = FIG / f"plots/{mode}/figure_16_2_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=180)
    for series, group in current.groupby("series"):
        history = group[group.year.lt(2015)]
        future = group[group.year.ge(2010)]
        line, = ax.plot(history.year, history.value, lw=1.4, label=series)
        ax.plot(future.year, future.value, color=line.get_color(), ls="--", lw=1.4)
    ax.axvline(2015, color="#888888", lw=.8)
    ax.set(xlim=(1990, int(current.year.max()) + 1), ylim=(0, 105), xlabel="Year", ylabel="Percent with some formal education",
           title="Rejected as extension: post-2015 values are projections")
    ax.legend(frameon=False, ncol=2, fontsize=8, loc="lower right")
    fig.tight_layout(rect=(0, .08, 1, 1))
    fig.text(.03, .025, "OWID current export, different regions and contradictory age metadata. Not observed book-series updates.", fontsize=8)
    path = FIG / "plots/diagnostics/rejected_projection_successor.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
