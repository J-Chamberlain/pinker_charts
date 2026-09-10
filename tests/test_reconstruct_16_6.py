from scripts.reconstruct_16_6 import load_data


def test_original_distinct_units_and_no_invented_endpoint():
    frame = load_data()
    assert len(frame) == 33
    assert not frame.duplicated(["series", "year"]).any()
    composite = frame[frame.series.eq("Well-Being Composite")]
    hihd = frame[frame.series.eq("Historical Index of Human Development")]
    assert composite.year.tolist() == list(range(1820, 2001, 10))
    assert composite.value.iloc[0] == -.82
    assert composite.value.iloc[-1] == .92
    assert hihd.year.max() == 2007
    assert hihd.value.iloc[0] == .076
    assert hihd.value.iloc[-1] == .460
    assert frame.unit.nunique() == 2
