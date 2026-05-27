# Taper-Protokoll Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the `/coach` skill from hardcoded KW23/24/25/26 taper logic to a dynamic, event-driven tapering system that works for any future race — including a TSB-Prognose, Taper-Checkliste, Taper-Anxiety-Handling, and enriched carb-loading science.

**Architecture:** Two files change: `.claude/skills/coach/SKILL.md` gets dynamic event detection and enriched taper output formats; `coaching_science.md` Section 6 gets a carb-loading countdown and TT warm-up protocol. No code, no database — all changes are markdown content edits. The skill reads events from `athlete/profil.md` (Saisonziele section) at runtime and computes weeks-to-race dynamically.

**Tech Stack:** Markdown, Jinja2-free (skill files are read verbatim by Claude at invocation)

---

## File Map

| File | Change |
|---|---|
| `.claude/skills/coach/SKILL.md` | 5 targeted edits — see Tasks 1–5 |
| `coaching_science.md` | 2 additions to Section 6 — see Task 6 |

---

### Task 1: Dynamic event detection — replace hardcoded KW references in Modus-Erkennung

**Files:**
- Modify: `.claude/skills/coach/SKILL.md` (lines 117–129, Schritt 2 Modus-Erkennung table)

Context: Currently the table has literal "KW23 / KW25" and "KW24 / KW26" rows. These break the moment a new season starts. Replace with weeks-to-race logic.

- [ ] **Step 1: Open SKILL.md and locate the Modus-Erkennung table**

The table starts at `| Signal | Modus |` and contains these two rows to replace:
```
| KW23 / KW25 (Tapering oder Recovery nach Rennen) | **Tapering / Recovery-Modus** |
| KW24 (RadRace-Woche) / KW26 (Rosenheimer-Woche) | **Rennwoche-Modus** |
```

- [ ] **Step 2: Replace those two rows with dynamic event-relative logic**

Replace with:
```markdown
| ≤14 Tage bis nächstem Event (aus `athlete/profil.md` Saisonziele) | **Tapering-Modus** |
| 0–6 Tage bis Event (Rennwoche) | **Rennwoche-Modus** |
| 1–14 Tage nach Event, nächstes Event >21 Tage weg | **Recovery-Modus** |
| "schlapp", "faul", "sollte ich mehr trainieren", "reicht das" während Tapering | **Taper-Anxiety** → in Tapering-Modus behandeln, kein Extra-Training |
```

- [ ] **Step 3: Add event-detection instruction before the table**

Directly before the `| Signal | Modus |` table, add:

```markdown
**Event-Erkennung (immer zuerst):**
Lies `athlete/profil.md` → Abschnitt "Saisonziele". Identifiziere das nächste bevorstehende Event mit Datum. Berechne `tage_bis_event = event_datum - heute`. Alle Modus-Entscheidungen basieren auf diesem Wert — nie auf fixen KW-Nummern. Bei mehreren Events: immer das nächste verwenden.
```

- [ ] **Step 4: Commit**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
git add .claude/skills/coach/SKILL.md
git commit -m "feat(coach): event-getriebene Taper-Erkennung statt hardcoded KW23/24"
```

---

### Task 2: Rewrite Tapering-Modus and Recovery-Modus sections to be event-agnostic

**Files:**
- Modify: `.claude/skills/coach/SKILL.md` (section `### Tapering-Modus (KW23 + KW25)` and `### Rennwoche-Modus (KW24 + KW26)`)

Context: These sections use fixed week numbers. Replace with T-minus language and add TSB-Prognose. The current Tapering-Modus text is at lines 214–232.

- [ ] **Step 1: Replace the Tapering-Modus section header and content**

Find:
```markdown
### Tapering-Modus (KW23 + KW25)
- **KW23** (vor RadRace): TSS auf ~50% der Vorwoche, 1× kurze HIT-Aktivierung, kein neues Reiz-Setzen, Schlaf + Ernährung priorisieren
- **KW25** (Recovery nach RadRace, vor Rosenheimer): lockere Erholung Mi–Fr, leichtes Aufbauen Sa/So; kein Kraft, kein HIT – nur LIT + optional kurze SwSp am So wenn Erholung gut
```

