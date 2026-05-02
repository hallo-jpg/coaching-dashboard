# Bonus-Aktivitäten im Wochenplan – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Alle aufgezeichneten Aktivitäten erscheinen im Wochenplan-Dashboard; nicht geplante Aktivitäten werden mit einem `+`-Badge und Split-TSS kenntlich gemacht.

**Architecture:** `match_activities()` wird erweitert um Sport-Typ-Matching (primäre vs. Bonus-Aktivität). `build_day_rows()` gibt neue Felder `bonus_activities`, `tss_primary`, `tss_bonus` weiter. Das Jinja2-Template rendert Bonus-Zeilen und einen TSS-Split.

**Tech Stack:** Python 3, Jinja2, pytest, intervals.icu activity types

---

## Files

| File | Change |
|---|---|
| `generate.py` | Modify `match_activities`, `build_day_rows`; add `_plan_sport` helper |
| `dashboard.template.html` | Bonus-Zeile + TSS-Split im Wochenplan-Block |
| `tests/test_generate.py` | Neue Tests für Bonus-Matching; bestehende Tests bleiben grün |

---

### Task 1: `_plan_sport` helper + `match_activities` refactor

**Files:**
- Modify: `generate.py` (Funktionen `match_activities` ab Zeile 518, neue Hilfsfunktion davor)
- Test: `tests/test_generate.py`

- [ ] **Step 1: Schreibe die failing Tests**

Füge am Ende von `tests/test_generate.py` nach den bestehenden `test_match_activities_*`-Tests ein:

```python
# ── Bonus-Aktivitäten ────────────────────────────────────────────────────────

SAMPLE_ACTIVITIES_WITH_BONUS = [
    # Wandern früh (Hike = nicht im SPORT_TYPE_MAP → immer Bonus)
    {"start_date_local": "2026-04-13T07:00:00", "type": "Hike",
     "icu_training_load": 32, "name": "Morgenwanderung"},
    # Rad am Nachmittag → primär (passt zu Plan-Typ ride)
    {"start_date_local": "2026-04-13T15:00:00", "type": "Ride",
     "icu_training_load": 88, "name": "HIT 4×8min"},
    # Wandern an Ruhetag (Mi)
    {"start_date_local": "2026-04-15T10:00:00", "type": "Hike",
     "icu_training_load": 25, "name": "Wandern Ruhetag"},
]


def test_match_activities_bonus_ride_day():
    """Hike früh + Ride nachmittags → Ride ist primär, Hike ist Bonus."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES_WITH_BONUS, SAMPLE_PLAN_DAYS, monday)
    mo = matched["Mo"]
    assert mo["primary"] is not None
    assert mo["primary"]["name"] == "HIT 4×8min"
    assert mo["primary"]["tss"] == 88
    assert len(mo["bonus"]) == 1
    assert mo["bonus"][0]["name"] == "Morgenwanderung"
    assert mo["bonus"][0]["tss"] == 32
    assert mo["tss_ist"] == 120
    assert mo["done"] is True


def test_match_activities_bonus_rest_day():
    """Aktivität an Ruhetag → alles Bonus, done bleibt False."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES_WITH_BONUS, SAMPLE_PLAN_DAYS, monday)
    mi = matched["Mi"]
    assert mi["primary"] is None
    assert len(mi["bonus"]) == 1
    assert mi["bonus"][0]["name"] == "Wandern Ruhetag"
    assert mi["tss_ist"] == 25
    assert mi["done"] is False


def test_match_activities_primary_structure():
    """Rückgabe enthält primary/bonus/tss_ist/done für alle Tage."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    for tag in ["Mo", "Di", "Mi", "Do"]:
        assert "primary" in matched[tag]
        assert "bonus" in matched[tag]
        assert "tss_ist" in matched[tag]
        assert "done" in matched[tag]


def test_match_activities_existing_compatibility():
    """Bestehende Tests-Felder (tss_ist, done) bleiben korrekt."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    assert matched["Mo"]["tss_ist"] == 71
    assert matched["Mo"]["done"] is True
    assert matched["Do"]["tss_ist"] == 48
    assert matched["Do"]["done"] is True
    assert matched["Di"]["done"] is False
    assert matched["Di"]["tss_ist"] == 0
```

