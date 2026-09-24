import pytest
from datetime import date, timedelta
from generate import calc_ring_offset, calc_readiness, week_date_range, fmt_tsb_color, parse_kw_plan, match_activities, build_day_rows, _calc_polarisation, calc_monotony_strain, calc_ramprate, project_pmc, calc_subjective
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
        "phases", "polar_z12_pct", "polar_z3_pct", "polar_z5_pct", "polar_z67_pct",
        "biometrics_pending",
        "monotony_val", "monotony_strain", "monotony_color",
        "ramprate", "ramprate_color",
        "countdown_main", "countdown_secondary",
    ]
    for key in required_keys:
        assert key in ctx, f"Missing key: {key}"


def test_ring_offset_full():
    assert calc_ring_offset(100, 100, 345.4) == pytest.approx(0, abs=1)


def test_ring_offset_half():
    assert calc_ring_offset(50, 100, 345.4) == pytest.approx(172.7, abs=1)


def test_ring_offset_zero():
    assert calc_ring_offset(0, 100, 345.4) == pytest.approx(345.4, abs=1)


def _hist(days=20, hrv=50, rhr=55, sleep_h=8.0):
    return [{"id": f"2026-04-{i+1:02d}", "hrv": hrv + (-6, -3, 0, 3, 6)[i % 5], "restingHR": rhr + (i % 3) - 1,
             "sleepSecs": int(sleep_h * 3600)} for i in range(days)]


def test_readiness_high():
    hist = _hist()
    hist[-1].update(hrv=55, restingHR=53)
    assert calc_readiness(hist) >= 80


def test_readiness_low_trend():
    """Mehrere Tage HRV unten + Puls oben + wenig Schlaf → rot."""
    hist = _hist()
    for w in hist[-5:]:
        w.update(hrv=44, restingHR=59, sleepSecs=6 * 3600)
    assert calc_readiness(hist) < 60


def test_readiness_single_outlier_is_smoothed():
    """Ein einzelner mäßig schwacher Tag kippt nicht sofort auf rot."""
    hist = _hist()
    hist[-1].update(hrv=46, restingHR=57)
    assert calc_readiness(hist) >= 60


def test_readiness_extreme_outlier_flags_red():
    """HRV-Absturz / Ruhepuls-Sprung erzwingt rot, auch wenn der Rest gut ist."""
    hist = _hist()
    hist[-1].update(hrv=24, restingHR=67)
    assert calc_readiness(hist) < 50


def test_readiness_ignores_tsb():
    """TSB ist kein Readiness-Signal: tiefer TSB bei guten Körperwerten bleibt grün."""
    hist = _hist()
    for w in hist:
        w.update(ctl=24.0, atl=40.0)
    assert calc_readiness(hist) >= 80


def test_readiness_uses_subjective():
    hist = _hist()
    hist[-1].update(fatigue=4, soreness=4, stress=4, injury=1)
    assert calc_readiness(hist) < calc_readiness(_hist())


def test_week_date_range():
    monday, sunday = week_date_range(16, 2026)
    assert monday == date(2026, 4, 13)
    assert sunday == date(2026, 4, 19)


def test_tsb_color_positive():
    from generate import STATUS_TEXT
    assert fmt_tsb_color(15) == STATUS_TEXT["good"]


def test_tsb_color_neutral():
    from generate import STATUS_TEXT
    assert fmt_tsb_color(0) == STATUS_TEXT["warn"]


def test_tsb_color_negative():
    from generate import STATUS_TEXT
    assert fmt_tsb_color(-15) == STATUS_TEXT["crit"]


def test_status_text_lesbar_auf_weiss():
    """Textfarben muessen Kontrast haben – Amber als Flaeche ist in Ordnung,
    als Zahl nicht. Deshalb gibt es beide Varianten."""
    from generate import STATUS_TEXT, STATUS_MARK
    assert set(STATUS_TEXT) == set(STATUS_MARK)
    assert STATUS_TEXT["warn"] != STATUS_MARK["warn"]


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


