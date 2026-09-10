"""Reconstruct Figure 18-4 from the NORC General Social Survey.

Source: https://gss.norc.org/get-the-data/stata.html
Raw release: https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_stata.zip
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


BOOK_START = 1972
BOOK_END = 2016


def load_source(path: Path) -> pd.DataFrame:
    """Read only the three needed columns from a NORC Stata release."""
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            member = next(name for name in archive.namelist() if name.endswith("gss7224_r3a.dta"))
            with archive.open(member) as handle:
                return pd.read_stata(handle, columns=["year", "happy", "life"], convert_categoricals=False)
    return pd.read_stata(path, columns=["year", "happy", "life"], convert_categoricals=False)


def summarize(source: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for year, group in source.groupby("year", sort=True):
        row = {"year": int(year)}
        for variable, output in [("happy", "very_happy_pct"), ("life", "exciting_pct")]:
            valid = group[variable].dropna()
            row[output] = (valid.eq(1).mean() * 100) if len(valid) else float("nan")
            row[f"{output}_n"] = int(len(valid))
        rows.append(row)
    return pd.DataFrame(rows)


def plot(data: pd.DataFrame, output: Path, title_suffix: str, extension: bool) -> None:
    fig, ax = plt.subplots(figsize=(10, 6.8), dpi=180)
    ax.set_xlim(1970, 2018)
    ax.set_ylim(0, 60)
    ax.set_xticks([1970, 1978, 1986, 1994, 2002, 2010, 2018])
    ax.set_yticks(range(0, 61, 10))
    ax.set_xlabel("")
    ax.set_ylabel("Percent agreeing", fontsize=14)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#5d5a5b")
    ax.tick_params(colors="#343031", labelsize=12, length=7, width=1.4)
    ax.grid(False)

    main = data[data["year"].between(BOOK_START, BOOK_END)]
    ax.plot(main["year"], main["exciting_pct"], color="#2c2829", linewidth=3.2, solid_capstyle="round")
    ax.plot(main["year"], main["very_happy_pct"], color="#969394", linewidth=3.2, solid_capstyle="round")

    if extension:
        later = data[data["year"] > BOOK_END]
        for column, color in [("exciting_pct", "#2c2829"), ("very_happy_pct", "#969394")]:
            segment = pd.concat([main.tail(1), later], ignore_index=True)
            ax.plot(segment["year"], segment[column], color=color, linewidth=2.4, linestyle=(0, (5, 4)), alpha=0.85)
        ax.text(2016.3, 57.5, "Book period", fontsize=10, color="#5b5758", ha="right")
        ax.text(2017.7, 57.5, "Extension", fontsize=10, color="#5b5758", ha="right")

    ax.text(2003, 54.0, "Life is exciting", fontsize=16, color="#2c2829")
    ax.text(2004.0, 23.0, "Very happy", fontsize=16, color="#2c2829")
    ax.set_title(f"Figure 18-4: Happiness and excitement, US, 1972-2016{title_suffix}", loc="left", fontsize=13, pad=14)
    ax.text(1970.2, -7.5, "Source: General Social Survey (NORC); percentages exclude nonresponses.", fontsize=8.5, color="#4f4b4c")
    fig.subplots_adjust(left=0.12, right=0.98, top=0.9, bottom=0.18)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, facecolor="white")
    plt.close(fig)


def compare(reference: Path, recreated: Path, output: Path, title: str) -> None:
    """Place the stored PDF crop beside the generated image for visual QA."""
    reference_image = mpimg.imread(reference)
    recreated_image = mpimg.imread(recreated)
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=180)
    for axis, image, label in zip(
        axes,
        [reference_image, recreated_image],
        ["Supplemental PDF reference", "Recreated"],
    ):
        axis.imshow(image)
        axis.set_title(label, fontsize=10)
        axis.axis("off")
    figure.suptitle(title, fontsize=12)
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, facecolor="white")
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--clean", type=Path, required=True)
    parser.add_argument("--book-plot", type=Path, required=True)
    parser.add_argument("--extended-plot", type=Path, required=True)
    parser.add_argument("--book-comparison", type=Path, required=True)
    parser.add_argument("--extended-comparison", type=Path, required=True)
    args = parser.parse_args()

    data = summarize(load_source(args.raw))
    args.clean.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(args.clean, index=False)
    plot(data, args.book_plot, "", extension=False)
    plot(data, args.extended_plot, " (extended)", extension=True)
    compare(args.raw.parent.parent.parent / "../../references/figures/figure_18_4.png", args.book_plot,
            args.book_comparison, "Figure 18-4 book-period comparison")
    compare(args.raw.parent.parent.parent / "../../references/figures/figure_18_4.png", args.extended_plot,
            args.extended_comparison, "Figure 18-4 extended comparison")


if __name__ == "__main__":
    main()
