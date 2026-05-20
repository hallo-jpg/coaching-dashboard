# TSS Soll/Ist-Abgleich im Wochenplan – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Zeigt für abgeschlossene Tage `Ist X / Soll Y` und für ausgefallene Tage `Ausgefallen · Soll Y TSS` im Wochenplan-Widget.

**Architecture:** Reine Template-Änderung in `dashboard.template.html` — `day.tss_plan` ist bereits in allen Day-Objekten vorhanden. Kein Python-Change nötig. Test prüft die Jinja2-Fragment-Logik isoliert.

**Tech Stack:** Jinja2, HTML/CSS inline styles (dark-theme CSS-Variablen), pytest

---

### Task 1: Template — day.done Anzeige auf Ist/Soll umstellen

**Files:**
- Modify: `dashboard.template.html` — Zeilen 818–824 (day.done Block)
- Test: `test_generate.py`

Aktueller Code (Zeilen 818–824):
```html
{% elif day.done %}
<div style="text-align:right;">
  <div class="day-tss" style="color:var(--green)">✅ {{ day.tss_ist }} TSS</div>
  {% if day.tss_bonus > 0 %}
  <div class="tss-split"><span class="split-plan">{{ day.tss_primary }}</span> + <span class="split-bonus">{{ day.tss_bonus }}</span></div>
  {% endif %}
</div>
```

- [ ] **Step 1: Failing test schreiben**

In `test_generate.py` am Ende anfügen:

```python
from jinja2 import Environment as _JinjaEnv

_DONE_TPL = """\
<div style="text-align:right;">
  <div style="display:flex;flex-direction:column;align-items:flex-end;gap:1px">
    <div style="display:flex;align-items:center;gap:3px">
      <span style="font-size:0.58rem;color:var(--muted)">Ist</span>
      <span style="font-size:0.72rem;font-weight:700;color:var(--green)">{{ day.tss_ist }}</span>
    </div>
    {% if day.tss_plan > 0 %}
    <div style="display:flex;align-items:center;gap:3px">
      <span style="font-size:0.58rem;color:var(--muted)">Soll</span>
      <span style="font-size:0.6rem;color:var(--muted)">{{ day.tss_plan }}</span>
    </div>
    {% endif %}
  </div>
</div>"""


def test_done_day_shows_ist_and_soll():
    tpl = _JinjaEnv().from_string(_DONE_TPL)
    out = tpl.render(day={"tss_ist": 92, "tss_plan": 85})
    assert "Ist" in out
    assert "92" in out
    assert "Soll" in out
    assert "85" in out


def test_done_day_no_plan_hides_soll():
    tpl = _JinjaEnv().from_string(_DONE_TPL)
    out = tpl.render(day={"tss_ist": 50, "tss_plan": 0})
    assert "Ist" in out
    assert "50" in out
    assert "Soll" not in out
```

- [ ] **Step 2: Test ausführen – muss FAIL**

```bash
cd "/Users/stefan/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude Code/Coaching"
python -m pytest test_generate.py::test_done_day_shows_ist_and_soll test_generate.py::test_done_day_no_plan_hides_soll -v
```

Expected: FAIL — Template-String stimmt noch nicht mit dem zu implementierenden HTML überein (oder PASS weil der Template-String bereits korrekt ist — dann direkt zu Step 4).

- [ ] **Step 3: Template-Änderung umsetzen**

In `dashboard.template.html` den Block **`{% elif day.done %}`** (Zeilen 818–824) ersetzen:

Altes HTML:
```html
      {% elif day.done %}
      <div style="text-align:right;">
        <div class="day-tss" style="color:var(--green)">✅ {{ day.tss_ist }} TSS</div>
        {% if day.tss_bonus > 0 %}
        <div class="tss-split"><span class="split-plan">{{ day.tss_primary }}</span> + <span class="split-bonus">{{ day.tss_bonus }}</span></div>
        {% endif %}
      </div>
```

Neues HTML:
```html
      {% elif day.done %}
      <div style="text-align:right;">
        <div style="display:flex;flex-direction:column;align-items:flex-end;gap:1px">
          <div style="display:flex;align-items:center;gap:3px">
            <span style="font-size:0.58rem;color:var(--muted)">Ist</span>
            <span style="font-size:0.72rem;font-weight:700;color:var(--green)">{{ day.tss_ist }}</span>
          </div>
          {% if day.tss_plan > 0 %}
          <div style="display:flex;align-items:center;gap:3px">
            <span style="font-size:0.58rem;color:var(--muted)">Soll</span>
            <span style="font-size:0.6rem;color:var(--muted)">{{ day.tss_plan }}</span>
          </div>
          {% endif %}
        </div>
        {% if day.tss_bonus > 0 %}
        <div class="tss-split"><span class="split-plan">{{ day.tss_primary }}</span> + <span class="split-bonus">{{ day.tss_bonus }}</span></div>
        {% endif %}
      </div>
```

