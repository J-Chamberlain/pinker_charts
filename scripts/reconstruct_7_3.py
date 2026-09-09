from __future__ import annotations

import csv
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/7-3"
ARCHIVED_XLSX = FIG / "data/candidates/fao_food_security_indicators_archived_20160317.xlsx"
EXTRACTED = FIG / "data/candidates/fao_food_security_indicators_archived_20160317_v_2_6_extracted.csv"
BOOK_CLEAN = FIG / "data/clean/figure_7_3_book_period_clean.csv"
EXTENDED_CLEAN = FIG / "data/clean/figure_7_3_extended_clean.csv"

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_OFFICE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


SERIES = {
    "Developing countries": "Developing world",
    "Sub-Saharan Africa": "Sub-Saharan Africa",
    "South-Eastern Asia": "Southeast Asia",
    "Southern Asia": "South Asia",
    "Eastern Asia": "East Asia",
    "Latin America": "Latin America",
}


def column_number(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def sheet_rows(path: Path, sheet_name: str) -> list[list[str]]:
    with zipfile.ZipFile(path) as zf:
        shared_strings: list[str] = []
        strings_root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
        for si in strings_root.findall(f"{{{NS_MAIN}}}si"):
            shared_strings.append("".join(t.text or "" for t in si.findall(f".//{{{NS_MAIN}}}t")))

        rel_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rels = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rel_root.findall(f"{{{NS_REL}}}Relationship")}
        workbook = ET.fromstring(zf.read("xl/workbook.xml"))

        target = None
        for sheet in workbook.findall(f"{{{NS_MAIN}}}sheets/{{{NS_MAIN}}}sheet"):
            if sheet.attrib["name"] == sheet_name:
                rid = sheet.attrib[f"{{{NS_OFFICE_REL}}}id"]
                target = rels[rid]
                break
        if target is None:
            raise ValueError(f"Sheet not found: {sheet_name}")
        if not target.startswith("worksheets/"):
            target = "worksheets/" + target.split("/")[-1]

        root = ET.fromstring(zf.read("xl/" + target))
        rows: list[list[str]] = []
        for row in root.findall(f".//{{{NS_MAIN}}}sheetData/{{{NS_MAIN}}}row"):
            values: list[str] = []
            for cell in row.findall(f"{{{NS_MAIN}}}c"):
                idx = column_number(cell.attrib.get("r", "A"))
                while len(values) <= idx:
                    values.append("")
                value_node = cell.find(f"{{{NS_MAIN}}}v")
                value = ""
                if value_node is not None:
                    value = value_node.text or ""
                    if cell.attrib.get("t") == "s":
                        value = shared_strings[int(value)]
                values[idx] = value
            rows.append(values)
        return rows


def midpoint_year(period: str) -> int | None:
    match = re.fullmatch(r"(\d{4})-(\d{2})\*?", period)
    if not match:
        return None
    start = int(match.group(1))
    end = (start // 100) * 100 + int(match.group(2))
    if end < start:
        end += 100
    return (start + end) // 2


def extract_fao_v_2_6() -> pd.DataFrame:
    rows = sheet_rows(ARCHIVED_XLSX, "V_2.6")
    # The workbook's header row omits trailing blanks if read naively; use the
    # widest row so the final 2012-14, 2013-15, and 2014-16 columns survive.
    width = max(len(row) for row in rows)
    header = rows[2] + [""] * (width - len(rows[2]))
    EXTRACTED.parent.mkdir(parents=True, exist_ok=True)
    with EXTRACTED.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows[3:]:
            padded = row + [""] * (len(header) - len(row))
            writer.writerow(padded[: len(header)])

    years = [midpoint_year(col) for col in header[2:]]
    clean_rows: list[dict[str, object]] = []
    for row in rows[3:]:
        source_entity = row[1] if len(row) > 1 else ""
        if source_entity not in SERIES:
            continue
        values = row[2:]
        for year, value in zip(years, values):
            if year is None or year < 1991 or year > 2015 or not value:
                continue
            raw_value = value.strip()
            is_censored = raw_value.startswith("<")
            numeric = float(raw_value[1:] if is_censored else raw_value)
            clean_rows.append(
                {
                    "Entity": SERIES[source_entity],
                    "Year": year,
                    "prevalence_percent": round(numeric, 2),
                    "source_entity": source_entity,
                    "source_value": raw_value,
                    "is_censored_threshold": str(is_censored).lower(),
                    "source_note": "FAO Food Security Indicators archived workbook 2016-03-17, sheet V_2.6",
                }
            )

    for year, value in [(1970, 34.75), (1980, 26.5)]:
        clean_rows.append(
            {
                "Entity": "Developing world",
                "Year": year,
                "prevalence_percent": value,
                "source_entity": "Developing countries",
                "source_value": str(value),
                "is_censored_threshold": "false",
                "source_note": "OWID/FAO long-run developing-country chart; 1970/1980 averaged from FAO SOFI 2006 and 2010 per OWID metadata",
            }
        )

    df = pd.DataFrame(clean_rows).sort_values(["Entity", "Year"])
    BOOK_CLEAN.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BOOK_CLEAN, index=False)
    # No post-2015 extension is plotted as comparable. Keep this file explicit.
    df.assign(extension_status="no comparable post-2015 extension plotted").to_csv(EXTENDED_CLEAN, index=False)
    return df


