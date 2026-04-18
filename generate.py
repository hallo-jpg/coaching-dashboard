#!/usr/bin/env python3
from __future__ import annotations
import os
import base64
import math
import re
from datetime import date, timedelta
from pathlib import Path
import requests

# ── Config ──────────────────────────────────────────────────────────────────
API_KEY = os.environ.get("INTERVALS_API_KEY", "")
ATHLETE_ID = os.environ.get("INTERVALS_ATHLETE_ID", "")
BASE_URL = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}"
AUTH = "Basic " + base64.b64encode(f"API_KEY:{API_KEY}".encode()).decode()
CIRC_OUTER = 2 * math.pi * 55   # ≈ 345.4 (r=55 ring)
CIRC_INNER = 2 * math.pi * 41   # ≈ 257.6 (r=41 ring)

# ── Pure utilities ────────────────────────────────────────────────────────────


def calc_ring_offset(value: float, max_value: float, circumference: float) -> float:
    """SVG stroke-dashoffset for a ring at value/max_value fill."""
    pct = min(max(value / max_value, 0), 1)
    return round(circumference * (1 - pct), 1)


def calc_readiness(hrv: float, hrv_7d_avg: float, sleep_secs: float, tsb: float) -> int:
    """Composite readiness score 0–100. Weights: HRV 40%, Sleep 35%, TSB 25%."""
    hrv_score = min(hrv / hrv_7d_avg, 1.25) / 1.25 * 100 if hrv_7d_avg else 50
    sleep_score = min(sleep_secs / (8 * 3600), 1.0) * 100
    tsb_score = min(max((tsb + 30) / 60, 0), 1) * 100
    return round(hrv_score * 0.40 + sleep_score * 0.35 + tsb_score * 0.25)


def week_date_range(kw: int, year: int) -> tuple[date, date]:
    """Returns (monday, sunday) for ISO week kw in year."""
    monday = date.fromisocalendar(year, kw, 1)
    return monday, monday + timedelta(days=6)


def fmt_tsb_color(tsb: float) -> str:
    """Returns hex color for TSB value."""
    if tsb >= 5:
        return "#3ecf8e"
    if tsb >= -5:
        return "#f5a623"
    return "#ef4444"


def readiness_label(score: int) -> str:
    """Returns emoji + label for readiness score."""
    if score >= 80:
        return "🟢 Voll trainieren"
    if score >= 60:
        return "🟡 Normal trainieren"
    if score >= 40:
        return "🟠 Reduziert trainieren"
    return "🔴 Ruhetag empfohlen"


def readiness_color(score: int) -> str:
    """Returns hex color for readiness score."""
    if score >= 80:
        return "#3ecf8e"
    if score >= 60:
        return "#f5a623"
    return "#ef4444"


# ── API client ────────────────────────────────────────────────────────────────


def _api_get(path: str) -> list | dict:
    """Generic GET request to intervals.icu API."""
    r = requests.get(
        f"{BASE_URL}{path}",
        headers={"Authorization": AUTH},
        timeout=15
    )
    r.raise_for_status()
    return r.json()


def get_wellness(oldest: str, newest: str) -> list[dict]:
    """Fetch wellness data for date range."""
    return _api_get(f"/wellness?oldest={oldest}&newest={newest}")


def get_activities(oldest: str, newest: str) -> list[dict]:
    """Fetch activities for date range."""
    return _api_get(f"/activities?oldest={oldest}&newest={newest}")


# ── KW Plan Parser ────────────────────────────────────────────────────────────

DAY_ORDER = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


