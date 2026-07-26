# Coaching-System – Schnellreferenz

*Automatisch geladen beim Öffnen dieses Projekts*

## Athlet & Aktueller Stand

| | |
|---|---|
| **Athlet** | Stefan |
| **Zeitzone** | Europe/Berlin (München) · Sommer: UTC+2 (CEST) |
| **⚠️ Verletzung** | Angebrochener Halswirbel (Unfall 28.6.) · Laufen + Rad freigegeben · **Rad defekt → nur Laufen** |
| **FTP** | 305W (Sentiero) · 3,35 W/kg · 91kg · *Referenz, aktuell nicht trainingsleitend* |
| **CTL** | 24,1 (26.7.) – nach 4 Wochen Verletzungspause |
| **Hauptrennen** | ~~RadRace 120~~ ✅ · 12.–14. Juni 2026 · **KW24** · abgeschlossen |
| **Nebenrennen** | ~~Rosenheimer Radmarathon~~ ⚠️ · 28. Juni 2026 · **KW26** · nach 45,8km Unfall, abgebrochen |
| **Zielevent** | 🎯 Karlsfelder Seelauf · 20. September 2026 · **KW38** · 10km Lauf – max. Pace |
| **Aktuelle KW** | KW30 (20. Juli – 26. Juli 2026) |
| **Aktuelle Phase** | Lauf-Block KW31–38 · Woche 1: Reanimation (HF-Anker + Strides) |
| **Nächste Phase** | KW33–36 Schwellen-/Renntempo-Block · KW37–38 Taper + Rennwoche |
| **Wochen bis Rennen** | 8 (Karlsfelder Seelauf 20.9.) |
| **Steuerung** | KW31–32: **HF statt Pace** · Cap 150 bpm · Gehpausen erlaubt |

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
