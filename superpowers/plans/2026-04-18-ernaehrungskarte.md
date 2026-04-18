# Ernährungs-Karte Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tagestyp-basierte Ernährungskarte im Dashboard direkt nach dem Readiness Score, zeigt Protein-Ziel, Pre/During/Post-Timing und 2 kontextuelle Tipps.

**Architecture:** Neue Funktion `get_nutrition_context()` in `generate.py` klassifiziert den heutigen Tag aus dem bestehenden Wochenplan und liefert alle Ernährungsdaten. Kein neuer API-Call. Ergebnis als `nutrition`-Key im Template-Kontext. Neue Karte in `dashboard.template.html` direkt nach dem Readiness-Score-Block.

**Tech Stack:** Python 3.9, Jinja2 — keine neuen Dependencies.

---

## File Structure

- Modify: `generate.py` — Neue Konstante `NUTRITION_CONFIG`, neue Funktionen `_classify_day_type()`, `_protein_dist()`, `get_nutrition_context()`, Einbindung in `build_context()`
- Modify: `tests/test_generate.py` — 5 neue Tests
- Modify: `dashboard.template.html` — Neue CSS-Klassen + neue Ernährungs-Karte nach Readiness-Card
- Modify: `docs/dashboard.html` — Wird durch `python3 generate.py` neu generiert

---

### Task 1: Nutrition-Klassifikation und Protein-Berechnung

**Files:**
- Modify: `generate.py` (nach Zeile 124, nach `get_power_bests()`)
- Modify: `tests/test_generate.py`

- [ ] **Step 1: Schreibe die failing Tests**

Füge am Ende von `tests/test_generate.py` ein:

```python
from generate import _classify_day_type, _protein_dist, get_nutrition_context


def test_classify_day_type_intense():
    day = {"workout": "SwSp 3×10", "tss_plan": 72, "rest": False}
    assert _classify_day_type(day, sick=False) == "intense"


def test_classify_day_type_endurance_long():
    day = {"workout": "LIT-3h", "tss_plan": 111, "rest": False}
    assert _classify_day_type(day, sick=False) == "endurance_long"


def test_classify_day_type_rest():
    day = {"workout": "–", "tss_plan": 0, "rest": True}
    assert _classify_day_type(day, sick=False) == "rest"


def test_classify_day_type_sick():
    day = {"workout": "LIT-2h", "tss_plan": 74, "rest": False}
    assert _classify_day_type(day, sick=True) == "sick"


def test_protein_dist_sums_correctly():
    dist = _protein_dist(180)
    # Extract numbers and sum — should be close to 180
    import re
    total = sum(int(re.search(r"\d+", s).group()) for s in dist)
    assert abs(total - 180) <= 20  # rounding to 5g may shift ±20g
```

- [ ] **Step 2: Tests laufen lassen — sie müssen FAIL**

```bash
python3 -m pytest tests/test_generate.py::test_classify_day_type_intense -v
```

Expected: `FAILED` mit `ImportError: cannot import name '_classify_day_type'`

- [ ] **Step 3: Implementiere `NUTRITION_CONFIG`, `_classify_day_type()`, `_protein_dist()` in `generate.py`**

Füge direkt nach `get_power_bests()` (nach Zeile 123) ein:

