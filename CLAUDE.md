# Coaching-System – Schnellreferenz

*Automatisch geladen beim Öffnen dieses Projekts*

## Athlet & Aktueller Stand

| | |
|---|---|
| **Athlet** | Stefan |
| **Zeitzone** | Europe/Berlin (München) · Sommer: UTC+2 (CEST) |
| **Beschwerden** | **keine** – Planung geht von beschwerdefrei aus, Stefan meldet sich selbst (28.9.) · keine Abbruchregeln in Pläne · Randnotiz: Halswirbelfraktur 28.6. ausgeheilt, Wade (MTSS-Verdacht 8/2026) wieder okay |
| **FTP** | **300W** (Baseline 1.10.2026, XCadey · 10min geschätzt) · 3,21 W/kg · **93,6 kg** (Ø 30d aus intervals.icu, Stand 20.9.) · Zonen trainingsleitend · Offset Tacx ÷ XCadey ≈ **1,0** · vorher 305W (4iiii) |
| **Events** | **aktuell keine geplant** · 2026 abgeschlossen: RadRace 120 ✅ (KW24) · Rosenheimer ⚠️ (KW26, Unfall) · Karlsfelder Seelauf ✅ (KW38, 1:05:08) |
| **Aktuelle KW** | KW40 (28. September – 4. Oktober 2026) · 🔬 FTP-Baseline Do 1.10. ✅ **300W** (3min 441W) · Mo nur morgens · **Sa Abflug London 16:00** (1h Rad vormittags) |
| **Aktuelle Phase** | Nullpunkt · Test-Taper Mo–Mi (Easy-Lauf, LIT 1h, Vorbelastung 3×1min) · Fr Ruhetag · KW39 Retro 🟢 (Kern 3/3, Kadenz Easy erstmals 166 spm) |
| **🎯 Saison** | **Winter 2026/27 · KW40–KW09** · Ziel: FTP **+8–12%** über KW40-Baseline · **10km sub-60** im Frühjahr 2027 · 9–10h/Woche · kein Zielrennen · Plan: `planung/periodisierung.md` |
| **Nächste Phase** | KW41 London-Laufwoche (Mo/Mi/Fr morgens, ~13 km, kein Rad) · So 11.10. LIT 2h · KW41–43 Volumen-Rampe + Kadenz-Projekt · ✈️ **London Sa 3.10. (ab 16:00) – Sa 10.10. (an MUC ~16:30)** |
| **Fixpunkte** | FTP-Baseline KW40 ✅ 300W · FTP + 5km KW01/27 · FTP + 10km-Benchmark KW09/27 · **Tests nur am Wochenende** |
| **CTL** | 27,1 (27.9.) · ATL 46,2 · TSB −19,0 · Readiness 95 🟢 (HRV 47, 7d-Ø 52, RP 54, Schlaf 7,9h) · Muster: Trainings-Ermüdung, keine Krank-Indikatoren |
| **🏁 Rennergebnis** | **1:05:08 / 6:31 pro km** (Uhr 66:00 / 10,1km) · Ø HF **183**, max 196 · RPE 8 · alter PR 1:11:28 → **−6:20** · Stefans Zielzeit war richtig, Coach-Ableitung (6:50) 20 sek/km zu konservativ |
| **Lauf-Schwellenwerte** | **Schwellenpace 6:28/km · LTHR 185** (aktualisiert 20.9. aus dem Wettkampf) · Zonen: Z1 7:25–8:40 · Z2 6:55–7:25 · Z3 6:10–6:40 · Z4 5:25–6:10 · ✅ in intervals.icu übernommen (Schwellentempo 6:28, Schwellen-HF 185, HFmax 205) |
| **⚠️ Referenzwerte** | Lauf 4.9. war Kreta/nüchtern/früh → **nicht als Tempo-Referenz nutzen**. Bedingungen immer miterfassen. |
| **🦵 Kadenz** | Gewohnt ~140 spm · **Rennen 20.9.: 154 spm @ 6:31 über 66min** (Training nach Gefühl: 160–163) → unter Stress driftet sie ~6 spm zurück · Arbeitsziel **165–170**, damit im Wettkampf 160 steht · Rückmeldung **nach Gefühl** (kein Metronom) · **wichtigstes Laufprojekt der nächsten 6–8 Wochen** |
| **💪 Kraft** | **2× Kraft A (Drücken) / B (Ziehen)**, je ~30–35min, Ziel **Oberkörper-Aufbau** (Stefan, 28.9.) + Läufer-Beinübungen · 2 KH bis 10 kg, Bänder, Klimmzugstange draußen · Programm: `athlete/profil.md` |
| **Wochenstruktur** | werktags **max. 90min** (Ausnahme 2h), vor oder nach der Arbeit · **Wochenende trägt die langen Einheiten** · Planung rollierend 1–2 Wochen im Voraus · Ruhetag unter der Woche · **3 Kern-Einheiten/Woche** (Rad-Qualität · Lauf-Qualität · 1 lange WE-Einheit, `🎯 Kern`) – Kern wird verschoben, der Rest ist flexibel |
| **Steuerung** | Easy-Cap **165 bpm** · ⚠️ Lauf-HF liegt 25–30 bpm über Rad – Easy-Run = 155–165 bpm, **nie unter 160 cappen** (Details `athlete/profil.md`) |

## Coaching-Skill

```
/coach "BRIEFING"
```

