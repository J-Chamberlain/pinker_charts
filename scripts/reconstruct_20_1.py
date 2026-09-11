"""Recover two poll components from saved tables, not plotted values.

Sources: https://ropercenter.cornell.edu/how-groups-voted-2016
https://lordashcroftpolls.com/wp-content/uploads/2016/06/How-the-UK-voted-Full-tables-1.pdf
"""
from pathlib import Path
import re
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

try:
    from reconstruct_18_4 import compare
except ImportError:
    from scripts.reconstruct_18_4 import compare

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "figures/20-1"
TRUMP_URL = "https://ropercenter.cornell.edu/how-groups-voted-2016"
BREXIT_URL = "https://lordashcroftpolls.com/wp-content/uploads/2016/06/How-the-UK-voted-Full-tables-1.pdf"


def cohort(age):
    numbers = [int(n) for n in re.findall(r"\d+", age)]
    if len(numbers) == 1:
        return 2016 - numbers[0], "upper birth-year bound; no midpoint for open-ended bin"
    return 2016 - sum(numbers) / 2, "2016 minus age-bin midpoint; approximate birth year"


def recover():
    tables = pd.read_html(BASE / "data/raw/roper_2016_exit_poll_age_table.html")
    table = next(t for t in tables if "Demographic" in t.columns and "Trump" in t.columns)
    ages = table.loc[table.Variable.eq("AGE")]
    if len(ages) != 4:
        raise ValueError("Unexpected Roper age table")
    rows = []
    for _, row in ages.iterrows():
        x, method = cohort(row.Demographic)
        rows.append(dict(series="Trump", age_group=row.Demographic,
                         birth_year_plot=x, coordinate_method=method,
                         percent=float(row.Trump), source_url=TRUMP_URL, source_locator="AGE table"))
    text = subprocess.check_output(["pdftotext", "-f", "5", "-l", "5", "-layout",
                                   str(BASE / "data/raw/lord_ashcroft_eu_referendum_full_tables_2016.pdf"), "-"], text=True)
    if "Q.2 Which way did you vote" not in text:
        raise ValueError("Wrong Ashcroft PDF page")
    header = next(line for line in text.splitlines() if "18-24" in line)
    labels = re.findall(r"\b(?:\d{2}-\d{2}|65\+)\b", header)
    if len(labels) != 5:  # trailing + has no word boundary
        raise ValueError("Unexpected Ashcroft age columns")
    labels.append("65+")
    line = next(line for line in text.splitlines() if line.strip().startswith("European Union"))
    values = re.findall(r"(\d+)%", line)[3:9]  # total/male/female precede age columns
    if len(values) != 6:
        raise ValueError("Unexpected Ashcroft percentage row")
    for age, value in zip(labels, values):
        x, method = cohort(age)
        rows.append(dict(series="Brexit", age_group=age, birth_year_plot=x,
                         coordinate_method=method, percent=float(value),
                         source_url=BREXIT_URL, source_locator="PDF page 5; Table 2; Leave row"))
    return pd.DataFrame(rows).sort_values(["series", "birth_year_plot"])


def main():
    data = recover()
    clean = BASE / "data/clean/figure_20_1_poll_components.csv"
    clean.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(clean, index=False)
    fig, ax = plt.subplots(figsize=(10, 7), dpi=180)
    ax.set(xlim=(1930, 2000), ylim=(25, 65), xlabel="Birth cohort (midpoint; open bins at boundary)",
           ylabel="Percentage voting for Trump or Brexit")
    ax.set_xticks(range(1930, 2001, 5))
    ax.set_yticks(range(25, 66, 5))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for name, color in [("Brexit", "#a4a4a4"), ("Trump", "#222222")]:
        g = data[data.series.eq(name)]
        closed = g[~g.coordinate_method.str.startswith("upper")]
        opened = g[g.coordinate_method.str.startswith("upper")]
        ax.plot(closed.birth_year_plot, closed.percent, color=color, linewidth=2.8)
        ax.scatter(opened.birth_year_plot, opened.percent, edgecolor=color, facecolor="white", s=45, zorder=3)
    ax.text(1975, 51, "Brexit", fontsize=14)
    ax.text(1989, 40, "Trump", fontsize=14)
    ax.text(1940, 62, "65+ shown at birth-year boundary (1951)", fontsize=9)
    ax.set_title("Figure 20-1: Populist support, 2016 | two recovered components", fontsize=12, loc="left", pad=15)
    fig.text(.12, .075, "Sources: Edison/NEP via Roper; Lord Ashcroft Table 2. European ESS series not recovered.\n"
             "Open 65+ bins have no defined midpoint; no invented upper age or connecting segment.\n"
             "No extension: later elections are different events, not additional birth cohorts.", fontsize=8.5)
    fig.subplots_adjust(left=.12, right=.96, top=.9, bottom=.22)
    plot_path = BASE / "plots/book_period/figure_20_1_book_period.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(plot_path, facecolor="white")
    plt.close(fig)
    compare(ROOT / "references/figures/figure_20_1.png", plot_path,
            BASE / "plots/comparisons/figure_20_1_book_period_review.png",
            "Figure 20-1 | partial reconstruction: European series missing")


if __name__ == "__main__":
    main()
