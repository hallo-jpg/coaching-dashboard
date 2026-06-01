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
    "mass_kg":   99.0,   # Fahrer (91kg) + Rad (8kg)
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
    "tt":          1.08,
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


# ── Athlete Data Reader ───────────────────────────────────────────────────────

def read_athlete_params() -> dict:
    """Read FTP, CP, W' from athlete/profil.md and athlete/fortschritt.md."""
    params = {"ftp_w": 305, "cp_w": 305, "w_prime_j": 28_100}

    profil = Path("athlete/profil.md")
    if profil.exists():
        text = profil.read_text(encoding="utf-8")
        m = re.search(r"\*\*FTP\*\*\s*\|\s*\*\*(\d+)W\*\*", text)
        if m:
            params["ftp_w"] = int(m.group(1))

    fortschritt = Path("athlete/fortschritt.md")
    if fortschritt.exists():
        text = fortschritt.read_text(encoding="utf-8")
        m_cp = re.search(r"\|\s*\*\*(\d+)W\*\*\s*\|\s*\*\*([\d,]+)\s*kJ\*\*", text)
        if m_cp:
            params["cp_w"] = int(m_cp.group(1))
            params["w_prime_j"] = int(float(m_cp.group(2).replace(",", ".")) * 1000)

    return params


def load_route_meta(gpx_path: str) -> dict:
    """Read optional JSON metadata beside the GPX file. Returns defaults if absent."""
    defaults = {
        "name": Path(gpx_path).stem.replace("-", " ").replace("_", " ").title(),
        "type": "climb",
        "event_date": None,
        "target_if": 0.95,
        "type_factor_override": None,
        "notes": "",
    }
    meta_path = Path(gpx_path).with_suffix(".json")
    if not meta_path.exists():
        return defaults
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        return {**defaults, **data}
    except (json.JSONDecodeError, OSError):
        return defaults


def compute_route(
    segments: list[dict],
    athlete: dict,
    route_type: str = "climb",
    type_factor_override: float | None = None,
) -> list[dict]:
    """Combine all engine steps into full segment dicts with power, speed, time, W'."""
    cp = athlete["cp_w"]
    w_prime = athlete["w_prime_j"]

    cum_dist = 0.0
    enriched = []
    for seg in segments:
        power = assign_power(seg["gradient_pct"], route_type, cp)
        if type_factor_override is not None:
            base_factor = _TYPE_FACTOR.get(route_type, 1.0)
            power = round(power * type_factor_override / base_factor)
        v_ms  = velocity_from_power(power, seg["gradient_pct"], route_type)
        time_s = seg["dist_m"] / max(v_ms, 0.1)

        pct_cp = power / cp
        if pct_cp < 0.65:
            zone_label, zone_color = "Erholung", "#4ade80"
        elif pct_cp < 0.97:
            zone_label, zone_color = "Aerob", "#4ade80"
        elif pct_cp < 1.03:
            zone_label, zone_color = "MIT", "#facc15"
        elif pct_cp < 1.08:
            zone_label, zone_color = "MIT+", "#f97316"
        else:
            zone_label, zone_color = "HIT", "#ef4444"

        km_start = round(cum_dist / 1000, 2)
        cum_dist += seg["dist_m"]
        km_end   = round(cum_dist / 1000, 2)

        enriched.append({
            **seg,
            "target_w":   power,
            "speed_kmh":  round(v_ms * 3.6, 1),
            "time_s":     round(time_s, 1),
            "km_start":   km_start,
            "km_end":     km_end,
            "km_label":   f"km {km_start:.1f}–{km_end:.1f}",
            "zone_label": zone_label,
            "zone_color": zone_color,
        })

    return compute_w_prime_balance(enriched, cp, w_prime)


# ── Intuition Text ────────────────────────────────────────────────────────────