def style(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.tick_params(labelsize=9)


def plot_reconstruction(df: pd.DataFrame, out: Path, extended: bool = False) -> None:
    colors = {
        "Developing world": "0.05",
        "Sub-Saharan Africa": "0.24",
        "Southeast Asia": "0.46",
        "South Asia": "0.58",
        "East Asia": "0.70",
        "Latin America": "0.34",
    }
    labels = {
        "Developing world": (1972, 33.3),
        "Sub-Saharan Africa": (2013.2, 23.4),
        "Southeast Asia": (2000.5, 27.4),
        "South Asia": (2011.2, 18.2),
        "East Asia": (2005.3, 13.7),
        "Latin America": (2007.5, 6.0),
    }
    fig, ax = plt.subplots(figsize=(8.4, 5.2), dpi=180)
    for entity in ["Developing world", "Sub-Saharan Africa", "Southeast Asia", "South Asia", "East Asia", "Latin America"]:
        sub = df[df["Entity"].eq(entity)].sort_values("Year")
        linewidth = 3.0 if entity == "Developing world" else 2.0
        ax.plot(sub["Year"], sub["prevalence_percent"], color=colors[entity], linewidth=linewidth)
        x, y = labels[entity]
        weight = "bold" if entity == "Developing world" else "normal"
        ax.text(x, y, entity, fontsize=9, color=colors[entity], weight=weight)

    ax.set_xlim(1970, 2016)
    ax.set_ylim(0, 36)
    ax.set_xticks(list(range(1970, 2020, 5)))
    ax.set_yticks(list(range(0, 36, 5)))
    ax.set_ylabel("Percentage of people in developing countries\nwho are undernourished")
    title = "Figure 7-3: Undernourishment, 1970-2015"
    if extended:
        title += " (no comparable post-2015 extension)"
    ax.set_title(title, loc="left", fontsize=12)
    ax.text(
        0,
        -0.18,
        "Source: FAO Food Security Indicators archived workbook, sheet V_2.6; 1970/1980 developing-world values from OWID long-run FAO chart.",
        transform=ax.transAxes,
        fontsize=7,
        va="top",
    )
    style(ax)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_comparison(reconstruction: Path, comparison: Path, title: str) -> None:
    reference = FIG / "plots/comparisons/kindle_reference_figure_7_3.png"
    ref = plt.imread(reference)
    rec = plt.imread(reconstruction)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), dpi=180)
    axes[0].imshow(ref)
    axes[0].set_title("Supplemental PDF reference crop", fontsize=10)
    axes[1].imshow(rec)
    axes[1].set_title(title, fontsize=10)
    for ax in axes:
        ax.axis("off")
    fig.tight_layout()
    comparison.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(comparison, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    df = extract_fao_v_2_6()
    book_plot = FIG / "plots/book_period/figure_7_3_book_period_reconstruction.png"
    extended_plot = FIG / "plots/extended/figure_7_3_extended_reconstruction.png"
    plot_reconstruction(df, book_plot)
    plot_reconstruction(df, extended_plot, extended=True)
    plot_comparison(book_plot, FIG / "plots/comparisons/figure_7_3_book_period_comparison.png", "Archived FAO reconstruction")
    plot_comparison(extended_plot, FIG / "plots/comparisons/figure_7_3_extended_comparison.png", "No comparable extension plotted")


if __name__ == "__main__":
    main()
