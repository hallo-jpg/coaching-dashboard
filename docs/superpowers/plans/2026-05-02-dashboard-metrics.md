# Dashboard-Metriken: Monotony, Ramprate, PMC Forward View (M1 · M2 · D1) – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Three new dashboard elements: Training Monotony + Strain card (M1), ATL Ramprate indicator in Readiness card (M2), and PMC Forward View card projecting CTL/TSB to race day KW24 (D1).

**Architecture:** New pure functions in `generate.py`, new context keys in `build_context()`, new HTML sections in `dashboard.template.html`. Uses existing data already fetched (`polar_acts`, `wellness_30`, `parse_kw_plan`).

**Tech Stack:** Python 3 (no new dependencies — uses existing `_avg`, `_std_dev` helpers), Jinja2, HTML/CSS.

---

## File Map

| File | Änderung |
|---|---|
| `generate.py` | 4 neue Funktionen + `build_context()` erweitern |
| `dashboard.template.html` | 3 neue/erweiterte HTML-Blöcke |
| `tests/test_generate.py` | 7 neue Unit-Tests |

---

### Task 1: M1 – `calc_monotony_strain()` in generate.py

**Files:**
- Modify: `generate.py`
- Test: `tests/test_generate.py`

- [ ] **Schritt 1: Failing test schreiben**

  In `tests/test_generate.py` nach dem letzten Import `from generate import ...` den Import erweitern:
  ```python
  from generate import calc_ring_offset, calc_readiness, week_date_range, fmt_tsb_color, parse_kw_plan, match_activities, build_day_rows, _calc_polarisation, calc_monotony_strain
  ```

  Dann Tests anfügen:
  ```python
  def test_calc_monotony_strain_varied():
      # Variierte Woche: niedrige Monotony
      # Mo=100, Di=0 (Ruhe), Mi=80, Do=0 (Ruhe), Fr=90, Sa=120, So=60
      daily = [100, 0, 80, 0, 90, 120, 60]
      result = calc_monotony_strain(daily)
      assert result["monotony"] < 1.5, f"Expected monotony < 1.5, got {result['monotony']}"
      assert result["strain"] == round(sum(daily) * result["monotony"])

  def test_calc_monotony_strain_uniform():
      # Gleichförmige Woche: hohe Monotony
      daily = [80, 80, 80, 80, 80, 80, 80]
      result = calc_monotony_strain(daily)
      assert result["monotony"] > 2.0, f"Expected monotony > 2.0 (uniform week), got {result['monotony']}"

  def test_calc_monotony_strain_rest_day():
      # Ruhetag senkt Monotony
      uniform = calc_monotony_strain([80, 80, 80, 80, 80, 80, 80])
      with_rest = calc_monotony_strain([80, 0, 80, 80, 80, 80, 80])
      assert with_rest["monotony"] < uniform["monotony"]
  ```

- [ ] **Schritt 2: Tests ausführen und Fehler bestätigen**

  ```bash
  cd /Users/stefan/Documents/Claude\ Code/Coaching
  python -m pytest tests/test_generate.py::test_calc_monotony_strain_varied tests/test_generate.py::test_calc_monotony_strain_uniform tests/test_generate.py::test_calc_monotony_strain_rest_day -v 2>&1 | head -20
  ```

  Erwartete Ausgabe: `ERROR` (ImportError weil Funktion noch nicht existiert).

- [ ] **Schritt 3: `calc_monotony_strain()` in generate.py implementieren**

  In `generate.py` direkt nach `def _std_dev()` (nach Zeile ~37) einfügen:

  ```python
  def calc_monotony_strain(daily_tss: list[float]) -> dict:
      """Training Monotony + Strain (Foster et al. 2001).
      Monotony = mean/std; Strain = sum × monotony. High monotony (>2) = overtraining risk."""
      n = len(daily_tss) or 1
      mean = sum(daily_tss) / n
      std = _std_dev(daily_tss) if len(daily_tss) >= 2 else 0.01
      monotony = round(mean / max(std, 0.01), 2)
      strain = int(sum(daily_tss) * monotony)
      if mean == 0:
          monotony = 0.0
          strain = 0
      return {"monotony": monotony, "strain": strain}
  ```

