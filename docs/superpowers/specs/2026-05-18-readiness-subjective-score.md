# Spec: Zweigleisiger Readiness-Score (Objektiv + Subjektiv)

*Erstellt: 18. Mai 2026*

## Ziel

Den Readiness-Score von einem rein physiologischen Messwert (HRV/Schlaf/TSB/Puls) zu einem vollständigeren Bild erweitern, das auch Stefan's subjektives Belastungsgefühl einschließt. Daten dafür sind bereits in intervals.icu vorhanden — sie werden bisher nur nicht genutzt.

## Kontext & Ausgangslage

- intervals.icu Wellness-Formular enthält: Schlafqualität, Muskelkater, Ermüdung, Stress, Stimmung, Motivation, Verletzung — alle auf 1–4-Skala (1=best)
- Der MCP-Server (`intervals-mcp/server.js`) liest davon nur `sleepQuality` — rest wird ignoriert
- Das Dashboard (`generate.py`) hat eine eigene Readiness-Darstellung, die ebenfalls nur objektive Daten nutzt
- Stefan trägt täglich alle relevanten Felder ein (Schlafqualität, Ermüdung+Muskelkater, Stress, Verletzung)
- Bereits gefixt (18.05.2026): Schlaf-Scoring war invertiert — `avgQ/5` statt `(5−avgQ)/4`

## Design: Score-Architektur

### Zwei Sub-Scores

```
Objektiv-Score  (Gewicht 60%):
  HRV       → 40 Punkte  (unverändert)
  Schlaf    → 25 Punkte  (bereits gefixt)
  TSB       → 20 Punkte  (unverändert)
  Ruhepuls  → 15 Punkte  (unverändert)
  Gesamt:     100 Punkte → skaliert auf 0–100

Subjektiv-Score (Gewicht 40%):
  Ermüdung    → 35 Punkte  (stärkster subjektiver Prädiktor)
  Muskelkater → 25 Punkte
  Stress      → 25 Punkte
  Verletzung  → 15 Punkte  + Sonderregel
  Gesamt:       100 Punkte → skaliert auf 0–100

Final = objektiv × 0.6 + subjektiv × 0.4
```

### Scoring-Formel (alle subjektiven Felder, 1–4-Skala, lower=better)

```javascript
pts = Math.round(((5 - value) / 4) * maxPts)
// value=1 → 100%  |  value=2 → 75%  |  value=3 → 50%  |  value=4 → 25%
```

### Sonderregel Verletzung

| Wert | Label | Auswirkung |
|---|---|---|
| 1 | Keine | Normal |
| 2 | Niggle | Hinweis im Output, kein Score-Abzug |
| 3 | Schlecht | ⚠️ Warnung + Subjektiv-Punkte halbieren |
| 4 | Verletzt | 🚨 Override → Ampel immer 🔴, Empfehlung: Pause |

### Fallback: Keine subjektiven Daten

Wenn Stefan an einem Tag keine Wellness-Felder eingetragen hat → subjektiver Score wird nicht berechnet. Final-Score = nur Objektiv-Score (wie bisher). Ausgabe zeigt: `(nur Körperdaten — Gefühlsdaten heute nicht eingetragen)`.

## Betroffene Dateien

### 1. `intervals-mcp/server.js` — `computeReadiness()`

**Änderungen:**
- Neue Funktion `computeSubjective(data)` → berechnet Subjektiv-Score aus `fatigue`, `muscle`, `stress`, `injury`
- `computeReadiness()` ruft beide auf und kombiniert sie
- Rückgabe erweitern um: `score_obj`, `score_sub`, `komponenten_subjektiv`, `verletzung_flag`

**Neue Ausgabe-Felder:**
```json
{
  "score": 88,
  "score_obj": 84,
  "score_sub": 94,
  "ampel": "🟢",
  "verletzung_flag": null,
  "komponenten": { ... },
  "komponenten_subjektiv": {
    "ermuedung": { "punkte": 35, "max": 35, "detail": "Niedrig (1/4)" },
    "muskelkater": { "punkte": 25, "max": 25, "detail": "Niedrig (1/4)" },
    "stress": { "punkte": 19, "max": 25, "detail": "Durchschnitt (2/4)" },
    "verletzung": { "punkte": 15, "max": 15, "detail": "Keine ✅" }
  }
}
```

