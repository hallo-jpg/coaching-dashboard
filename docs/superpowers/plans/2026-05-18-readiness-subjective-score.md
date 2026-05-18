# Readiness Score: Objektiv + Subjektiv — Implementierungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Den Readiness-Score um subjektive Wellness-Daten (Ermüdung, Muskelkater, Stress, Verletzung) aus intervals.icu erweitern — Anzeige als Körper/Gefühl-Split im Dashboard und /coach-Output.

**Architecture:** `computeSubjective()` (server.js) + `calc_subjective()` (generate.py) berechnen einen Sub-Score 0–100. `computeReadiness()` kombiniert: Final = objektiv × 0.6 + subjektiv × 0.4. Dashboard-Template erhält neue Template-Variablen für den Gefühl-Abschnitt.

**Tech Stack:** Node.js (MCP server), Python 3.11 (generate.py + Jinja2 template), pytest

---

## Dateiübersicht

| Datei | Änderung |
|---|---|
| `intervals-mcp/server.js` | Neue `computeSubjective()`, `computeReadiness()` erweitern, beide Tools updaten |
| `generate.py` | Sleep-Bug fixen, neue `calc_subjective()`, `calc_readiness()` und `build_context()` erweitern |
| `dashboard.template.html` | Körper/Gefühl-Abschnitte, Verletzungs-Flag |
| `.claude/skills/coach/SKILL.md` | Readiness-Ausgabeformat + Verletzungs-Muster |
| `tests/test_generate.py` | Tests für `calc_subjective()` + neue Keys |

---

## Task 1: API-Feldnamen verifizieren

**Files:**
- Modify: `intervals-mcp/server.js` (temporär, wird wieder entfernt)

- [ ] **Step 1: Debug-Log temporär hinzufügen**

In `server.js`, in der Funktion `get_wellness_range` (um Zeile 853), direkt nach `apiFetch`:

```javascript
async ({ oldest, newest }) => {
  const data = await apiFetch(`/wellness?oldest=${oldest}&newest=${newest}`);
  // TEMP DEBUG — nach Verifikation wieder entfernen
  if (data.length) console.error("WELLNESS_KEYS:", Object.keys(data[data.length - 1]).join(", "));
  const simplified = data.map(d => ({
```

- [ ] **Step 2: MCP-Server neu starten und get_wellness_range aufrufen**

```bash
# MCP server läuft als Subprocess von Claude — restart via: claude mcp restart intervals-icu
# Dann im Claude-Chat aufrufen: get_wellness_range(oldest: "2026-05-18", newest: "2026-05-18")
# Output in stderr: WELLNESS_KEYS: id, ctl, atl, hrv, ...
```

Erwartete Felder basierend auf intervals.icu API-Dokumentation:
`fatigue`, `muscle`, `stress`, `mood`, `motivation`, `injury` (alle lowercase)

- [ ] **Step 3: Debug-Log entfernen, tatsächliche Feldnamen im Plan dokumentieren**

Ersetze `fatigue`/`muscle`/`stress`/`injury` überall im Code durch die verifizierten Namen, falls sie abweichen.

- [ ] **Step 4: Commit**

```bash
git add intervals-mcp/server.js
git commit -m "chore: verify wellness API field names"
```

---

## Task 2: computeSubjective() in server.js

**Files:**
- Modify: `intervals-mcp/server.js` — neue Funktion nach `computeReadiness()` (ca. Zeile 714)

- [ ] **Step 1: Funktion hinzufügen**

Einfügen direkt nach der schließenden `}` von `computeReadiness()` (nach Zeile 714):

