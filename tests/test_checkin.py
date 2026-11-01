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