- [ ] **Schritt 4: Tests ausführen und grün bestätigen**

  ```bash
  python -m pytest tests/test_generate.py::test_calc_monotony_strain_varied tests/test_generate.py::test_calc_monotony_strain_uniform tests/test_generate.py::test_calc_monotony_strain_rest_day -v
  ```

  Erwartete Ausgabe: `3 passed`.

- [ ] **Schritt 5: Commit**

  ```bash
  git add generate.py tests/test_generate.py
  git commit -m "feat(generate): calc_monotony_strain() – Foster Monotony + Strain"
  ```

---

### Task 2: M2 – `calc_ramprate()` in generate.py

**Files:**
- Modify: `generate.py`
- Test: `tests/test_generate.py`

- [ ] **Schritt 1: Failing tests schreiben**

  Import in tests erweitern:
  ```python
  from generate import ..., calc_monotony_strain, calc_ramprate
  ```

  Tests anfügen:
  ```python
  def test_calc_ramprate_normal():
      # ATL heute=45, ATL vor 7d=38 → ramprate=+7.0
      w30 = [{"id": f"2026-04-{i:02d}", "atl": 38.0 + i * 0.0} for i in range(1, 24)]
      w30.append({"id": "2026-04-25", "atl": 45.0})
      assert calc_ramprate(w30) == pytest.approx(7.0, abs=0.5)

  def test_calc_ramprate_alert():
      # ATL heute=52, ATL vor 7d=38 → ramprate=+14 → Alarm
      w30 = [{"id": f"2026-04-{i:02d}", "atl": 38.0} for i in range(1, 25)]
      result = calc_ramprate(w30[:17] + [{"id": "2026-04-25", "atl": 52.0}])
      assert result > 7.0

  def test_calc_ramprate_insufficient_data():
      # Zu wenig Daten → 0.0
      assert calc_ramprate([{"id": "2026-04-25", "atl": 45.0}]) == 0.0
  ```

- [ ] **Schritt 2: Tests ausführen und Fehler bestätigen**

  ```bash
  python -m pytest tests/test_generate.py::test_calc_ramprate_normal tests/test_generate.py::test_calc_ramprate_alert tests/test_generate.py::test_calc_ramprate_insufficient_data -v 2>&1 | head -15
  ```

  Erwartete Ausgabe: `ERROR` (ImportError).

- [ ] **Schritt 3: `calc_ramprate()` in generate.py implementieren**

  Direkt nach `calc_monotony_strain()` einfügen:

  ```python
  def calc_ramprate(wellness_history: list[dict]) -> float:
      """ATL change over last 7 days. >7 = elevated, >10 = too fast (injury risk)."""
      atl_entries = [(w["id"][:10], w["atl"]) for w in wellness_history if w.get("atl") and w.get("id")]
      if len(atl_entries) < 8:
          return 0.0
      atl_today = atl_entries[-1][1]
      atl_7d_ago = atl_entries[-8][1]
      return round(atl_today - atl_7d_ago, 1)
  ```

- [ ] **Schritt 4: Tests grün**

  ```bash
  python -m pytest tests/test_generate.py::test_calc_ramprate_normal tests/test_generate.py::test_calc_ramprate_alert tests/test_generate.py::test_calc_ramprate_insufficient_data -v
  ```

  Erwartete Ausgabe: `3 passed`.

- [ ] **Schritt 5: Commit**

  ```bash
  git add generate.py tests/test_generate.py
  git commit -m "feat(generate): calc_ramprate() – ATL 7-day delta"
  ```

---

### Task 3: D1 – `project_pmc()` + `parse_planned_tss_from_kw_files()` in generate.py

**Files:**
- Modify: `generate.py`
- Test: `tests/test_generate.py`