```javascript
// Berechnet subjektiven Sub-Score aus Wellness-Einträgen des letzten Tages.
// Felder: fatigue, muscle, stress, injury — alle 1–4-Skala, 1=best.
// Gibt null zurück wenn keine subjektiven Daten vorhanden.
function computeSubjective(data) {
  const latest = data[data.length - 1];
  const fatigue = latest.fatigue ?? null;
  const muscle  = latest.muscle  ?? null;
  const stress  = latest.stress  ?? null;
  const injury  = latest.injury  ?? null;

  if (fatigue == null && muscle == null && stress == null && injury == null) return null;

  // 1–4-Skala, lower=better: (5-value)/4 * maxPts
  const subPts = (value, maxPts) =>
    value != null ? Math.round(((5 - value) / 4) * maxPts) : null;

  const FATIGUE_LABELS  = ["Niedrig", "Durchschn.", "Hoch", "Extrem"];
  const MUSCLE_LABELS   = ["Niedrig", "Durchschn.", "Hoch", "Extrem"];
  const STRESS_LABELS   = ["Niedrig", "Durchschn.", "Hoch", "Extrem"];
  const INJURY_LABELS   = ["Keine ✅", "Niggle", "Schlecht", "Verletzt"];

  // Verletzungs-Sonderregel
  let verletzungFlag = null;
  if (injury === 4) verletzungFlag = "🚨 Verletzt";
  else if (injury === 3) verletzungFlag = "⚠️ Schlecht";
  else if (injury === 2) verletzungFlag = "Niggle";

  let fatiguePts = subPts(fatigue, 35);
  let musclePts  = subPts(muscle,  25);
  let stressPts  = subPts(stress,  25);
  let injuryPts  = subPts(injury,  15);
  if (injury === 3) injuryPts = Math.round(injuryPts / 2); // 50% Abzug
  if (injury === 4) injuryPts = 0;                         // Override

  const fields = [
    { pts: fatiguePts, max: 35 },
    { pts: musclePts,  max: 25 },
    { pts: stressPts,  max: 25 },
    { pts: injuryPts,  max: 15 },
  ].filter(f => f.pts != null);

  const totalPts = fields.reduce((s, f) => s + f.pts, 0);
  const totalMax = fields.reduce((s, f) => s + f.max, 0);
  const score = injury === 4 ? 0 : (totalMax > 0 ? Math.round(totalPts / totalMax * 100) : null);

  return {
    score,
    verletzung_flag: verletzungFlag,
    komponenten: {
      ermuedung:   fatiguePts != null ? { punkte: fatiguePts, max: 35, detail: `${FATIGUE_LABELS[fatigue - 1]} (${fatigue}/4)` } : null,
      muskelkater: musclePts  != null ? { punkte: musclePts,  max: 25, detail: `${MUSCLE_LABELS[muscle - 1]} (${muscle}/4)` }   : null,
      stress:      stressPts  != null ? { punkte: stressPts,  max: 25, detail: `${STRESS_LABELS[stress - 1]} (${stress}/4)` }   : null,
      verletzung:  injuryPts  != null ? { punkte: injuryPts,  max: 15, detail: `${INJURY_LABELS[injury - 1]}` }                 : null,
    },
  };
}
```

- [ ] **Step 2: Manuell verifizieren mit Testdaten**

Direkt nach der Funktion temporär ausführen (Node.js REPL oder kurzer inline-Test):

```javascript
// Erwartet: score=94, verletzung_flag=null
// fatigue=1 → 35/35, muscle=1 → 25/25, stress=2 → 19/25, injury=1 → 15/15
// total=94/100
const testResult = computeSubjective([{ fatigue: 1, muscle: 1, stress: 2, injury: 1 }]);
console.assert(testResult.score === 94, `Expected 94, got ${testResult.score}`);

// Erwartet: verletzung_flag="🚨 Verletzt", score=0
const testVerletzt = computeSubjective([{ fatigue: 1, muscle: 1, stress: 1, injury: 4 }]);
console.assert(testVerletzt.score === 0, `Expected 0, got ${testVerletzt.score}`);
console.assert(testVerletzt.verletzung_flag === "🚨 Verletzt");

// Erwartet: null (keine subjektiven Daten)
const testNull = computeSubjective([{ hrv: 50 }]);
console.assert(testNull === null);
```

- [ ] **Step 3: Commit**

```bash
git add intervals-mcp/server.js
git commit -m "feat(mcp): add computeSubjective() for wellness fields"
```

---

## Task 3: computeReadiness() in server.js integrieren

**Files:**
- Modify: `intervals-mcp/server.js:633–714` (computeReadiness-Funktion)

- [ ] **Step 1: computeReadiness() erweitern**

Die letzten 5 Zeilen von `computeReadiness()` (aktuell Zeilen 695–713) ersetzen:

```javascript
// ALT (ersetzen):
  const score = hrvPts + sleepPts + tsbPts + hrPts;
  let ampel, empfehlung;
  if (score >= 80)      { ampel = "🟢"; empfehlung = "Voll trainieren – alle Einheiten wie geplant."; }
  else if (score >= 60) { ampel = "🟡"; empfehlung = "Planmäßig trainieren, gut beobachten."; }
  else if (score >= 40) { ampel = "🟡"; empfehlung = "Intensität −20% reduzieren, Volumen optional kürzen."; }
  else                  { ampel = "🔴"; empfehlung = "Nur LIT oder Ruhetag – Erholung priorisieren."; }

  return {
    score,
    ampel,
    empfehlung,
    komponenten: {
      hrv:      { punkte: hrvPts,   max: 40, detail: hrvDetail },
      schlaf:   { punkte: sleepPts, max: 25, detail: sleepDetail },
      tsb:      { punkte: tsbPts,   max: 20, detail: tsbDetail },
      ruhepuls: { punkte: hrPts,    max: 15, detail: hrDetail },
    },
    _meta: { hrvDiffSDs, hrDiff, tsbVal: tsb, sleepPts },
  };
}
```

