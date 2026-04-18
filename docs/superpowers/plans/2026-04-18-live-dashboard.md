# Live Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the static `dashboard.html` to a live PWA that auto-updates from intervals.icu whenever a workout is uploaded.

**Architecture:** A Python script (`generate.py`) reads the weekly coaching plan from `planung/kw{N}.md` and fetches live data from the intervals.icu API, then renders `dashboard.template.html` into `docs/dashboard.html`. GitHub Actions runs this script on a daily schedule and on every `repository_dispatch` event (fired by the intervals.icu webhook). GitHub Pages serves `docs/` as the PWA.

**Tech Stack:** Python 3.11+, requests, Jinja2, pytest, GitHub Actions, GitHub Pages

---

## File Structure

| File | Action | Purpose |
|---|---|---|
| `requirements.txt` | Create | Python deps: requests, jinja2 |
| `generate.py` | Create | All generation logic (API client, parser, builder, renderer) |
| `dashboard.template.html` | Create | Jinja2 template (converted from dashboard.html) |
| `tests/test_generate.py` | Create | Unit tests for pure functions |
| `.github/workflows/build.yml` | Create | GitHub Actions workflow |
| `docs/.gitkeep` | Create | Ensures docs/ is tracked in git |
| `docs/manifest.json` | Create | Copy of manifest.json for GitHub Pages |
| `docs/sw.js` | Create | Copy of sw.js for GitHub Pages |
| `docs/icon.svg` | Create | Copy of icon.svg for GitHub Pages |
| `dashboard.html` | Keep | Stays as source of truth / local preview |
| `sw.js` | Keep | Unchanged |
| `manifest.json` | Keep | Unchanged |

---

## Task 1: Project Setup

**Files:**
- Create: `requirements.txt`
- Create: `tests/__init__.py`
- Create: `docs/.gitkeep`

- [ ] **Step 1: Create requirements.txt**

```
requests==2.32.3
jinja2==3.1.4
pytest==8.3.4
```

- [ ] **Step 2: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: Successfully installed requests jinja2 pytest (plus deps)

- [ ] **Step 3: Create test module init**

```bash
mkdir -p tests docs
touch tests/__init__.py docs/.gitkeep
```

- [ ] **Step 4: Verify intervals.icu API field names (discovery)**

Create a temporary `discover_api.py`, run it once, then delete it:

```python
#!/usr/bin/env python3
"""Run once to discover real API field names. Delete after use."""
import os, base64, json, requests
from datetime import date, timedelta

API_KEY = os.environ["INTERVALS_API_KEY"]
ATHLETE_ID = os.environ["INTERVALS_ATHLETE_ID"]
BASE = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}"
AUTH = "Basic " + base64.b64encode(f"API_KEY:{API_KEY}".encode()).decode()
H = {"Authorization": AUTH}

today = date.today()
monday = today - timedelta(days=today.weekday())
oldest = monday.isoformat()
newest = today.isoformat()

print("=== WELLNESS (last 7 days) ===")
r = requests.get(f"{BASE}/wellness?oldest={(today-timedelta(7)).isoformat()}&newest={today.isoformat()}", headers=H)
data = r.json()
if data:
    print(json.dumps(data[-1], indent=2))  # latest entry

print("\n=== ACTIVITIES (this week) ===")
r = requests.get(f"{BASE}/activities?oldest={oldest}&newest={newest}", headers=H)
data = r.json()
if data:
    print(json.dumps(data[0], indent=2))  # first activity
```

Run: `INTERVALS_API_KEY=xxx INTERVALS_ATHLETE_ID=xxx python discover_api.py`
Expected: JSON output showing actual field names for wellness and activities. Note down the exact field names for HRV, sleep, resting HR, TSS, and activity type.

- [ ] **Step 5: Delete discovery script, commit**

```bash
rm discover_api.py
git add requirements.txt tests/__init__.py docs/.gitkeep
git commit -m "chore: python project setup for live dashboard"
```

---

## Task 2: API Client + Pure Utilities

**Files:**
- Create: `generate.py` (initial skeleton with API functions)
- Create: `tests/test_generate.py` (pure function tests)

- [ ] **Step 1: Write failing tests for pure utility functions**

```python
# tests/test_generate.py
import pytest
from datetime import date
from generate import calc_ring_offset, calc_readiness, week_date_range, fmt_tsb_color

def test_ring_offset_full():
    # 100% → offset 0
    assert calc_ring_offset(100, 100, 345.4) == pytest.approx(0, abs=1)

def test_ring_offset_half():
    # 50% → offset = 345.4 * 0.5 ≈ 173
    assert calc_ring_offset(50, 100, 345.4) == pytest.approx(172.7, abs=1)

def test_ring_offset_zero():
    # 0% → offset = circumference
    assert calc_ring_offset(0, 100, 345.4) == pytest.approx(345.4, abs=1)

def test_readiness_high():
    score = calc_readiness(hrv=45, hrv_7d_avg=42, sleep_secs=28800, tsb=20)
    assert score >= 80

def test_readiness_low():
    score = calc_readiness(hrv=28, hrv_7d_avg=42, sleep_secs=18000, tsb=-15)
    assert score < 60

def test_week_date_range():
    monday, sunday = week_date_range(16, 2026)
    assert monday == date(2026, 4, 13)
    assert sunday == date(2026, 4, 19)

def test_tsb_color_positive():
    assert fmt_tsb_color(15) == "#3ecf8e"   # green

def test_tsb_color_negative():
    assert fmt_tsb_color(-15) == "#ef4444"  # red
```

- [ ] **Step 2: Run tests to confirm they fail**

Run: `pytest tests/test_generate.py -v`
Expected: `ModuleNotFoundError: No module named 'generate'`

