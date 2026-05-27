# Wochen-Retro Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Beim Aufruf "neue KW planen" schließt der Coach-Skill automatisch die Vorwoche mit einer strukturierten Retro ab und archiviert sie — ohne dass Stefan einen extra Befehl eingeben muss.

**Architecture:** Zwei Edits an `.claude/skills/coach/SKILL.md`. Task 1 fügt einen neuen "Schritt 0a" vor "Schritt 0" ein — Pre-Check, API-Aufruf, Retro-Format, Gesamtnote-Logik. Task 2 ergänzt die Periodisierungsempfehlung-Logik und aktualisiert Schritt 5 (Dateien aktualisieren) Item 2 auf den neuen Prozess.

**Tech Stack:** Markdown-only. Keine Code-Änderungen. Skill-Datei wird von Claude zur Laufzeit gelesen.

---

## File Map

| Datei | Änderung |
|---|---|
| `.claude/skills/coach/SKILL.md` | Task 1: neuer Schritt 0a vor Schritt 0 · Task 2: Periodisierungsempfehlung + Schritt 5 Update |

---

### Task 1: Schritt 0a — Pre-Check, API-Aufruf, Retro-Format, Gesamtnote

**Files:**
- Modify: `.claude/skills/coach/SKILL.md` (vor der Zeile `## Schritt 0: Metriken & Review automatisch abrufen`, ca. Zeile 24)

- [ ] **Step 1: Datei lesen und genaue Einfügestelle bestimmen**

Öffne `/Users/stefan/Documents/Claude Code/Coaching/.claude/skills/coach/SKILL.md` und suche die Zeile:
```
## Schritt 0: Metriken & Review automatisch abrufen
```
Der neue Schritt 0a wird **direkt davor** eingefügt (zwischen `---` und `## Schritt 0`).

- [ ] **Step 2: Schritt 0a einfügen**

Füge direkt vor `## Schritt 0: Metriken & Review automatisch abrufen` ein:

```markdown
## Schritt 0a: Vorwoche prüfen & Retro (nur bei Wochenplanung)

**Wann ausführen:** Nur wenn der Aufruf eine neue Wochenplanung ist (Modus-Erkennung ergibt Planungs-Modus oder ähnlich). Bei Ad-hoc-Anfragen, Taper-Modus und Monats-Retro überspringen.

### Pre-Check

Prüfe ob `planung/kw[N-1].md` existiert (d.h. die Datei liegt in `planung/`, nicht in `planung/archiv/`):
- **Datei nicht vorhanden oder bereits in archiv/** → Schritt 0a überspringen, weiter mit Schritt 0
- **Datei vorhanden in `planung/`** → Retro ausführen (Schritte unten)

### Daten abrufen

Rufe auf: `get_weekly_review(week_start: Montag der Vorwoche)`
→ Liefert: TSS Ist/Soll, Zonen-Verteilung (Z1–Z7), HRV-Verlauf (Tageswerte), abgeschlossene Aktivitäten

### Retro berechnen

**TSS-Erreichung:** `tss_pct = tss_ist / tss_soll × 100`

**Polarisation:** Aus Zonen-Daten (intervals.icu Mapping anwenden — siehe Schritt 0):
- LIT = Z1+Z2, Grauzone = Z3+unteres Z4, HIT = Z5+Z6+Z7
- Bewertung: `Z3+Z4 < 15% Gesamtvolumen` → gut polarisiert

**HRV-Trend:** Vergleich erster und letzter HRV-Wert der Woche:
- `↗ steigend` = letzter > erster + 3 Punkte
- `→ stabil` = Differenz ≤ 3 Punkte
- `↘ fallend` = letzter < erster − 3 Punkte
- Differenz für Schwellen-Prüfung: `hrv_abfall = erster_wert − letzter_wert`

**Gesamtnote:**
| Bedingung | Note |
|---|---|
| TSS ≥ 85% UND HRV stabil oder steigend | 🟢 Gut |
| TSS 65–84% ODER HRV leicht fallend (≤10 Punkte) | 🟡 Mittel |
| TSS < 65% ODER HRV stark fallend (>10 Punkte) | 🔴 Schwach |
| TSS > 120% (Überbelastung) | 🟡 Mittel + Hinweis auf Überbelastung |

### Retro-Abschnitt ausgeben (im Chat) und in Datei schreiben

**Format — exakt so an `planung/kw[N-1].md` anhängen:**

```markdown
## Wochen-Retro

**TSS:** Ist [tss_ist] / Soll [tss_soll] → [tss_pct]% ([✅ im Plan / ⚠️ unter Plan / 🔥 über Plan])
**Polarisation:** Z1 [X]% · Z2 [Y]% · Z3 [Z]% → [gut polarisiert / zu viel Grauzone / etc.]
**HRV-Trend:** [↗ steigend / → stabil / ↘ fallend] ([erster_wert] → [letzter_wert])

### Einheiten
| Tag | Workout | TSS Ist | Status | Notiz |
|---|---|---|---|---|
[Tabelle aus der Planung — Status ✅/❌/⬜ und TSS Ist aus intervals.icu-Aktivitäten befüllen]

### Bewertung
**Was lief gut:** [konkret aus den Aktivitätsdaten und Kontext ableiten]
**Was fehlte / warum:** [konkret, sachlich, kein Vorwurf]
**Lernpunkt für KW[N]:** [eine konkrete Handlungsempfehlung]

