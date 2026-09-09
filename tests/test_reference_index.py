from scripts.index_references import visible_caption


def test_correct_id_and_source_are_extracted_without_axes():
    status, title, source = visible_caption("100\n80\nFigure 5-3: Maternal mortality, 1751-2013\nSource: Roser 2016p", "5-3")
    assert status == "ocr_id_confirmed"
    assert title.startswith("Figure 5-3")
    assert source == "Roser 2016p"
    assert "100" not in title


def test_wrong_figure_or_two_figures_cannot_pass():
    assert visible_caption("Figure 5-2: Child mortality", "5-3")[0] == "identity_unconfirmed"
    assert visible_caption("Figure 5-3: One\nFigure 5-2: Two", "5-3")[0] == "identity_unconfirmed"


def test_em_dash_id_is_normalized():
    assert visible_caption("Figure 5\u20143: Maternal mortality", "5-3")[0] == "ocr_id_confirmed"
from PIL import Image, ImageDraw
from scripts.index_references import panel_split


def test_split_uses_white_gutter_not_midpoint():
    image = Image.new("RGB", (100, 1000), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 0, 90, 450), fill="black")
    draw.rectangle((10, 480, 90, 999), fill="black")
    assert 451 <= panel_split(image) < 480
