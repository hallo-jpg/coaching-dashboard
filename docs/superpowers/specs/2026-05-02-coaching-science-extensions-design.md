# coaching_science.md Erweiterungen (W1 · W2 · W3)

**Datum:** 2026-05-02  
**Status:** Approved

## Problem

Drei wissenschaftlich relevante Wissensblöcke fehlen in `coaching_science.md`, die der `/coach`-Skill regelmäßig braucht:
1. **W1** – CP/W' lässt sich aus dem bestehenden Sentiero-Test ableiten, aber die Formel und der Speicherort fehlen
2. **W2** – TT Warm-up Protokoll ist nicht dokumentiert; für RadRace TT am ersten Renntag kritisch
3. **W3** – ACWR und Foster Monotony/Strain fehlen komplett; sind Standard in Profi-Coaching

## Ziel

Drei neue Abschnitte in `coaching_science.md` hinzufügen. Kein Code, rein inhaltlich. Nach der Erweiterung muss der Skill diese Sektionen in seiner Ladematrix referenzieren.

---

## W1: CP/W' aus Sentiero-Daten ableiten

### Änderung

**Sektion 12** (`Critical Power / W'`) erhält einen neuen Unterabschnitt **"CP/W' aus Sentiero berechnen"**.

### Inhalt

- **Kein separater Testprotokoll nötig** – Sentiero 3+10min liefert zwei Datenpunkte auf der Power-Dauer-Kurve
- **Berechnungsformeln** (aus Moritani/Jones linearisierter CP-Gleichung):
  - `P₁` = 3min-Avg-Watt, `t₁` = 180s
  - `P₂` = 10min-Avg-Watt, `t₂` = 600s
  - `CP = (P₂ × t₂ − P₁ × t₁) / (t₂ − t₁)`
  - `W' = (P₁ − P₂) × t₁ × t₂ / (t₂ − t₁)` [Joule] → in kJ: ÷ 1000
- **Genauigkeit**: 2-Punkte-Schätzung hat ±5% Fehler; optionaler 5min-Maximalversuch (separater Tag) verbessert auf ±2–3%
- **Stefan-Beispiel** mit aktuellen Werten dokumentieren (für Anschaulichkeit)
- **Speicherort**: CP und W' nach jedem FTP-Test in `athlete/fortschritt.md` eintragen (neuer Abschnitt "CP/W'-Verlauf")

### Skill-Erweiterung

Nach FTP-Testauswertung (Schritt 3, FTP-Update): Wenn 3min- und 10min-Avg-Werte vorliegen, CP/W' berechnen und in `athlete/fortschritt.md` speichern. Ausgabe im Post-Test-Block ergänzen.

### Ladematrix-Eintrag

Sektion 12 wird bereits bei `TT-Spezifik KW22` und `Rennwoche-Modus` geladen (Referenz `· 12=Critical Power/W'` ist bereits im Skill vorhanden). Keine neue Zeile nötig – nur die Abschnittsnummer war bisher noch nicht explizit gelistet in `coaching_science.md` Sektion 8/Ernährung-Hinweis (irrelevant). Skill-Sektions-Referenz bereits korrekt.

---

## W2: TT Warm-up Protokoll

### Änderung

**Sektion 13** (`Zeitfahren-Spezifik: Pacing-Wissenschaft`) erhält einen neuen Unterabschnitt **"Warm-up Protokoll"** am Ende der Sektion.

### Inhalt

- **Wissenschaft**: Golich & Andersen (2014, Int J Sports Physiol Perform): 20–45min strukturiertes Warm-up mit kurzen VO2max-Intervallen vor TT → +3–8% Leistung vs. kurzes/kein Warm-up. Mechanismus: O₂-Aufnahme-Kinetik (VO₂ slow component verkürzt), Muskeltemperatur, neuromuskuläre Aktivierung
- **Optimales Timing**: letzter intensiver Block endet ≥12–15min vor Start (Laktat abbauen, aber Primer-Effekt erhalten)
- **Protokoll (Stefan, RadRace TT ~10–12min):**