MOCK_WELLNESS_WITH_SUBJEKTIV = [
    {"id": "2026-04-12", "hrv": 40, "sleepSecs": 25200, "sleepQuality": 2, "ctl": 42.0, "atl": 38.0, "restingHR": 50,
     "fatigue": 1, "soreness": 1, "stress": 2, "injury": 1},
    {"id": "2026-04-13", "hrv": 43, "sleepSecs": 27000, "sleepQuality": 2, "ctl": 42.5, "atl": 37.0, "restingHR": 49,
     "fatigue": 1, "soreness": 1, "stress": 2, "injury": 1},
    {"id": "2026-04-14", "hrv": 45, "sleepSecs": 28800, "sleepQuality": 2, "ctl": 43.0, "atl": 36.0, "restingHR": 48,
     "fatigue": 1, "soreness": 1, "stress": 2, "injury": 1},
]


@patch("generate.get_wellness", return_value=MOCK_WELLNESS_WITH_SUBJEKTIV * 10)
@patch("generate.get_activities", return_value=[])
def test_build_context_subjektiv_keys(mock_act, mock_well):
    from generate import build_context
    ctx = build_context(kw=16, monday=date(2026, 4, 13), sunday=date(2026, 4, 19))
    assert "score_obj" in ctx
    assert "score_sub" in ctx
    assert "subjektiv_bars" in ctx
    assert "has_subjektiv" in ctx
    assert "verletzung_flag" in ctx
    assert ctx["has_subjektiv"] is True
    assert ctx["score_sub"] is not None


@patch("generate.get_wellness", return_value=[
    {"id": "2026-04-12", "hrv": 40, "sleepSecs": 25200, "sleepQuality": 2, "ctl": 42.0, "atl": 38.0, "restingHR": 50},
    {"id": "2026-04-13", "hrv": 43, "sleepSecs": 27000, "sleepQuality": 2, "ctl": 42.5, "atl": 37.0, "restingHR": 49},
    {"id": "2026-04-14", "hrv": 45, "sleepSecs": 28800, "sleepQuality": 2, "ctl": 43.0, "atl": 36.0, "restingHR": 48},
] * 10)
@patch("generate.get_activities", return_value=[])
def test_build_context_no_subjektiv_fallback(mock_act, mock_well):
    from generate import build_context
    ctx = build_context(kw=16, monday=date(2026, 4, 13), sunday=date(2026, 4, 19))
    assert ctx["has_subjektiv"] is False
    assert ctx["score_sub"] is None
    assert ctx["subjektiv_bars"] is None
    assert ctx["readiness_score"] == ctx["score_obj"]


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
    assert result["z5"] == 0,   "MIT should be 0%"
    assert result["z67"] == 0,  "HIT should be 0%"
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
    assert result["z5"] == 0,  "MIT should be 0"
    assert result["z67"] == 0, "HIT should be 0"


@patch("generate._api_get")
def test_calc_polarisation_mit_is_z5_hit_is_z6_z7(mock_api):
    # 300s Z5 = MIT (Schwelle); 300s each Z6, Z7 = HIT; 300s Z1 = LIT
    mock_api.return_value = {"icu_zone_times": _zone_times({1: 300, 5: 300, 6: 300, 7: 300})}
    acts = [{"id": "act1", "type": "Ride"}]
    result = _calc_polarisation(acts)
    total = 1200
    assert result["z12"] == round(300 / total * 100), "LIT wrong"
    assert result["z3"]  == 0,                        "Grauzone should be 0"
    assert result["z5"]  == round(300 / total * 100), "MIT should be Z5"
    assert result["z67"] == round(600 / total * 100), "HIT should be Z6+Z7"


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


# ── M1: calc_monotony_strain ─────────────────────────────────────────────────

