#!/usr/bin/env python3
from __future__ import annotations
import os
import base64
import math
import re
from datetime import date, timedelta
from pathlib import Path
import requests
from jinja2 import Environment, FileSystemLoader

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


POWER_TARGETS = [
    (1, "1s"), (3, "3s"), (5, "5s"), (15, "15s"), (30, "30s"), (60, "1 min"), (180, "3 min"),
    (360, "6 min"), (480, "8 min"), (600, "10 min"),
    (1200, "20 min"), (3600, "60 min"), (5400, "90 min"),
]

def get_power_bests() -> list[dict]:
    """Fetch all-time power best efforts for target durations."""
    try:
        data = _api_get("/power-curves?type=Ride")
        curve = next((c for c in data.get("list", []) if c.get("id") == "1y"), None)
        if not curve:
            return []
        secs = curve.get("secs", [])
        watts = curve.get("watts", [])
        wkg = curve.get("watts_per_kg", [])
        results = []
        for target_s, label in POWER_TARGETS:
            if target_s in secs:
                idx = secs.index(target_s)
                w = watts[idx] if idx < len(watts) else None
                w_kg = round(wkg[idx], 2) if wkg and idx < len(wkg) else None
                results.append({"label": label, "watts": w, "wkg": w_kg})
            else:
                results.append({"label": label, "watts": None, "wkg": None})
        return results
    except Exception:
        return []


ATHLETE_WEIGHT_KG = 88

NUTRITION_CONFIG: dict = {
    "intense": {
        "protein_gkg": 2.0,
        "banner_color": "orange",
        "day_sub": "Intensiver Tag → Carbs + Protein hoch",
        "pre":    {"emoji": "🍌", "title": "Leicht",   "sub": "Banane, Toast, 90min vorher"},
        "during": {"emoji": "🍫", "title": "30–60g",   "sub": "Gel oder Riegel ab 45min"},
        "post":   {"emoji": "🥛", "title": "3:1",      "sub": "Carbs:Protein in 30min"},
        "tips": [
            {"color": "green",  "text": "Anti-entzündlich: Beeren, Omega-3 — unterstützt Anpassung"},
            {"color": "orange", "text": "Hydration: +500ml heute Abend, morgens Elektrolyte"},
        ],
    },
    "endurance_long": {
        "protein_gkg": 1.9,
        "banner_color": "orange",
        "day_sub": "Langer Ausdauertag → Kohlenhydrat-Fokus",
        "pre":    {"emoji": "🍝", "title": "Carbs",    "sub": "Pasta, Reis, 2–3h vorher"},
        "during": {"emoji": "🍫", "title": "60–90g/h", "sub": "Alle 20min essen/trinken"},
        "post":   {"emoji": "🥛", "title": "4:1",      "sub": "Carbs:Protein in 30min"},
        "tips": [
            {"color": "orange", "text": "Laden: Kohlenhydratspeicher voll auffüllen"},
            {"color": "green",  "text": "Hydration: 500ml extra + Elektrolyte vor dem Start"},
        ],
    },
    "endurance_short": {
        "protein_gkg": 1.8,
        "banner_color": "blue",
        "day_sub": "Kurzer Ausdauertag → Normal essen",
        "pre":    {"emoji": "🥣", "title": "Normal",   "sub": "Haferbrei, 1–2h vorher"},
        "during": {"emoji": "💧", "title": "Optional", "sub": "Wasser reicht bis 90min"},
        "post":   {"emoji": "🥛", "title": "3:1",      "sub": "Carbs:Protein in 30min"},
        "tips": [
            {"color": "green", "text": "Protein-Fokus: Quark, Eier, Hülsenfrüchte nach dem Training"},
            {"color": "blue",  "text": "Leichte Mahlzeiten — kein Volumen-Druck bei kurzen Einheiten"},
        ],
    },
    "rest": {
        "protein_gkg": 1.7,
        "banner_color": "muted",
        "day_sub": "Ruhetag → Carbs reduziert, Protein halten",
        "pre": None, "during": None, "post": None,
        "tips": [
            {"color": "green",  "text": "Carbs reduzieren: Mehr Gemüse, weniger Getreide heute"},
            {"color": "purple", "text": "Magnesium abends: 300–400mg unterstützt Schlafqualität"},
        ],
    },
    "sick": {
        "protein_gkg": 1.8,
        "banner_color": "red",
        "day_sub": "Krank → Leicht essen, viel trinken",
        "pre": None, "during": None, "post": None,
        "tips": [
            {"color": "blue",  "text": "Leicht essen — kein Druck, Appetit bestimmt die Menge"},
            {"color": "green", "text": "Viel trinken: Wasser, Tee, Brühe — Immunsystem unterstützen"},
        ],
    },
}


