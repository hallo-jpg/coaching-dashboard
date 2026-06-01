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
