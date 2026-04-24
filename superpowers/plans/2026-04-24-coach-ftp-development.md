# Coach Skill FTP Development Extension – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend SKILL.md with structured FTP development logic: seasonal test windows, 3-week announcement, automated test week output, and Power-PR detection via MCP.

**Architecture:** Three markdown files get new content; SKILL.md gets three new sections inserted at precise anchor points. No code runs — the skill is read by Claude at runtime, so changes are pure Markdown/prose. Each task produces a self-contained commit.

**Tech Stack:** Markdown, `intervals.icu` MCP (`get_recent_activities`), existing SKILL.md instruction format.

---

## Context for agentic worker

This is a Markdown-based coaching system. All "code" is prose instructions that Claude reads at runtime via the `/coach` skill. The files live in:

- `/Users/stefan/Documents/Claude Code/Coaching/planung/langfristplan.md` — long-term plan (no expiry)
- `/Users/stefan/Documents/Claude Code/Coaching/athlete/fortschritt.md` — FTP history + progress log
- `/Users/stefan/Documents/Claude Code/Coaching/.claude/skills/coach/SKILL.md` — the coach skill (795 lines)

Key SKILL.md structure (anchors you'll use):

| Section | Starts at line | Anchor text |
|---|---|---|
| Schritt 0 – Metriken (Wochenplanung) | ~155 | `### Bei Wochenplanung` |
| Schritt 1 – Kontext laden | ~208 | `## Schritt 1: Kontext laden` |
| Schritt 2 – Modus erkennen | ~243 | `## Schritt 2: Modus erkennen` |
| Schritt 3 – FTP-Update | ~512 | `### FTP-Update` |
| Schritt 5 – Dateien aktualisieren | ~678 | `**Dateien aktualisieren:**` |

**"Testing" in this project** = read the file back, verify anchors are correct, verify no placeholder text, check no formatting breakage. There is no test suite.

---

## File Structure

| File | Change |
|---|---|
| `planung/langfristplan.md` | Add new section "FTP-Test-Fenster" with KW21 + KW39 |
| `athlete/fortschritt.md` | Add "Power-PR-Referenz" table; update "Nächster FTP-Test" |
| `.claude/skills/coach/SKILL.md` | (1) Add `get_recent_activities` to Schritt 0; (2) Add "Proaktive Checks" section after Schritt 1; (3) Add "FTP-Testwoche" to Schritt 3; (4) Add `fortschritt.md` PR-note to Schritt 5 |

---

## Task 1: Add FTP test windows to Langfristplan

**Files:**
- Modify: `planung/langfristplan.md`

- [ ] **Step 1: Verify current file state**

```bash
grep -n "FTP-Test\|Testfenster\|KW21\|KW39" /Users/stefan/Documents/Claude\ Code/Coaching/planung/langfristplan.md
```

Expected: No matches (section doesn't exist yet).

- [ ] **Step 2: Add new section before "Wann den Plan anpassen?"**

Insert the following before the line `## Wann den Plan anpassen?` in `planung/langfristplan.md`:

```markdown
## FTP-Test-Fenster (Saisonal)

Zwei formale Testfenster pro Saison. Kein Test außerhalb dieser Fenster ohne explizite Begründung.

| Testfenster | KW | Datum | Timing-Rationale |
|---|---|---|---|
| 🔬 Frühjahrstest 2026 | **KW21** | 18.–24. Mai 2026 | Nach HIT-Block KW18–20 (VO2max-Gains brauchen 2–4 Wo zum FTP-Transfer); vor Taper KW22–23 für RadRace |
| 🔬 Herbsttest 2026 | **KW39** | 21.–27. Sep 2026 | Nach Sommerpause + Herbstaufbau; Basis für Winterblock-Planung |

**Testprotokoll:** Sentiero 3+10min · outdoor · 4iiii Powermeter · FTP = 10min-Avg × 0,90

**Coach-Verhalten:**
- 3 Wochen vor Testfenster: automatischer Hinweis im nächsten `/coach`-Aufruf
- Stefan bestätigt oder verschiebt um 1 Woche
- Bei Bestätigung: Testwoche wird vollständig ausgeplant

**Verschiebungsregel:** Maximal 1 KW nach vorne oder hinten. Kein Test im Tapering (≤14 Tage vor Event).

---

```

- [ ] **Step 3: Verify insertion**

```bash
grep -n "FTP-Test-Fenster\|KW21\|KW39\|Herbsttest" /Users/stefan/Documents/Claude\ Code/Coaching/planung/langfristplan.md
```

Expected: Lines found, no duplicate section headers.

- [ ] **Step 4: Commit**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
git add planung/langfristplan.md
git commit -m "feat(langfristplan): FTP-Testfenster KW21 + KW39 eingetragen"
git pull --rebase && git push
```

---

## Task 2: Add Power-PR reference table to Fortschritt

**Files:**
- Modify: `athlete/fortschritt.md`

- [ ] **Step 1: Verify current file state**

```bash
grep -n "Power-PR\|5min\|10min\|20min\|Bestwert" /Users/stefan/Documents/Claude\ Code/Coaching/athlete/fortschritt.md
```

Expected: No matches for Power-PR section (doesn't exist yet).

- [ ] **Step 2: Update "Nächster FTP-Test" section**

Replace the existing `## Nächster FTP-Test` section (currently the last section in the file) with:

```markdown
## Nächster FTP-Test

**Testfenster:** KW21 (18.–24. Mai 2026)
**Methode:** 3+10min Protokoll, outdoor, 4iiii Referenz
**Danach:** Sentiero-Eingabe für aktualisiertes metabolisches Profil

---

## Power-PR-Referenz (5/10/20min)

*Referenzwerte für PR-Erkennung im Coach-Skill. Wird automatisch aktualisiert wenn ein neuer PR erkannt und bestätigt wird.*

| Dauer | Bestwert (W) | Datum | FTP-Proxy (×0,90) | Notiz |
|---|---|---|---|---|
| 5min | – | – | – | Noch nicht erfasst |
| 10min | 352W | 04.04.2026 | 317W | Feldtest KW14 (Coggan) |
| 20min | – | – | – | Noch nicht erfasst |

**Schwellenwert für Ankündigung:** >2% über Referenzwert → Coach meldet PR und fragt ob FTP angepasst werden soll.

**Update-Logik:**
- Bei "ja" (FTP übernehmen): Bestwert + FTP in `athlete/profil.md` aktualisiert
- Bei "nein": Bestwert wird trotzdem hier aktualisiert, FTP bleibt
- Bei "warten": Bestwert wird hier aktualisiert → kein erneuter Hinweis beim nächsten /coach
```

- [ ] **Step 3: Verify content**

```bash
grep -n "Power-PR\|Bestwert\|Schwellenwert\|10min.*352" /Users/stefan/Documents/Claude\ Code/Coaching/athlete/fortschritt.md
```

Expected: Lines found for all four patterns.

- [ ] **Step 4: Commit**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
git add athlete/fortschritt.md
git commit -m "feat(fortschritt): Power-PR-Referenztabelle 5/10/20min hinzugefügt"
git pull --rebase && git push
```

---

## Task 3: Add get_recent_activities to SKILL.md Schritt 0

**Files:**
- Modify: `.claude/skills/coach/SKILL.md`

The goal is to add a 4th MCP call in the "Bei Wochenplanung" block of Schritt 0, right after the existing 3 calls (`get_readiness_score`, `get_weekly_review`, `get_current_fitness`).

- [ ] **Step 1: Locate exact anchor**

```bash
grep -n "get_current_fitness\|Bei Ad-hoc-Anfragen" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Note the line number of `get_current_fitness` and the line after it (`**Bei Ad-hoc-Anfragen**`). The insertion goes between these two lines.

- [ ] **Step 2: Add get_recent_activities call**

After the line `3. \`get_current_fitness\` → CTL, ATL, TSB Verlauf (wenn mehr Kontext nötig)` and before `**Bei Ad-hoc-Anfragen**`, insert:

```markdown
4. `get_recent_activities(weeks: 4)` → Lade Aktivitäten der letzten 4 Wochen; extrahiere 5min/10min/20min Power-Bests (höchste Werte über alle Aktivitäten); vergleiche mit Referenzwerten in `athlete/fortschritt.md` (Abschnitt "Power-PR-Referenz") → PR-Flag setzen wenn >2% über Referenz

```

- [ ] **Step 3: Verify insertion**

```bash
grep -n "get_recent_activities\|Power-PR-Referenz" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Expected: One match for `get_recent_activities`, one for `Power-PR-Referenz`.

- [ ] **Step 4: Commit**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
git add .claude/skills/coach/SKILL.md
git commit -m "feat(skill): get_recent_activities für Power-PR-Erkennung in Schritt 0"
git pull --rebase && git push
```

---

## Task 4: Add "Proaktive Checks" section to SKILL.md

**Files:**
- Modify: `.claude/skills/coach/SKILL.md`

This adds a new section between Schritt 1 and Schritt 2. It covers:
- **Check A**: FTP-Test-Ankündigung (Komponente 2)
- **Check B**: Power-PR-Erkennung Output (Komponente 4)

- [ ] **Step 1: Locate insertion point**

```bash
grep -n "## Schritt 2: Modus erkennen" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Note the line number. The new section goes directly before `## Schritt 2`.

- [ ] **Step 2: Insert "Proaktive Checks" section**

Insert the following block directly before `## Schritt 2: Modus erkennen`:

```markdown
---

## Proaktive Checks (nur bei Wochenplanung, nach Schritt 1)

Diese Checks laufen nach dem Kontextladen. Sie erzeugen keinen eigenen Modus — ihre Ergebnisse werden als Zusatz-Abschnitt am Anfang von Schritt 4 (Output) ausgegeben, direkt nach 🎯 Standort.

### Check A: FTP-Test-Ankündigung

**Wann prüfen:** Bei jeder Wochenplanung.

**Logik:**
1. Lies aus `planung/langfristplan.md` → Abschnitt "FTP-Test-Fenster": extrahiere alle Testfenster-Daten
2. Für jedes Testfenster: berechne `tage_bis_test = testfenster_datum_donnerstag - heute`
3. Falls `14 < tage_bis_test ≤ 21` (= 3-Wochen-Fenster, aber nicht schon Testwoche):

**Output (in Schritt 4, nach 🎯 Standort):**

```
📊 FTP-Test in ~3 Wochen (KW21 · Do, 21. Mai)

Voraussetzungen für validen Test:
· ≥3 Tage ohne HIT/MIT in der Vorwoche
· kein Wettkampf-Stress, volle Erholung
· TSB am Testtag: Ziel > 0 (nicht zu frisch, nicht zu müde)

Soll ich die Testwoche (KW21) jetzt vorplanen?
→ [ja] → Testwoche wird vollständig ausgeplant
→ [verschieben auf KW22] → Reminder in 7 Tagen, Testfenster in langfristplan.md verschoben
```

**Bei "verschieben":**
- In `planung/langfristplan.md` das entsprechende Testfenster-Datum um +7 Tage verschieben
- Eintrag in `COACHING_AKTE.md`: `→ FTP-Test KW21 auf KW22 verschoben ([Datum heute])`

**Wenn kein Testfenster im 3-Wochen-Radius:** Check A überspringen, kein Output.

---

### Check B: Power-PR-Erkennung

**Wann prüfen:** Bei jeder Wochenplanung, wenn `get_recent_activities` in Schritt 0 Daten geliefert hat.

**Logik:**
1. Lade aktuelle Referenzwerte aus `athlete/fortschritt.md` → Abschnitt "Power-PR-Referenz"
2. Für jede Dauer (5min, 10min, 20min):
   - `pr_neu` = höchster Wert aus den letzten 4 Wochen (aus `get_recent_activities`)
   - `pr_ref` = gespeicherter Referenzwert in `fortschritt.md`
   - Falls `pr_ref == "–"` (noch nicht erfasst): `pr_neu` als ersten Wert eintragen, kein Hinweis ausgeben
   - Falls `pr_neu > pr_ref × 1.02` (>2% Steigerung): PR-Flag setzen

**Output bei PR-Flag (in Schritt 4, nach 🎯 Standort, nach Check A falls vorhanden):**

```
💪 Neuer [Xmin]-Power-PR erkannt: [pr_neu]W (vorher: [pr_ref]W, +[delta]%)
Das deutet auf eine FTP von ~[pr_neu × 0.90 gerundet auf 1W]W hin.
Aktuell gespeichert: [aktuelle FTP]W.

Soll ich die FTP auf [pr_neu × 0.90]W aktualisieren?
→ [ja] → FTP + Zonen werden aktualisiert (Ausgabe wie bei Post-Test)
→ [nein] → PR wird gespeichert, FTP bleibt
→ [warten] → PR wird gespeichert, kein erneuter Hinweis
```

Beispiel bei 10min-PR von 341W (vorher 333W):
```
💪 Neuer 10min-Power-PR erkannt: 341W (vorher: 333W, +2,4%)
Das deutet auf eine FTP von ~307W hin.
Aktuell gespeichert: 305W.

Soll ich die FTP auf 307W aktualisieren?
→ [ja] → FTP + Zonen werden aktualisiert
→ [nein] → PR wird gespeichert, FTP bleibt
→ [warten] → PR wird gespeichert, kein erneuter Hinweis
```

**Nach Stefan's Antwort:**

| Antwort | Aktion |
|---|---|
| ja | FTP auf `pr_neu × 0.90` setzen. Zonen neu berechnen. `athlete/profil.md` + `athlete/fortschritt.md` aktualisieren (PR-Wert + FTP). COACHING_AKTE-Eintrag. |
| nein | Nur PR-Wert in `athlete/fortschritt.md` aktualisieren. FTP unverändert. COACHING_AKTE-Eintrag: `→ [Xmin]-PR [W] erfasst, FTP-Update abgelehnt` |
| warten | Nur PR-Wert in `athlete/fortschritt.md` aktualisieren. FTP unverändert. Kein erneuter Hinweis beim nächsten /coach (Referenzwert ist jetzt auf pr_neu — nächster PR braucht wieder >2% darüber). |

**Wenn kein PR:** Check B erzeugt keinen Output.

---

```

- [ ] **Step 3: Verify insertion**

```bash
grep -n "Proaktive Checks\|Check A\|Check B\|FTP-Test-Ankündigung\|Power-PR-Erkennung" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Expected: All 5 patterns found. Run also:

```bash
grep -n "## Schritt 2: Modus erkennen" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Expected: Still present (insertion was before it, not replacing it).

- [ ] **Step 4: Commit**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
git add .claude/skills/coach/SKILL.md
git commit -m "feat(skill): Proaktive Checks – FTP-Test-Ankündigung + Power-PR-Erkennung"
git pull --rebase && git push
```

---

## Task 5: Add FTP test week structure to SKILL.md Schritt 3

**Files:**
- Modify: `.claude/skills/coach/SKILL.md`

Adds the test week planning output and post-test FTP recalculation to Schritt 3. This handles Komponente 3.

- [ ] **Step 1: Locate anchor**

```bash
grep -n "### FTP-Update" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Note the line number. The new "FTP-Testwoche" section goes directly before `### FTP-Update`.

- [ ] **Step 2: Insert FTP-Testwoche section**

Insert the following block directly before `### FTP-Update`:

```markdown
### FTP-Testwoche (wenn Stefan "ja" nach Ankündigung sagt)

**Wann ausführen:** Stefan hat auf die Check-A-Frage mit "ja" geantwortet. Erstelle vollständigen Wochenplan für die Testwoche.

**Testwoche-Struktur (Mini-Taper + Sentiero 3+10min):**

| Tag | Workout | TSS ca. | Notiz |
|---|---|---|---|
| Mo | Ruhetag | – | Mini-Taper |
| Di | LIT-1h30 locker | ~45 | Beine frisch halten, Z1–Z2, <229W |
| Mi | Aktivierung: 3×5min Z4 (308W) + LIT 30min | ~55 | Neuromuskuläre Aktivierung – kein Ausreißen |
| Do | **FTP-Test: Sentiero 3+10min** (outdoor, 4iiii) | ~80 | Protokoll unten |
| Fr | Ruhetag | – | Erholung |
| Sa | LIT-2h | ~55 | Recovery-Ride, Z1 |
| So | LIT-2h oder Ruhetag | ~55 | Laut Gefühl |

**Testprotokoll Sentiero 3+10min:**
1. Aufwärmen: 20min progressiv bis ~80% FTP
2. 3min All-Out (max. Leistung, nicht überpacen)
3. 5min aktive Erholung
4. 10min All-Out (gleichmäßiges Tempo, die letzten 2min etwas geben)
5. Abwärmen 10min
→ **FTP = 10min-Avg × 0,90**

**intervals.icu Workouts anlegen:**
- Di: `create_planned_workout` mit passendem LIT-Workout aus Bibliothek
- Mi: `create_planned_workout` Aktivierung (3×5min @ 308W, 5min Pause @ 168W, dann 30min LIT)
- Do: `create_planned_workout` als "Ride", Name "🔬 FTP-Test – Sentiero 3+10min", keine ERG-Workout-Steps (outdoor-Test)
- Sa/So: LIT aus Bibliothek

**Post-Test-Berechnung (wenn Stefan das Ergebnis mitteilt: "10min: XXW"):**

```
📊 FTP-Test Ergebnis

10min-Avg: [X]W → FTP = [X × 0.90 gerundet]W

Vergleich:
  Alt: [alter FTP]W ([alter W/kg] W/kg @ 88kg)
  Neu: [neuer FTP]W ([neuer W/kg] W/kg @ 88kg) → [+/- delta]%

Neue Zonen (Sentiero-Modell):
  Z0 Recovery: 0–[neuer FTP × 0.52]W
  Z1 Base:     [neuer FTP × 0.52]–[neuer FTP × 0.62]W
  Z2 FatMax:   [neuer FTP × 0.62]–[neuer FTP × 0.70]W
  Z3 Tempo:    [neuer FTP × 0.70]–[neuer FTP × 0.93]W
  Z4 FTP:      [neuer FTP × 0.93]–[neuer FTP × 1.03]W
  Z5 VO2max:   [neuer FTP × 1.03]–[neuer FTP × 1.38]W
  Z6 Anaerob:  [neuer FTP × 1.38]+W

Neue Workout-Zielwatts:
  LIT (55%):  [neuer FTP × 0.55]W
  SwSp (89%): [neuer FTP × 0.89]W
  KA (91%):   [neuer FTP × 0.91]W
  MIT (101%): [neuer FTP × 1.01]W

Übernehmen? [ja / nein]
```

**Zonenberechnung – exakte Schwellen (Sentiero-Modell):**
Z0: 0–52% · Z1: 52–62% · Z2: 62–70% · Z3: 70–93% · Z4: 93–103% · Z5: 103–138% · Z6: 138%+

Bei "ja":
1. `athlete/profil.md` aktualisieren: FTP, W/kg, alle Zonenwatts, alle Workout-Zielwatts
2. `athlete/fortschritt.md` aktualisieren: Neuer Eintrag in FTP-Verlauf-Tabelle + 10min-PR in Power-PR-Referenz
3. `COACHING_AKTE.md` Eintrag:
   ```
   ## [Datum] FTP-Test KW[N]
   10min: [X]W → FTP: [alt]W → [neu]W ([+/-%]) · Methode: Sentiero 3+10min outdoor
   ```
4. `CLAUDE.md` FTP-Zeile aktualisieren

---

```

- [ ] **Step 3: Verify insertion**

```bash
grep -n "FTP-Testwoche\|Sentiero 3+10min\|Post-Test-Berechnung\|Zonenberechnung.*exakte" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Expected: All 4 patterns found.

Also verify `### FTP-Update` is still present immediately after:

```bash
grep -n "### FTP-Update" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Expected: One match.

- [ ] **Step 4: Commit**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
git add .claude/skills/coach/SKILL.md
git commit -m "feat(skill): FTP-Testwoche-Struktur + Post-Test-Berechnung in Schritt 3"
git pull --rebase && git push
```

---

## Task 6: Update Schritt 5 file list for PR tracking

**Files:**
- Modify: `.claude/skills/coach/SKILL.md`

The file-update list in Schritt 5 mentions `athlete/fortschritt.md` only for FTP-Update. Now it must also be updated for Power-PR tracking. This is a one-line annotation change.

- [ ] **Step 1: Locate the exact line**

```bash
grep -n "fortschritt.md.*FTP-Update\|FTP-Update.*fortschritt" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Note the exact line. It currently reads approximately:
`5. **\`athlete/fortschritt.md\`** – nur bei FTP-Update oder neuem Körpergewicht`

- [ ] **Step 2: Update the annotation**

Replace the existing line with:

```markdown
5. **`athlete/fortschritt.md`** – bei FTP-Update, neuem Körpergewicht, oder Power-PR-Update (Bestwert aktualisieren, ggf. FTP)
```

- [ ] **Step 3: Verify**

```bash
grep -n "Power-PR-Update\|Bestwert aktualisieren" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Expected: One match.

- [ ] **Step 4: Final integration check**

Confirm all 4 new sections are present and in the correct order:

```bash
grep -n "get_recent_activities\|Proaktive Checks\|FTP-Testwoche\|Power-PR-Update" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Expected: 4 distinct matches. Verify line numbers are in ascending order (get_recent_activities < Proaktive Checks < FTP-Testwoche < Power-PR-Update).

- [ ] **Step 5: Commit**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
git add .claude/skills/coach/SKILL.md
git commit -m "feat(skill): fortschritt.md Power-PR-Update in Schritt-5-Dateiliste"
git pull --rebase && git push
```

---

## Self-review checklist

After all tasks complete, verify:

- [ ] `langfristplan.md` contains "FTP-Test-Fenster" section with KW21 (18.–24. Mai 2026) and KW39
- [ ] `fortschritt.md` contains "Power-PR-Referenz" table with 5/10/20min rows; 10min row pre-filled with 352W / 04.04.2026
- [ ] `SKILL.md` Schritt 0 has `get_recent_activities` as call #4 under Wochenplanung
- [ ] `SKILL.md` has "Proaktive Checks" section between Schritt 1 and Schritt 2
- [ ] `SKILL.md` Check A output uses KW21, Do 21. Mai as example (not a hardcoded wrong date)
- [ ] `SKILL.md` Check B output includes the ja/nein/warten decision table
- [ ] `SKILL.md` "FTP-Testwoche" is before `### FTP-Update`, not after
- [ ] Sentiero zone percentages in Post-Test match `athlete/profil.md` (Z0: 0–52%, Z1: 52–62%, Z2: 62–70%, Z3: 70–93%, Z4: 93–103%, Z5: 103–138%)
- [ ] No placeholder text ("TBD", "TODO", "fill in") anywhere in new content
- [ ] All 4 git commits pushed successfully
