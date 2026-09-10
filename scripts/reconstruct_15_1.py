"""Reconstruct Figure 15-1 from Pew's public 2012 Values Survey topline.

The downloadable combined microdata require a Pew account.  The public
topline PDF contains the structured response tables used here, so the clean
file is an explicit transcription of those published tables, not of Pinker's
plotted pixels.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/15-1"
REF = ROOT / "references/figures/figure_15_1.png"

TOPLINE_URL = "https://www.pewresearch.org/wp-content/uploads/sites/4/legacy-questionnaires/Values-topline-for-release.pdf"
REPORT_URL = "https://www.pewresearch.org/wp-content/uploads/sites/4/legacy-pdf/06-04-12-Values-Release.pdf"
DATASET_URL = "https://www.pewresearch.org/dataset/1987-2012-values-survey-combined-dataset/"

YEARS = [1987, 1988, 1989, 1990, 1991, 1992, 1994, 1997, 1999, 2002, 2003, 2007, 2009, 2012]

# Values are transcribed from the official Pew topline tables.  The visual
# series names follow the published Pinker chart; source_question records the
# table question whose values match each line's visible trajectory.
SERIES = {
    "Agree: Women should return to their traditional roles in society": {
        "source_question": "Q41e School boards ought to have the right to fire teachers who are known homosexuals (agree)",
        "values": [51, 51, 48, 49, 39, 40, 39, 33, 32, 36, 33, 28, 28, 21],
        "color": "#d3d1d1",
    },
    "Agree: School boards ought to have the right to fire teachers who are known homosexuals": {
        "source_question": "Q41j Women should return to their traditional roles in society (agree)",
        "values": [30, 31, 26, 30, 23, 23, 30, 24, 25, 20, 24, 20, 19, 18],
        "color": "#242222",
    },
    "Disagree: I think it's all right for blacks and whites to date each other": {
        "source_question": "Q40k I think it's all right for blacks and whites to date each other (disagree)",
        "values": [46, 46, 45, 44, 30, 32, 29, 26, 23, 21, 20, 13, 13, 10],
        "color": "#898787",
    },
}


def build_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, object]] = []
    for visual_label, spec in SERIES.items():
        for year, value in zip(YEARS, spec["values"]):
            rows.append(
                {
                    "year": year,
                    "series": visual_label,
                    "percentage": value,
                    "visual_label": visual_label,
                    "source_question": spec["source_question"],
                    "source_type": "official Pew topline table transcription",
                }
            )
    book = pd.DataFrame(rows)
    # Pew's comparable political-values series ends in 2012.  Keep a schema-
    # compatible empty successor file so the extended artifact is explicit.
    successor = pd.DataFrame(columns=book.columns)
    return book, successor


def draw(book: pd.DataFrame, successor: pd.DataFrame, output: Path, extended: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12.2, 7.2), dpi=180)
    for visual_label, spec in SERIES.items():
        group = book[book.series == visual_label].sort_values("year")
        ax.plot(group.year, group.percentage, color=spec["color"], lw=3.0, label=visual_label)

    # Match the source figure's editorial annotations: arrows mark the last
    # comparable years in Pinker 2011 for the corresponding topics.
    arrows = [(1995, 37, "#d3d1d1"), (1997, 28, "#898787"), (2009, 22, "#d3d1d1")]
    for year, y, color in arrows:
        ax.annotate("", xy=(year, y - 3), xytext=(year, y + 3),
                    arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.7})

    ax.text(1990.8, 12.8, "Agree: School boards\nought to have the right\nto fire teachers who are\nknown homosexuals",
            fontsize=13.5, color="#242222", ha="left", va="center")
    ax.text(2003.0, 43.0, "Agree: Women should\nreturn to their traditional\nroles in society",
            fontsize=13.5, color="#242222", ha="left", va="center")
    ax.text(2003.0, 8.2, "Disagree: I think it's\nall right for blacks and\nwhites to date each other",
            fontsize=13.5, color="#242222", ha="left", va="center")

    ax.set_title("Figure 15-1: Racist, sexist, and homophobic opinions, US, 1987-2012", loc="left", fontsize=15)
    ax.set_xlabel("")
    ax.set_ylabel("Percentage", fontsize=13)
    ax.set_xlim(1985, 2015)
    ax.set_ylim(0, 60)
    ax.set_xticks([1985, 1990, 1995, 2000, 2005, 2010, 2015])
    ax.set_yticks(range(0, 61, 10))
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#626060")
    ax.spines["bottom"].set_color("#626060")
    ax.tick_params(colors="#3e3c3c", labelsize=10)
    note = "Source: Pew Research Center 2012b public topline tables; values are transcribed from Q41e, Q41j, and Q40k."
    if extended:
        note += " No comparable post-2012 continuation was found; this panel intentionally contains no extension."
    else:
        note += " The two apparent line/label assignments are documented in the anomaly review."
    fig.text(0.02, 0.018, note, fontsize=7.8, color="#555555")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def compare(recreated: Path, output: Path, title: str) -> None:
    ref, rec = mpimg.imread(REF), mpimg.imread(recreated)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=180)
    for axis, image, label in zip(axes, [ref, rec], ["Supplemental PDF reference", "Recreated"]):
        axis.imshow(image)
        axis.set_title(label, fontsize=10)
        axis.axis("off")
    fig.suptitle(title, fontsize=12)
    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_package(book: pd.DataFrame, successor: pd.DataFrame, book_plot: Path, extended_plot: Path) -> None:
    for sub in ["data/clean", "plots/comparisons", "captions", "provenance", "source_logs", "search_iterations", "anomaly_reviews", "discrepancy_logs", "lineage", "checksums"]:
        (FIG / sub).mkdir(parents=True, exist_ok=True)
    book.to_csv(FIG / "data/clean/figure_15_1_book_period.csv", index=False)
    successor.to_csv(FIG / "data/clean/figure_15_1_successor.csv", index=False)
    compare(book_plot, FIG / "plots/comparisons/figure_15_1_book_period_review.png", "Figure 15-1 book-period comparison")
    compare(extended_plot, FIG / "plots/comparisons/figure_15_1_extended_review.png", "Figure 15-1 extended comparison")
    (FIG / "README.md").write_text("""# Figure 15-1 - Racist, sexist, and homophobic opinions

