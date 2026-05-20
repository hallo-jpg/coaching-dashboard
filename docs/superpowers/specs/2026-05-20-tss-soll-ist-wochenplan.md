# TSS Soll/Ist-Abgleich im Wochenplan

## Goal

Für jeden abgeschlossenen und ausgefallenen Tag im Wochenplan-Widget den geplanten TSS-Wert neben dem tatsächlichen anzeigen — als explizite Ist/Soll-Beschriftung.

## Architecture

Reine Template-Änderung in `dashboard.template.html`. `day.tss_plan` ist bereits in allen Day-Objekten vorhanden und wird heute schon für Zukunftstage gerendert. Kein Python-Change, kein MCP-Change.

## Behavior

### Abgeschlossene Tage (`day.done`)

Aktuell: `✅ 92 TSS`

Neu (rechtsbündig gestapelt):
```
Ist  92
Soll 85
```
- "Ist" in `var(--green)` + Wert fett
- "Soll" in `var(--muted)` + Wert normal
- Schriftgrößen: Ist 0.72rem, Soll 0.6rem
- Wenn `day.tss_plan == 0`: nur `✅ 92 TSS` wie bisher (kein Soll-Wert verfügbar)

### Ausgefallene Tage (`day.missed`)

Aktuell: `Ausgefallen` Badge

Neu:
```
Ausgefallen
Soll 95 TSS
```
- Badge bleibt oben
- Soll-TSS darunter in `var(--muted)` 0.6rem
- Wenn `day.tss_plan == 0`: nur Badge wie bisher

### Zukünftige und Ruhetage

Unverändert.

## File

- Modify: `dashboard.template.html` — Abschnitt `day.done` (Zeile ~818) und `day.missed` (Zeile ~825)
