"""Recreate the exact cited HumanProgress World series and separate Polity update.

Original: https://web.archive.org/web/20170427220920id_/http://humanprogress.org/f1/2560
Successors: https://www.systemicpeace.org/inscr/ (p4v2018 and p5v2018).
Full raw sources are local-only; recover_14_1.py produces retained aggregates.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/14-1"


def load_data():
    old = pd.read_csv(FIG / "data/raw/hp_world_2016.csv").rename(
        columns={"value": "score", "generated": "provider_generated"})
    if old.year.tolist() != list(range(1800, 2016)) or not old.score.between(-10, 10).all():
        raise ValueError("Unexpected World coverage or score range")
    old["source_version"] = "HumanProgress2560 July18,2016"
    old["unit"] = "HumanProgress World average; polity score -10 to10"
    successors = []
    for release in ["p4v2015", "p4v2018", "p5v2018"]:
        data = pd.read_csv(FIG / f"data/raw/{release}_world_aggregates.csv")
        # The current p5v2018 file includes isolated US-only 2019/2020 rows.
        # Those must NEVER be interpreted as a subsequent global estimate.
        data = data[data.year.between(1800, 2015 if release == "p4v2015" else 2018)].copy()
        if data.year.ge(2015).any() and data.loc[data.year.ge(2015), "n_polity2"].min() < 150:
            raise ValueError("Incomplete global coverage")
        data["release"] = release
        successors.append(data)
    current = pd.concat(successors, ignore_index=True)
    diagnostic = current.merge(old[["year", "score"]], on="year", how="left")
    diagnostic["polity2_minus_hp"] = diagnostic.polity2_mean - diagnostic.score
    return old, current, diagnostic


def main():
    old, current, diagnostic = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, data in [("book_period", old), ("successor", current), ("diagnostic", diagnostic)]:
        data.to_csv(clean / f"figure_14_1_{name}.csv", index=False)
    for mode in ["book_period", "extended"]:
        fig = plt.figure(figsize=(8.5, 6.5 if mode == "book_period" else 8.5), dpi=200)
        ax = fig.add_axes([.12, .27 if mode == "book_period" else .49, .855, .69 if mode == "book_period" else .47])
        ax.plot(old.year, old.score, color="#252525", lw=2.7)
        ax.set(xlim=(1800, 2020), ylim=(-8, 5), ylabel="Democracy vs. autocracy score")
        ax.set_xticks(range(1800, 2021, 20))
        ax.set_yticks(range(-8, 5, 2))
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=11, length=6)
        value = old.set_index("year").loc[2008, "score"]
        ax.annotate("", xy=(2008, value-.1), xytext=(2008, value-1.65),
                    arrowprops={"arrowstyle": "->", "color": "#d0d0d0", "lw": 1.5})
        if mode == "extended":
            extra = fig.add_axes([.12, .185, .855, .20])
            overlap = old[old.year.ge(2000)]
            extra.plot(overlap.year, overlap.score, color="#252525", lw=2, label="Original HP aggregation")
            for release, color, label in [("p4v2018", "#197f7c", "Polity IV 2018"),
                                           ("p5v2018", "#a33b7d", "Polity5 2018")]:
                data = current[(current.release == release) & current.year.ge(2000)]
                prior, later = data[data.year.le(2015)], data[data.year.ge(2015)]
                extra.plot(prior.year, prior.polity2_mean, ls=":", color=color, lw=1.8)
                extra.plot(later.year, later.polity2_mean, ls="--", color=color, lw=1.8, marker=".", label=label)
            extra.axvline(2015, lw=.6, color="#888888")
            extra.set(xlim=(2000, 2019), ylim=(3.0, 4.5), ylabel="Democracy score", title="Separate source aggregates: dotted overlap, dashed after 2015")
            extra.set_xticks([2000, 2005, 2010, 2015, 2018])
            extra.spines[["top", "right"]].set_visible(False)
            extra.legend(frameon=False, fontsize=8, loc="lower right")
        fig.text(.025, .15 if mode == "book_period" else .105,
                 "Figure 14-1: Democracy versus autocracy, 1800-2015", fontsize=11)
        fig.text(.025, .035, "Source: HumanProgress dataset 2560, July 2016; based on Polity IV 2015.\n"
                 "Exact provider World average, including provider-generated values; not a sum or population-weighted mean.\n"
                 + ("Successor panel uses different coverage/handling; no forced join. Latest broad coverage: 2018."
                    if mode == "extended" else "Arrow marks 2008. Country coverage and missing-data treatment differ from all-country Polity averages."), fontsize=8)
        path = FIG / f"plots/{mode}/figure_14_1_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(8.5, 6), sharex=True, dpi=180)
    for name, group in diagnostic.groupby("release"):
        axes[0].plot(group.year, group.polity2_minus_hp, label=name)
        axes[1].plot(group.year, group.n_polity2, label=name)
    axes[0].set(title="Figure 14-1: source aggregation / coverage differences", ylabel="Mean polity2 minus HP")
    axes[0].axhline(0, lw=.6, color="gray")
    axes[0].legend(frameon=False)
    axes[1].set(ylabel="Countries with polity2", xlabel="Year")
    fig.tight_layout()
    path = FIG / "plots/diagnostics/aggregation_and_coverage.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