- [ ] **Step 3: Create generate.py with API client and pure functions**

```python
#!/usr/bin/env python3
import os, base64, math
from datetime import date, timedelta
import requests

# ── Config ──────────────────────────────────────────────────────────────────
API_KEY     = os.environ.get("INTERVALS_API_KEY", "")
ATHLETE_ID  = os.environ.get("INTERVALS_ATHLETE_ID", "")
BASE_URL    = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}"
AUTH        = "Basic " + base64.b64encode(f"API_KEY:{API_KEY}".encode()).decode()
CIRC_OUTER  = 2 * math.pi * 55   # ≈ 345.4 (r=55 ring)
CIRC_INNER  = 2 * math.pi * 41   # ≈ 257.6 (r=41 ring)

# ── Pure utilities ───────────────────────────────────────────────────────────

def calc_ring_offset(value: float, max_value: float, circumference: float) -> float:
    """SVG stroke-dashoffset for a ring at value/max_value fill."""
    pct = min(max(value / max_value, 0), 1)
    return round(circumference * (1 - pct), 1)

def calc_readiness(hrv: float, hrv_7d_avg: float, sleep_secs: float, tsb: float) -> int:
    """Composite readiness score 0–100. Weights: HRV 40%, Sleep 35%, TSB 25%."""
    hrv_score   = min(hrv / hrv_7d_avg, 1.25) / 1.25 * 100 if hrv_7d_avg else 50
    sleep_score = min(sleep_secs / (8 * 3600), 1.0) * 100
    tsb_score   = min(max((tsb + 30) / 60, 0), 1) * 100
    return round(hrv_score * 0.40 + sleep_score * 0.35 + tsb_score * 0.25)

def week_date_range(kw: int, year: int) -> tuple[date, date]:
    """Returns (monday, sunday) for ISO week kw in year."""
    monday = date.fromisocalendar(year, kw, 1)
    return monday, monday + timedelta(days=6)

def fmt_tsb_color(tsb: float) -> str:
    if tsb >= 5:   return "#3ecf8e"  # green
    if tsb >= -5:  return "#f5a623"  # yellow
    return "#ef4444"                 # red

def readiness_label(score: int) -> str:
    if score >= 80: return "🟢 Voll trainieren"
    if score >= 60: return "🟡 Normal trainieren"
    if score >= 40: return "🟠 Reduziert trainieren"
    return "🔴 Ruhetag empfohlen"

def readiness_color(score: int) -> str:
    if score >= 80: return "#3ecf8e"
    if score >= 60: return "#f5a623"
    return "#ef4444"

# ── API client ───────────────────────────────────────────────────────────────

def _api_get(path: str) -> list | dict:
    r = requests.get(f"{BASE_URL}{path}", headers={"Authorization": AUTH}, timeout=15)
    r.raise_for_status()
    return r.json()

def get_wellness(oldest: str, newest: str) -> list[dict]:
    return _api_get(f"/wellness?oldest={oldest}&newest={newest}")

def get_activities(oldest: str, newest: str) -> list[dict]:
    return _api_get(f"/activities?oldest={oldest}&newest={newest}")
```

- [ ] **Step 4: Run tests — should pass now**

Run: `pytest tests/test_generate.py -v`
Expected: 7 tests PASSED

- [ ] **Step 5: Commit**

```bash
git add generate.py tests/test_generate.py
git commit -m "feat: api client and pure utility functions with tests"
```

---

## Task 3: KW Markdown Parser

**Files:**
- Modify: `generate.py` (add `parse_kw_plan`)
- Modify: `tests/test_generate.py` (add parser tests)

- [ ] **Step 1: Write failing tests for the parser**

Add to `tests/test_generate.py`:

```python
from generate import parse_kw_plan

def test_parse_kw_plan_days():
    plan = parse_kw_plan(16)
    assert len(plan["days"]) == 7

def test_parse_kw_plan_tss():
    plan = parse_kw_plan(16)
    assert plan["tss_plan"] == 493

def test_parse_kw_plan_monday():
    plan = parse_kw_plan(16)
    mo = plan["days"][0]
    assert mo["tag"] == "Mo"
    assert mo["workout"] == "LIT-2h"
    assert mo["tss_plan"] == 74

def test_parse_kw_plan_rest_day():
    plan = parse_kw_plan(16)
    mi = plan["days"][2]
    assert mi["tag"] == "Mi"
    assert mi["rest"] is True

def test_parse_kw_plan_theme():
    plan = parse_kw_plan(16)
    assert "Grundlagen" in plan["theme"]
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `pytest tests/test_generate.py::test_parse_kw_plan_days -v`
Expected: FAIL with `ImportError` or `AttributeError`

- [ ] **Step 3: Implement parse_kw_plan in generate.py**

Add after the API client section:

```python
import re
from pathlib import Path

DAY_ORDER = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