```javascript
// NEU (einsetzen):
  const score_obj = hrvPts + sleepPts + tsbPts + hrPts;
  const subResult = computeSubjective(data);
  const score_sub = subResult?.score ?? null;

  // Kombiniert: 60% objektiv + 40% subjektiv; fallback auf objektiv wenn kein Gefühl
  const score = score_sub != null
    ? Math.round(score_obj * 0.6 + score_sub * 0.4)
    : score_obj;

  // Verletzung-Override: immer 🔴 wenn Verletzt (injury=4)
  let ampel, empfehlung;
  if (subResult?.verletzung_flag === "🚨 Verletzt") {
    ampel = "🔴";
    empfehlung = "🚨 Verletzt – Training pausieren bis zur Erholung.";
  } else if (score >= 80) {
    ampel = "🟢"; empfehlung = "Voll trainieren – alle Einheiten wie geplant.";
  } else if (score >= 60) {
    ampel = "🟡"; empfehlung = "Planmäßig trainieren, gut beobachten.";
  } else if (score >= 40) {
    ampel = "🟡"; empfehlung = "Intensität −20% reduzieren, Volumen optional kürzen.";
  } else {
    ampel = "🔴"; empfehlung = "Nur LIT oder Ruhetag – Erholung priorisieren.";
  }

  return {
    score,
    score_obj,
    score_sub,
    ampel,
    empfehlung,
    verletzung_flag: subResult?.verletzung_flag ?? null,
    komponenten: {
      hrv:      { punkte: hrvPts,   max: 40, detail: hrvDetail },
      schlaf:   { punkte: sleepPts, max: 25, detail: sleepDetail },
      tsb:      { punkte: tsbPts,   max: 20, detail: tsbDetail },
      ruhepuls: { punkte: hrPts,    max: 15, detail: hrDetail },
    },
    komponenten_subjektiv: subResult?.komponenten ?? null,
    _meta: { hrvDiffSDs, hrDiff, tsbVal: tsb, sleepPts },
  };
}
```

- [ ] **Step 2: Commit**

```bash
git add intervals-mcp/server.js
git commit -m "feat(mcp): integrate subjective score into computeReadiness (60/40 split)"
```

---

## Task 4: get_readiness_score und get_wellness_range Tools updaten

**Files:**
- Modify: `intervals-mcp/server.js:776–868`

- [ ] **Step 1: get_readiness_score Tool-Beschreibung + Output updaten**

Zeile 779 (Tool-Beschreibung) ersetzen:

```javascript
// ALT:
  "Readiness-Score (0–100) aus HRV-Trend, Schlaf, TSB und Ruhepuls. Erkennt Krank-Risiko vs. Trainings-Ermüdung, gibt konkrete Workout-Modifikationen für geplante Einheiten und zeigt 7/30-Tage-Verlauf.",

// NEU:
  "Readiness-Score (0–100) aus HRV/Schlaf/TSB/Puls (objektiv, 60%) + Ermüdung/Muskelkater/Stress/Verletzung (subjektiv, 40%). Gibt score_obj, score_sub, ampel, Workout-Empfehlungen und 7/30-Tage-Verlauf zurück.",
```

Zeile 824–838 (JSON return innerhalb des Tools) — `score_obj`, `score_sub`, `verletzung_flag`, `komponenten_subjektiv` ergänzen:

```javascript
// ALT:
        text: JSON.stringify({
          datum: checkDate,
          score,
          ampel,
          empfehlung,
          muster,
          muster_hinweis: hinweis,
          workout_empfehlungen,
          komponenten,
          trend: { ... },
        }, null, 2),

// NEU:
        text: JSON.stringify({
          datum: checkDate,
          score,
          score_obj,
          score_sub,
          ampel,
          empfehlung,
          verletzung_flag,
          muster,
          muster_hinweis: hinweis,
          workout_empfehlungen,
          komponenten,
          komponenten_subjektiv,
          trend: {
            richtung_7d: trendRichtung,
            verlauf_7d:  verlauf7,
            verlauf_30d: verlauf30,
          },
        }, null, 2),
```

Damit das funktioniert, müssen `score_obj`, `score_sub`, `verletzung_flag`, `komponenten_subjektiv` aus dem `computeReadiness()`-Rückgabewert destructured werden. Zeile 796 updaten:

