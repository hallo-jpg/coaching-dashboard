"""COROS-Uhrdaten → data/coros_wellness.json.

Liest die Textausgaben der COROS-MCP-Tools `querySleepOverview`, `querySleepHrv`,
`queryRestingHeartRate` und `queryDailyHealthData` (von der täglichen Claude-Routine
als Dateien abgelegt) und führt sie in data/coros_wellness.json zusammen.
generate.py legt diese Werte über die intervals.icu-Wellness: alles, was die Uhr misst,
kommt von COROS – intervals.icu liefert nur noch Gefühl, Gewicht und CTL/ATL.

    python3 coros_wellness.py --overview overview.txt --hrv hrv.txt --rhr rhr.txt --daily daily.txt

Schlüssel = Aufwach-Tag (COROS-Konvention, gleich wie intervals.icu-Wellness).
"""
import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "coros_wellness.json"
KEEP_DAYS = 120
EARLY_MIN = 120   # „erste Nachthälfte" für das Vorabend-Muster: die ersten 2h nach dem Einschlafen

_DATE = re.compile(r"^(\d{4}-\d{2}-\d{2}):?\s*$")


def _read(path: str) -> str:
    """MCP-Ausgabe kann roh oder als JSON-String (mit \\n-Escapes) gespeichert sein."""
    text = Path(path).read_text(encoding="utf-8").strip()
    if text.startswith('"'):
        text = json.loads(text)
    return text


def _minutes(s: str) -> int:
    h = re.search(r"(\d+)h", s)
    m = re.search(r"(\d+)\s*min", s)
    return (int(h[1]) * 60 if h else 0) + (int(m[1]) if m else 0)


def parse_overview(text: str) -> dict:
    nights, cur = {}, None
    for line in text.splitlines():
        line = line.strip()
        m = _DATE.match(line)
        if m:
            cur = nights.setdefault(m[1], {})
            continue
        if cur is None or ":" not in line:
            continue
        key, val = (p.strip() for p in line.split(":", 1))
        pct = re.match(r"(\d+)%", val)
        if key == "Sleep Score":
            cur["score"] = int(val)
        elif key.startswith("Main Sleep (asleep)"):
            cur["asleep_min"] = _minutes(val)
        elif key.startswith("Main Sleep Period"):
            cur["in_bed_min"] = _minutes(val)
        elif key == "Deep Sleep Ratio" and pct:
            cur["deep_pct"] = int(pct[1])
        elif key == "Light Sleep Ratio" and pct:
            cur["light_pct"] = int(pct[1])
        elif key == "REM Ratio" and pct:
            cur["rem_pct"] = int(pct[1])
        elif key == "Awake Time":
            cur["awake_min"] = _minutes(val)
        elif key.startswith("Awake Count"):
            cur["awake_count"] = int(val)
        elif key.startswith("Naps Total"):
            cur["nap_min"] = _minutes(val)
        elif key == "Main Sleep Window":
            w = re.findall(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})", val)
            if len(w) == 2:
                cur["bed"], cur["wake"] = f"{w[0][0]}T{w[0][1]}", f"{w[1][0]}T{w[1][1]}"
    return nights


def parse_hrv(text: str) -> tuple[dict, list]:
    """→ ({Datum: Tagesbewertung}, [(lokale Zeit, hrv), …])."""
    days, cur = {}, None
    head, _, series = text.partition("Sleep HRV Time Series")
    for line in head.splitlines():
        line = line.strip()
        m = _DATE.match(line)
        if m:
            cur = days.setdefault(m[1], {})
            continue
        if cur is None:
            continue
        if m := re.match(r"HRV Avg:\s*(\d+)\s*ms\s*[—-]\s*(.+)", line):
            cur["hrv"], cur["hrv_status"] = int(m[1]), m[2].strip()
        elif m := re.match(r"Normal Range:\s*(\d+)\s*-\s*(\d+)", line):
            cur["hrv_low"], cur["hrv_high"] = int(m[1]), int(m[2])
        elif m := re.match(r"Baseline:\s*(\d+)", line):
            cur["hrv_baseline"] = int(m[1])
    points = []
    for m in re.finditer(r"timestamp=(\d+), timezone=(-?\d+), hrv=(\d+)", series):
        tz = timezone(timedelta(minutes=15 * int(m[2])))   # COROS: Zeitzone in 15-min-Einheiten
        local = datetime.fromtimestamp(int(m[1]), tz).replace(tzinfo=None)
        points.append((local, int(m[3])))
    return days, points


