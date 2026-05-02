# Coaching Science Extensions (W1 · W2 · W3) – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three knowledge blocks to `coaching_science.md` and update the `/coach` skill to reference them: CP/W' calculation from Sentiero data (W1), TT warm-up protocol (W2), and ACWR/Foster load management (W3).

**Architecture:** Pure content changes — `coaching_science.md` gets new/extended sections, `SKILL.md` gets updated section references and a CP/W' post-test calculation, `athlete/fortschritt.md` gets a new CP/W'-Verlauf section.

**Tech Stack:** Markdown editing only. No code changes. No tests needed (content, not logic).

---

### Task 1: W1 – CP/W' Abschnitt in coaching_science.md Sektion 12 erweitern

**Files:**
- Modify: `coaching_science.md` (Sektion 12 erweitern)

- [ ] **Schritt 1: Sektion 12 lesen**

  Öffne `coaching_science.md` und lies Sektion 12 komplett (ab Zeile `## 12. Critical Power / W'`).

- [ ] **Schritt 2: Neuen Unterabschnitt "CP/W' aus Sentiero berechnen" einfügen**

  Füge direkt nach dem Abschnitt "Einsatz im Training (Hybridansatz)" (vor dem `---`-Trenner) ein:

  ```markdown
  ### CP/W' aus Sentiero-Testergebnissen berechnen

  **Kein separater Testtermin nötig** – der Sentiero 3+10min-Test liefert zwei Datenpunkte auf der
  Power-Dauer-Kurve und ist ausreichend für eine valide CP/W'-Schätzung (±5% Fehler).

  **Formel (linearisiertes Moritani-Modell):**

  | Variable | Wert |
  |---|---|
  | P₁ | 3min-Durchschnittsleistung [W] |
  | t₁ | 180 s |
  | P₂ | 10min-Durchschnittsleistung [W] |
  | t₂ | 600 s |

  ```
  CP  = (P₂ × t₂ − P₁ × t₁) / (t₂ − t₁)    [W]
  W'  = (P₁ − P₂) × t₁ × t₂ / (t₂ − t₁)    [J] → in kJ: ÷ 1000
  ```

  **Beispiel Stefan (FTP 305W, Sentiero-Daten geschätzt):**
  - Annahme: 3min-Avg ≈ 380W, 10min-Avg ≈ 310W
  - CP = (310 × 600 − 380 × 180) / (600 − 180) = (186000 − 68400) / 420 ≈ **280W**
  - W' = (380 − 310) × 180 × 600 / 420 ≈ **18 000 J = 18 kJ**

  **Genauigkeit verbessern:** Ein optionaler 5min-Maximalversuch (separater Tag, frisch) als dritter
  Datenpunkt reduziert den Fehler auf ±2–3% (drei-Punkte-Kurvenanpassung).

  **Speicherung nach dem Test:** CP und W' in `athlete/fortschritt.md` → Abschnitt "CP/W'-Verlauf"
  eintragen. Der `/coach`-Skill erledigt das automatisch nach jedem FTP-Test.
  ```

- [ ] **Schritt 3: Überprüfen**

  Stell sicher dass der neue Abschnitt korrekt eingerückt ist und der `---`-Trenner nach Sektion 12 erhalten bleibt.

- [ ] **Schritt 4: Commit**

  ```bash
  git add coaching_science.md
  git commit -m "docs(science): W1 – CP/W' Berechnung aus Sentiero-Daten"
  ```

---

### Task 2: W2 – TT Warm-up Protokoll in Sektion 13 einfügen

**Files:**
- Modify: `coaching_science.md` (Sektion 13 erweitern)

- [ ] **Schritt 1: Sektion 13 lesen**

  Öffne `coaching_science.md` und lies Sektion 13 komplett (`## 13. Zeitfahren-Spezifik`).