def parse_kw_plan(kw: int) -> dict:
    """Parse planung/kw{kw}.md → {theme, tss_plan, days: list[dict]}"""
    path = Path(f"planung/kw{kw}.md")
    if not path.exists():
        return {"theme": f"KW{kw}", "tss_plan": 0, "days": _empty_days()}

    text = path.read_text(encoding="utf-8")

    # Theme from heading: "# KW16 – Grundlagenblock Start" → "Grundlagenblock Start"
    m = re.search(r"^#\s+KW\d+\s+[-–]\s+(.+)$", text, re.MULTILINE)
    theme = m.group(1).strip() if m else f"KW{kw}"

    # Sub from "*Thema: ...*" line
    m_sub = re.search(r"^\*Thema:\s*(.+?)\*$", text, re.MULTILINE)
    sub = m_sub.group(1).strip() if m_sub else ""

    # Parse markdown table rows (skip header rows with ---|--- or Tag)
    table_rows = re.findall(
        r"^\|\s*(Mo|Di|Mi|Do|Fr|Sa|So|\*\*Total\*\*)\s*\|(.+)$",
        text, re.MULTILINE
    )

    days = []
    tss_plan_total = 0

    for tag, rest in table_rows:
        if tag == "**Total**":
            # Extract total TSS: | | | **~493** | ... → 493
            m = re.search(r"\*\*~?(\d+)\*\*", rest)
            if m:
                tss_plan_total = int(m.group(1))
            continue

        cols = [c.strip() for c in rest.split("|")]
        # cols: [workout, datei, tss_soll, tss_ist, status, notiz, ...]
        workout = cols[0] if len(cols) > 0 else ""
        tss_soll_raw = cols[2] if len(cols) > 2 else "–"
        status = cols[4] if len(cols) > 4 else "–"

        # Parse TSS: "~50" → 50, "–" → 0
        tss_plan = 0
        m = re.search(r"(\d+)", tss_soll_raw)
        if m:
            tss_plan = int(m.group(1))

        # Detect run: workout starts with 🏃 or contains "Lauf"
        is_run  = "🏃" in workout or "Lauf" in workout.lower()
        is_rest = workout.strip() in ("Ruhetag", "–", "")

        # Strip emoji prefix from workout name for clean display
        workout_clean = re.sub(r"^[🚴🏃💪🧘]\s*", "", workout).strip()

        days.append({
            "tag":       tag,
            "workout":   workout_clean,
            "tss_plan":  tss_plan,
            "status":    status,   # "✅", "❌", "–"
            "rest":      is_rest,
            "is_run":    is_run,
        })

    # Ensure all 7 days present (some kw files might be incomplete)
    present = {d["tag"] for d in days}
    for t in DAY_ORDER:
        if t not in present:
            days.append({"tag": t, "workout": "", "tss_plan": 0,
                         "status": "–", "rest": False, "is_run": False})
    days.sort(key=lambda d: DAY_ORDER.index(d["tag"]))

    return {"theme": theme, "sub": sub, "tss_plan": tss_plan_total, "days": days}

def _empty_days() -> list[dict]:
    return [{"tag": t, "workout": "", "tss_plan": 0, "status": "–",
             "rest": t == "Mi", "is_run": False} for t in DAY_ORDER]
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_generate.py -v`
Expected: all tests PASSED

- [ ] **Step 5: Commit**

```bash
git add generate.py tests/test_generate.py
git commit -m "feat: kw markdown parser with tests"
```

---

## Task 4: Data Builder

**Files:**
- Modify: `generate.py` (add `build_context`, `match_activities`)
- Modify: `tests/test_generate.py` (add builder tests)

- [ ] **Step 1: Write failing tests**

Add to `tests/test_generate.py`:

```python
from generate import match_activities, build_day_rows

SAMPLE_ACTIVITIES = [
    {"start_date_local": "2026-04-14T09:00:00", "type": "Ride",
     "icu_training_load": 71, "name": "Morgenfahrt"},
    {"start_date_local": "2026-04-16T18:00:00", "type": "Run",
     "icu_training_load": 48, "name": "Lauf"},
]
SAMPLE_PLAN_DAYS = [
    {"tag": "Mo", "workout": "LIT-2h", "tss_plan": 74, "status": "❌",
     "rest": False, "is_run": False},
    {"tag": "Di", "workout": "SwSp 3×10", "tss_plan": 72, "status": "❌",
     "rest": False, "is_run": False},
    {"tag": "Mi", "workout": "Ruhetag", "tss_plan": 0, "status": "–",
     "rest": True, "is_run": False},
    {"tag": "Do", "workout": "Lauf 2×8min", "tss_plan": 50, "status": "❌",
     "rest": False, "is_run": True},
]

def test_match_activities_monday():
    from datetime import date
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    assert matched["Mo"]["tss_ist"] == 71
    assert matched["Mo"]["done"] is True

def test_match_activities_run():
    from datetime import date
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    assert matched["Do"]["tss_ist"] == 48
    assert matched["Do"]["done"] is True

def test_match_activities_no_activity():
    from datetime import date
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    assert matched["Di"]["done"] is False
    assert matched["Di"]["tss_ist"] == 0

def test_build_day_rows():
    from datetime import date
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    rows = build_day_rows(SAMPLE_PLAN_DAYS, matched)
    mo = rows[0]
    assert mo["tag"] == "Mo"
    assert mo["tss_ist"] == 71
    assert mo["done"] is True
    assert mo["rest"] is False
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `pytest tests/test_generate.py::test_match_activities_monday -v`
Expected: FAIL with ImportError

- [ ] **Step 3: Implement match_activities and build_day_rows**

Add to `generate.py`:

```python
from datetime import date, timedelta

SPORT_TYPE_MAP = {
    "Ride": "ride", "VirtualRide": "ride", "GravelRide": "ride",
    "Run":  "run",  "TrailRun": "run",
    "WeightTraining": "strength", "Workout": "strength",
}

def match_activities(activities: list[dict], plan_days: list[dict],
                     monday: date) -> dict[str, dict]:
    """Match activities to plan days by date + sport type.
    Returns {tag: {tss_ist, done, activity_name}}"""
    # Build date → day-tag lookup
    date_to_tag = {
        (monday + timedelta(days=i)).isoformat(): DAY_ORDER[i]
        for i in range(7)
    }

    matched: dict[str, dict] = {
        d["tag"]: {"tss_ist": 0, "done": False, "activity_name": ""}
        for d in plan_days
    }

    for act in activities:
        act_date = act.get("start_date_local", "")[:10]
        tag = date_to_tag.get(act_date)
        if not tag:
            continue
        tss = act.get("icu_training_load") or 0
        # Accumulate TSS (multiple activities same day)
        matched[tag]["tss_ist"] += tss
        matched[tag]["done"] = True
        if not matched[tag]["activity_name"]:
            matched[tag]["activity_name"] = act.get("name", "")

    return matched

def build_day_rows(plan_days: list[dict], matched: dict[str, dict]) -> list[dict]:
    """Merge plan + matched activity data into display rows."""
    rows = []
    for day in plan_days:
        tag = day["tag"]
        m = matched.get(tag, {"tss_ist": 0, "done": False, "activity_name": ""})
        done = m["done"]
        rest = day["rest"]

        # Dot class for coloured indicator
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

        # Row class
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
```

