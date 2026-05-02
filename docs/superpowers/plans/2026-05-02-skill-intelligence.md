# Skill-Intelligenz: Check D + Check E (S1 · S4) – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Two new proactive checks in `SKILL.md`: Check D (Deload-Trigger + FTP-Test Readiness) and Check E (Concurrent Training Scheduling Optimizer). Plus: CP/W' post-test calculation added to existing FTP-Update flow.

**Architecture:** Changes exclusively in `.claude/skills/coach/SKILL.md` and `athlete/fortschritt.md`. No code changes. Logic expressed in Markdown skill instructions.

**Tech Stack:** Markdown editing only. No tests (skill content). Manual verification by running `/coach` after changes.

---

### Task 1: Check D – Deload-Trigger in SKILL.md

**Files:**
- Modify: `.claude/skills/coach/SKILL.md`

- [ ] **Schritt 1: Position im Skill finden**

  Öffne `SKILL.md` und suche den Abschnitt `### Check C: Lauf-Schwellenpace-Erkennung`. Check D wird direkt **nach** Check C eingefügt (vor `## Schritt 2: Modus erkennen`).

- [ ] **Schritt 2: Check D einfügen**

  Füge nach dem `---` am Ende von Check C (und vor `## Schritt 2`) ein:

  ````markdown
  ---

  ### Check D: Deload-Trigger + FTP-Test Readiness

  **Wann prüfen:** Bei jeder Wochenplanung.

  **Datenbedarf:** `get_current_fitness` für CTL/ATL/TSB-Verlauf (letzten 7 Tage). `get_readiness_score` für HRV und 30d-Baseline (bereits in Schritt 0 geladen).

  #### Teil 1: Deload-Trigger

  **ACWR berechnen:** `ACWR = letzter ATL-Wert / letzter CTL-Wert` (aus `get_current_fitness`)

  **TSB-Verlauf prüfen:** Aus den letzten 7 Tagen CTL/ATL-Werte → TSB = CTL − ATL pro Tag. Zähle Tage mit TSB < −30.

  **HRV prüfen:** `hrv_abfall_pct = (hrv_baseline_30d − hrv_avg_7d) / hrv_baseline_30d × 100`

  **Auslösebedingungen (erste zutreffende gewinnt):**

  | Priorität | Bedingung | Schwere |
  |---|---|---|
  | 1 | TSB < −30 für ≥ 3 aufeinanderfolgende Tage | 🔴 Dringend |
  | 2 | HRV >10% unter 30d-Baseline für ≥ 5 Tage | 🟡 Erhöht |
  | 3 | ACWR > 1.5 | 🟡 Erhöht |

  **Output (in Schritt 4, direkt nach 🎯 Standort, vor allen anderen Checks):**

  ```
  ⚠️ Deload-Signal erkannt

  [🔴/🟡] [Begründung: z.B. "TSB seit 4 Tagen < −30" / "ACWR 1.62"]

  Empfehlung: Deload-Woche KW[N]
  → TSS-Ziel um 40–50% reduzieren (Soll: ~[X] → Deload: ~[X×0.5])
  → Keine HIT-Einheiten diese Woche
  → Alle Workouts: LIT oder Ruhetag

  Soll ich KW[N] als Deload planen?
  → [ja] → Wochenplan als Deload ausgeben (nur LIT, TSS-Cap)
  → [nein] → Hinweis in COACHING_AKTE.md, normaler Plan
  ```

  **Wenn kein Deload-Signal:** Kein Output für Teil 1. Direkt weiter mit Teil 2.

  #### Teil 2: FTP-Test Readiness

  **Nur prüfen wenn Teil 1 KEIN Signal ausgelöst hat.**

  **Letztes Testdatum bestimmen:** Aus `COACHING_AKTE.md` den letzten Eintrag mit `FTP-Test` suchen → Datum extrahieren. Falls kein Eintrag vorhanden: `tage_seit_test = 999` (immer prüfen).

  **Auslösebedingungen (alle müssen gleichzeitig erfüllt sein):**

  1. TSB zwischen +5 und +15
  2. HRV 7d-Mittelwert ≥ persönliche 30d-Baseline (= erholt)
  3. Tage seit letztem FTP-Test ≥ 21
  4. `tage_bis_event > 10` (kein Event in Kürze)

  **Output (in Schritt 4, nach Deload-Abschnitt falls vorhanden):**

  ```
  💡 Optimale Testbedingungen

  TSB: +[X] | HRV: +[Y]% über Baseline | Letzter Test: vor [N] Tagen

  Körper ist frisch und responsiv — die nächsten 3 Tage ideal für FTP-Test.

  Soll ich den Test für [nächster geeigneter Tag aus Wochenplan] einplanen?
  → [ja] → Testwoche wird ausgeplant (wie Check A)
  → [nicht jetzt] → Kein erneuter Hinweis für 14 Tage
  ```

  **Bei Antwort "nicht jetzt":** In `COACHING_AKTE.md` eintragen:
  ```
  → FTP-Readiness-Alert unterdrückt bis [heute + 14 Tage]
  ```
  Beim nächsten `/coach`: prüfe ob dieses Datum überschritten ist, bevor Check D/Teil 2 ausgelöst wird.

  **Wenn keine Bedingungen erfüllt:** Kein Output. Check D vollständig überspringen.
  ````