def test_calc_monotony_strain_varied():
    daily = [100, 0, 80, 0, 90, 120, 60]
    result = calc_monotony_strain(daily)
    assert result["monotony"] < 1.5, f"Expected monotony < 1.5 for varied week, got {result['monotony']}"
    assert result["strain"] == round(sum(daily) * result["monotony"])


def test_calc_monotony_strain_uniform():
    daily = [80, 80, 80, 80, 80, 80, 80]
    result = calc_monotony_strain(daily)
    assert result["monotony"] > 2.0, f"Expected high monotony for uniform week, got {result['monotony']}"


def test_calc_monotony_strain_rest_lowers_monotony():
    with_rest = calc_monotony_strain([80, 0, 80, 80, 80, 80, 80])
    uniform   = calc_monotony_strain([80, 80, 80, 80, 80, 80, 80])
    assert with_rest["monotony"] < uniform["monotony"]


def test_calc_monotony_strain_zero_week():
    result = calc_monotony_strain([0, 0, 0, 0, 0, 0, 0])
    assert result["monotony"] == 0.0
    assert result["strain"] == 0


# ── M2: calc_ramprate ────────────────────────────────────────────────────────

def test_calc_ramprate_normal():
    w = [{"id": f"2026-04-{i:02d}", "atl": 38.0} for i in range(1, 18)]
    w.append({"id": "2026-04-25", "atl": 45.0})
    result = calc_ramprate(w)
    assert result == pytest.approx(7.0, abs=0.5)


def test_calc_ramprate_insufficient_data():
    assert calc_ramprate([{"id": "2026-04-25", "atl": 45.0}]) == 0.0


# ── D1: project_pmc ──────────────────────────────────────────────────────────

def test_project_pmc_keys():
    race_date = date.today() + timedelta(days=42)
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    planned = [(monday + timedelta(weeks=i), 400.0) for i in range(6)]
    result = project_pmc(ctl_today=65.0, atl_today=70.0,
                         planned_weekly_tss=planned, race_date=race_date)
    assert "ctl_race" in result
    assert "tsb_race" in result
    assert "tsb_status" in result
    assert isinstance(result["ctl_race"], float)


def test_project_pmc_taper_raises_tsb():
    # No training after today → ATL falls faster than CTL → TSB rises
    race_date = date.today() + timedelta(days=14)
    result = project_pmc(ctl_today=65.0, atl_today=75.0,
                         planned_weekly_tss=[], race_date=race_date)
    assert result["tsb_race"] > 0


from generate import _phase_for_kw, calc_compliance


def test_phase_for_kw_historie():
    """Abgeschlossene Saisons kommen aus SEASON_PHASES_ARCHIV."""
    assert _phase_for_kw(32, 2026)[0] == "Lauf"     # KW31–33 Lauf-Block
    assert _phase_for_kw(18, 2026)[0] == "Rad"      # KW14–26 Radsaison
    assert _phase_for_kw(38, 2026)[0] == "Race"     # KW38 Seelauf


def test_phase_for_kw_aus_dem_plan():
    """Die laufende Saison kommt aus periodisierung.md, nicht aus dem Code."""
    assert _phase_for_kw(40, 2026)[0] == "Nullpunkt"
    assert _phase_for_kw(45, 2026)[0] == "Schwelle"


def test_phase_for_kw_unbekannt():
    label, _ = _phase_for_kw(25, 2027)  # nach Saisonende, kein Plan
    assert label == "–"


def test_phase_farben_folgen_der_art():
    """Entlastung neutral, Test dunkel, Belastung auf der Marke."""
    from generate import _phase_style
    assert _phase_style("Entlastung", "−45%")[1] == "#8b837e"
    assert _phase_style("Nullpunkt", "🔬 FTP-Test")[1] == "#992f07"
    assert _phase_style("Block 1 · Schwelle", "Rad SwSp")[1] == "#d1450f"


