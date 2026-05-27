# Krankheits-Protokoll Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wenn Stefan "ich bin krank" meldet, führt der Coach-Skill ein 3-Fragen-Interview durch, berechnet Rückkehrdatum (Neck-Check + Fieber-Regel) und passt `planung/kw[N].md` mit Rampe an.

**Architecture:** Zwei Edits an `.claude/skills/coach/SKILL.md`. Task 1 ergänzt die Modus-Erkennungstabelle um eine Krank-Modus-Zeile. Task 2 fügt den vollständigen "Schritt K: Krank-Modus"-Block nach der Modus-Erkennungstabelle ein.

**Tech Stack:** Markdown-only. Keine Code-Änderungen. Skill-Datei wird von Claude zur Laufzeit gelesen.

---

## File Map

| Datei | Änderung |
|---|---|
| `.claude/skills/coach/SKILL.md` | Task 1: Krank-Modus in Modus-Erkennungstabelle · Task 2: Schritt K — vollständiges Protokoll |

---

### Task 1: Krank-Modus in Modus-Erkennung eintragen

**Files:**
- Modify: `.claude/skills/coach/SKILL.md` (Modus-Erkennungstabelle, ca. Zeile 238–252)

- [ ] **Step 1: Datei lesen und Einfügestelle bestimmen**

Öffne `/Users/stefan/Documents/Claude Code/Coaching/.claude/skills/coach/SKILL.md` und suche die Zeile:
```
| "fällt aus", "muss verschieben", Terminkonflikt | **Ad-hoc Anpassung** |
```
Der neue Krank-Modus-Eintrag wird **direkt davor** eingefügt (zwischen Wochen-Review-Zeile und Ad-hoc-Zeile).

- [ ] **Step 2: Neue Zeile in Modus-Erkennungstabelle einfügen**

Ersetze:
```
| "fällt aus", "muss verschieben", Terminkonflikt | **Ad-hoc Anpassung** |
```

Durch:
```
| "krank", "Fieber", "Erkältung", "fühle mich nicht gut", "bin krank", "Halsweh", "Grippe" | **Krank-Modus** → Schritt K ausführen, alle anderen Schritte überspringen |
| "fällt aus", "muss verschieben", Terminkonflikt | **Ad-hoc Anpassung** |
```

- [ ] **Step 3: Prüfen**

```bash
grep -n "Krank-Modus\|krank\b" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md | head -5
```

Erwartete Ausgabe: Zeile mit "Krank-Modus" in der Tabelle sichtbar, Zeilennummer vor "Ad-hoc".

- [ ] **Step 4: Commit**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
git add .claude/skills/coach/SKILL.md
git commit -m "feat(coach): Krank-Modus in Modus-Erkennung eingetragen"
```

---

### Task 2: Schritt K — vollständiges Krank-Protokoll einfügen

**Files:**
- Modify: `.claude/skills/coach/SKILL.md` — neuen Block nach der Modus-Erkennungstabelle einfügen (nach der `---` Linie die auf `## Schritt 3: Entscheidungslogik` folgt, also vor Schritt 3)

- [ ] **Step 1: Einfügestelle bestimmen**

Suche in der Datei die Zeile:
```
## Schritt 3: Entscheidungslogik
```

Der neue Schritt K wird **direkt davor** eingefügt (zwischen `---` und `## Schritt 3`).

- [ ] **Step 2: Schritt K einfügen**

Füge direkt vor `## Schritt 3: Entscheidungslogik` ein:

```markdown
## Schritt K: Krank-Modus

**Wann ausführen:** Nur wenn Modus-Erkennung Krank-Modus ergibt. Alle anderen Schritte (0a, 0, 1, 2, 3, 4, 5) überspringen — Schritt K ersetzt den gesamten normalen Ablauf.

### Interview

Stelle Stefan alle 3 Fragen in **einer** Nachricht:

```
Verstanden — ich kümmere mich darum. Drei kurze Fragen damit ich den Plan anpassen kann:

