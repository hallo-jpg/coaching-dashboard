# TSS-Übersicht Erweiterung Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** TSS-Übersicht · 8 Wochen Kachel um Plan-Umriss-Balken, Phasen-Labels, Compliance-Stat und nächste-KW-Plan-Stat erweitern.

**Architecture:** Drei unabhängige Änderungen: (1) `generate.py` bekommt zwei neue Hilfsfunktionen + erweiterte Wochendaten, (2) `get_tss_overview_history()` gibt neue Felder zurück, (3) Template-Block wird mit neuer `.barea`-Struktur ersetzt. Alle Daten kommen aus vorhandenen Quellen (`SEASON_PHASES`, `parse_kw_plan()`).

**Tech Stack:** Python 3.11, Jinja2, pytest, dashboard.template.html (Dark-Theme CSS)

---

## File Map

| Datei | Änderung |
|---|---|
| `generate.py` | `PHASE_ABBREV`-Konstante nach `SEASON_PHASES` (Zeile ~712), neue Funktion `_phase_for_kw()` (nach `PHASE_ABBREV`), neue Funktion `calc_compliance()` (vor `get_tss_overview_history()`), `get_tss_overview_history()` erweitern (Zeilen 1119–1156) |
| `dashboard.template.html` | TSS-Übersicht-Block (Zeilen 782–820) ersetzen |
| `tests/test_generate.py` | 5 neue Tests am Ende der Datei |

---

### Task 1: `PHASE_ABBREV`, `_phase_for_kw()`, `calc_compliance()` zu generate.py hinzufügen

**Files:**
- Modify: `generate.py:710–712` (nach `SEASON_PHASES`)
- Test: `tests/test_generate.py` (am Ende der Datei anhängen)

**Kontext:** `SEASON_PHASES` ist ab Zeile 700 definiert. Die neuen Hilfsfunktionen kommen direkt danach.

- [ ] **Step 1: Failing tests schreiben**

In `tests/test_generate.py` am Ende der Datei anhängen:

```python
from generate import _phase_for_kw, calc_compliance


def test_phase_for_kw_hit():
    label, color = _phase_for_kw(18)  # KW18 = HIT-Aufbau
    assert label == "HIT"
    assert color == "#f97316"


def test_phase_for_kw_taper():
    label, color = _phase_for_kw(23)  # KW23 = Tapering
    assert label == "Taper"
    assert color == "#60a5fa"


def test_phase_for_kw_unknown():
    label, color = _phase_for_kw(99)  # unbekannte KW
    assert label == "–"
    assert color == "#94a3b8"


def test_calc_compliance_full():
    weeks = [
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 500},
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 480},
    ]
    assert calc_compliance(weeks) == 100


def test_calc_compliance_partial():
    weeks = [
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 500},
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 200},
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 500},
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 200},
    ]
    assert calc_compliance(weeks) == 50


def test_calc_compliance_ignores_no_plan():
    weeks = [
        {"is_current": False, "is_future": False, "tss_plan": 0,   "tss_ist": 0},
        {"is_current": False, "is_future": False, "tss_plan": 30,  "tss_ist": 20},
        {"is_current": False, "is_future": False, "tss_plan": 500, "tss_ist": 500},
    ]
    # Nur die Woche mit tss_plan > 50 zählt → 1/1 = 100%
    assert calc_compliance(weeks) == 100


def test_calc_compliance_empty():
    assert calc_compliance([]) == 0
    weeks = [{"is_current": True, "is_future": False, "tss_plan": 500, "tss_ist": 300}]
    assert calc_compliance(weeks) == 0  # laufende Woche ignoriert
```

- [ ] **Step 2: Tests ausführen — müssen FAIL sein**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
python3 -m pytest tests/test_generate.py::test_phase_for_kw_hit tests/test_generate.py::test_calc_compliance_full -v
```

Erwartetes Ergebnis: `ImportError: cannot import name '_phase_for_kw'` oder `NameError`

- [ ] **Step 3: `PHASE_ABBREV`, `_phase_for_kw()`, `calc_compliance()` implementieren**

In `generate.py` **nach Zeile 710** (direkt nach dem Ende von `SEASON_PHASES`) einfügen:

```python
PHASE_ABBREV: dict[str, tuple[str, str]] = {
    "Baseline":    ("Base",   "#94a3b8"),
    "Urlaub":      ("Urlaub", "#94a3b8"),
    "Grundlage":   ("Base",   "#94a3b8"),
    "HIT-Aufbau":  ("HIT",    "#f97316"),
    "TT-Spezifik": ("TT",     "#a78bfa"),
    "Tapering":    ("Taper",  "#60a5fa"),
    "🏁 RadRace":  ("Race",   "#60a5fa"),
    "Erholung":    ("Erhol.", "#94a3b8"),
    "🗺️ Rosen.":  ("Race",   "#60a5fa"),
}