def test_phase_kurzname_ohne_nummer():
    """"Block 1 · Schwelle" → "Schwelle": die Nummer traegt keine Information."""
    from generate import _phase_style
    assert _phase_style("Block 1 · Schwelle", "")[0] == "Schwelle"
    assert _phase_style("Rampe", "")[0] == "Rampe"


def test_calc_compliance_full():
    weeks = [
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 500},
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 480},
    ]
    assert calc_compliance(weeks) == 100


def test_calc_compliance_partial():
    weeks = [
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 500},
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 200},
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 500},
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 200},
    ]
    assert calc_compliance(weeks) == 50


def test_calc_compliance_ignores_no_plan():
    weeks = [
        {"is_current": False, "is_future": False, "tss_plan": 0,   "tss_ist": 0},
        {"is_current": False, "is_future": False, "tss_plan": 30,  "tss_ist": 20},
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 500},
    ]
    # Nur die Woche mit tss_plan > 50 zählt → 1/1 = 100%
    assert calc_compliance(weeks) == 100


def test_calc_compliance_empty():
    assert calc_compliance([]) == 0
    weeks = [{"is_current": True, "is_future": False, "tss_plan": 500, "tss_ist": 300}]
    assert calc_compliance(weeks) == 0  # laufende Woche ignoriert


from generate import get_tss_overview_history


def test_tss_weeks_has_plan_fields():
    """Jede Woche im Rückgabewert hat tss_plan, plan_bar_height_pct, phase_short, phase_color."""
    with patch("generate.get_activities", return_value=[]):
        weeks, summary = get_tss_overview_history(current_kw=18, num_weeks=3)
    for w in weeks:
        assert "tss_plan" in w, f"tss_plan fehlt in {w}"
        assert "plan_bar_height_pct" in w, f"plan_bar_height_pct fehlt in {w}"
        assert "phase_short" in w, f"phase_short fehlt in {w}"
        assert "phase_color" in w, f"phase_color fehlt in {w}"
    assert "compliance_pct" in summary
    assert "next_kw_plan" in summary


# ── calc_subjective ──────────────────────────────────────────────────────────

def test_calc_subjective_typical():
    """fatigue=1, soreness=1, stress=2, injury=1 → score=94"""
    result = calc_subjective([{"fatigue": 1, "soreness": 1, "stress": 2, "injury": 1}])
    assert result is not None
    assert result["score"] == 94
    assert result["verletzung_flag"] is None
    assert result["komponenten"]["ermuedung"]["punkte"] == 35
    assert result["komponenten"]["stress"]["punkte"] == 19


def test_calc_subjective_no_data():
    """Keine subjektiven Felder → None"""
    result = calc_subjective([{"hrv": 50, "ctl": 40.0}])
    assert result is None


def test_calc_subjective_verletzt():
    """injury=4 → score=0, verletzung_flag gesetzt"""
    result = calc_subjective([{"fatigue": 1, "soreness": 1, "stress": 1, "injury": 4}])
    assert result["score"] == 0
    assert result["verletzung_flag"] == "🚨 Verletzt"


def test_calc_subjective_partial():
    """Nur fatigue vorhanden → score aus 35/35 Punkten"""
    result = calc_subjective([{"fatigue": 1}])
    assert result is not None
    assert result["score"] == 100
    assert result["komponenten"]["muskelkater"] is None


# ── Template Tests: day.done Ist/Soll Display ────────────────────────────────

from jinja2 import Environment as _JinjaEnv

_DONE_TPL = """\
<div style="text-align:right;">
  <div style="display:flex;flex-direction:column;align-items:flex-end;gap:1px">
    <div style="display:flex;align-items:center;gap:3px">
      <span style="font-size:0.58rem;color:var(--muted)">Ist</span>
      <span style="font-size:0.72rem;font-weight:700;color:var(--green)">{{ day.tss_ist }}</span>
    </div>
    {% if day.tss_plan > 0 %}
    <div style="display:flex;align-items:center;gap:3px">
      <span style="font-size:0.58rem;color:var(--muted)">Soll</span>
      <span style="font-size:0.6rem;color:var(--muted)">{{ day.tss_plan }}</span>
    </div>
    {% endif %}
  </div>
</div>"""