1. Welcher Tag der Krankheit? (Tag 1 = heute begonnen, Tag 3 = seit 3 Tagen)
2. Fieber? (ja + Temperatur wenn bekannt / nein)
3. Symptome unterhalb des Halses? Husten, Brustenge oder Ganzkörperschmerzen — ja oder nein?
```

### Rückkehr-Logik (nach Stefans Antwort)

**Neck-Check-Regel:**
| Symptome | Rückkehrstart |
|---|---|
| Nur oberhalb Hals (Schnupfen, Hals) | Symptomfrei + 24h → LIT möglich |
| Unterhalb Hals (Husten, Körperschmerzen) | Symptomfrei + 48h → Spaziergang; + 72h → LIT |

**Fieber-Überlagerungsregel (immer zuerst prüfen):**
Falls Fieber vorhanden: Fieberfrei + 24h warten, dann Neck-Check-Regel anwenden.

**Verbleibende Kranktage schätzen (für Rückkehrdatum):**
- Tag 1–2, keine Komplikationen → noch ~3–5 Tage
- Tag 3+ → noch ~2–3 Tage
- `rückkehrtag = heute + geschätzte_kranktage_rest + wartefrist_laut_tabelle`

### Rampe nach Wiedereinstieg

| Offset ab Rückkehrtag | Aktivität |
|---|---|
| +0 | Spaziergang / Mobilität ≤ 30 min |
| +1 | LIT 45 min, RPE ≤ 12, HF < 130 |
| +2 | LIT 60 min, Z1–Z2 normal |
| +3–4 | Normales LIT-Programm |
| +5+ | Volle Last möglich |

### Plananpassung `planung/kw[N].md`

1. Alle Einheiten **bis und einschließlich Tag vor Rückkehrtag** → Status `❌ Krank`, TSS Ist = 0
2. Verbleibende Tage der Woche → durch Rampe ersetzen (Tabelle oben, ab +0)
3. TSS-Wochenziel-Zeile in der Datei durch folgenden Text ersetzen:

```markdown
> **Krankheitswoche** — TSS-Ziel entfällt. Rückkehrtag: [Datum]. Rampe läuft bis [Datum +5].
```

4. Datei speichern (kein extra git commit — COACHING_AKTE-Commit folgt)

### Sonderfall: < 3 Wochen bis nächstem Event

Prüfe `tage_bis_event` aus `athlete/profil.md`:
- Falls `tage_bis_event < 21`: Folgenden Hinweis an den Output anhängen:

```
⚠️ Taper-Phase — lieber 1 Extratag Pause als zu früh zurück.
CTL-Verlust durch Krankheit wird nicht kompensiert; Taper läuft beim nächsten Wochenplan normal weiter.
```

### COACHING_AKTE.md Eintrag

Anfügen:

```markdown
## [Datum heute] Krankheit KW[N]
Krank ab [Datum] · [oberhalb/unterhalb Hals] · Fieber: [ja X°C / nein]
Rückkehrtag: [Datum] · [N] Trainingstage ausgefallen
→ Rückkehrwoche KW[N+1]: TSS-Ziel 50%, nur LIT
```

### Output im Chat

```
🤒 Krank-Modus

Rückkehrdatum: [Datum] (LIT ab +1) · [Datum +5] (volle Last)

Plananpassung KW[N]:
[angepasste Wochentabelle — ❌ Krank bis Rückkehrtag, dann Rampe]

Beim nächsten Wochenplan (KW[N+1]) plane ich automatisch mit 50% TSS und nur LIT.
```

---
```

- [ ] **Step 3: Prüfen dass Schritt K vor Schritt 3 steht**

```bash
grep -n "## Schritt K\|## Schritt 3" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Erwartete Ausgabe: Schritt K hat niedrigere Zeilennummer als Schritt 3.

- [ ] **Step 4: Commit**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
git add .claude/skills/coach/SKILL.md
git commit -m "feat(coach): Schritt K — Krank-Modus mit Neck-Check, Rampe, Plananpassung"
```

---

## Self-Review

**Spec-Coverage:**
- ✅ Trigger-Wörter in Modus-Erkennung (Task 1)
- ✅ 3-Fragen-Interview in einer Nachricht (Task 2)
- ✅ Neck-Check-Regel (oberhalb/unterhalb Hals) mit Rückkehrtabelle
- ✅ Fieber-Überlagerungsregel
- ✅ Schätzung verbleibende Kranktage für Rückkehrdatum
- ✅ Rampe +0 bis +5 (konservatives Protokoll)
- ✅ `planung/kw[N].md` Anpassung: ❌ Krank + Rampe + TSS-Ziel-Notiz
- ✅ Sonderfall Taper-Phase (< 21 Tage bis Event)
- ✅ COACHING_AKTE Eintrag mit Rückkehrwoche-Hinweis
- ✅ Output-Format mit Rückkehrdaten + angepasster Wochentabelle
- ✅ Hinweis für Schritt 0a: TSS-Compliance entfällt bei Krankheitswoche (via COACHING_AKTE-Eintrag erkennbar)

**Placeholder-Scan:** Keine TBDs. Alle Tabellen konkret. Rückkehrdatum-Berechnung explizit mit Formel.

**Konsistenz:** `rückkehrtag`, `tage_bis_event`, `kw[N]` konsistent mit bestehendem Skill-Sprachgebrauch.