- [ ] **Schritt 1: Failing test schreiben**

  Import erweitern:
  ```python
  from generate import ..., calc_ramprate, project_pmc
  ```

  Tests anfügen:
  ```python
  def test_project_pmc_on_track():
      # CTL=65, ATL=70, Renntag in 42 Tagen, 400 TSS/Woche geplant → TSB sollte positiv werden durch Taper
      from datetime import date, timedelta
      race_date = date.today() + timedelta(days=42)
      # Woche 1-5: 400 TSS/Woche, Woche 6: Taper 200 TSS
      today = date.today()
      monday = today - timedelta(days=today.weekday())
      planned = [(monday + timedelta(weeks=i), 400 if i < 5 else 200) for i in range(6)]
      result = project_pmc(ctl_today=65.0, atl_today=70.0, planned_weekly_tss=planned, race_date=race_date)
      assert "ctl_race" in result
      assert "tsb_race" in result
      assert "tsb_status" in result
      assert isinstance(result["ctl_race"], float)

  def test_project_pmc_no_data():
      # Keine Planungsdaten → CTL verfällt, TSB steigt
      from datetime import date, timedelta
      race_date = date.today() + timedelta(days=14)
      result = project_pmc(ctl_today=65.0, atl_today=70.0, planned_weekly_tss=[], race_date=race_date)
      assert result["tsb_race"] > 0  # ATL fällt schneller als CTL ohne Training
  ```

- [ ] **Schritt 2: Tests ausführen und Fehler bestätigen**

  ```bash
  python -m pytest tests/test_generate.py::test_project_pmc_on_track tests/test_generate.py::test_project_pmc_no_data -v 2>&1 | head -15
  ```

  Erwartete Ausgabe: `ERROR` (ImportError).

- [ ] **Schritt 3: `project_pmc()` in generate.py implementieren**

  Direkt nach `calc_ramprate()` einfügen:

  ```python
  def project_pmc(ctl_today: float, atl_today: float,
                  planned_weekly_tss: list[tuple],
                  race_date: date) -> dict:
      """Project CTL/ATL/TSB forward to race_date using planned weekly TSS.
      Banister decay: CTL τ=42d, ATL τ=7d. Starts from tomorrow (today already in ctl_today)."""
      # Build day→daily_tss map (weekly TSS distributed evenly)
      daily_map: dict[str, float] = {}
      for week_start, total_tss in planned_weekly_tss:
          daily_avg = total_tss / 7
          for d in range(7):
              day = (week_start + timedelta(days=d)) if isinstance(week_start, date) else date.fromisoformat(week_start) + timedelta(days=d)
              daily_map[day.isoformat()] = daily_avg

      ctl, atl = ctl_today, atl_today
      current = date.today() + timedelta(days=1)
      while current <= race_date:
          daily_tss = daily_map.get(current.isoformat(), 0.0)
          ctl = ctl * (1 - 1/42) + daily_tss / 42
          atl = atl * (1 - 1/7) + daily_tss / 7
          current += timedelta(days=1)

      tsb_race = round(ctl - atl, 1)
      if 5 <= tsb_race <= 25:
          status = "on_track"
      elif tsb_race > 25:
          status = "too_fresh"
      else:
          status = "too_tired"
      return {"ctl_race": round(ctl, 1), "atl_race": round(atl, 1),
              "tsb_race": tsb_race, "tsb_status": status}
  ```

- [ ] **Schritt 4: `parse_planned_tss_from_kw_files()` implementieren**

  Direkt nach `project_pmc()` einfügen:

  ```python
  def parse_planned_tss_from_kw_files(from_kw: int, to_kw: int, year: int) -> list[tuple]:
      """Read planned weekly TSS from kw-plan files for PMC projection.
      Returns list of (monday_date, tss_float) for each KW with a parseable tss_plan."""
      result = []
      for kw in range(from_kw, to_kw + 1):
          plan = parse_kw_plan(kw)
          tss = plan.get("tss_plan", 0)
          if tss > 0:
              monday, _ = week_date_range(kw, year)
              result.append((monday, float(tss)))
      return result
  ```

- [ ] **Schritt 5: Tests grün**

  ```bash
  python -m pytest tests/test_generate.py::test_project_pmc_on_track tests/test_generate.py::test_project_pmc_no_data -v
  ```

  Erwartete Ausgabe: `2 passed`.

