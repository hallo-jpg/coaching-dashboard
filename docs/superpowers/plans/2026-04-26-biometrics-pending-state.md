# Biometrics Pending State Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wenn HRV/Schlaf/Ruhepuls noch nicht von der Uhr synchronisiert sind, zeigt die Readiness-Card einen Banner mit gedimmten Werten — kein Fallback auf Vortag.

**Architecture:** Flag `biometrics_pending` in `generate.py` gesetzt wenn `hrv` null; Template reagiert mit Banner + Opacity-Dimming der betroffenen Elemente. Readiness-Ring zeigt leer (offset = CIRC_OUTER), Score zeigt „–".

**Tech Stack:** Python 3.11, Jinja2, pytest

---

## Files

- Modify: `generate.py` — Fallbacks entfernen, Flag setzen, r_score=0 wenn pending
- Modify: `dashboard.template.html` — Banner + Dimming
- Modify: `tests/test_generate.py` — 2 kaputte Tests reparieren, 2 neue Tests hinzufügen

---

### Task 1: Tests reparieren und biometrics_pending-Tests hinzufügen

**Files:**
- Modify: `tests/test_generate.py`

Aktueller Stand: `test_readiness_high` und `test_readiness_low` scheitern weil sie die alte Signatur `calc_readiness(hrv=..., hrv_7d_avg=..., ...)` verwenden. Die aktuelle Signatur ist `calc_readiness(wellness_window: list[dict], hrv_baseline=None)`.

- [ ] **Step 1: Verifiziere die 2 kaputten Tests**

```bash
cd /Users/stefan/Documents/Claude\ Code/Coaching
python3 -m pytest tests/test_generate.py::test_readiness_high tests/test_generate.py::test_readiness_low -v
```

Expected output:
```
FAILED tests/test_generate.py::test_readiness_high - TypeError: calc_readiness() got an unexpected keyword argument 'hrv'
FAILED tests/test_generate.py::test_readiness_low - TypeError: ...
```

- [ ] **Step 2: Repariere test_readiness_high und test_readiness_low**

Ersetze in `tests/test_generate.py` die beiden defekten Tests:

```python
# ALT (entfernen):
def test_readiness_high():
    score = calc_readiness(hrv=45, hrv_7d_avg=42, sleep_secs=28800, tsb=20)
    assert score >= 80

def test_readiness_low():
    score = calc_readiness(hrv=28, hrv_7d_avg=42, sleep_secs=18000, tsb=-15)
    assert score < 60
```

```python
# NEU (ersetzen durch):
def test_readiness_high():
    window = [
        {"id": "2026-04-10", "hrv": 42, "sleepSecs": 28800, "ctl": 45.0, "atl": 35.0, "restingHR": 48},
        {"id": "2026-04-11", "hrv": 44, "sleepSecs": 27000, "ctl": 45.5, "atl": 34.0, "restingHR": 47},
        {"id": "2026-04-12", "hrv": 45, "sleepSecs": 28800, "ctl": 46.0, "atl": 33.0, "restingHR": 47},
    ]
    score = calc_readiness(wellness_window=window, hrv_baseline=window)
    assert score >= 60


def test_readiness_low():
    window = [
        {"id": "2026-04-10", "hrv": 42, "sleepSecs": 25200, "ctl": 40.0, "atl": 55.0, "restingHR": 52},
        {"id": "2026-04-11", "hrv": 35, "sleepSecs": 18000, "ctl": 40.5, "atl": 56.0, "restingHR": 56},
        {"id": "2026-04-12", "hrv": 28, "sleepSecs": 18000, "ctl": 41.0, "atl": 57.0, "restingHR": 58},
    ]
    score = calc_readiness(wellness_window=window, hrv_baseline=window)
    assert score < 60
```

- [ ] **Step 3: Füge biometrics_pending zu required_keys hinzu**

In `test_build_context_keys`, ergänze `"biometrics_pending"` in der `required_keys`-Liste:

```python
required_keys = [
    "kw", "kw_dates", "phase_name", "readiness_score", "readiness_color",
    "ctl", "atl", "tsb_display", "ctl_offset", "atl_offset",
    "tss_ist", "tss_plan", "days", "sparkline", "outlook",
    "phases", "polar_z12_pct", "polar_z3_pct", "polar_z47_pct",
    "biometrics_pending",
]
```

- [ ] **Step 4: Füge Test für biometrics_pending=True hinzu**

Am Ende der Datei (nach `test_build_context_has_nutrition`):

```python
MOCK_WELLNESS_NO_HRV = [
    {"id": "2026-04-12", "hrv": None, "sleepSecs": None, "ctl": 42.0, "atl": 38.0, "restingHR": None},
    {"id": "2026-04-13", "hrv": None, "sleepSecs": None, "ctl": 42.5, "atl": 37.0, "restingHR": None},
    {"id": "2026-04-14", "hrv": None, "sleepSecs": None, "ctl": 43.0, "atl": 36.0, "restingHR": None},
]


@patch("generate.get_wellness", return_value=MOCK_WELLNESS_NO_HRV)
@patch("generate.get_activities", return_value=MOCK_ACTIVITIES)
@patch("generate.get_power_bests", return_value=[])
def test_build_context_biometrics_pending(mock_pb, mock_act, mock_well):
    from generate import build_context
    ctx = build_context(kw=16, monday=date(2026, 4, 13), sunday=date(2026, 4, 19))
    assert ctx["biometrics_pending"] is True
    assert ctx["readiness_score"] == 0
```

