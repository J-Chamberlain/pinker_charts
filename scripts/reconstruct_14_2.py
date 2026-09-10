"""Reconstruct from archived numerical chart data, never image coordinates.

Book-era upload June21,2016: https://web.archive.org/web/20180913134846id_/https://ourworldindata.org/grapher/data/variables/358.json?v=3
Successor: https://dataverse.harvard.edu/api/access/datafile/7209241
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/14-2"
COUNTRIES = {385: "Norway", 710: "China", 731: "North Korea", 732: "South Korea"}
STYLES = {"Norway": ("#252525", "--", 2.5), "World": ("#252525", "-", 3.2),
          "South Korea": ("#aaaaaa", "-", 2.5), "China": ("#aaaaaa", ":", 2.5),
          "North Korea": ("#646464", "-", 2.5)}


def load_data():
    payload = json.loads((FIG / "data/raw/owid_variable358_2018.json").read_text())
    variable = payload["variables"]["358"]
    all_old = pd.DataFrame({"year": variable["years"], "entity_id": variable["entities"],
                            "value": pd.to_numeric(variable["values"])})
    all_old["series"] = all_old.entity_id.map(lambda e: payload["entityKey"][str(e)]["name"])
    book = all_old[all_old.series.isin(STYLES)].copy()
    if book.duplicated(["year", "series"]).any() or not book.groupby("series").year.nunique().eq(66).all():
        raise ValueError("Original five annual series are incomplete")
    book["unit"] = "Original latent human rights protection score"
    book["source_version"] = "OWID variable358; upload2016-06-21; archive2018-09-13"
    successor = pd.read_csv(FIG / "data/raw/fariss_v4_02_2021.csv")
    successor = successor[successor.COW.isin(COUNTRIES)].copy()
    successor = successor.rename(columns={"YEAR": "year", "theta_mean": "value",
                                         "theta_q025": "lower_95", "theta_q975": "upper_95"})
    successor["series"] = successor.COW.map(COUNTRIES)
    successor["unit"] = "Revised v4.02 latent human rights protection score"
    successor["source_version"] = "Fariss/Kenwick/Reuning v4.02 through2021"
    successor = successor[["year", "series", "value", "theta_sd", "lower_95", "upper_95", "unit", "source_version"]]
    if successor.duplicated(["year", "series"]).any() or successor.year.max() != 2021:
        raise ValueError("Unexpected successor coverage")
    world = book[book.series.eq("World")][["year", "value"]].rename(columns={"value": "provider_world"})
    mean = all_old[all_old.series.ne("World")].groupby("year").value.agg(["mean", "count"]).reset_index()
    diagnostic = world.merge(mean, on="year").rename(columns={"mean": "unweighted_country_mean", "count": "country_count"})
    diagnostic["difference"] = diagnostic.provider_world - diagnostic.unweighted_country_mean
    return book, successor, diagnostic


def historical(ax, book):
    for name, (color, style, width) in STYLES.items():
        group = book[book.series.eq(name)].sort_values("year")
        ax.plot(group.year, group.value, color=color, ls=style, lw=width,
                solid_capstyle="round", dash_capstyle="round")
    for name, x, y in [("Norway", 2007, 2.7), ("World", 2003, 1.0),
                       ("South Korea", 2003, -.02), ("China", 2007, -1.03),
                       ("North Korea", 2003, -2.43)]:
        ax.text(x, y, name, fontsize=13, weight="bold" if name == "World" else "normal")
    ax.set(xlim=(1945, 2015), ylim=(-3, 3.65), ylabel="Human rights protection")
    ax.set_xticks(range(1945, 2016, 5))
    ax.set_yticks(range(-3, 4))
    ax.tick_params(labelsize=10, length=7)
    ax.spines[["top", "right"]].set_visible(False)


def main():
    book, successor, diagnostic = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, data in [("book_period", book), ("successor", successor), ("diagnostic", diagnostic)]:
        data.to_csv(clean / f"figure_14_2_{name}.csv", index=False)
    for mode in ["book_period", "extended"]:
        extended = mode == "extended"
        fig = plt.figure(figsize=(9, 9 if extended else 6.8), dpi=200)
        ax = fig.add_axes([.11, .49 if extended else .26, .87, .48 if extended else .71])
        historical(ax, book)
        if extended:
            extra = fig.add_axes([.11, .18, .87, .23])
            colors = {"Norway": "#252525", "South Korea": "#197f7c", "China": "#a33b7d", "North Korea": "#666666"}
            for name, group in successor[successor.year.ge(2000)].groupby("series"):
                color = colors[name]
                prior, later = group[group.year.le(2014)], group[group.year.ge(2014)]
                extra.plot(prior.year, prior.value, color=color, ls=":", lw=1.7)
                extra.plot(later.year, later.value, color=color, ls="--", lw=1.7, label=name)
            extra.axvline(2014, lw=.6, color="#888888")
            extra.set(xlim=(2000, 2022), ylim=(-3.2, 5), ylabel="Revised score",
                      title="Separate v4.02 estimates: dotted overlap, dashed after 2014")
            extra.set_xticks([2000, 2005, 2010, 2014, 2018, 2021])
            extra.spines[["top", "right"]].set_visible(False)
            extra.legend(frameon=False, ncols=4, fontsize=8, loc="upper center", bbox_to_anchor=(.5, .85))
        fig.text(.025, .115 if extended else .15, "Figure 14-2: Human rights, 1949-2014", fontsize=12)
        fig.text(.025, .025, "Source: OWID/Roser2016, Fariss2014; original numerical chart-data archive.\n"
                 "World is the provider's supplied series, NOT a mean calculated from this country file.\n"
                 + ("Revised successor has different historical estimates/scale; no forced join or invented World extension."
                    if extended else "No values digitized or shifted to fit the image. Source-series / zero-level discrepancy remains under review."), fontsize=8)
        path = FIG / f"plots/{mode}/figure_14_2_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 4), dpi=180)
    ax.plot(diagnostic.year, diagnostic.provider_world, label="Archived provider World", color="black")
    ax.plot(diagnostic.year, diagnostic.unweighted_country_mean, label="Rejected substitute: mean of country file", ls="--", color="#a33b7d")
    ax.set(title="Figure 14-2: World aggregation is not interchangeable", xlabel="Year", ylabel="Original score")
    ax.legend(frameon=False)
    fig.tight_layout()
    path = FIG / "plots/diagnostics/world_aggregation.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
