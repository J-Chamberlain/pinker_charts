"""Extract published regression coefficients, not plotted coordinates.

Source: https://eprints.qut.edu.au/124698/1/Clark_decling%20loneliness.pdf
Accepted manuscript printed p.8; microdata/meta-analysis not re-estimated.
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
BASE = ROOT / "figures/18-2"
URL = "https://eprints.qut.edu.au/124698/1/Clark_decling%20loneliness.pdf"


def coefficients(text):
    match = re.search(r"regression equation \(B = ([-.\d]+), constant = ([.\d]+)\)", text)
    if not match:
        raise ValueError("Published coefficient sentence not found")
    return tuple(map(float, match.groups()))


def main():
    clean = BASE / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    pdf = BASE / "data/raw/Clark_declining_loneliness_accepted.pdf"
    if pdf.exists():
        text = subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"], text=True)
        slope, intercept = coefficients(text)
        pd.DataFrame([dict(slope=slope, intercept=intercept, source_url=URL,
                           locator="accepted manuscript printed page 8", method="text extraction")]).to_csv(
            clean / "figure_18_2_published_coefficients.csv", index=False)
    else:
        # Redistribution of the full manuscript is not authorized; retain numeric evidence.
        row = pd.read_csv(clean / "figure_18_2_published_coefficients.csv").iloc[0]
        slope, intercept = row.slope, row.intercept
    data = pd.DataFrame({"year": range(1978, 2010)})
    data["fitted_loneliness"] = slope * data.year + intercept
    data["series_kind"] = "published fitted line; not annual survey observations"
    data["source_url"] = URL
    data.to_csv(clean / "figure_18_2_college_fitted_line.csv", index=False)
    fig, ax = plt.subplots(figsize=(10, 8.4), dpi=180)
    ax.plot(data.year, data.fitted_loneliness, color="#222222", lw=3)
    ax.set(xlim=(1978, 2012), ylim=(34, 39), ylabel="College R-UCLA loneliness score")
    ax.set_xticks(range(1978, 2013, 2))
    ax.tick_params(axis="x", labelrotation=50)
    ax.tick_params(labelsize=13)
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(1985, 37.8, "College (published fitted equation)", fontsize=14)
    ax.text(1980, 34.6, "Grades 8, 10 and 12: data not recovered", fontsize=13, color="#666666")
    ax.set_title("Figure 18-2: Loneliness | college component only", loc="left", fontsize=13)
    fig.text(.12, .055, "Source: Clark, Loxton & Tobin (2015), accepted manuscript p.8.\n"
             "Published rounded coefficients; not a re-estimation. School-grade curves/right axis omitted.\n"
             "Source fit covers 1978-2009; no extrapolation to book endpoints or invented extension.", fontsize=8)
    fig.subplots_adjust(left=.12, right=.97, top=.92, bottom=.22)
    out = BASE / "plots/book_period/figure_18_2_book_period.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    compare(ROOT / "references/figures/figure_18_2.png", out,
            BASE / "plots/comparisons/figure_18_2_book_period_review.png",
            "Figure 18-2 | partial: published college fit only")


if __name__ == "__main__":
    main()