Status: `partial_match`. Pew's public topline tables recover the three visible trajectories, but the combined microdata are account-gated and the published chart appears to place the women and school-board labels opposite the matching source trajectories. No comparable post-2012 extension was located.

- Original: [../../references/figures/figure_15_1.png](../../references/figures/figure_15_1.png)
- Script: [../../scripts/reconstruct_15_1.py](../../scripts/reconstruct_15_1.py)
- Book comparison: [plots/comparisons/figure_15_1_book_period_review.png](plots/comparisons/figure_15_1_book_period_review.png)
- Extended comparison: [plots/comparisons/figure_15_1_extended_review.png](plots/comparisons/figure_15_1_extended_review.png)
""")
    (FIG / "captions/caption.txt").write_text("Figure 15-1: Racist, sexist, and homophobic opinions, US, 1987-2012. Values are transcribed from the public Pew Research Center 2012 Values Survey topline tables for the matching question responses (Q41e, Q41j, and Q40k), not from the Pinker chart. The extended panel contains no post-2012 line because a comparable continuation was not identified. Visual inspection suggests that the source chart's top light line follows the school-board response while its black line follows the women response; this apparent label/trajectory inversion is retained as an unresolved source-figure anomaly. Status: partial_match.")
    (FIG / "provenance/provenance.md").write_text(f"""# Figure 15-1 provenance

## Original book source line

Pew Research Center 2012b. The arrows point to the most recent years plotted in Pinker 2011 for similar questions: Blacks, 1997 (fig. 7-7); Women, 1995 (fig. 7-11); Homosexuals, 2009 (fig. 7-24).

## Public source chain

- Pew 1987-2012 combined dataset landing page (account-gated): {DATASET_URL}
- Public 2012 Values Survey topline PDF: {TOPLINE_URL}
- Public report PDF: {REPORT_URL}
- Raw files: `figures/15-1/data/raw/pew_values_topline_2012.pdf`, `figures/15-1/data/raw/pew_values_release_2012.pdf`

