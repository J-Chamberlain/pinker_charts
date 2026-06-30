from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()


@dataclass(frozen=True)
class FigureMeta:
    fig_id: str
    chapter: str
    title: str
    claim: str
    source_note: str
    crop_page: str


FIGURES = {
    "7-3": FigureMeta(
        "7-3",
        "7",
        "Undernourishment, 1970-2015",
        "The share of people in developing countries who are undernourished declined from 1970 to 2015.",
        "Our World in Data, Roser 2016j, based on data from the Food and Agriculture Organization 2014, also reported in FAOSTAT.",
        "page-06.png",
    ),
    "7-4": FigureMeta(
        "7-4",
        "7",
        "Famine deaths, 1860-2016",
        "Famine deaths per 100,000 people per decade fell sharply after the mid-twentieth century.",
        "Our World in Data, Hasell & Roser 2017, based on data from Devereux 2000; O Grada 2009; White 2011; EM-DAT; and other sources.",
        "page-06.png",
    ),
    "8-1": FigureMeta(
        "8-1",
        "8",
        "Gross World Product, 1-2015",
        "Gross world product was nearly flat for most of history and rose steeply after industrialization.",
        "Our World in Data, Roser 2016c, based on data from the World Bank and from Angus Maddison and Maddison Project 2014.",
        "page-07.png",
    ),
    "8-2": FigureMeta(
        "8-2",
        "8",
        "GDP per capita, 1600-2015",
        "Selected countries and the world became much richer, with uneven timing and levels.",
        "Our World in Data, Roser 2016c, based on data from the World Bank and from Maddison Project 2014.",
        "page-07.png",
    ),
    "8-5": FigureMeta(
        "8-5",
        "8",
        "Extreme poverty (number), 1820-2015",
        "The number of people in extreme poverty fell even as the number not in extreme poverty rose rapidly.",
        "Our World in Data, Roser & Ortiz-Ospina 2017, based on data from Bourguignon & Morrison 2002 (1820-1992) and the World Bank 2016g (1981-2015).",
        "page-09.png",
    ),
}


def base(fig_id: str) -> Path:
    root = ROOT / "figures" / fig_id
    for part in [
        "metadata",
        "provenance",
        "source_logs",
        "search_iterations",
        "discrepancy_logs",
        "anomaly_reviews",
        "captions",
        "lineage",
        "plots/book_period",
        "plots/extended",
        "plots/comparisons",
        "plots/diagnostics",
        "data/raw",
        "data/clean",
        "checksums",
    ]:
        (root / part).mkdir(parents=True, exist_ok=True)
    return root


