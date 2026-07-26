# Coaching-Akte – Logs & Notizen

*Letzte Aktualisierung: 26. Juli 2026*
*Athletenprofil → `athlete/profil.md` | Periodisierung → `planung/periodisierung.md`*

---

## 26. Juli 2026 – Wiedereinstieg nach Halswirbelfraktur · Lauf-Block KW31–38 gestartet

**Ausgangslage:** Radunfall 28.6.2026 beim Rosenheimer (nach 45,8km). Angebrochener Halswirbel. 4 Wochen komplette Pause (KW27–30). Ärztliche Freigabe für Laufen und Radfahren liegt vor. **Rad defekt → Trainingsfokus 100% Laufen.**

**Datenlage beim Wiedereinstieg:**
- CTL 45,7 (28.6.) → **24,1** (26.7.) = −21,6 Punkte / −47%
- Readiness 77 🟡 · TSB +20,4 · HRV 45ms · Ruhepuls 57 (+1,3) · Trend 7d fallend
- Referenzlauf Fr 24.7.: 29min / 3,7km / 7:50/km bei Ø166 bpm, max 181

### ⚠️ Korrektur am 26.7. (Einwand Stefan) – Laufzonen-HF war falsch

Erste Einschätzung war: „HF 166 bei 7:50/km = Detraining, Zonen-Soll wäre ~130 bpm, Cap 150." **Das war falsch.** Stefan hat widersprochen (HF <150 sei beim Laufen unerreichbar), die Aktivitätshistorie bestätigt ihn:

| Datum | Dauer | Pace | Ø HF | CTL |
|---|---|---|---|---|
| 05.03. | 64min | 7:32/km | 162 | 45,7 |
| 18.03. | 73min | 7:10/km | 156 | 46,1 |
| 29.04. | 35min | 7:27/km | 157 | 35,4 |
| 06.05. | 42min | 7:30/km | 163 | 40,2 |
| 20.05. | 45min | 7:30/km | 161 | 41,7 |
| 06.06. | 25min | 7:09/km | 155 | 46,5 |
| **24.07.** | **29min** | **7:50/km** | **166** | **25,3** |

Stefans Easy-Run-HF liegt saisonübergreifend bei **155–163 bpm** – auch bei voller Fitness (CTL 40–48). Der Lauf vom 24.7. liegt damit nur **3–5 bpm** über der Norm, bei 20 sek/km langsamerer Pace, in Julihitze, zweiter Lauf nach 4 Wochen Pause. **Kein Detraining-Signal.**

**Fehlerursache:** Die HF%-Spalte der Laufzonen in `profil.md` war von der **Rad**-HFmax (205) abgeleitet (Z1 = 60–72% = 123–148 bpm). Beim Laufen liegt Stefans HF systematisch 25–30 bpm höher als auf dem Rad bei gleicher Belastungsstufe. Derselbe Fehler wurde bereits in KW18 gemacht („HF 157 → leicht über Easy-Zone") und KW19 („Puls <148 bpm") – zweimal unkorrigiert geblieben.

**Behoben:** `profil.md` Laufzonen-Tabelle auf gemessene HF-Werte umgestellt + Warnhinweis + Belegtabelle hinterlegt. Regel: **nie einen Easy-Run-Cap unter 160 bpm vorgeben** – das erzwingt Gehen. Kein Detraining aus erhöhter Lauf-HF ableiten, ohne gegen die Belegtabelle zu prüfen.

**Was die Korrektur NICHT ändert:** CTL-Verlust 45,7 → 24,1 ist real (Volumen-/Gewebefrage). Blockdesign bleibt unverändert – es folgte aus der Riegel-Lücke (s.u.) und aus der Impact-Toleranz, nicht aus der HF-Zahl. Neuer Easy-Cap: **165 bpm**, Fortschrittsmesser „Pace bei HF 160" (Referenz 06.05.: 7:30/km @ 163).

**Pace-Kurven-Analyse (all-time, entscheidend für Blockdesign):**
| Distanz | Bestzeit | Pace |
|---|---|---|
| 1,5km | 8:10 | 5:27/km |
| 5km | 30:46 | 6:09/km |
| 10km | 1:11:28 | 7:09/km |

