# Coaching-System – Schnellreferenz

*Automatisch geladen beim Öffnen dieses Projekts*

## Athlet & Aktueller Stand

| | |
|---|---|
| **Athlet** | Stefan |
| **Zeitzone** | Europe/Berlin (München) · Sommer: UTC+2 (CEST) |
| **⚠️ Verletzung** | Angebrochener Halswirbel (Unfall 28.6.) · Laufen + Rad freigegeben · Rad seit Sept. wieder verfügbar (147km am 12.9.) |
| **FTP** | 305W (Sentiero) · 3,35 W/kg · 91kg · *Referenz, aktuell nicht trainingsleitend* |
| **Hauptrennen** | ~~RadRace 120~~ ✅ · 12.–14. Juni 2026 · **KW24** · abgeschlossen |
| **Nebenrennen** | ~~Rosenheimer Radmarathon~~ ⚠️ · 28. Juni 2026 · **KW26** · nach 45,8km Unfall, abgebrochen |
| **Zielevent** | 🎯 Karlsfelder Seelauf · 20. September 2026 · **KW38** · 10km Lauf – max. Pace |
| **Aktuelle KW** | KW38 (14.–20. September 2026) · **Rennwoche** |
| **Aktuelle Phase** | Rennvorbereitung · Renntempo einprägen, kein Aufbau mehr möglich |
| **Nächste Phase** | KW38 Rennwoche (Mujika, 3 Touches) · danach Neuaufbau |
| **Tage bis Rennen** | **1** (Karlsfelder Seelauf So 20.9.) |
| **CTL** | 22,2 (19.9.) · ATL 32,3 · TSB −10 · Readiness 70 🟡 (HRV 57, Schlaf 8,5h, RP 53) · TSB bei dieser CTL kein Steuerungssignal |
| **🎯 Renntempo** | **6:30–6:40/km → ~66:00** — Stefans Entscheidung 14.9. (Coach-Ableitung war 6:50 aus 3×7min: 6:34/6:43/6:47 @ HF 172) · PR 71:28 |
| **Renntaktik** | km 1–2 **6:45** (HF <175) · km 3–7 6:35 · **km 5 HF-Entscheidung** (≤177 drücken · 178–181 halten · >182 auf 6:45 zurück) · km 8–10 6:30+ |
| **⚠️ Referenzwerte** | Lauf 4.9. war Kreta/nüchtern/früh → **nicht als Tempo-Referenz nutzen**. Bedingungen immer miterfassen. |
| **⚠️ Wade / Kadenz** | MTSS-Verdacht Soleus/Tibia · **Gewohnte Kadenz ~140 spm** (auch bei Tempo) = Hauptursache · Arbeitsziel **155–165** (Metronom 160), nach dem Rennen 165–170 |
| **Wochenstruktur** | Kern **Mo/Mi/Fr früh** · Wochenende nur Bonus (KW31+32 beide am WE gescheitert) |
| **Steuerung** | Easy-Cap **165 bpm** · ⚠️ Lauf-HF liegt 25–30 bpm über Rad – Easy-Run = 155–165 bpm, **nie unter 160 cappen** (Details `athlete/profil.md`) |

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
- Ausblick 4 Wochen (aus `planung/kw[N].md` bis kw[N+3].md) – rechts neben dem Wochenplan
- Power Bestwerte All-Time (Rad, 11 Dauern)
- Lauf Bestwerte All-Time (Tempokurven, 7 Distanzen)

## Wichtige Regeln

- **Vor jedem Commit an `planung/kw*.md`: `python3 validate_plans.py` ausführen.** Prüft alle Wochenpläne gegen den echten Dashboard-Parser. Tag-Spalte muss exakt `Mo`/`Di`/… sein – **kein Datum** (`Mo 7.9.` bricht den Parser lautlos, das Dashboard bleibt dann leer). Pflichtformat: 6 Spalten + `**Total**`-Zeile.

- Alle Workouts laufen auf **%FTP** → .zwo Dateien skalieren automatisch
- **FTP-Update** nur nach formalem Test (3+10min Protokoll, outdoor, XCadey-Powermeter am Tarmac). ⚠️ FTP 305W stammt vom alten 4iiii-Setup → **neuer Test nötig, bevor Zonen wieder trainingsleitend sind.** Indoor = Tacx-Leistung (Aeroad ohne PM), nicht 1:1 mit Outdoor vergleichbar.
- **Periodisierungsplan** nur mit Stefans Zustimmung ändern
- **Git: immer direkt auf `main` committen und pushen** – auch in Cloud-/Web-Sessions (Claude-App). Keine Session-Branches, keine PRs: das Dashboard baut aus `main`, alles andere ist für Stefan unsichtbar. Vor dem Push `git pull --rebase`.
- Lauf-Workouts: kein .zwo möglich → Beschreibung im Output, manuell in TP einpflegen
- HIT/VO2max ist **kein Neuland** – Stefan hat Ötztaler 2025 absolviert
