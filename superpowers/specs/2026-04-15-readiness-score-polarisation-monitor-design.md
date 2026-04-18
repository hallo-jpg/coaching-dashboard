# Design: Readiness Score & Polarisations-Monitor

*Datum: 2026-04-15 | Status: Implementiert*

---

## Kontext

Das Coaching-System für Stefan (RadRace 120, KW24/Juni 2026) nutzt intervals.icu als Datenquelle und einen Claude-basierten Coach-Skill. Bisher wurde die Trainingsbereitschaft manuell bewertet (HRV-Ampel im Briefing-Template). Die Polarisationsqualität war nicht sichtbar – es fehlte ein Check ob das Training wirklich polarisiert ist oder in Sweetspot-Drift läuft.

---

## Feature 1: HRV Readiness Score

### Problem
Stefan bewertet jeden Montag manuell (HRV ok? Schlaf gut? RPE?). Diese subjektive Bewertung ist inkonsistent und nutzt vorhandene Wellness-Daten aus intervals.icu nicht systematisch aus.

### Lösung
Neues MCP-Tool `get_readiness_score` – aggregiert 4 Komponenten zu einem Score 0–100:

| Komponente | Gewicht | Datenquelle | Logik |
|---|---|---|---|
| HRV-Trend | 40 Punkte | `wellness.hrv` (7 Tage) | Letzter Wert vs. Mittelwert ± Standardabweichung |
| Schlaf | 25 Punkte | `wellness.sleepQuality` (0–5) oder `sleepSecs` | Ø letzte 3 Nächte; Qualität bevorzugt, Dauer als Fallback |
| TSB | 20 Punkte | `wellness.ctl - atl` | >+10 frisch, -10 bis 0 neutral, <-20 stark ermüdet |
| Ruhepuls | 15 Punkte | `wellness.restingHR` (7 Tage) | Heute vs. 6-Tage-Ø; niedriger = besser |

**Score-Schwellen:**
- 🟢 80–100: Voll trainieren
- 🟡 60–79: Planmäßig, beobachten
- 🟡 40–59: Intensität −20%
- 🔴 <40: Nur LIT oder Ruhe

### Wissenschaftliche Basis
- Kiviniemi et al. 2007: HRV-guided daily training adjustments überlegen gegenüber festen Protokollen
- Plews et al. 2013: 7-Tage-rolling-Trend stabiler als Einzelwert (RMSSD-Methodik)
- Einzelner HRV-Tageswert ist anfällig für Messartefakte → SD-basierte Bewertung robuster

### Integration im Skill
- Schritt 0 ruft `get_readiness_score` als ersten API-Call auf (ersetzt `get_current_fitness` + `get_wellness_range` für Readiness-Bewertung)
- Score erscheint im Output unter **🎯 Standort**: `Readiness: XX/100 🟢 – Voll trainieren`
- Wenn Score < 60: explizit im Wochenplan berücksichtigen (Intensität drosseln)

---

## Feature 2: Polarisations-Monitor

### Problem
Stefan plant polarisiert (80% Z1-2, 20% Z4-7 nach Seiler-Modell), aber es gab keinen automatischen Check ob dies in der Realität so umgesetzt wird. Klassische Falle: LIT-Einheiten werden zu intensiv gefahren und landen in Z3 (Sweetspot) statt Z2.

### Lösung
Erweiterung von `get_weekly_review` – neue Sektion `polarisation` im Output:

**Berechnung:**
- Summiert `icu_zone_times` aller Rad-Aktivitäten der Woche (VirtualRide + Ride)
- Gruppiert: Low (Z1-Z2) / Moderate (Z3) / High (Z4-Z7)
- Berechnet Polarisations-Index: `Z1-2 / (Z1-2 + Z4-7) × 100`

**Warnungen:**
- Sweetspot-Drift: Z3 > 15% → `⚠️ Sweetspot-Drift: Z3 = X%`
- PI zu niedrig: PI < 80% → `⚠️ Polarisations-Index: X% (Ziel: ≥80%)`

**Ausgabe im Skill (Rückblick-Sektion):**
```
📊 Polarisation: Z1–2: 76% | Z3: 18% ⚠️ | Z4–7: 6%  →  PI: 93%
```

### Wissenschaftliche Basis
- Seiler & Kjerland 2006: Weltklasse-Ausdauersportler trainieren ~75-80% im Low-Bereich
- Stöggl & Sperlich 2014: Polarisiertes Training > Schwellentraining für CTL-Aufbau ohne Übertraining
- 15%-Schwelle für Z3 basiert auf Seiler-Modell; Z3 ist "no-mans-land" – zu intensiv für echte Erholung, zu wenig für HIT-Adaptation

### Einschränkung
Nur Rad-Aktivitäten werden gezählt – Läufe haben keine verlässlichen Power-Zonen via API, nur HR-Zonen mit anderen Schwellenwerten.

---

## Geänderte Dateien

| Datei | Änderung |
|---|---|
| `intervals-mcp/server.js` | Neues Tool `get_readiness_score` (Tool 9); `get_weekly_review` um `polarisation`-Sektion erweitert |
| `.claude/skills/coach/SKILL.md` | Schritt 0 umgeschrieben: `get_readiness_score` als Primär-Call; Review-Tabelle um Polarisations-Zeilen ergänzt; Rückblick-Sektion mit Polarisations-Ausgabeformat |