Riegel-Prognose 5km → 10km: **64:10**. Ist: 71:28. **Lücke 7:18.**
→ Limiter ist **aerobe Durability auf Renntempo**, nicht VO2max und nicht Grundschnelligkeit (1,5km→5km ist konsistent).
→ **Konsequenz für den Block:** Schwerpunkt Schwellen-/Renntempo-Volumen, nicht flache VO2max-Intervalle. Hügelläufe als VO2max-Ersatz (niedrigere Impact-Last bei 91kg, Gehpause bergab).

**Stefans Wünsche + Coach-Antwort:**
| Wunsch | Bewertung |
|---|---|
| "Viele Intervalle, schnell schneller werden" | ✅ Berechtigt (8 Wochen Vorlauf) – aber als Schwelle statt VO2max, weil das seine echte Lücke trifft. Strides ab Tag 1. |
| "Langsame Läufe orthopädisch teuer wegen geringer Pace" | ❌ Sachlich invers: Peak-Impact pro Schritt ist bei langsamem Tempo *niedriger*. Bei 91kg ist schnelles Laufen der teure Teil. Nielsen 2014: Risikotreiber ist Volumensprung, nicht Intensität. |
| "Grundlagenausdauer solide" | ⚠️ Teilweise: CTL-Verlust real (−47%), aber die HF-Antwort beim Laufen ist nahezu normal → aerob deutlich besser erhalten als zunächst angenommen |
| "Ersten Lauf nicht überinterpretieren" | ✅ **Richtig.** n=1, erste ungewohnte Belastung, Julihitze. Erst 3–4 Läufe abwarten, dann bewerten. |

**Blockstruktur (8 Wochen bis Karlsfelder Seelauf 20.9.):**
KW31 Reanimation (HF-Anker + Strides) · KW32 Tempo-Kalibrierung (2km-Check) · KW33–34 Schwellen-Block + Hügel · KW35 5km-TT + Peak 1 · KW36 Renntempo-Spezifik (3×2km) · KW37 Taper 1 (Volumen −40%, Intensität halten) · KW38 Rennwoche (Mujika 3 Touches)

**Steuerungsregel KW31–32:** Easy-Cap **165 bpm** (korrigiert, s.o.), Pace ergibt sich (erwartbar 7:45–8:15/km). Fortschrittsmesser: Pace bei HF 160. Die limitierende Größe in KW31 ist die Impact-Toleranz des Gewebes nach 4 Wochen ohne Laufbelastung, nicht die Herzfrequenz.

**Zielzeit:** sub-60min realistisch, sub-58 Stretch – **Neubewertung nach dem 2km-Tempo-Check in KW32**, vorher keine belastbare Prognose.

**Empfohlener Zusatzhebel:** 1–2×/Woche Cross-Training (Spinning-Bike / Crosstrainer / Aqua-Jogging, Z1–Z2). Baut CTL ohne Impact – der einzige Weg, Stefans Orthopädie-Bedenken und den Grundlagenbedarf gleichzeitig zu bedienen, solange das Rad defekt ist.

**Dateien:** kw30.md + kw31.md (voll) + kw32–34.md (Stubs) angelegt · kw26–29 archiviert (kw26 mit Unfall-Retro, kw27–29 ❌ Verletzungspause) · periodisierung.md **noch nicht ersetzt – Zustimmung ausstehend**

### 🐞 Workout-Anlage: zwei Fehler, beide von Stefan entdeckt (26.7.)

**Fehler 1 – Strides verschwanden lautlos.** `6×(20s @ 120% + 100s @ 55%)` als `workout_steps` gesendet. Der MCP-Server rendert Dauern nur in ganzen Minuten → `20s` wurde `0m` → intervals.icu verwarf die Schritte. Übrig blieben nur die auf 2min aufgerundeten Gehpausen bei 55% Pace = **11:00/km**. Ergebnis in der App: lauter identische langsame 2-Minuten-Stufen, null Intensität. Die MCP-Erfolgsmeldung „✅ Struktur: 15 Schritte" zählte die *gesendeten*, nicht die *gespeicherten* Schritte — deshalb unbemerkt geblieben.

