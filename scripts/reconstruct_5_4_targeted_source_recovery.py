from __future__ import annotations

import csv
import subprocess
from datetime import date
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "5-4"
RAW = FIG / "data" / "raw"
CLEAN = FIG / "data" / "clean"
PLOTS = FIG / "plots"
TMP = ROOT / "tmp" / "pdfs"
TODAY = date.today().isoformat()

BOOK_SOURCE_NOTE = (
    "Our World in Data, Roser 2016n. Data before 1845 are for England and Wales "
    "and come from OECD Clio Infra, van Zanden et al. 2014. Data from 1845 on "
    "are for mid-decade years only, and come from the Human Mortality Database."
)


def ensure_dirs() -> None:
    for path in [
        RAW,
        CLEAN,
        PLOTS / "book_period",
        PLOTS / "extended",
        PLOTS / "comparisons",
        PLOTS / "diagnostics",
        FIG / "source_logs",
        FIG / "search_iterations",
        FIG / "discrepancy_logs",
        FIG / "anomaly_reviews",
        FIG / "provenance",
        FIG / "captions",
        FIG / "metadata",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def download(url: str, dest: Path) -> tuple[str, str]:
    req = Request(url, headers={"User-Agent": "pinker-figure-5-4-source-recovery/1.0"})
    try:
        with urlopen(req, timeout=45) as response:
            data = response.read()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            return "downloaded", f"{response.status} {response.headers.get('Content-Type', '')}"
    except URLError as exc:
        return "failed", str(exc)


def render_pdf_reference() -> Path:
    TMP.mkdir(parents=True, exist_ok=True)
    prefix = TMP / "fig5_4_supplemental_page"
    subprocess.run(
        [
            "pdftoppm",
            "-f",
            "4",
            "-l",
            "4",
            "-r",
            "200",
            "-png",
            str(ROOT / "references/enlightenment_now_supplemental_graphics.pdf"),
            str(prefix),
        ],
        check=True,
    )
    page = TMP / "fig5_4_supplemental_page-04.png"
    out = PLOTS / "comparisons" / "supplemental_pdf_reference_figure_5_4.png"
    # Crop includes the full figure, title, and source note from Supplemental PDF page 4.
    Image.open(page).convert("RGB").crop((120, 170, 1110, 980)).save(out)
    return out


def trim(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, "white")
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    return im.crop(bbox) if bbox else im


def side_by_side(reference: Path, recreated: Path, output: Path, title: str) -> None:
    ref = trim(reference)
    rec = trim(recreated)
    panel_w, panel_h = 980, 700
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

    draw.text((canvas.width // 2, 18), title, fill="black", anchor="ma", font=title_font)
    left_x = margin
    right_x = margin + panel_w + gap
    label_y = title_h + 8
    draw.text((left_x + panel_w // 2, label_y), "Supplemental PDF reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, label_y), "Current artifact", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def build_partial_book_period() -> pd.DataFrame:
    birth = pd.read_csv(RAW / "owid_life_expectancy_riley_clio_un_2019.csv")
    age = pd.read_csv(RAW / "owid_hmd_age_specific_life_expectancy_partial.csv")

    uk_birth = birth[birth["Entity"].eq("United Kingdom") & birth["Year"].between(1701, 1844)][
        ["Year", "Life expectancy"]
    ].copy()
    uk_birth["series"] = "At birth"
    uk_birth = uk_birth.rename(columns={"Life expectancy": "life_expectancy"})

    uk_age = age[age["Entity"].eq("United Kingdom")].copy()
    birth_hmd = uk_age[
        [
            "Year",
            "Male life expectancy at birth (HMD (2018) and others)",
            "Female life expectancy at birth (HMD (2018) and others)",
        ]
    ].copy()
    birth_hmd["life_expectancy"] = birth_hmd[
        [
            "Male life expectancy at birth (HMD (2018) and others)",
            "Female life expectancy at birth (HMD (2018) and others)",
        ]
    ].mean(axis=1)
    birth_hmd["series"] = "At birth"
    rows = []
    for label, male_col, female_col in [
        (
            "For a 15-year-old",
            "Male life expectancy at 15 (HMD (2018) and others)",
            "Female life expectancy at 15 (HMD (2018) and others)",
        ),
        (
            "For a 45-year-old",
            "Male life expectancy at 45 (HMD (2018) and others)",
            "Female life expectancy at 45 (HMD (2018) and others)",
        ),
    ]:
        tmp = uk_age[["Year", male_col, female_col]].copy()
        tmp["life_expectancy"] = tmp[[male_col, female_col]].mean(axis=1)
        tmp["series"] = label
        rows.append(tmp[["Year", "life_expectancy", "series"]])

    book = pd.concat([uk_birth[["Year", "life_expectancy", "series"]], birth_hmd[["Year", "life_expectancy", "series"]], *rows], ignore_index=True)
    book = book[book["Year"].between(1701, 2013)].copy()
    book.to_csv(CLEAN / "figure_5_4_book_period_clean.csv", index=False)
    book.to_csv(CLEAN / "figure_5_4_extended_clean.csv", index=False)
    return book


def plot_partial(book: pd.DataFrame, out: Path, title_suffix: str) -> None:
    fig, ax = plt.subplots(figsize=(8.3, 5.1), dpi=180)
    colors = {"At birth": "black", "For a 15-year-old": "0.45", "For a 45-year-old": "0.7"}
    label_positions = {
        "For a 45-year-old": (1982, 84.0),
        "For a 15-year-old": (1982, 81.8),
        "At birth": (1982, 79.6),
    }
    for series in ["For a 45-year-old", "For a 15-year-old", "At birth"]:
        sub = book[book["series"].eq(series)].sort_values("Year")
        if sub.empty:
            continue
        ax.plot(sub["Year"], sub["life_expectancy"], color=colors[series], linewidth=2.3)
        lx, ly = label_positions[series]
        ax.text(lx, ly, series, fontsize=8, color=colors[series])
    ax.set_xlim(1700, 2020)
    ax.set_ylim(25, 88)
    ax.set_xticks([1701, 1720, 1740, 1760, 1780, 1800, 1820, 1840, 1860, 1880, 1900, 1920, 1940, 1960, 1980, 2000, 2020])
    ax.set_yticks([25, 35, 45, 55, 65, 75, 85])
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.set_ylabel("Life expectancy")
    ax.set_title(f"Figure 5-4: Life expectancy, UK, 1701-2013{title_suffix}", loc="left", fontsize=12)
    ax.text(
        0,
        -0.23,
        "Partial artifact only: recovered local OWID/HMD file exposes birth, age 15, and age 45; "
        "book requires birth, 1, 5, 10, 20, 30, 40, 50, 60, and 70.",
        transform=ax.transAxes,
        fontsize=7,
    )
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_audit_files() -> None:
    current_csv = RAW / "owid_current_life_expectancy_at_different_ages.csv"
    current_meta = RAW / "owid_current_life_expectancy_at_different_ages.metadata.json"
    current_config = RAW / "owid_current_life_expectancy_at_different_ages.config.json"
    downloads = [
        (
            "OWID current life-expectancy-at-different-ages CSV",
            "https://ourworldindata.org/grapher/life-expectancy-at-different-ages.csv",
            current_csv,
        ),
        (
            "OWID current life-expectancy-at-different-ages metadata",
            "https://ourworldindata.org/grapher/life-expectancy-at-different-ages.metadata.json",
            current_meta,
        ),
        (
            "OWID current life-expectancy-at-different-ages config",
            "https://ourworldindata.org/grapher/life-expectancy-at-different-ages.config.json",
            current_config,
        ),
        (
            "HMD England & Wales public country page",
            "https://www.mortality.org/Country/Country?cntr=GBRTENW",
            RAW / "hmd_gbrtenw_country_page.html",
        ),
        (
            "HMD England & Wales background documentation",
            "https://www.mortality.org/File/GetDocument/hmd.v6/GBRTENW/Public/InputDB/GBRTENWcom.pdf",
            RAW / "hmd_gbrtenw_background_documentation.pdf",
        ),
        (
            "HMD country codes",
            "https://www.mortality.org/File/GetDocument/Public/country_codes.csv",
            RAW / "hmd_country_codes.csv",
        ),
    ]

    audit_rows = []
    for label, url, dest in downloads:
        status, detail = download(url, dest)
        audit_rows.append({"item": label, "url": url, "status": status, "detail": detail, "stored_file": str(dest.relative_to(ROOT))})

    # Probe raw HMD data endpoint without storing login HTML as if it were data.
    probe_url = "https://www.mortality.org/File/GetDocument/hmd.v6/GBRTENW/STATS/bltper_1x1.txt"
    req = Request(probe_url, headers={"User-Agent": "pinker-figure-5-4-source-recovery/1.0"})
    try:
        with urlopen(req, timeout=45) as response:
            body = response.read(200)
            detail = f"{response.status} {response.geturl()} {response.headers.get('Content-Type', '')}; first bytes={body[:30]!r}"
            status = "unexpected_public_response"
    except Exception as exc:  # noqa: BLE001 - audit should record the exact blocker.
        status = "failed"
        detail = str(exc)
    audit_rows.append({"item": "HMD both-sex period life table 1x1 raw data probe", "url": probe_url, "status": status, "detail": detail, "stored_file": ""})

    with (CLEAN / "figure_5_4_source_recovery_audit.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["item", "url", "status", "detail", "stored_file"])
        writer.writeheader()
        writer.writerows(audit_rows)

    successor = pd.read_csv(current_csv)
    uk = successor[successor["Entity"].eq("United Kingdom")].copy()
    available = []
    for col in ["at birth", "10 year old", "25 year old", "45 year old", "65 year old", "80 year old"]:
        values = uk[["Year", col]].dropna()
        available.append(
            {
                "series": col,
                "first_year": int(values["Year"].min()) if not values.empty else "",
                "last_year": int(values["Year"].max()) if not values.empty else "",
                "book_required_exact_age": col in {"at birth", "10 year old"},
                "accepted_for_book_reconstruction": col in {"at birth"},
                "note": "Current OWID successor omits several book ages and uses UN WPP after 1950.",
            }
        )
    pd.DataFrame(available).to_csv(CLEAN / "figure_5_4_current_owid_successor_availability.csv", index=False)


def main() -> None:
    ensure_dirs()
    reference = render_pdf_reference()
    write_audit_files()
    book = build_partial_book_period()

    book_plot = PLOTS / "book_period" / "figure_5_4_book_period_reconstruction.png"
    ext_plot = PLOTS / "extended" / "figure_5_4_extended_reconstruction.png"
    plot_partial(book, book_plot, " (partial source-recovery artifact)")
    plot_partial(book, ext_plot, " (no accepted extension)")
    side_by_side(reference, book_plot, PLOTS / "comparisons" / "figure_5_4_book_period_comparison.png", "Figure 5-4 book-period comparison")
    side_by_side(reference, ext_plot, PLOTS / "comparisons" / "figure_5_4_extended_comparison.png", "Figure 5-4 extended/status comparison")

    (FIG / "captions" / "caption.txt").write_text(
        "Figure 5-4: Life expectancy, UK, 1701-2013. Source note: "
        f"{BOOK_SOURCE_NOTE} Status after targeted recovery on {TODAY}: "
        "source chain is documented, but the exact OWID/Roser 2016n book-era age-specific "
        "dataset was not recovered. The current artifact remains partial because it contains "
        "only at-birth, age-15, and age-45 series; the printed figure requires at-birth and "
        "ages 1, 5, 10, 20, 30, 40, 50, 60, and 70. No successor extension is plotted because "
        "the current public OWID successor omits several required ages and switches to UN WPP "
        "after 1950.\n"
    )


if __name__ == "__main__":
    main()