**Aufruf-Beispiele** (HRV/CTL/TSB werden automatisch via MCP abgerufen):
```
/coach KW42 planen
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
| `planung/periodisierung.md` | Aktueller Saisonplan **Winter 26/27 (KW40–KW09)** – wird nach KW09/2027 ersetzt | Skill (mit Zustimmung) |
| `planung/kw[N].md` | Aktuelle Wochenplanung | Skill |
| `planung/archiv/` | Abgeschlossene Wochen (Plan + Ist + Feedback) | Skill (nach Wochenabschluss) |
| `.claude/skills/coach/SKILL.md` | Coach-Skill (Kern) – lädt je nach Situation die Module in `modules/` (retro, checks, krank, ftp-test, event) | Manuell |
| `planung/workout_index.md` | Kompakter Workout-Index (55 Workouts) | Manuell |
| `coaching_science.md` | Wissenschaftliche Referenz (Rønnestad et al.) | Manuell |
| `COACHING_AKTE.md` | Änderungs-Log, Coach-Notizen, Retro-Einträge (neueste oben) | Skill |
| `COACH_MEMORY.md` | **Gelernte Regeln & Korrekturen des Coaches** – gilt lokal und in der Claude-App | Skill (bei jeder neuen Erkenntnis) |

## Live Dashboard

Das Coaching-Dashboard wird **automatisch** aus intervals.icu-Daten generiert — der Skill muss es **nicht manuell anfassen**.

| | |
|---|---|
| **URL** | https://hallo-jpg.github.io/coaching-dashboard/ (Passwort-geschützt) |
| **Rebuild** | alle 30 min via GitHub Actions, bei Push auf `planung/`, `athlete/`, Generator + manuell triggerbar |
| **Generator** | `generate.py` + `dashboard.template.html` → `docs/dashboard.html` |
| **Datenquellen** | intervals.icu API: Wellness, Activities, Power-Curves, Pace-Curves, Wochenplan aus `planung/kw[N].md` |

**Karten im Dashboard (alle auto-generiert):**
- Recovery-Ring (Readiness Score), Trainingsform-Ring (CTL/ATL/TSB), Wochenziel-Ring (TSS-Compliance)
- Wochenplan (aus `planung/kw[N].md` + intervals.icu Aktivitäten, Kern-Einheiten markiert)
- Polarisation 8 Wochen **Rad + Lauf** (Rad nach Watt, Lauf nach HF) + Zeitanteil Rad : Lauf gegen den Soll-Split
- **Lauf-Aufbau** 12 Wochen: km/Woche gegen die +10%-Grenze, längster Lauf gegen die 30-Tage-Regel
- **Pace bei HF 160** (6 Monate, je Easy-Lauf) – Fortschrittsmesser der Lauf-Aerobie
- Readiness-Card mit HRV/Schlaf/TSB/Puls-Balken + Sparkline
- Ausblick 4 Wochen (aus `planung/kw[N].md` bis kw[N+3].md) – rechts neben dem Wochenplan
- Power Bestwerte All-Time (Rad, 11 Dauern)
- Lauf Bestwerte All-Time (Tempokurven, 7 Distanzen)

## Wichtige Regeln

- **`COACH_MEMORY.md` vor jeder Coaching-Antwort lesen und befolgen.** Neue Korrekturen oder Erkenntnisse aus einer Session dort ergänzen (nicht nur im Chat bestätigen) – das ist die einzige Quelle, die alle Sessions teilen.

- **Vor jedem Commit an `planung/kw*.md`: `python3 validate_plans.py` ausführen.** Prüft alle Wochenpläne gegen den echten Dashboard-Parser. Tag-Spalte muss exakt `Mo`/`Di`/… sein – **kein Datum** (`Mo 7.9.` bricht den Parser lautlos, das Dashboard bleibt dann leer). Pflichtformat: 6 Spalten + `**Total**`-Zeile.

- Alle Workouts laufen auf **%FTP** → .zwo Dateien skalieren automatisch
- **FTP-Update** nur nach formalem Test (3+10min, **Tarmac mit XCadey auf der Rolle, kein ERG**, DURA + Tacx-App parallel). **Tests nur am Wochenende** (Stefan, 1.10.2026). FTP 300W seit dem Baseline-Test 1.10. (XCadey). Indoor-Training = Tacx-Leistung (Aeroad ohne PM) → Offset-Faktor ≈ 1,0, Tacx-Watt = XCadey-Watt.
- **Periodisierungsplan** nur mit Stefans Zustimmung ändern
- **Git: immer direkt auf `main` committen und pushen** – auch in Cloud-/Web-Sessions (Claude-App). Keine Session-Branches, keine PRs: das Dashboard baut aus `main`, alles andere ist für Stefan unsichtbar. Vor dem Push `git pull --rebase`.
- Lauf-Workouts: kein .zwo – werden per `workout_steps` (% Schwellenpace) in intervals.icu angelegt und synchronisieren auf die COROS Pace 3

- **Distanz-Intervalle (400er, 1000er) immer über `distance_m` anlegen**, nie in Minuten umrechnen — sonst misst die Uhr Zeit statt Meter. In intervals.icu heißt `m` **Minuten**: `- 400m` wird still zu 400 Minuten, Distanzen müssen als `0.4km` geschrieben werden. Freitext in der Description nie mit `- ` beginnen (wird als Schritt geparst) — `·` benutzen. Details + Gegenprobe: Coach-Skill, Abschnitt Lauf-Workouts.
- HIT/VO2max ist **kein Neuland** – Stefan hat Ötztaler 2025 absolviert