- [ ] **Schritt 3: Überprüfen**

  Lies den eingefügten Abschnitt und stelle sicher:
  - Check D steht zwischen Check C und `## Schritt 2`
  - Alle Markdown-Tabellen korrekt formatiert
  - Code-Blöcke vollständig geschlossen

- [ ] **Schritt 4: Commit**

  ```bash
  git add .claude/skills/coach/SKILL.md
  git commit -m "feat(skill): Check D – Deload-Trigger + FTP-Test Readiness"
  ```

---

### Task 2: Check E – Concurrent Training Scheduling-Check

**Files:**
- Modify: `.claude/skills/coach/SKILL.md`

- [ ] **Schritt 1: Position im Skill finden**

  Öffne `SKILL.md` und suche den Abschnitt `## Schritt 3: Entscheidungslogik`. Check E wird am **Ende von Schritt 3** eingefügt, direkt vor `## Schritt 4: Output`.

  Suche nach dem letzten `---` vor `## Schritt 4: Output`.

- [ ] **Schritt 2: Check E einfügen**

  Füge vor `## Schritt 4: Output` ein:

  ````markdown
  ---

  ### Check E: Concurrent Training Scheduling-Check

  **Wann ausführen:** Am Ende von Schritt 3, nach der Wochenplan-Erstellung, nur bei **Wochenplanung**.

  **Intensitäts-Klassifizierung für diesen Check:**

  | Klasse | Rad-Einheiten | Lauf-Einheiten |
  |---|---|---|
  | **Hoch** | HIT, MIT, KA, FRT (alle mit Intervallen/Schwellenarbeit) | Qualitätslauf (Schwelle Z3, VO2max Z4) |
  | **Niedrig** | LIT, Easy Spin, Ruhetag | Easy Run (Z1) |

  **Prüflogik:** Iteriere über alle Tagespaare im soeben erstellten Wochenplan.

  **❌ Konflikt (Plan anpassen — kein extra Nachfragen):**
  - Gleicher Tag: Hoch-Rad + Hoch-Lauf (egal in welcher Reihenfolge)
  - Lösung: Qualitätslauf auf nächsten freien Tag verschieben der ≥24h Abstand hat

  **⚠️ Warnung (Plan anpassen + erklären):**
  - Aufeinanderfolgende Tage: Hoch-Rad an Tag X + Hoch-Lauf an Tag X+1 (oder umgekehrt)
  - VO2max-Effekt des zweiten Quality-Workouts reduziert sich um ~30%
  - Lösung: sofern möglich, die Einheiten durch einen LIT- oder Ruhetag trennen

  **ℹ️ Hinweis (nur ausgeben, Plan nicht ändern):**
  - Gleicher Tag: Hoch-Rad + Niedrig-Lauf → Empfehlung Reihenfolge: Lauf AM, Rad PM (oder >6h Abstand)

  **Output-Block (erscheint in Schritt 4 direkt VOR dem Wochenplan, nur wenn mindestens ein Befund):**

  ```
  🔄 Trainingsplan optimiert

  [❌ Konflikt behoben] [Tag]: [Rad-Workout] + [Lauf-Workout] am selben Tag
  → Beide Adaptationen würden unterdrückt
  → [Lauf-Workout] verschoben auf [neuer Tag] (24h Abstand)

  [⚠️ Warnung behoben] [Tag X]→[Tag X+1]: [Rad] → [Lauf], ~[X]h Abstand
  → VO2max-Nutzen des Laufs reduziert um ~30%
  → Umgestellt: [Lauf] jetzt am [neuer Tag]

  [ℹ️ Tipp] [Tag]: [Rad] + [Easy Run] am selben Tag
  → Reihenfolge empfohlen: Lauf AM, Rad PM (oder >6h Abstand) für maximale Adaptation
  ```

  **Wichtige Regeln:**
  - Niemals eine Qualitätslauf-Einheit streichen — immer einen anderen Tag suchen
  - Laufziele respektieren: Aus einem Qualitätslauf wird kein Easy Run
  - Falls kein geeigneter Alternativtag existiert (alle Tage voll): Hinweis ausgeben und Entscheidung Stefan überlassen
  - Wenn kein Befund: Check E gibt keinen Output aus (kein "alles gut"-Satz)
  ````