def test_done_day_shows_ist_and_soll():
    tpl = _JinjaEnv().from_string(_DONE_TPL)
    out = tpl.render(day={"tss_ist": 92, "tss_plan": 85})
    assert "Ist" in out
    assert "92" in out
    assert "Soll" in out
    assert "85" in out


def test_done_day_no_plan_hides_soll():
    tpl = _JinjaEnv().from_string(_DONE_TPL)
    out = tpl.render(day={"tss_ist": 50, "tss_plan": 0})
    assert "Ist" in out
    assert "50" in out
    assert "Soll" not in out


# ── Template Tests: day.missed Soll-TSS Display ────────────────────────────────

_MISSED_TPL = """\
<div style="text-align:right;">
  <span class="badge-missed">Ausgefallen</span>
  {% if day.tss_plan > 0 %}
  <div style="font-size:0.6rem;color:var(--muted);margin-top:2px">Soll {{ day.tss_plan }} TSS</div>
  {% endif %}
</div>"""


def test_missed_day_shows_soll():
    tpl = _JinjaEnv().from_string(_MISSED_TPL)
    out = tpl.render(day={"tss_plan": 95})
    assert "Ausgefallen" in out
    assert "Soll" in out
    assert "95" in out


def test_missed_day_no_plan_hides_soll():
    tpl = _JinjaEnv().from_string(_MISSED_TPL)
    out = tpl.render(day={"tss_plan": 0})
    assert "Ausgefallen" in out
    assert "Soll" not in out


# ── Template Tests: RPE Mini-Bar ──────────────────────────────────────────────

_RPE_TPL = """\
{% if day.rpe %}
{% set rpe_color = "#60b8f5" if day.rpe <= 3 else ("#f5c842" if day.rpe <= 7 else "#f56060") %}
<div style="display:flex;align-items:center;gap:3px;margin-top:1px">
  <span style="font-size:0.58rem;color:var(--muted)">RPE</span>
  <span style="font-size:0.6rem;font-weight:600;color:{{ rpe_color }}">{{ day.rpe }}</span>
  <div style="width:32px;height:4px;background:rgba(255,255,255,0.1);border-radius:2px;overflow:hidden">
    <div style="width:{{ (day.rpe * 10)|int }}%;height:100%;border-radius:2px;background:{{ rpe_color }}"></div>
  </div>
</div>
{% endif %}"""


def test_rpe_shows_value_and_bar():
    tpl = _JinjaEnv().from_string(_RPE_TPL)
    out = tpl.render(day={"rpe": 7})
    assert "RPE" in out
    assert "7" in out
    assert "70%" in out
    assert "#f5c842" in out  # yellow for 4-7


def test_rpe_color_easy():
    tpl = _JinjaEnv().from_string(_RPE_TPL)
    out = tpl.render(day={"rpe": 2})
    assert "#60b8f5" in out  # blue for 1-3


def test_rpe_color_hard():
    tpl = _JinjaEnv().from_string(_RPE_TPL)
    out = tpl.render(day={"rpe": 9})
    assert "#f56060" in out  # red for 8-10
    assert "90%" in out


def test_rpe_hidden_when_none():
    tpl = _JinjaEnv().from_string(_RPE_TPL)
    out = tpl.render(day={"rpe": None})
    assert "RPE" not in out


# ── Saisonphasen aus planung/periodisierung.md ────────────────────────────────

def test_periodisierung_wird_geparst():
    from generate import parse_periodisierung
    phases = parse_periodisierung()
    assert phases, "Phasentabelle aus periodisierung.md nicht lesbar"
    assert all(p["start"] <= p["end"] for p in phases)