def _phase_for_kw(kw: int) -> tuple[str, str]:
    """Return (short_label, css_color) for a given week number."""
    phase = next((p for p in SEASON_PHASES if p["start_kw"] <= kw <= p["end_kw"]), None)
    if phase is None:
        return ("–", "#94a3b8")
    return PHASE_ABBREV.get(phase["name"], ("–", "#94a3b8"))


def calc_compliance(weeks: list[dict]) -> int:
    """Percentage of completed weeks where tss_ist >= 75% of tss_plan. Ignores weeks with tss_plan <= 50."""
    completed = [
        w for w in weeks
        if not w["is_current"] and not w["is_future"] and w["tss_plan"] > 50
    ]
    if not completed:
        return 0
    ok = sum(1 for w in completed if w["tss_ist"] >= 0.75 * w["tss_plan"])
    return round(ok / len(completed) * 100)
```

- [ ] **Step 4: Tests ausführen — müssen PASS sein**

```bash
python3 -m pytest tests/test_generate.py::test_phase_for_kw_hit tests/test_generate.py::test_phase_for_kw_taper tests/test_generate.py::test_phase_for_kw_unknown tests/test_generate.py::test_calc_compliance_full tests/test_generate.py::test_calc_compliance_partial tests/test_generate.py::test_calc_compliance_ignores_no_plan tests/test_generate.py::test_calc_compliance_empty -v
```

Erwartetes Ergebnis: 7 passed

- [ ] **Step 5: Commit**

```bash
git add generate.py tests/test_generate.py
git commit -m "feat(generate): PHASE_ABBREV, _phase_for_kw(), calc_compliance() hinzufügen"
```

---

### Task 2: `get_tss_overview_history()` mit Plan-/Phasen-/Compliance-Daten erweitern

**Files:**
- Modify: `generate.py:1119–1156` (innere Loop + summary dict)
- Test: `tests/test_generate.py` (ein neuer Test)

**Kontext:** Die Funktion baut in zwei Phasen: (1) `weeks_raw` Liste → (2) `weeks` Liste mit berechneten Farben. Erweiterung erfolgt in Phase 2. Summary-Dict am Ende bekommt `compliance_pct` und `next_kw_plan`.

- [ ] **Step 1: Failing test schreiben**

In `tests/test_generate.py` am Ende anhängen:

```python
from generate import get_tss_overview_history
from unittest.mock import patch


def test_tss_weeks_has_plan_fields():
    """Jede Woche im Rückgabewert hat tss_plan, plan_bar_height_pct, phase_short, phase_color."""
    with patch("generate.get_activities", return_value=[]):
        weeks, summary = get_tss_overview_history(current_kw=18, num_weeks=3)
    for w in weeks:
        assert "tss_plan" in w, f"tss_plan fehlt in {w}"
        assert "plan_bar_height_pct" in w, f"plan_bar_height_pct fehlt in {w}"
        assert "phase_short" in w, f"phase_short fehlt in {w}"
        assert "phase_color" in w, f"phase_color fehlt in {w}"
    assert "compliance_pct" in summary
    assert "next_kw_plan" in summary
