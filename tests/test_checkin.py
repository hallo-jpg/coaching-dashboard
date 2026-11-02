import pytest
from datetime import date

from checkin import already_done, checkin_file, gate, marker

TODAY = date(2026, 11, 3)  # Di
COROS_OK = {"2026-11-03": {"hrv": 48, "confirmed": True}}
COROS_UNCONFIRMED = {"2026-11-03": {"hrv": 42, "confirmed": False}}
PLAN_RUN = {"tag": "Mo", "workout": "Lauf 45min", "rest": False, "tss_plan": 40, "is_run": True}
PLAN_REST = {"tag": "Mo", "workout": "Ruhetag", "rest": True}
DONE = {"done": True}
NOT_DONE = {"done": False}


def test_file_belongs_to_week_of_assessed_day():
    # Mo 9.11. bewertet So 8.11. → gehört in die KW45-Datei (Retro KW45 sieht den Sonntag)
    assert checkin_file(date(2026, 11, 9)).as_posix() == "planung/checkins/kw45.md"
    assert checkin_file(date(2026, 11, 3)).as_posix() == "planung/checkins/kw45.md"


def test_already_done_detects_marker():
    text = f"# KW45\n\n{marker(TODAY)}\n## Di 3.11.\n"
    assert already_done(text, TODAY)
    assert not already_done(text, date(2026, 11, 4))
    assert not already_done("", TODAY)


def test_ready_when_coros_confirmed_and_yesterday_done():
    ok, _ = gate(TODAY, 8, COROS_OK, "", PLAN_RUN, DONE)
    assert ok


def test_waits_for_coros_confirmation():
    ok, reason = gate(TODAY, 8, COROS_UNCONFIRMED, "", PLAN_RUN, DONE)
    assert not ok and "COROS" in reason
    ok, _ = gate(TODAY, 9, {}, "", PLAN_RUN, DONE)
    assert not ok


def test_waits_for_yesterdays_activity_sync():
    ok, reason = gate(TODAY, 9, COROS_OK, "", PLAN_RUN, NOT_DONE)
    assert not ok and "intervals" in reason


def test_rest_day_needs_no_activity():
    ok, _ = gate(TODAY, 8, COROS_OK, "", PLAN_REST, NOT_DONE)
    assert ok


def test_skips_when_already_done_today():
    ok, reason = gate(TODAY, 10, COROS_OK, marker(TODAY), PLAN_RUN, DONE)
    assert not ok and "bereits" in reason


def test_last_run_goes_ahead_with_notes():
    ok, reason = gate(TODAY, 13, COROS_UNCONFIRMED, "", PLAN_RUN, NOT_DONE)
    assert ok
    assert "COROS" in reason and "fehlt" in reason


def test_last_run_still_respects_already_done():
    ok, _ = gate(TODAY, 13, {}, marker(TODAY), PLAN_RUN, NOT_DONE)
    assert not ok


def test_non_training_plan_entry_needs_no_activity():
    umzug = {"tag": "Sa", "workout": "Umzugshilfe", "rest": False, "tss_plan": 0,
             "is_run": False, "is_kraft": False}
    ok, _ = gate(TODAY, 8, COROS_OK, "", umzug, NOT_DONE)
    assert ok


def test_kraft_day_waits_for_activity():
    kraft = {"tag": "Mo", "workout": "Kraft A", "rest": False, "tss_plan": 0,
             "is_run": False, "is_kraft": True}
    ok, _ = gate(TODAY, 9, COROS_OK, "", kraft, NOT_DONE)
    assert not ok


# ── Intervall-Qualität ────────────────────────────────────────────────────────
from checkin import work_targets, quality_report, run_cadence_spm

FTP = 300
THR = 2.5773196  # m/s = 6:28/km

SWSP_DOC = {"steps": [  # SwSp 3×12 vom 21.10. (inkl. 2-min-Opener 90 % im Warmup)
    {"ramp": True, "power": {"start": 45, "end": 65, "units": "%ftp"}, "warmup": True, "duration": 900},
    {"power": {"units": "%ftp", "value": 75}, "duration": 120},
    {"power": {"units": "%ftp", "value": 90}, "duration": 120},
    {"power": {"units": "%ftp", "value": 55}, "duration": 300},
    {"reps": 3, "steps": [{"power": {"units": "%ftp", "value": 89}, "duration": 720},
                          {"power": {"units": "%ftp", "value": 55}, "duration": 300}]},
    {"power": {"units": "%ftp", "value": 55}, "duration": 780}]}

