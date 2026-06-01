#!/usr/bin/env python3
"""Route Pacing System — GPX Parser, Physics Model, HTML Renderer."""
from __future__ import annotations
import json
import math
import re
from datetime import date, datetime
from pathlib import Path

import gpxpy
from jinja2 import Environment, FileSystemLoader


# ── GPX Parser ────────────────────────────────────────────────────────────────

def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distance in metres between two lat/lon points."""
    R = 6_371_000
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    dφ = math.radians(lat2 - lat1)
    dλ = math.radians(lon2 - lon1)
    a = math.sin(dφ / 2) ** 2 + math.cos(φ1) * math.cos(φ2) * math.sin(dλ / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def parse_gpx(path: str) -> list[dict]:
    """Parse GPX file → list of {"dist": float, "ele": float} points at 50m intervals."""
    with open(path, encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    raw: list[dict] = []
    for track in gpx.tracks:
        for segment in track.segments:
            for pt in segment.points:
                raw.append({"lat": pt.latitude, "lon": pt.longitude, "ele": pt.elevation or 0.0})

    if len(raw) < 2:
        return []

    # Cumulative distance
    cum = 0.0
    pts: list[dict] = [{"dist": 0.0, "ele": raw[0]["ele"]}]
    for i in range(1, len(raw)):
        cum += _haversine_m(raw[i - 1]["lat"], raw[i - 1]["lon"], raw[i]["lat"], raw[i]["lon"])
        pts.append({"dist": cum, "ele": raw[i]["ele"]})

    # Resample at 50m intervals via linear interpolation
    INTERVAL = 50.0
    total = pts[-1]["dist"]
    resampled: list[dict] = []
    d = 0.0
    j = 0
    while d <= total:
        while j < len(pts) - 2 and pts[j + 1]["dist"] < d:
            j += 1
        seg_len = pts[j + 1]["dist"] - pts[j]["dist"]
        frac = (d - pts[j]["dist"]) / seg_len if seg_len > 0 else 0.0
        ele = pts[j]["ele"] + frac * (pts[j + 1]["ele"] - pts[j]["ele"])
        resampled.append({"dist": round(d, 1), "ele": round(ele, 1)})
        d += INTERVAL

    return resampled


def group_segments(pts: list[dict], min_dist_m: float = 300.0, grad_threshold: float = 1.5) -> list[dict]:
    """Group resampled points into meaningful segments.

    A new segment starts when gradient changes by >grad_threshold % OR
    after min_dist_m metres, whichever gives better readability (4-8 segs per route).
    """
    if len(pts) < 2:
        return []

    segments: list[dict] = []
    start = pts[0]

    for i in range(1, len(pts)):
        dist_m = pts[i]["dist"] - start["dist"]
        if dist_m < min_dist_m:
            continue

        grad = (pts[i]["ele"] - start["ele"]) / dist_m * 100

        # Check if gradient changed significantly vs previous segment
        prev_grad = segments[-1]["gradient_pct"] if segments else None
        new_seg = prev_grad is None or abs(grad - prev_grad) >= grad_threshold or dist_m >= 1200

        if new_seg:
            segments.append({
                "dist_m": round(dist_m, 1),
                "elev_start": round(start["ele"], 1),
                "elev_end": round(pts[i]["ele"], 1),
                "gradient_pct": round(grad, 2),
            })
            start = pts[i]

    # Last partial segment
    if pts[-1]["dist"] > start["dist"]:
        dist_m = pts[-1]["dist"] - start["dist"]
        if dist_m > 50:
            grad = (pts[-1]["ele"] - start["ele"]) / dist_m * 100
            segments.append({
                "dist_m": round(dist_m, 1),
                "elev_start": round(start["ele"], 1),
                "elev_end": round(pts[-1]["ele"], 1),
                "gradient_pct": round(grad, 2),
            })

    return segments


# ── Physics Model ─────────────────────────────────────────────────────────────

_PHYSICS = {
    "mass_kg":   96.0,   # Fahrer (88kg) + Rad (8kg)
    "g":          9.81,
    "Cr":         0.004,  # Rollwiderstand Asphalt
    "rho":        1.20,   # Luftdichte Meereshöhe
    "CdA_road":   0.32,   # Aufsitzposition Rennrad
    "CdA_tt":     0.26,   # TT-Position
}

_POWER_TABLE = [
    (0.0,          0.60),  # Abfahrt (<0%): 60% CP Erholung
    (2.0,          0.92),  # 0-2%: 92% CP
    (4.0,          0.97),  # 2-4%: 97% CP
    (6.0,          1.00),  # 4-6%: 100% CP
    (8.0,          1.05),  # 6-8%: 105% CP (W' Einsatz)
    (float("inf"), 1.08),  # >8%: 108% CP (W' aggressiv)
]

_TYPE_FACTOR = {
    "tt":          1.03,
    "climb":       1.00,
    "gran_fondo":  0.95,
}


def velocity_from_power(power_w: float, gradient_pct: float, route_type: str = "climb") -> float:
    """Solve velocity from target power and gradient (Newton's method).

    P = m*g*v*sin(arctan(g%/100)) + m*g*v*Cr*cos(theta) + 0.5*rho*CdA*v^3
    """
    m   = _PHYSICS["mass_kg"]
    g   = _PHYSICS["g"]
    Cr  = _PHYSICS["Cr"]
    rho = _PHYSICS["rho"]
    CdA = _PHYSICS["CdA_tt"] if route_type == "tt" else _PHYSICS["CdA_road"]

    theta     = math.atan(gradient_pct / 100)
    F_gravity = m * g * math.sin(theta)
    F_roll    = m * g * Cr * math.cos(theta)
    A_lin     = F_gravity + F_roll
    A_cube    = 0.5 * rho * CdA

    # Newton: f(v) = A_cube*v^3 + A_lin*v - P = 0
    v = max(power_w / max(A_lin + 1, 0.01), 0.5)
    for _ in range(30):
        fv  = A_cube * v ** 3 + A_lin * v - power_w
        dfv = 3 * A_cube * v ** 2 + A_lin
        if abs(dfv) < 1e-12:
            break
        delta = fv / dfv
        v = max(v - delta, 0.1)
        if abs(delta) < 1e-7:
            break
    return round(v, 4)


def assign_power(gradient_pct: float, route_type: str, cp_w: float) -> float:
    """Return target power for a segment (gradient table x type factor x CP)."""
    if gradient_pct < 0:
        return round(cp_w * 0.60)
    factor = _TYPE_FACTOR.get(route_type, 1.0)
    for threshold, pct in _POWER_TABLE:
        if gradient_pct < threshold:
            return round(cp_w * pct * factor)
    return round(cp_w * 1.08 * factor)


def compute_w_prime_balance(
    segments: list[dict],
    cp_w: float,
    w_prime_total_j: float,
    k_recovery: float = 0.35,
) -> list[dict]:
    """Track W' balance through the route. Adds 'w_prime_balance_j' to each segment."""
    balance = w_prime_total_j
    result = []
    for seg in segments:
        power = seg["target_w"]
        time_s = seg["time_s"]
        if power > cp_w:
            balance -= (power - cp_w) * time_s
        else:
            balance += k_recovery * (cp_w - power) * time_s
        balance = min(balance, w_prime_total_j)
        balance = max(balance, 0.0)
        result.append({**seg, "w_prime_balance_j": round(balance, 1)})
    return result