- [ ] **Step 4: Run all tests**

Run: `pytest tests/test_generate.py -v`
Expected: all tests PASSED

- [ ] **Step 5: Commit**

```bash
git add generate.py tests/test_generate.py
git commit -m "feat: activity matcher and day row builder with tests"
```

---

## Task 5: dashboard.template.html

**Files:**
- Create: `dashboard.template.html` (converted from `dashboard.html`)

This is the largest single step. Convert every hardcoded value to a Jinja2 placeholder. The visual output must be identical to the current dashboard.

- [ ] **Step 1: Copy dashboard.html as base**

```bash
cp dashboard.html dashboard.template.html
```

- [ ] **Step 2: Replace header values**

Find and replace in `dashboard.template.html`:

| Find | Replace |
|---|---|
| `Grundlagenblock` (in phase-pill) | `{{ phase_name }}` |
| `KW16` (in header-sub) | `KW{{ kw }}` |
| `14.–20. April 2026` | `{{ kw_dates }}` |

- [ ] **Step 3: Replace countdown (countdowns are calculated in JS — keep JS, update race dates if needed)**

The countdown JS already reads from hardcoded dates. These dates don't change, so leave the countdown JS as-is.

- [ ] **Step 4: Replace phase bar**

Replace the entire `<div class="phases">` block with:

```html
<div class="phases">
  {% for phase in phases %}
  <div class="phase {{ phase.state }}">
    {% if phase.state == 'done' %}✓ {% elif phase.state == 'active' %}◉ {% endif %}{{ phase.name }}<div class="kw">{{ phase.kw }}</div>
  </div>
  {% endfor %}
</div>
```

- [ ] **Step 5: Replace Recovery ring**

```html
<!-- Recovery ring -->
<circle cx="65" cy="65" r="55" fill="none" stroke="{{ readiness_color }}" stroke-width="10" stroke-linecap="round"
  stroke-dasharray="345.4" stroke-dashoffset="{{ readiness_offset }}" transform="rotate(-90 65 65)"/>
...
<span class="ring-num" style="color:{{ readiness_color }}">{{ readiness_score }}</span>
...
<div class="ring-status-tag">{{ readiness_label }}</div>
<div class="ring-status-sub">{{ readiness_sub }}</div>
```

- [ ] **Step 6: Replace Trainingsform ring**

```html
<circle ... stroke-dashoffset="{{ ctl_offset }}" .../>
<circle ... stroke-dashoffset="{{ atl_offset }}" .../>
...
<span class="ring-num" style="color:{{ tsb_color }};font-size:1.8rem">{{ tsb_display }}</span>
...
<span class="dl-val" style="color:#4f8ef7">{{ ctl }} <span ...>/ 90</span></span>
<span class="dl-val" style="color:#f5a623">{{ atl }}</span>
```

- [ ] **Step 7: Replace Saisonfortschritt ring**

```html
<circle ... stroke-dashoffset="{{ season_offset }}" .../>
...
<span class="ring-num" style="color:#9b7fe8;font-size:1.8rem">KW{{ season_kw_current }}</span>
<span class="ring-sub">von {{ season_kw_total }}</span>
...
<div class="pri-main">◉ {{ phase_name }}</div>
<div class="pri-sub">Nächste Phase: {{ next_phase }}</div>
```

- [ ] **Step 8: Replace week header and day rows**

Replace the week TSS pill:
```html
<span class="tss-pill">{{ tss_ist }} / ~{{ tss_plan }} TSS</span>
```

Replace all day rows with a Jinja2 loop:
```html
{% if sick_notice %}
<div class="sick-notice">🤒 <div><strong>{{ sick_notice }}</strong></div></div>
{% endif %}

{% for day in days %}
<div class="day-row {% if day.done %}day-done{% elif day.rest %}{% else %}{{ day.row_class }}{% endif %}">
  <span class="day-name">{{ day.tag }}</span>
  <span class="day-dot {{ day.dot_class }}"></span>
  <div>
    {% if day.rest %}
    <div class="day-workout" style="color:var(--subtle);font-weight:400;">Ruhetag</div>
    {% else %}
    <div class="day-workout">
      {% if day.is_run %}🏃{% else %}🚴{% endif %} {{ day.workout }}
    </div>
    {% endif %}
  </div>
  {% if day.rest %}
  <span class="day-tss" style="color:var(--subtle)">–</span>
  {% elif day.done %}
  <span class="day-tss" style="color:var(--green)">✅ {{ day.tss_ist }} TSS</span>
  {% else %}
  <span class="day-tss">{% if day.tss_plan > 0 %}❌ 0 TSS{% else %}–{% endif %}</span>
  {% endif %}
</div>
{% endfor %}
```

- [ ] **Step 9: Replace readiness card**

