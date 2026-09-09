"""Build a source-evidence panel without extracting or reconstructing data."""
from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "4-1"
OUT = FIG / "plots" / "comparisons" / "figure_4_1_source_evidence.png"


def font(size: int):
    for candidate in ("/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def main() -> None:
    paths = [
        FIG / "data" / "candidates" / "leetaru_2011_figure10_nyt.png",
        FIG / "data" / "candidates" / "leetaru_2011_figure11_swb.png",
    ]
    images = [Image.open(path).convert("RGB") for path in paths]
    width = 1800
    margin = 70
    chart_width = width - 2 * margin
    resized = []
    for image in images:
        height = round(image.height * chart_width / image.width)
        resized.append(image.resize((chart_width, height), Image.Resampling.LANCZOS))
    title_h, label_h, gap, footer_h = 125, 55, 55, 145
    height = title_h + sum(image.height + label_h for image in resized) + gap + footer_h
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, 35), "Figure 4-1 source evidence (not a reconstruction)", fill="#111111", font=font(40))
    y = title_h
    labels = [
        "Leetaru 2011, Figure 10: New York Times monthly tone, 1945-2005",
        "Leetaru 2011, Figure 11: Summary of World Broadcasts monthly tone, 1979-July 2010",
    ]
    for label, image in zip(labels, resized):
        draw.text((margin, y), label, fill="#222222", font=font(26))
        y += label_h
        canvas.paste(image, (margin, y))
        y += image.height
    y += gap
    footer = (
        "Pinker combined these two published source series on a -3 to 3 axis labeled 1945-2010. "
        "The monthly values were not published; pixels were not converted into data, and no successor extension is shown."
    )
    footer = "\n".join(textwrap.wrap(footer, width=112))
    draw.multiline_text((margin, y), footer, fill="#333333", font=font(25), spacing=8)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT, optimize=True)


if __name__ == "__main__":
    main()