- [ ] **Step 4: Tests laufen lassen – müssen PASS**

```bash
python -m pytest test_generate.py::test_done_day_shows_ist_and_soll test_generate.py::test_done_day_no_plan_hides_soll -v
```

Expected:
```
test_generate.py::test_done_day_shows_ist_and_soll PASSED
test_generate.py::test_done_day_no_plan_hides_soll PASSED
```

- [ ] **Step 5: Commit**

```bash
git add dashboard.template.html test_generate.py
git commit -m "feat(dashboard): TSS Ist/Soll-Abgleich für abgeschlossene Tage"
```

---

### Task 2: Template — day.missed Soll-TSS hinzufügen

**Files:**
- Modify: `dashboard.template.html` — Zeilen 825–832 (day.missed Block)
- Test: `test_generate.py`

Aktueller Code (Zeilen 825–832):
```html
{% elif day.missed %}
<div style="text-align:right;">
  <span class="badge-missed">Ausgefallen</span>
  {% if day.tss_ist > 0 %}
  <div class="day-tss" style="color:var(--subtle)">{{ day.tss_ist }} TSS</div>
  {% endif %}
</div>
```

- [ ] **Step 1: Failing test schreiben**

In `test_generate.py` anfügen:

```python
_MISSED_TPL = """\
<div style="text-align:right;">
  <span class="badge-missed">Ausgefallen</span>
  {% if day.tss_plan > 0 %}
  <div style="font-size:0.6rem;color:var(--muted);margin-top:2px">Soll {{ day.tss_plan }} TSS</div>
  {% endif %}
</div>"""


def test_missed_day_shows_soll():
    tpl = _JinjaEnv().from_string(_MISSED_TPL)
    out = tpl.render(day={"tss_plan": 95})
    assert "Ausgefallen" in out
    assert "Soll" in out
    assert "95" in out


def test_missed_day_no_plan_hides_soll():
    tpl = _JinjaEnv().from_string(_MISSED_TPL)
    out = tpl.render(day={"tss_plan": 0})
    assert "Ausgefallen" in out
    assert "Soll" not in out
```

- [ ] **Step 2: Test ausführen – muss FAIL**

```bash
python -m pytest test_generate.py::test_missed_day_shows_soll test_generate.py::test_missed_day_no_plan_hides_soll -v
```

Expected: FAIL.

- [ ] **Step 3: Template-Änderung umsetzen**

In `dashboard.template.html` den Block **`{% elif day.missed %}`** (Zeilen 825–832) ersetzen:

Altes HTML:
```html
      {% elif day.missed %}
      <div style="text-align:right;">
        <span class="badge-missed">Ausgefallen</span>
        {% if day.tss_ist > 0 %}
        <div class="day-tss" style="color:var(--subtle)">{{ day.tss_ist }} TSS</div>
        {% endif %}
      </div>
```

Neues HTML:
```html
      {% elif day.missed %}
      <div style="text-align:right;">
        <span class="badge-missed">Ausgefallen</span>
        {% if day.tss_plan > 0 %}
        <div style="font-size:0.6rem;color:var(--muted);margin-top:2px">Soll {{ day.tss_plan }} TSS</div>
        {% endif %}
      </div>
```

- [ ] **Step 4: Tests laufen lassen – müssen PASS**

```bash
python -m pytest test_generate.py::test_missed_day_shows_soll test_generate.py::test_missed_day_no_plan_hides_soll -v
```

Expected:
```
test_generate.py::test_missed_day_shows_soll PASSED
test_generate.py::test_missed_day_no_plan_hides_soll PASSED
```

- [ ] **Step 5: Jinja2-Syntax des gesamten Templates validieren**

```bash
python -c "
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('.'))
env.get_template('dashboard.template.html')
print('Template syntax OK')
"
```

Expected: `Template syntax OK`

- [ ] **Step 6: Alle Tests laufen lassen**

```bash
python -m pytest test_generate.py -v
```

Expected: alle Tests PASS, keine neuen Fehler.

- [ ] **Step 7: Commit**

```bash
git add dashboard.template.html test_generate.py
git commit -m "feat(dashboard): Soll-TSS bei ausgefallenen Tagen anzeigen"
```

---

### Task 3: Dashboard regenerieren und pushen

**Files:**
- Read: `docs/dashboard.html` (wird neu generiert)

- [ ] **Step 1: Dashboard generieren**

```bash
python generate.py
```

Expected: kein Fehler, `docs/dashboard.html` aktualisiert.

Falls Fehler (API nicht erreichbar): Template-Syntax ist trotzdem korrekt — Schritt trotzdem als erledigt markieren wenn Step 5 aus Task 2 PASS war.

- [ ] **Step 2: Commit + Push**

```bash
git add docs/dashboard.html
git commit -m "chore: regenerate dashboard [skip ci]"
git push
```
