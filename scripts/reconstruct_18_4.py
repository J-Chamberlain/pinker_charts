"""Reconstruct Figure 18-4 from the NORC General Social Survey.

Source: https://gss.norc.org/get-the-data/stata.html
Raw release: https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_stata.zip
"""

from __future__ import annotations

import argparse
import re
import subprocess
import zipfile
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


BOOK_START = 1972
BOOK_END = 2016


def load_source(path: Path) -> pd.DataFrame:
    """Keep both historical and current weighting alternatives for audit."""
    columns = ["year", "happy", "life", "wtssall", "wtssps"]
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            member = next(name for name in archive.namelist() if name.endswith("gss7224_r3a.dta"))
            with archive.open(member) as handle:
                return pd.read_stata(handle, columns=columns, convert_categoricals=False)
    return pd.read_stata(path, columns=columns, convert_categoricals=False)


def summarize(source: pd.DataFrame, weight: str | None = None) -> pd.DataFrame:
    rows = []
    for year, group in source.groupby("year", sort=True):
        row = {"year": int(year), "weight": weight or "unweighted", "unit": "percent of valid responses"}
        for variable, output in [("happy", "very_happy_pct"), ("life", "exciting_pct")]:
            valid = group.loc[group[variable].isin([1, 2, 3])]
            if weight:
                valid = valid.loc[valid[weight].notna() & valid[weight].gt(0)]
                denominator = valid[weight].sum()
                value = 100 * valid.loc[valid[variable].eq(1), weight].sum() / denominator if denominator else float("nan")
            else:
                value = valid[variable].eq(1).mean() * 100
            row[output] = value
            row[f"{output}_n"] = int(len(valid))
        rows.append(row)
    return pd.DataFrame(rows)


def report_tables(path: Path) -> pd.DataFrame:
    """Extract printed numeric tables 1/5, never chart pixels."""
    rows = []
    for page, variable in [(7, "very_happy_pct"), (11, "exciting_pct")]:
        text = subprocess.check_output(["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(path), "-"], text=True)
        matches = re.findall(r"^\s*(19\d{2}|20\d{2})\s+(\d+\.\d+)%", text, re.M)
        if len(matches) != (30 if page == 7 else 25):
            raise ValueError(f"Unexpected report table layout at PDF page {page}")
        rows.extend({"year": int(year), "variable": variable, "report_pct": float(value),
                     "source_pdf_page": page} for year, value in matches)
    return pd.DataFrame(rows)


def plot(data: pd.DataFrame, output: Path, title_suffix: str, extension: bool,
         successor: pd.DataFrame | None = None) -> None:
    fig, ax = plt.subplots(figsize=(10, 6.8), dpi=180)
    end = max(2018, int(successor["year"].max()) + 1) if extension and successor is not None else 2018
    ax.set_xlim(1970, end)
    ax.set_ylim(0, 60)
    ax.set_xticks([1970, 1978, 1986, 1994, 2002, 2010, 2018] + ([end - 1] if end > 2018 else []))
    ax.set_yticks(range(0, 61, 10))
    ax.set_xlabel("")
    ax.set_ylabel("Percent agreeing", fontsize=14)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#5d5a5b")
    ax.tick_params(colors="#343031", labelsize=12, length=7, width=1.4)
    ax.grid(False)

    main = data[data["year"].between(BOOK_START, BOOK_END)]
    for column, color in [("exciting_pct", "#2c2829"), ("very_happy_pct", "#969394")]:
        observed = main.dropna(subset=[column])
        ax.plot(observed["year"], observed[column], color=color, linewidth=3.2, solid_capstyle="round")

    if extension:
        if successor is None:
            raise ValueError("Extension requires explicit weighted successor data")
        later = successor[successor["year"] >= BOOK_END]
        for column, color in [("exciting_pct", "#2c2829"), ("very_happy_pct", "#969394")]:
            # Do not bridge the survey-mode break or silently splice estimators.
            for mask in [later["year"].le(2018), later["year"].ge(2021)]:
                segment = later.loc[mask].dropna(subset=[column])
                ax.plot(segment["year"], segment[column], color=color, linewidth=2.4,
                        linestyle=(0, (5, 4)), marker="o", markersize=3)
        ax.axvspan(2019, 2020.5, color="#eeeeee", zorder=0)
        ax.text(2019.75, 58, "Mode\nbreak", fontsize=8, ha="center", va="top")

    ax.text(2003, 54.0, "Life is exciting", fontsize=16, color="#2c2829")
    ax.text(2004.0, 23.0, "Very happy", fontsize=16, color="#2c2829")
    ax.set_title(f"Figure 18-4: Happiness and excitement, US{title_suffix}", loc="left", fontsize=13, pad=14)
    note = "NORC GSS release 3a: solid = unweighted book-period candidate; observed years joined."
    if extension:
        note += "\nDashed = WTSSPS-weighted successor (2016 overlap); 2021+ not joined across mode break."
    else:
        note += "\nExact book extract unresolved; weighted report tables retained separately."
    fig.text(0.12, 0.055, note, fontsize=8.5, color="#4f4b4c")
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
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    source = load_source(args.raw)
    data = summarize(source)
    successor = summarize(source, "wtssps")
    args.clean.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(args.clean, index=False)
    successor.to_csv(args.clean.with_name("figure_18_4_weighted_successor.csv"), index=False)
    diagnostic = pd.concat([data, summarize(source, "wtssall"), successor], ignore_index=True)
    diagnostic.to_csv(args.clean.with_name("figure_18_4_weighting_diagnostic.csv"), index=False)
    if args.report:
        report = report_tables(args.report)
        report.to_csv(args.clean.with_name("figure_18_4_original_report_tables.csv"), index=False)
        audit = diagnostic.melt(id_vars=["year", "weight", "unit"],
                                value_vars=["very_happy_pct", "exciting_pct"], var_name="variable", value_name="current_pct")
        audit = audit.merge(report, on=["year", "variable"])
        audit["difference_pp"] = audit["current_pct"] - audit["report_pct"]
        audit.to_csv(args.clean.with_name("figure_18_4_report_diagnostic.csv"), index=False)
    plot(data, args.book_plot, " (1972-2016)", extension=False)
    plot(data, args.extended_plot, " (successor through 2024)", extension=True, successor=successor)
    compare(args.raw.parent.parent.parent / "../../references/figures/figure_18_4.png", args.book_plot,
            args.book_comparison, "Figure 18-4 book-period comparison")
    compare(args.raw.parent.parent.parent / "../../references/figures/figure_18_4.png", args.extended_plot,
            args.extended_comparison, "Figure 18-4 extended comparison")


if __name__ == "__main__":
    main()
