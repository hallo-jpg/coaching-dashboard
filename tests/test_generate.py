import pytest
from datetime import date
from generate import calc_ring_offset, calc_readiness, week_date_range, fmt_tsb_color, parse_kw_plan, match_activities, build_day_rows
from unittest.mock import patch


MOCK_WELLNESS = [
    {"id": "2026-04-12", "hrv": 40, "sleepSecs": 25200, "ctl": 42.0, "atl": 38.0, "restingHR": 50},
    {"id": "2026-04-13", "hrv": 43, "sleepSecs": 27000, "ctl": 42.5, "atl": 37.0, "restingHR": 49},
    {"id": "2026-04-14", "hrv": 45, "sleepSecs": 28800, "ctl": 43.0, "atl": 36.0, "restingHR": 48},
]
MOCK_ACTIVITIES = []


@patch("generate.get_wellness", return_value=MOCK_WELLNESS)
@patch("generate.get_activities", return_value=MOCK_ACTIVITIES)
def test_build_context_keys(mock_act, mock_well):
    from generate import build_context
    ctx = build_context(kw=16, monday=date(2026, 4, 13), sunday=date(2026, 4, 19))
    required_keys = [
        "kw", "kw_dates", "phase_name", "readiness_score", "readiness_color",
        "ctl", "atl", "tsb_display", "ctl_offset", "atl_offset",
        "tss_ist", "tss_plan", "days", "sparkline", "outlook",
        "phases", "polar_z12_pct", "polar_z3_pct", "polar_z47_pct",
        "biometrics_pending",
    ]
    for key in required_keys:
        assert key in ctx, f"Missing key: {key}"


def test_ring_offset_full():
    assert calc_ring_offset(100, 100, 345.4) == pytest.approx(0, abs=1)


def test_ring_offset_half():
    assert calc_ring_offset(50, 100, 345.4) == pytest.approx(172.7, abs=1)


def test_ring_offset_zero():
    assert calc_ring_offset(0, 100, 345.4) == pytest.approx(345.4, abs=1)


def test_readiness_high():
    window = [
        {"id": "2026-04-10", "hrv": 42, "sleepSecs": 28800, "ctl": 45.0, "atl": 35.0, "restingHR": 48},
        {"id": "2026-04-11", "hrv": 44, "sleepSecs": 27000, "ctl": 45.5, "atl": 34.0, "restingHR": 47},
        {"id": "2026-04-12", "hrv": 45, "sleepSecs": 28800, "ctl": 46.0, "atl": 33.0, "restingHR": 47},
    ]
    score = calc_readiness(wellness_window=window, hrv_baseline=window)
    assert score >= 80


def test_readiness_low():
    window = [
        {"id": "2026-04-10", "hrv": 42, "sleepSecs": 25200, "ctl": 40.0, "atl": 55.0, "restingHR": 52},
        {"id": "2026-04-11", "hrv": 35, "sleepSecs": 18000, "ctl": 40.5, "atl": 56.0, "restingHR": 56},
        {"id": "2026-04-12", "hrv": 28, "sleepSecs": 18000, "ctl": 41.0, "atl": 57.0, "restingHR": 58},
    ]
    score = calc_readiness(wellness_window=window, hrv_baseline=window)
    assert score < 60


def test_week_date_range():
    monday, sunday = week_date_range(16, 2026)
    assert monday == date(2026, 4, 13)
    assert sunday == date(2026, 4, 19)


def test_tsb_color_positive():
    assert fmt_tsb_color(15) == "#3ecf8e"


def test_tsb_color_negative():
    assert fmt_tsb_color(-15) == "#ef4444"


def test_parse_kw_plan_days():
    plan = parse_kw_plan(16)
    assert len(plan["days"]) == 7


def test_parse_kw_plan_tss():
    plan = parse_kw_plan(16)
    assert plan["tss_plan"] == 493


def test_parse_kw_plan_monday():
    plan = parse_kw_plan(16)
    mo = plan["days"][0]
    assert mo["tag"] == "Mo"
    assert mo["workout"] == "LIT-2h"
    assert mo["tss_plan"] == 74


def test_parse_kw_plan_rest_day():
    plan = parse_kw_plan(16)
    mi = plan["days"][2]
    assert mi["tag"] == "Mi"
    assert mi["rest"] is True


def test_parse_kw_plan_theme():
    plan = parse_kw_plan(16)
    assert "Grundlagen" in plan["theme"]