def parse_rhr(text: str) -> dict:
    return {m[1]: {"rhr": int(m[2])}
            for m in re.finditer(r"^\s*(\d{4}-\d{2}-\d{2}):\s*(\d+)\s*bpm", text, re.M)}


def parse_daily(text: str) -> dict:
    """Schritte, Stress-Ø und Schlaf-HF je Tag (Abschnitte `--- yyyyMMdd ---`)."""
    days = {}
    for m in re.finditer(r"---\s*(\d{4})(\d{2})(\d{2})\s*---(.*?)(?=---\s*\d{8}\s*---|\Z)", text, re.S):
        d, body, vals = f"{m[1]}-{m[2]}-{m[3]}", m[4], {}
        if s := re.search(r"Steps:\s*([\d,.]+)", body):
            vals["steps"] = int(re.sub(r"[,.]", "", s[1]))
        if s := re.search(r"Stress:\s*Avg\s*(\d+)", body):
            vals["stress_avg"] = int(s[1])
        if s := re.search(r"Sleep HR:\s*Avg\s*(\d+)\s*bpm\s*\|\s*Min\s*(\d+)", body):
            vals["sleep_hr_avg"], vals["sleep_hr_min"] = int(s[1]), int(s[2])
        days[d] = vals
    return days


def night_split(night: dict, points: list) -> dict:
    """HRV-Schnitt der ersten 2h nach dem Einschlafen vs. Rest der Nacht."""
    if "bed" not in night or "wake" not in night:
        return {}
    bed, wake = datetime.fromisoformat(night["bed"]), datetime.fromisoformat(night["wake"])
    cut = bed + timedelta(minutes=EARLY_MIN)
    early = [h for t, h in points if bed <= t < cut]
    late  = [h for t, h in points if cut <= t <= wake]
    if len(early) < 3 or len(late) < 3:
        return {}
    return {"hrv_early": round(sum(early) / len(early)), "hrv_late": round(sum(late) / len(late))}


def merge(store: dict, overview: dict, hrv_days: dict, points: list, *extra: dict) -> dict:
    days = store.setdefault("days", {})
    fetched = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for source in (overview, hrv_days, *extra):
        for d, vals in source.items():
            days.setdefault(d, {}).update(vals, fetched=fetched)
    for day in days.values():
        day.update(night_split(day, points))
    cutoff = (datetime.now() - timedelta(days=KEEP_DAYS)).date().isoformat()
    store["days"] = {d: days[d] for d in sorted(days) if d >= cutoff}
    store["updated"] = fetched
    return store


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--overview", help="Ausgabe von querySleepOverview")
    ap.add_argument("--hrv", help="Ausgabe von querySleepHrv")
    ap.add_argument("--rhr", help="Ausgabe von queryRestingHeartRate")
    ap.add_argument("--daily", help="Ausgabe von queryDailyHealthData")
    ap.add_argument("--out", default=str(DATA_FILE))
    args = ap.parse_args()

    overview = parse_overview(_read(args.overview)) if args.overview else {}
    hrv_days, points = parse_hrv(_read(args.hrv)) if args.hrv else ({}, [])
    rhr   = parse_rhr(_read(args.rhr)) if args.rhr else {}
    daily = parse_daily(_read(args.daily)) if args.daily else {}
    if not (overview or hrv_days or rhr or daily):
        raise SystemExit("Keine Tage erkannt – MCP-Ausgaben prüfen")

    out = Path(args.out)
    store = json.loads(out.read_text()) if out.exists() else {}
    merge(store, overview, hrv_days, points, rhr, daily)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(store, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for d in sorted(set(overview) | set(hrv_days) | set(rhr) | set(daily)):
        print(d, store["days"].get(d, "(älter als Aufbewahrung)"))


if __name__ == "__main__":
    main()