def generate_intuition(segments: list[dict], athlete: dict) -> list[str]:
    """Generate 3-4 coaching sentences explaining what the numbers feel like."""
    cp = athlete["cp_w"]
    w_total_kj = athlete["w_prime_j"] / 1000
    tips: list[str] = []

    if not segments:
        return ["Keine Segmentdaten verfügbar."]

    first = segments[0]
    tips.append(
        f"Start ({first['km_label']}): {first['target_w']}W fühlt sich zu leicht an — das ist korrekt. "
        f"Bei richtigem Pacing setzt das Belastungsgefühl erst nach 3–5 Min ein. Wenn es schon am "
        f"Start schwer wirkt, bist du zu schnell."
    )

    hard_segs = [s for s in segments if s["gradient_pct"] > 4]
    if hard_segs:
        steepest = max(hard_segs, key=lambda s: s["gradient_pct"])
        min_dur  = int(steepest["time_s"] / 60)
        tips.append(
            f"Steilstück {steepest['km_label']} ({steepest['gradient_pct']:.1f}%): "
            f"{steepest['target_w']}W für ~{min_dur} Min — das entspricht von der Intensität "
            f"deiner MIT-Schwellenarbeit vom Training. Dieses Gefühl kennst du. Hier ist es wichtig, "
            f"nicht zu überziehen: über {steepest['target_w'] + 15}W kosten unverhältnismäßig viel W'."
        )

    w_spent  = (athlete["w_prime_j"] - segments[-1]["w_prime_balance_j"]) / 1000
    w_remain = segments[-1]["w_prime_balance_j"] / 1000
    if w_remain < 5:
        budget_comment = "sehr knapp — kein Spielraum. Pacing exakt einhalten."
    elif w_remain < 10:
        budget_comment = "ausreichend für kleinere Tempoanpassungen."
    else:
        budget_comment = "komfortabel — du kannst auf unerwartete Steilpassagen reagieren."
    tips.append(
        f"W'-Budget: {w_spent:.1f} von {w_total_kj:.1f} kJ verplant, "
        f"{w_remain:.1f} kJ Reserve — {budget_comment}"
    )

    tips.append(
        "Herzrate ignorieren: Bei dieser Belastungsdauer steigt die HR kontinuierlich bis zum Ziel. "
        "Watt ist der Anker — HR ist nur Kontrollgröße, kein Steuerungsinstrument."
    )
    return tips


# ── SVG Profile Generator ─────────────────────────────────────────────────────