| Phase | Dauer | Intensität | Ziel |
|---|---|---|---|
| Locker einfahren | 10min | 55–65% FTP | Aufwärmen, Muskeln |
| Progressive Blöcke | 10min | Stufenweise bis 85% FTP | CV-Drift auslösen |
| 3×1min VO2max-Primer | 3min | 110–120% FTP (338–366W), 1min Pause | VO₂-Kinetik aktivieren |
| Locker ausrollen | 5–7min | 50–60% FTP | Laktat ≥12min vor Start senken |
| **Gesamt** | **28–30min** | | Start: ≥12min nach letztem Block |

- **Material**: Rollentrainer mitbringen falls Start am Veranstaltungsort; Alternativ: Zufahrt zum Start als Warm-up nutzen
- **Ernährung Warm-up**: 30–40g KH in letzten 15min vor Start (Gel)

---

## W3: ACWR + Foster Load Management

### Änderung

**Neuer Abschnitt 19** am Ende von `coaching_science.md`.

### Inhalt

#### Wissenschaft

- **Foster et al. (2001)**: Session-RPE × Dauer [min] = Training Load (TL) pro Einheit; einfachste valide Methode für Trainingssteuerung ohne Powermeter
- **Monotony = µTSS / σTSS** (Wochenmittel ÷ Standardabweichung); Grenzwert <2.0 für Nachhaltigkeit
- **Strain = ΣTSS × Monotony**; hohe Monotonie bedeutet Übertrainingsrisiko auch bei moderatem Gesamtvolumen
- **ACWR (Acute:Chronic Workload Ratio)** = ATL / CTL; Bannen & Gabbett (2016), Meeuwisse et al.:

| ACWR | Status | Konsequenz |
|---|---|---|
| 0.8–1.3 | Optimal | Weiter wie geplant |
| <0.8 | Zu niedrig | Trainingsstimulus fehlt |
| 1.3–1.5 | Erhöhtes Risiko | Vorsicht, HRV beobachten |
| >1.5 | Gefährlich | Verletzungsrisiko signifikant erhöht |

#### Stefan-spezifische Richtwerte

- **Monotony-Alarm**: >1.5 → gelb; >2.0 → rot
- **Strain-Referenz**: <500 = geringes Risiko; >800 = hohes Risiko
- **ACWR-Ziel in Aufbauphase**: 1.0–1.3 (Wachstum ohne Überlastung)
- **ACWR nach Krankheit/Pause**: bewusst ≤1.1 halten bis CTL wieder stabil

#### Verbindung zum Dashboard

M1 (Monotony + Strain) und M2 (ATL Ramprate) im Dashboard basieren auf diesen Formeln — Sektion 19 ist die wissenschaftliche Referenz dafür.

#### Praktische Faustregeln

- **Gleiche TSS jeden Tag** ist schlechter als variable TSS, auch wenn die Woche gleich hart ist
- **Ruhetage senken Monotony** mehr als gedacht — 0 TSS an einem Tag erhöht σ drastisch
- **Laufeinheiten haben eigene TSS** (rTSS) → im Monotony-Check nicht mit Rad-TSS vermischen, separat bewerten

### Ladematrix-Eintrag

Neue Sektion 19 (`19=ACWR/Monotony`) wird zur Skill-Ladematrix hinzugefügt:
- `HIT-Aufbaublock KW18–21`: + 19
- `Alle Phasen | Readiness Score < 40 / Krank-Risiko`: + 19

---

## Nicht in Scope

- RPE-Logging-System (S2 — eigenes Projekt)
- CP/W'-Testprotokoll mit separaten 3 Testtagen (W1-Anpassung: Sentiero reicht)
- Änderungen an `generate.py` oder Dashboard (gehört zu Sub-Projekt A)
- Neue Felder in `athlete/fortschritt.md` anlegen (gehört zur Plan-Implementierung)
