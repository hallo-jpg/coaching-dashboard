# Skill-Intelligenz: Deload-Trigger + Concurrent-Check (S1 · S4)

**Datum:** 2026-05-02  
**Status:** Approved

## Problem

Der `/coach`-Skill reagiert heute nur auf explizite Anfragen. Zwei proaktive Checks fehlen:

1. **S1** – Kein automatischer Deload-Vorschlag wenn TSB/HRV Warnsignale senden; kein "optimale Testbedingungen"-Alert
2. **S4** – Concurrent-Training-Interferenz wird nicht geprüft; der Skill kann einen Plan ausgeben der Qualitätslauf und HIT-Rad konfliktbehaftet platziert — Stefan muss selbst aufpassen

## Ziel

Zwei neue proaktive Checks in `SKILL.md` hinzufügen: **Check D** (Deload-Trigger + FTP-Readiness) und **Check E** (Concurrent Training Scheduling-Check). Beide sind non-blocking — sie warnen und empfehlen, verbieten nicht.

---

## S1: Check D – Deload-Trigger + FTP-Test Readiness

### Einordnung

Neuer **Check D** in Schritt 0 (nach Check A, B, C). Wird nur bei **Wochenplanung** ausgeführt. Datenquellen: `get_current_fitness` (CTL, ATL, TSB, Verlauf), `get_readiness_score` (HRV, 30d-Baseline).

### Deload-Trigger

**Auslösebedingungen (erste zutreffende gewinnt):**

| Priorität | Bedingung | Schwere |
|---|---|---|
| 1 | TSB < −30 für ≥3 aufeinanderfolgende Tage | 🔴 Dringend |
| 2 | HRV >10% unter persönlicher 30d-Baseline für ≥5 aufeinanderfolgende Tage | 🟡 Erhöht |
| 3 | ACWR > 1.5 (ATL/CTL) | 🟡 Erhöht |
| 4 | TSB < −20 UND Monotony > 2.0 (falls M1 bereits implementiert) | 🟡 Erhöht |

**Datenbeschaffung:**
- TSB-Verlauf: aus `get_current_fitness` → `ctl`/`atl` Arrays → TSB = CTL − ATL pro Tag
- HRV-Baseline: aus `get_readiness_score` → `hrv_baseline_7` (oder 30d wenn verfügbar)
- ACWR: letzter ATL-Wert / letzter CTL-Wert

**Output (in Schritt 4, nach 🎯 Standort, vor allen anderen Checks):**

```
⚠️ Deload-Signal erkannt

[🔴/🟡] TSB seit [N] Tagen < [Wert] / HRV [X]% unter Baseline seit [N] Tagen / ACWR [X.X]

Empfehlung: Deload-Woche
→ TSS-Ziel um 40–50% reduzieren
→ Keine HIT-Einheiten
→ Alle Workouts LIT oder Ruhetag
→ Nächste volle Trainingswoche: KW[N+1]

Soll ich die aktuelle Woche als Deload planen?
→ [ja] → Wochenplan als Deload ausgeben
→ [nein] → Hinweis in COACHING_AKTE.md, normaler Plan
```

**Wenn kein Deload-Signal:** Check D (Deload) überspringen, weiter mit FTP-Readiness-Check.

### FTP-Test Readiness

**Auslösebedingungen (alle müssen gleichzeitig erfüllt sein):**
1. TSB zwischen +5 und +15
2. HRV ≥ Baseline (≥ 0% über 7d-Mittelwert) — erhöhtes HRV zeigt Erholung an
3. Letztes FTP-Testdatum ≥ 21 Tage zurück (aus `COACHING_AKTE.md` oder `athlete/fortschritt.md`)
4. Kein Event in den nächsten 10 Tagen (`tage_bis_event > 10`)
5. Kein Deload-Signal aktiv (Bedingung 1 nicht ausgelöst)

**Output (in Schritt 4, nach Deload-Abschnitt falls vorhanden):**

```
💡 Optimale Testbedingungen

TSB: +[X] | HRV: +[Y]% über Baseline | Letzter Test: vor [N] Tagen

Körper ist frisch und responsiv — die nächsten 3 Tage wären ideal für einen FTP-Test.

Soll ich den FTP-Test für [Wochentag] einplanen?
→ [ja] → Testwoche wird ausgeplant (wie Check A)
→ [nicht jetzt] → Kein erneuter Hinweis für 14 Tage
```

**Wenn keine Bedingungen erfüllt:** Kein Output, Check D vollständig überspringen.

### Persistenz "nicht jetzt"

Bei Antwort "nicht jetzt": Datum in `COACHING_AKTE.md` vermerken (`→ FTP-Readiness-Alert unterdrückt bis [Datum+14]`). Beim nächsten `/coach`: dieses Datum prüfen, Hinweis nicht erneut ausgeben wenn Datum noch nicht überschritten.