- [ ] **Step 2: Tests ausführen – müssen FAIL**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
python -m pytest tests/test_generate.py::test_match_activities_bonus_ride_day tests/test_generate.py::test_match_activities_bonus_rest_day tests/test_generate.py::test_match_activities_primary_structure -v
```

Erwartet: `FAILED` mit `KeyError: 'primary'` o.ä.

- [ ] **Step 3: `_plan_sport` Helper und neues `match_activities` implementieren**

In `generate.py` ersetze den Block ab `def match_activities(` (Zeile 518–541) mit:

```python
def _plan_sport(day: dict) -> str:
    """Return expected sport type string for a plan day."""
    if day.get("is_run"):
        return "run"
    if day.get("is_kraft"):
        return "strength"
    return "ride"


def match_activities(activities: list, plan_days: list, monday: date) -> dict:
    """Match activities to plan days by date and sport type.

    Returns {tag: {primary, bonus, tss_ist, done}} where:
      primary: {name, tss} of the activity matching the plan sport, or None
      bonus:   [{name, tss}, ...] for all other activities on that day
      tss_ist: total TSS (primary + all bonus)
      done:    True when primary activity was completed
    """
    date_to_tag = {
        (monday + timedelta(days=i)).isoformat(): DAY_ORDER[i]
        for i in range(7)
    }
    plan_by_tag = {d["tag"]: d for d in plan_days}

    matched = {
        d["tag"]: {"primary": None, "bonus": [], "tss_ist": 0, "done": False}
        for d in plan_days
    }

    for act in sorted(activities, key=lambda a: a.get("start_date_local", "")):
        act_date = act.get("start_date_local", "")[:10]
        tag = date_to_tag.get(act_date)
        if not tag:
            continue
        tss = act.get("icu_training_load") or 0
        matched[tag]["tss_ist"] += tss

        plan_day = plan_by_tag[tag]
        act_sport = SPORT_TYPE_MAP.get(act.get("type", ""))

        if (
            not plan_day["rest"]
            and act_sport == _plan_sport(plan_day)
            and matched[tag]["primary"] is None
        ):
            matched[tag]["primary"] = {"name": act.get("name", ""), "tss": tss}
            matched[tag]["done"] = True
        else:
            matched[tag]["bonus"].append({"name": act.get("name", ""), "tss": tss})

    return matched
```

- [ ] **Step 4: Tests ausführen – müssen PASS**

```bash
python -m pytest tests/test_generate.py -v
```

Erwartet: alle Tests grün, inkl. der neuen und der bestehenden `test_match_activities_*`.

- [ ] **Step 5: Commit**

```bash
git add generate.py tests/test_generate.py
git commit -m "feat: match_activities erkennt primäre vs. Bonus-Aktivitäten per Sport-Typ"
```

---

### Task 2: `build_day_rows` um Bonus-Felder erweitern

**Files:**
- Modify: `generate.py` (Funktion `build_day_rows`, Zeile 544–586)
- Test: `tests/test_generate.py`

- [ ] **Step 1: Failing Tests schreiben**

Füge in `tests/test_generate.py` nach `test_build_day_rows` ein:

```python
def test_build_day_rows_bonus_fields_present():
    """build_day_rows liefert bonus_activities, tss_primary, tss_bonus."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES, SAMPLE_PLAN_DAYS, monday)
    rows = build_day_rows(SAMPLE_PLAN_DAYS, matched)
    mo = rows[0]
    assert "bonus_activities" in mo
    assert "tss_primary" in mo
    assert "tss_bonus" in mo
    assert mo["bonus_activities"] == []
    assert mo["tss_primary"] == 71
    assert mo["tss_bonus"] == 0


def test_build_day_rows_bonus_ride_day():
    """Bei Bonus-Aktivität korrekte Felder im Row-Dict."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES_WITH_BONUS, SAMPLE_PLAN_DAYS, monday)
    rows = build_day_rows(SAMPLE_PLAN_DAYS, matched)
    mo = rows[0]  # Mo: Ride primär (88 TSS) + Hike Bonus (32 TSS)
    assert mo["tss_ist"] == 120
    assert mo["tss_primary"] == 88
    assert mo["tss_bonus"] == 32
    assert len(mo["bonus_activities"]) == 1
    assert mo["bonus_activities"][0]["name"] == "Morgenwanderung"
    assert mo["done"] is True


def test_build_day_rows_bonus_rest_day():
    """An Ruhetag mit Aktivität: done=False, bonus_activities gefüllt."""
    monday = date(2026, 4, 13)
    matched = match_activities(SAMPLE_ACTIVITIES_WITH_BONUS, SAMPLE_PLAN_DAYS, monday)
    rows = build_day_rows(SAMPLE_PLAN_DAYS, matched)
    mi = rows[2]  # Mi ist Ruhetag
    assert mi["rest"] is True
    assert mi["done"] is False
    assert len(mi["bonus_activities"]) == 1
    assert mi["tss_bonus"] == 25
    assert mi["tss_primary"] == 0
```

- [ ] **Step 2: Tests ausführen – müssen FAIL**

```bash
python -m pytest tests/test_generate.py::test_build_day_rows_bonus_fields_present tests/test_generate.py::test_build_day_rows_bonus_ride_day tests/test_generate.py::test_build_day_rows_bonus_rest_day -v
```

Erwartet: `FAILED` mit `KeyError: 'bonus_activities'`.

- [ ] **Step 3: `build_day_rows` erweitern**

In `generate.py` ersetze den `rows.append({...})` Block in `build_day_rows` (Zeile 572–585):

```python
        primary = m.get("primary")
        bonus   = m.get("bonus", [])
        tss_primary = primary["tss"] if primary else 0
        tss_bonus   = sum(b["tss"] for b in bonus)

        rows.append({
            "tag":              tag,
            "workout":          day["workout"],
            "tss_plan":         day["tss_plan"],
            "tss_ist":          m["tss_ist"],
            "tss_primary":      tss_primary,
            "tss_bonus":        tss_bonus,
            "done":             done,
            "rest":             rest,
            "missed":           missed,
            "is_run":           day["is_run"],
            "is_kraft":         day.get("is_kraft", False),
            "dot_class":        dot,
            "row_class":        row_class,
            "activity_name":    primary["name"] if primary else "",
            "bonus_activities": bonus,
        })
```

Direkt davor muss auch die Default-Fallback-Zeile aktualisiert werden (Zeile 549):

```python
        m = matched.get(tag, {"primary": None, "bonus": [], "tss_ist": 0, "done": False})
```

- [ ] **Step 4: Tests ausführen – alle grün**

```bash
python -m pytest tests/test_generate.py -v
```

Erwartet: alle Tests grün.

- [ ] **Step 5: Commit**

```bash
git add generate.py tests/test_generate.py
git commit -m "feat: build_day_rows liefert bonus_activities, tss_primary, tss_bonus"
```

---

### Task 3: Template – Bonus-Zeile und TSS-Split rendern

**Files:**
- Modify: `dashboard.template.html` (CSS-Block ~Zeile 157–185, Wochenplan-Block ~Zeile 566–588)

- [ ] **Step 1: CSS für Bonus-Elemente hinzufügen**

In `dashboard.template.html`, füge nach der Zeile `.badge-missed { ... }` (ca. Zeile 159) ein:

```css
  .bonus-activity { display: flex; align-items: center; gap: 6px; margin-top: 5px; padding-top: 5px; border-top: 1px dashed var(--border); }
  .badge-bonus { font-size: 0.58rem; font-weight: 800; color: var(--orange); background: rgba(255,107,53,0.1); border: 1px solid rgba(255,107,53,0.25); border-radius: 5px; padding: 1px 5px; flex-shrink: 0; }
  .bonus-name { font-size: 0.75rem; color: var(--subtle); }
  .tss-split { font-size: 0.65rem; color: #4a5568; white-space: nowrap; }
  .tss-split .split-plan { color: var(--subtle); }
  .tss-split .split-bonus { color: var(--orange); }
```

- [ ] **Step 2: Wochenplan-Block im Template ersetzen**

Ersetze den `{% for day in days %}...{% endfor %}` Block (Zeile 566–587) mit:

```html
    {% for day in days %}
    <div class="day-row {{ day.row_class }}">
      <span class="day-name">{{ day.tag }}</span>
      <span class="day-dot {{ day.dot_class }}"></span>
      <div>
        {% if day.rest %}
        <div class="day-workout" style="color:var(--subtle);font-weight:400;{% if day.bonus_activities %}text-decoration:line-through;{% endif %}">Ruhetag</div>
        {% else %}
        <div class="day-workout">{% if day.is_run %}🏃{% elif day.is_kraft %}🏋️{% else %}🚴{% endif %} {{ day.workout }}</div>
        {% endif %}
        {% for bonus in day.bonus_activities %}
        <div class="bonus-activity">
          <span class="badge-bonus">+</span>
          <span class="bonus-name">{{ bonus.name }}</span>
        </div>
        {% endfor %}
      </div>
      {% if day.rest and day.bonus_activities %}
      <span class="day-tss" style="color:var(--orange)">+{{ day.tss_bonus }} TSS</span>
      {% elif day.rest %}
      <span class="day-tss" style="color:var(--subtle)">–</span>
      {% elif day.done %}
      <div style="text-align:right;">
        <div class="day-tss" style="color:var(--green)">✅ {{ day.tss_ist }} TSS</div>
        {% if day.tss_bonus > 0 %}
        <div class="tss-split"><span class="split-plan">{{ day.tss_primary }}</span> + <span class="split-bonus">{{ day.tss_bonus }}</span></div>
        {% endif %}
      </div>
      {% elif day.missed %}
      <span class="badge-missed">Ausgefallen</span>
      {% else %}
      <span class="day-tss">{% if day.tss_plan > 0 %}~{{ day.tss_plan }} TSS{% else %}–{% endif %}</span>
      {% endif %}
    </div>
    {% endfor %}
```

- [ ] **Step 3: Dashboard regenerieren und visuell prüfen**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
python generate.py
```

Erwartet: kein Python-Fehler, `docs/dashboard.html` wird aktualisiert.

Öffne `docs/dashboard.html` im Browser und prüfe:
- Normaler Trainingstag (kein Bonus): Anzeige unverändert
- Ruhetag ohne Aktivität: zeigt `–`
- (Wenn gestern's Wandern noch in der aktuellen KW liegt) Ruhetag mit Wandern: durchgestrichenes "Ruhetag" + `+ Wandern` + `+32 TSS` in Orange
- Trainingstag mit Bonus: ✅ Gesamt-TSS + split `88 + 32` darunter

- [ ] **Step 4: Alle Tests nochmals ausführen**

```bash
python -m pytest tests/test_generate.py -v
```

Erwartet: alle grün.

- [ ] **Step 5: Commit**

```bash
git add dashboard.template.html
git commit -m "feat: Wochenplan zeigt Bonus-Aktivitäten mit + Badge und TSS-Split"
```

---

### Task 4: Dashboard neu generieren und pushen

**Files:**
- Modify: `docs/dashboard.html` (auto-generiert)

- [ ] **Step 1: Finales Generate**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
python generate.py
```

- [ ] **Step 2: Finaler Test-Lauf**

```bash
python -m pytest tests/test_generate.py -v
```

Erwartet: alle Tests grün.

- [ ] **Step 3: Commit und Push**

```bash
git add docs/dashboard.html
git commit -m "chore: regenerate dashboard mit Bonus-Aktivitäten"
git push
```
