"""Fueling-Check für planung/kw*.md – prüft ⛽-Angaben gegen das geplante intervals.icu-Workout.

Bänder (g/h) aus coaching_science.md 10.3 – zwei Achsen:
  Intensität (Workout-Name) wählt die Gruppe, Dauer (moving_time) wählt die Zeile.
Eine Begründung in Klammern direkt hinter g/h – "⛽ 0g/h (nüchtern, FatMax)" – markiert
eine bewusste Abweichung und unterdrückt alle Befunde für diesen Tag.
Entstanden nach dem Fehler vom 8.11.2026 (45g/h für 1h45 SwSp, richtig 70–90g/h).
"""
import os
import re
from datetime import date, timedelta

GPH = re.compile(r"⛽\s*(\d+)\s*g/h(\s*\()?")
# KA als eigenes Wort in Großbuchstaben – "Kadenz" ist keine KA-Einheit
KA = re.compile(r"(?<![A-Za-z])KA(?![A-Za-z])")

# Reihenfolge = Vorrang bei Mischformen (z.B. "KA_1x10_SwSp_3x12" -> KA)
GROUPS = [
    ("rennen", re.compile(r"Rennen|Race")),
    ("hit", re.compile(r"HIT|VO2")),
    ("ka", KA),
    ("swsp", re.compile(r"SwSp|MIT|Schwelle|Over-Under")),
    ("lit", re.compile(r"LIT|Grundlage")),
]

WASSER_AB_GPH = 75   # coaching_science.md 10.2: über 75g/h zweite Flasche reines Wasser
LIT_MAX_IF = 70      # icu_intensity (IF × 100): darüber ist es keine LIT-Einheit mehr
RIDE_TYPES = ("Ride", "VirtualRide")


def _group(name):
    for group, pattern in GROUPS:
        if pattern.search(name):
            return group
    return None


def _band(group, minutes):
    """Erlaubte g/h laut coaching_science.md 10.3."""
    if group == "lit":
        if minutes < 90:
            return (0, 30)
        return (30, 50) if minutes <= 180 else (50, 70)
    if group == "ka":
        return (40, 60)      # bewusst unter Bedarf: AMPK-Reiz (Burke 2011)
    if group == "swsp":
        return (50, 70) if minutes <= 90 else (70, 90)
    if group == "hit":
        return (60, 80)
    if group == "rennen":
        return (90, 110)


def check_day(notiz, events):
    """Befunde [(code, text)] für einen Tag. events = intervals.icu-Events dieses Datums."""
    m = GPH.search(notiz)
    if not m or m.group(2):
        return []
    gph = int(m.group(1))

    workouts = [e for e in events if e.get("category") == "WORKOUT"]
    rides = [e for e in workouts if e.get("type") in RIDE_TYPES]
    if not rides:
        if any(e.get("type") == "Run" for e in workouts):
            return [("run", "⛽ an einem Lauftag – Läufe bekommen kein Fueling (außer Wettkampf)")]
        return [("kein_workout", f"⛽ {gph}g/h, aber kein geplantes Rad-Workout in intervals.icu")]

    ev = max(rides, key=lambda e: e.get("moving_time") or 0)
    name, minutes, intensity = ev["name"], (ev.get("moving_time") or 0) / 60, ev.get("icu_intensity")

    group = _group(name)
    if group is None:
        return [("gruppe", f"Intensität aus Name nicht erkennbar: '{name}'")]
    if intensity is not None and (group == "lit") != (intensity < LIT_MAX_IF):
        return [("if", f"'{name}' passt nicht zu IF {intensity / 100:.2f}")]

    lo, hi = _band(group, minutes)
    if not lo <= gph <= hi:
        return [("band", f"{gph}g/h außerhalb {lo}–{hi}g/h ({group}, {minutes:.0f}min) – '{name}'")]

    if gph >= WASSER_AB_GPH:
        texte = [notiz] + [e.get("description") or "" for e in events if e.get("category") == "NOTE"]
        if not any("Wasser" in t for t in texte):
            return [("wasser", f"{gph}g/h ohne Hinweis auf eine Flasche reines Wasser")]
    return []



ROW = re.compile(r"^\|\s*(Mo|Di|Mi|Do|Fr|Sa|So)\s*\|(.*)\|\s*$", re.MULTILINE)
TAGE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


def _week_monday(kw, today):
    """Montag der KW – das Jahr, in dem diese KW am nächsten an heute liegt (KW01 im Dezember = Folgejahr)."""
    kandidaten = []
    for jahr in (today.year - 1, today.year, today.year + 1):
        try:
            kandidaten.append(date.fromisocalendar(jahr, kw, 1))
        except ValueError:  # KW53 gibt es nicht in jedem Jahr
            pass
    return min(kandidaten, key=lambda d: abs((d - today).days))


def check_plan(text, kw, fetch, today):
    """Befunde ["Tag: text"] für eine kw*.md und ggf. ein Hinweis, warum übersprungen wurde.

    fetch(oldest, newest) liefert die intervals.icu-Events der Woche (siehe fetch_events).
    """
    notizen = {tag: zeile.split("|")[-1] for tag, zeile in ROW.findall(text)}
    if not any(GPH.search(n) for n in notizen.values()):
        return [], None  # Stub oder Woche ohne Fueling: intervals.icu nicht fragen

    montag = _week_monday(kw, today)
    try:
        events = fetch(montag, montag + timedelta(days=6))
    except Exception as e:  # offline, Proxy, fehlender Key: nicht blockieren (Design 8.11.)
        return [], f"Fueling-Check übersprungen: intervals.icu nicht erreichbar ({type(e).__name__})"

    befunde = []
    for i, tag in enumerate(TAGE):
        if tag not in notizen:
            continue
        datum = (montag + timedelta(days=i)).isoformat()
        tages_events = [e for e in events if (e.get("start_date_local") or "").startswith(datum)]
        befunde += [f"{tag}: {text}" for _, text in check_day(notizen[tag], tages_events)]
    return befunde, None


def fetch_events(oldest, newest):
    """Geplante Events aus intervals.icu (Key + Athlet aus der Umgebung, wie im Rest des Repos)."""
    import requests
    key, athlet = os.environ["INTERVALS_API_KEY"], os.environ["INTERVALS_ATHLETE_ID"]
    r = requests.get(
        f"https://intervals.icu/api/v1/athlete/{athlet}/events",
        params={"oldest": oldest.isoformat(), "newest": newest.isoformat()},
        auth=("API_KEY", key), timeout=15,
    )
    r.raise_for_status()
    return r.json()
