import json
from pathlib import Path

from coros_wellness import _read, merge, parse_daily, parse_hrv, parse_overview, parse_rhr
from generate import apply_coros, coros_sleep_summary, sync_status

FIX = Path(__file__).parent / "fixtures"


def _parsed():
    overview = parse_overview(_read(FIX / "coros_sleep_overview.txt"))
    hrv_days, points = parse_hrv(_read(FIX / "coros_sleep_hrv.txt"))
    rhr = parse_rhr(_read(FIX / "coros_rhr.txt"))
    daily = parse_daily(_read(FIX / "coros_daily.txt"))
    return overview, hrv_days, points, rhr, daily


def test_parse_overview_json_string():
    overview = _parsed()[0]
    n = overview["2026-10-08"]
    assert n["asleep_min"] == 437 and n["in_bed_min"] == 454
    assert (n["deep_pct"], n["rem_pct"], n["awake_min"], n["score"]) == (19, 25, 17, 79)
    assert n["bed"] == "2026-10-07T23:23" and n["wake"] == "2026-10-08T06:57"


def test_parse_hrv_assessment_and_series():
    _, hrv_days, points, _, _ = _parsed()
    assert hrv_days["2026-10-08"] == {"hrv": 44, "hrv_status": "Below normal",
                                      "hrv_low": 47, "hrv_high": 57, "hrv_baseline": 52}
    assert len(points) > 40


def test_merge_detects_early_night_dip():
    store = merge({}, *_parsed())
    n = store["days"]["2026-10-08"]
    assert n["hrv_early"] < n["hrv_late"] - 8
    assert "hrv_early" not in store["days"]["2026-10-09"]   # keine Kurve für diese Nacht


def test_merge_keeps_existing_nights():
    store = {"days": {"2026-10-07": {"score": 89, "hrv_early": 35, "hrv_late": 50}}}
    merge(store, *_parsed())
    assert store["days"]["2026-10-07"]["hrv_early"] == 35
    assert store["days"]["2026-10-07"]["hrv"] == 44


def test_parse_rhr_and_daily():
    *_, rhr, daily = _parsed()
    assert rhr["2026-10-09"] == {"rhr": 58} and len(rhr) == 7
    assert daily["2026-10-08"] == {"steps": 19124, "stress_avg": 31, "sleep_hr_avg": 57, "sleep_hr_min": 43}


def test_apply_takes_watch_data_from_coros():
    days = merge({}, *_parsed())["days"]
    wellness = [{"id": "2026-10-08", "sleepSecs": 27360, "hrv": 40, "restingHR": 50, "steps": 20000,
                 "weight": 93.6, "fatigue": 2},
                {"id": "2026-10-09", "sleepSecs": None, "hrv": None, "restingHR": None, "steps": None},
                {"id": "2026-10-10", "sleepSecs": 30000, "hrv": 50}]
    apply_coros(wellness, days)
    w = wellness[0]
    assert (w["sleepSecs"], w["hrv"], w["restingHR"]) == (437 * 60, 44, 57)
    assert w["steps"] == 20000                                   # höherer Wert gewinnt
    assert (w["weight"], w["fatigue"]) == (93.6, 2)              # Gewicht & Gefühl bleiben icu
    assert (wellness[1]["hrv"], wellness[1]["restingHR"], wellness[1]["steps"]) == (49, 58, 70)
    assert (wellness[2]["sleepSecs"], wellness[2]["hrv"]) == (30000, 50)   # Fallback icu
    assert "coros" not in wellness[2]


def test_summary_hint():
    nights = merge({}, *_parsed())["days"]
    s = coros_sleep_summary(nights["2026-10-08"])
    assert "Tief 19 %" in s["detail"] and s["hint"]
    assert coros_sleep_summary(nights["2026-10-09"])["hint"] is None
    assert coros_sleep_summary(None) is None


def test_sync_status_chips():
    days = merge({}, *_parsed())["days"]
    rows = [{"id": "2026-10-09", "hrv": None},
            {"id": "2026-10-08", "hrv": 44},
            {"id": "2026-10-07", "hrv": None, "fatigue": 1}]
    apply_coros(rows, days)
    assert sync_status(rows[0]) == {"coros": True, "icu": False}   # icu hatte noch nichts
    assert sync_status(rows[1]) == {"coros": True, "icu": True}
    assert sync_status(rows[2])["icu"] is True                      # Gefühl zählt als intervals
    assert sync_status(None) == {"coros": False, "icu": False}