```html
<div class="readiness-score" style="color:{{ readiness_color }}">{{ readiness_score }}</div>
<div class="readiness-tag" style="color:{{ readiness_color }}">{{ readiness_label }}</div>
<div class="readiness-sub">{{ readiness_sub }}</div>

<!-- HRV -->
<div class="rbar-row">
  <span class="rbar-lbl">HRV</span>
  <div class="rbar-track"><div class="rbar-fill" style="width:{{ hrv_pct }}%;background:{{ hrv_color }}"></div></div>
  <span class="rbar-val">{{ hrv_val }}</span>
</div>
<!-- Schlaf -->
<div class="rbar-row">
  <span class="rbar-lbl">Schlaf</span>
  <div class="rbar-track"><div class="rbar-fill" style="width:{{ sleep_pct }}%;background:{{ sleep_color }}"></div></div>
  <span class="rbar-val">{{ sleep_val }}</span>
</div>
<!-- TSB -->
<div class="rbar-row">
  <span class="rbar-lbl">TSB</span>
  <div class="rbar-track"><div class="rbar-fill" style="width:{{ tsb_bar_pct }}%;background:{{ tsb_bar_color }}"></div></div>
  <span class="rbar-val">{{ tsb_bar_val }}</span>
</div>
<!-- Puls -->
<div class="rbar-row">
  <span class="rbar-lbl">Puls</span>
  <div class="rbar-track"><div class="rbar-fill" style="width:{{ pulse_pct }}%;background:{{ pulse_color }}"></div></div>
  <span class="rbar-val">{{ pulse_val }}</span>
</div>

<!-- Sparkline -->
<div class="sparkline">
  {% for bar in sparkline %}
  <div class="spark-bar {% if loop.last %}spark-today{% endif %}" style="height:{{ bar.pct }}%;background:{{ bar.color }}"></div>
  {% endfor %}
</div>
```

- [ ] **Step 10: Replace polarisation card**

```html
<div class="section-label">Polarisation · KW{{ kw - 1 }} · Rad</div>
<span class="pi-badge {% if polar_ok %}pi-ok{% else %}pi-warn{% endif %}">
  PI: {{ polar_pi }}% · {% if polar_ok %}✅ Grüner Bereich{% else %}⚠️ Zu viel Z3{% endif %}
</span>
<div class="polar-row">
  <span class="polar-lbl">Z1–Z2</span>
  <div class="polar-track"><div class="polar-fill" style="width:{{ polar_z12_pct }}%;background:#3a7a4a"></div></div>
  <span class="polar-pct" style="color:var(--green)">{{ polar_z12_pct }}%</span>
</div>
<div class="polar-row">
  <span class="polar-lbl">Z3</span>
  <div class="polar-track"><div class="polar-fill" style="width:{{ polar_z3_pct }}%;background:#7a6a2a"></div></div>
  <span class="polar-pct">{{ polar_z3_pct }}%</span>
</div>
<div class="polar-row">
  <span class="polar-lbl">Z4–Z7</span>
  <div class="polar-track"><div class="polar-fill" style="width:{{ polar_z47_pct }}%;background:#7040a0"></div></div>
  <span class="polar-pct" style="color:var(--subtle)">{{ polar_z47_pct }}%</span>
</div>
```

- [ ] **Step 11: Replace 4-week outlook table rows**

```html
{% for week in outlook %}
<tr {% if loop.first %}style="background:rgba(79,142,247,0.05)"{% endif %}>
  <td><span class="ausblick-kw" style="color:{% if loop.first %}var(--accent){% else %}var(--muted){% endif %}">KW{{ week.kw }}</span></td>
  <td>
    <div>{{ week.theme }}</div>
    <div class="ausblick-sub">{{ week.sub }}</div>
  </td>
  <td class="ausblick-tss" {% if loop.first and week.tss_ist == 0 %}style="color:var(--red)"{% endif %}>
    {% if loop.first %}{{ week.tss_ist }} / ~{{ week.tss_plan }}{% else %}~{{ week.tss_plan }}{% endif %}
  </td>
  <td><div class="ausblick-sub">{{ week.key_workouts }}</div></td>
</tr>
{% endfor %}
```

- [ ] **Step 12: Replace footer**

```html
<footer>Stefan · Coaching Dashboard · FTP 305W (Sentiero) · KW{{ kw }} · Powered by Claude Code</footer>
```

- [ ] **Step 13: Add JS password protection (before closing `</body>`)**

```html
<script>
(function() {
  var PASS = "coaching2026";
  var key  = "coach_auth";
  if (localStorage.getItem(key) !== PASS) {
    var input = prompt("Passwort:");
    if (input !== PASS) {
      document.body.innerHTML = "";
      return;
    }
    localStorage.setItem(key, PASS);
  }
})();
</script>
```

> **Note:** Change `"coaching2026"` to a password of your choice before deploying.

- [ ] **Step 14: Verify template renders locally (no commit yet — do in Task 6)**

---

## Task 6: Renderer + Main Script

**Files:**
- Modify: `generate.py` (add `build_context`, `render`, `main`)

- [ ] **Step 1: Write failing integration test**

Add to `tests/test_generate.py`:

```python
from unittest.mock import patch
from generate import build_context

MOCK_WELLNESS = [
    {"id": "2026-04-12", "hrv": 40, "sleepSecs": 25200, "ctl": 42.0, "atl": 38.0, "restingHR": 50},
    {"id": "2026-04-13", "hrv": 43, "sleepSecs": 27000, "ctl": 42.5, "atl": 37.0, "restingHR": 49},
    {"id": "2026-04-14", "hrv": 45, "sleepSecs": 28800, "ctl": 43.0, "atl": 36.0, "restingHR": 48},
]
MOCK_ACTIVITIES = []

@patch("generate.get_wellness", return_value=MOCK_WELLNESS)
@patch("generate.get_activities", return_value=MOCK_ACTIVITIES)
def test_build_context_keys(mock_act, mock_well):
    from datetime import date
    ctx = build_context(kw=16, monday=date(2026, 4, 13), sunday=date(2026, 4, 19))
    required_keys = [
        "kw", "kw_dates", "phase_name", "readiness_score", "readiness_color",
        "ctl", "atl", "tsb_display", "ctl_offset", "atl_offset",
        "tss_ist", "tss_plan", "days", "sparkline", "outlook",
        "phases", "polar_z12_pct", "polar_z3_pct", "polar_z47_pct",
    ]
    for key in required_keys:
        assert key in ctx, f"Missing key: {key}"
```