- [ ] **Schritt 6: Alle bisherigen Tests bestätigen**

  ```bash
  python -m pytest tests/test_generate.py -v 2>&1 | tail -5
  ```

  Erwartete Ausgabe: Alle Tests `passed`, keine `FAILED`.

- [ ] **Schritt 7: Commit**

  ```bash
  git add generate.py tests/test_generate.py
  git commit -m "feat(generate): project_pmc() + parse_planned_tss_from_kw_files() für PMC Forward View"
  ```

---

### Task 4: build_context() um M1, M2, D1 erweitern

**Files:**
- Modify: `generate.py`

- [ ] **Schritt 1: M1-Tages-TSS-Aggregation in build_context() hinzufügen**

  In `build_context()` suche die Zeile:
  ```python
  polar_acts = get_activities(
      (date.today() - timedelta(7)).isoformat(),
      date.today().isoformat()
  )
  ```

  Direkt **nach** `polar = _calc_polarisation(polar_acts)` einfügen:

  ```python
  # M1: Training Monotony + Strain (last 7 days)
  _daily_tss_map: dict[str, float] = {}
  for _act in polar_acts:
      _d = _act.get("start_date_local", "")[:10]
      _daily_tss_map[_d] = _daily_tss_map.get(_d, 0) + float(_act.get("icu_training_load") or 0)
  _tss_7days = [
      _daily_tss_map.get((date.today() - timedelta(days=6 - i)).isoformat(), 0.0)
      for i in range(7)
  ]
  monotony_data = calc_monotony_strain(_tss_7days)
  monotony_val      = monotony_data["monotony"]
  monotony_strain   = monotony_data["strain"]
  monotony_color    = ("var(--green)" if monotony_val < 1.5
                       else "var(--yellow)" if monotony_val < 2.0
                       else "var(--accent)")

  # M2: ATL Ramprate (from wellness_30 ATL history)
  ramprate = calc_ramprate(wellness_30)
  ramprate_color = ("var(--accent)"  if ramprate > 10
                    else "var(--yellow)" if ramprate > 7
                    else "var(--green)"  if ramprate >= 0
                    else "var(--blue)")
  ramprate_icon = "⚠️" if ramprate > 7 else ("🔴" if ramprate > 10 else "")
  ```

- [ ] **Schritt 2: D1-PMC-Projektion in build_context() hinzufügen**

  Direkt nach dem M2-Block einfügen:

  ```python
  # D1: PMC Forward View (project to RadRace KW24)
  _current_year = monday.year
  _planned_tss = parse_planned_tss_from_kw_files(kw + 1, RACE_KW, _current_year)
  _race_monday, _ = week_date_range(RACE_KW, _current_year)
  _race_date = _race_monday + timedelta(days=4)  # Friday of race week (TT day)
  pmc_forecast = project_pmc(ctl, atl, _planned_tss, _race_date)
  _tsb_s = pmc_forecast["tsb_race"]
  pmc_tsb_color = ("var(--green)"  if 5 <= _tsb_s <= 25
                   else "var(--yellow)" if -5 <= _tsb_s < 5 or 25 < _tsb_s <= 35
                   else "var(--accent)")
  pmc_tsb_label = ("✅ auf Kurs" if pmc_forecast["tsb_status"] == "on_track"
                   else "⚠️ zu wenig getapert" if pmc_forecast["tsb_status"] == "too_tired"
                   else "⚠️ zu frisch")
  pmc_available = bool(_planned_tss)
  ```

- [ ] **Schritt 3: Alle neuen Keys zum return-Dict hinzufügen**

  Im `return`-Dict (letzte Zeile von `build_context()`), nach `"tss_summary": tss_summary,` hinzufügen:

  ```python
  "monotony_val":    monotony_val,
  "monotony_strain": monotony_strain,
  "monotony_color":  monotony_color,
  "tss_7days":       _tss_7days,
  "ramprate":        ramprate,
  "ramprate_color":  ramprate_color,
  "ramprate_icon":   ramprate_icon,
  "pmc_ctl_race":    pmc_forecast["ctl_race"],
  "pmc_tsb_race":    pmc_forecast["tsb_race"],
  "pmc_tsb_color":   pmc_tsb_color,
  "pmc_tsb_label":   pmc_tsb_label,
  "pmc_available":   pmc_available,
  "race_kw":         RACE_KW,
  ```