**Fehler 2 – Name ≠ Dauer.** Ein-/Auslaufen (je 5min) wurde *zusätzlich* zur genannten Dauer angelegt: „Easy 28min" hatte 33min Gesamtzeit.

**Behoben:** Alle 5 Einheiten neu angelegt. Struktur jetzt 3 Schritte (Einlaufen / Easy / Auslaufen), Gesamtdauer = genannte Dauer. Strides als Klartext in der `description`. Pace-Bänder: Einlaufen 65–73% (9:18–8:17/km), Hauptteil 70–80% (8:38–7:33/km), Auslaufen 62–70% (9:45–8:38/km). Gegen `get_planned_events` verifiziert.

**Regeln in `planung/workout_index.md` dokumentiert:** Pace-Konvention (höherer % = schneller, `Pace = 363s / pct`), 1-Minuten-Mindestdauer, Pflicht zur Nachkontrolle via `get_planned_events`.

### Planänderung 26.7. – Intensität eine Woche vorgezogen (Stefans Einwand, angenommen)

Stefan: „So viele Easy Runs bringen mir gar nichts, wieso keine Intervalle?" — **berechtigt, Plan geändert.**

Begründung für die Änderung:
- 8 Wochen Vorlauf: zwei reine Easy-Wochen = 25% der verfügbaren Zeit
- Nielsen et al. 2014: Risikotreiber ist der **Volumensprung** (>30% über 2 Wochen), nicht die Intensität
- Die „erste 4 Wochen nur Easy"-Regel im Regelwerk gilt für **Laufeinstieg**, nicht für Rückkehr nach 4 Wochen Pause bei vorhandener Basis. Stefan lief 27.2. Schwellenintervalle (54min) und 1.4. 2×8min Schwelle (60min)
- Seine Lauf-HF-Antwort ist nahezu normal → aerob belastbar

**Geändert:** KW31 Do von „Easy 32min + Strides" auf **Tempo 3×6min** (HF 172–180, RPE 7, 18min Z3). Gesamter Block eine Woche nach vorn:

| KW | Qualität | Inhalt |
|---|---|---|
| 31 | 1× | Tempo 3×6min |
| 32 | 2× | Tempo 4×6min · 2km-Check (Kalibrierung) |
| 33 | 2× | Schwelle 2×10min · Hügel 6×90s |
| 34 | 2× | Schwelle 2×12min · Hügel 8×90s |
| 35 | 2× | 5km-TT · Qualität |
| 36 | 2× | 3×2km Renntempo · Qualität |
| 37–38 | Taper + Rennwoche | |

**Der Deal, explizit vereinbart:** Intensität ja — Volumen dafür streng nach Ramp (längster Lauf max. +10%/Woche, Gesamt max. +15%). Beides gleichzeitig zu steigern ist die Kombination, die zuverlässig verletzt.

**Warnstrukturen bei Tempoarbeit mit 91kg nach Impact-Pause:** Achillessehne, Schienbeinkante, Fußgewölbe. Stechender Schmerz → abbrechen, melden.

**Steuerung bis KW32-Check:** alle Qualitätseinheiten nach **HF (Z3 = 172–180 bpm) und RPE 7**, nicht nach Pace — die 6:03/km im Profil ist ein All-Time-Wert und aktuell nicht gültig.

---

## 21. Juni 2026 KW25 Retro
🟡 Mittel · TSS 179/95 (188% – ungeplante Sa-Fahrt) · HRV ↘ fallend (47→40ms) · Polarisation PI 97% ✅
→ Recovery-Woche: Mi LIT-1h perfekt (100% Z2), Fr LIT+Opener sauber (IF 0.63)
→ Sa ungeplante Fahrt 75 TSS (IF 0.76, 4min Z6/Z7) — Recovery-Plan gebrochen
→ kw25.md archiviert → planung/archiv/kw25.md