- [ ] **Step 2: Run test to confirm failure**

Run: `pytest tests/test_generate.py::test_build_context_keys -v`
Expected: FAIL with ImportError

- [ ] **Step 3: Implement build_context in generate.py**

```python
from jinja2 import Environment, FileSystemLoader

# Season phases — static, aligned with periodisierung.md
SEASON_PHASES = [
    {"name": "Baseline",   "kw": "KW14",    "start_kw": 14, "end_kw": 14},
    {"name": "Urlaub",     "kw": "KW15",    "start_kw": 15, "end_kw": 15},
    {"name": "Grundlage",  "kw": "KW16–17", "start_kw": 16, "end_kw": 17},
    {"name": "HIT-Aufbau", "kw": "KW18–21", "start_kw": 18, "end_kw": 21},
    {"name": "TT-Spezifik","kw": "KW22",    "start_kw": 22, "end_kw": 22},
    {"name": "Tapering",   "kw": "KW23",    "start_kw": 23, "end_kw": 23},
    {"name": "🏁 RadRace", "kw": "KW24",    "start_kw": 24, "end_kw": 24},
    {"name": "Erholung",   "kw": "KW25",    "start_kw": 25, "end_kw": 25},
    {"name": "🗺️ Rosen.", "kw": "KW26",    "start_kw": 26, "end_kw": 26},
]
RACE_KW = 24  # RadRace

MONTH_DE = ["", "Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
            "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

def build_context(kw: int, monday: date, sunday: date) -> dict:
    oldest = monday.isoformat()
    newest = sunday.isoformat()

    wellness  = get_wellness(f"{(monday - timedelta(7)).isoformat()}", newest)
    activities = get_activities(oldest, newest)

    # Latest wellness entry
    today_w = wellness[-1] if wellness else {}
    hrv     = today_w.get("hrv") or 0
    sleep_s = today_w.get("sleepSecs") or 0
    ctl     = today_w.get("ctl") or 0
    atl     = today_w.get("atl") or 0
    tsb     = round(ctl - atl, 1)
    rhr     = today_w.get("restingHR") or 60

    # HRV 7-day average for normalisation
    hrv_7d  = [w.get("hrv") or 0 for w in wellness if w.get("hrv")]
    hrv_avg = (sum(hrv_7d) / len(hrv_7d)) if hrv_7d else hrv or 40

    # Readiness
    r_score = calc_readiness(hrv=hrv, hrv_7d_avg=hrv_avg,
                             sleep_secs=sleep_s, tsb=tsb)
    r_color = readiness_color(r_score)
    r_label = readiness_label(r_score)
    r_sub   = _readiness_sub(rhr, hrv, hrv_avg, wellness)

    # Rings
    ctl_offset    = calc_ring_offset(ctl, 90, CIRC_OUTER)
    atl_offset    = calc_ring_offset(atl, 60, CIRC_INNER)
    r_offset      = calc_ring_offset(r_score, 100, CIRC_OUTER)
    season_pos    = kw - 14              # weeks since start (KW14=0)
    season_total  = RACE_KW - 14 + 1    # KW14–KW24 = 11 weeks
    season_offset = calc_ring_offset(season_pos, season_total, CIRC_OUTER)

    # Phase
    current_phase = next(
        (p for p in SEASON_PHASES if p["start_kw"] <= kw <= p["end_kw"]),
        SEASON_PHASES[0]
    )
    next_phase_obj = next(
        (p for p in SEASON_PHASES if p["start_kw"] > kw), None
    )
    next_phase = f"{next_phase_obj['name']} ab KW{next_phase_obj['start_kw']}" if next_phase_obj else ""

    phases = [
        {**p, "state": "done" if p["end_kw"] < kw
                         else "active" if p["start_kw"] <= kw <= p["end_kw"]
                         else "upcoming"}
        for p in SEASON_PHASES
    ]

    # Plan
    plan = parse_kw_plan(kw)
    matched = match_activities(activities, plan["days"], monday)
    days = build_day_rows(plan["days"], matched)

    tss_ist = sum(d["tss_ist"] for d in days)

    # Sick notice (detect from kw file status column)
    sick_days = [d for d in days if not d["done"] and not d["rest"] and _is_past(d["tag"])]
    sick_notice = ""
    if sick_days and all(not d["done"] for d in days if not d["rest"]):
        sick_notice = f"Krank – alle Einheiten ausgefallen (Details in kw{kw}.md)"

    # Readiness bars
    hrv_pct   = min(round(hrv / hrv_avg * 100), 100) if hrv_avg else 0
    sleep_h   = sleep_s / 3600 if sleep_s else 0
    sleep_pct = min(round(sleep_h / 8 * 100), 100)
    tsb_pct   = min(max(round((tsb + 30) / 60 * 100), 0), 100)
    rhr_baseline = 50  # rough baseline; improve after collecting data
    pulse_pct = max(0, min(100, round((1 - (rhr - rhr_baseline) / 20) * 100)))

    def bar_color(pct: int) -> str:
        return "var(--green)" if pct >= 75 else "var(--yellow)" if pct >= 50 else "var(--red)"

    # Sparkline (last 7 wellness entries, readiness score each day)
    sparkline_data = wellness[-7:] if len(wellness) >= 7 else wellness
    sparkline = []
    for w in sparkline_data:
        w_hrv   = w.get("hrv") or hrv_avg
        w_sleep = w.get("sleepSecs") or 0
        w_ctl   = w.get("ctl") or ctl
        w_atl   = w.get("atl") or atl
        w_tsb   = w_ctl - w_atl
        pct = calc_readiness(hrv=w_hrv, hrv_7d_avg=hrv_avg,
                             sleep_secs=w_sleep, tsb=w_tsb)
        sparkline.append({"pct": pct, "color": readiness_color(pct)})

    # Polarisation (last week's rides — use previous week activities)
    prev_oldest = (monday - timedelta(7)).isoformat()
    prev_newest = (monday - timedelta(1)).isoformat()
    prev_acts   = get_activities(prev_oldest, prev_newest)
    polar = _calc_polarisation(prev_acts)

    # 4-week outlook
    outlook = []
    for i in range(4):
        w = kw + i
        p = parse_kw_plan(w)
        outlook.append({
            "kw":          w,
            "theme":       p["theme"],
            "sub":         p["sub"],
            "tss_plan":    p["tss_plan"],
            "tss_ist":     sum(d["tss_ist"] for d in days) if i == 0 else 0,
            "key_workouts": _key_workouts(p["days"]),
        })

    # KW date string
    kw_dates = (f"{monday.day}.–{sunday.day}. "
                f"{MONTH_DE[monday.month]} {monday.year}"
                if monday.month == sunday.month
                else f"{monday.day}. {MONTH_DE[monday.month]}–"
                     f"{sunday.day}. {MONTH_DE[sunday.month]} {monday.year}")

    return {
        "kw":               kw,
        "kw_dates":         kw_dates,
        "phase_name":       current_phase["name"],
        "next_phase":       next_phase,
        "phases":           phases,
        "season_kw_current": season_pos,
        "season_kw_total":  season_total,
        "season_offset":    season_offset,
        # Readiness ring
        "readiness_score":  r_score,
        "readiness_offset": r_offset,
        "readiness_color":  r_color,
        "readiness_label":  r_label,
        "readiness_sub":    r_sub,
        # Form ring
        "ctl":              round(ctl, 1),
        "atl":              round(atl, 1),
        "tsb_display":      f"+{round(tsb,0):.0f}" if tsb >= 0 else f"{round(tsb,0):.0f}",
        "tsb_color":        fmt_tsb_color(tsb),
        "ctl_offset":       ctl_offset,
        "atl_offset":       atl_offset,
        # Week plan
        "tss_ist":          tss_ist,
        "tss_plan":         plan["tss_plan"],
        "sick_notice":      sick_notice,
        "days":             days,
        # Readiness bars
        "hrv_pct":          hrv_pct,
        "hrv_val":          f"{round(hrv)}/40",
        "hrv_color":        bar_color(hrv_pct),
        "sleep_pct":        sleep_pct,
        "sleep_val":        f"{sleep_h:.1f}h",
        "sleep_color":      bar_color(sleep_pct),
        "tsb_bar_pct":      tsb_pct,
        "tsb_bar_val":      f"{tsb:+.0f}",
        "tsb_bar_color":    bar_color(tsb_pct),
        "pulse_pct":        pulse_pct,
        "pulse_val":        f"{round(rhr)} bpm",
        "pulse_color":      bar_color(pulse_pct),
        "sparkline":        sparkline,
        # Polarisation
        "polar_z12_pct":    polar["z12"],
        "polar_z3_pct":     polar["z3"],
        "polar_z47_pct":    polar["z47"],
        "polar_pi":         polar["pi"],
        "polar_ok":         polar["ok"],
        # Outlook
        "outlook":          outlook,
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
    """Estimate Z1-2 / Z3 / Z4-7 split from ride activities."""
    rides = [a for a in activities if a.get("type") in ("Ride", "VirtualRide", "GravelRide")]
    if not rides:
        return {"z12": 80, "z3": 15, "z47": 5, "pi": 80, "ok": True}
    # intervals.icu returns icu_z1..icu_z7 as seconds in each zone
    totals = [0] * 8
    for r in rides:
        for z in range(1, 8):
            totals[z] += r.get(f"icu_z{z}") or 0
    total = sum(totals[1:]) or 1
    z12 = round((totals[1] + totals[2]) / total * 100)
    z3  = round(totals[3] / total * 100)
    z47 = round((totals[4] + totals[5] + totals[6] + totals[7]) / total * 100)
    pi  = z12
    return {"z12": z12, "z3": z3, "z47": z47, "pi": pi, "ok": z3 < 15}

def _key_workouts(days: list) -> str:
    non_lit = [d["workout"] for d in days
               if d["workout"] and not d["rest"]
               and not d["workout"].lower().startswith("lit")]
    return " · ".join(non_lit[:3]) if non_lit else "–"

def render(ctx: dict) -> str:
    env = Environment(loader=FileSystemLoader("."), autoescape=False)
    return env.get_template("dashboard.template.html").render(**ctx)

def main():
    today    = date.today()
    kw       = today.isocalendar()[1]
    year     = today.isocalendar()[0]
    monday, sunday = week_date_range(kw, year)

    ctx = build_context(kw=kw, monday=monday, sunday=sunday)
    html = render(ctx)

    out = Path("docs/dashboard.html")
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"✓ docs/dashboard.html generated for KW{kw}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_generate.py -v`
Expected: all tests PASSED