```

- [ ] **Step 2: Test ausführen — muss FAIL sein**

```bash
python3 -m pytest tests/test_generate.py::test_tss_weeks_has_plan_fields -v
```

Erwartetes Ergebnis: `AssertionError: tss_plan fehlt`

- [ ] **Step 3: `get_tss_overview_history()` erweitern**

Den Block in `generate.py` Zeilen 1119–1143 (die `weeks`-Loop) ersetzen:

**Vorher (Zeilen 1119–1143):**
```python
    weeks = []
    for w in weeks_raw:
        tss = w["tss_ist"]
        is_current, is_future = w["is_current"], w["is_future"]
        ratio = tss / avg_tss if avg_tss > 0 and not is_future else 0

        if is_current or is_future:
            bar_color, label_color, arrow = "var(--muted)", "var(--muted)", ""
        elif ratio > 1.15:
            bar_color, label_color, arrow = "var(--yellow)", "var(--yellow)", " ↑"
        elif ratio >= 0.75:
            bar_color, label_color, arrow = "var(--green)", "var(--green)", ""
        elif ratio >= 0.50:
            bar_color, label_color, arrow = "var(--yellow)", "var(--yellow)", " ↓"
        else:
            bar_color, label_color, arrow = "var(--red)", "var(--red)", ""

        bar_h = max(round(tss / bar_scale * 100), 3) if tss > 0 else (5 if is_current else 2)

        weeks.append({
            "kw": w["kw"], "tss_ist": tss,
            "bar_color": bar_color, "bar_height_pct": bar_h,
            "label_color": label_color, "arrow": arrow,
            "is_current": is_current, "is_future": is_future,
        })
```

**Nachher:**
```python
    weeks = []
    for w in weeks_raw:
        tss = w["tss_ist"]
        is_current, is_future = w["is_current"], w["is_future"]
        ratio = tss / avg_tss if avg_tss > 0 and not is_future else 0

        if is_current or is_future:
            bar_color, label_color, arrow = "var(--muted)", "var(--muted)", ""
        elif ratio > 1.15:
            bar_color, label_color, arrow = "var(--yellow)", "var(--yellow)", " ↑"
        elif ratio >= 0.75:
            bar_color, label_color, arrow = "var(--green)", "var(--green)", ""
        elif ratio >= 0.50:
            bar_color, label_color, arrow = "var(--yellow)", "var(--yellow)", " ↓"
        else:
            bar_color, label_color, arrow = "var(--red)", "var(--red)", ""

        bar_h = max(round(tss / bar_scale * 100), 3) if tss > 0 else (5 if is_current else 2)

        tss_plan = parse_kw_plan(w["kw"]).get("tss_plan", 0)
        plan_h = min(round(tss_plan / bar_scale * 100), 100) if tss_plan > 0 else 0
        phase_short, phase_color = _phase_for_kw(w["kw"])

        weeks.append({
            "kw": w["kw"], "tss_ist": tss,
            "bar_color": bar_color, "bar_height_pct": bar_h,
            "label_color": label_color, "arrow": arrow,
            "is_current": is_current, "is_future": is_future,
            "tss_plan": tss_plan,
            "plan_bar_height_pct": plan_h,
            "phase_short": phase_short,
            "phase_color": phase_color,
        })
```

Dann den `summary`-Dict (Zeilen 1150–1155) ersetzen:

**Vorher:**
```python
    summary = {
        "avg_tss": avg_tss,
        "max_tss": max_week["tss_ist"], "max_kw": max_week["kw"],
        "min_tss": min_week["tss_ist"], "min_kw": min_week["kw"],
        "avg_line_pct": avg_pct,
    }
```

**Nachher:**
```python
    next_kw_plan = next((w["tss_plan"] for w in weeks if w["is_future"]), 0)
    compliance = calc_compliance(weeks)
    summary = {
        "avg_tss": avg_tss,
        "max_tss": max_week["tss_ist"], "max_kw": max_week["kw"],
        "min_tss": min_week["tss_ist"], "min_kw": min_week["kw"],
        "avg_line_pct": avg_pct,
        "compliance_pct": compliance,
        "next_kw_plan": next_kw_plan,
    }