Replace with:
```markdown
### Tapering-Modus (≤14 Tage vor Event)

**Grundregel:** Volumen runter, Intensität halten. Kein neues Reiz-Setzen ab T-10.

| Zeitraum | Volumen | Training |
|---|---|---|
| T-14 bis T-9 (Woche 2 vor Rennen) | −40% ggü. Vorwoche | 1× kurze HIT-Aktivierung (3×4min @ ~355W), Rest LIT |
| T-8 bis T-2 (Rennwoche Anfang) | −55% | 1× kurze Aktivierung (20×30s @ 400W oder 3×5min @ 295W), Rest LIT |
| T-1 (Vortag) | minimal | Aktivierun.zwo: 20–30min + kurze Intensität |

**TSB-Ziel am Renntag:** +10 bis +20
**TSB-Prognose berechnen** (immer im Tapering-Output ausgeben):
- CTL decays: × 0.965 pro Tag (42-Tage-Zeitkonstante)
- ATL decays: × 0.916 pro Tag (7-Tage-Zeitkonstante)
- Nimm aktuellen CTL und ATL aus `get_current_fitness`, reduziere ATL mit reduzierten TSS-Werten, projiziere T Tage voraus
- Ausgabe: `Prognose TSB Renntag: +XX (Ziel: +10 bis +20) → [auf Kurs / zu niedrig / zu hoch]`

**Recovery-Modus (1–14 Tage nach Event, nächstes Event >21 Tage):**
- Tage 1–4: Nur Easy LIT oder Pause, kein Kraft, kein HIT
- Tage 5–10: Leicht aufbauen, LIT + optional kurze SwSp ab Tag 7 wenn HRV normal
- Danach: Readiness-Score entscheidet über Rückkehr zu normalem Training
```

- [ ] **Step 2: Replace the Rennwoche-Modus section header**

Find:
```markdown
### Rennwoche-Modus (KW24 + KW26)
**KW24 – RadRace:**
```

Replace the header with:
```markdown
### Rennwoche-Modus (0–6 Tage bis Event)

**Allgemeines Rennwoche-Schema (T-6 bis T-0):**
- T-6 bis T-4: LIT oder Pause, viel Schlaf, Carb-Loading starten (siehe coaching_science.md Abschnitt 6 → Carb-Loading-Protokoll)
- T-3: LIT-1h locker
- T-2: Aktivierun.zwo (Aktivierung)
- T-1: Pause oder 20min Easy Spin
- T-0: Renntag — Warm-up-Protokoll (siehe coaching_science.md Abschnitt 6 → Renntag Warm-up)

**RadRace spezifisch (Zeitfahren T-1, Rennen T-0):**
```

Leave the specific RadRace and Rosenheimer content as-is below this new header.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/coach/SKILL.md
git commit -m "feat(coach): Tapering/Recovery-Modus event-agnostisch + TSB-Prognose-Formel"
```

---

### Task 3: Update Phase × Modus Ladematrix to remove hardcoded KW numbers

**Files:**
- Modify: `.claude/skills/coach/SKILL.md` (Phase × Modus Ladematrix table, lines ~94–106)

Context: The matrix has `Tapering KW23/KW25` and `Rennwoche KW24/KW26`. Replace with relative references.

- [ ] **Step 1: Find and update the two tapering/race rows in the matrix table**

Find:
```markdown
| Tapering KW23/KW25 | Tapering-Modus | **6** · 9 · **10** · **11** |
| Rennwoche KW24/KW26 | Rennwoche-Modus | **6** · **8** · **10** · **11** · **13** · **16** |
```

Replace with:
```markdown
| ≤14 Tage bis Event | Tapering-Modus | **6** · 9 · **10** · **11** |
| 0–6 Tage bis Event | Rennwoche-Modus | **6** · **8** · **10** · **11** · **13** · **16** |
| 1–14 Tage nach Event | Recovery-Modus | 9 · **10** · **11** |
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/coach/SKILL.md
git commit -m "feat(coach): Ladematrix ohne hardcoded KW-Nummern"
```

---

### Task 4: Add Taper-Checkliste output format and Taper-Anxiety response

**Files:**
- Modify: `.claude/skills/coach/SKILL.md` (Schritt 4: Output section)

Context: Two additions to the Output section — a Taper-Checkliste block that gets generated in Tapering-Modus, and a Taper-Anxiety response template.

- [ ] **Step 1: Add Taper-Checkliste to Schritt 4 Output**

After the `### 📅 Ausblick 4 Wochen` block, add:

```markdown
### 🗓 Taper-Checkliste (nur bei Tapering-Modus und Rennwoche-Modus ausgeben)

Immer wenn `tage_bis_event ≤ 7`, diese Tag-für-Tag-Liste ausgeben:

```
| Tag | Training | Ernährung | Schlaf | Check |
|---|---|---|---|---|
| T-6 | LIT 60min easy | Normal + leicht mehr KH | Ziel 8h | ☐ |
| T-5 | LIT 45min oder Pause | Normal + mehr KH (7g/kg) | Ziel 8h | ☐ |
| T-4 | Aktivierung 30min | Carb-Loading Start (8g KH/kg) | Ziel 8–9h | ☐ |
| T-3 | Pause oder 20min Easy | Carb-Loading voll (10g KH/kg) | Ziel 9h | ☐ |
| T-2 | Aktivierun.zwo | Carb-Loading (10g KH/kg) | Ziel 9h | ☐ |
| T-1 | Pause / 20min Easy Spin | Leichtes Frühstück + KH-reich Mittag | Früh ins Bett | ☐ |
| T-0 | 🏁 Renntag | Renntag-Frühstück 3h vorher (150g KH) | — | ☐ |
```

KH-Mengen für Stefan (88kg): 7g/kg = 616g · 8g/kg = 704g · 10g/kg = 880g
```

- [ ] **Step 2: Add Taper-Anxiety response pattern to Schritt 3 Entscheidungslogik**

At the end of the `### Tapering-Modus` section, add:

```markdown
**Taper-Anxiety erkennen und behandeln:**
Wenn Stefan während Tapering schreibt: "ich fühle mich schlapp", "reicht das", "sollte ich mehr trainieren", "fühle mich faul", "bin ich fit genug" — dies ist Taper-Anxiety. Standardantwort:
1. Bestätigen dass das Gefühl normal ist (Glykogenspeicher füllen sich, Muskeln reparieren — das fühlt sich träge an)
2. TSB-Prognose ausgeben (konkrete Zahl beruhigt)
3. Kein Extra-Training — jede zusätzliche Einheit kostet mehr als sie bringt
4. Letztes Training war ausreichend — Fitness verliert man in 14 Tagen nicht
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/coach/SKILL.md
git commit -m "feat(coach): Taper-Checkliste + Taper-Anxiety-Handling"
```

---

### Task 5: Add "events are never hardcoded" rule to Coaching-Philosophie

**Files:**
- Modify: `.claude/skills/coach/SKILL.md` (section `## Coaching-Philosophie`)

Context: Make explicit that event dates always come from `athlete/profil.md`, never from memory or hardcoded references.

- [ ] **Step 1: Add rule to Coaching-Philosophie → Grundregeln**

At the end of `### Grundregeln`, add:

```markdown
- **Event-Daten nie hardcoden**: Renndaten kommen immer aus `athlete/profil.md` → Saisonziele. Wenn Stefan ein neues Event nennt, dieses sofort in `athlete/profil.md` eintragen — nie nur in `COACHING_AKTE.md` oder `CLAUDE.md`. Nur `profil.md` ist die autoritative Quelle für Taper-Triggering.
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/coach/SKILL.md
git commit -m "feat(coach): Regel — Events immer aus profil.md, nie hardcoded"
```

---

### Task 6: Enrich coaching_science.md Section 6 with carb-loading and TT warm-up

**Files:**
- Modify: `coaching_science.md` (after line 157, within Section 6)

Context: Section 6 currently ends with the TSB-Ziel and a horizontal rule. Add two new subsections: Carb-Loading-Protokoll (structured, day-by-day) and Renntag Warm-up für Zeitfahren.

- [ ] **Step 1: Find the end of Section 6 in coaching_science.md**

Locate the line:
```
**TSB-Ziel**: +10 bis +20 am Renntag. Keine neuen Belastungsreize in letzten 10 Tagen.
```
followed by `---`

- [ ] **Step 2: Insert Carb-Loading and Warm-up content before the `---`**

After `**TSB-Ziel**: +10 bis +20 am Renntag. Keine neuen Belastungsreize in letzten 10 Tagen.` and before `---`, insert:

```markdown

### Carb-Loading-Protokoll (vor Ausdauerevents >2h)

Wissenschaftliche Basis: Bergström et al. (1967) – Glykogensupercompensation. Burke et al. (2011, IJSNEM): 10g KH/kg/Tag für 24–48h vor Event maximiert Glykogenspeicher auf ~750mmol/kg DM. Jeukendrup (2017): Bei gut trainierten Athleten reichen 24–36h Carb-Loading.

**Stefan-spezifisch (88kg):**

| Zeitraum | KH-Ziel | Beispielquellen | Hinweise |
|---|---|---|---|
| T-3 (3 Tage vor Rennen) | 7g/kg = 616g | Normal essen + extra Pasta/Reis | Fett und Protein normal |
| T-2 | 8g/kg = 704g | Pasta, Reis, Brot, Bananen, Gels | Ballaststoffe reduzieren |
| T-1 | 10g/kg = 880g | Weißer Reis, Weißbrot, Maltodextrin | Kein Salat, kein Rohkost |
| Renntag-Frühstück (3h vor Start) | 150–200g KH | Reis + Honig, Weißbrot + Marmelade, Gels | Fett und Protein minimal |
| 30min vor Start | 30–40g KH | Gel + Wasser | Koffein-Gel wenn gewünscht |

**Wichtig:** Während des Carb-Loadings +500–700ml mehr Wasser/Tag trinken (Glykogen bindet Wasser ~3:1).

### Renntag Warm-up (Zeitfahren)

Wissenschaftliche Basis: Burnley et al. (2005, JAP): VO2-Kinetik-Priming durch Warm-up reduziert O2-Deficit in den ersten Minuten des Zeitfahrens. Bishop (2003): 15–20min progressives Warm-up + kurze Intensität optimiert Muskeltemperatur und metabolische Bereitschaft.

**Standardprotokoll Zeitfahren (35–40min gesamt):**

```
1. 10min @ 160–180W (Z1, locker einkurbeln)
2. 5min @ 200–230W (Z2, Aerob aufwärmen)
3. 2× 1min @ 300–320W (FTP-Bereich), 2min Pause dazwischen
4. 1× 20s @ 400–430W (neurales Priming)
5. 5min @ 160W (Auskurbeln, klar werden)
→ Start: 3–5min nach Ende des Warm-ups
```

Bei Massenstart-Rennen (kein Zeitfahren): Warm-up 20min, weniger Intensität, mehr Aerob.
```

- [ ] **Step 3: Commit**

```bash
git add coaching_science.md
git commit -m "feat(science): Carb-Loading-Protokoll + Renntag Warm-up in Sektion 6"
```

---

### Task 7: Update athlete/profil.md to be the authoritative event source

**Files:**
- Modify: `athlete/profil.md` (Saisonziele section)

Context: Add explicit date fields so the skill can parse them unambiguously. Currently the dates are embedded in prose. Make them machine-readable for the skill.

- [ ] **Step 1: Add structured events table to profil.md**

In `athlete/profil.md`, after the existing Saisonziele text, add a new subsection:

```markdown
### Event-Kalender (autoritativ für Taper-Triggering)

| Event | Datum | Tage bis Event (auto) | Charakter | Taper-Start |
|---|---|---|---|---|
| RadRace 120 – Zeitfahren | 2026-06-12 | — | TT + Rennen | 2026-05-29 (T-14) |
| Rosenheimer Radmarathon | 2026-06-28 | — | 197km / 3.550hm | 2026-06-14 (T-14) |

*"Tage bis Event" wird vom Coach-Skill beim Aufruf berechnet (heute − Event-Datum). Neue Events hier eintragen.*
```

- [ ] **Step 2: Commit**

```bash
git add athlete/profil.md
git commit -m "feat(profil): Event-Kalender als autoritative Taper-Quelle"
```

---

## Self-Review

**Spec coverage:**
- ✅ Dynamic event detection (Tasks 1, 3, 5)
- ✅ TSB-Prognose (Task 2)
- ✅ Taper-Checkliste (Task 4)
- ✅ Taper-Anxiety-Handling (Task 4)
- ✅ Carb-Loading countdown (Task 6)
- ✅ Event-agnostic language throughout (Tasks 1–5)
- ✅ Authoritative event source (Task 7)
- ✅ TT Warm-up protocol (Task 6)

**Placeholder scan:** No TBDs, no "add appropriate handling" — all content is concrete.

**Consistency:** `athlete/profil.md` is named as the event source in Tasks 1, 5, and 7. TSB decay constants (0.965 / 0.916) are stated once in Task 2 and not duplicated.