## 24. Juni 2026 – KW26 Taper-Korrektur (Mujika-Protokoll)
→ Do T-3 geändert: LIT-1h → LIT-1h + Openers (5×30s @ >120% FTP) · intervals.icu aktualisiert
→ Grund: Mujika & Padilla (2003/2004) — Intensitätserhalt im Taper ist kritischster Faktor. Bisheriger Plan hatte 5 Tage ohne Intensität bis T-1 Aktivierung → neuromuskuläre Stille
→ Protokoll-Update: coaching_science.md Sektion 6 + SKILL.md Rennwoche-Modus/Tapering/Taper-Checkliste — künftig 3 Intensity-Touches (T-5 Sharpening, T-3 Openers, T-1 Aktivierung) statt nur T-1

## 21. Juni 2026 – KW26 Rennwoche Rosenheimer
→ Rennwoche geplant: Mo Ruhe / Di LIT-1h / Mi Ruhe / Do LIT-1h+Openers / Fr Ruhe / Sa Aktivierun.zwo 1:30h / So 🏁 Rosenheimer · ~139 TSS
→ TSB-Prognose Renntag So 28.6.: ~+17 (Ziel: +10 bis +20) ✅
→ Carb-Loading: Mi 7g/kg (637g) → Do 8g/kg (728g) → Fr+Sa 10g/kg (910g)
→ Race Plan: Ø220W NP · IF 0.72 · 90–107g KH/h · Crux km118–167 (49km ohne Labe)

## 14. Juni 2026 – KW24 Retro + KW25 Planung (Sonderfall)

🟢 Gut (Rennwoche) · TSS 521 (Race-Vergleich n.a.) · HRV ↘ post-race (43→38ms) · TSB Peak +11.8 Do – Taper-Timing perfekt
→ 🏁 RR120 Prolog (Sa): Ø337W · ~342W NP · 20min · IF 1.12 · HF 192bpm (Max) · near All-Time 20min PR (341W, Apr 2025)
→ 🏁 Rad Race 120 (So): Ø248W · 272min · 129.2km · TSS 300 · RPE 9 · MaxHF 190bpm · vollständig finishiert
→ 💡 FTP-Signal: intervals.icu schätzt +17W → 322W (Basis: Prolog ~342W NP × 0.95 = 325W, konsistent). Kein formeller Sentiero-Test → kein Update. LTHR 192→188bpm angepasst.
→ Sonderfall aktiv: Rosenheimer (28.6.) ist 14 Tage weg → Mo–Di Pause · Mi–Sa LIT · So Easy Run · ~214 TSS geplant
→ kw24.md archiviert → planung/archiv/kw24.md

## 07. Juni 2026 – KW23 Retro + KW24 Rennwoche Planung
🔴 Schwach (Regelwerk) · TSS 214/207 (103%) · HRV ↘ stark fallend (61→28ms am letzten Tag) · Polarisation PI 95% ✅
→ Taper-Woche war perfekt: 6/6 Einheiten, LIT-Zonen exakt (IF 0.54–0.55), Aktivierung Do ideal dosiert (RPE 7)
→ 🚨 HRV-Alarm: 28ms (>2SD supprimiert) + Ruhepuls 66bpm (+11 über Basis) am letzten Tag → Krank-Risiko-Muster
→ KW24 geplant: Mo FULL REST (HRV-Alarm), Di HRV-abhängig LIT-1h, Mi LIT-1h, Do Pause/Packen, Fr Aktivierun.zwo+Anreise, Sa Zeitfahren, So Rennen
→ TSB-Prognose Zeitfahren Sa 13.6.: ~+5 (unter Idealziel +10–20) · Swing vs. TT-Sim 29.5.: +32.7 Pkt → ~+3.3% Leistungsbonus
→ Pacing TT: Ø 326–332W · Negativer Split 320→332→340W+ · W' 28.1kJ für Steilsektionen + Finish
→ kw23.md archiviert → planung/archiv/kw23.md

