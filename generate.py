#!/usr/bin/env python3
from __future__ import annotations
import os
import base64
import math
from datetime import date, timedelta
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