- [ ] **Step 5: Führe Tests aus — erwarte 1 Fehler (biometrics_pending fehlt noch im Context)**

```bash
python3 -m pytest tests/test_generate.py -v 2>&1 | tail -20
```

Expected: `test_readiness_high` und `test_readiness_low` PASS, `test_build_context_biometrics_pending` und `test_build_context_keys` FAIL (biometrics_pending noch nicht implementiert).

- [ ] **Step 6: Commit**

```bash
git add tests/test_generate.py
git commit -m "test: repariere readiness-Tests + füge biometrics_pending-Tests hinzu"
```

---

### Task 2: generate.py — Fallbacks entfernen, biometrics_pending Flag setzen

**Files:**
- Modify: `generate.py:617-640`

- [ ] **Step 1: Ersetze den Fallback-Block (Zeilen 617–629)**

Aktueller Code:
```python
today_w = next((w for w in reversed(wellness) if w.get("id", "") <= today_iso and (w.get("ctl") or w.get("hrv"))), wellness[-1] if wellness else {})
hrv     = today_w.get("hrv") or 0
if not hrv:
    hrv = next((w.get("hrv") for w in reversed(wellness) if w.get("hrv")), 0)
sleep_s = today_w.get("sleepSecs") or 0
if not sleep_s:
    sleep_s = next((w.get("sleepSecs") for w in reversed(wellness) if w.get("sleepSecs")), 0)
ctl     = today_w.get("ctl") or 0
atl     = today_w.get("atl") or 0
tsb     = round(ctl - atl, 1)
rhr     = today_w.get("restingHR") or 0
if not rhr:
    rhr = next((w.get("restingHR") for w in reversed(wellness) if w.get("restingHR")), 60)
```

Neuer Code:
```python
today_w           = next((w for w in reversed(wellness) if w.get("id", "") <= today_iso and (w.get("ctl") or w.get("hrv"))), wellness[-1] if wellness else {})
biometrics_pending = not bool(today_w.get("hrv"))
hrv     = today_w.get("hrv") or 0
sleep_s = today_w.get("sleepSecs") or 0
ctl     = today_w.get("ctl") or 0
atl     = today_w.get("atl") or 0
tsb     = round(ctl - atl, 1)
rhr     = today_w.get("restingHR") or 0
```

- [ ] **Step 2: Setze r_score=0 wenn biometrics_pending (nach Zeile 635)**

Aktueller Code nach Zeile 635:
```python
    r_score = calc_readiness(wellness_30[-7:], hrv_baseline=wellness_30)
    r_color = readiness_color(r_score)
    r_label = readiness_label(r_score)
    r_sub   = _readiness_sub(rhr, hrv, hrv_mean, wellness)
```

Neuer Code:
```python
    r_score = calc_readiness(wellness_30[-7:], hrv_baseline=wellness_30)
    r_color = readiness_color(r_score)
    r_label = readiness_label(r_score)
    r_sub   = _readiness_sub(rhr, hrv, hrv_mean, wellness)
    if biometrics_pending:
        r_score = 0  # Ring zeigt leer; Template zeigt "–"
```

- [ ] **Step 3: Füge biometrics_pending in den Context-Dict ein**

Suche den Block der mit `"readiness_score": r_score` beginnt (ca. Zeile 735) und ergänze:

```python
        "readiness_score": r_score, "readiness_offset": r_offset,
        "readiness_color": r_color, "readiness_label": r_label, "readiness_sub": r_sub,
        # ... (bestehende Zeilen bleiben) ...
        "polar_no_data": polar["no_data"],
        "biometrics_pending": biometrics_pending,   # ← NEU, direkt nach polar_no_data
```

- [ ] **Step 4: Führe Tests aus — alle sollen PASS**

```bash
python3 -m pytest tests/test_generate.py -v 2>&1 | tail -20
```

Expected: `24 passed, 0 failed`

- [ ] **Step 5: Commit**

```bash
git add generate.py
git commit -m "feat(dashboard): biometrics_pending Flag – kein Fallback auf Vortag"
```

---

### Task 3: dashboard.template.html — Banner + Dimming

**Files:**
- Modify: `dashboard.template.html` (Readiness-Card, ca. Zeilen 655–699)

- [ ] **Step 1: Readiness Score: zeige „–" wenn biometrics_pending**

Finde diesen Block:
```html
    <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:14px">
      <div class="readiness-score" style="color:{{ readiness_color }}">{{ readiness_score }}</div>
      <div class="readiness-tag" style="color:{{ readiness_color }}">{{ readiness_label }}</div>
    </div>
```