- [ ] **Schritt 2: Neuen Unterabschnitt "TT Warm-up Protokoll" am Ende von Sektion 13 einfügen**

  Füge direkt vor dem `---`-Trenner nach Sektion 13 ein:

  ```markdown
  ### TT Warm-up Protokoll

  **Wissenschaft:** Golich & Andersen (2014, Int J Sports Physiol Perform): Strukturiertes 20–45min
  Warm-up mit kurzen VO₂max-Impulsen vor einem TT → +3–8% Leistung vs. kurzes oder kein Warm-up.
  Mechanismus: VO₂-Kinetik (slow component verkürzt), Muskeltemperatur ↑, neuromuskuläre Aktivierung.

  **Optimales Timing:** Letzter intensiver Block endet ≥12–15min vor dem Start (Laktatabbau, aber
  Primer-Effekt bleibt erhalten).

  **Protokoll für Stefan (RadRace TT ~10–12min):**

  | Phase | Dauer | Intensität | Ziel |
  |---|---|---|---|
  | Locker einfahren | 10 min | 55–65% FTP (168–198W) | Aufwärmen, Durchblutung |
  | Progressive Blöcke | 10 min | Stufenweise bis 85% FTP (~259W) | CV-Drift auslösen |
  | 3×1min VO₂max-Primer | 5 min | 110–120% FTP (336–366W), je 1min Pause | VO₂-Kinetik aktivieren |
  | Locker ausrollen | 5–7 min | 50–60% FTP (153–183W) | Laktat ≥12min vor Start senken |
  | **Gesamt** | **30–32 min** | | Letzter Block ≥12min vor Start |

  **Logistik:**
  - Rollentrainer mitbringen wenn Start am Veranstaltungsort — nicht auf der Zufahrtstraße warm fahren
    (Verkehr, unkontrollierbare Intensität)
  - Alternativ: Zufahrt als lockeres Einfahren nutzen, dann 3×1min-Primer am Startplatz
  - **Ernährung Warm-up-Ende:** 30–40g KH in letzten 15min vor Start (1 Gel)
  - **Koffein:** 3mg/kg ≈ 264mg, 45–60min vor Start (= vor dem Warm-up einnehmen)
  ```

- [ ] **Schritt 3: Überprüfen**

  Prüfe Markdown-Tabellen-Formatierung, kein `---`-Trenner verloren gegangen.

- [ ] **Schritt 4: Commit**

  ```bash
  git add coaching_science.md
  git commit -m "docs(science): W2 – TT Warm-up Protokoll (Golich 2014)"
  ```

---

### Task 3: W3 – Neue Sektion 19 (ACWR + Foster Load Management)

**Files:**
- Modify: `coaching_science.md` (neuen Abschnitt 19 am Ende anhängen)

- [ ] **Schritt 1: Ende von coaching_science.md prüfen**

  Lese die letzten 20 Zeilen von `coaching_science.md` um die aktuelle letzte Sektion und den Dateiabschluss zu sehen.

- [ ] **Schritt 2: Neue Sektion 19 anhängen**

  Füge am Ende der Datei (nach dem letzten `---`) ein:

  ```markdown
  ## 19. Load Management: ACWR + Foster Monotony/Strain

  *Referenz für Dashboard-Metriken M1 (Monotony/Strain) und M2 (ATL Ramprate)*

  ### Foster et al. (2001) – Monotony und Strain

  **Foster et al. (2001, J Strength Cond Res):** Session-RPE × Dauer [min] = Training Load (TL) pro
  Einheit. Aus den täglichen TL-Werten einer Woche lassen sich zwei Kennzahlen berechnen:

  ```
  Monotony = Wochenmittel TSS / Standardabweichung TSS
  Strain   = Wochen-TSS-Summe × Monotony
  ```

  **Interpretation:**

  | Monotony | Status | Bedeutung |
  |---|---|---|
  | < 1.5 | 🟢 Gut variiert | Gesundes Trainingsmuster |
  | 1.5 – 2.0 | 🟡 Erhöht | Zu gleichförmig, Risiko steigt |
  | > 2.0 | 🔴 Kritisch | Übertrainingsrisiko auch bei moderatem Volumen |

  | Strain | Bewertung |
  |---|---|
  | < 500 | Niedrig |
  | 500 – 800 | Moderat |
  | > 800 | Hoch |

  **Wichtige Erkenntnis:** Hohe Monotony bedeutet Übertrainingsrisiko *unabhängig vom absoluten
  Trainingsvolumen* — ein gleichförmiger Plan ohne Ruhetage ist riskanter als ein variierter Plan
  mit gleichem Gesamtvolumen. **Ruhetage senken Monotony mehr als gedacht** (0 TSS erhöht σ).

  ### ACWR – Acute:Chronic Workload Ratio

  **Gabbett (2016, Br J Sports Med):** Das Verhältnis von kurzfristiger zu langfristiger Trainingslast
  ist der stärkste Prädiktor für Verletzungsrisiko in Ausdauersport.

  ```
  ACWR = ATL / CTL
  ```

  **Zielzonen:**

  | ACWR | Zone | Konsequenz |
  |---|---|---|
  | < 0.8 | Unterlastet | Trainingsstimulus unzureichend |
  | 0.8 – 1.3 | Optimal | Weiter wie geplant |
  | 1.3 – 1.5 | Erhöhtes Risiko | Vorsicht, HRV täglich beobachten |
  | > 1.5 | Gefährlich | Verletzungsrisiko signifikant erhöht — Belastung reduzieren |

  ### Stefan-spezifische Richtwerte

  - **ACWR-Ziel im HIT-Aufbaublock (KW18–21):** 1.0–1.3 (kontrolliertes Wachstum)
  - **ACWR nach Krankheit oder Trainingspause:** Bewusst ≤ 1.1 halten bis CTL stabilisiert
  - **Regenerationswoche-ACWR:** ergibt typisch 0.6–0.8 → normal und gewünscht
  - **Monotony im HIT-Block:** Kann steigen durch ähnliche Intervall-Sessions → bewusst
    LIT-Tage variieren (Dauer, Kadenz, Gelände)

  ### Verbindung zu anderen Sektionen

  - **Sektion 9 (CTL/ATL/TSB):** ACWR nutzt dieselben Variablen, fügt aber die Ratio hinzu
  - **Sektion 15 (NFOR/Übertraining):** Monotony > 2.0 + hoher Strain sind Frühwarnindikatoren
  - **Dashboard M1/M2:** Monotony, Strain und ATL-Ramprate werden aus diesen Formeln berechnet
  ```