```

- [ ] **Step 4: Test ausführen — muss PASS sein**

```bash
python3 -m pytest tests/test_generate.py::test_tss_weeks_has_plan_fields -v
```

Erwartetes Ergebnis: 1 passed

- [ ] **Step 5: Alle Tests ausführen — kein Regression**

```bash
python3 -m pytest tests/test_generate.py -v
```

Erwartetes Ergebnis: alle Tests passed (mindestens 52 — vorher 45 + 8 neue)

- [ ] **Step 6: Commit**

```bash
git add generate.py tests/test_generate.py
git commit -m "feat(generate): TSS-Wochen um Plan, Phasen, Compliance erweitern"
```

---

### Task 3: dashboard.template.html — TSS-Übersicht-Block ersetzen

**Files:**
- Modify: `dashboard.template.html:782–820`

**Kontext:** Der Block startet mit `<!-- TSS-ÜBERSICHT 8 WOCHEN -->` und endet nach dem schließenden `</div>` des Stats-Grids. Er wird vollständig ersetzt. Neue Variablen die jetzt verfügbar sind: `w.tss_plan`, `w.plan_bar_height_pct`, `w.phase_short`, `w.phase_color`, `tss_summary.compliance_pct`, `tss_summary.next_kw_plan`.

- [ ] **Step 1: Alten Block exakt identifizieren**

```bash
grep -n "TSS-ÜBERSICHT 8 WOCHEN" "/Users/stefan/Documents/Claude Code/Coaching/dashboard.template.html"
```

Erwartetes Ergebnis: Zeile 782

- [ ] **Step 2: Alten Block ersetzen**

In `dashboard.template.html` den folgenden exakten Block (old_string für Edit-Tool):

```html
  <!-- TSS-ÜBERSICHT 8 WOCHEN -->
  <div class="ausblick-card" style="margin-bottom:0">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px">
      <div class="card-headline">TSS-Übersicht · 8 Wochen</div>
      <span style="font-size:0.7rem;font-weight:600;color:var(--muted)">Ø {{ tss_summary.avg_tss }} TSS</span>
    </div>

    <div style="position:relative;height:80px;margin-bottom:18px">
      <div style="position:absolute;left:0;right:0;bottom:{{ tss_summary.avg_line_pct }}%;border-top:1px dashed rgba(148,163,184,0.25);pointer-events:none;z-index:1">
        <span style="position:absolute;right:0;top:-8px;font-size:0.48rem;color:rgba(148,163,184,0.4)">Ø</span>
      </div>
      <div style="display:flex;align-items:flex-end;gap:4px;height:100%">
        {% for w in tss_weeks %}
        <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;position:relative">
          <span style="font-size:0.5rem;color:{{ w.label_color }};margin-bottom:2px;white-space:nowrap">
            {% if not w.is_future and w.tss_ist > 0 %}{{ w.tss_ist }}{{ w.arrow }}{% elif w.is_current %}▶{% endif %}
          </span>
          <div style="width:100%;height:{{ w.bar_height_pct }}%;background:{{ w.bar_color }};border-radius:3px 3px 0 0;{% if w.is_current %}opacity:0.55{% endif %}"></div>
          <span style="position:absolute;bottom:-14px;font-size:0.5rem;color:{% if w.is_current %}var(--text){% else %}var(--muted){% endif %}">KW{{ w.kw }}</span>
        </div>
        {% endfor %}
      </div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px">
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:6px;text-align:center">
        <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px">Ø 8 Wochen</div>
        <div style="font-size:0.85rem;font-weight:800;color:var(--text)">{{ tss_summary.avg_tss }}</div>
      </div>
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:6px;text-align:center">
        <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px">Höchste</div>
        <div style="font-size:0.85rem;font-weight:800;color:var(--yellow)">{{ tss_summary.max_tss }}</div>
      </div>
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:6px;text-align:center">
        <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px">Niedrigste</div>
        <div style="font-size:0.85rem;font-weight:800;color:var(--red)">{{ tss_summary.min_tss }}</div>
      </div>
    </div>
  </div>