def _classify_day_type(day: dict, sick: bool) -> str:
    if sick:
        return "sick"
    workout = (day.get("workout") or "").lower()
    if day.get("rest") or workout in ("–", "-", "ruhetag", ""):
        return "rest"
    if any(k in workout for k in ("swsp", "hit", "vo2", "ka", "intervall", "_eb")):
        return "intense"
    if "lit" in workout and (day.get("tss_plan") or 0) >= 80:
        return "endurance_long"
    return "endurance_short"


def _protein_dist(protein_g: int) -> list:
    def r5(x: float) -> int:
        return round(x / 5) * 5
    return [
        f"~{r5(protein_g * 0.25)}g Frühstück",
        f"~{r5(protein_g * 0.30)}g Mittagessen",
        f"~{r5(protein_g * 0.25)}g Abendessen",
        f"~{r5(protein_g * 0.20)}g Snacks",
    ]


def get_nutrition_context(today_day: dict, sick: bool) -> dict:
    day_type = _classify_day_type(today_day, sick)
    cfg = NUTRITION_CONFIG[day_type]
    protein_g = round(cfg["protein_gkg"] * ATHLETE_WEIGHT_KG / 5) * 5
    workout = today_day.get("workout") or "Ruhetag"
    return {
        "day_type":     day_type,
        "day_label":    workout,
        "day_sub":      cfg["day_sub"],
        "banner_color": cfg["banner_color"],
        "protein_g":    protein_g,
        "protein_gkg":  cfg["protein_gkg"],
        "protein_dist": _protein_dist(protein_g),
        "pre":          cfg["pre"],
        "during":       cfg["during"],
        "post":         cfg["post"],
        "tips":         cfg["tips"],
    }


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


# ── Season config ─────────────────────────────────────────────────────────────

