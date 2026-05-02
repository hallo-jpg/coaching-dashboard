import pytest
from datetime import date
from generate import calc_ring_offset, calc_readiness, week_date_range, fmt_tsb_color, parse_kw_plan, match_activities, build_day_rows, _calc_polarisation
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


def test_parse_kw_plan_archiv_fallback(tmp_path, monkeypatch):
    # Simulate: primary planung/kw99.md missing, but planung/archiv/kw99.md exists
    archiv_dir = tmp_path / "planung" / "archiv"
    archiv_dir.mkdir(parents=True)
    (tmp_path / "planung" / "archiv" / "kw99.md").write_text(
        "# KW99 – Archiviert\n\n*Thema: Test*\n\n"
        "## Wochenplan\n\n"
        "| Tag | Workout | TSS ca. | TSS Ist | Status | Notiz |\n"
        "|---|---|---|---|---|---|\n"
        "| Mo | LIT-2h | 74 | – | ⬜ | |\n"
        "| Di | Ruhetag | – | – | ⬜ | |\n"
        "| Mi | Ruhetag | – | – | ⬜ | |\n"
        "| Do | Ruhetag | – | – | ⬜ | |\n"
        "| Fr | Ruhetag | – | – | ⬜ | |\n"
        "| Sa | LIT-2h | 74 | – | ⬜ | |\n"
        "| So | LIT-2h | 74 | – | ⬜ | |\n"
        "| **Total** | | **~222** | | | |\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    plan = parse_kw_plan(99)
    assert len(plan["days"]) == 7, "Archiv-Fallback muss 7 Tage liefern"
    assert plan["tss_plan"] > 0, "Archiv-Fallback muss TSS liefern"
    assert plan["theme"] != "KW99", "Archiv-Fallback muss Theme aus Datei lesen"


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


# ---------------------------------------------------------------------------
# _calc_polarisation – Sentiero/intervals.icu zone mapping
# Sentiero Z0-Z6 = intervals.icu Z1-Z7 (offset +1)
# LIT = icu Z1+Z2+Z3, Grauzone = icu Z4, HIT = icu Z5+Z6+Z7
# ---------------------------------------------------------------------------

def _make_activities_with_zones(zone_secs: dict) -> list:
    """Return a mock activity list that _calc_polarisation can process via _api_get patch."""
    return [{"id": "act1", "type": "Ride"}]


def _zone_times(zone_secs: dict) -> list:
    """Build icu_zone_times structure from {zone_num: secs} dict."""
    return [{"id": f"Z{z}", "secs": s} for z, s in zone_secs.items()]


@patch("generate._api_get")
def test_calc_polarisation_lit_includes_z3(mock_api):
    # 600s in Z1, 600s in Z2, 600s in Z3 (all LIT), 0 Grauzone, 0 HIT
    mock_api.return_value = {"icu_zone_times": _zone_times({1: 600, 2: 600, 3: 600})}
    acts = [{"id": "act1", "type": "Ride"}]
    result = _calc_polarisation(acts)
    assert result["z12"] == 100, f"LIT should be 100%, got {result['z12']}"
    assert result["z3"] == 0,   "Grauzone should be 0%"
    assert result["z47"] == 0,  "HIT should be 0%"
    assert result["ok"] is True


@patch("generate._api_get")
def test_calc_polarisation_grauzone_is_z4_not_z3(mock_api):
    # 600s LIT (Z1), 0 Z2, 0 Z3, 400s Z4 (Grauzone), 0 HIT
    mock_api.return_value = {"icu_zone_times": _zone_times({1: 600, 4: 400})}
    acts = [{"id": "act1", "type": "Ride"}]
    result = _calc_polarisation(acts)
    total = 1000
    assert result["z12"] == round(600 / total * 100), "LIT wrong"
    assert result["z3"]  == round(400 / total * 100), "Grauzone should be Z4 time"
    assert result["z47"] == 0, "HIT should be 0"


@patch("generate._api_get")
def test_calc_polarisation_hit_is_z5_z6_z7(mock_api):
    # 300s each in Z5, Z6, Z7 = HIT; 300s Z1 = LIT
    mock_api.return_value = {"icu_zone_times": _zone_times({1: 300, 5: 300, 6: 300, 7: 300})}
    acts = [{"id": "act1", "type": "Ride"}]
    result = _calc_polarisation(acts)
    total = 1200
    assert result["z12"] == round(300 / total * 100), "LIT wrong"
    assert result["z3"]  == 0,                        "Grauzone should be 0"
    assert result["z47"] == round(900 / total * 100), "HIT should be Z5+Z6+Z7"


@patch("generate._api_get")
def test_calc_polarisation_ok_flag_triggers_on_z4(mock_api):
    # Z4 = 20% → should fail ok check (>15%)
    mock_api.return_value = {"icu_zone_times": _zone_times({1: 800, 4: 200})}
    acts = [{"id": "act1", "type": "Ride"}]
    result = _calc_polarisation(acts)
    assert result["ok"] is False, "ok should be False when Z4 (Grauzone) > 15%"


# ── Bonus-Aktivitäten ────────────────────────────────────────────────────────

SAMPLE_ACTIVITIES_WITH_BONUS = [
    # Wandern früh (Hike = nicht im SPORT_TYPE_MAP → immer Bonus)
    {"start_date_local": "2026-04-13T07:00:00", "type": "Hike",
     "icu_training_load": 32, "name": "Morgenwanderung"},
    # Rad am Nachmittag → primär (passt zu Plan-Typ ride)
    {"start_date_local": "2026-04-13T15:00:00", "type": "Ride",
     "icu_training_load": 88, "name": "HIT 4×8min"},
    # Wandern an Ruhetag (Mi)
    {"start_date_local": "2026-04-15T10:00:00", "type": "Hike",
     "icu_training_load": 25, "name": "Wandern Ruhetag"},
]


def test_match_activities_bonus_ride_day():
    """Hike früh + Ride nachmittags → Ride ist primär, Hike ist Bonus."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES_WITH_BONUS, SAMPLE_PLAN_DAYS, monday)
    mo = matched["Mo"]
    assert mo["primary"] is not None
    assert mo["primary"]["name"] == "HIT 4×8min"
    assert mo["primary"]["tss"] == 88
    assert len(mo["bonus"]) == 1
    assert mo["bonus"][0]["name"] == "Morgenwanderung"
    assert mo["bonus"][0]["tss"] == 32
    assert mo["tss_ist"] == 120
    assert mo["done"] is True


def test_match_activities_bonus_rest_day():
    """Aktivität an Ruhetag → alles Bonus, done bleibt False."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES_WITH_BONUS, SAMPLE_PLAN_DAYS, monday)
    mi = matched["Mi"]
    assert mi["primary"] is None
    assert len(mi["bonus"]) == 1
    assert mi["bonus"][0]["name"] == "Wandern Ruhetag"
    assert mi["tss_ist"] == 25
    assert mi["done"] is False


def test_match_activities_primary_structure():
    """Rückgabe enthält primary/bonus/tss_ist/done für alle Tage."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    for tag in ["Mo", "Di", "Mi", "Do"]:
        assert "primary" in matched[tag]
        assert "bonus" in matched[tag]
        assert "tss_ist" in matched[tag]
        assert "done" in matched[tag]


def test_match_activities_existing_compatibility():
    """Bestehende Tests-Felder (tss_ist, done) bleiben korrekt."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    assert matched["Mo"]["tss_ist"] == 71
    assert matched["Mo"]["done"] is True
    assert matched["Do"]["tss_ist"] == 48
    assert matched["Do"]["done"] is True
    assert matched["Di"]["done"] is False
    assert matched["Di"]["tss_ist"] == 0


def test_build_day_rows_bonus_fields_present():
    """build_day_rows liefert bonus_activities, tss_primary, tss_bonus."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    rows = build_day_rows(SAMPLE_PLAN_DAYS, matched)
    mo = rows[0]
    assert "bonus_activities" in mo
    assert "tss_primary" in mo
    assert "tss_bonus" in mo
    assert mo["bonus_activities"] == []
    assert mo["tss_primary"] == 71
    assert mo["tss_bonus"] == 0


def test_build_day_rows_bonus_ride_day():
    """Bei Bonus-Aktivität korrekte Felder im Row-Dict."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES_WITH_BONUS, SAMPLE_PLAN_DAYS, monday)
    rows = build_day_rows(SAMPLE_PLAN_DAYS, matched)
    mo = rows[0]  # Mo: Ride primär (88 TSS) + Hike Bonus (32 TSS)
    assert mo["tss_ist"] == 120
    assert mo["tss_primary"] == 88
    assert mo["tss_bonus"] == 32
    assert len(mo["bonus_activities"]) == 1
    assert mo["bonus_activities"][0]["name"] == "Morgenwanderung"
    assert mo["done"] is True


def test_build_day_rows_bonus_rest_day():
    """An Ruhetag mit Aktivität: done=False, bonus_activities gefüllt."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES_WITH_BONUS, SAMPLE_PLAN_DAYS, monday)
    rows = build_day_rows(SAMPLE_PLAN_DAYS, matched)
    mi = rows[2]  # Mi ist Ruhetag
    assert mi["rest"] is True
    assert mi["done"] is False
    assert len(mi["bonus_activities"]) == 1
    assert mi["tss_bonus"] == 25
    assert mi["tss_primary"] == 0