## 02. Juni 2026 – Neues Event: Karlsfelder Seelauf
→ Karlsfelder Seelauf 2026 eingetragen: 20.09.2026 (KW38) · 10km · Ziel: max. Pace / sub-60min
→ athlete/profil.md: Event-Kalender + Saisonziele aktualisiert (Taper-Start T-14 = 06.09.)
→ planung/langfristplan.md: Laufen-Abschnitt + Dual-Focus-Block Herbst beschrieben
→ FTP-Herbsttest verschoben: KW39 → KW40 (28. Sep–4. Okt) — KW39-Do wäre nur 4 Tage nach Rennen
→ Fokuspriorität bis Rosenheimer (28.6.): Rad bleibt Hauptfokus, Lauf wie bisher 2–4×/Woche

## 31. Mai 2026 – KW22 Retro + KW23 Planung
🟡 Mittel · TSS 602/499 (120,6%) · HRV → stabil (47→50ms) · Polarisation PI 57% ⚠️ Outdoor-LIT Mo zu intensiv
→ 3 starke Qualitätseinheiten (Over-Under 124 TSS, MIT_4x16 168 TSS, TT-Sim 1×25min 113 TSS)
→ Sa LIT ❌ ausgefallen · So Rad statt Lauf · TSB bei Taper-Start: −22.0
→ KW23 Tapering geplant: ~210 TSS · Do Taper-Aktivierung 3×4min@355W · 2× Easy Run Mo+Sa · TSB-Prognose Zeitfahren Sa 13.6.: ~0 bis +2
→ TSS-Ziel bewusst konservativ: Aus −22 sind +10 bis +20 in 13 Tagen unrealistisch ohne Fitness-Verlust. Subjektivwert 100/100 ist positives Signal.
→ kw22.md archiviert → planung/archiv/kw22.md

## 26. Mai 2026 – Ad-hoc KW22
→ Mi 27.5. Easy Run 35min gestrichen → Ruhetag/Spaziergang · TSS ~437 → ~412

---

## 25. Mai 2026 – KW21 Retro + KW22 Planung
🟡 Mittel · TSS 361/381 (94.8%) · HRV ↘ fallend (50→44ms, −6 Pkt) · Sa-Fahrt zu intensiv (Z3: 20% statt <15% für LIT)
→ KW22 TT-Spezifik geplant: Mo LIT-3h Outdoor (Feiertag, 90 TSS) / Di 6x4-4 Over-Under (90) / Mi Easy Run 35min / Do MIT_4x16 (95) / Fr MIT TT-Sim 1x22 (82) / Sa LIT-1h / So Easy Run 35min · ~437 TSS
→ 3 Qualitätseinheiten: Over-Under (Di), Schwellenausdauer (Do), TT-Rennsimulation (Fr als letzte Intensität vor Taper T-14)
→ Pfingstmontag = langer Outdoor-LIT, wichtig: <213W konsequent

---

## 17. Mai 2026 – KW20 Retro + KW21 Planung
🟢 Gut (geschätzt) · TSS ~304/304 (~100%) · intervals.icu MCP nicht verfügbar – Schätzung basiert auf Kontext (kein Hinweis auf ausgefallene Einheiten Mo–Do) · HRV-Suppression durch JGA (Alkohol Fr–So) — kein Trainings-Signal
→ KW21 geplant: Di HIT_EB_8x1 Glykolyse-Akt. (85 TSS, morgens) / Mi Easy Run 45min / Do HITdec_5x3 (105 TSS) / Sa LIT-3h outdoor (111 TSS) / So Easy Run optional · ~329 TSS
→ Dienstag-Constraint: nur morgens verfügbar → HIT_EB_8x1 (1:45h) passt ideal
→ Wochenende verlängert wegen schönem Wetter: Sa LIT-3h statt LIT-2h

---

## 10. Mai 2026 – KW19 Retro + KW20 Planung
🟡 Mittel · TSS 243/176 (138%, Überbelastung trotz Deload) · HRV ↘ stark fallend (51→35, −16 Pkt) · Polarisation PI 92% ✅
Läufe mit deutlich erhöhtem rTSS (46+53 statt 25+25): bei supprimierter HRV nach Österreich steigt Puls bei gleicher Pace → rTSS-Algorithmus rechnet das ein. LIT-Radeinheiten sauber gehalten.
→ KW20 als konservativer HIT-Einstieg: nur 4 Tage (Mo–Do), keine Läufe, Fr–So Ruhetag
→ KW20 Plan: Mo LIT-1h / Di HIT_EB 6×3 (88 TSS) / Mi LIT-2h / Do HIT_IE 3x10×30-30+SwSp (105 TSS) · ~304 TSS gesamt

