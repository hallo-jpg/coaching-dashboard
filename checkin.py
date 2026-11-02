#!/usr/bin/env python3
"""Daten und Startsignal für den täglichen Morgen-Check-in des Coaches.

Die Routine „Morgen-Check-in“ läuft stündlich 8:10–13:10 (Berlin), 10 min nach dem COROS-Abruf.

  python3 checkin.py --gate   Exit 0, wenn der Check-in jetzt laufen soll, sonst 1 (Grund auf stdout)
  python3 checkin.py          Datenpaket für den Coach (gestern Soll/Ist, Nacht, Form, heute/morgen)

Startsignal: die heutige COROS-Nacht ist da (Bestätigung durch einen zweiten Abruf wird nicht
abgewartet – Nachschlafen nach 8 Uhr ist die Ausnahme, Stefan sagt es dann im Check-in), die gestrige Einheit ist bei intervals.icu
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
    night = coros_days.get(today.isoformat()) or {}
    if not (night.get("hrv") or night.get("asleep_min")):
        missing.append("COROS-Nacht noch nicht da")
    is_training = (yday_plan.get("tss_plan", 0) > 0 or yday_plan.get("is_run")
                   or yday_plan.get("is_kraft"))
    if not yday_plan.get("rest") and is_training and not yday_matched.get("done"):
        missing.append(f"gestrige Einheit ({yday_plan['workout']}) fehlt bei intervals.icu")

    if not missing:
        return True, "bereit"
    if hour >= LAST_HOUR:
        return True, "letzter Lauf, trotzdem starten – " + "; ".join(missing)
    return False, "warten: " + "; ".join(missing)


# ── Intervall-Qualität (Soll aus dem geplanten Workout, Ist aus icu_intervals) ──

QUALITY_MIN = {"Ride": 80, "Run": 90}   # % FTP bzw. % Schwellenpace – darunter keine Qualitätsarbeit
SINGLE_BAND = 0.02                      # Einzelwert-Ziel (z.B. 89 % FTP) → ±2 % Zielbereich
SLACK = 0.01                            # Rundung/Sensor: 1 % Luft am Rand, bevor ⬇️/⬆️


def _sport(t: str) -> str:
    return "Run" if "Run" in (t or "") else "Ride"


def _intensity(step: dict, sport: str):
    tgt = step.get("power") if sport == "Ride" else step.get("pace")
    if not tgt:
        return None
    if "value" in tgt:
        return tgt["value"], tgt["value"], tgt.get("units")
    return tgt.get("start"), tgt.get("end"), tgt.get("units")


def _to_abs(pct: float, units: str, sport: str, ftp: float, thr: float) -> float:
    if sport == "Ride":
        return ftp * pct / 100 if units == "%ftp" else pct
    return thr * pct / 100          # %pace: 100 % = Schwellentempo (als m/s)


def work_targets(doc: dict, sport: str, ftp: float, thr: float) -> list[dict]:
    """Arbeits-Intervalle des geplanten Workouts, ausgerollt, mit absolutem Zielbereich.

    Mit reps-Block: der intensivste Schritt je Block (Warmup-Opener zählen nicht).
    Ohne reps-Block: Schritte ab QUALITY_MIN, mind. 60 s, nicht Warmup/Cooldown, und
    mindestens halb so lang wie der längste davon (filtert kurze Opener).
    """
    sport = _sport(sport)
    steps = (doc or {}).get("steps") or []
    out = []
    blocks = [s for s in steps if s.get("reps") and s.get("steps")]
    if blocks:
        for b in blocks:
            inner = [(st, _intensity(st, sport)) for st in b["steps"]]
            inner = [(st, i) for st, i in inner if i and i[0] is not None]
            if not inner:
                continue
            top = max(i[1] for _, i in inner)
            if top < QUALITY_MIN[sport]:
                continue
            for _ in range(b["reps"]):
                for st, i in inner:
                    if i[1] == top:
                        out.append((st, i))
    else:
        cand = []
        for st in steps:
            i = _intensity(st, sport)
            if (i and i[0] is not None and min(i[0], i[1]) >= QUALITY_MIN[sport]
                    and st.get("duration", 0) >= 60 and not st.get("warmup") and not st.get("cooldown")):
                cand.append((st, i))
        longest = max((st["duration"] for st, _ in cand), default=0)
        out = [(st, i) for st, i in cand if st["duration"] >= longest / 2]

    targets = []
    for st, (a, b, units) in out:
        lo, hi = sorted((_to_abs(a, units, sport, ftp, thr), _to_abs(b, units, sport, ftp, thr)))
        if lo == hi:
            lo, hi = lo * (1 - SINGLE_BAND), hi * (1 + SINGLE_BAND)
        targets.append({"duration": st.get("duration", 0), "lo": lo, "hi": hi})
    return targets


def _pace(speed: float) -> str:
    s = round(1000 / speed)
    return f"{s // 60}:{s % 60:02d}"


def run_cadence_spm(a: dict):
    """intervals.icu liefert Laufkadenz in Doppelschritten/min → ×2."""
    if "Run" in (a.get("type") or "") and a.get("average_cadence"):
        return round(a["average_cadence"] * 2)
    return None


def quality_report(sport: str, doc: dict, intervals: list[dict], ftp: float, thr: float):
    """Soll/Ist je Arbeits-Intervall + Abfall erstes → letztes. None bei Einheiten ohne Qualitätsarbeit."""
    sport = _sport(sport)
    targets = work_targets(doc, sport, ftp, thr)
    if not targets:
        return None
    work = [iv for iv in intervals if iv.get("type") == "WORK"]
    key = "average_watts" if sport == "Ride" else "average_speed"
    rows, matched, pos = [], [], 0
    for t in targets:
        tol = max(0.2 * t["duration"], 30)
        hit = None
        for j in range(pos, len(work)):
            if abs(work[j].get("moving_time", 0) - t["duration"]) <= tol:
                hit, pos = work[j], j + 1
                break
        if sport == "Ride":
            soll = f"{round(t['lo'])}–{round(t['hi'])} W"
        else:
            soll = f"{_pace(t['hi'])}–{_pace(t['lo'])}/km"
        if hit is None or not hit.get(key):
            rows.append({"soll": soll, "ist": None, "urteil": "❌ fehlt"})
            continue
        val = hit[key]
        if val < t["lo"] * (1 - SLACK):
            urteil = "⬇️"
        elif val > t["hi"] * (1 + SLACK):
            urteil = "⬆️"
        else:
            urteil = "✅"
        row = {"soll": soll, "ist": f"{round(val)} W" if sport == "Ride" else f"{_pace(val)}/km",
               "urteil": urteil, "dauer_s": hit.get("moving_time"),
               "hf_avg": hit.get("average_heartrate"), "hf_max": hit.get("max_heartrate")}
        cad = hit.get("average_cadence")
        if cad:
            row["kadenz"] = round(cad * 2) if sport == "Run" else round(cad)
        rows.append(row)
        matched.append(hit)

    report = {"intervalle": rows,
              "erfuellt": f"{sum(r['urteil'] == '✅' for r in rows)}/{len(rows)}"}
    if len(matched) >= 2:
        first, last = matched[0], matched[-1]
        report["abfall"] = {
            "leistung_pct": round((last[key] - first[key]) / first[key] * 100, 1),
            "hf_max": (last.get("max_heartrate") or 0) - (first.get("max_heartrate") or 0)
                      if first.get("max_heartrate") and last.get("max_heartrate") else None,
        }
    return report


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
    if run_cadence_spm(a):
        out["kadenz_spm"] = run_cadence_spm(a)
        out.pop("average_cadence", None)   # Rohwert = Doppelschritte, nicht melden
    if a.get("type") in ("Run", "TrailRun") and a.get("distance") and a.get("moving_time"):
        s = a["moving_time"] / (a["distance"] / 1000)
        out["pace_min_km"] = f"{int(s // 60)}:{int(s % 60):02d}"
    return out


def _thresholds() -> tuple[float, float]:
    """FTP (W) und Schwellentempo (m/s) aus den intervals.icu-Sporteinstellungen."""
    from generate import _api_get
    ftp, thr = 300.0, 1000 / 388   # Fallback: 300 W · 6:28/km
    for st in _api_get("").get("sportSettings", []):
        types = st.get("types") or []
        if "Ride" in types and st.get("ftp"):
            ftp = st["ftp"]
        if "Run" in types and st.get("threshold_pace"):
            thr = st["threshold_pace"]
    return ftp, thr


def _quality(acts: list[dict]) -> list[dict]:
    """Intervall-Auswertung für jede gestrige Aktivität mit gekoppeltem Plan-Workout."""
    from generate import _api_get, _api_get_activity
    out, th = [], None
    for a in acts:
        if not a.get("paired_event_id") or a.get("type") == "WeightTraining":
            continue
        try:
            ev = _api_get(f"/events/{a['paired_event_id']}")
            doc = ev.get("workout_doc")
            if not doc:
                continue
            th = th or _thresholds()
            ivs = _api_get_activity(f"/{a['id']}/intervals").get("icu_intervals", [])
            rep = quality_report(a.get("type", ""), doc, ivs, *th)
        except Exception as e:  # Auswertung darf den Check-in nie blockieren
            out.append({"aktivitaet": a.get("name"), "fehler": str(e)})
            continue
        if rep:
            out.append({"aktivitaet": a.get("name"), "workout": ev.get("name"), **rep})
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
                    "erledigt": ymatched.get("done"),
                    "qualitaet": _quality(acts)},
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