```javascript
// ALT:
    const { score, ampel, empfehlung, komponenten, _meta } = computeReadiness(window7, wellnessAll);

// NEU:
    const { score, score_obj, score_sub, ampel, empfehlung, verletzung_flag,
            komponenten, komponenten_subjektiv, _meta } = computeReadiness(window7, wellnessAll);
```

- [ ] **Step 2: get_wellness_range Tool — subjektive Felder ergänzen**

Zeilen 854–863 (simplified map) ersetzen:

```javascript
// ALT:
    const simplified = data.map(d => ({
      datum: d.id,
      ctl: d.ctl?.toFixed(1),
      atl: d.atl?.toFixed(1),
      tsb: d.ctl && d.atl ? (d.ctl - d.atl).toFixed(1) : null,
      hrv: d.hrv,
      ruhepuls: d.restingHR,
      schlaf_h: d.sleepSecs ? (d.sleepSecs / 3600).toFixed(1) : null,
      schritte: d.steps,
    }));

// NEU:
    const simplified = data.map(d => ({
      datum: d.id,
      ctl: d.ctl?.toFixed(1),
      atl: d.atl?.toFixed(1),
      tsb: d.ctl && d.atl ? (d.ctl - d.atl).toFixed(1) : null,
      hrv: d.hrv,
      ruhepuls: d.restingHR,
      schlaf_h: d.sleepSecs ? (d.sleepSecs / 3600).toFixed(1) : null,
      schlaf_qualitaet: d.sleepQuality ?? null,
      ermuedung: d.fatigue ?? null,
      muskelkater: d.muscle ?? null,
      stress: d.stress ?? null,
      verletzung: d.injury ?? null,
      schritte: d.steps,
    }));
```

- [ ] **Step 3: MCP-Server neu starten und Tool testen**

```bash
# In Claude Chat:
# get_readiness_score() aufrufen → muss score_obj, score_sub, komponenten_subjektiv enthalten
# get_wellness_range(oldest: "2026-05-15", newest: "2026-05-18") → muss ermuedung/muskelkater/stress/verletzung zeigen
```

Erwartetes Ergebnis für heute (18. Mai): `score_obj: 84, score_sub: 94, score: 88`

- [ ] **Step 4: Commit**

```bash
git add intervals-mcp/server.js
git commit -m "feat(mcp): expose score_obj/score_sub/subjektiv fields in readiness + wellness tools"
```

---

## Task 5: generate.py — Sleep-Bug fixen + calc_subjective() hinzufügen

**Files:**
- Modify: `generate.py:109–162` (calc_readiness) und neue Funktion davor
- Modify: `tests/test_generate.py`

- [ ] **Step 1: Sleep-Bug in generate.py fixen**

Zeile 135 in `calc_readiness()`:

```python
# ALT:
        sleep_pts = round(_avg(quality_vals) / 5 * 25)

# NEU (1–4-Skala, lower=better):
        avg_q = _avg(quality_vals)
        sleep_pts = round(((5 - avg_q) / 4) * 25)
```

- [ ] **Step 2: calc_subjective() Funktion hinzufügen**

Direkt vor `calc_readiness()` (vor Zeile 109) einfügen:

```python
def calc_subjective(wellness_window: list[dict]) -> dict | None:
    """Subjektiver Sub-Score aus Ermüdung/Muskelkater/Stress/Verletzung.
    Felder: fatigue, muscle, stress, injury — 1–4-Skala, 1=best.
    Gibt None zurück wenn keine subjektiven Daten vorhanden.
    """
    latest = wellness_window[-1] if wellness_window else {}
    fatigue = latest.get("fatigue")
    muscle  = latest.get("muscle")
    stress  = latest.get("stress")
    injury  = latest.get("injury")

    if all(v is None for v in [fatigue, muscle, stress, injury]):
        return None

    FATIGUE_LABELS = ["Niedrig", "Durchschn.", "Hoch", "Extrem"]
    MUSCLE_LABELS  = ["Niedrig", "Durchschn.", "Hoch", "Extrem"]
    STRESS_LABELS  = ["Niedrig", "Durchschn.", "Hoch", "Extrem"]
    INJURY_LABELS  = ["Keine ✅", "Niggle", "Schlecht", "Verletzt"]

    def sub_pts(value: int | None, max_pts: int) -> int | None:
        if value is None:
            return None
        return round(((5 - value) / 4) * max_pts)

    verletzung_flag = None
    if injury == 4:
        verletzung_flag = "🚨 Verletzt"
    elif injury == 3:
        verletzung_flag = "⚠️ Schlecht"
    elif injury == 2:
        verletzung_flag = "Niggle"

    fatigue_pts = sub_pts(fatigue, 35)
    muscle_pts  = sub_pts(muscle,  25)
    stress_pts  = sub_pts(stress,  25)
    injury_pts  = sub_pts(injury,  15)
    if injury == 3 and injury_pts is not None:
        injury_pts = round(injury_pts / 2)
    if injury == 4:
        injury_pts = 0

    fields = [
        (fatigue_pts, 35), (muscle_pts, 25), (stress_pts, 25), (injury_pts, 15)
    ]
    available = [(p, m) for p, m in fields if p is not None]
    total_pts = sum(p for p, _ in available)
    total_max = sum(m for _, m in available)

    score = 0 if injury == 4 else (round(total_pts / total_max * 100) if total_max else None)

    def comp(value, max_pts, labels, pts):
        if value is None:
            return None
        return {"punkte": pts, "max": max_pts, "detail": f"{labels[value-1]} ({value}/4)"}

    return {
        "score": score,
        "verletzung_flag": verletzung_flag,
        "komponenten": {
            "ermuedung":   comp(fatigue, 35, FATIGUE_LABELS, fatigue_pts),
            "muskelkater": comp(muscle,  25, MUSCLE_LABELS,  muscle_pts),
            "stress":      comp(stress,  25, STRESS_LABELS,  stress_pts),
            "verletzung":  comp(injury,  15, INJURY_LABELS,  injury_pts),
        },
    }
```