def parse_kw_plan(kw: int) -> dict:
    """Parse planung/kw{kw}.md → {theme, sub, tss_plan, days: list[dict]}"""
    path = Path(f"planung/kw{kw}.md")
    if not path.exists():
        return {"theme": f"KW{kw}", "sub": "", "tss_plan": 0, "days": _empty_days()}

    text = path.read_text(encoding="utf-8")

    # Theme from heading: "# KW16 – Grundlagenblock Start" → "Grundlagenblock Start"
    m = re.search(r"^#\s+KW\d+\s+[-–]\s+(.+)$", text, re.MULTILINE)
    theme = m.group(1).strip() if m else f"KW{kw}"

    # Sub from "*Thema: ...*" line
    m_sub = re.search(r"^\*Thema:\s*(.+?)\*$", text, re.MULTILINE)
    sub = m_sub.group(1).strip() if m_sub else ""

    # Parse markdown table rows
    table_rows = re.findall(
        r"^\|\s*(Mo|Di|Mi|Do|Fr|Sa|So|\*\*Total\*\*)\s*\|(.+)$",
        text, re.MULTILINE
    )

    days = []
    tss_plan_total = 0

    for tag, rest in table_rows:
        if tag == "**Total**":
            m = re.search(r"\*\*~?(\d+)\*\*", rest)
            if m:
                tss_plan_total = int(m.group(1))
            continue

        cols = [c.strip() for c in rest.split("|")]
        workout = cols[0] if len(cols) > 0 else ""
        tss_soll_raw = cols[2] if len(cols) > 2 else "–"
        status = cols[4] if len(cols) > 4 else "–"

        tss_plan = 0
        m = re.search(r"(\d+)", tss_soll_raw)
        if m:
            tss_plan = int(m.group(1))

        is_run  = "🏃" in workout or "lauf" in workout.lower()
        is_rest = workout.strip() in ("Ruhetag", "–", "")

        # Strip emoji prefix
        workout_clean = re.sub(r"^[🚴🏃💪🧘]\s*", "", workout).strip()

        days.append({
            "tag":      tag,
            "workout":  workout_clean,
            "tss_plan": tss_plan,
            "status":   status,
            "rest":     is_rest,
            "is_run":   is_run,
        })

    # Ensure all 7 days present
    present = {d["tag"] for d in days}
    for t in DAY_ORDER:
        if t not in present:
            days.append({"tag": t, "workout": "", "tss_plan": 0,
                         "status": "–", "rest": False, "is_run": False})
    days.sort(key=lambda d: DAY_ORDER.index(d["tag"]))

    return {"theme": theme, "sub": sub, "tss_plan": tss_plan_total, "days": days}


def _empty_days() -> list:
    return [{"tag": t, "workout": "", "tss_plan": 0, "status": "–",
             "rest": t == "Mi", "is_run": False} for t in DAY_ORDER]


# ── Activity Matching & Data Building ────────────────────────────────────────

SPORT_TYPE_MAP = {
    "Ride": "ride", "VirtualRide": "ride", "GravelRide": "ride",
    "Run":  "run",  "TrailRun": "run",
    "WeightTraining": "strength", "Workout": "strength",
}


def match_activities(activities: list, plan_days: list, monday: date) -> dict:
    """Match activities to plan days by date. Returns {tag: {tss_ist, done, activity_name}}"""
    date_to_tag = {
        (monday + timedelta(days=i)).isoformat(): DAY_ORDER[i]
        for i in range(7)
    }

    matched = {
        d["tag"]: {"tss_ist": 0, "done": False, "activity_name": ""}
        for d in plan_days
    }

    for act in activities:
        act_date = act.get("start_date_local", "")[:10]
        tag = date_to_tag.get(act_date)
        if not tag:
            continue
        tss = act.get("icu_training_load") or 0
        matched[tag]["tss_ist"] += tss
        matched[tag]["done"] = True
        if not matched[tag]["activity_name"]:
            matched[tag]["activity_name"] = act.get("name", "")

    return matched


def build_day_rows(plan_days: list, matched: dict) -> list:
    """Merge plan + matched activity data into display rows."""
    rows = []
    for day in plan_days:
        tag = day["tag"]
        m = matched.get(tag, {"tss_ist": 0, "done": False, "activity_name": ""})
        done = m["done"]
        rest = day["rest"]

        if rest:
            dot = "dot-rest"
        elif day["is_run"]:
            dot = "dot-run"
        elif "KA" in day["workout"] or "55rpm" in day["workout"].lower():
            dot = "dot-ka"
        elif any(k in day["workout"] for k in ["SwSp", "HIT", "EB", "Schlüssel"]):
            dot = "dot-key"
        else:
            dot = "dot-planned"

        if not rest and not done:
            row_class = "day-missed" if _is_past(tag) else ""
        else:
            row_class = ""

        rows.append({
            "tag":           tag,
            "workout":       day["workout"],
            "tss_plan":      day["tss_plan"],
            "tss_ist":       m["tss_ist"],
            "done":          done,
            "rest":          rest,
            "is_run":        day["is_run"],
            "dot_class":     dot,
            "row_class":     row_class,
            "activity_name": m["activity_name"],
        })
    return rows


def _is_past(tag: str) -> bool:
    today_tag = DAY_ORDER[date.today().weekday()]
    return DAY_ORDER.index(tag) < DAY_ORDER.index(today_tag)
