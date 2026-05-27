# Wochen-Retro Design

**Ziel:** Beim Aufruf "KW[N] planen" schließt der Coach-Skill automatisch die Vorwoche ab — mit strukturierter Auswertung, optionaler Periodisierungsanpassung (mit Bestätigung) und Archivierung.

**Architektur:** Neuer Schritt 0a in `.claude/skills/coach/SKILL.md`, läuft als Pre-Check vor allen anderen Schritten. Kein eigener Modus — transparent in den Planungs-Aufruf integriert.

**Tech Stack:** Markdown-Edits an SKILL.md; Datenquellen: `get_weekly_review` (intervals.icu), `planung/kw[N-1].md`, `planung/periodisierung.md`, `COACHING_AKTE.md`

---

## Ablauf (Schritt 0a)

1. **Prüfe Archiv-Status:** Existiert `planung/kw[N-1].md` (nicht in `planung/archiv/`)?
   - Nein → Schritt 0a überspringen, normal weiter
   - Ja → Retro ausführen

2. **Daten abrufen:** `get_weekly_review(week_start: Montag der Vorwoche)` direkt in Schritt 0a aufrufen. Schritt 0 ruft danach denselben Endpunkt für die aktuelle Woche auf — kein Konflikt, andere Zeitfenster.

3. **Retro berechnen und ausgeben** (im Chat):
   - TSS Ist vs. Soll mit Prozent-Abweichung
   - Polarisations-Qualität (Z1/Z2/Z3-Verteilung)
   - HRV-Trend (Richtung + Extremwerte)
   - Einheiten-Tabelle finalisiert (✅/❌/⬜ + TSS Ist)
   - Bewertung: was lief gut, was nicht, warum
   - Lernpunkt für die neue Woche
   - Gesamtnote: 🟢 / 🟡 / 🔴

4. **Periodisierungsempfehlung** (nur wenn Abweichung signifikant):
   - Schwelle: TSS-Erreichung <75% oder >120%, oder HRV-Trend stark fallend (>10 Punkte)
   - Konkreter Vorschlag: welche KW, welcher Wert, warum
   - Warten auf Bestätigung ("ja" / "nein") bevor `planung/periodisierung.md` angepasst wird

5. **Archivieren:**
   - Retro-Abschnitt an `planung/kw[N-1].md` anhängen
   - Datei nach `planung/archiv/kw[N-1].md` verschieben (git mv)
   - Kurzeintrag in `COACHING_AKTE.md` anfügen

6. **Weiter mit Planungs-Ablauf** (Schritt 0–5 wie bisher)

---

## Retro-Format (Abschnitt in kw[N-1].md)

```markdown
## Wochen-Retro

**TSS:** Ist [X] / Soll [Y] → [Z]% ([Bewertung: ✅ im Plan / ⚠️ unter Plan / 🔥 über Plan])
**Polarisation:** Z1 [X]% · Z2 [Y]% · Z3 [Z]% → [gut polarisiert / zu viel Mittelzone / etc.]
**HRV-Trend:** [↗ steigend / → stabil / ↘ fallend] ([Mo XX → Fr XX])

### Einheiten
| Tag | Workout | TSS Ist | Status | Notiz |
|---|---|---|---|---|
[finalisierte Tabelle aus Planung]

### Bewertung
**Was lief gut:** [konkret]
**Was fehlte / warum:** [konkret, kein Vorwurf]
**Lernpunkt für KW[N]:** [eine Handlungsempfehlung]

### Gesamtnote
[🟢 Gut / 🟡 Mittel / 🔴 Schwach] — [ein Satz Begründung]

### Periodisierungsempfehlung
*(nur wenn Abweichung signifikant — sonst weglassen)*
→ Empfehle [konkrete Änderung] weil [Begründung]
→ Bestätigung abgewartet vor Änderung an periodisierung.md
```

---

## Gesamtnote-Logik

| Bedingung | Note |
|---|---|
| TSS ≥ 85% UND HRV stabil oder steigend | 🟢 Gut |
| TSS 65–84% ODER HRV leicht fallend | 🟡 Mittel |
| TSS < 65% ODER HRV stark fallend (>10 Punkte) | 🔴 Schwach |
| TSS > 120% (Überbelastung) | 🟡 Mittel (mit Hinweis) |

---

## Periodisierungsempfehlung-Schwellen

Empfehlung wird nur ausgegeben wenn mind. eine Bedingung zutrifft:
- TSS-Erreichung < 75% (deutlich unter Plan)
- TSS-Erreichung > 120% (deutlich über Plan)
- HRV-Abfall > 10 Punkte über die Woche
- Zwei aufeinanderfolgende Wochen mit 🔴 oder 🟡 (aus Archiv lesbar)

Bei Bestätigung: Skill passt `planung/periodisierung.md` an und dokumentiert Änderung in `COACHING_AKTE.md`.
Bei Ablehnung: Notiz in `COACHING_AKTE.md` "Empfehlung abgelehnt durch Stefan".

---

## COACHING_AKTE Eintrag

```markdown
## [Datum] KW[N-1] Retro

[🟢/🟡/🔴] TSS [Ist]/[Soll] ([Z]%) · HRV [Trend] · [ein Satz Kernerkenntnis]
[Falls Periodisierung angepasst: → periodisierung.md KW[X] angepasst: [was]]
```

---

## Betroffene Dateien

| Datei | Änderung |
|---|---|
| `.claude/skills/coach/SKILL.md` | Neuer Schritt 0a vor Schritt 0 |
| `planung/kw[N-1].md` | Retro-Abschnitt anhängen, dann via git mv archivieren |
| `planung/archiv/kw[N-1].md` | Zieldatei nach Archivierung |
| `COACHING_AKTE.md` | Kurzeintrag pro Woche |
| `planung/periodisierung.md` | Nur bei bestätigter Empfehlung |
