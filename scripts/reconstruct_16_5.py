"""Reproduce regional IQ-gain trajectories from the retained 2015 OWID dataset.

Original study: https://doi.org/10.1177/1745691615577701
Pinned numeric data and download URL: figures/16-5/data/raw/owid_iq.*
Different baselines/tests prohibit comparison of regional IQ levels.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/16-5"
COLUMN = "Fullscale IQ change by region 1909-2013 (Pietschnig and Voracek (2015))"
NAMES = {"Global": "World", "America": "Americas", "Oceania": "Australia & NZ"}
STYLES = {"World": ("#222222", "-", 3.3), "Americas": ("#888888", "-", 2.6),
          "Asia": ("#dddddd", "-", 2.6), "Europe": ("#bbbbbb", "-", 2.6),
          "Australia & NZ": ("#aaaaaa", "-", 2.6), "Africa": ("#222222", ":", 2.6)}


def load_data():
    raw = pd.read_csv(FIG / "data/raw/owid_iq.csv")
    frame = raw[["Entity", "Year", COLUMN]].dropna().rename(
        columns={"Entity": "series", "Year": "year", COLUMN: "gain_iq_points"})
    frame["source_series"] = frame.series
    frame["series"] = frame.series.replace(NAMES)
    frame = frame.sort_values(["series", "year"])
    if set(frame.series) != set(STYLES) or len(frame) != 36 or frame.duplicated(["series", "year"]).any():
        raise ValueError("Unexpected regional IQ data")
    if not frame.groupby("series").gain_iq_points.first().eq(0).all():
        raise ValueError("Expected each source series to start from its own zero")
    frame["unit"] = "IQ point change from own first observation; not IQ level"
    frame["shown_in_book_plot"] = ~(frame.series.eq("Europe") & frame.gain_iq_points.eq(0))
    segments = frame.copy()
    segments["years_elapsed"] = segments.groupby("series").year.diff()
    segments["gain_since_prior"] = segments.groupby("series").gain_iq_points.diff()
    segments["implied_gain_per_year"] = segments.gain_since_prior / segments.years_elapsed
    return frame, segments.dropna()


def main():
    book, segments = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    book.to_csv(clean / "figure_16_5_book_period.csv", index=False)
    segments.to_csv(clean / "figure_16_5_segments.csv", index=False)
    labels = {"Asia": (2006, 38), "Americas": (1967, 29.5), "World": (2006, 26),
              "Europe": (2005, 20.4), "Australia & NZ": (1981, 14.2), "Africa": (2005, 10.9)}
    for mode in ["book_period", "extended"]:
        fig, ax = plt.subplots(figsize=(8.5, 6.45), dpi=200)
        fig.subplots_adjust(left=.12, right=.975, top=.95, bottom=.28)
        for name, group in book.groupby("series"):
            group = group[group.shown_in_book_plot]
            color, style, width = STYLES[name]
            ax.plot(group.year, group.gain_iq_points, color=color, ls=style, lw=width,
                    solid_capstyle="round", dash_capstyle="round")
            ax.text(*labels[name], name, fontsize=11, weight="bold" if name == "World" else "normal")
        ax.set(xlim=(1905, 2015), ylim=(0, 40), ylabel="Gain in IQ points relative to earliest data")
        ax.set_xticks(range(1905, 2016, 10))
        ax.set_yticks(range(0, 41, 5))
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(length=6, labelsize=11)
        fig.text(.025, .16, "Figure 16-5: IQ gains, 1909-2013", fontsize=11)
        fig.text(.025, .035, "Source: Pietschnig & Voracek (2015), via OWID July 2015 numerical dataset.\n"
                 "Different tests and starting years: trajectories are NOT comparable regional IQ levels.\n"
                 + ("No comparable extension recovered; book-period result repeated, no extrapolation."
                    if mode == "extended" else "Original supplement weights remain unverified. No plotted values digitized."), fontsize=8.5)
        path = FIG / f"plots/{mode}/figure_16_5_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)


if __name__ == "__main__":
    main()