### 2. `intervals-mcp/server.js` — `get_wellness_range`

**Änderungen:**
- Neue Felder im Output: `ermuedung`, `muskelkater`, `stress`, `verletzung`
- API-Feldnamen (intervals.icu): `fatigue`, `muscle`, `stress`, `injury`

### 3. `generate.py` — Readiness-Karte im Dashboard

**Änderungen:**
- Wellness-Abruf um `fatigue`, `muscle`, `stress`, `injury` Felder erweitern
- `computeReadiness`-Logik analog zum MCP in Python nachbauen
- Template-Variablen erweitern: `score_obj`, `score_sub`, `subjektiv_bars`

### 4. `dashboard.template.html` — Readiness-Karte

**Änderungen:**
- Zwei Mini-Score-Boxen ("Körper" / "Gefühl") über den Komponenten-Bars
- Abschnitt "── Körper" mit bisherigen 4 Bars
- Abschnitt "── Gefühl" mit 4 neuen Bars (Ermüdung, Muskelkater, Stress, Verletzung)
- Verletzungs-Flag: wenn ≥ Niggle → farbige Hervorhebung

### 5. `.claude/skills/coach/SKILL.md`

**Änderungen (Schritt 0 / Readiness-Output):**
```
Readiness: 88/100 🟢
  Körper:  84 🟢  (HRV: +5.6 · Schlaf: Gut · TSB: +1 · Puls: -3.7)
  Gefühl:  94 🟢  (Ermüdung: Niedrig · Kater: Niedrig · Stress: Durchschn. · Verletzung: Keine)
```

- Verletzungs-Sonderregel in Muster-Logik eintragen: Niggle → Workout-Note, Schlecht/Verletzt → kein HIT

## API-Feldnamen (intervals.icu Wellness-Endpoint)

Zu verifizieren via Raw-API-Call vor Implementierung. Erwartete Feldnamen:

| intervals.icu Feld | Label im UI | Skala |
|---|---|---|
| `fatigue` | Ermüdung | 1–4, lower=better |
| `muscle` | Muskelkater | 1–4, lower=better |
| `stress` | Stress | 1–4, lower=better |
| `injury` | Verletzung | 1=Keine, 2=Niggle, 3=Schlecht, 4=Verletzt |
| `mood` | Stimmung | 1–4, lower=better |
| `motivation` | Motivation | 1–4, lower=better |

*Hinweis: `mood` und `motivation` sind in intervals.icu verfügbar, aber nicht im ersten Ausbau enthalten — können später ergänzt werden.*

## Beispiel: Heutige Werte (18. Mai 2026)

| Komponente | Wert | Punkte |
|---|---|---|
| HRV (+5.6ms) | leicht über Mittel | 33/40 |
| Schlaf (Gut, 2/4) | nach Fix | 19/25 |
| TSB (+1.0) | ausgeglichen | 17/20 |
| Ruhepuls (-3.7) | sehr gut | 15/15 |
| **Objektiv** | | **84/100** |
| Ermüdung (Niedrig) | 1/4 | 35/35 |
| Muskelkater (Niedrig) | 1/4 | 25/25 |
| Stress (Durchschn.) | 2/4 | 19/25 |
| Verletzung (Keine) | 1/4 | 15/15 |
| **Subjektiv** | | **94/100** |
| **Final** | 84×0.6 + 94×0.4 | **88/100 🟢** |

Vorher: 75/100 🟡 — obwohl Stefan sich gut fühlt.

## Nicht im Scope dieses Specs

- W' (W-prime) Tracking — separates Thema
- Monatsretro-Template — separates Thema
- Verletzungshistorie (`athlete/gesundheit.md`) — kann als kleines Add-on nach diesem Feature kommen
- Lauf-Workout-Bibliothek — separates Thema
