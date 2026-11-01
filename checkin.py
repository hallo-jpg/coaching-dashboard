#!/usr/bin/env python3
"""Daten und Startsignal für den täglichen Morgen-Check-in des Coaches.

Die Routine „Morgen-Check-in“ läuft stündlich 8:20–13:20 (Berlin), 20 min nach dem COROS-Abruf.

  python3 checkin.py --gate   Exit 0, wenn der Check-in jetzt laufen soll, sonst 1 (Grund auf stdout)
  python3 checkin.py          Datenpaket für den Coach (gestern Soll/Ist, Nacht, Form, heute/morgen)

Startsignal: COROS hat die heutige Nacht bestätigt, die gestrige Einheit ist bei intervals.icu
angekommen und heute gab es noch keinen Check-in. Ab dem letzten Lauf (13 Uhr) geht es auch mit
fehlenden Daten los – dann mit Hinweis, was fehlt.
"""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

BERLIN = ZoneInfo("Europe/Berlin")
LAST_HOUR = 13
CHECKIN_DIR = Path("planung/checkins")
DAY_ORDER = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


def checkin_file(today: date) -> Path:
    """Log-Datei der Woche des bewerteten Tages (gestern) – so sieht die Retro auch den Sonntag."""
    kw = (today - timedelta(days=1)).isocalendar()[1]
    return CHECKIN_DIR / f"kw{kw}.md"


def marker(today: date) -> str:
    return f"<!-- checkin {today.isoformat()} -->"


def already_done(log_text: str, today: date) -> bool:
    return marker(today) in log_text


def gate(today: date, hour: int, coros_days: dict, log_text: str,
         yday_plan: dict, yday_matched: dict) -> tuple[bool, str]:
    if already_done(log_text, today):
        return False, "Check-in heute bereits erledigt"

    missing = []
    if not (coros_days.get(today.isoformat()) or {}).get("confirmed"):
        missing.append("COROS-Nacht noch nicht bestätigt")
    is_training = (yday_plan.get("tss_plan", 0) > 0 or yday_plan.get("is_run")
                   or yday_plan.get("is_kraft"))
    if not yday_plan.get("rest") and is_training and not yday_matched.get("done"):
        missing.append(f"gestrige Einheit ({yday_plan['workout']}) fehlt bei intervals.icu")

    if not missing:
        return True, "bereit"
    if hour >= LAST_HOUR:
        return True, "letzter Lauf, trotzdem starten – " + "; ".join(missing)
    return False, "warten: " + "; ".join(missing)


# ── Datenabruf (intervals.icu + data/coros_wellness.json) ─────────────────────

def _plan_day(day: date) -> dict:
    from generate import parse_kw_plan
    plan = parse_kw_plan(day.isocalendar()[1])
    return next(d for d in plan["days"] if d["tag"] == DAY_ORDER[day.weekday()])


def _yesterday(today: date):
    from generate import get_activities, match_activities, parse_kw_plan
    yday = today - timedelta(days=1)
    monday = yday - timedelta(days=yday.weekday())
    plan = parse_kw_plan(yday.isocalendar()[1])
    acts = get_activities(yday.isoformat(), yday.isoformat())
    matched = match_activities(acts, plan["days"], monday)
    tag = DAY_ORDER[yday.weekday()]
    return next(d for d in plan["days"] if d["tag"] == tag), matched[tag], acts


def _activity_summary(a: dict) -> dict:
    keys = ["name", "type", "start_date_local", "moving_time", "distance", "icu_training_load",
            "average_heartrate", "max_heartrate", "icu_average_watts", "icu_weighted_avg_watts",
            "average_cadence", "icu_rpe", "feel", "pace", "icu_intensity", "description"]
    out = {k: a.get(k) for k in keys if a.get(k) not in (None, "")}
    if a.get("moving_time"):
        out["moving_min"] = round(a["moving_time"] / 60)
    if a.get("type") in ("Run", "TrailRun") and a.get("distance") and a.get("moving_time"):
        s = a["moving_time"] / (a["distance"] / 1000)
        out["pace_min_km"] = f"{int(s // 60)}:{int(s % 60):02d}"
    return out


def collect(today: date) -> dict:
    from generate import get_wellness, readiness_breakdown, load_coros
    yplan, ymatched, acts = _yesterday(today)
    hist = get_wellness((today - timedelta(days=40)).isoformat(), today.isoformat())
    hist = [w for w in hist if w.get("id", "")[:10] <= today.isoformat()]
    t = hist[-1] if hist else {}
    rb = readiness_breakdown(hist)
    return {
        "heute": today.isoformat(),
        "gestern": {"plan": yplan, "aktivitaeten": [_activity_summary(a) for a in acts],
                    "erledigt": ymatched.get("done")},
        "nacht_coros": load_coros().get(today.isoformat()),
        "readiness": {"score": rb["score"], "teile": rb["parts"], "flag": rb["flag"]},
        "form": {"ctl": t.get("ctl"), "atl": t.get("atl"),
                 "tsb": round(t["ctl"] - t["atl"], 1) if t.get("ctl") is not None and t.get("atl") is not None else None},
        "gefuehl_icu": {k: t.get(k) for k in ("fatigue", "soreness", "stress", "mood", "sleepQuality", "injury")
                        if t.get(k) is not None},
        "plan_heute": _plan_day(today),
        "plan_morgen": _plan_day(today + timedelta(days=1)),
        "log_datei": checkin_file(today).as_posix(),
        "marker": marker(today),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true", help="nur prüfen, ob der Check-in jetzt laufen soll")
    args = ap.parse_args()

    now = datetime.now(BERLIN)
    today = now.date()
    if args.gate:
        from generate import load_coros
        log = checkin_file(today)
        log_text = log.read_text(encoding="utf-8") if log.exists() else ""
        if already_done(log_text, today):
            print("Check-in heute bereits erledigt")
            raise SystemExit(1)
        yplan, ymatched, _ = _yesterday(today)
        ok, reason = gate(today, now.hour, load_coros(), log_text, yplan, ymatched)
        print(reason)
        raise SystemExit(0 if ok else 1)

    print(json.dumps(collect(today), indent=1, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