- [ ] **Schritt 3: Überprüfen**

  Stelle sicher dass Check E zwischen dem Ende von Schritt 3 und `## Schritt 4: Output` steht.

- [ ] **Schritt 4: Commit**

  ```bash
  git add .claude/skills/coach/SKILL.md
  git commit -m "feat(skill): Check E – Concurrent Training Scheduling Optimizer"
  ```

---

### Task 3: CP/W' Post-Test-Berechnung in FTP-Update-Flow

**Files:**
- Modify: `.claude/skills/coach/SKILL.md`

- [ ] **Schritt 1: Post-Test-Block finden**

  Öffne `SKILL.md` und suche `### FTP-Testwoche` → dann den Block `**Post-Test-Berechnung (wenn Stefan das Ergebnis mitteilt: "10min: XXW")**`.

  Finde die Tabelle "Bei "ja":" die beschreibt was bei FTP-Update passiert.

- [ ] **Schritt 2: CP/W'-Berechnung in "Bei 'ja'" einfügen**

  In der "Bei 'ja':" Auflistung (die aktuell die Schritte 1–5 enthält), nach Schritt 2 (`athlete/fortschritt.md` aktualisieren) einen neuen Schritt einfügen:

  ```markdown
  2b. **CP/W' berechnen und speichern:** Falls 3min-Avg-Watt aus dem Test bekannt (Stefan hat mitgeteilt oder aus intervals.icu-Aktivität lesbar):
      - `CP = (P₂ × 600 − P₁ × 180) / 420` (P₁ = 3min-Avg, P₂ = 10min-Avg)
      - `W' = (P₁ − P₂) × 180 × 600 / 420 / 1000` [kJ]
      - In `athlete/fortschritt.md` → Abschnitt "CP/W'-Verlauf" neuen Eintrag hinzufügen
      - Im Post-Test-Output nach der Zonen-Tabelle ausgeben:
        ```
        CP (geschätzt): [CP]W | W' (geschätzt): [W']kJ
        → Basis für TT-Pacing Oberjochpass: kurze Steilsektionen mit W' einplanen
        ```
      Falls 3min-Avg nicht bekannt: CP/W'-Berechnung überspringen, nur FTP-Update durchführen.
  ```

- [ ] **Schritt 3: Überprüfen**

  Lies den gesamten Post-Test-Block und stelle sicher dass die Nummerierung (1, 2, 2b, 3, 4, 5) klar und konsistent ist.

- [ ] **Schritt 4: Commit**

  ```bash
  git add .claude/skills/coach/SKILL.md
  git commit -m "feat(skill): W1 – CP/W' Berechnung nach FTP-Test automatisch"
  ```

---

### Task 4: Abschluss und Push

- [ ] **Schritt 1: Alle Commits prüfen**

  ```bash
  git log --oneline -5
  ```

  Erwartete Commits:
  1. `feat(skill): Check D – Deload-Trigger + FTP-Test Readiness`
  2. `feat(skill): Check E – Concurrent Training Scheduling Optimizer`
  3. `feat(skill): W1 – CP/W' Berechnung nach FTP-Test automatisch`

- [ ] **Schritt 2: Push**

  ```bash
  git pull --rebase && git push
  ```

- [ ] **Schritt 3: Manuelle Verifikation**

  Öffne `SKILL.md` und prüfe:
  - Check D steht nach Check C, vor `## Schritt 2`
  - Check E steht am Ende von Schritt 3, vor `## Schritt 4`
  - CP/W'-Block steht im Post-Test-Abschnitt
  - Keine Markdown-Syntax-Fehler (unclosed code blocks, kaputte Tabellen)
