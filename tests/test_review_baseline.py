import importlib.util
from pathlib import Path
import sys

from PIL import Image
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_review_baseline import eligible, render_comparison, trimmed


def test_source_only_never_in_gallery():
    assert not eligible({"artifact_kind": "source_recovery", "artifacts": {"book_period_reconstruction": {}}})


def test_blank_reference_rejected(tmp_path):
    path = tmp_path / "blank.png"
    Image.new("RGB", (100, 100), "white").save(path)
    with pytest.raises(ValueError, match="Blank"):
        trimmed(path)


def test_comparison_preserves_real_pixels(tmp_path):
    ref, plot, out = (tmp_path / n for n in ["original.png", "plot.png", "comparison.png"])
    Image.new("RGB", (500, 300), "red").save(ref)
    Image.new("RGB", (500, 300), "blue").save(plot)
    render_comparison(ref, plot, out, "Figure test", "Reconstructed", "Not reviewed")
    image = Image.open(out)
    assert image.getpixel((600, 400)) == (255, 0, 0)
    assert image.getpixel((1800, 400)) == (0, 0, 255)