### Gesamtnote
[🟢 Gut / 🟡 Mittel / 🔴 Schwach] — [ein Satz Begründung]
```

### Datei archivieren

Nach dem Schreiben des Retro-Abschnitts:
```
git mv planung/kw[N-1].md planung/archiv/kw[N-1].md
git commit -m "archiv: KW[N-1] Retro abgeschlossen"
```

### COACHING_AKTE.md Eintrag anfügen

Unter dem neuesten Eintrag in `COACHING_AKTE.md` anfügen:

```markdown
## [Datum heute] KW[N-1] Retro
[🟢/🟡/🔴] TSS [tss_ist]/[tss_soll] ([tss_pct]%) · HRV [Trend] · [ein Satz Kernerkenntnis]
```

---
```

- [ ] **Step 3: Prüfen dass Schritt 0a korrekt vor Schritt 0 steht**

Nach der Änderung: grep -n "Schritt 0a\|Schritt 0:" in der Datei — Schritt 0a muss eine niedrigere Zeilennummer haben als Schritt 0.

```bash
grep -n "## Schritt 0" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Erwartete Ausgabe (Schritt 0a vor Schritt 0):
```
24:## Schritt 0a: Vorwoche prüfen & Retro (nur bei Wochenplanung)
XX:## Schritt 0: Metriken & Review automatisch abrufen
```

- [ ] **Step 4: Commit**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
git add .claude/skills/coach/SKILL.md
git commit -m "feat(coach): Schritt 0a — Wochen-Retro automatisch bei neuer Wochenplanung"
```

---

### Task 2: Periodisierungsempfehlung-Logik + Schritt 5 Update

**Files:**
- Modify: `.claude/skills/coach/SKILL.md` — zwei Stellen:
  1. Am Ende von Schritt 0a (nach dem `---` Abschluss von Task 1): Periodisierungsempfehlung-Block einfügen
  2. Schritt 5, Dateien aktualisieren, Item 2: Text aktualisieren

- [ ] **Step 1: Periodisierungsempfehlung-Block in Schritt 0a einfügen**

Suche die Zeile am Ende von Schritt 0a (die `---` Linie nach dem COACHING_AKTE-Block). Füge **vor** dieser `---` Linie ein:

```markdown
### Periodisierungsempfehlung (nur wenn Schwelle erreicht)

Prüfe ob eine der folgenden Bedingungen zutrifft:
- TSS-Erreichung < 75%
- TSS-Erreichung > 120%
- HRV-Abfall > 10 Punkte über die Woche
- Letzte zwei archivierte Wochen haben beide 🔴 oder 🟡 (aus `planung/archiv/` lesbar)

**Wenn keine Bedingung zutrifft:** Keine Empfehlung ausgeben — weiter mit Archivieren.

**Wenn mind. eine Bedingung zutrifft:** Konkrete Änderung vorschlagen und auf Bestätigung warten:

```
📋 Periodisierungsempfehlung:
→ [Konkrete Änderung, z.B. "KW18 TSS-Ziel von 420 auf 360 reduzieren"]
Grund: [eine Zeile Begründung aus den Daten]
Bestätigen? (ja / nein / später)
```

**Bei "ja":** `planung/periodisierung.md` entsprechend anpassen, Änderung in `COACHING_AKTE.md` dokumentieren:
```markdown
→ periodisierung.md angepasst: [was genau geändert wurde]
```

**Bei "nein" oder "später":** Keine Änderung, Eintrag in `COACHING_AKTE.md`:
```markdown
→ Empfehlung abgelehnt: [kurze Beschreibung der vorgeschlagenen Änderung]
```

**Dann:** Datei archivieren und COACHING_AKTE-Eintrag schreiben (wie oben beschrieben).
```

- [ ] **Step 2: Schritt 5 Item 2 aktualisieren**

Finde in `.claude/skills/coach/SKILL.md` die Zeile:
```
2. **`planung/kw[N-1].md`** – Status-Updates: ✅/❌, TSS Ist eintragen; danach in `planung/archiv/` verschieben wenn abgeschlossen
```

Ersetze durch:
```markdown
2. **`planung/kw[N-1].md`** – wird via **Schritt 0a** automatisch mit Retro-Abschnitt befüllt und nach `planung/archiv/` archiviert. Manuell anfassen nur wenn Schritt 0a übersprungen wurde (Ad-hoc-Modus).
```

- [ ] **Step 3: Prüfen**

```bash
grep -n "kw\[N-1\]" /Users/stefan/Documents/Claude\ Code/Coaching/.claude/skills/coach/SKILL.md
```

Erwartet: 2 Treffer — einer in Schritt 0a (Pre-Check), einer in Schritt 5 (aktualisierter Text).

- [ ] **Step 4: Commit**

```bash
cd "/Users/stefan/Documents/Claude Code/Coaching"
git add .claude/skills/coach/SKILL.md
git commit -m "feat(coach): Periodisierungsempfehlung + Schritt 5 auf Retro-Prozess aktualisiert"
```

---

## Self-Review

**Spec-Coverage:**
- ✅ Automatischer Trigger bei Wochenplanung (Schritt 0a Pre-Check)
- ✅ Überspringen bei Ad-hoc/Taper/Monats-Retro
- ✅ get_weekly_review-Aufruf für Vorwoche
- ✅ TSS Ist/Soll, Polarisation, HRV-Trend berechnet
- ✅ Retro-Format vollständig (alle Felder)
- ✅ Gesamtnote 🟢/🟡/🔴 mit Logik-Tabelle
- ✅ git mv + commit für Archivierung
- ✅ COACHING_AKTE Kurzeintrag
- ✅ Periodisierungsempfehlung mit Schwellen + Bestätigung-Flow
- ✅ Schritt 5 Item 2 aktualisiert

**Placeholder-Scan:** Keine TBDs. Alle Formate konkret mit Beispielwerten.

**Konsistenz:** `tss_ist`, `tss_soll`, `tss_pct`, `hrv_abfall` konsistent durch beide Tasks. `kw[N-1]` konsistent mit bestehendem Skill-Sprachgebrauch.