---

## S4: Check E – Concurrent Training Scheduling-Check

### Einordnung

Neuer **Check E** am Ende von **Schritt 3** (nach Workout-Auswahl und Wochenplan-Erstellung), **vor** dem Output (Schritt 4). Wird nur bei **Wochenplanung** ausgeführt. Prüft den soeben erstellten Wochenplan auf Interferenz-Verletzungen.

### Intensitäts-Klassifizierung

Für den Check gilt:

| Klasse | Rad-Einheiten | Lauf-Einheiten |
|---|---|---|
| **Hoch** | HIT (≥115% FTP), MIT (95–115% FTP), KA, FRT | Qualitätslauf (Z3 Schwelle, Z4 VO2max) |
| **Niedrig** | LIT, Easy Spin, Ruhetag | Easy Run (Z1) |

### Prüflogik

Der Check iteriert über alle Tagespaare und prüft:

**Level ❌ Konflikt (muss behoben werden):**
- Gleicher Kalendertag: Hoch-Rad + Hoch-Lauf

**Level ⚠️ Warnung (sollte behoben werden):**
- Aufeinanderfolgende Tage: Hoch-Rad am Tag X, Hoch-Lauf am Tag X+1 (oder umgekehrt) → <24h Abstand

**Level ℹ️ Hinweis (optional optimieren):**
- Gleicher Tag: Hoch-Rad + Niedrig-Lauf mit <6h Abstand (kein Zeitpunkt im Plan angegeben) → Reihenfolge empfehlen

**Kein Output wenn:** Kein Konflikt auf keinem Level.

### Output-Format

Der Check gibt einen **Optimizer-Block** aus der in Schritt 4 direkt **vor** dem Wochenplan erscheint:

```
🔄 Trainingsplanung optimiert

[❌ Konflikt] [Tag]: Hoch-Rad ([Name]) + Hoch-Lauf ([Name]) am selben Tag
→ Adaptationen beider Einheiten werden unterdrückt
→ Empfehlung: [Laufeinheit] verschieben auf [Tag Y] (dann 24h Abstand)
→ Plan angepasst: [kurze Beschreibung was geändert wird]

[⚠️ Warnung] [Tag X] + [Tag X+1]: [Rad] → [Lauf] = [~Xh] Abstand
→ VO2max-Effekt des Laufs reduziert (~30%)
→ Empfehlung: [Laufeinheit] auf [Tag Z] verschieben für maximalen Benefit
→ Plan angepasst: [Beschreibung]
```

**Der Skill passt den Plan automatisch an** wenn ein ❌ Konflikt vorliegt — kein extra Nachfragen. Bei ⚠️ Warnung: Empfehlung ausgeben + Plan anpassen. Bei ℹ️: nur Hinweis, Plan bleibt.

### Wichtige Prinzipien

- **Niemals eine Qualitätslauf-Einheit streichen** — immer einen anderen Tag suchen
- Wenn Umplanung nicht möglich (z.B. alle Tage voll): Hinweis ausgeben dass eine Einheit auf niedrigere Intensität wechseln sollte, aber Entscheidung bei Stefan lassen
- **Laufziele respektieren**: Der Check macht aus einem Qualitätslauf keinen Easy Run — er platziert ihn nur besser

---

## Technische Änderungen

### `SKILL.md`

1. **Check D** hinzufügen nach Check C (Lauf-Schwellenpace) in Schritt 0 — eigener `###`-Abschnitt mit vollständiger Logik
2. **Check E** hinzufügen als neuer `###`-Abschnitt am Ende von Schritt 3 (vor Output-Übergang)
3. **Ladematrix** in Schritt 1 ergänzen: Sektion 19 (`19=ACWR/Monotony`) bei HIT-Block und Krank-Risiko
4. **Sektions-Referenz** am Ende von Schritt 1 ergänzen: `19=ACWR/Load Management`
5. **Post-FTP-Test-Block** (Schritt 3): CP/W'-Berechnung aus 3min/10min-Avg hinzufügen + Speicherung in `athlete/fortschritt.md`

### `athlete/fortschritt.md`

Neuer Abschnitt `## CP/W'-Verlauf` hinzufügen:
```markdown
## CP/W'-Verlauf

| Datum | CP [W] | W' [kJ] | Basis (3min/10min Avg) | Methode |
|---|---|---|---|---|
| – | – | – | – | – |
```

---

## Nicht in Scope

- RPE-Logging (S2)
- Block-Abschluss-Retrospektive (S3)
- Illness-Recovery-Protokoll (S5 — Krank-Modus existiert bereits)
- Dashboard-Änderungen (gehört zu Sub-Projekt A)
- Änderungen an `coaching_science.md` (gehört zu Sub-Projekt B)