- [ ] **Step 5: Copy static assets to docs/**

```bash
cp manifest.json docs/manifest.json
cp sw.js docs/sw.js
cp icon.svg docs/icon.svg
```

- [ ] **Step 6: Test full render locally**

Run: `INTERVALS_API_KEY=xxx INTERVALS_ATHLETE_ID=xxx python generate.py`
Expected: `✓ docs/dashboard.html generated for KW16`

Open `docs/dashboard.html` in a browser and verify it looks identical to the current `dashboard.html` but with live values.

- [ ] **Step 7: Commit**

```bash
git add generate.py dashboard.template.html docs/
git commit -m "feat: full render pipeline — generate.py + template"
```

---

## Task 7: GitHub Actions Workflow

**Files:**
- Create: `.github/workflows/build.yml`

- [ ] **Step 1: Create workflow file**

```yaml
# .github/workflows/build.yml
name: Regenerate Dashboard

on:
  schedule:
    - cron: "0 5 * * *"      # 07:00 CEST (05:00 UTC)
  repository_dispatch:
    types: [activity-uploaded]
  workflow_dispatch:           # manual trigger via GitHub UI

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - run: pip install -r requirements.txt

      - name: Generate dashboard
        env:
          INTERVALS_API_KEY:    ${{ secrets.INTERVALS_API_KEY }}
          INTERVALS_ATHLETE_ID: ${{ secrets.INTERVALS_ATHLETE_ID }}
        run: python generate.py

      - name: Copy static assets
        run: |
          cp manifest.json docs/manifest.json
          cp sw.js docs/sw.js
          cp icon.svg docs/icon.svg

      - name: Commit generated files
        run: |
          git config user.name  "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/
          git diff --staged --quiet || git commit -m "chore: regenerate dashboard [skip ci]"
          git push
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/build.yml
git commit -m "feat: github actions workflow for dashboard rebuild"
```

---

## Task 8: GitHub Repository & Pages Setup

**Steps are manual (no code):**

- [ ] **Step 1: Create private GitHub repository**

Go to github.com → New repository → Name: `coaching` → Private → Create

- [ ] **Step 2: Push local files to GitHub**

```bash
git remote add origin git@github.com:YOUR_USERNAME/coaching.git
git branch -M main
git push -u origin main
```

- [ ] **Step 3: Add GitHub Secrets**

Go to: repo → Settings → Secrets and variables → Actions → New repository secret

Add:
- `INTERVALS_API_KEY` → your intervals.icu API key (Settings → Developer Settings in intervals.icu)
- `INTERVALS_ATHLETE_ID` → your athlete ID (visible in intervals.icu URL: `intervals.icu/athlete/i12345` → `i12345`)

- [ ] **Step 4: Enable GitHub Pages**

Go to: repo → Settings → Pages
- Source: Deploy from a branch
- Branch: `main` / `docs`
- Save

Note the URL shown (e.g. `https://YOUR_USERNAME.github.io/coaching/dashboard.html`)

- [ ] **Step 5: Trigger first build manually**

Go to: repo → Actions → Regenerate Dashboard → Run workflow
Expected: workflow runs, commits `docs/dashboard.html`, GitHub Pages deploys within ~2 min

- [ ] **Step 6: Verify dashboard is live**

Open `https://YOUR_USERNAME.github.io/coaching/dashboard.html` in Safari on iPhone.
Expected: Password prompt → enter password → dashboard loads with live data.

- [ ] **Step 7: Install as PWA on iPhone**

In Safari: Share button → "Zum Home-Bildschirm" → Add
Expected: App icon appears on home screen, opens fullscreen without browser chrome.

---

## Task 9: intervals.icu Webhook

- [ ] **Step 1: Create a GitHub Personal Access Token (PAT)**

Go to: github.com → Settings → Developer settings → Personal access tokens → Fine-grained tokens
- Name: `intervals-webhook`
- Expiration: 1 year
- Repository access: Only `coaching`
- Permissions: Actions → Read and Write (to trigger workflows)

Copy the token.

- [ ] **Step 2: Test if intervals.icu supports custom headers**

Go to: intervals.icu → Settings → Integrations → Webhooks (or similar)
Check if there's a field for custom headers.

**If YES (custom headers supported):**
Configure webhook:
- URL: `https://api.github.com/repos/YOUR_USERNAME/coaching/dispatches`
- Events: `ACTIVITY_ANALYZED`
- Headers: `Authorization: token YOUR_PAT`, `Accept: application/vnd.github+json`
- Payload (if configurable): `{"event_type": "activity-uploaded"}`

**If NO (no custom headers):**
Proceed to Step 3.

- [ ] **Step 3: (Only if Step 2 failed) Create Cloudflare Worker relay**

Go to: dash.cloudflare.com → Workers & Pages → Create Worker
Paste this code:

```js
export default {
  async fetch(req, env) {
    if (req.method !== "POST") return new Response("ok");
    await fetch("https://api.github.com/repos/YOUR_USERNAME/coaching/dispatches", {
      method: "POST",
      headers: {
        "Authorization": `token ${env.GITHUB_PAT}`,
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ event_type: "activity-uploaded" }),
    });
    return new Response("ok");
  }
}
```

In Worker Settings → Variables → Add `GITHUB_PAT` = your PAT (as secret).

Deploy. Note the Worker URL (e.g. `https://intervals-relay.YOUR_USERNAME.workers.dev`).

Configure intervals.icu webhook to POST to this Worker URL on `ACTIVITY_ANALYZED`.

- [ ] **Step 4: Test end-to-end**

Upload any activity to intervals.icu (or sync from Garmin/Wahoo).
Wait 2–3 minutes.
Check repo → Actions → verify a new build was triggered.
Open PWA on iPhone — pull to refresh if needed.
Expected: Dashboard shows the just-uploaded workout as ✅ done with real TSS.
