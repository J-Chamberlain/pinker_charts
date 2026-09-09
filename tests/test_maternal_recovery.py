import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from reconstruct_5_3 import load_preserved, recover_early_sweden


def test_source_recovery_adds_missing_years_without_replacing_values():
    _, old = load_preserved()
    new, audit = recover_early_sweden(old)
    assert new[:len(old)] == old
    assert len(new) == len(old) + 49
    assert {r["Year"] for r in new[len(old):]} == set(range(1751, 1800))
    assert audit["count_ratio_max_error"] < 1e-8
    assert audit["overlap_max_mmr_error"] <= .051