SWSP_IVS = [  # echte icu_intervals 21.10.
    {"type": "RECOVERY", "moving_time": 1023, "average_watts": 168, "average_heartrate": 133, "max_heartrate": 151},
    {"type": "WORK", "moving_time": 111, "average_watts": 227, "average_heartrate": 152, "max_heartrate": 157},
    {"type": "WORK", "moving_time": 117, "average_watts": 273, "average_heartrate": 163, "max_heartrate": 170},
    {"type": "RECOVERY", "moving_time": 305, "average_watts": 169, "average_heartrate": 145, "max_heartrate": 170},
    {"type": "WORK", "moving_time": 717, "average_watts": 270, "average_heartrate": 169, "max_heartrate": 177, "average_cadence": 95},
    {"type": "RECOVERY", "moving_time": 302, "average_watts": 168},
    {"type": "WORK", "moving_time": 717, "average_watts": 270, "average_heartrate": 170, "max_heartrate": 177, "average_cadence": 95},
    {"type": "RECOVERY", "moving_time": 303, "average_watts": 168},
    {"type": "WORK", "moving_time": 718, "average_watts": 255, "average_heartrate": 174, "max_heartrate": 180, "average_cadence": 94},
]

RUN_DOC = {"steps": [  # Lauf-Schwelle 3×6 (KW45 Fr), ohne reps-Block
    {"pace": {"start": 75, "end": 85, "units": "%pace"}, "duration": 720},
    {"pace": {"start": 96, "end": 100, "units": "%pace"}, "duration": 360},
    {"pace": {"start": 70, "end": 78, "units": "%pace"}, "duration": 120},
    {"pace": {"start": 96, "end": 100, "units": "%pace"}, "duration": 360},
    {"pace": {"start": 70, "end": 78, "units": "%pace"}, "duration": 120},
    {"pace": {"start": 96, "end": 100, "units": "%pace"}, "duration": 360},
    {"pace": {"start": 75, "end": 85, "units": "%pace"}, "duration": 360}]}


def test_ride_targets_take_main_set_not_warmup_opener():
    t = work_targets(SWSP_DOC, "Ride", FTP, THR)
    assert len(t) == 3
    assert all(x["duration"] == 720 for x in t)
    assert t[0]["lo"] == pytest.approx(267 * 0.98, abs=1) and t[0]["hi"] == pytest.approx(267 * 1.02, abs=1)


def test_run_targets_without_reps_block():
    t = work_targets(RUN_DOC, "Run", FTP, THR)
    assert len(t) == 3
    assert all(x["duration"] == 360 for x in t)
    assert t[0]["lo"] == pytest.approx(THR * 0.96, rel=1e-3)


def test_quality_report_rates_each_interval_and_fade():
    r = quality_report("Ride", SWSP_DOC, SWSP_IVS, FTP, THR)
    v = [i["urteil"] for i in r["intervalle"]]
    assert v == ["✅", "✅", "⬇️"]
    assert r["intervalle"][0]["ist"] == "270 W"
    assert r["erfuellt"] == "2/3"
    assert r["abfall"]["hf_max"] == 3          # 177 → 180
    assert r["abfall"]["leistung_pct"] == pytest.approx(-5.6, abs=0.1)


def test_quality_report_marks_missing_interval():
    ivs = SWSP_IVS[:7]  # drittes Intervall nicht gefahren
    r = quality_report("Ride", SWSP_DOC, ivs, FTP, THR)
    assert [i["urteil"] for i in r["intervalle"]] == ["✅", "✅", "❌ fehlt"]
    assert r["erfuellt"] == "2/3"


def test_quality_report_run_pace_and_cadence():
    ivs = [{"type": "WORK", "moving_time": 720, "average_speed": 2.1},
           {"type": "WORK", "moving_time": 362, "average_speed": 2.55, "average_heartrate": 178, "max_heartrate": 184, "average_cadence": 85},
           {"type": "RECOVERY", "moving_time": 120, "average_speed": 1.9},
           {"type": "WORK", "moving_time": 358, "average_speed": 2.62, "average_heartrate": 181, "max_heartrate": 188, "average_cadence": 86},
           {"type": "RECOVERY", "moving_time": 120, "average_speed": 1.9},
           {"type": "WORK", "moving_time": 360, "average_speed": 2.40, "average_heartrate": 182, "max_heartrate": 190, "average_cadence": 84}]
    r = quality_report("Run", RUN_DOC, ivs, FTP, THR)
    assert [i["urteil"] for i in r["intervalle"]] == ["✅", "⬆️", "⬇️"]
    assert r["intervalle"][0]["ist"] == "6:32/km"
    assert r["intervalle"][0]["kadenz"] == 170
    assert r["intervalle"][0]["soll"] == "6:28–6:44/km"


def test_easy_workout_has_no_quality_report():
    easy = {"steps": [{"pace": {"start": 75, "end": 87, "units": "%pace"}, "duration": 1800}]}
    assert quality_report("Run", easy, [], FTP, THR) is None


def test_run_cadence_doubled():
    assert run_cadence_spm({"type": "Run", "average_cadence": 82.5}) == 165
    assert run_cadence_spm({"type": "VirtualRide", "average_cadence": 90}) is None