```python
ATHLETE_WEIGHT_KG = 88

NUTRITION_CONFIG: dict = {
    "intense": {
        "protein_gkg": 2.0,
        "banner_color": "orange",
        "day_sub": "Intensiver Tag → Carbs + Protein hoch",
        "pre":    {"emoji": "🍌", "title": "Leicht",   "sub": "Banane, Toast, 90min vorher"},
        "during": {"emoji": "🍫", "title": "30–60g",   "sub": "Gel oder Riegel ab 45min"},
        "post":   {"emoji": "🥛", "title": "3:1",      "sub": "Carbs:Protein in 30min"},
        "tips": [
            {"color": "green",  "text": "Anti-entzündlich: Beeren, Omega-3 — unterstützt Anpassung"},
            {"color": "orange", "text": "Hydration: +500ml heute Abend, morgens Elektrolyte"},
        ],
    },
    "endurance_long": {
        "protein_gkg": 1.9,
        "banner_color": "orange",
        "day_sub": "Langer Ausdauertag → Kohlenhydrat-Fokus",
        "pre":    {"emoji": "🍝", "title": "Carbs",    "sub": "Pasta, Reis, 2–3h vorher"},
        "during": {"emoji": "🍫", "title": "60–90g/h", "sub": "Alle 20min essen/trinken"},
        "post":   {"emoji": "🥛", "title": "4:1",      "sub": "Carbs:Protein in 30min"},
        "tips": [
            {"color": "orange", "text": "Laden: Kohlenhydratspeicher voll auffüllen"},
            {"color": "green",  "text": "Hydration: 500ml extra + Elektrolyte vor dem Start"},
        ],
    },
    "endurance_short": {
        "protein_gkg": 1.8,
        "banner_color": "blue",
        "day_sub": "Kurzer Ausdauertag → Normal essen",
        "pre":    {"emoji": "🥣", "title": "Normal",   "sub": "Haferbrei, 1–2h vorher"},
        "during": {"emoji": "💧", "title": "Optional", "sub": "Wasser reicht bis 90min"},
        "post":   {"emoji": "🥛", "title": "3:1",      "sub": "Carbs:Protein in 30min"},
        "tips": [
            {"color": "green", "text": "Protein-Fokus: Quark, Eier, Hülsenfrüchte nach dem Training"},
            {"color": "blue",  "text": "Leichte Mahlzeiten — kein Volumen-Druck bei kurzen Einheiten"},
        ],
    },
    "rest": {
        "protein_gkg": 1.7,
        "banner_color": "muted",
        "day_sub": "Ruhetag → Carbs reduziert, Protein halten",
        "pre": None, "during": None, "post": None,
        "tips": [
            {"color": "green",  "text": "Carbs reduzieren: Mehr Gemüse, weniger Getreide heute"},
            {"color": "purple", "text": "Magnesium abends: 300–400mg unterstützt Schlafqualität"},
        ],
    },
    "sick": {
        "protein_gkg": 1.8,
        "banner_color": "red",
        "day_sub": "Krank → Leicht essen, viel trinken",
        "pre": None, "during": None, "post": None,
        "tips": [
            {"color": "blue",  "text": "Leicht essen — kein Druck, Appetit bestimmt die Menge"},
            {"color": "green", "text": "Viel trinken: Wasser, Tee, Brühe — Immunsystem unterstützen"},
        ],
    },
}


def _classify_day_type(day: dict, sick: bool) -> str:
    if sick:
        return "sick"
    workout = (day.get("workout") or "").lower()
    if day.get("rest") or workout in ("–", "-", "ruhetag", ""):
        return "rest"
    if any(k in workout for k in ("swsp", "hit", "vo2", "ka", "intervall", "eb")):
        return "intense"
    if "lit" in workout and (day.get("tss_plan") or 0) >= 80:
        return "endurance_long"
    return "endurance_short"


def _protein_dist(protein_g: int) -> list:
    def r5(x: float) -> int:
        return round(x / 5) * 5
    return [
        f"~{r5(protein_g * 0.25)}g Frühstück",
        f"~{r5(protein_g * 0.30)}g Mittagessen",
        f"~{r5(protein_g * 0.25)}g Abendessen",
        f"~{r5(protein_g * 0.20)}g Snacks",
    ]


def get_nutrition_context(today_day: dict, sick: bool) -> dict:
    day_type = _classify_day_type(today_day, sick)
    cfg = NUTRITION_CONFIG[day_type]
    protein_g = round(cfg["protein_gkg"] * ATHLETE_WEIGHT_KG / 5) * 5
    workout = today_day.get("workout") or "Ruhetag"
    return {
        "day_type":     day_type,
        "day_label":    workout,
        "day_sub":      cfg["day_sub"],
        "banner_color": cfg["banner_color"],
        "protein_g":    protein_g,
        "protein_gkg":  cfg["protein_gkg"],
        "protein_dist": _protein_dist(protein_g),
        "pre":          cfg["pre"],
        "during":       cfg["during"],
        "post":         cfg["post"],
        "tips":         cfg["tips"],
    }
```

- [ ] **Step 4: Tests laufen lassen — alle PASS**

```bash
python3 -m pytest tests/test_generate.py::test_classify_day_type_intense tests/test_generate.py::test_classify_day_type_endurance_long tests/test_generate.py::test_classify_day_type_rest tests/test_generate.py::test_classify_day_type_sick tests/test_generate.py::test_protein_dist_sums_correctly -v
```

Expected: 5 Tests PASSED

- [ ] **Step 5: Commit**

```bash
git add generate.py tests/test_generate.py
git commit -m "feat: nutrition classification and protein calculation with tests"
```

---

### Task 2: `get_nutrition_context` in `build_context` einbinden

**Files:**
- Modify: `generate.py` (Zeile 401–424, `return {…}` in `build_context`)
- Modify: `tests/test_generate.py`

- [ ] **Step 1: Schreibe den failing Test**

Füge am Ende von `tests/test_generate.py` ein:

```python
@patch("generate.get_wellness", return_value=MOCK_WELLNESS)
@patch("generate.get_activities", return_value=MOCK_ACTIVITIES)
@patch("generate.get_power_bests", return_value=[])
def test_build_context_has_nutrition(mock_pb, mock_act, mock_well):
    from generate import build_context
    ctx = build_context(kw=16, monday=date(2026, 4, 13), sunday=date(2026, 4, 19))
    assert "nutrition" in ctx
    n = ctx["nutrition"]
    assert "day_type" in n
    assert "protein_g" in n
    assert isinstance(n["protein_g"], int)
    assert n["protein_g"] > 0
    assert "tips" in n
    assert len(n["tips"]) == 2
```

- [ ] **Step 2: Test laufen lassen — muss FAIL**

```bash
python3 -m pytest tests/test_generate.py::test_build_context_has_nutrition -v
```

Expected: `FAILED` mit `AssertionError: assert 'nutrition' in {...}`

- [ ] **Step 3: `nutrition` in `build_context` einbinden**

In `generate.py`, finde den `return {…}` Block in `build_context` (aktuell Zeile 401–424). Füge direkt vor dem `return` folgende Zeilen ein und ergänze `"nutrition"` im return-dict:

```python
    # Heute's Tag aus days ermitteln
    today_tag = DAY_ORDER[date.today().weekday()]
    today_day_plan = next((d for d in days if d["tag"] == today_tag),
                          {"workout": "", "tss_plan": 0, "rest": True})
    nutrition = get_nutrition_context(today_day_plan, bool(sick_notice))
```

Dann im `return {…}` Block nach `"power_bests": get_power_bests(),` hinzufügen:

```python
        "nutrition": nutrition,
```

- [ ] **Step 4: Test laufen lassen — PASS**

```bash
python3 -m pytest tests/test_generate.py::test_build_context_has_nutrition -v
```

Expected: PASSED

- [ ] **Step 5: Alle Tests laufen lassen**

```bash
python3 -m pytest tests/test_generate.py -v
```

Expected: Alle Tests PASSED (jetzt 24 Tests)

- [ ] **Step 6: Commit**

```bash
git add generate.py tests/test_generate.py
git commit -m "feat: wire nutrition context into build_context"
```

---

### Task 3: Ernährungs-Karte ins Template + Dashboard generieren

**Files:**
- Modify: `dashboard.template.html`
- Modify: `docs/dashboard.html` (generiert)

- [ ] **Step 1: CSS-Klassen für die Ernährungs-Karte hinzufügen**

In `dashboard.template.html`, füge direkt vor `footer { margin-top: 28px; …` (aktuell ca. Zeile 234) folgende CSS-Blöcke ein:

```css
  /* ── ERNÄHRUNGS-KARTE ── */
  .nutr-card { background: var(--surface); border-radius: 16px; padding: 18px; margin-bottom: 12px; }
  .nutr-banner {
    border-radius: 10px; padding: 10px 12px; margin-bottom: 14px;
    display: flex; align-items: center; gap: 10px;
  }
  .nutr-banner-orange { background: linear-gradient(135deg,rgba(249,115,22,0.12),rgba(249,115,22,0.04)); border: 1px solid rgba(249,115,22,0.18); }
  .nutr-banner-blue   { background: linear-gradient(135deg,rgba(79,142,247,0.12),rgba(79,142,247,0.04)); border: 1px solid rgba(79,142,247,0.18); }
  .nutr-banner-red    { background: linear-gradient(135deg,rgba(239,68,68,0.12),rgba(239,68,68,0.04)); border: 1px solid rgba(239,68,68,0.18); }
  .nutr-banner-muted  { background: var(--surface2); border: 1px solid var(--border); }
  .nutr-banner-text  { font-size: 0.76rem; font-weight: 700; }
  .nutr-banner-sub   { font-size: 0.6rem; color: var(--muted); margin-top: 1px; }
  .nutr-banner-orange .nutr-banner-text { color: var(--orange, #f97316); }
  .nutr-banner-blue   .nutr-banner-text { color: var(--accent); }
  .nutr-banner-red    .nutr-banner-text { color: var(--red, #ef4444); }
  .nutr-banner-muted  .nutr-banner-text { color: var(--muted); }

  .nutr-protein {
    background: linear-gradient(135deg,rgba(62,207,142,0.1),rgba(62,207,142,0.04));
    border: 1px solid rgba(62,207,142,0.2);
    border-radius: 10px; padding: 10px 12px; margin-bottom: 14px;
    display: flex; align-items: center; justify-content: space-between;
  }
  .nutr-protein-left { display: flex; align-items: center; gap: 8px; }
  .nutr-protein-icon { font-size: 1.1rem; }
  .nutr-protein-lbl  { font-size: 0.62rem; color: var(--muted); }
  .nutr-protein-val  { font-size: 1.1rem; font-weight: 900; color: var(--green); }
  .nutr-protein-unit { font-size: 0.6rem; color: var(--muted); font-weight: 400; }
  .nutr-protein-dist { font-size: 0.56rem; color: var(--muted); text-align: right; line-height: 1.6; }

  .nutr-timing { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 14px; }
  .nutr-timing-block { background: var(--surface2); border-radius: 10px; padding: 10px 8px; text-align: center; }
  .nutr-timing-lbl  { font-size: 0.5rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 4px; }
  .nutr-timing-main { font-size: 0.7rem; font-weight: 700; margin-bottom: 3px; }
  .nutr-timing-sub  { font-size: 0.56rem; color: var(--muted); line-height: 1.3; }

  .nutr-tip { display: flex; align-items: flex-start; gap: 8px; padding: 5px 0; border-bottom: 1px solid var(--border); }
  .nutr-tip:last-child { border-bottom: none; }
  .nutr-tip-dot { width: 6px; height: 6px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
  .nutr-tip-dot-green  { background: var(--green); }
  .nutr-tip-dot-orange { background: var(--orange, #f97316); }
  .nutr-tip-dot-blue   { background: var(--accent); }
  .nutr-tip-dot-purple { background: var(--purple); }
  .nutr-tip-text { font-size: 0.66rem; color: var(--muted); line-height: 1.4; }
```