The public topline contains the response tables used here. The clean CSV is a transparent transcription of the official table rows for the survey years 1987, 1988, 1989, 1990, 1991, 1992, 1994, 1997, 1999, 2002, 2003, 2007, 2009, and 2012. The account-gated microdata were not downloaded. No values were digitized from the Pinker chart.

## Transformation

The table responses were placed in long format. For visual fidelity, each source response is drawn under the label attached to the corresponding visible trajectory in the book image. The source-question column preserves the underlying Pew question and makes the apparent women/school-board inversion auditable.
""")
    (FIG / "source_logs/source_log.md").write_text(f"""# Figure 15-1 source discovery log

## Queries attempted

- `Pew Research Center 2012b values survey combined dataset download`
- `Pew 1987-2012 Values Survey Combined Dataset women traditional roles school boards homosexual teachers`
- `Pew 2012 values topline Q41e Q41j Q40k`
- `Pinker Enlightenment Now Figure 15-1 Pew Research Center 2012b`
- `Pew values survey post-2012 comparable social values series`

## Sources investigated

- Pew combined dataset landing page ({DATASET_URL}) - accepted as the cited dataset identity, but raw download rejected for this run because it requires a Pew account.
- Pew public 2012 topline PDF ({TOPLINE_URL}) - accepted; it exposes the relevant structured response tables and all plotted survey years.
- Pew public 2012 report PDF ({REPORT_URL}) - accepted for question context and confirmation of the 1987-2012 series.
- Pew interactive values graphic - rejected as a data source because it is an image, not a downloadable table.
- Search results for later Pew values surveys - no comparable continuation with all three exact questions and a continuous public series was found.

## Evidence resolution

Q41e school-board agree values match the top light trajectory in the book image. Q41j women agree values match the lower black trajectory. Q40k interracial-dating disagree values match the middle gray trajectory. The displayed labels appear to name the first two trajectories in the opposite order; this is documented rather than silently corrected.

## Remaining uncertainties

- Pew account-gated combined microdata were not independently downloaded.
- The original chart may use a different response recode, release, or label placement than the public 2012 topline; the apparent line/label inversion remains unresolved.
- No defensible post-2012 continuation for all three exact questions was identified.

## Recommended next steps

Obtain the combined dataset through an authorized Pew account or archive, inspect the original data dictionary, and verify whether the line-label inversion is present in the source data or introduced during chart preparation.
""")
    (FIG / "search_iterations/search_iterations.md").write_text("""# Search iterations

1. Inspected the Supplemental Graphics PDF crop and extracted the title, source note, and arrow years.
2. Resolved Pew Research Center 2012b as the source family.
3. Located the public 2012 topline and report PDFs; the combined microdata landing page is account-gated.
4. Matched the three visible trajectories to the published Q41e, Q41j, and Q40k response tables.
5. Recorded the apparent women/school-board line-label inversion as an anomaly rather than using Pinker's pixels as data.
6. Generated and visually inspected book-period and no-extension comparison panels.
""")
    (FIG / "anomaly_reviews/anomaly_review.md").write_text("""# Anomaly review

Major: the public Pew topline recovers three trajectories, but the original figure's light top trajectory matches the Q41e school-board response while its black lower trajectory matches the Q41j women response, opposite the nearby labels. This could be a source-chart label placement issue or a difference between the published topline and the chart-preparation file.

Major: the exact combined microdata are account-gated and were not independently recovered. Minor: the arrows and annotation placement are approximated from the PDF reference. No post-2012 continuation was found, so the extended panel is deliberately identical in time coverage and says so explicitly.

Status remains `partial_match`; promotion requires resolving the label/source discrepancy and obtaining the underlying combined release.
""")
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text("""# Discrepancy log

The reconstructed lines reproduce the source-table trajectories and the overall 0-60 percentage scale. The obvious unresolved difference is semantic rather than numeric: the line locations in the book image appear to be labeled opposite the matching published Pew question trajectories for women and school boards. The layout and annotation positions are approximations. Because no comparable post-2012 three-question series was located, the extended panel contains no dashed continuation.
""")
    (FIG / "review_checklist.md").write_text("""# Review checklist

