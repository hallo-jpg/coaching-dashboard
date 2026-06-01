# Route Pacing System – Design Spec

**Datum:** 1. Juni 2026  
**Status:** Approved for implementation  
**Ziel:** Generisches Pacing-System für beliebige GPX-Routen — Zeitfahren, Rennen, Trainingsfahrten

---

## Zusammenfassung

Stefan hat wenig Pacing-Intuition und möchte vor einem Event (oder einer harten Trainingsfahrt) wissen: was kann ich realistisch leisten, wie verteile ich meine Kraft, wo sind die kritischen Stellen? Das System nimmt eine GPX-Datei, berechnet via Physikmodell segment-genaue Wattziele, visualisiert diese als interaktives Höhenprofil und gibt taktische Hinweise die das Gefühl dahinter erklären — nicht nur Zahlen.

---

## Architektur-Übersicht

```
athlete/routes/
  oberjochpass-tt.gpx        ← TT Zeitfahren
  radrace-120.gpx            ← Rennen Tag 2
  rosenheimer.gpx            ← Nebenevent (28.6.)
  archiv/                    ← Auf Stefans Wunsch archivierte Routen
    alte-strecke.gpx

generate_pacing.py           ← GPX-Parser + Physikmodell + Template-Renderer
pacing.template.html         ← Jinja2-Template (analog dashboard.template.html)
docs/pacing.html             ← Generierte Ausgabe (GitHub Actions, stündlich)
generate.py                  ← Kompakte Pacing-Karte für Dashboard (T-14 bis T-0)
.claude/skills/coach/SKILL.md ← Neuer Pacing-Block in Rennwoche-Modus
```

---

## 1. Routen-Verwaltung

**Speicherort:** `athlete/routes/*.gpx`

**Aktiv vs. Archiv:**
- Aktive Routen: alle `.gpx`-Dateien direkt in `athlete/routes/`
- Archivieren: Stefan sagt „archiviere Route X" → Datei wird nach `athlete/routes/archiv/` verschoben
- `generate_pacing.py` liest ausschließlich `athlete/routes/*.gpx` (nicht Unterordner)

**Route-Metadaten** (optional, `athlete/routes/<name>.json`):
```json
{
  "name": "Oberjochpass TT",
  "type": "tt",
  "event_date": "2026-06-13",
  "target_if": 1.00,
  "notes": "Zeitfahren RadRace · negativer Split"
}
```
Fehlt die JSON-Datei, werden Defaults verwendet (`type: "climb"`, `target_if: 0.95`).

---

## 2. Pacing-Engine (`generate_pacing.py`)

### 2a. GPX-Parser

Eingabe: `.gpx`-Datei  
Ausgabe: Liste von Segmenten mit je 50m Auflösung:
```python
[{"dist_m": 50, "elev_start": 845, "elev_end": 847, "gradient_pct": 4.0}, ...]
```

Segmente werden zu sinnvollen Blöcken gruppiert (Gradient-Änderung >1% über min. 200m → neues Segment). Typisch 4–8 Segmente pro Route.

### 2b. Physikmodell

Gegebene Zielleistung P → Geschwindigkeit v (numerisch gelöst):

```
P = m·g·v·sin(arctan(gradient/100)) + m·g·v·Cr + 0.5·ρ·Cd·A·v³
```

**Parameter (Stefan):**
| Variable | Wert | Quelle |
|---|---|---|
| m | 96 kg | 88kg Fahrer + 8kg Rad |
| g | 9.81 m/s² | Konstante |
| Cr | 0.004 | Standard Asphalt |
| ρ | 1.20 kg/m³ | Meereshöhe; bei >1000m: 1.11 |
| Cd·A | 0.32 m² | Rennrad Aufsitzposition |
| Cd·A (TT) | 0.26 m² | TT-Position (wenn `type: "tt"`) |

Masse, Cr, Cd·A sind in `generate_pacing.py` als Konstanten definiert — bei Gewichtsänderung einmalig anpassen.

### 2c. Segment-Leistungszuweisung

Strategie basierend auf Gradient und Streckentyp:

| Gradient | Ziel-Watt (relativ zu CP) | Zone |
|---|---|---|
| < 2% | 92% CP | Aerob |
| 2–4% | 97% CP | Aerob+ |
| 4–6% | 100% CP | MIT |
| 6–8% | 105% CP | MIT+ (W' Einsatz) |
| > 8% | 108% CP | HIT kurz (W' Budget prüfen) |
| Abfahrt | 60% CP | Erholung / W' Rekonstituierung |

**Korrekturfaktoren:**
- Streckentyp `tt`: +3% (Einzelstart, maximale Intensität)
- Streckentyp `gran_fondo` (>100km): −5% (Ausdauer über 4–6h)
- Streckentyp `climb` (isolierter Anstieg): Basistabelle

**Negativ-Split-Logik (nur `type: "tt"`):** Erste 20% der Streckendistanz: −3% vom Segment-Zielwatt. Letzte 20%: +2%.

### 2d. W'-Balance-Tracking

```
W'_balance = W'_total              # Start: 28.1 kJ (aus fortschritt.md)
für jedes Segment:
  wenn P > CP:
    W'_balance -= (P - CP) × t    # Verbrauch
  sonst:
    W'_balance += k × (CP - P) × t  # Rekonstituierung, k=0.35 (empirisch)
```

**Warnung:** Wenn `W'_balance < 5 kJ` vor dem letzten Streckendrittel → Pacing zu aggressiv, Zielwatt um 5% reduzieren und neu berechnen.

### 2e. Zeitprognose

```
segment_time = segment_dist / v
total_time = Σ segment_times
range_low = total_time × 0.97   # guter Tag (+TSB, Windschatten)
range_high = total_time × 1.05  # schwerer Tag (Gegenwind, Ermüdung)
```

---

## 3. Ausgabe 1: `docs/pacing.html`

### Struktur

Standalone HTML-Datei, generiert von `generate_pacing.py` via `pacing.template.html`. Selbe Design-Sprache wie `dashboard.html`. Automatisch neu gebaut via GitHub Actions bei jedem Push (oder stündlich).

**Tab-Navigation** oben: ein Tab pro aktiver Route in `athlete/routes/`.  
Tab-Reihenfolge: nach `event_date` aufsteigend (nächstes Event zuerst).

### Inhalt pro Route-Tab

**Header-Zeile:** Route-Name · Event-Datum · Streckentyp · Distanz · Höhenmeter

**KPI-Karte (4 Felder):**
- Zielzeit (mit Range)
- Ø Zielwatt + IF
- W' verbraucht (von total)
- W' Reserve

**Höhenprofil (SVG, volle Breite):**
- Farbige Segmentflächen (grün/gelb/orange = Intensität)
- Höhenlinie als Polyline
- Gradient-Label + Watt-Ziel pro Segment über der Kurve
- Distanzmarker an der X-Achse, Höhenmarker rechts
- Text außerhalb des skalierten SVG-Bereichs (kein `preserveAspectRatio="none"`)

**W'-Balance-Balken:** Fortschrittsbalken von voll (grün) bis leer (rot), Zahl rechts.

**Segmenttabelle:**
| Segment | Gradient | Zone | Zielwatt | Ø km/h | Split |
|---|---|---|---|---|---|

**Intuitions-Abschnitt** (das Alleinstellungsmerkmal):  
Erklärt was die Zahlen im Körper bedeuten. Pro Route 3–4 Sätze, generiert aus den Segment-Daten:

> *„Das Steilstück km 3,5–5,0 (7,1%) entspricht von der Intensität deiner 4×4min VO2max-Einheit — das Gefühl in den Beinen kennst du. Du planst 322W für ~8 Minuten. Dein W' schrumpft hier um ~9 kJ — das ist die Hälfte deines Puffers."*

> *„Start (km 0–1,5): 295W fühlen sich zu leicht an. Das ist korrekt. Nach 5 Minuten bei richtigem Pacing setzt das 'es wird ernst'-Gefühl ein. Wenn es sich schon am Start schwer anfühlt, bist du zu schnell."*

**Taktik-Hinweise** (3–5 kompakte Bullets):
- ⚠️ Segment-spezifische Warnungen (steilste Stelle, W'-kritische Zone)
- ✅ Wo du Tempo rausnehmen kannst (Abfahrten, flache Pasagen)
- 🔋 W'-Budget Zusammenfassung

---

## 4. Ausgabe 2: Coach-Skill-Block (Rennwoche-Modus)

**Trigger:** Automatisch wenn `tage_bis_event ≤ 7` und eine Route mit passendem `event_date` in `athlete/routes/` existiert.

**Manuell:** Wenn Stefan schreibt „gib mir Pacing für [Route]" oder „ich will morgen X richtig fahren".

**Format im Coach-Output** (nach 🎯 Standort, vor Wochenplan):

```
🏁 Pacing · Oberjochpass TT · Sa 13.6.

Zielzeit: 23:20 (Range 22:30–24:10) · Ø 305W · IF 1.00
W' Budget: 19,7 von 28,1 kJ verplant · 8,4 kJ Reserve ✅

Anker-Watt:
  km 0–1,5  (3,8%) → 295W  — locker beginnen, nicht mitreißen lassen
  km 1,5–3,5 (5,2%) → 308W  — Hauptanstieg, Rhythmus halten
  km 3,5–5,0 (7,1%) → 322W  ⚠ Steilstück, max. W'-Einsatz
  km 5,0–6,8 (4,4%) → 302W  — Finale, Restenergie leeren

→ Vollanalyse: https://hallo-jpg.github.io/coaching-dashboard/pacing.html
```

**Für Rennen (Gran-Fondo-Typ):**
```
🏁 Pacing · RadRace 120 · So 14.6.

Energie-Budget: ~3.500 kJ aerob (5h bei Ø 194W) · W' 28,1 kJ
Ziel-Ø: 195W (IF 0.64) — konservativ, Gruppe nutzen

Schlüssel-Anstiege:
  [Anstieg A]  (5,8%) → 280W  — nicht attackieren, Gruppe lassen
  [Anstieg B]  (7,4%) → 295W  ⚠ kritisch, W' schonen
  [Finale]     (3,1%) → 310W  — hier alles geben

Intuition: "Tag 2 nach TT — erste 2h unter 185W fahren, auch wenn es langweilig ist."
```

---

## 5. Ausgabe 3: Dashboard-Karte (optional, T-14 bis T-0)

Kompakte Karte im bestehenden Dashboard. Nur sichtbar wenn `tage_bis_event ≤ 14`.

**Inhalt:**
- Event-Name + Datum
- Zielzeit + Ø Watt
- 2 Anker-Wattwerte (erster Anstieg + steilstes Segment)
- Deep-Link zu `pacing.html`

Implementierung: neue Kontextvariable `pacing_card` in `build_context()`, Template-Block in `dashboard.template.html`.

---

## 6. Datei-Änderungen

| Datei | Änderung |
|---|---|
| `athlete/routes/` | Neuer Ordner (+ `archiv/` Unterordner) |
| `generate_pacing.py` | Neue Datei: GPX-Parser + Physikmodell + HTML-Renderer |
| `pacing.template.html` | Neues Jinja2-Template |
| `docs/pacing.html` | Generierte Ausgabe (nicht manuell anfassen) |
| `generate.py` | `build_pacing_card()` Funktion + `pacing_card` Kontext |
| `dashboard.template.html` | Neuer Template-Block für Pacing-Karte |
| `.claude/skills/coach/SKILL.md` | Pacing-Block in Rennwoche-Modus + manueller Trigger |
| `.github/workflows/build.yml` | `generate_pacing.py` in Build-Pipeline einbinden |

---

## 7. Nicht im Scope

- Upload-Interface für GPX im Browser (GPX wird manuell in `athlete/routes/` abgelegt)
- Live-Segment-Auswahl (Klick auf Profil zeigt Detail) — zu komplex für Phase 1
- Wind-Korrektur (Windgeschwindigkeit unbekannt, ±5% ist im Range abgebildet)
- Herzraten-basiertes Pacing (Watt ist der Anker, HR sekundär)

---

## 8. Offene Abhängigkeiten

- GPX-Dateien müssen von Stefan besorgt und in `athlete/routes/` abgelegt werden bevor der Build sinnvoll ist
- Oberjochpass GPX: Komoot/Strava (öffentlich verfügbar)
- RadRace 120 GPX: Veranstalter-Website oder Vorjahres-Strava-Aufzeichnung
- `gpxpy`-Library muss zu Python-Dependencies hinzugefügt werden (`pip install gpxpy`)
