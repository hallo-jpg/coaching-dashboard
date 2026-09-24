# Modul: Wochen-Retro & Monats-Retro

*Geladen aus `SKILL.md` – bei jeder Wochenplanung (Schritt R) und im Modus Monats-Review.*
*Stand: 24.9.2026 · Bewertungslogik mit Stefan abgestimmt: Kern-Einheiten statt TSS-Quote.*

---

## A. Wochen-Retro (bei jeder Wochenplanung, vor der neuen Woche)

### Pre-Check
- `planung/kw[N-1].md` liegt in `planung/` → Retro ausführen.
- Datei fehlt oder liegt schon in `planung/archiv/` → Retro überspringen.

### Daten abrufen
1. `get_recent_activities(days: 35)` → Aktivitäten der Vorwoche **und** der 4 Wochen davor
   (für die 30-Tage-Regel und den Wochenvergleich). Felder: `distanz_km`, `dauer_min`, `kadenz`
   (Lauf bereits in **spm**, nicht verdoppeln), `pace_min_km`, `intensity_if`, `rpe`, `avg_hf`, `tss`.
2. `get_weekly_review(week_start: Montag der Vorwoche)` → Zonenzeiten pro Tag, HRV-Verlauf.
3. `planung/kw[N-1].md` → welche Einheiten waren `🎯 Kern`, welche flexibel, wo stand Athletik.

Leere Aktivitäten (alle Felder `null`) sind Strava-Hüllen → nicht als fehlende Einheit werten, Stefan fragen.

### Die sechs Kennzahlen

| # | Kennzahl | Berechnung | ✅ | ⚠️ | ❌ |
|---|---|---|---|---|---|
| 1 | **Kern-Einheiten** | erfüllte `🎯 Kern`-Einheiten / geplante (verschoben & gefahren = erfüllt) | 3/3 | 2/3 | ≤1/3 |
| 2 | **Lauf-km** | Σ `distanz_km` der Woche vs. **Basis = höherer Wert aus Vorwoche und Ø der 4 Wochen davor** | ≤ +10% | +10–20% | > +20% |
| 3 | **Längster Lauf** | längster Einzellauf vs. längster Lauf der 30 Tage davor | ≤ +10% | +10–20% | > +20% |
| 4 | **Kadenz Easy** | Ø `kadenz` der Easy-Läufe (Pace langsamer als 6:50/km), nach Dauer gewichtet | ≥ Wochenziel aus dem Plan | bis 5 spm darunter | > 5 spm darunter |
| 5 | **Athletik** | im Plan abgehakte Athletik-Blöcke (Stefan meldet sie; ohne Meldung nachfragen) | 2/2 | 1/2 | 0/2 |
| 6 | **Wade / Nacken** | aus Stefans Meldungen und dem Plan (kein Wellness-Feld) | beschwerdefrei | Ziehen / Muskelkater | punktueller Schmerz → Abbruchregel |

Hinweise:
- **Lauf-km:** Basis < 15 km/Woche → +3 km absolut gelten als ✅ (sonst blockiert die Regel den Einstieg).
  Die Ø-4-Wochen-Basis verhindert, dass eine einzelne Ausfall- oder Entlastungswoche die Grenze auf null
  drückt. Identische Rechnung wie die Dashboard-Karte „Lauf-Aufbau" (`generate.py` → `_run_km_limit`).