- [ ] **Step 3: Tests für calc_subjective() schreiben**

In `tests/test_generate.py` nach dem bestehenden `MOCK_WELLNESS` Block ergänzen:

```python
from generate import calc_subjective

def test_calc_subjective_typical():
    """fatigue=1,muscle=1,stress=2,injury=1 → score=94"""
    result = calc_subjective([{"fatigue": 1, "muscle": 1, "stress": 2, "injury": 1}])
    assert result is not None
    assert result["score"] == 94
    assert result["verletzung_flag"] is None
    assert result["komponenten"]["ermuedung"]["punkte"] == 35
    assert result["komponenten"]["stress"]["punkte"] == 19

def test_calc_subjective_no_data():
    """Keine subjektiven Felder → None"""
    result = calc_subjective([{"hrv": 50, "ctl": 40.0}])
    assert result is None

def test_calc_subjective_verletzt():
    """injury=4 → score=0, verletzung_flag gesetzt"""
    result = calc_subjective([{"fatigue": 1, "muscle": 1, "stress": 1, "injury": 4}])
    assert result["score"] == 0
    assert result["verletzung_flag"] == "🚨 Verletzt"

def test_calc_subjective_partial():
    """Nur fatigue vorhanden → score aus 35/35 Punkten"""
    result = calc_subjective([{"fatigue": 1}])
    assert result is not None
    assert result["score"] == 100
    assert result["komponenten"]["muskelkater"] is None
```

- [ ] **Step 4: Tests ausführen**

```bash
cd "/Users/stefan/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude Code/Coaching"
python -m pytest tests/test_generate.py::test_calc_subjective_typical tests/test_generate.py::test_calc_subjective_no_data tests/test_generate.py::test_calc_subjective_verletzt tests/test_generate.py::test_calc_subjective_partial -v
```

Erwartetes Ergebnis: alle 4 Tests PASSED

- [ ] **Step 5: Commit**

```bash
git add generate.py tests/test_generate.py
git commit -m "feat(generate): fix sleep quality scoring + add calc_subjective()"
```

---

## Task 6: calc_readiness() und build_context() in generate.py integrieren

**Files:**
- Modify: `generate.py:109–162` (calc_readiness return)
- Modify: `generate.py` (build_context — wo r_score berechnet wird, ca. Zeile 796)
- Modify: `tests/test_generate.py`

- [ ] **Step 1: calc_readiness() Rückgabe erweitern**

`calc_readiness()` gibt aktuell einen `int` zurück. Ändern zu `dict`:

```python
# ALT (letztes return in calc_readiness):
    return min(100, hrv_pts + sleep_pts + tsb_pts + hr_pts)

# NEU:
    return min(100, hrv_pts + sleep_pts + tsb_pts + hr_pts)
```

Warte — `calc_readiness` wird an mehreren Stellen als `int` verwendet (z.B. Zeile 856: `pct = calc_readiness([w], hrv_baseline=wellness_30)`). Statt den Rückgabetyp zu ändern, **kombinierten Score separat in build_context berechnen**:

Die Funktion `calc_readiness()` bleibt wie sie ist (gibt `int` zurück). Stattdessen `calc_subjective()` in `build_context()` separat aufrufen.

- [ ] **Step 2: build_context() erweitern**

In `generate.py`, in `build_context()`, direkt nach Zeile 796–798:

```python
# BESTEHEND (nicht ändern):
    r_score = calc_readiness(wellness_30[-7:], hrv_baseline=wellness_30)
    r_color = readiness_color(r_score)
    r_label = readiness_label(r_score)
    r_sub   = _readiness_sub(rhr, hrv, hrv_mean, wellness)

# NEU — nach diesen 4 Zeilen einfügen:
    # Subjektiver Sub-Score
    sub_result = calc_subjective(wellness_30[-7:])
    score_obj  = r_score  # objektiver Score (unverändert)
    score_sub  = sub_result["score"] if sub_result else None
    verletzung_flag = sub_result["verletzung_flag"] if sub_result else None

    # Kombinierter Score: 60% obj + 40% sub (fallback auf obj wenn kein sub)
    if score_sub is not None:
        r_score_combined = round(score_obj * 0.6 + score_sub * 0.4)
        # Verletzung-Override
        if verletzung_flag == "🚨 Verletzt":
            r_score_combined = 0
    else:
        r_score_combined = score_obj

    r_color    = readiness_color(r_score_combined)
    r_label    = readiness_label(r_score_combined)

    # Subjektive Bars für Template
    def _bar(komp):
        if komp is None:
            return None
        pct = round(komp["punkte"] / komp["max"] * 100) if komp["max"] else 0
        color = "#22c55e" if pct >= 75 else "#eab308" if pct >= 50 else "#ef4444"
        return {"detail": komp["detail"], "pct": pct, "color": color}

    subjektiv_bars = None
    if sub_result:
        k = sub_result["komponenten"]
        subjektiv_bars = {
            "ermuedung":   _bar(k.get("ermuedung")),
            "muskelkater": _bar(k.get("muskelkater")),
            "stress":      _bar(k.get("stress")),
            "verletzung":  _bar(k.get("verletzung")),
        }
```

- [ ] **Step 3: Template-Variablen in build_context() ergänzen**

In der `return`-Dict von `build_context()` (ca. Zeile 940) ergänzen:

```python
# Bestehende Zeile:
        "readiness_score": r_score, "readiness_offset": r_offset,
        "readiness_color": r_color, "readiness_label": r_label, "readiness_sub": r_sub,

# NEU ersetzen durch (r_score → r_score_combined):
        "readiness_score": r_score_combined, "readiness_offset": calc_ring_offset(r_score_combined),
        "readiness_color": r_color, "readiness_label": r_label, "readiness_sub": r_sub,
        "score_obj": score_obj, "score_sub": score_sub,
        "verletzung_flag": verletzung_flag,
        "subjektiv_bars": subjektiv_bars,
        "has_subjektiv": subjektiv_bars is not None,
```

- [ ] **Step 4: Test für neue build_context-Keys schreiben**

In `tests/test_generate.py`, `MOCK_WELLNESS` erweitern und neuen Test hinzufügen:

```python
MOCK_WELLNESS_WITH_SUBJEKTIV = [
    {"id": "2026-04-12", "hrv": 40, "sleepSecs": 25200, "ctl": 42.0, "atl": 38.0, "restingHR": 50,
     "fatigue": 1, "muscle": 1, "stress": 2, "injury": 1},
    {"id": "2026-04-13", "hrv": 43, "sleepSecs": 27000, "ctl": 42.5, "atl": 37.0, "restingHR": 49,
     "fatigue": 1, "muscle": 1, "stress": 2, "injury": 1},
    {"id": "2026-04-14", "hrv": 45, "sleepSecs": 28800, "ctl": 43.0, "atl": 36.0, "restingHR": 48,
     "fatigue": 1, "muscle": 1, "stress": 2, "injury": 1},
]

@patch("generate.get_wellness", return_value=MOCK_WELLNESS_WITH_SUBJEKTIV)
@patch("generate.get_activities", return_value=MOCK_ACTIVITIES)
def test_build_context_subjektiv_keys(mock_act, mock_well):
    from generate import build_context
    ctx = build_context(kw=16, monday=date(2026, 4, 13), sunday=date(2026, 4, 19))
    assert "score_obj" in ctx
    assert "score_sub" in ctx
    assert "subjektiv_bars" in ctx
    assert "has_subjektiv" in ctx
    assert "verletzung_flag" in ctx
    assert ctx["has_subjektiv"] is True
    assert ctx["score_sub"] is not None

@patch("generate.get_wellness", return_value=MOCK_WELLNESS)  # kein fatigue/muscle/stress/injury
@patch("generate.get_activities", return_value=MOCK_ACTIVITIES)
def test_build_context_no_subjektiv_fallback(mock_act, mock_well):
    from generate import build_context
    ctx = build_context(kw=16, monday=date(2026, 4, 13), sunday=date(2026, 4, 19))
    assert ctx["has_subjektiv"] is False
    assert ctx["score_sub"] is None
    assert ctx["subjektiv_bars"] is None
    # Readiness fällt auf objektiv zurück
    assert ctx["readiness_score"] == ctx["score_obj"]
```

