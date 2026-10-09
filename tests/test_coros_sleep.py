import json
from pathlib import Path

from coros_sleep import _read, merge, parse_hrv, parse_overview
from generate import apply_coros_sleep, coros_sleep_summary

FIX = Path(__file__).parent / "fixtures"


def _parsed():
    overview = parse_overview(_read(FIX / "coros_sleep_overview.txt"))
    hrv_days, points = parse_hrv(_read(FIX / "coros_sleep_hrv.txt"))
    return overview, hrv_days, points


def test_parse_overview_json_string():
    overview, _, _ = _parsed()
    n = overview["2026-10-08"]
    assert n["asleep_min"] == 437 and n["in_bed_min"] == 454
    assert (n["deep_pct"], n["rem_pct"], n["awake_min"], n["score"]) == (19, 25, 17, 79)
    assert n["bed"] == "2026-10-07T23:23" and n["wake"] == "2026-10-08T06:57"


def test_parse_hrv_assessment_and_series():
    _, hrv_days, points = _parsed()
    assert hrv_days["2026-10-08"] == {"hrv": 44, "hrv_status": "Below normal",
                                      "hrv_low": 47, "hrv_high": 57, "hrv_baseline": 52}
    assert len(points) > 40


def test_merge_detects_early_night_dip():
    store = merge({}, *_parsed())
    n = store["nights"]["2026-10-08"]
    assert n["hrv_early"] < n["hrv_late"] - 8
    assert "hrv_early" not in store["nights"]["2026-10-09"]   # keine Kurve für diese Nacht


def test_merge_keeps_existing_nights():
    store = {"nights": {"2026-10-07": {"score": 89, "hrv_early": 35, "hrv_late": 50}}}
    merge(store, *_parsed())
    assert store["nights"]["2026-10-07"]["hrv_early"] == 35
    assert store["nights"]["2026-10-07"]["hrv"] == 44


def test_apply_overrides_sleep_and_fills_missing_hrv():
    nights = merge({}, *_parsed())["nights"]
    wellness = [{"id": "2026-10-08", "sleepSecs": 27360, "hrv": 44},
                {"id": "2026-10-09", "sleepSecs": None, "hrv": None},
                {"id": "2026-10-10", "sleepSecs": 30000, "hrv": 50}]
    apply_coros_sleep(wellness, nights)
    assert wellness[0]["sleepSecs"] == 437 * 60
    assert wellness[1]["hrv"] == 49
    assert wellness[2] == {"id": "2026-10-10", "sleepSecs": 30000, "hrv": 50}   # Fallback icu


def test_summary_hint():
    nights = merge({}, *_parsed())["nights"]
    s = coros_sleep_summary(nights["2026-10-08"])
    assert "Tief 19 %" in s["detail"] and s["hint"]
    assert coros_sleep_summary(nights["2026-10-09"])["hint"] is None
    assert coros_sleep_summary(None) is None