- [ ] **Step 2: Karte im Template einfügen**

In `dashboard.template.html`, finde den Block `<!-- POLARISATION -->` (aktuell ca. Zeile 501). Füge direkt **davor** (also nach `</div>` das die Readiness-Card schließt, Zeile 499) folgendes ein:

```html
    <!-- ERNÄHRUNG -->
    {% if nutrition %}
    <div class="nutr-card">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
        <div class="section-label" style="margin:0">Ernährung · Heute</div>
        <span class="kw-pill" style="margin-left:auto">{{ nutrition.day_type }}</span>
      </div>

      <div class="nutr-banner nutr-banner-{{ nutrition.banner_color }}">
        <div>
          <div class="nutr-banner-text">{{ nutrition.day_label }}</div>
          <div class="nutr-banner-sub">{{ nutrition.day_sub }}</div>
        </div>
      </div>

      <div class="nutr-protein">
        <div class="nutr-protein-left">
          <div class="nutr-protein-icon">🥚</div>
          <div>
            <div class="nutr-protein-lbl">Protein-Ziel heute</div>
            <div><span class="nutr-protein-val">{{ nutrition.protein_g }}</span><span class="nutr-protein-unit"> g · {{ nutrition.protein_gkg }} g/kg</span></div>
          </div>
        </div>
        <div class="nutr-protein-dist">
          {% for line in nutrition.protein_dist %}{{ line }}<br>{% endfor %}
        </div>
      </div>

      {% if nutrition.pre %}
      <div class="nutr-timing">
        <div class="nutr-timing-block">
          <div class="nutr-timing-lbl">Pre-Workout</div>
          <div class="nutr-timing-main">{{ nutrition.pre.emoji }} {{ nutrition.pre.title }}</div>
          <div class="nutr-timing-sub">{{ nutrition.pre.sub }}</div>
        </div>
        <div class="nutr-timing-block">
          <div class="nutr-timing-lbl">During</div>
          <div class="nutr-timing-main">{{ nutrition.during.emoji }} {{ nutrition.during.title }}</div>
          <div class="nutr-timing-sub">{{ nutrition.during.sub }}</div>
        </div>
        <div class="nutr-timing-block">
          <div class="nutr-timing-lbl">Post · 30min</div>
          <div class="nutr-timing-main">{{ nutrition.post.emoji }} {{ nutrition.post.title }}</div>
          <div class="nutr-timing-sub">{{ nutrition.post.sub }}</div>
        </div>
      </div>
      {% endif %}

      <div>
        {% for tip in nutrition.tips %}
        <div class="nutr-tip">
          <div class="nutr-tip-dot nutr-tip-dot-{{ tip.color }}"></div>
          <div class="nutr-tip-text">{{ tip.text }}</div>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}
```

- [ ] **Step 3: Dashboard neu generieren**

```bash
INTERVALS_API_KEY=... INTERVALS_ATHLETE_ID=... python3 generate.py
```

Expected: `✓ docs/dashboard.html generated for KW16`

- [ ] **Step 4: Prüfen dass keine Jinja2-Platzhalter mehr übrig sind**

```bash
grep -c "{{" docs/dashboard.html
```

Expected: `0`

- [ ] **Step 5: Prüfen dass die Ernährungs-Karte im Output vorhanden ist**

```bash
grep "Ernährung" docs/dashboard.html
grep "Protein-Ziel" docs/dashboard.html
```

Expected: Beide Zeilen geben Treffer zurück.

- [ ] **Step 6: Commit**

```bash
git add dashboard.template.html docs/dashboard.html
git commit -m "feat: nutrition card in dashboard — today's type, protein goal, timing, tips"
```

- [ ] **Step 7: Push**

```bash
git push
```