- [ ] **Schritt 4: Build_context Test erweitern**

  In `tests/test_generate.py`, die `required_keys`-Liste in `test_build_context_keys` um neue Keys erweitern:

  ```python
  "monotony_val", "monotony_strain", "monotony_color",
  "ramprate", "ramprate_color",
  "pmc_ctl_race", "pmc_tsb_race", "pmc_tsb_label", "pmc_available",
  ```

- [ ] **Schritt 5: Alle Tests ausführen**

  ```bash
  python -m pytest tests/test_generate.py -v 2>&1 | tail -10
  ```

  Erwartete Ausgabe: Alle Tests `passed`.

- [ ] **Schritt 6: Commit**

  ```bash
  git add generate.py tests/test_generate.py
  git commit -m "feat(generate): build_context – M1 Monotony, M2 Ramprate, D1 PMC Forward View"
  ```

---

### Task 5: Dashboard-Template – M1 Load Quality Karte

**Files:**
- Modify: `dashboard.template.html`

- [ ] **Schritt 1: Bestehende Trainingsform-Karte im Template finden**

  Öffne `dashboard.template.html` und suche nach dem Block der die CTL/ATL/TSB-Karte enthält (suche nach `ctl_offset` oder `"Trainingsform"`). Merke dir die Stelle direkt **nach** diesem Card-Block.

- [ ] **Schritt 2: CSS für Load Quality Karte hinzufügen**

  Im `<style>`-Block des Templates (nach den vorhandenen Card-Styles) hinzufügen:

  ```css
  /* M1 Load Quality */
  .lq-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
  .lq-label { font-size: 0.72rem; color: var(--muted); }
  .lq-val { font-size: 0.88rem; font-weight: 700; }
  .lq-bars { display: flex; align-items: flex-end; gap: 2px; height: 24px; margin-top: 8px; }
  .lq-bar { flex: 1; border-radius: 2px 2px 0 0; min-height: 2px; }
  ```

- [ ] **Schritt 3: Load Quality Karte HTML einfügen**

  Direkt nach dem Ende der Trainingsform-Karte (nach dem schließenden `</div>` des Cards) einfügen:

  ```html
  <!-- M1: Load Quality Card -->
  <div class="card">
    <div class="card-title">Load Quality</div>
    <div style="margin-top: 10px;">
      <div class="lq-row">
        <span class="lq-label">Monotony</span>
        <span class="lq-val" style="color: {{ monotony_color }}">{{ "%.2f"|format(monotony_val) }}</span>
      </div>
      <div class="lq-row">
        <span class="lq-label">Strain</span>
        <span class="lq-val">{{ monotony_strain }}</span>
      </div>
      <div class="lq-label" style="margin-top: 6px; margin-bottom: 3px;">Letzte 7 Tage TSS</div>
      <div class="lq-bars">
        {% set max_tss = tss_7days | max %}
        {% for tss in tss_7days %}
        <div class="lq-bar"
             style="height: {{ [((tss / max_tss * 100) | round | int), 5] | max }}%;
                    background: {{ 'var(--green)' if tss > 0 else 'var(--subtle)' }};
                    opacity: 0.7;"
             title="{{ tss | round | int }} TSS"></div>
        {% endfor %}
      </div>
    </div>
  </div>
  ```

  **Hinweis:** Wenn `max_tss` 0 ist (keine Aktivitäten), würde Division durch 0 entstehen. Absicherung in Template:
  ```html
  {% set max_tss = [tss_7days | max, 1] | max %}
  ```
  Diese Zeile ersetzt die obige `{% set max_tss ... %}` Zeile.

- [ ] **Schritt 4: Commit**

  ```bash
  git add dashboard.template.html
  git commit -m "feat(template): M1 Load Quality Karte – Monotony + Strain"
  ```

---

### Task 6: Dashboard-Template – M2 Ramprate in Readiness Card

**Files:**
- Modify: `dashboard.template.html`

