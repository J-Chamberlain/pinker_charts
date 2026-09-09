"""Reconstruct spending shares from retained 2016 and 2026 BEA observations.

HumanProgress archive: https://web.archive.org/web/20170117185627id_/http://humanprogress.org/static/1937
Series URLs, vintage labels and numeric precision are retained in data/raw/.
The book's abbreviated 'gasoline' category is an inference; not an exact claim.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from scripts.alfred_labels import read_labels, vintage_values
except ModuleNotFoundError:
    from alfred_labels import read_labels, vintage_values

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/17-5"
RAW = FIG / "data/raw"
BASICS = ["food", "vehicles", "furnishings", "clothing", "housing"]


def humanprogress():
    html = (FIG / "data/candidates/humanprogress_2017_archive.html").read_text()
    decoder = json.JSONDecoder()
    metadata = decoder.raw_decode(html.split("gon.dataset=", 1)[1])[0]
    data = decoder.raw_decode(html.split("gon.countries=", 1)[1])[0]
    frame = pd.DataFrame(data["data"]).set_index("year").sort_index()
    if metadata["data"]["_id"] != 1937 or frame.index.tolist() != list(range(1929, 2016)):
        raise ValueError("Unexpected HumanProgress dataset or coverage")
    if frame.generated.any() or frame.index.has_duplicates:
        raise ValueError("Generated or duplicate HumanProgress observations")
    return frame.value


def load_data():
    frames = []
    for vintage, end in [("2016", 2015), ("2026", 2025)]:
        data = {}
        for component in BASICS + ["energy", "income", "motor_fuels"]:
            date = ("2016-08-03" if component == "motor_fuels" else "2016-07-29") if vintage == "2016" else (
                "2026-05-28" if component == "income" else "2026-04-09")
            data[component] = vintage_values(RAW / f"alfred_{component}_labels.json", date, 1929, end)
        frame = pd.DataFrame(data)
        if not frame.gt(0).all().all():
            raise ValueError("Nonpositive expenditure or income")
        frame["basics_percent"] = 100 * frame[BASICS].sum(axis=1) / frame.income
        frame["necessities_percent"] = frame.basics_percent + 100 * frame.energy / frame.income
        frame["narrow_fuel_percent"] = frame.basics_percent + 100 * frame.motor_fuels / frame.income
        frame["source_version"] = vintage
        frame["excluded_from_book"] = frame.index.to_series().between(1941, 1946)
        frames.append(frame.reset_index())
    old, current = frames
    old["humanprogress_basics_percent"] = old.year.map(humanprogress())
    if not np.allclose(old.basics_percent, old.humanprogress_basics_percent, atol=5e-9, rtol=0):
        raise ValueError("2016 components do not reproduce archived HumanProgress basics")
    diagnostic = old.merge(current, on="year", suffixes=("_2016", "_2026"))
    diagnostic["revised_minus_original_pp"] = diagnostic.necessities_percent_2026 - diagnostic.necessities_percent_2016
    long = pd.concat([read_labels(RAW / f"alfred_{n}_labels.json").assign(component=n)
                      for n in BASICS + ["energy", "income", "motor_fuels"]], ignore_index=True)
    return old, current, diagnostic, long


def main():
    old, current, diagnostic, long = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, frame in [("book_period", old), ("revised_successor", current), ("diagnostic", diagnostic), ("components", long)]:
        if name in {"book_period", "revised_successor"}:
            frame = frame.drop(columns=["motor_fuels", "narrow_fuel_percent"])
        frame.to_csv(clean / f"figure_17_5_{name}.csv", index=False)
    for mode in ["book_period", "extended"]:
        fig, ax = plt.subplots(figsize=(8.2, 6.25), dpi=200)
        fig.subplots_adjust(left=.115, right=.975, top=.96, bottom=.295)
        y = old.necessities_percent.mask(old.excluded_from_book)
        ax.plot(old.year, y, color="#252525", lw=2.5)
        if mode == "extended":
            overlap = current[current.year.between(2005, 2015)]
            later = current[current.year.ge(2015)]
            ax.plot(overlap.year, overlap.necessities_percent, color="#187f7b", ls=":", lw=2,
                    label="2026 vintage: revised overlap, 2005-2015")
            ax.plot(later.year, later.necessities_percent, color="#187f7b", ls="--", lw=2,
                    label="2026 vintage: later data, 2016-2025")
            ax.legend(loc="upper right", frameon=False, fontsize=8.5)
        ax.set(xlim=(1925, 2026 if mode == "extended" else 2016.5), ylim=(30, 65),
               ylabel="Percentage of disposable income spent on necessities")
        ax.set_xticks(range(1925, 2026 if mode == "extended" else 2016, 10))
        ax.set_yticks(range(30, 66, 5))
        ax.tick_params(length=6, labelsize=11)
        ax.spines[["top", "right"]].set_visible(False)
        for side in ["left", "bottom"]:
            ax.spines[side].set_color("#666666")
            ax.spines[side].set_linewidth(1.2)
        fig.text(.025, .155, "Figure 17-5: Spending on necessities, US" + ("; revised continuation to 2025" if mode == "extended" else ", 1929-2015"), fontsize=11)
        fig.text(.025, .035, "Sources: BEA, ALFRED 2016 / 2026 vintages; HumanProgress archived dataset 1937.\n"
                 "Basket includes gasoline AND other energy goods; exact book adaptation is not confirmed.\n"
                 "1941-1946 omitted as in the book. Original title ends 2016; archived series ends 2015.\n"
                 "Later data are revised national-account aggregates, not a household affordability measure.", fontsize=7.5, linespacing=1.4)
        path = FIG / f"plots/{mode}/figure_17_5_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(8.2, 6), dpi=180, sharex=True)
    for field, label, style in [("necessities_percent", "Basics + gasoline and other energy", "-"),
                                ("narrow_fuel_percent", "Basics + motor fuels only", "--"),
                                ("basics_percent", "Archived HumanProgress basics (no energy)", ":")]:
        axes[0].plot(old.year, old[field].mask(old.excluded_from_book), style, label=label)
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].set(ylabel="Share of disposable income (%)", title="Figure 17-5: basket and source-vintage sensitivity")
    axes[1].plot(diagnostic.year, diagnostic.revised_minus_original_pp, color="#187f7b")
    axes[1].axhline(0, color="#777777", lw=.8)
    axes[1].set(xlabel="Year", ylabel="2026 minus 2016 (percentage points)")
    fig.tight_layout()
    path = FIG / "plots/diagnostics/basket_and_vintage.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