def _build_svg_profile(segments: list[dict], width: int = 800, height: int = 160) -> str:
    """Build SVG elevation profile. Text outside scaled SVG area (no distortion)."""
    if not segments:
        return ""

    total_dist = sum(s["dist_m"] for s in segments)
    all_eles   = [s["elev_start"] for s in segments] + [segments[-1]["elev_end"]]
    ele_min    = min(all_eles)
    ele_max    = max(all_eles)
    ele_range  = max(ele_max - ele_min, 1)

    PAD_TOP, PAD_BOT = 30, 20
    chart_h = height - PAD_TOP - PAD_BOT

    def x(dist_m: float) -> float:
        return dist_m / total_dist * width

    def y(ele: float) -> float:
        return PAD_TOP + chart_h * (1 - (ele - ele_min) / ele_range)

    pts_coords: list[tuple] = []
    cum = 0.0
    for seg in segments:
        pts_coords.append((x(cum), y(seg["elev_start"])))
        cum += seg["dist_m"]
    pts_coords.append((x(cum), y(segments[-1]["elev_end"])))

    poly_pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts_coords)
    fill_pts = poly_pts + f" {width:.1f},{height} 0,{height}"

    lines: list[str] = [
        f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" '
        f'style="display:block;border-radius:8px;overflow:visible">',
    ]

    cum = 0.0
    for seg in segments:
        color = seg["zone_color"]
        x1 = x(cum)
        x2 = x(cum + seg["dist_m"])
        lines.append(
            f'<rect x="{x1:.1f}" y="{PAD_TOP}" width="{x2-x1:.1f}" height="{chart_h}" '
            f'fill="{color}" fill-opacity="0.18"/>'
        )
        cum += seg["dist_m"]

    lines.append(f'<polygon points="{fill_pts}" fill="rgba(255,255,255,0.04)"/>')
    lines.append(
        f'<polyline points="{poly_pts}" fill="none" stroke="#e2e8f0" '
        f'stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>'
    )

    cum = 0.0
    for seg in segments:
        cx = x(cum + seg["dist_m"] / 2)
        color = seg["zone_color"]
        lines.append(
            f'<text x="{cx:.1f}" y="{PAD_TOP - 12}" text-anchor="middle" '
            f'fill="{color}" font-size="12" font-weight="700" font-family="sans-serif">'
            f'{seg["gradient_pct"]:.1f}%</text>'
        )
        lines.append(
            f'<text x="{cx:.1f}" y="{PAD_TOP}" text-anchor="middle" '
            f'fill="{color}" font-size="11" font-family="sans-serif">'
            f'{seg["target_w"]}W</text>'
        )
        x_start = x(cum)
        lines.append(
            f'<text x="{x_start:.1f}" y="{height}" text-anchor="middle" '
            f'fill="#475569" font-size="10" font-family="sans-serif">'
            f'{seg["km_start"]:.1f}</text>'
        )
        cum += seg["dist_m"]

    lines.append(
        f'<text x="{width}" y="{height}" text-anchor="end" '
        f'fill="#475569" font-size="10" font-family="sans-serif">'
        f'{segments[-1]["km_end"]:.1f} km</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


# ── Route Context Builder ─────────────────────────────────────────────────────

def build_route_context(gpx_path: str) -> dict:
    """Full context dict for Jinja2 template from a GPX file."""
    meta    = load_route_meta(gpx_path)
    athlete = read_athlete_params()
    pts     = parse_gpx(gpx_path)
    segs_raw = group_segments(pts)
    segments = compute_route(segs_raw, athlete, route_type=meta["type"],
                             type_factor_override=meta.get("type_factor_override"))

    total_time_s  = sum(s["time_s"] for s in segments)
    total_dist_m  = sum(s["dist_m"] for s in segments)
    total_ele     = sum(max(s["elev_end"] - s["elev_start"], 0) for s in segments)
    avg_power     = (sum(s["target_w"] * s["time_s"] for s in segments)
                     / max(total_time_s, 1))
    w_spent_kj    = (athlete["w_prime_j"] - segments[-1]["w_prime_balance_j"]) / 1000 if segments else 0
    w_remain_kj   = segments[-1]["w_prime_balance_j"] / 1000 if segments else athlete["w_prime_j"] / 1000

    def fmt_time(secs: float) -> str:
        m, s = divmod(int(secs), 60)
        return f"{m}:{s:02d}"

    t_low  = fmt_time(total_time_s * 0.97)
    t_high = fmt_time(total_time_s * 1.05)

    event_date_str = ""
    if meta.get("event_date"):
        try:
            d = date.fromisoformat(meta["event_date"])
            event_date_str = d.strftime("%-d. %B %Y")
        except ValueError:
            event_date_str = meta["event_date"]

    for seg in segments:
        m_t, s_t = divmod(int(seg["time_s"]), 60)
        seg["time_fmt"] = f"{m_t}:{s_t:02d}"

    return {
        "name":               meta["name"],
        "route_type":         meta["type"],
        "event_date":         event_date_str,
        "notes":              meta.get("notes", ""),
        "segments":           segments,
        "total_time_s":       round(total_time_s),
        "total_time_fmt":     fmt_time(total_time_s),
        "total_time_range":   f"{t_low}–{t_high}",
        "total_dist_km":      round(total_dist_m / 1000, 2),
        "total_ele_m":        round(total_ele),
        "avg_power_w":        round(avg_power),
        "avg_if":             round(avg_power / max(athlete["ftp_w"], 1), 2),
        "w_prime_spent_kj":   round(w_spent_kj, 1),
        "w_prime_remaining_kj": round(w_remain_kj, 1),
        "w_prime_total_kj":   round(athlete["w_prime_j"] / 1000, 1),
        "w_prime_pct_used":   round(w_spent_kj / max(athlete["w_prime_j"] / 1000, 1) * 100),
        "intuition":          generate_intuition(segments, athlete),
        "svg_profile":        _build_svg_profile(segments),
        "athlete":            athlete,
    }


# ── Renderer + Entry Point ────────────────────────────────────────────────────

def render_pacing(
    routes_dir: str = "athlete/routes",
    template_path: str = "pacing.template.html",
    output_path: str = "docs/pacing.html",
) -> None:
    """Render all active GPX routes to docs/pacing.html."""
    gpx_files = sorted(Path(routes_dir).glob("*.gpx"))
    if not gpx_files:
        print(f"[pacing] Keine GPX-Dateien in {routes_dir} gefunden — übersprungen.")
        return

    routes = []
    for gpx_path in gpx_files:
        try:
            ctx = build_route_context(str(gpx_path))
            routes.append(ctx)
            print(f"[pacing] {ctx['name']}: {ctx['total_time_fmt']} · {ctx['avg_power_w']}W")
        except Exception as e:
            print(f"[pacing] Fehler bei {gpx_path.name}: {e}")

    if not routes:
        return

    routes.sort(key=lambda r: (r["event_date"] == "", r["event_date"] or "9999"))

    env = Environment(loader=FileSystemLoader("."), autoescape=False)
    template = env.get_template(template_path)
    html = template.render(routes=routes, generated_at=datetime.now().strftime("%d.%m.%Y %H:%M"))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(html, encoding="utf-8")
    print(f"[pacing] -> {output_path} ({len(routes)} Route(n))")


if __name__ == "__main__":
    render_pacing()