- **Kadenz:** Das Wochenziel steht in der Workout-Spalte des Plans (z.B. „Kadenz-Fokus 165"). Qualitätsläufe
  und Rennen fließen nicht ein (dort ist die Kadenz ohnehin höher bzw. driftet).
- Fehlt eine Datengrundlage (kein Lauf in der Woche): Kennzahl `–`, zählt nicht in die Note.
- Pläne vor KW39 haben keine `🎯 Kern`-Markierungen → Kennzahl 1 = `–`, Note ohne Zeile 2.

### Rad-Block (kein Einfluss auf die Note, aber immer ausgeben)
- **Rad-Qualität:** gefahren ja/nein · Qualität per Tabelle unten.
- **LIT-Disziplin:** alle LIT-Fahrten mit IF ≥ 0,78 auflisten (Sweetspot-Drift).
- **Polarisation beide Sportarten:** Zeit in LIT / Grauzone / HIT aus `get_weekly_review`-Zonenzeiten.
  Rad über Power-Zonen (LIT = icu Z1–Z3, Grauzone = Z4, HIT = Z5–Z7), Lauf über HF-Zonen
  (LIT = icu Z1–Z2 ≤165, Grauzone = Z3 166–174, HIT = Z4+ ≥175). ⛔ Nie die vorberechneten
  `weekly_review.polarisation`-Buckets übernehmen (MCP wertet icu-Z3 als Moderate, Sentiero-Z3 ist LIT).
  Warnung wenn Grauzone > 15% oder LIT < 75%.

**Qualitätsbewertung je Einheit:**

| Typ | ✅ | ⚠️ | ❌ |
|---|---|---|---|
| Rad LIT | IF < 0,73, RPE ≤ 5 | IF 0,73–0,77 oder RPE 6 | IF ≥ 0,78 |
| Rad HIT / VO2max | IF ≥ 0,90, RPE ≥ 7 | IF 0,85–0,89 | IF < 0,85 |
| Rad Schwelle / SwSp / KA | IF 0,85–1,00, RPE 6–8 | ±0,05 daneben | deutlich daneben |
| Lauf Easy | 7:15–7:45/km, HF ≤ 165, Kadenz ≥ Ziel | eins davon knapp verfehlt | HF > 170 oder Pace < 6:50 |
| Lauf Qualität | Zielpace ±10 s/km, RPE 7–8 | ±10–20 s/km | deutlich verfehlt |

Kein IF (Lauf) → Pace/HF/Kadenz. Kein RPE → nur Messwerte.

### Gesamtnote (erste zutreffende Zeile gewinnt)

| # | Bedingung | Note |
|---|---|---|
| 1 | Kennzahl 6 ❌ **oder** Kennzahl 2 oder 3 ❌ | 🔴 Belastungssignal – Laufvolumen nächste Woche nicht steigern |
| 2 | Kern ❌ (≤1/3) | 🔴 Kern verfehlt – Grund klären (Zeit, Krankheit, Planung zu voll?) |
| 3 | Kern ✅ **und** keine ❌ **und** höchstens eine ⚠️ | 🟢 Gut |
| 4 | alle übrigen Fälle | 🟡 Mittel |

**TSS** erscheint nur als Info-Zeile (Ist / Plan) und fließt **nicht** in die Note. Ausnahme: Ist > 130% des
Plans → als eigener Hinweis „Mehrbelastung" in der Bewertung erwähnen (kein Notenabzug).

### Format – an `planung/kw[N-1].md` anhängen

```markdown
## Wochen-Retro

| Kennzahl | Wert | |
|---|---|---|
| 🎯 Kern-Einheiten | 3/3 | ✅ |
| Lauf-km | 18,4 km (Vorwoche 16,5 · +12%) | ⚠️ |
| Längster Lauf | 8,2 km (30 Tage davor: 7,5 · +9%) | ✅ |
| Kadenz Easy | Ø 163 spm (Ziel 165) | ⚠️ |
| Athletik | 2/2 | ✅ |
| Wade / Nacken | beschwerdefrei | ✅ |

**Rad:** Qualität ✅ (Di SwSp IF 0,88 · RPE 7) · LIT-Disziplin ✅ · Polarisation (Rad+Lauf): LIT 82% · Grauzone 11% · HIT 7%
**Info:** TSS 312 / Plan 300 · HRV → stabil (48 → 50)

### Einheiten
| Tag | Workout | TSS Ist | Qualität | Status | Notiz |
|---|---|---|---|---|---|
[Plantabelle mit Status ✅/❌/↪ verschoben, TSS Ist, Qualität]

### Bewertung
**Was lief gut:** [konkret aus den Daten]
**Was fehlte / warum:** [sachlich, kein Vorwurf]
**Lernpunkt für KW[N]:** [eine konkrete Handlungsempfehlung]

### Gesamtnote
[🟢/🟡/🔴] — [ein Satz Begründung]
```

Die Retro auch im Chat ausgeben (kompakt: Kennzahlen-Tabelle + Note + Lernpunkt).

### Archivieren & Akte
```bash
mkdir -p planung/archiv
git mv planung/kw[N-1].md planung/archiv/kw[N-1].md
```
In `COACHING_AKTE.md` einen Eintrag **oben** (neueste zuerst) ergänzen:
```markdown
## [Datum] – KW[N-1] Retro
[🟢/🟡/🔴] Kern [x]/3 · Lauf [km] km ([±%]) · Kadenz Easy [spm] · Athletik [x]/2 · [ein Satz Kernerkenntnis]
```

### Periodisierungsempfehlung (nur wenn eine Schwelle erreicht ist)
- zwei 🔴 in Folge (aktuelle + letzte archivierte Woche)
- Kern zwei Wochen in Folge ⚠️ oder ❌ → Wochenstruktur passt nicht zum Alltag
- Wade/Nacken ❌
- HRV 7d-Schnitt > 10% unter 30d-Basis über die ganze Woche

Dann konkret vorschlagen und auf Bestätigung warten (Periodisierung nur mit Stefans Zustimmung):
```
📋 Periodisierungsempfehlung: [konkrete Änderung]
Grund: [eine Zeile aus den Daten]
Bestätigen? (ja / nein / später)
```
Antwort in der Akte dokumentieren (`→ periodisierung.md angepasst: …` bzw. `→ Empfehlung abgelehnt: …`).

---

## B. Monats-Retro (Modus Monats-Review)

**Daten:** alle `planung/archiv/kw*.md` des Monats (Retro-Tabellen) · `get_recent_activities(days: 35)` ·
`get_wellness_range` für den Monat · Akte-Einträge des Monats.

```markdown
## 📊 Monats-Retrospektive [Monat YYYY]

### Zahlen
| KW | Kern | Lauf-km | Längster Lauf | Kadenz Easy | Athletik | Rad-h | Note |
|---|---|---|---|---|---|---|---|

**Monat:** Lauf [km] (Vormonat [km]) · Rad [h] · Kern [x]/[y] · Ø Kadenz Easy [spm]

### Fortschritt gegen die Saisonziele
| Ziel (periodisierung.md) | Start | jetzt | Tendenz |
|---|---|---|---|
| Laufvolumen 28–32 km/Woche | 6,5 | [Ø letzte 4 Wochen] | ↗/→/↘ |
| Kadenz 165–170 | 154 (Rennen) | [Ø Easy] | |
| Pace @ HF 160 | 7:30 | [aus HF-160-Check] | |
| FTP +8–12% | [Baseline KW40] | [letzter Test/Indikator] | |
| CTL 60–68 | 23 | [aktuell] | |

### Readiness-Verlauf
Tiefstwert [XX] ([Datum], [Kontext]) · Warnsignal aufgetreten: ja/nein

### Coach-Einschätzung
[2–4 Sätze, kein Beschönigen]

### Prio nächster Monat
[1 klarer Fokus]
```

**Speicherung:** in `COACHING_AKTE.md` unter `## Monats-Retrospektiven` (neueste zuerst).