- [x] Original Supplemental PDF figure inspected
- [x] Title, source note, and arrow years extracted
- [x] Pew source family resolved
- [x] Public official topline saved
- [x] Structured table values transcribed into clean data
- [x] Book-period reconstruction generated
- [x] Extended artifact generated with no-extension explanation
- [x] Both comparisons generated and inspected
- [x] No plotted values digitized
- [x] Apparent line/label inversion documented
- [ ] Combined microdata obtained through authorized access
- [ ] Line/label inversion resolved against original chart data
- [ ] Comparable post-2012 extension found
""")
    lineage = {
        "schema_version": 1,
        "figure_id": "15-1",
        "book_citation": "Pew Research Center 2012b",
        "original_dataset": DATASET_URL,
        "public_source": TOPLINE_URL,
        "script": "scripts/reconstruct_15_1.py",
        "mappings": [
            {
                "role": "book_period",
                "raw_inputs": ["figures/15-1/data/raw/pew_values_topline_2012.pdf"],
                "selection": "Published response-table rows for Q41e, Q41j, and Q40k, survey years 1987-2012",
                "transformation": "Transcribe published net agree/disagree values into long format; map source questions to visible chart trajectories",
                "clean": "figures/15-1/data/clean/figure_15_1_book_period.csv",
                "plot": "figures/15-1/plots/figure_15_1_book_period.png",
            },
            {
                "role": "extension",
                "raw_inputs": [],
                "selection": "No comparable post-2012 series found",
                "transformation": "No extension plotted; extended artifact documents the absence",
                "clean": "figures/15-1/data/clean/figure_15_1_successor.csv",
                "plot": "figures/15-1/plots/figure_15_1_extended.png",
            },
        ],
    }
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    record = {
        "figure_id": "15-1",
        "title": "Racist, sexist, and homophobic opinions, US, 1987-2012",
        "scientific_status": "partial_match",
        "artifact_kind": "reconstruction",
        "publication_status": "not_reviewed",
        "execution_status": "processed",
        "lifecycle_stage": "visual_review",
        "next_action": "Obtain authorized Pew combined microdata and resolve the apparent women/school-board line-label inversion.",
        "notes": "Official public topline transcription; no digitized Pinker values; no comparable post-2012 extension.",
        "extension": {"status": "not_found", "label": "No comparable post-2012 continuation"},
        "visual_review": {"status": "pending", "reference_basis": "original", "issues": ["line/label inversion", "microdata account gate", "no extension"]},
        "artifacts": {
            "metadata": {"path": "figures/15-1/figure.json", "self": True},
            "original_reference": {"path": "references/figures/figure_15_1.png"},
            "book_period_reconstruction": {"path": "figures/15-1/plots/figure_15_1_book_period.png"},
            "extended_reconstruction": {"path": "figures/15-1/plots/figure_15_1_extended.png"},
            "book_period_clean": {"path": "figures/15-1/data/clean/figure_15_1_book_period.csv"},
            "successor_clean": {"path": "figures/15-1/data/clean/figure_15_1_successor.csv"},
            "book_period_comparison": {"path": "figures/15-1/plots/comparisons/figure_15_1_book_period_review.png"},
            "extended_comparison": {"path": "figures/15-1/plots/comparisons/figure_15_1_extended_review.png"},
            "caption": {"path": "figures/15-1/captions/caption.txt"},
            "provenance": {"path": "figures/15-1/provenance/provenance.md"},
            "source_log": {"path": "figures/15-1/source_logs/source_log.md"},
            "anomaly_review": {"path": "figures/15-1/anomaly_reviews/anomaly_review.md"},
            "discrepancy_log": {"path": "figures/15-1/discrepancy_logs/discrepancy_log.md"},
            "review_checklist": {"path": "figures/15-1/review_checklist.md"},
            "lineage": {"path": "figures/15-1/lineage/lineage.json"},
            "reconstruction_script": {"path": "scripts/reconstruct_15_1.py"},
        },
    }
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")


def main() -> None:
    book, successor = build_data()
    book_plot = FIG / "plots/figure_15_1_book_period.png"
    extended_plot = FIG / "plots/figure_15_1_extended.png"
    draw(book, successor, book_plot, extended=False)
    draw(book, successor, extended_plot, extended=True)
    write_package(book, successor, book_plot, extended_plot)
    print(json.dumps({"figure": "15-1", "book_rows": len(book), "successor_rows": len(successor)}, indent=2))


if __name__ == "__main__":
    main()