- [ ] **Step 5: Tests ausführen**

```bash
python -m pytest tests/test_generate.py -v
```

Alle Tests müssen PASSED sein (inkl. bestehende `test_build_context_keys`).

- [ ] **Step 6: Commit**

```bash
git add generate.py tests/test_generate.py
git commit -m "feat(generate): integrate subjective score into build_context (60/40 split)"
```

---

## Task 7: dashboard.template.html — Körper/Gefühl-Abschnitte

**Files:**
- Modify: `dashboard.template.html:798–860` (Readiness-Karte)

- [ ] **Step 1: Zwei Mini-Score-Boxen nach dem Readiness-Score einfügen**

Nach dem `{% endif %}` (Ende des `biometrics_pending`-Blocks, ca. Zeile 816), vor dem HRV-Block (Zeile 818) einfügen:

```html
    {% if has_subjektiv %}
    <div style="display:flex;gap:8px;margin-bottom:12px">
      <div style="flex:1;background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:8px;text-align:center">
        <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px;text-transform:uppercase;letter-spacing:.05em">Körper</div>
        <div style="font-size:1.2rem;font-weight:900;color:var(--text)">{{ score_obj }}</div>
        <div style="font-size:0.55rem;color:var(--muted)">HRV · Schlaf · TSB · Puls</div>
      </div>
      <div style="flex:1;background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);border-radius:8px;padding:8px;text-align:center">
        <div style="font-size:0.58rem;color:var(--muted);margin-bottom:2px;text-transform:uppercase;letter-spacing:.05em">Gefühl</div>
        <div style="font-size:1.2rem;font-weight:900;color:var(--text)">{{ score_sub }}</div>
        <div style="font-size:0.55rem;color:var(--muted)">Ermüdung · Kater · Stress</div>
      </div>
    </div>
    {% endif %}
```

- [ ] **Step 2: Gefühl-Abschnitt nach den Körper-Bars einfügen**

Nach dem schließenden `</div>` des 3er-Grid (nach Zeile 850, Ende der Schlaf/TSB/Puls-Boxen), vor `<div class="sparkline-wrap">` einfügen:

```html
    {% if has_subjektiv %}
    <div style="font-size:0.6rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin:10px 0 6px">── Gefühl</div>
    <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:12px">

      {% if subjektiv_bars.ermuedung %}
      <div>
        <div style="display:flex;justify-content:space-between;margin-bottom:2px">
          <span style="font-size:0.62rem;color:var(--muted)">Ermüdung</span>
          <span style="font-size:0.62rem;color:{{ subjektiv_bars.ermuedung.color }}">{{ subjektiv_bars.ermuedung.detail }}</span>
        </div>
        <div style="background:rgba(255,255,255,0.06);border-radius:3px;height:4px">
          <div style="background:{{ subjektiv_bars.ermuedung.color }};width:{{ subjektiv_bars.ermuedung.pct }}%;height:4px;border-radius:3px"></div>
        </div>
      </div>
      {% endif %}

      {% if subjektiv_bars.muskelkater %}
      <div>
        <div style="display:flex;justify-content:space-between;margin-bottom:2px">
          <span style="font-size:0.62rem;color:var(--muted)">Muskelkater</span>
          <span style="font-size:0.62rem;color:{{ subjektiv_bars.muskelkater.color }}">{{ subjektiv_bars.muskelkater.detail }}</span>
        </div>
        <div style="background:rgba(255,255,255,0.06);border-radius:3px;height:4px">
          <div style="background:{{ subjektiv_bars.muskelkater.color }};width:{{ subjektiv_bars.muskelkater.pct }}%;height:4px;border-radius:3px"></div>
        </div>
      </div>
      {% endif %}

      {% if subjektiv_bars.stress %}
      <div>
        <div style="display:flex;justify-content:space-between;margin-bottom:2px">
          <span style="font-size:0.62rem;color:var(--muted)">Stress</span>
          <span style="font-size:0.62rem;color:{{ subjektiv_bars.stress.color }}">{{ subjektiv_bars.stress.detail }}</span>
        </div>
        <div style="background:rgba(255,255,255,0.06);border-radius:3px;height:4px">
          <div style="background:{{ subjektiv_bars.stress.color }};width:{{ subjektiv_bars.stress.pct }}%;height:4px;border-radius:3px"></div>
        </div>
      </div>
      {% endif %}

      {% if subjektiv_bars.verletzung %}
      <div>
        <div style="display:flex;justify-content:space-between;margin-bottom:2px">
          <span style="font-size:0.62rem;color:var(--muted)">Verletzung</span>
          <span style="font-size:0.62rem;color:{{ subjektiv_bars.verletzung.color }}">
            {{ subjektiv_bars.verletzung.detail }}
            {% if verletzung_flag %}{{ verletzung_flag }}{% endif %}
          </span>
        </div>
        <div style="background:rgba(255,255,255,0.06);border-radius:3px;height:4px">
          <div style="background:{{ subjektiv_bars.verletzung.color }};width:{{ subjektiv_bars.verletzung.pct }}%;height:4px;border-radius:3px"></div>
        </div>
      </div>
      {% endif %}

    </div>
    {% endif %}
```