Ersetze durch:
```html
    <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:14px">
      {% if biometrics_pending %}
      <div class="readiness-score" style="color:var(--muted)">–</div>
      {% else %}
      <div class="readiness-score" style="color:{{ readiness_color }}">{{ readiness_score }}</div>
      <div class="readiness-tag" style="color:{{ readiness_color }}">{{ readiness_label }}</div>
      {% endif %}
    </div>
```

- [ ] **Step 2: Banner einfügen — direkt nach dem Score-Block, vor der HRV-Box**

Finde die Zeile die die HRV-Box beginnt:
```html
    <div style="display:flex;align-items:center;gap:10px;padding:10px;background:rgba(255,255,255,0.03);border:1px solid {{ hrv_status_color }}
```

Füge direkt davor ein:
```html
    {% if biometrics_pending %}
    <div style="background:rgba(15,17,23,0.7);border:1px solid rgba(99,102,241,0.3);border-radius:8px;padding:8px 12px;font-size:0.65rem;color:#94a3b8;text-align:center;margin-bottom:10px">
      ⏳ Uhr noch nicht synchronisiert – Werte folgen
    </div>
    {% endif %}
```

- [ ] **Step 3: HRV-Box dimmen wenn biometrics_pending**

Finde die HRV-Box (das `<div>` das mit `display:flex;align-items:center;gap:10px;padding:10px;...border-radius:10px;margin-bottom:10px` beginnt). Ergänze `{% if biometrics_pending %}opacity:0.15;{% endif %}` im style:

```html
    <div style="display:flex;align-items:center;gap:10px;padding:10px;background:rgba(255,255,255,0.03);border:1px solid {{ hrv_status_color }};border-color:{{ hrv_status_color }};opacity-border:0.3;border-radius:10px;margin-bottom:10px;border-color:color-mix(in srgb,{{ hrv_status_color }} 35%,transparent){% if biometrics_pending %};opacity:0.15{% endif %}">
```

- [ ] **Step 4: Schlaf- und Ruhepuls-Zellen dimmen (NICHT TSB)**

Finde das Mini-Grid (3 Zellen: Schlaf | TSB | Ruhepuls). Die einzelnen `<div>`-Zellen sehen so aus:

```html
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:7px;text-align:center">
        <div class="rbar-lbl" style="margin-bottom:3px">Schlaf</div>
        ...
      </div>
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:7px;text-align:center">
        <div class="rbar-lbl" style="margin-bottom:3px">TSB</div>
        ...
      </div>
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:7px;text-align:center">
        <div class="rbar-lbl" style="margin-bottom:3px">Ruhepuls</div>
        ...
      </div>
```

Ergänze `{% if biometrics_pending %}opacity:0.15;{% endif %}` **nur** bei Schlaf- und Ruhepuls-Zelle, **nicht** bei TSB:

```html
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:7px;text-align:center{% if biometrics_pending %};opacity:0.15{% endif %}">
        <div class="rbar-lbl" style="margin-bottom:3px">Schlaf</div>
        ...
      </div>
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:7px;text-align:center">
        <div class="rbar-lbl" style="margin-bottom:3px">TSB</div>
        ...
      </div>
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:7px;text-align:center{% if biometrics_pending %};opacity:0.15{% endif %}">
        <div class="rbar-lbl" style="margin-bottom:3px">Ruhepuls</div>
        ...
      </div>
```

- [ ] **Step 5: Manuelle Verifikation**

Generiere das Dashboard lokal mit einem Wellness-Eintrag ohne HRV um das Pending-State zu sehen:

```bash
INTERVALS_API_KEY=test INTERVALS_ATHLETE_ID=test python3 -c "
from generate import build_context
from datetime import date
from unittest.mock import patch

wellness_no_hrv = [
    {'id': '2026-04-14', 'hrv': None, 'sleepSecs': None, 'ctl': 43.0, 'atl': 36.0, 'restingHR': None},
    {'id': '2026-04-19', 'hrv': None, 'sleepSecs': None, 'ctl': 35.0, 'atl': 23.0, 'restingHR': None},
]
with patch('generate.get_wellness', return_value=wellness_no_hrv), \
     patch('generate.get_activities', return_value=[]), \
     patch('generate.get_power_bests', return_value=[]):
    ctx = build_context(kw=17, monday=date(2026, 4, 20), sunday=date(2026, 4, 26))
    print('biometrics_pending:', ctx['biometrics_pending'])
    print('readiness_score:', ctx['readiness_score'])
"
```

Expected:
```
biometrics_pending: True
readiness_score: 0
```

- [ ] **Step 6: Tests ausführen — alle sollen PASS**

```bash
python3 -m pytest tests/test_generate.py -v 2>&1 | tail -10
```

Expected: `24 passed, 0 failed`

- [ ] **Step 7: Commit + Push**

```bash
git add dashboard.template.html
git commit -m "feat(dashboard): Banner + Dimming wenn Biometrik-Sync ausstehend"
git push
```
