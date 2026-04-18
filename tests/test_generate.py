import pytest
from datetime import date
from generate import calc_ring_offset, calc_readiness, week_date_range, fmt_tsb_color, parse_kw_plan


def test_ring_offset_full():
    assert calc_ring_offset(100, 100, 345.4) == pytest.approx(0, abs=1)


def test_ring_offset_half():
    assert calc_ring_offset(50, 100, 345.4) == pytest.approx(172.7, abs=1)


def test_ring_offset_zero():
    assert calc_ring_offset(0, 100, 345.4) == pytest.approx(345.4, abs=1)


def test_readiness_high():
    score = calc_readiness(hrv=45, hrv_7d_avg=42, sleep_secs=28800, tsb=20)
    assert score >= 80


def test_readiness_low():
    score = calc_readiness(hrv=28, hrv_7d_avg=42, sleep_secs=18000, tsb=-15)
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