```

ersetzen mit:

```html
<!-- TSS-ÜBERSICHT 8 WOCHEN -->
<div class="ausblick-card" style="margin-bottom:0">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px">
    <div class="card-headline">TSS-Übersicht · 8 Wochen</div>
    <span style="font-size:0.7rem;font-weight:600;color:var(--muted)">Ø {{ tss_summary.avg_tss }} TSS</span>
  </div>

  <div style="position:relative;height:95px;margin-bottom:6px">
    <div style="position:absolute;left:0;right:0;bottom:{{ tss_summary.avg_line_pct }}%;border-top:1px dashed rgba(148,163,184,0.25);pointer-events:none;z-index:2">
      <span style="position:absolute;right:0;top:-8px;font-size:0.48rem;color:rgba(148,163,184,0.4)">Ø</span>
    </div>
    <div style="display:flex;gap:3px;height:100%">
      {% for w in tss_weeks %}
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;height:100%">
        <span style="font-size:0.46rem;color:{{ w.label_color }};height:12px;line-height:12px;white-space:nowrap">
          {% if not w.is_future and w.tss_ist > 0 %}{{ w.tss_ist }}{{ w.arrow }}{% elif w.is_current %}▶{% endif %}
        </span>
        <div style="flex:1;width:100%;display:flex;align-items:flex-end;position:relative">
          {% if w.plan_bar_height_pct > 0 %}
          <div style="position:absolute;bottom:0;left:0;width:100%;height:{{ w.plan_bar_height_pct }}%;border-radius:3px 3px 0 0;border:1.5px solid rgba(148,163,184,0.35);background:transparent;box-sizing:border-box;z-index:0;{% if w.is_future %}border-style:dashed{% endif %}"></div>
          {% endif %}
          <div style="width:100%;height:{{ w.bar_height_pct }}%;background:{{ w.bar_color }};border-radius:3px 3px 0 0;position:relative;z-index:1;{% if w.is_current %}opacity:0.55{% endif %}"></div>
        </div>
        <span style="font-size:0.44rem;color:{% if w.is_current %}var(--text){% else %}var(--muted){% endif %};height:10px;line-height:10px">KW{{ w.kw }}</span>
        <span style="font-size:0.38rem;color:{{ w.phase_color }};height:9px;line-height:9px;text-align:center">{{ w.phase_short }}</span>
      </div>
      {% endfor %}
    </div>
  </div>

  <div style="font-size:0.44rem;color:var(--muted);display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;margin-top:4px">
    <span style="display:inline-flex;align-items:center;gap:3px">
      <span style="display:inline-block;width:10px;height:6px;border:1.5px solid rgba(148,163,184,0.4);border-radius:1px"></span>Plan
    </span>
    <span style="display:inline-flex;align-items:center;gap:3px">
      <span style="display:inline-block;width:10px;height:6px;background:var(--green);border-radius:1px"></span>Ist
    </span>
    <span><span style="color:#94a3b8">■</span> Base</span>
    <span><span style="color:#f97316">■</span> HIT</span>
    <span><span style="color:#60a5fa">■</span> Taper/Race</span>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:6px">
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:6px;text-align:center">
      <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px">Ø 8 Wochen</div>
      <div style="font-size:0.85rem;font-weight:800;color:var(--text)">{{ tss_summary.avg_tss }}</div>
    </div>
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:6px;text-align:center">
      <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px">Höchste</div>
      <div style="font-size:0.85rem;font-weight:800;color:var(--yellow)">{{ tss_summary.max_tss }}</div>
    </div>
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:6px;text-align:center">
      <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px">Compliance</div>
      <div style="font-size:0.85rem;font-weight:800;color:{% if tss_summary.compliance_pct >= 80 %}var(--green){% elif tss_summary.compliance_pct >= 60 %}var(--yellow){% else %}var(--accent){% endif %}">{{ tss_summary.compliance_pct }}%</div>
    </div>
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:6px;text-align:center">
      <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px">KW{{ tss_weeks | selectattr('is_future') | map(attribute='kw') | first | default('?') }} Plan</div>
      <div style="font-size:0.85rem;font-weight:800;color:var(--blue)">{% if tss_summary.next_kw_plan > 0 %}{{ tss_summary.next_kw_plan }}{% else %}–{% endif %}</div>
    </div>
  </div>
</div>
```

- [ ] **Step 3: Template-Rendering testen**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
python3 -m pytest tests/test_generate.py::test_build_context_keys -v
```

Erwartetes Ergebnis: passed

- [ ] **Step 4: Dashboard lokal generieren und HTML prüfen**

```bash
python3 generate.py 2>&1 | tail -5
grep -c "plan_bar_height_pct\|phase_short\|compliance_pct" docs/dashboard.html || echo "0 Treffer – Variablen nicht gerendert"
grep "Compliance" docs/dashboard.html | head -3
```

Erwartetes Ergebnis: `generate.py` läuft ohne Fehler, "Compliance" erscheint im Output.

- [ ] **Step 5: Alle Tests ausführen — kein Regression**

```bash
python3 -m pytest tests/test_generate.py -v
```

Erwartetes Ergebnis: alle Tests passed

- [ ] **Step 6: Commit und Push**

```bash
git add dashboard.template.html docs/dashboard.html
git commit -m "feat(template): TSS-Übersicht – Plan-Balken, Phasen, Compliance, KW-Plan"
git pull --rebase && git push
```

---

## Vollständige Test-Suite nach Abschluss

```bash
python3 -m pytest tests/test_generate.py -v
```

Erwartetes Ergebnis: ≥ 53 tests passed, 0 failed