- [ ] **Schritt 3: Sektions-Referenz im Skill aktualisieren**

  In `SKILL.md`, Schritt 1 ("Kontext laden"), die Sektions-Referenz-Zeile am Ende des Abschnitts erweitern:

  Bestehend:
  ```
  1=Block-Periodisierung · 2=Polarized · 3=HRV · 4=VO2max · 5=KA/Low-Cadence · 6=Tapering · 7=Laktat-Clearance · 8=Ernährungsperiodisierung · 9=CTL/ATL/TSB · 10=Fueling (Stefan-spezifisch) · **11=Concurrent Training Laufen** · 12=Critical Power/W' · **13=TT Pacing Science** · 14=Sprint Training · **15=NFOR/Übertraining** · **16=Hitzeadaptation** · 17=Kadenz · 18=FTP Plateau
  ```

  Neu (anhängen):
  ```
  · **19=ACWR/Load Management**
  ```

- [ ] **Schritt 4: Ladematrix im Skill erweitern**

  In `SKILL.md`, Schritt 1 ("Phase × Modus Ladematrix"), zwei Zeilen ergänzen:

  | HIT-Aufbaublock KW18–21 | Wochenplanung | Bestehend: `1 · 2 · 3 · **4** · **7** · 9 · **10** · **11**` → Neu: `1 · 2 · 3 · **4** · **7** · 9 · **10** · **11** · **19**` |
  | Alle Phasen | Readiness Score < 40 / Krank-Risiko | Bestehend: `+ **15** (NFOR-Check)` → Neu: `+ **15** · **19**` |

- [ ] **Schritt 5: Commit**

  ```bash
  git add coaching_science.md .claude/skills/coach/SKILL.md
  git commit -m "docs(science): W3 – ACWR + Monotony/Strain (Sektion 19) + Skill-Ladematrix"
  ```

---

### Task 4: athlete/fortschritt.md – CP/W'-Verlauf Abschnitt

**Files:**
- Modify: `athlete/fortschritt.md`

- [ ] **Schritt 1: fortschritt.md lesen**

  Öffne `athlete/fortschritt.md` und lies die gesamte Datei um den richtigen Einfügepunkt zu finden (nach dem letzten bestehenden Abschnitt).

- [ ] **Schritt 2: Neuen Abschnitt "CP/W'-Verlauf" anhängen**

  Am Ende der Datei einfügen:

  ```markdown
  ## CP/W'-Verlauf

  *Wird automatisch nach jedem FTP-Test (Sentiero 3+10min) vom /coach-Skill aktualisiert.*
  *Berechnung: CP = (P₂×t₂ − P₁×t₁)/(t₂−t₁), W' = (P₁−P₂)×t₁×t₂/(t₂−t₁)*

  | Datum | CP [W] | W' [kJ] | 3min-Avg [W] | 10min-Avg [W] | FTP [W] |
  |---|---|---|---|---|---|
  | – | – | – | – | – | – |

  *Erster Eintrag nach nächstem FTP-Test in KW21.*
  ```

- [ ] **Schritt 3: Commit**

  ```bash
  git add athlete/fortschritt.md
  git commit -m "docs(athlete): CP/W'-Verlauf Abschnitt anlegen"
  ```

---

### Task 5: Abschluss und Push

- [ ] **Schritt 1: Alle Änderungen prüfen**

  ```bash
  git log --oneline -5
  ```

  Erwartete Commits (in dieser Reihenfolge):
  1. `docs(science): W1 – CP/W' Berechnung aus Sentiero-Daten`
  2. `docs(science): W2 – TT Warm-up Protokoll (Golich 2014)`
  3. `docs(science): W3 – ACWR + Monotony/Strain (Sektion 19) + Skill-Ladematrix`
  4. `docs(athlete): CP/W'-Verlauf Abschnitt anlegen`

- [ ] **Schritt 2: Push**

  ```bash
  git pull --rebase && git push
  ```

  Erwartete Ausgabe: `Branch 'main' set up to track remote branch 'main'` oder ähnlich ohne Fehler.
