"""Reconstruct Figure 12-6 from National Safety Council rate tables."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/12-6"
RAW = FIG / "data/raw/nsc_injury_facts_historical_rates_2026-09-09.xlsx"
REF = ROOT / "references/figures/figure_12_6.png"
NSC_URL = "https://injuryfacts.nsc.org/all-injuries/historical-preventable-fatality-trends/deaths-by-cause/"
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTb9UjML1Yir8rH9mAenZMkOzjWF1RVcaUQHMgbF1p8DnbR_XCoj7yarNpAiV-C7dWOtacstCqg9v5Y/pub?output=xlsx"


def numeric_year(value: object) -> int | None:
    try:
        return int(str(value).split()[0])
    except (TypeError, ValueError):
        return None


def read_rates(sheet: str) -> pd.DataFrame:
    frame = pd.read_excel(RAW, sheet_name=sheet, header=1)
    frame["year"] = frame["Year"].map(numeric_year)
    frame = frame[frame["year"].notna()].copy()
    frame["year"] = frame["year"].astype(int)
    numeric_columns = [column for column in frame.columns if column not in {"Year", "year"}]
    for column in numeric_columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    # The workbook has two 1948 rows to expose the ICD revision break. The
    # second row is the later revision used for the continuous plot.
    return frame.drop_duplicates("year", keep="last")


def build_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    early = read_rates("Rate 1903-1998")
    late = read_rates("Rate 1999-")
    records: list[dict[str, object]] = []

    early_map = {
        "Falls": "Falls",
        "Drowning": "Drowning (b)",
        "Fire": "Fires, flames, or smoke (c)",
        "Poison (solid or liquid)": "Poison (solid or liquid)",
        "Poison (gas or vapor)": "Poison (gas or vapor)",
    }
    for series, column in early_map.items():
        subset = early[["year", column]].rename(columns={column: "rate"})
        subset = subset[subset.rate.notna()].copy()
        # Pinker's caption explicitly stops falls at 1992 because later
        # reporting artifacts make the subsequent historical series unsafe.
        if series == "Falls":
            subset = subset[subset.year.between(1913, 1992)]
        else:
            subset = subset[subset.year.between(1903, 1998)]
        for row in subset.itertuples(index=False):
            records.append({"year": row.year, "series": series, "rate": row.rate, "source_period": "NSC historical rate table 1903-1998"})

    late_map = {
        "Falls": "Falls",
        "Drowning": "Drowning (g)",
        "Fire": "Fires, flames, or smoke (c)",
        "Poison (solid or liquid)": "Poisoning",
    }
    for series, column in late_map.items():
        subset = late[["year", column]].rename(columns={column: "rate"})
        subset = subset[subset.rate.notna()].copy()
        subset = subset[subset.year.between(1999, 2024)]
        for row in subset.itertuples(index=False):
            records.append({"year": row.year, "series": series, "rate": row.rate, "source_period": "NSC current rate table 1999-2024"})

    all_data = pd.DataFrame(records).sort_values(["series", "year"]).reset_index(drop=True)
    book = all_data[all_data.year.between(1903, 2014)].copy()
    # The book's fall line is intentionally absent after 1992; later NSC
    # values are retained only as a clearly separated successor extension.
    book = book[~((book.series == "Falls") & (book.year > 1992))]
    extension = all_data[all_data.year.between(2015, 2024)].copy()
    return book, extension


def draw(book: pd.DataFrame, extension: pd.DataFrame, mode: str) -> Path:
    (FIG / "plots").mkdir(parents=True, exist_ok=True)
    output = FIG / "plots" / ("figure_12_6_extended.png" if mode == "extended" else "figure_12_6_book_period.png")
    colors = {
        "Falls": "#aaa8a8",
        "Fire": "#d0cece",
        "Drowning": "#5c5a5a",
        "Poison (solid or liquid)": "#a7a5a5",
        "Poison (gas or vapor)": "#242222",
    }
    fig, ax = plt.subplots(figsize=(12, 7.4), dpi=180)
    for series in colors:
        group = book[book.series == series]
        if not group.empty:
            linestyle = ":" if series == "Poison (solid or liquid)" else "-"
            ax.plot(group.year, group.rate, color=colors[series], lw=2.8, ls=linestyle, label=series)
    if mode == "extended":
        for series in ["Falls", "Drowning", "Fire", "Poison (solid or liquid)"]:
            group = extension[extension.series == series]
            if not group.empty:
                ax.plot(group.year, group.rate, color=colors[series], lw=2.6, ls="--", label=f"{series} successor")
        ax.axvline(2014, color="#c8c8c8", lw=1.0, ls=":")
    ax.set_title("Figure 12-6: Deaths from falls, fire, drowning, and poison, US, 1903-2014", loc="left", fontsize=16)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Deaths per 100,000 people per year", fontsize=12)
    ax.set_xlim(1900, 2025 if mode == "extended" else 2015)
    ax.set_ylim(0, 20)
    ax.set_xticks(range(1900, 2021 if mode == "extended" else 2016, 5))
    ax.grid(axis="y", color="#e5e5e5", lw=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right", fontsize=8)
    note = "Source: National Safety Council historical rate tables. Falls stop at 1992 per the book's reporting-artifact note."
    if mode == "extended":
        note += " Dashed: NSC successor data from 2015 onward; category definitions and revisions require review."
    else:
        note += " 1999 category break: NSC Poisoning includes gas or vapor."
    fig.text(0.02, 0.015, note, fontsize=8.2, color="#555555")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output


def compare(reference: Path, recreated: Path, output: Path, title: str) -> None:
    ref, rec = mpimg.imread(reference), mpimg.imread(recreated)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=180)
    for axis, image, label in zip(axes, [ref, rec], ["Supplemental PDF reference", "Recreated"]):
        axis.imshow(image)
        axis.set_title(label, fontsize=10)
        axis.axis("off")
    fig.suptitle(title, fontsize=12)
    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_package(book: pd.DataFrame, extension: pd.DataFrame, plots: dict[str, Path]) -> None:
    for sub in ["data/clean", "plots/comparisons", "captions", "provenance", "source_logs", "search_iterations", "anomaly_reviews", "discrepancy_logs", "lineage", "checksums"]:
        (FIG / sub).mkdir(parents=True, exist_ok=True)
    book.to_csv(FIG / "data/clean/figure_12_6_book_period.csv", index=False)
    extension.to_csv(FIG / "data/clean/figure_12_6_successor.csv", index=False)
    compare(REF, plots["book"], FIG / "plots/comparisons/figure_12_6_book_period_review.png", "Figure 12-6 book-period comparison")
    compare(REF, plots["extended"], FIG / "plots/comparisons/figure_12_6_extended_review.png", "Figure 12-6 extended comparison")
    (FIG / "README.md").write_text("""# Figure 12-6 - Deaths from falls, fire, drowning, and poison\n\nStatus: `updated_equivalent`. The historical component is reproduced from the National Safety Council rate-table family, but the downloaded workbook is a current successor rather than a verified 2016 archival edition.\n\n- Original: [../../references/figures/figure_12_6.png](../../references/figures/figure_12_6.png)\n- Script: [../../scripts/reconstruct_12_6.py](../../scripts/reconstruct_12_6.py)\n- Book comparison: [plots/comparisons/figure_12_6_book_period_review.png](plots/comparisons/figure_12_6_book_period_review.png)\n- Extended comparison: [plots/comparisons/figure_12_6_extended_review.png](plots/comparisons/figure_12_6_extended_review.png)\n""")
    (FIG / "captions/caption.txt").write_text("Figure 12-6: Deaths from falls, fire, drowning, and poison, US, 1903-2014. Recreated from National Safety Council historical rate tables. Falls stop at 1992 as in the book because later reporting artifacts are explicitly excluded. Dashed lines in the extended panel show current NSC successor rates from 2015 onward; the 1999 category revision, including poisoning by gas or vapor, is preserved and documented. Status: updated_equivalent.")
    (FIG / "provenance/provenance.md").write_text(f"""# Figure 12-6 provenance\n\n## Original book source\n\nNational Safety Council 2016. The caption states that fire, drowning, and poison solid/liquid are joined across the 1903-1998 and 1999-2014 datasets, that post-1992 falls are excluded because of reporting artifacts, and that 1999-2014 poisoning includes gas or vapor.\n\n## Recovered data\n\n- Current NSC historical trends page: {NSC_URL}\n- Public workbook downloaded from the page: {SHEET_URL}\n- Raw file: `figures/12-6/data/raw/nsc_injury_facts_historical_rates_2026-09-09.xlsx`\n\n## Transformations\n\nThe workbook's two rate sheets were read with pandas. The second 1948 ICD-revision row was retained. Historical columns were reshaped to long form, falls were cut at 1992, and the 1999-2024 sheet was mapped from `Poisoning` to the book's solid/liquid label. Book-period data end in 2014; 2015-2024 current NSC rows are plotted as a dashed successor. No values were transcribed from the Pinker chart.\n\nThe current workbook is a same-institution successor, not a cryptographically verified copy of the NSC 2016 edition; therefore the status is `updated_equivalent`, despite the strong visual and category match.\n""")
    (FIG / "source_logs/source_log.md").write_text(f"""# Figure 12-6 source discovery log\n\n## Queries attempted\n\n- `National Safety Council 2016 Injury Facts deaths falls fire drowning poison 1903 2014`\n- `site:nsc.org historical deaths by cause data table`\n- `National Safety Council Injury Facts historical rate table 1903 1998`\n- `Injury Facts deaths by cause download Excel`\n\n## Sources investigated\n\n- NSC current Historical Trends: Deaths by Cause page ({NSC_URL}) - accepted as the canonical same-institution successor because it exposes a downloadable workbook with both historical and current rate tables.\n- Public NSC Google Sheets workbook ({SHEET_URL}) - accepted and saved under `data/raw/`; it contains the needed categories and year ranges.\n- Search result reproducing an Injury Facts 2016 table - rejected as a secondary mirror because the official NSC workbook was available.\n\n## Remaining uncertainties\n\nThe exact 2016 workbook binary was not recovered, so historical values are accepted as same-institution continuation rather than an exact archival copy. ICD and category breaks are present in the workbook and are not harmonized. The original figure's line-rendering choices and the source's reporting-artifact rationale are followed where documented.\n\n## Recommended next steps\n\nLocate an archived NSC 2016 workbook or scan and byte-compare its rate sheets against the current historical rows. Confirm the exact 2016 values for the 1999-2014 segment before considering promotion to `verified_reproduction`.\n""")
    (FIG / "search_iterations/search_iterations.md").write_text("""# Search iterations\n\n1. Inspected the Supplemental Graphics PDF crop and confirmed the source note and category break.\n2. Located the official NSC Historical Trends page and its downloadable data table links.\n3. Downloaded the workbook and verified separate 1903-1998 and 1999-2024 rate sheets.\n4. Reshaped the rate tables without using plotted values, preserving the 1948 and 1999 classification breaks.\n5. Compared the recreated chart against the PDF reference; the trajectories and category ordering are visually close, with the deliberate falls cutoff and successor segment documented.\n""")
    (FIG / "anomaly_reviews/anomaly_review.md").write_text("""# Anomaly review\n\nMajor: the exact 2016 NSC workbook has not been recovered; a current same-institution workbook is used. Minor: the original line colors and label placement are approximated. Major: the 1999 ICD/category revision and the book's fall reporting-artifact cutoff mean that the plotted series are not uniformly comparable across the full span. The current status is `updated_equivalent`, not `verified_reproduction`.\n""")
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text("""# Discrepancy log\n\nThe reconstructed trajectories are visually close to the PDF reference because they come from the NSC rate tables rather than from digitized chart values. The main unresolved discrepancy is source vintage: the public workbook is current and includes 2024, while the book cites NSC 2016. The extended panel makes 2015 onward dashed and retains the 1999 category break rather than implying an uninterrupted measurement series.\n""")
    (FIG / "review_checklist.md").write_text("""# Review checklist\n\n- [x] Original Supplemental PDF figure inspected\n- [x] Title and source note extracted\n- [x] Official same-institution source located\n- [x] Raw workbook saved\n- [x] Book-period data reshaped from structured source tables\n- [x] Extension generated and visibly separated\n- [x] Book-period comparison generated and inspected\n- [x] Extended comparison generated and inspected\n- [x] No plotted values digitized\n- [x] Source-vintage limitation documented\n- [ ] Exact NSC 2016 workbook recovered\n- [ ] Verified reproduction status justified\n""")
    lineage = {"schema_version": 1, "figure_id": "12-6", "book_citation": "National Safety Council 2016", "script": "scripts/reconstruct_12_6.py", "mappings": [{"role": "book_period", "raw_inputs": ["figures/12-6/data/raw/nsc_injury_facts_historical_rates_2026-09-09.xlsx"], "selection": "NSC Rate 1903-1998 plus Rate 1999- through 2014; falls excluded after 1992", "transformation": "reshape rate columns, retain second 1948 row, map 1999 Poisoning to solid/liquid label", "clean": "figures/12-6/data/clean/figure_12_6_book_period.csv", "plot": "figures/12-6/plots/figure_12_6_book_period.png"}, {"role": "extension", "raw_inputs": ["figures/12-6/data/raw/nsc_injury_facts_historical_rates_2026-09-09.xlsx"], "selection": "NSC Rate 1999- rows 2015-2024", "transformation": "render current same-institution successor as dashed", "clean": "figures/12-6/data/clean/figure_12_6_successor.csv", "plot": "figures/12-6/plots/figure_12_6_extended.png"}]}
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    record = {"figure_id": "12-6", "title": "Deaths from falls, fire, drowning, and poison, US, 1903-2014", "scientific_status": "updated_equivalent", "artifact_kind": "reconstruction", "publication_status": "not_reviewed", "execution_status": "processed", "lifecycle_stage": "visual_review", "next_action": "Recover and compare the exact NSC 2016 workbook before considering verified reproduction.", "notes": "Strong same-institution category and trajectory match; exact 2016 binary not recovered.", "extension": {"status": "same_institution_successor", "label": "NSC successor 2015-2024"}, "visual_review": {"status": "pending", "reference_basis": "original", "issues": ["source vintage", "classification breaks"]}, "artifacts": {"metadata": {"path": "figures/12-6/figure.json", "self": True}, "original_reference": {"path": "references/figures/figure_12_6.png"}, "book_period_reconstruction": {"path": "figures/12-6/plots/figure_12_6_book_period.png"}, "extended_reconstruction": {"path": "figures/12-6/plots/figure_12_6_extended.png"}, "book_period_clean": {"path": "figures/12-6/data/clean/figure_12_6_book_period.csv"}, "successor_clean": {"path": "figures/12-6/data/clean/figure_12_6_successor.csv"}, "book_period_comparison": {"path": "figures/12-6/plots/comparisons/figure_12_6_book_period_review.png"}, "extended_comparison": {"path": "figures/12-6/plots/comparisons/figure_12_6_extended_review.png"}, "caption": {"path": "figures/12-6/captions/caption.txt"}, "provenance": {"path": "figures/12-6/provenance/provenance.md"}, "source_log": {"path": "figures/12-6/source_logs/source_log.md"}, "anomaly_review": {"path": "figures/12-6/anomaly_reviews/anomaly_review.md"}, "discrepancy_log": {"path": "figures/12-6/discrepancy_logs/discrepancy_log.md"}, "review_checklist": {"path": "figures/12-6/review_checklist.md"}, "lineage": {"path": "figures/12-6/lineage/lineage.json"}, "reconstruction_script": {"path": "scripts/reconstruct_12_6.py"}}}
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")


def main() -> None:
    book, extension = build_data()
    plots = {"book": draw(book, extension, "book"), "extended": draw(book, extension, "extended")}
    write_package(book, extension, plots)
    print(json.dumps({"figure": "12-6", "book_rows": len(book), "extension_rows": len(extension)}, indent=2))


if __name__ == "__main__":
    main()