---

## 07. Mai 2026 – Ad-hoc KW19
→ LIT-1h30 von Do auf Fr verschoben (war in intervals.icu bereits korrekt auf Fr, kw19.md angepasst)

---

## 06. Mai 2026 – Plankorrektur KW20/21
→ Sperrblock 15.–17.5. eingetragen (Fr–So, unterwegs, kein Rad/Lauf) → KW20 TSS-Vorschau ~412 → ~227
→ FTP-Test KW21 aus Stub entfernt (war bereits in langfristplan.md als gestrichen markiert 03.05.) → KW21 wird volle HIT-Woche ~329 TSS
→ KW21-Stub: Di HIT ~90, Do LC ~100, Sa/So LIT

---

## 03. Mai 2026 – KW18 Retro + KW19 Planung

🟡 Mittel · TSS 543/383 (142%) · HRV ↘ stark fallend (57→38, −19 Pkt) · Österreich-Woche mit Postalm Epic (274min, 231 TSS)
Grauzone-Problem: Z3 25% (Ziel <15%), PI 51%. Kein einziger echter LIT-Ride möglich im Berggelände.
→ KW19 als Deload-Woche geplant: ACWR 1.79 (>1.5), TSB −35.3 · nur LIT + Easy Runs · ~208 TSS (54% Soll)
→ FTP-Test KW21 gestrichen auf Stefan's Wunsch: Krankheitspause KW16 hat Basis reduziert, KW21 bleibt voller HIT-Block. Nächster Test: KW39 (Herbst).
→ HIT-Aufbaublock verschiebt sich effektiv auf KW20–21 als Kern-HIT-Wochen

---

## Änderungs- & Fehlen-Log

| Datum | Geplant | Durchgeführt | Grund | Auswirkung |
|---|---|---|---|---|
| KW14 | Normaler Trainingsstart | Konservative Woche | Erholung Mallorca + Lebensmittelvergiftung | FTP-Test auf Sa verschoben |
| KW15 | Grundlagenblock Start (~396 TSS Rad) | 2 Läufe (77 TSS) + So LIT-1h | Urlaub, nur 2 Läufe möglich (Do/Sa ausgefallen) | TSS Ist ~114, Grundlagenblock echter Start KW16 |
| KW16 | Grundlagenblock ~493 TSS | 0 TSS – komplett ausgefallen | Krank ab Mo 14. April | Grundlagenblock verschoben auf KW17. HIT-Aufbau KW18–21 bleibt vorerst unverändert. |

---

## Workout-Wunschliste

| Name | Beschreibung | Priorität | Status |
|---|---|---|---|
| FTP-Test 3+10min | ZWO für Outdoor-Test | – | ✅ Erstellt |

---

## Coach-Notizen

### 26. April 2026 – KW17 Retro + KW18 Planung

- KW17 Retro: 🟢 Gut · TSS 158/135 (117%) · HRV stabil (45→43) · Polarisation LIT 84% / Grauzone 17% / HIT 2%
- KW18 geplant: SwSp Di (indoor) · Easy Run Mi · LIT-1h Do · LIT-2h Fr outdoor AT · Berg-HIT 4×5min Sa · LIT-2h So · TSS ~389
- Austria-Urlaub Fr–So: Freiheit bei Sa-Extension, LIT konsequent <229W
- Zone-Mapping korrigiert: Sentiero Z0-Z6 = intervals.icu Z1-Z7 · LIT=icu Z1+Z2+Z3 · Grauzone=icu Z4 · HIT=icu Z5+Z6+Z7