SEASON_PHASES = [
    {"name": "Baseline",    "kw": "KW14",    "start_kw": 14, "end_kw": 14},
    {"name": "Urlaub",      "kw": "KW15",    "start_kw": 15, "end_kw": 15},
    {"name": "Grundlage",   "kw": "KW16–17", "start_kw": 16, "end_kw": 17},
    {"name": "HIT-Aufbau",  "kw": "KW18–21", "start_kw": 18, "end_kw": 21},
    {"name": "TT-Spezifik", "kw": "KW22",    "start_kw": 22, "end_kw": 22},
    {"name": "Tapering",    "kw": "KW23",    "start_kw": 23, "end_kw": 23},
    {"name": "🏁 RadRace",  "kw": "KW24",    "start_kw": 24, "end_kw": 24},
    {"name": "Erholung",    "kw": "KW25",    "start_kw": 25, "end_kw": 25},
    {"name": "🗺️ Rosen.",  "kw": "KW26",    "start_kw": 26, "end_kw": 26},
]
RACE_KW  = 24
MONTH_DE = ["", "Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
            "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

# ── Context builder ───────────────────────────────────────────────────────────

def build_context(kw: int, monday: date, sunday: date) -> dict:
    wellness   = get_wellness((monday - timedelta(7)).isoformat(), sunday.isoformat())
    activities = get_activities(monday.isoformat(), sunday.isoformat())

    today_iso = date.today().isoformat()
    today_w = next((w for w in reversed(wellness) if w.get("id", "") <= today_iso and (w.get("ctl") or w.get("hrv"))), wellness[-1] if wellness else {})
    hrv     = today_w.get("hrv") or 0
    sleep_s = today_w.get("sleepSecs") or 0
    ctl     = today_w.get("ctl") or 0
    atl     = today_w.get("atl") or 0
    tsb     = round(ctl - atl, 1)
    rhr     = today_w.get("restingHR") or 60

    hrv_7d  = [w.get("hrv") or 0 for w in wellness if w.get("hrv")]
    hrv_avg = (sum(hrv_7d) / len(hrv_7d)) if hrv_7d else hrv or 40

    r_score = calc_readiness(hrv=hrv, hrv_7d_avg=hrv_avg, sleep_secs=sleep_s, tsb=tsb)
    r_color = readiness_color(r_score)
    r_label = readiness_label(r_score)
    r_sub   = _readiness_sub(rhr, hrv, hrv_avg, wellness)

    ctl_offset    = calc_ring_offset(ctl, 90, CIRC_OUTER)
    atl_offset    = calc_ring_offset(atl, 60, CIRC_INNER)
    r_offset      = calc_ring_offset(r_score, 100, CIRC_OUTER)
    season_pos    = kw - 14
    season_total  = RACE_KW - 14 + 1
    season_offset = calc_ring_offset(season_pos, season_total, CIRC_OUTER)

    current_phase = next(
        (p for p in SEASON_PHASES if p["start_kw"] <= kw <= p["end_kw"]),
        SEASON_PHASES[0]
    )
    next_phase_obj = next((p for p in SEASON_PHASES if p["start_kw"] > kw), None)
    next_phase = (f"{next_phase_obj['name']} ab KW{next_phase_obj['start_kw']}"
                  if next_phase_obj else "")

    phases = [
        {**p, "state": ("done"   if p["end_kw"] < kw else
                         "active" if p["start_kw"] <= kw <= p["end_kw"] else
                         "upcoming")}
        for p in SEASON_PHASES
    ]

    plan    = parse_kw_plan(kw)
    matched = match_activities(activities, plan["days"], monday)
    days    = build_day_rows(plan["days"], matched)
    tss_ist = sum(d["tss_ist"] for d in days)

    tss_plan_week = plan["tss_plan"]
    tss_compliance_pct = min(round(tss_ist / tss_plan_week * 100), 100) if tss_plan_week > 0 else 0
    tss_compliance_offset = calc_ring_offset(tss_compliance_pct, 100, CIRC_OUTER)
    tss_compliance_color = ("var(--green)" if tss_compliance_pct >= 80
                            else "var(--yellow)" if tss_compliance_pct >= 40
                            else "var(--accent)")

    sick_days   = [d for d in days if not d["done"] and not d["rest"] and _is_past(d["tag"])]
    sick_notice = ""
    if sick_days and all(not d["done"] for d in days if not d["rest"]):
        sick_notice = f"Krank – alle Einheiten ausgefallen (Details in kw{kw}.md)"

    def bar_color(pct: int) -> str:
        return "var(--green)" if pct >= 75 else "var(--yellow)" if pct >= 50 else "var(--red)"

    hrv_pct   = min(round(hrv / hrv_avg * 100), 100) if hrv_avg else 0
    sleep_h   = sleep_s / 3600 if sleep_s else 0
    sleep_pct = min(round(sleep_h / 8 * 100), 100)
    tsb_pct   = min(max(round((tsb + 30) / 60 * 100), 0), 100)
    rhr_base  = 50
    pulse_pct = max(0, min(100, round((1 - (rhr - rhr_base) / 20) * 100)))

    sparkline_data = wellness[-7:] if len(wellness) >= 7 else wellness
    sparkline = []
    for w in sparkline_data:
        w_hrv   = w.get("hrv") or hrv_avg
        w_sleep = w.get("sleepSecs") or 0
        w_ctl   = w.get("ctl") or ctl
        w_atl   = w.get("atl") or atl
        pct = calc_readiness(hrv=w_hrv, hrv_7d_avg=hrv_avg,
                             sleep_secs=w_sleep, tsb=w_ctl - w_atl)
        sparkline.append({"pct": pct, "color": readiness_color(pct)})

    prev_acts = get_activities(
        (monday - timedelta(7)).isoformat(),
        (monday - timedelta(1)).isoformat()
    )
    polar = _calc_polarisation(prev_acts)

    outlook = []
    for i in range(4):
        p = parse_kw_plan(kw + i)
        outlook.append({
            "kw":          kw + i,
            "theme":       p["theme"],
            "sub":         p["sub"],
            "tss_plan":    p["tss_plan"],
            "tss_ist":     tss_ist if i == 0 else 0,
            "key_workouts": _key_workouts(p["days"]),
        })

    kw_dates = (
        f"{monday.day}.–{sunday.day}. {MONTH_DE[monday.month]} {monday.year}"
        if monday.month == sunday.month
        else f"{monday.day}. {MONTH_DE[monday.month]}–{sunday.day}. {MONTH_DE[sunday.month]} {monday.year}"
    )

    today_tag = DAY_ORDER[date.today().weekday()]
    today_day_plan = next((d for d in days if d["tag"] == today_tag),
                          {"workout": "", "tss_plan": 0, "rest": True})
    nutrition = get_nutrition_context(today_day_plan, bool(sick_notice))

    return {
        "kw": kw, "kw_dates": kw_dates,
        "phase_name": current_phase["name"], "next_phase": next_phase,
        "phases": phases,
        "season_kw_current": season_pos, "season_kw_total": season_total,
        "season_offset": season_offset,
        "tss_compliance_pct": tss_compliance_pct,
        "tss_compliance_offset": tss_compliance_offset,
        "tss_compliance_color": tss_compliance_color,
        "readiness_score": r_score, "readiness_offset": r_offset,
        "readiness_color": r_color, "readiness_label": r_label, "readiness_sub": r_sub,
        "ctl": round(ctl, 1), "atl": round(atl, 1),
        "tsb_display": f"+{round(tsb):.0f}" if tsb >= 0 else f"{round(tsb):.0f}",
        "tsb_color": fmt_tsb_color(tsb),
        "ctl_offset": ctl_offset, "atl_offset": atl_offset,
        "tss_ist": tss_ist, "tss_plan": plan["tss_plan"],
        "sick_notice": sick_notice, "days": days,
        "hrv_pct": hrv_pct, "hrv_val": f"{round(hrv)}/40", "hrv_color": bar_color(hrv_pct),
        "sleep_pct": sleep_pct, "sleep_val": f"{sleep_h:.1f}h", "sleep_color": bar_color(sleep_pct),
        "tsb_bar_pct": tsb_pct, "tsb_bar_val": f"{tsb:+.0f}", "tsb_bar_color": bar_color(tsb_pct),
        "pulse_pct": pulse_pct, "pulse_val": f"{round(rhr)} bpm", "pulse_color": bar_color(pulse_pct),
        "sparkline": sparkline,
        "polar_z12_pct": polar["z12"], "polar_z3_pct": polar["z3"],
        "polar_z47_pct": polar["z47"], "polar_pi": polar["pi"], "polar_ok": polar["ok"],
        "outlook": outlook,
        "power_bests": get_power_bests(),
        "nutrition": nutrition,
    }

def _readiness_sub(rhr: float, hrv: float, hrv_avg: float, wellness: list) -> str:
    trend = ""
    if len(wellness) >= 2:
        prev_hrv = wellness[-2].get("hrv") or hrv
        diff = hrv - prev_hrv
        trend = " · Trend: ↑" if diff > 2 else " · Trend: ↓" if diff < -2 else ""
    rhr_note = " · Puls erhöht" if rhr > 55 else ""
    return f"HRV {'über' if hrv > hrv_avg else 'unter'} Schnitt{rhr_note}{trend}"

def _calc_polarisation(activities: list) -> dict:
    """Estimate zone split from ride activities via icu_z1..icu_z7 fields."""
    rides = [a for a in activities
             if a.get("type") in ("Ride", "VirtualRide", "GravelRide")]
    if not rides:
        return {"z12": 80, "z3": 15, "z47": 5, "pi": 80, "ok": True}
    totals = [0] * 8
    for r in rides:
        for z in range(1, 8):
            totals[z] += r.get(f"icu_z{z}") or 0
    total = sum(totals[1:]) or 1
    z12 = round((totals[1] + totals[2]) / total * 100)
    z3  = round(totals[3] / total * 100)
    z47 = 100 - z12 - z3
    return {"z12": z12, "z3": z3, "z47": z47, "pi": z12, "ok": z3 < 15}

def _key_workouts(days: list) -> str:
    non_lit = [d["workout"] for d in days
               if d["workout"] and not d["rest"]
               and not d["workout"].lower().startswith("lit")]
    return " · ".join(non_lit[:3]) if non_lit else "–"

# ── Renderer + entry point ────────────────────────────────────────────────────

def render(ctx: dict) -> str:
    env = Environment(loader=FileSystemLoader("."), autoescape=False)
    return env.get_template("dashboard.template.html").render(**ctx)

def main() -> None:
    today          = date.today()
    kw             = today.isocalendar()[1]
    year           = today.isocalendar()[0]
    monday, sunday = week_date_range(kw, year)
    ctx  = build_context(kw=kw, monday=monday, sunday=sunday)
    html = render(ctx)
    out  = Path("docs/dashboard.html")
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"✓ docs/dashboard.html generated for KW{kw}")

if __name__ == "__main__":
    main()