def test_periodisierung_lueckenlos():
    """Jede Phase schliesst direkt an die vorige an – sonst faellt eine Woche
    aus der Saisonleiste."""
    from generate import parse_periodisierung
    phases = parse_periodisierung()
    for a, b in zip(phases, phases[1:]):
        assert (b["start"] - a["end"]).days == 1, f"{a['kw']} -> {b['kw']}"


def test_periodisierung_ueber_jahreswechsel():
    """KW52-53 liegt 2026, KW01/27 im Folgejahr – die Reihenfolge muss halten."""
    from generate import parse_periodisierung
    phases = parse_periodisierung()
    assert phases == sorted(phases, key=lambda p: p["start"])
    jahreswechsel = [p for p in phases if p["start"].year != p["end"].year]
    assert jahreswechsel, "erwartet eine Phase ueber den Jahreswechsel"


def test_hinweis_nur_wenn_plan_auslaeuft():
    from datetime import timedelta
    from generate import parse_periodisierung, plan_horizon_note
    phases = parse_periodisierung()
    ende = phases[-1]["end"]
    assert plan_horizon_note(phases[0]["start"]) == ""
    assert "steht aus" in plan_horizon_note(ende - timedelta(days=7))
    assert "ausgelaufen" in plan_horizon_note(ende + timedelta(days=7))


def test_phase_fuer_datum():
    from datetime import date
    from generate import phase_for_date
    assert phase_for_date(date(2026, 9, 30))["short"] == "Nullpunkt"
    assert phase_for_date(date(2027, 1, 6))["short"] == "Standort"
    assert phase_for_date(date(2027, 6, 1)) is None


# ── Lauf-Aufbau, HF-160, Kern ────────────────────────────────────────────────

def test_run_km_limit_small_base_adds_3km():
    from generate import _run_km_limit
    assert _run_km_limit(8.0) == 11.0


def test_run_km_limit_uses_higher_of_prev_and_avg4():
    from generate import _run_km_limit
    # Ausfallwoche (0 km) darf die Grenze nicht auf 3 km druecken
    assert _run_km_limit(0.0, 20.0) == 22.0
    assert _run_km_limit(25.0, 20.0) == 27.5


def test_hf160_pace_median_in_band_after_10min():
    from generate import _hf160_pace
    n = 1200
    streams = [
        {"type": "time", "data": list(range(n))},
        {"type": "heartrate", "data": [150] * 600 + [160] * 600},
        {"type": "velocity_smooth", "data": [3.0] * 600 + [2.222] * 600},
    ]
    assert _hf160_pace(streams) == 450  # 2.222 m/s = 7:30/km


def test_hf160_pace_needs_3min_in_band():
    from generate import _hf160_pace
    streams = [
        {"type": "time", "data": list(range(900))},
        {"type": "heartrate", "data": [170] * 800 + [160] * 100},
        {"type": "velocity_smooth", "data": [2.5] * 900},
    ]
    assert _hf160_pace(streams) is None


def test_parse_kw_plan_detects_kern(tmp_path, monkeypatch):
    from generate import parse_kw_plan
    (tmp_path / "planung").mkdir()
    (tmp_path / "planung" / "kw50.md").write_text(
        "# KW50 – Test\n\n## Wochenplan\n\n"
        "| Tag | Workout | TSS ca. | TSS Ist | Status | Notiz |\n|---|---|---|---|---|---|\n"
        "| Mo | 🏃 Easy 40min | 30 | – | ⬜ | 🎯 Kern · morgens |\n"
        "| Di | 🚴 LIT-1h | 35 | – | ⬜ | |\n"
        "| **Total** | | **~65** | | | |\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    days = {d["tag"]: d for d in parse_kw_plan(50)["days"]}
    assert days["Mo"]["kern"] is True
    assert days["Di"]["kern"] is False
