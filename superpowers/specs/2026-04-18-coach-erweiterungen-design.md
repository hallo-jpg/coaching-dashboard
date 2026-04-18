# Design: Coach Skill Erweiterungen
*2026-04-18 · Genehmigt durch Stefan*

## Scope

Zwei unabhängige Erweiterungen des Coach Skills (`SKILL.md`):

1. **Automatische Block-Skizze** — 4-Wochen-Ausblick im Dashboard wird nach jeder Skill-Invokation automatisch aktualisiert, nicht nur bei expliziter Wochenplanung.
2. **Monats-Retrospektive** — Neuer Skill-Modus, der auf Abruf eine strukturierte Monatsanalyse erstellt und in der Coaching-Akte speichert.

---

## Feature 1: Automatische Block-Skizze

### Problem heute
Der 4-Wochen-Ausblick in `dashboard.html` wird nur bei `Wochenplanung`- und `Block-Skizze`-Modus aktualisiert. Bei Ad-hoc-Anpassungen (Einheit ausgefallen, Terminverschiebung) oder Mid-Week Check-Ins bleibt die Tabelle veraltet — sie zeigt den alten Plan, obwohl sich der Kontext geändert hat.

### Lösung
In **Schritt 5 / Dateien aktualisieren** von SKILL.md wird die Regel erweitert: dashboard.html Ausblick-Tabelle wird bei **jeder** Skill-Invokation aktualisiert, unabhängig vom Modus. Ausnahme: reine FTP-Update-Aufrufe (kein Plankontext).

### Logik für die Neuberechnung
- **Aktuelle Woche (KW N)**: Status aus `kw[N].md` — wenn TSS Ist < Soll, wird das Delta notiert
- **Nächste 3 Wochen**: aus `periodisierung.md`, angepasst falls Verschiebungen bekannt
- Bei Krankheit/Ausfall: Kommentar in der Ausblick-Zeile (z.B. „nach Rückkehr")
- Format bleibt identisch: 4 `<tr>` Zeilen, aktive Woche mit Accent-Hintergrund

### Änderung in SKILL.md
- Schritt 5 / Punkt 8 (dashboard.html): Regel ergänzen — Ausblick-Tabelle ist **immer** zu aktualisieren, nicht nur bei Wochenplanung
- Modus-Tabelle in Schritt 2: Kein neuer Modus nötig — ist eine stille Erweiterung bestehender Modi

---

## Feature 2: Monats-Retrospektive

### Trigger
```
/coach Monats-Retro [Monat]
```
Beispiel: `/coach Monats-Retro April`

### Modus-Erkennung (Schritt 2)
Neuer Eintrag in der Modus-Tabelle:
- Signal: `"Monats-Retro"`, `"Retro [Monat]"`, Monatsname + Review-Kontext
- Modus: **Monats-Review**

### Datenzugriff
1. `planung/archiv/kw[N].md` — alle KW-Dateien des Monats (TSS Soll/Ist, Status, Feedback)
2. `get_weekly_review(week_start: Montag jeder KW)` — Zonen, Polarisation, HRV-Verlauf
3. `COACHING_AKTE.md` — Coach-Notizen des Monats als Kontext

### Output-Format (Schritt 4)

```
## 📊 Monats-Retrospektive [Monat YYYY]

### Zahlen
| KW | TSS Soll | TSS Ist | Compliance | LIT-Anteil | Besonderheit |
|---|---|---|---|---|---|
| KW15 | ~396 | 114 | 29% | 96% | Urlaub |
| KW16 | ~493 | 0 | 0% | – | Krank |

**Gesamt:** Soll ~889 · Ist 114 · Compliance 13%

### Zonen-Compliance
- LIT-Anteil (Wochen mit Training): XX%
- Z3-Drift: XX% (Grenze: 15%)
- Polarisations-Index: XX%

### Readiness-Verlauf
- Tiefstwert: XX/100 (Datum, Kontext)
- Krank-Risiko-Muster: ja/nein

### Coach-Einschätzung
[2–4 Sätze: was lief gut, was war der Hauptfaktor für Abweichungen, kein Beschönigen]

### Prio nächster Monat
[1 klarer Fokus — nicht mehr]
```

### Speicherung
Wird als neuer Abschnitt in `COACHING_AKTE.md` unter einem neuen Heading `## Monats-Retrospektiven` gespeichert (chronologisch, neueste zuerst).

### Dashboard-Karte
Nach jeder Retro-Erstellung wird `dashboard.html` um eine **Monats-Retrospektive-Karte** aktualisiert (zwischen Kraft-Karten und Ausblick-Tabelle). Die Karte zeigt:
- Monat + Compliance-Zahl prominent
- TSS-Tabelle (KW-Zeilen, kompakt)
- Zonen-Compliance (LIT-Balken)
- Coach-Prio als farbige Zeile

Format: gleicher Stil wie `ausblick-card` (dark surface, border-radius 16px). Die Karte bleibt stehen bis die nächste Retro überschreibt. Bei noch keiner Retro: Karte nicht anzeigen.

### Coaching_science-Sektionen
Keine spezifischen Sektionen nötig — rein datengetrieben. Polarisations-Check aus Sektion 2 wenn Z3-Drift > 15%.

---

## Nicht im Scope

- Automatischer Cron-Trigger für Retro (zu viel Komplexität, Handaufruf reicht)
- Vergleich mit Vormonat (nice-to-have, aber nicht für v1)