- [ ] **Schritt 1: Readiness Card im Template finden**

  Suche nach dem Block der `tsb_bar_val` anzeigt (TSB-Zeile in der Readiness-Card). Das ist die Stelle direkt nach der TSB-Zeile.

- [ ] **Schritt 2: ATL Δ7d Zeile einfügen**

  Direkt nach der TSB-Zeile (dem `<div>` der `tsb_bar_val` enthält), **innerhalb der Readiness-Card**, einfügen:

  ```html
  <!-- M2: ATL Ramprate -->
  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
    <span style="font-size: 0.72rem; color: var(--muted);">ATL Δ7d</span>
    <span style="font-size: 0.82rem; font-weight: 700; color: {{ ramprate_color }};">
      {{ "%+.1f"|format(ramprate) }}
      {% if ramprate_icon %} {{ ramprate_icon }}{% endif %}
    </span>
  </div>
  ```

- [ ] **Schritt 3: Commit**

  ```bash
  git add dashboard.template.html
  git commit -m "feat(template): M2 ATL Ramprate in Readiness Card"
  ```

---

### Task 7: Dashboard-Template – D1 PMC Forward View Karte

**Files:**
- Modify: `dashboard.template.html`

- [ ] **Schritt 1: Einfügepunkt finden**

  Suche die CTL-History-Karte (die SVG-Linienchart mit `ctl_history`). Die neue Rennprognose-Karte wird direkt **nach** dieser Karte eingefügt.

- [ ] **Schritt 2: CSS für Rennprognose ergänzen**

  Im `<style>`-Block hinzufügen:

  ```css
  /* D1 PMC Forward View */
  .forecast-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; }
  .forecast-label { font-size: 0.72rem; color: var(--muted); }
  .forecast-val { font-size: 1.1rem; font-weight: 800; }
  .forecast-sub { font-size: 0.65rem; color: var(--muted); margin-top: 4px; }
  ```

- [ ] **Schritt 3: Rennprognose Card HTML einfügen**

  ```html
  <!-- D1: PMC Forward View -->
  {% if pmc_available %}
  <div class="card">
    <div class="card-title">Rennprognose 🏁 KW{{ race_kw }}</div>
    <div style="margin-top: 10px;">
      <div class="forecast-row">
        <span class="forecast-label">CTL Renntag</span>
        <span class="forecast-val">~{{ pmc_ctl_race }}</span>
      </div>
      <div class="forecast-row">
        <span class="forecast-label">TSB Renntag</span>
        <span class="forecast-val" style="color: {{ pmc_tsb_color }};">
          {{ "%+.1f"|format(pmc_tsb_race) }}
        </span>
      </div>
      <div class="forecast-sub">{{ pmc_tsb_label }}</div>
      <div class="forecast-sub" style="margin-top: 6px;">Ziel TSB: +5 bis +25 · Basis: Plan wie vorgesehen</div>
    </div>
  </div>
  {% endif %}
  ```

- [ ] **Schritt 4: Commit**

  ```bash
  git add dashboard.template.html
  git commit -m "feat(template): D1 PMC Forward View Karte – CTL/TSB Rennprognose"
  ```

---

### Task 8: Integration testen + Dashboard regenerieren

**Files:**
- Run: `generate.py` lokal

- [ ] **Schritt 1: Alle Tests grün**

  ```bash
  python -m pytest tests/test_generate.py -v 2>&1 | tail -5
  ```

  Erwartete Ausgabe: Alle Tests `passed`.

- [ ] **Schritt 2: Dashboard lokal generieren**

  ```bash
  python generate.py
  ```

  Erwartete Ausgabe: Kein Traceback, `docs/dashboard.html` wird neu erstellt.

- [ ] **Schritt 3: HTML auf Fehler prüfen**

  ```bash
  grep -c "undefined\|None\|Error\|Traceback" docs/dashboard.html || echo "Keine offensichtlichen Fehler"
  ```

- [ ] **Schritt 4: Finaler Push**

  ```bash
  git add docs/dashboard.html
  git commit -m "chore: regenerate dashboard mit M1/M2/D1"
  git pull --rebase && git push
  ```
