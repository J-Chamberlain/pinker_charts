"""Reconstruct Figure 12-7 from published occupational-fatality sources."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/12-7"
RAW = FIG / "data/raw/source_transcribed_rates.csv"
REF = ROOT / "references/figures/figure_12_7.png"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    data = pd.read_csv(RAW)
    data["period"] = data.year.map(lambda year: "book" if year <= 2015 else "successor")
    book = data[data.year.between(1913, 2015)].copy()
    successor = data[data.year > 2015].copy()
    return book, successor


def draw(data: pd.DataFrame, output: Path, extended: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10.5, 6.4), dpi=180)
    book = data[data.year <= 2015]
    ax.plot(book.year, book.rate_per_100k, color="#242222", lw=2.8, marker="o", ms=3.5, label="Book-period source observations")
    if extended:
        successor = data[data.year >= 2015]
        ax.plot(successor.year, successor.rate_per_100k, color="#242222", lw=2.8, ls="--", marker="o", ms=3.5, label="BLS successor")
        ax.axvline(2015, color="#c5c5c5", lw=1.0, ls=":")
    ax.set_title("Figure 12-7: Occupational accident deaths, US, 1913-2015", loc="left", fontsize=16)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Deaths per 100,000 workers per year", fontsize=12)
    ax.set_xlim(1910, 2020 if extended else 2020)
    ax.set_ylim(0, 70)
    ax.set_xticks(range(1910, 2021, 10))
    ax.grid(axis="y", color="#e5e5e5", lw=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    note = "Published source observations; rates are not a homogeneous series."
    if extended:
        note += " Dashed 2016 successor; 2006 onward uses BLS FTE rate x .95."
    else:
        note += " 2006-2015 values use the book's .95 FTE adjustment."
    fig.text(0.02, 0.015, note, fontsize=8.2, color="#555555")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
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
    book.to_csv(FIG / "data/clean/figure_12_7_book_period.csv", index=False)
    successor.to_csv(FIG / "data/clean/figure_12_7_successor.csv", index=False)
    compare(book_plot, FIG / "plots/comparisons/figure_12_7_book_period_review.png", "Figure 12-7 book-period comparison")
    compare(extended_plot, FIG / "plots/comparisons/figure_12_7_extended_review.png", "Figure 12-7 extended comparison")
    (FIG / "README.md").write_text("""# Figure 12-7 - Occupational accident deaths\n\nStatus: `partial_match`. Published anchor and CFOI observations are reconstructed from primary source material, but the mixed source definitions and blocked BLS archive downloads prevent a fully verified homogeneous series.\n\n- Original: [../../references/figures/figure_12_7.png](../../references/figures/figure_12_7.png)\n- Script: [../../scripts/reconstruct_12_7.py](../../scripts/reconstruct_12_7.py)\n- Book comparison: [plots/comparisons/figure_12_7_book_period_review.png](plots/comparisons/figure_12_7_book_period_review.png)\n- Extended comparison: [plots/comparisons/figure_12_7_extended_review.png](plots/comparisons/figure_12_7_extended_review.png)\n""")
    (FIG / "captions/caption.txt").write_text("Figure 12-7: Occupational accident deaths, US, 1913-2015. Recreated from published BLS, National Safety Council, CDC/NIOSH, OSHA, NCHS, and CFOI observations named in the book's source note. The 2006-2015 rates are BLS FTE rates multiplied by .95 as described by Pinker. The dashed 2016 point is a successor observation. Because source definitions and denominators change, this is a partial reconstruction, not a homogeneous verified series.")
    (FIG / "provenance/provenance.md").write_text("""# Figure 12-7 provenance\n\n## Book source line\n\nData are from different sources and may not be completely commensurable. The book names BLS/NSC/CDC NIOSH for 1913, 1933, and 1980; OSHA for 1970; BLS for 1993-1994; NCHS table 38 for 1995-2005; and BLS for 2006-2014. The latter are FTE rates multiplied by .95.\n\n## Recovered sources\n\n- CDC workplace safety article, including the 1913 and 1933 historical anchors and the 1980/1995 NIOSH discussion: `figures/12-7/data/raw/cdc_workplace_safety_1900_1999.html`.\n- CDC 1980-1997 report: `figures/12-7/data/raw/cdc_occupational_injuries_1980_1997.html`.\n- CDC Health, United States 2009 table: `figures/12-7/data/raw/cdc_health_us_2009.pdf`.\n- BLS CFOI 1992-2005 chart PDF, recovered via CDC Stacks: `figures/12-7/data/raw/cfoi_charts_1992_2005.pdf`.\n- Source-transcribed observations: `figures/12-7/data/raw/source_transcribed_rates.csv`.\n\nThe raw CSV is explicitly a transcription of published source tables/text, not of Pinker's plotted line. BLS archive PDFs were attempted but were blocked by the host's automated-access control; those failures are recorded in the source log.\n""")
    (FIG / "source_logs/source_log.md").write_text("""# Figure 12-7 source discovery log\n\n## Queries attempted\n\n- `occupational accident deaths 1913 1933 1980 source`\n- `CDC Improvements in Workplace Safety 1900-1999`\n- `BLS CFOI charts 1992-2005 rate`\n- `BLS CFOI charts 1992-2016 rate FTE`\n- `Pegula Janocha 2013 fatal work injuries`\n- `OSHA timeline 40 year history 1970 fatality rate`\n\n## Sources investigated\n\n- CDC MMWR 1999: accepted for 1913=61, 1933=37, and NIOSH 1980=7.5/1995=4.3 source context.\n- CDC MMWR 2001: accepted for the NTOF 1980-1997 methodology and 1980/1997 range.\n- CDC Health, United States 2009: accepted for published 1995, 2000, 2001, 2004-2007 checkpoints.\n- BLS CFOI archive 1992-2005 via CDC Stacks: accepted as a preserved BLS chart artifact; its PDF is image-heavy and values were transcribed from the official chart text available in search output.\n- BLS CFOI archive 1992-2016 and BLS MLR chart: investigated as primary sources. Automated downloads from bls.gov returned Access Denied, so the published chart values used here are explicitly marked as source transcription.\n- OSHA 40-year timeline: citation resolved, but the archived page did not yield a machine-readable full series.\n\n## Remaining uncertainties\n\nThe source line intentionally combines incompatible historical definitions. The 1970 value available from a BLS chart is 18.0 while the Pinker plot appears to use the OSHA-era estimate; exact OSHA timeline extraction and exact NCHS table 38 values for every year were not recovered.\n\n## Recommended next steps\n\nUse a browser/manual download of the BLS 1992-2016 archive and locate an archived OSHA timeline page. Compare all source-transcribed rows against those artifacts before any status promotion.\n""")
    (FIG / "search_iterations/search_iterations.md").write_text("""# Search iterations\n\n1. Inspected the PDF figure and extracted the complete mixed-source note.\n2. Recovered CDC primary text for 1913, 1933, 1980, and 1995 context.\n3. Recovered a preserved BLS CFOI 1992-2005 chart artifact and CDC Health US table.\n4. Attempted BLS archive downloads; automated access returned an explicit Access Denied page.\n5. Stored published-source transcriptions with source URL and basis columns.\n6. Generated and inspected both comparisons; the declining trajectory is recognizable, but source-vintage and 1970 differences remain.\n""")
    (FIG / "anomaly_reviews/anomaly_review.md").write_text("""# Anomaly review\n\nCritical evidence limitation: the BLS archive download for the 2006-2016 chart could not be retrieved automatically, so those values are explicitly source-transcribed from official published chart data. Major scientific limitation: the book itself warns that sources are not fully commensurable; employment-based and FTE-based rates are joined with a .95 adjustment. Major visual discrepancy: the 1970 anchor differs from the apparent Pinker point because the recoverable BLS chart reports 18.0 while Pinker's cited OSHA source may use a different denominator. Status remains `partial_match`.\n""")
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text("""# Discrepancy log\n\nThe recreated line has the same steep historical decline and low modern plateau as the PDF reference. The plotted 1970 point is lower than the apparent reference point because the primary recoverable BLS chart reports 18.0; the exact OSHA timeline value was not recovered. Modern annual fluctuations are also source-vintage dependent. No values were digitized from the reference image.\n""")
    (FIG / "review_checklist.md").write_text("""# Review checklist\n\n- [x] Original Supplemental PDF figure inspected\n- [x] Title, caption, and source note extracted\n- [x] CDC primary historical source recovered\n- [x] BLS CFOI chart artifact recovered via CDC Stacks\n- [x] Book and successor clean files written\n- [x] Book-period and extended plots generated\n- [x] Both side-by-side comparisons generated and inspected\n- [x] Source-transcribed rows labeled and sourced\n- [x] No Pinker plotted values used\n- [x] Mixed denominators and source breaks documented\n- [ ] Exact OSHA 1970 source extraction recovered\n- [ ] Exact BLS 2006-2014 archive artifact downloaded\n- [ ] Homogeneous verified series established\n""")
    lineage = {"schema_version": 1, "figure_id": "12-7", "book_citation": "BLS; National Safety Council; CDC NIOSH; OSHA; NCHS; CFOI", "script": "scripts/reconstruct_12_7.py", "mappings": [{"role": "book_period", "raw_inputs": ["figures/12-7/data/raw/source_transcribed_rates.csv", "figures/12-7/data/raw/cdc_workplace_safety_1900_1999.html", "figures/12-7/data/raw/cdc_health_us_2009.pdf"], "selection": "Published observations 1913-2015 from the cited source families", "transformation": "retain source rates; 2006-2015 FTE rates multiplied by .95", "clean": "figures/12-7/data/clean/figure_12_7_book_period.csv", "plot": "figures/12-7/plots/figure_12_7_book_period.png"}, {"role": "extension", "raw_inputs": ["figures/12-7/data/raw/source_transcribed_rates.csv"], "selection": "2016 BLS successor observation", "transformation": "render as dashed successor", "clean": "figures/12-7/data/clean/figure_12_7_successor.csv", "plot": "figures/12-7/plots/figure_12_7_extended.png"}]}
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    record = {"figure_id": "12-7", "title": "Occupational accident deaths, US, 1913-2015", "scientific_status": "partial_match", "artifact_kind": "reconstruction", "publication_status": "not_reviewed", "execution_status": "processed", "lifecycle_stage": "visual_review", "next_action": "Recover exact OSHA 1970 and BLS 2006-2014 source artifacts; reconcile denominators before promotion.", "notes": "Mixed sources as warned in book; source-transcribed values are not digitized from chart.", "extension": {"status": "successor_limited", "label": "BLS 2016 successor"}, "visual_review": {"status": "pending", "reference_basis": "original", "issues": ["1970 source mismatch", "mixed rate definitions", "BLS archive access blocked"]}, "artifacts": {"metadata": {"path": "figures/12-7/figure.json", "self": True}, "original_reference": {"path": "references/figures/figure_12_7.png"}, "book_period_reconstruction": {"path": "figures/12-7/plots/figure_12_7_book_period.png"}, "extended_reconstruction": {"path": "figures/12-7/plots/figure_12_7_extended.png"}, "book_period_clean": {"path": "figures/12-7/data/clean/figure_12_7_book_period.csv"}, "successor_clean": {"path": "figures/12-7/data/clean/figure_12_7_successor.csv"}, "book_period_comparison": {"path": "figures/12-7/plots/comparisons/figure_12_7_book_period_review.png"}, "extended_comparison": {"path": "figures/12-7/plots/comparisons/figure_12_7_extended_review.png"}, "caption": {"path": "figures/12-7/captions/caption.txt"}, "provenance": {"path": "figures/12-7/provenance/provenance.md"}, "source_log": {"path": "figures/12-7/source_logs/source_log.md"}, "anomaly_review": {"path": "figures/12-7/anomaly_reviews/anomaly_review.md"}, "discrepancy_log": {"path": "figures/12-7/discrepancy_logs/discrepancy_log.md"}, "review_checklist": {"path": "figures/12-7/review_checklist.md"}, "lineage": {"path": "figures/12-7/lineage/lineage.json"}, "reconstruction_script": {"path": "scripts/reconstruct_12_7.py"}}}
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")


def main() -> None:
    book, successor = load_data()
    book_plot = FIG / "plots/figure_12_7_book_period.png"
    extended_plot = FIG / "plots/figure_12_7_extended.png"
    draw(book, book_plot, extended=False)
    draw(pd.concat([book, successor], ignore_index=True), extended_plot, extended=True)
    write_package(book, successor, book_plot, extended_plot)
    print(json.dumps({"figure": "12-7", "book_rows": len(book), "successor_rows": len(successor)}, indent=2))


if __name__ == "__main__":
    main()