def style(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.tick_params(labelsize=9)


def savefig(fig, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def trim(im: Image.Image) -> Image.Image:
    bg = Image.new("RGB", im.size, "white")
    bbox = ImageChops.difference(im.convert("RGB"), bg).getbbox()
    return im.crop(bbox) if bbox else im


def side_by_side(reference: Path, recreated: Path, output: Path, title: str) -> None:
    ref = trim(Image.open(reference).convert("RGB"))
    rec = trim(Image.open(recreated).convert("RGB"))
    panel_w, panel_h = 980, 720
    margin, gap, header_h, title_h = 45, 45, 58, 58
    canvas = Image.new("RGB", (margin * 2 + panel_w * 2 + gap, title_h + header_h + panel_h + margin), "white")
    draw = ImageDraw.Draw(canvas)
    try:
        title_font = ImageFont.truetype("Arial.ttf", 30)
        label_font = ImageFont.truetype("Arial.ttf", 24)
    except OSError:
        title_font = label_font = None

    def paste_fit(im: Image.Image, x: int, y: int) -> None:
        fitted = ImageOps.contain(im, (panel_w, panel_h), method=Image.Resampling.LANCZOS)
        canvas.paste(fitted, (x + (panel_w - fitted.width) // 2, y + (panel_h - fitted.height) // 2))
        draw.rectangle([x, y, x + panel_w, y + panel_h], outline=(230, 230, 230), width=1)

    left_x = margin
    right_x = margin + panel_w + gap
    draw.text((canvas.width // 2, 18), title, fill="black", anchor="ma", font=title_font)
    draw.text((left_x + panel_w // 2, title_h + 8), "Book/PDF reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, title_h + 8), "Recreated", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    canvas.save(output)


def compare_images(info: FigureMeta) -> None:
    b = base(info.fig_id)
    stem = info.fig_id.replace("-", "_")
    ref = b / f"plots/comparisons/kindle_reference_figure_{stem}.png"
    book_plot = b / f"plots/book_period/figure_{stem}_book_period_reconstruction.png"
    ext_plot = b / f"plots/extended/figure_{stem}_extended_reconstruction.png"
    side_by_side(ref, book_plot, b / f"plots/comparisons/figure_{stem}_book_period_comparison.png", f"Figure {info.fig_id} book-period comparison")
    side_by_side(ref, ext_plot, b / f"plots/comparisons/figure_{stem}_extended_comparison.png", f"Figure {info.fig_id} extended comparison")


@dataclass(frozen=True)
class Review:
    fig_id: str
    title: str
    previous_status: str
    status: str
    confidence: str
    visual_validation: str
    decision: str
    notes: str


REVIEWS = {
    "7-3": Review(
        "7-3",
        "Undernourishment, 1970-2015",
        "partial_match",
        "partial_match",
        "medium-low",
        "partial; improved labels but incomplete regional vintage",
        "Retain partial_match and lower confidence.",
        "Fresh review found that the prior reconstruction substituted broad Africa/Asia/World curves for several book regional curves. The remediation replaces those with current FAO successor regional entities where available, but the exact Roser 2016j/FAO 2014 regional vintage and 1991-1999 regional segments remain unrecovered.",
    ),
    "7-4": Review(
        "7-4",
        "Famine deaths, 1860-2016",
        "partial_match",
        "partial_match",
        "medium-low",
        "partial; aggregation improved with successor OWID decadal-rate series",
        "Retain partial_match and lower confidence.",
        "The previous reconstruction recomputed rates from an event table with a current population denominator. Remediation uses OWID's explicit decadal famine-death-rate grapher series, which fixes the aggregation treatment, but it is a 2025 World Peace Foundation/OWID successor rather than the archived 2017 Hasell-Roser book vintage.",
    ),
    "8-1": Review(
        "8-1",
        "Gross World Product, 1-2015",
        "updated_equivalent",
        "updated_equivalent",
        "medium",
        "strong shape match; source-vintage/scaling differences remain",
        "Do not promote to verified_reproduction.",
        "The successor OWID/Maddison/World Bank series preserves the hockey-stick shape and book-period coverage, but the 2015 scale is materially above the printed figure's apparent endpoint, so this is an updated equivalent rather than an exact reproduction.",
    ),
    "8-2": Review(
        "8-2",
        "GDP per capita, 1600-2015",
        "updated_equivalent",
        "updated_equivalent",
        "medium",
        "publication-readable, but not source-identical",
        "Retain updated_equivalent.",
        "The selected countries and line ordering broadly match the book, but current Maddison 2020/OWID data are not the cited Maddison Project 2014/World Bank 2016 vintage. Remaining differences are not typography-only.",
    ),
    "8-5": Review(
        "8-5",
        "Extreme poverty (number), 1820-2015",
        "verified_reproduction",
        "verified_reproduction",
        "high",
        "verified after falsification audit",
        "Retain verified_reproduction.",
        "A falsification audit found no material source, encoding, or endpoint issue. The reconstruction uses the cited OWID historical absolute-count series and matches the stacked-area visual claim; remaining differences are production styling only.",
    ),
}


SCORES = {
    "7-3": [
        ("Source recovery", 2, "Main developing-world line is recovered; regional book vintage is not."),
        ("Citation chain", 3, "FAO/OWID chain is documented, but Roser 2016j regional file remains missing."),
        ("Visual similarity", 2, "Improved regional labels and removed World substitution, but regional curves start at 2000 rather than the book's early-1990s coverage."),
        ("Extension quality", 3, "Current FAO successor extends to 2024 and is clearly separated as successor evidence."),
        ("Caption quality", 4, "Caption now states the substitution risk and missing vintage."),
        ("Editorial quality", 4, "Status is not over-promoted and discrepancies are explicit."),
        ("Overall confidence", 2, "Useful source-family partial match only."),
    ],
    "7-4": [
        ("Source recovery", 3, "Event table and current OWID decadal-rate successor recovered; exact archived 2017 grapher not recovered."),
        ("Citation chain", 3, "Hasell-Roser/OWID and successor WPF/OWID chains are documented separately."),
        ("Visual similarity", 3, "Decadal rate shape improves, but the successor series starts at 1870 and includes revised rates."),
        ("Extension quality", 3, "2020s successor exists but is provisional and not book-comparable."),
        ("Caption quality", 4, "Caption explicitly names aggregation and vintage differences."),
        ("Editorial quality", 4, "Confidence lowered and prior recomputation caveat documented."),
        ("Overall confidence", 3, "Better aggregation fidelity, still not an exact book reproduction."),
    ],
    "8-1": [
        ("Source recovery", 4, "OWID successor source family recovered, but exact 2016c archive is absent."),
        ("Citation chain", 4, "Maddison/World Bank source chain is clear."),
        ("Visual similarity", 4, "Shape is very close; endpoint scale differs from the book."),
        ("Extension quality", 4, "Post-2015 extension is coherent successor data."),
        ("Caption quality", 4, "Caption identifies successor vintage and scale caveat."),
        ("Editorial quality", 4, "Not promoted above evidence."),
        ("Overall confidence", 4, "Strong updated equivalent, not verified."),
    ],
    "8-2": [
        ("Source recovery", 3, "Current Maddison 2020 series recovered; Maddison Project 2014 vintage not recovered."),
        ("Citation chain", 4, "Country series source family is well documented."),
        ("Visual similarity", 3, "Country set/order match broadly, with label overlap and revised levels."),
        ("Extension quality", 4, "Extension is consistent with the successor dataset."),
        ("Caption quality", 4, "Caption distinguishes typography issues from source vintage issues."),
        ("Editorial quality", 4, "Classification remains conservative."),
        ("Overall confidence", 3, "Good update, not source-identical."),
    ],
    "8-5": [
        ("Source recovery", 5, "Cited OWID absolute-count source is recovered."),
        ("Citation chain", 5, "Bourguignon-Morrison and World Bank/PovcalNet chain is explicit."),
        ("Visual similarity", 4, "Stacked areas and endpoint behavior match; only production styling differs."),
        ("Extension quality", 4, "No comparable extension is plotted, avoiding false comparability."),
        ("Caption quality", 5, "Caption accurately states source and no-extension treatment."),
        ("Editorial quality", 5, "Classification survived falsification audit."),
        ("Overall confidence", 5, "Verified reproduction remains justified."),
    ],
}


SERIES_7_3 = [
    ("Developing world", "Present, 1970-2015 main black line.", "Recovered from OWID/FAO developing-country dataset, 1970-2015.", "Good source-family match."),
    ("Sub-Saharan Africa", "Present, early-1990s-2015 regional line.", "Current FAO successor entity `Sub-Saharan Africa (FAO)`, 2000-2015 book-period subset.", "Partial; early years missing and vintage differs."),
    ("Southeast Asia", "Present, early-1990s-2015 regional line.", "Current FAO successor entity `South-eastern Asia (FAO)`, 2000-2015 book-period subset.", "Partial; early years missing and naming/vintage differ."),
    ("South Asia", "Present, early-1990s-2015 regional line.", "Current FAO successor entity `Southern Asia (FAO)`, 2000-2015 book-period subset.", "Partial; source-family curve only."),
    ("East Asia", "Present, early-1990s-2015 regional line.", "Current FAO successor entity `Eastern Asia (FAO)`, 2000-2015 book-period subset.", "Weak partial; levels/trend are revised and early years missing."),
    ("Latin America", "Present, early-1990s-2015 regional line.", "Current FAO successor entity `Latin America and the Caribbean (FAO)`, 2000-2015 book-period subset.", "Partial; early years missing and regional definition is broader label."),
    ("World", "Absent from original.", "Removed from book-period recreation; retained only as a documented successor diagnostic if needed.", "Prior substitution corrected."),
]


def raw_col(df: pd.DataFrame, prefix: str | None = None) -> str:
    candidates = [c for c in df.columns if c not in {"Entity", "Code", "Year"}]
    if prefix:
        for c in candidates:
            if c.startswith(prefix):
                return c
    return candidates[-1]


def plot_7_3() -> None:
    b = base("7-3")
    dev = pd.read_csv(b / "data/raw/owid_fao_developing_countries_2017.csv")
    cur = pd.read_csv(b / "data/raw/owid_current_prevalence_of_undernourishment.csv")
    dev_col = raw_col(dev)
    cur_col = raw_col(cur, "2.1.1")
    dev_clean = dev.rename(columns={dev_col: "prevalence_percent"})[["Entity", "Year", "prevalence_percent"]]
    cur_clean = cur.rename(columns={cur_col: "prevalence_percent"})[["Entity", "Year", "prevalence_percent"]]
    region_map = {
        "Sub-Saharan Africa": "Sub-Saharan Africa (FAO)",
        "South Asia": "Southern Asia (FAO)",
        "Southeast Asia": "South-eastern Asia (FAO)",
        "East Asia": "Eastern Asia (FAO)",
        "Latin America": "Latin America and the Caribbean (FAO)",
    }
    region_rows = cur_clean[cur_clean["Entity"].isin(region_map.values()) & cur_clean["Year"].between(2000, 2015)].copy()
    region_rows["Entity"] = region_rows["Entity"].map({v: k for k, v in region_map.items()})
    book = pd.concat([dev_clean, region_rows], ignore_index=True)
    book.to_csv(b / "data/clean/figure_7_3_book_period_clean.csv", index=False)
    cur_clean.to_csv(b / "data/clean/figure_7_3_extended_clean.csv", index=False)

    colors = {
        "Developing world": "0.05",
        "Sub-Saharan Africa": "0.30",
        "South Asia": "0.48",
        "Southeast Asia": "0.62",
        "East Asia": "0.72",
        "Latin America": "0.18",
    }

    def draw(out: Path, extended: bool) -> None:
        fig, ax = plt.subplots(figsize=(8.4, 5.2), dpi=180)
        dev_line = dev_clean.sort_values("Year")
        ax.plot(dev_line["Year"], dev_line["prevalence_percent"], color=colors["Developing world"], linewidth=3.1)
        ax.text(1972, 33.0, "Developing world", fontsize=10, weight="bold", color=colors["Developing world"])
        offsets = {
            "Sub-Saharan Africa": 0.7,
            "South Asia": -1.0,
            "Southeast Asia": 0.5,
            "East Asia": -0.5,
            "Latin America": 0.4,
        }
        for label, entity in region_map.items():
            sub = cur_clean[cur_clean["Entity"].eq(entity)].sort_values("Year")
            book_sub = sub[sub["Year"].between(2000, 2015)]
            ax.plot(book_sub["Year"], book_sub["prevalence_percent"], color=colors[label], linewidth=2)
            if extended:
                ext_sub = sub[sub["Year"] > 2015]
                ax.plot(ext_sub["Year"], ext_sub["prevalence_percent"], color=colors[label], linewidth=1.6, linestyle="--")
            label_x = 2015 if not extended else min(2024, int(sub["Year"].max()))
            label_data = sub[sub["Year"].eq(label_x)]
            if not label_data.empty:
                ax.text(label_x + 0.3, float(label_data["prevalence_percent"].iloc[-1]) + offsets[label], label, fontsize=8, color=colors[label], va="center")
        ax.set_xlim(1970, 2026 if extended else 2017)
        ax.set_ylim(0, 36)
        ax.set_ylabel("Percentage of people who are undernourished")
        ax.set_title("Figure 7-3: Undernourishment, 1970-2015", loc="left", fontsize=12)
        ax.text(0, -0.16, "Source: OWID/FAO developing-country data plus current FAO regional successor entities; exact Roser 2016j regional vintage not recovered.", transform=ax.transAxes, fontsize=7, va="top")
        style(ax)
        savefig(fig, out)

    draw(b / "plots/book_period/figure_7_3_book_period_reconstruction.png", False)
    draw(b / "plots/extended/figure_7_3_extended_reconstruction.png", True)


def plot_7_4() -> None:
    b = base("7-4")
    raw = b / "data/raw/owid_death_rate_from_famines_by_decade.csv"
    meta = b / "data/raw/owid_death_rate_from_famines_by_decade.metadata.json"
    pd.read_csv("https://ourworldindata.org/grapher/death-rate-from-famines-by-decade.csv").to_csv(raw, index=False)
    metadata = requests.get(
        "https://ourworldindata.org/grapher/death-rate-from-famines-by-decade.metadata.json",
        timeout=30,
    ).json()
    meta.write_text(json.dumps(metadata, indent=2) + "\n")
    df = pd.read_csv(raw)
    col = raw_col(df)
    world = df[df["Entity"].eq("World")][["Year", col]].rename(columns={col: "deaths_per_100k_per_decade"}).sort_values("Year")
    book = world[world["Year"].between(1860, 2010)].copy()
    book["decade_label"] = book["Year"].astype(int).astype(str) + "s"
    book.to_csv(b / "data/clean/figure_7_4_book_period_clean.csv", index=False)
    ext = world[world["Year"].between(1860, 2020)].copy()
    ext["decade_label"] = ext["Year"].astype(int).astype(str) + "s"
    ext.to_csv(b / "data/clean/figure_7_4_extended_clean.csv", index=False)

    def draw(data: pd.DataFrame, out: Path, extended: bool) -> None:
        fig, ax = plt.subplots(figsize=(8.4, 5.2), dpi=180)
        base_series = data[data["Year"] <= 2010]
        ax.plot(base_series["Year"], base_series["deaths_per_100k_per_decade"], color="0.05", linewidth=2.6)
        if extended:
            ext_series = data[data["Year"] > 2010]
            ax.plot(ext_series["Year"], ext_series["deaths_per_100k_per_decade"], color="0.45", linewidth=2, linestyle="--")
        ax.set_xlim(1860, 2024 if extended else 2016)
        ax.set_ylim(0, 1500)
        ticks = list(range(1860, 2030 if extended else 2020, 20))
        ax.set_xticks(ticks)
        ax.set_xticklabels([f"{t}s" for t in ticks], rotation=45, ha="right")
        ax.set_ylabel("Famine deaths per 100,000 people per decade")
        ax.set_title("Figure 7-4: Famine deaths, 1860-2016", loc="left", fontsize=12)
        note = "Source: OWID decadal famine-death-rate successor series. Book-era 2017 Hasell-Roser vintage not recovered."
        if extended:
            note += " 2020s value is provisional successor data."
        ax.text(0, -0.20, note, transform=ax.transAxes, fontsize=7, va="top")
        style(ax)
        savefig(fig, out)

    draw(book, b / "plots/book_period/figure_7_4_book_period_reconstruction.png", False)
    draw(ext, b / "plots/extended/figure_7_4_extended_reconstruction.png", True)


def write_metadata_and_docs() -> None:
    for fig_id, review in REVIEWS.items():
        b = base(fig_id)
        info = FIGURES[fig_id]
        stem = fig_id.replace("-", "_")
        metadata = {
            "figure_id": fig_id,
            "chapter": info.chapter,
            "title": review.title,
            "book_page": f"Rendered PDF preview page {info.crop_page}",
            "claim_summary": info.claim,
            "book_citation": info.source_note,
            "download_date": TODAY,
            "reproduction_status": review.status,
            "confidence_score": review.confidence,
            "visual_validation": review.visual_validation,
            "editorial_remediation_decision": review.decision,
            "notes": review.notes,
            "canonical_artifacts": {
                "original_reference": f"figures/{fig_id}/plots/comparisons/kindle_reference_figure_{stem}.png",
                "book_period_reconstruction": f"figures/{fig_id}/plots/book_period/figure_{stem}_book_period_reconstruction.png",
                "extended_reconstruction": f"figures/{fig_id}/plots/extended/figure_{stem}_extended_reconstruction.png",
                "book_period_comparison": f"figures/{fig_id}/plots/comparisons/figure_{stem}_book_period_comparison.png",
                "extended_comparison": f"figures/{fig_id}/plots/comparisons/figure_{stem}_extended_comparison.png",
            },
        }
        (b / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
        (b / "captions/caption.txt").write_text(
            f"Figure {fig_id}: {review.title}. Editorial remediation status: {review.status}; confidence: {review.confidence}. "
            f"{review.notes} Source note: {info.source_note}\n"
        )
        if fig_id == "7-3":
            series_lines = ["| Series | Original | Recreated | Match |", "| --- | --- | --- | --- |"]
            series_lines += [f"| {a} | {b0} | {c} | {d} |" for a, b0, c, d in SERIES_7_3]
            series_section = "\n".join(series_lines)
        else:
            series_section = "No regional-series table required for this figure."
        score_lines = ["| Criterion | Score (1-5) | Justification |", "| --- | ---: | --- |"]
        score_lines += [f"| {criterion} | {score} | {justification} |" for criterion, score, justification in SCORES[fig_id]]
        challenge = {
            "7-3": [
                ("What would Steven Pinker question?", "Whether each book regional curve is present and named correctly. Resolved partly: labels now target the right FAO successor regions; documented blocker: exact 1991-2015 regional vintage missing."),
                ("What would a skeptical data journalist question?", "Whether Africa/Asia/World substitutions hid missing series. Resolved: World substitution removed; broad-region substitutions replaced with specific successor region entities."),
                ("What would another researcher question?", "Whether current FAO 2000-2024 values can stand in for FAO 2014. Documented as a research task, not treated as verified."),
            ],
            "7-4": [
                ("What would Steven Pinker question?", "Whether the declining decadal rate is computed the same way as the book. Partly resolved with OWID's own decadal-rate series; vintage remains documented."),
                ("What would a skeptical data journalist question?", "Whether the endpoint and smoothing were manipulated. Resolved/documented: no smoothing; decade-start bins; 2020s only in successor extension."),
                ("What would another researcher question?", "Whether revised WPF 2025 rates are comparable with Hasell-Roser 2017. Documented as source-vintage blocker."),
            ],
            "8-1": [
                ("What would Steven Pinker question?", "Whether the near-vertical post-1800 rise remains visible. Resolved: yes."),
                ("What would a skeptical data journalist question?", "Why 2015 scale is higher than the book. Documented: current successor data revisions prevent verified reproduction."),
                ("What would another researcher question?", "Whether Maddison Project 2014 was recovered. Documented as outstanding source task."),
            ],
            "8-2": [
                ("What would Steven Pinker question?", "Whether the selected countries and ordering still communicate uneven enrichment. Resolved: yes, with label caveats."),
                ("What would a skeptical data journalist question?", "Whether label overlap conceals country ranking differences. Documented: placement improved only modestly; source differences remain."),
                ("What would another researcher question?", "Whether current Maddison 2020 is source-equivalent to Maddison 2014. Documented: no, status remains updated_equivalent."),
            ],
            "8-5": [
                ("What would Steven Pinker question?", "Whether the absolute number in extreme poverty falls while non-poor population rises. Resolved: yes."),
                ("What would a skeptical data journalist question?", "Whether the stacked areas swap categories or hide a post-2015 update. Resolved: categories verified; no successor extension plotted."),
                ("What would another researcher question?", "Whether the cited historical count series is recovered. Resolved: yes, retained verified_reproduction."),
            ],
        }[fig_id]
        challenge_lines = "\n".join(f"- **{q}** {a}" for q, a in challenge)
        (b / "anomaly_reviews/anomaly_review.md").write_text(
            f"# Editorial Remediation Review: Figure {fig_id}\n\n"
            f"Status decision: `{review.status}` ({review.confidence}).\n\n"
            f"{review.notes}\n\n"
            "## Series Audit\n\n"
            f"{series_section}\n\n"
            "## Reviewer Challenge\n\n"
            f"{challenge_lines}\n\n"
            "## Scorecard\n\n"
            f"{chr(10).join(score_lines)}\n"
        )
        (b / "discrepancy_logs/discrepancy_log.md").write_text(
            f"# Discrepancy Log: Figure {fig_id}\n\n"
            f"Previous status: `{review.previous_status}`\n\n"
            f"Editorial remediation status: `{review.status}`\n\n"
            f"Confidence: `{review.confidence}`\n\n"
            f"{review.notes}\n"
        )
        (b / "review_checklist.md").write_text(
            f"# Editorial Review Checklist: Figure {fig_id}\n\n"
            "- [x] Fresh visual comparison performed.\n"
            "- [x] Source chain reassessed.\n"
            "- [x] Reviewer challenge answered.\n"
            "- [x] Editorial scorecard completed.\n"
            f"- [x] Final classification set to `{review.status}`.\n"
        )
        source_notes = {
            "7-3": [
                "Rechecked the original crop for the regional inventory: Developing world, Sub-Saharan Africa, Southeast Asia, South Asia, East Asia, and Latin America.",
                "Rechecked local OWID FAO datasets and the current OWID `prevalence-of-undernourishment` grapher.",
                "Recovered current FAO successor entities for each named region, but only for 2000 onward: `Sub-Saharan Africa (FAO)`, `South-eastern Asia (FAO)`, `Southern Asia (FAO)`, `Eastern Asia (FAO)`, and `Latin America and the Caribbean (FAO)`.",
                "The exact Roser 2016j / FAO 2014 regional file with early-1990s coverage was not recovered; this remains a research task.",
            ],
            "7-4": [
                "Rechecked the original crop for x-axis treatment: decade labels from 1860s through 2010-2016, no visible smoothing.",
                "The previous reconstruction computed decadal rates from an event table and current OWID world population; this was documented as non-identical aggregation/denominator treatment.",
                "Recovered OWID's explicit `death-rate-from-famines-by-decade` grapher series and metadata, which defines rates as sum of famine deaths in each ten-year period divided by population.",
                "The recovered grapher is a 2025 World Peace Foundation / OWID successor, not the archived 2017 Hasell-Roser book vintage; this explains remaining visual divergence and prevents promotion.",
            ],
        }.get(fig_id, [
            f"Editorial review reassessed source-family recovery and retained the conservative status decision: {review.decision}",
            review.notes,
        ])
        (b / "source_logs/source_log.md").write_text(
            f"# Source Discovery Log: Figure {fig_id}\n\n"
            f"Editorial remediation date: {TODAY}\n\n"
            + "\n".join(f"- {note}" for note in source_notes)
            + "\n\nPrimary public source URLs used during remediation:\n\n"
            "- https://ourworldindata.org/grapher/prevalence-of-undernourishment.csv\n"
            "- https://ourworldindata.org/grapher/death-rate-from-famines-by-decade.csv\n"
            "- https://ourworldindata.org/grapher/world-gdp-over-the-last-two-millennia.csv\n"
            "- https://ourworldindata.org/grapher/gdp-per-capita-maddison-2020.csv\n"
            "- https://ourworldindata.org/grapher/world-population-in-extreme-poverty-absolute.csv\n"
        )
        (b / "provenance/provenance.md").write_text(
            f"# Provenance: Figure {fig_id}\n\n"
            f"Book/PDF figure -> source note -> source-family recovery -> `scripts/remediate_track_b_editorial.py` -> regenerated review artifacts.\n\n"
            f"Book source note: {info.source_note}\n\n"
            f"Editorial decision: `{review.status}` with `{review.confidence}` confidence.\n\n"
            f"{review.notes}\n"
        )
        (b / "README.md").write_text(f"# Figure {fig_id}: {review.title}\n\nStatus: `{review.status}`.\n\n{review.notes}\n")
        checksums = []
        for p in sorted(b.rglob("*")):
            if p.is_file() and "checksums" not in p.parts:
                checksums.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(b)}")
        (b / "checksums/sha256sums.txt").write_text("\n".join(checksums) + "\n")


def write_report() -> None:
    lines = [
        "# Track B Editorial Remediation",
        "",
        f"Date: {TODAY}",
        "",
        "Scope: editorial review and remediation only. No new production-batch figures were started.",
        "",
        "## Status Changes",
        "",
        "| Figure | Previous status | Remediated status | Confidence | Decision |",
        "| --- | --- | --- | --- | --- |",
    ]
    for review in REVIEWS.values():
        lines.append(f"| {review.fig_id} | `{review.previous_status}` | `{review.status}` | {review.confidence} | {review.decision} |")
    lines += ["", "## Figure 7-3 Series Audit", "", "| Series | Original | Recreated | Match |", "| --- | --- | --- | --- |"]
    lines += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in SERIES_7_3]
    lines += ["", "## Per-Figure Findings", ""]
    for review in REVIEWS.values():
        lines += [
            f"### Figure {review.fig_id} - {review.title}",
            "",
            review.notes,
            "",
            "#### Reviewer Challenge",
            "",
            (ROOT / f"figures/{review.fig_id}/anomaly_reviews/anomaly_review.md").read_text().split("## Reviewer Challenge\n\n", 1)[1].split("\n\n## Scorecard", 1)[0],
            "",
            "#### Scorecard",
            "",
            "| Criterion | Score (1-5) | Justification |",
            "| --- | ---: | --- |",
        ]
        lines += [f"| {criterion} | {score} | {justification} |" for criterion, score, justification in SCORES[review.fig_id]]
        stem = review.fig_id.replace("-", "_")
        lines += [
            "",
            "#### Updated Comparisons",
            "",
            f"![Figure {review.fig_id} book-period comparison](../figures/{review.fig_id}/plots/comparisons/figure_{stem}_book_period_comparison.png)",
            "",
            f"![Figure {review.fig_id} extended comparison](../figures/{review.fig_id}/plots/comparisons/figure_{stem}_extended_comparison.png)",
            "",
        ]
    lines += [
        "## Remaining Blockers",
        "",
        "- Figure 7-3: exact Roser 2016j / FAO 2014 regional data with early-1990s coverage remains unrecovered.",
        "- Figure 7-4: exact archived 2017 Hasell-Roser OWID decadal-rate output remains unrecovered; current WPF/OWID successor is documented separately.",
        "- Figure 8-1: exact OWID Roser 2016c/Maddison Project 2014 GDP vintage remains unrecovered.",
        "- Figure 8-2: exact Maddison Project 2014/World Bank vintage remains unrecovered.",
        "- Figure 8-5: no material blocker after audit.",
        "",
    ]
    (ROOT / "reports/track_b_editorial_remediation.md").write_text("\n".join(lines))


def update_project_state_addendum() -> None:
    path = ROOT / "PROJECT_STATE.md"
    text = path.read_text()
    marker = "\n## Track B Editorial Remediation Addendum\n"
    text = text.split(marker)[0].rstrip()
    rows = "\n".join(
        f"| {r.fig_id} | `{r.previous_status}` | `{r.status}` | {r.confidence} | {r.decision} |"
        for r in REVIEWS.values()
    )
    text += (
        marker
        + f"\nDate: {TODAY}\n\n"
        + "| Figure | Prior status | Remediated status | Confidence | Editorial decision |\n"
        + "| --- | --- | --- | --- | --- |\n"
        + rows
        + "\n\n"
        + "See `reports/track_b_editorial_remediation.md` for the full reviewer challenge, scorecards, comparison images, and remaining blockers.\n"
    )
    path.write_text(text.rstrip() + "\n")


def update_registry_files() -> None:
    registry_path = ROOT / "data/figure_registry.csv"
    rows = list(csv.DictReader(registry_path.open()))
    registry_updates = {
        "7-3": {
            "current_status": "partial_match",
            "lifecycle_stage": "editorial_remediated_partial_source_family_reconstruction",
            "priority": "high",
            "current_owner": "Codex",
            "next_action": "Research task: recover exact Roser 2016j / FAO 2014 regional data with early-1990s coverage before any promotion.",
            "notes": f"Editorial remediation {TODAY}: all named regional successor curves now plotted where available; World substitution removed; confidence lowered because exact regional vintage and early regional segments remain unrecovered.",
        },
        "7-4": {
            "current_status": "partial_match",
            "lifecycle_stage": "editorial_remediated_successor_decadal_rate_reconstruction",
            "priority": "high",
            "current_owner": "Codex",
            "next_action": "Research task: recover archived 2017 Hasell-Roser OWID decadal-rate grapher/output and denominator notes.",
            "notes": f"Editorial remediation {TODAY}: replaced hand-computed event-table rate with OWID decadal-rate successor series; confidence lowered because successor vintage diverges visibly from book-era curve.",
        },
        "8-1": {
            "current_status": "updated_equivalent",
            "lifecycle_stage": "editorial_reviewed_successor_equivalent",
            "priority": "high",
            "current_owner": "Codex",
            "next_action": "Recover exact OWID Roser 2016c/Maddison Project 2014 vintage before considering verified_reproduction.",
            "notes": f"Editorial remediation {TODAY}: remains updated_equivalent, not verified_reproduction, because current successor scaling differs from the printed 2015 endpoint.",
        },
        "8-2": {
            "current_status": "updated_equivalent",
            "lifecycle_stage": "editorial_reviewed_successor_equivalent",
            "priority": "high",
            "current_owner": "Codex",
            "next_action": "Recover exact Maddison Project 2014/World Bank 2016 vintage before considering verified_reproduction.",
            "notes": f"Editorial remediation {TODAY}: remains updated_equivalent; source-vintage differences remain in addition to label/typography issues.",
        },
        "8-5": {
            "current_status": "verified_reproduction",
            "lifecycle_stage": "editorial_audited_verified_reproduction",
            "priority": "publication_review",
            "current_owner": "Codex",
            "next_action": "No source blocker; retain verified_reproduction unless future audit finds a material issue.",
            "notes": f"Editorial remediation {TODAY}: falsification audit found no material issue; classification retained.",
        },
    }
    for row in rows:
        update = registry_updates.get(row["figure_id"])
        if update:
            row.update(update)
    with registry_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data/figure_registry.json").write_text(json.dumps(rows, indent=2) + "\n")

    metadata_path = ROOT / "data/metadata/figure_metadata.csv"
    metadata_rows = list(csv.DictReader(metadata_path.open()))
    review_notes = {fig_id: review.notes for fig_id, review in REVIEWS.items()}
    for row in metadata_rows:
        review = REVIEWS.get(row["figure_id"])
        if not review:
            continue
        row["reproduction_status"] = review.status
        row["confidence_score"] = review.confidence
        row["visual_validation"] = review.visual_validation
        row["notes"] = review_notes[review.fig_id]
    with metadata_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=metadata_rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(metadata_rows)


def main() -> None:
    plot_7_3()
    plot_7_4()
    for fig_id in REVIEWS:
        compare_images(FIGURES[fig_id])
    write_metadata_and_docs()
    write_report()
    update_project_state_addendum()
    update_registry_files()


if __name__ == "__main__":
    main()