SAMPLE_ACTIVITIES = [
    {"start_date_local": "2026-04-13T09:00:00", "type": "Ride",
     "icu_training_load": 71, "name": "Morgenfahrt"},
    {"start_date_local": "2026-04-16T18:00:00", "type": "Run",
     "icu_training_load": 48, "name": "Lauf"},
]
SAMPLE_PLAN_DAYS = [
    {"tag": "Mo", "workout": "LIT-2h", "tss_plan": 74, "status": "❌",
     "rest": False, "is_run": False},
    {"tag": "Di", "workout": "SwSp 3×10", "tss_plan": 72, "status": "❌",
     "rest": False, "is_run": False},
    {"tag": "Mi", "workout": "Ruhetag", "tss_plan": 0, "status": "–",
     "rest": True, "is_run": False},
    {"tag": "Do", "workout": "Lauf 2×8min", "tss_plan": 50, "status": "❌",
     "rest": False, "is_run": True},
]


def test_match_activities_monday():
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    assert matched["Mo"]["tss_ist"] == 71
    assert matched["Mo"]["done"] is True


def test_match_activities_run():
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    assert matched["Do"]["tss_ist"] == 48
    assert matched["Do"]["done"] is True


def test_match_activities_no_activity():
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    assert matched["Di"]["done"] is False
    assert matched["Di"]["tss_ist"] == 0


def test_build_day_rows():
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    rows = build_day_rows(SAMPLE_PLAN_DAYS, matched)
    mo = rows[0]
    assert mo["tag"] == "Mo"
    assert mo["tss_ist"] == 71
    assert mo["done"] is True
    assert mo["rest"] is False


from generate import _classify_day_type, _protein_dist, get_nutrition_context


def test_classify_day_type_intense():
    day = {"workout": "SwSp 3×10", "tss_plan": 72, "rest": False}
    assert _classify_day_type(day, sick=False) == "intense"


def test_classify_day_type_endurance_long():
    day = {"workout": "LIT-3h", "tss_plan": 111, "rest": False}
    assert _classify_day_type(day, sick=False) == "endurance_long"


def test_classify_day_type_rest():
    day = {"workout": "–", "tss_plan": 0, "rest": True}
    assert _classify_day_type(day, sick=False) == "rest"


def test_classify_day_type_sick():
    day = {"workout": "LIT-2h", "tss_plan": 74, "rest": False}
    assert _classify_day_type(day, sick=True) == "sick"


def test_protein_dist_sums_correctly():
    dist = _protein_dist(180)
    import re
    total = sum(int(re.search(r"\d+", s).group()) for s in dist)
    assert abs(total - 180) <= 20


@patch("generate.get_wellness", return_value=MOCK_WELLNESS)
@patch("generate.get_activities", return_value=MOCK_ACTIVITIES)
@patch("generate.get_power_bests", return_value=[])
def test_build_context_has_nutrition(mock_pb, mock_act, mock_well):
    from generate import build_context
    ctx = build_context(kw=16, monday=date(2026, 4, 13), sunday=date(2026, 4, 19))
    assert "nutrition" in ctx
    n = ctx["nutrition"]
    assert "day_type" in n
    assert "protein_g" in n
    assert isinstance(n["protein_g"], int)
    assert n["protein_g"] > 0
    assert "tips" in n
    assert len(n["tips"]) == 2


MOCK_WELLNESS_NO_HRV = [
    {"id": "2026-04-12", "hrv": None, "sleepSecs": None, "ctl": 42.0, "atl": 38.0, "restingHR": None},
    {"id": "2026-04-13", "hrv": None, "sleepSecs": None, "ctl": 42.5, "atl": 37.0, "restingHR": None},
    {"id": "2026-04-14", "hrv": None, "sleepSecs": None, "ctl": 43.0, "atl": 36.0, "restingHR": None},
]


@patch("generate.get_wellness", return_value=MOCK_WELLNESS_NO_HRV)
@patch("generate.get_activities", return_value=MOCK_ACTIVITIES)
@patch("generate.get_power_bests", return_value=[])
def test_build_context_biometrics_pending(mock_pb, mock_act, mock_well):
    from generate import build_context
    ctx = build_context(kw=16, monday=date(2026, 4, 13), sunday=date(2026, 4, 19))
    assert ctx["biometrics_pending"] is True
    assert ctx["readiness_score"] == 0