- [ ] **Step 3: Dashboard lokal testen**

```bash
cd "/Users/stefan/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude Code/Coaching"
INTERVALS_API_KEY=... INTERVALS_ATHLETE_ID=i554154 python generate.py
# Dann http://localhost:8080/docs/dashboard.html aufrufen
```

Prüfen: Körper/Gefühl-Boxen erscheinen, Gefühl-Bars mit korrekten Farben.

- [ ] **Step 4: Commit**

```bash
git add dashboard.template.html docs/dashboard.html
git commit -m "feat(dashboard): add Körper/Gefühl sub-scores to readiness card"
```

---

## Task 8: SKILL.md — Readiness-Ausgabeformat + Verletzungs-Muster

**Files:**
- Modify: `.claude/skills/coach/SKILL.md`

- [ ] **Step 1: Readiness-Ausgabeformat in Schritt 0 updaten**

In SKILL.md, den Abschnitt "Readiness-Score Interpretationslogik" suchen (ca. Zeile mit `Readiness: XX/100`). Das bisherige Format ersetzen:

```
# ALT:
Readiness: XX/100 🟢/🟡/🔴 – [Empfehlung]
Muster: [🟢 Normal / 🟡 Trainings-Ermüdung / 🔴 Krank-Risiko]
Trend (7d): steigend ↑ / stabil / fallend ↓

# NEU:
Readiness: XX/100 🟢/🟡/🔴 – [Empfehlung]
  Körper:  XX 🟢/🟡/🔴  (HRV: [detail] · Schlaf: [detail] · TSB: [detail] · Puls: [detail])
  Gefühl:  XX 🟢/🟡/🔴  (Ermüdung: [detail] · Kater: [detail] · Stress: [detail] · Verletzung: [detail])
  ← Gefühl-Zeile weglassen wenn score_sub == null (kein Eintrag heute)
Muster: [🟢 Normal / 🟡 Trainings-Ermüdung / 🔴 Krank-Risiko]
Trend (7d): steigend ↑ / stabil / fallend ↓
```

- [ ] **Step 2: Verletzungs-Sonderregel in Muster-Logik eintragen**

In der Muster-Logik-Tabelle (Zeile mit `🔴 Krank-Risiko`) eine neue Zeile für Verletzung ergänzen:

```
| Verletzungs-Flag vorhanden | Ausgabe |
|---|---|
| verletzung_flag = "🚨 Verletzt" | 🚨 Im Plan als Warnung ausgeben, kein Training empfehlen, Ampel 🔴 setzen |
| verletzung_flag = "⚠️ Schlecht" | ⚠️ Warnung ausgeben, kein HIT, nur LIT oder Ruhetag |
| verletzung_flag = "Niggle" | 📌 Hinweis ausgeben, Training möglich, bei HIT erste Sätze beobachten |
```

- [ ] **Step 3: Commit + Push**

```bash
git add ".claude/skills/coach/SKILL.md"
git commit -m "feat(skill): update readiness output format with Körper/Gefühl split + Verletzungs-Muster"
git push
```

---

## Self-Review Checklist

- [x] **Spec-Abdeckung:** Alle 5 Spec-Dateien abgedeckt (server.js ×2, generate.py ×2, template, SKILL.md)
- [x] **Keine Platzhalter:** Alle Code-Blöcke vollständig
- [x] **Typen-Konsistenz:** `computeSubjective()` → `calc_subjective()` in Python, gleiche Logik, gleiche Felder
- [x] **Fallback:** Kein subjektiver Score → `has_subjektiv=False`, Template-Blöcke ausgeblendet, Score = Objektiv
- [x] **Sleep-Bug:** In generate.py (Task 5 Step 1) und in server.js (bereits commited vor Plan)
- [x] **API-Feldverifikation:** Task 1 stellt sicher dass `fatigue`/`muscle`/`stress`/`injury` die richtigen Namen sind
- [x] **Tests:** calc_subjective (4 Tests) + build_context (2 neue Tests)
