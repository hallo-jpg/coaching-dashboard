# Coaching-System – Schnellreferenz

*Automatisch geladen beim Öffnen dieses Projekts*

## Athlet & Aktueller Stand

| | |
|---|---|
| **Athlet** | Stefan |
| **Zeitzone** | Europe/Berlin (München) · Sommer: UTC+2 (CEST) |
| **FTP** | 305W (Sentiero) · 3,47 W/kg · 88kg |
| **VO2max** | 59 ml/min/kg (Sentiero) |
| **Hauptrennen** | RadRace 120 · 12.–14. Juni 2026 · **KW24** |
| **Nebenrennen** | Rosenheimer Radmarathon Tour V · 28. Juni 2026 · **KW26** · 197km / 3.550hm |
| **Aktuelle KW** | KW18 (28. April – 4. Mai 2026) |
| **Aktuelle Phase** | HIT-Aufbaublock Einstieg |
| **Nächste Phase** | HIT-Aufbau progressiv KW19–21 |
| **Wochen bis Rennen** | 6 |

## Coaching-Skill

```
/coach "BRIEFING"
```

**Aufruf-Beispiele** (HRV/CTL/TSB werden automatisch via MCP abgerufen):
```
/coach KW16 planen
plane mir die nächste Woche
/coach – ich bin krank, was jetzt?
/coach Donnerstag fällt aus, Umplanung nötig
/coach neues FTP: 318W nach Test
```

**Optional: Kontext mitgeben** der nicht automatisch verfügbar ist:
```
/coach KW17 | RPE letzte Einheit: 8/10 | Knie zwickt leicht
```

## Dateistruktur

| Datei | Inhalt | Aktualisiert durch |
|---|---|---|
| `athlete/profil.md` | Athletenprofil, Zonen, Geräte | Skill (bei FTP-Update) |
| `athlete/fortschritt.md` | FTP-Verlauf, VO2max, Tests | Skill |
| `planung/langfristplan.md` | **Mehrjähriger Entwicklungsplan, Jahreszyklus, CTL-Kurve** – läuft nie ab | Skill (bei Zielprofil-Änderung) |
| `planung/periodisierung.md` | Aktueller Saisonplan (KW14–27) – wird nach KW26 ersetzt | Skill (mit Zustimmung) |
| `planung/kw[N].md` | Aktuelle Wochenplanung | Skill |
| `planung/archiv/` | Abgeschlossene Wochen (Plan + Ist + Feedback) | Skill (nach Wochenabschluss) |
| `planung/workout_index.md` | Kompakter Workout-Index (55 Workouts) | Manuell |
| `coaching_science.md` | Wissenschaftliche Referenz (Rønnestad et al.) | Manuell |
| `COACHING_AKTE.md` | Änderungs-Log, Coach-Notizen, Fehlen-Log | Skill |

## Live Dashboard

Das Coaching-Dashboard wird **automatisch** aus intervals.icu-Daten generiert — der Skill muss es **nicht manuell anfassen**.

| | |
|---|---|
| **URL** | https://hallo-jpg.github.io/coaching-dashboard/ (Passwort-geschützt) |
| **Rebuild** | Stündlich via GitHub Actions + manuell triggerbar |
| **Generator** | `generate.py` + `dashboard.template.html` → `docs/dashboard.html` |
| **Datenquellen** | intervals.icu API: Wellness, Activities, Power-Curves, Pace-Curves, Wochenplan aus `planung/kw[N].md` |

**Karten im Dashboard (alle auto-generiert):**
- Recovery-Ring (Readiness Score), Trainingsform-Ring (CTL/ATL/TSB), Wochenziel-Ring (TSS-Compliance)
- Wochenplan (aus `planung/kw[N].md` + intervals.icu Aktivitäten)
- Polarisations-Monitor (letzte Woche Rad-Zonen)
- Readiness-Card mit HRV/Schlaf/TSB/Puls-Balken + Sparkline
- Ernährungs-Karte (Tagestyp, Protein-Ziel, Pre/During/Post, Tipps)
- Ausblick 4 Wochen (aus `planung/kw[N].md` bis kw[N+3].md)
- Power Bestwerte All-Time (Rad, 13 Dauern)
- Lauf Bestwerte All-Time (Tempokurven, 7 Distanzen)

## Wichtige Regeln

- Alle Workouts laufen auf **%FTP** → .zwo Dateien skalieren automatisch
- **FTP-Update** nur nach formalem Test (3+10min Protokoll, outdoor, 4iiii)
- **Periodisierungsplan** nur mit Stefans Zustimmung ändern
- Lauf-Workouts: kein .zwo möglich → Beschreibung im Output, manuell in TP einpflegen
- HIT/VO2max ist **kein Neuland** – Stefan hat Ötztaler 2025 absolviert