### 24. April 2026 – KW17 Krankheitsverlängerung (Do + Fr)
- Krankheit dauert an – Do 23.4. und Fr 24.4. als ❌ Krank markiert
- Geplante intervals.icu-Workouts für Do/Fr gelöscht
- Sa/So bleiben im Plan – Entscheidung bei Rückkehr
- Dashboard-Logik verbessert: vergangene Tage ohne Aktivität werden automatisch als "Ausgefallen" angezeigt

### 21. April 2026 – KW17 Umplanung (Husten)
- Di 21.4. noch nicht fit: Husten, Plan um einen Tag verschoben
- Mi 22.4.: längerer Spaziergang · Do 23.4.: LIT-1h (+1) · Fr 24.4.: LIT-1h30 (+2)
- Sa/So bleiben unverändert: LIT-2h / LIT-2h30

### 20. April 2026 – KW17 Planung (Wiederanlauf)
- KW17 als konservative Rückkehrwoche geplant: Mo Ruhe · Di Spaziergang · Mi LIT-1h · Do LIT-1h30 · Fr Ruhe · Sa LIT-2h · So LIT-2h30
- TSS-Ziel: ~251 (kein Kompensations-TSS)
- Kein KA, kein SwSp, kein Laufen diese Woche – sauberer Neustart
- HIT-Aufbaublock KW18 bleibt wie geplant, Entscheidung über SwSp-Einstieg zu Beginn KW18

### 18. April 2026 – KW16 Krankheit

- KW16 komplett ausgefallen: krank ab Mo 14. April, 0 TSS
- Readiness-Verlauf KW16: Mo 86🟢 → Di 58🟡 → Mi 77🟡 → Do 90🟢 → Fr 86🟢
- Ruhepuls leicht erhöht (59 bpm, +0,5), TSB jetzt +27,7 (sehr frisch durch Trainingspause)
- Kein Krank-Risiko-Muster in intervals.icu – Erholung scheint in Gang
- Stefan meldet sich wenn Rückkehr möglich. Bis dahin: keine Workouts geplant.
- **Plan-Impact**: Grundlagenblock (ursprgl. KW16–17) reduziert auf 1 Woche (KW17). HIT-Aufbau KW18–21 vorerst unverändert – Entscheidung bei Rückkehr.
- **Rückkehrprotokoll**: Erster Tag nur LIT, kein Kompensations-TSS, Readiness ≥ 70 vor erster Belastung

### 12. April 2026 – KW15 Abschluss + KW16 Planung
- KW15 Ist: 2 Läufe (Mo 36 TSS + Mi 41 TSS) + So LIT-1h geplant = ~114 TSS
- CTL/ATL/TSB beim Planen: 45/31/+20 → sehr frisch, HRV normal, Schlaf exzellent
- RPE Schwellenlauf: 6–7 → gut, Luft nach oben
- KW16 geplant: volle Grundlagenwoche ~446 TSS, SwSp_3x10 + KA-Einstieg + Kraft A/B
- KW15 archiviert → planung/archiv/kw15.md

### 7. April 2026
- KW15 Urlaubswoche: nur Laufen, 3 Einheiten, ~165 TSS
- Lauf-Workouts neu erstellt (manuell in TP anlegen): Easy 45min, Easy 60min, Schwelle 2×8min
- FTP auf 305W (Sentiero) aktualisiert, alle Zonen neu gesetzt
- VO2max Sentiero: 59 ml/min/kg (COROS-Wert 44 unzuverlässig)
- Profil korrigiert: HIT/VO2max ist kein Neuland – Ötztaler 2025 absolviert
- System-Upgrade: CLAUDE.md, Split-Dateien, coaching_science.md, Briefing-Template

### 4. April 2026
- FTP-Test absolviert: 317W (Coggan) → 305W (Sentiero aktiv)
- Indoor-Setup bestätigt: Wahoo + Tacx Flux S via ANT+ FE-C
- Kraft-Programm A+B definiert (Start KW16)
- Lauf-Vorlage: 2×8min @ 97–100% Schwelle

### 29. März 2026
- Projektstart, 55 Workouts kategorisiert
- Starke Grundlagenbasis vom Winter
- KA und LC neu einführen ab KW16/18
