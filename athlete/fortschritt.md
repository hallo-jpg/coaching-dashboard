# Fortschritts-Log

## FTP-Verlauf

| Datum | FTP | W/kg | Gewicht | Methode | Notiz |
|---|---|---|---|---|---|
| 01.11.2023 | 271W | – | – | intervals.icu/Strava | Historischer Wert |
| 19.02.2024 | 300W | – | – | intervals.icu/Strava | Historischer Wert |
| 18.09.2024 | 286W | – | – | intervals.icu/Strava | Historischer Wert |
| 18.12.2024 | 301W | – | – | intervals.icu/Strava | Historischer Wert |
| 04.05.2025 | 324W | – | – | intervals.icu/Strava | Historischer Wert |
| vor Projektstart | 324W | 3,34 | 97 kg | – | Historischer Wert |
| 29.03.2026 | 310W (geschätzt) | 3,48 | 89 kg | Schätzung | Projektstart |
| 04.04.2026 | 317W | 3,60 | 88 kg | 3+10min outdoor (Coggan 90%) | Feldtest, 10min Avg 352W |
| 04.04.2026 | 305W | 3,47 | 88 kg | Sentiero metabolisches Modell | 4iiii – historisch |
| **01.10.2026** | **300W** | **3,21** | **93,6 kg** | **3+10 Rolle/XCadey · 10min geschätzt** | **Aktiver Referenzwert** · Baseline Winter 26/27 · 3min 441W gemessen · 10min nach 2:01 @ 328W abgebrochen (mental, Arbeitstag) → Stefan: 333W wären drin gewesen → 333 × 0,90 = 300W · Ausnahme, kein vollwertiger Test |

## Historischer Vergleich

| | Früher | Jetzt | Δ |
|---|---|---|---|
| FTP absolut | 324W | 300W | −24W (−7,4%) |
| Gewicht | 97 kg | 93,6 kg | −3,4 kg (−3,5%) |
| W/kg | 3,34 | 3,21 | −0,13 (−3,9%) |

*Gewichtsverlauf: 97 kg (2023) → 91 kg (1.6.2026, Tiefstwert) → **93,6 kg (Ø 30 Tage, Stand 20.9.2026)**. Quelle ab jetzt: intervals.icu-Wellness, der Coach liest den Wert bei jedem Aufruf aus. Die Pause nach dem Unfall am 28.6. und das reduzierte Volumen im Sommer erklären den Wiederanstieg. Relevanz: beim Laufen wird jedes Kilo bei jedem Schritt getragen (~200 ml O₂/kg/km), auf dem flachen Rad zählen absolute Watt — Gewicht wirkt sich beim Laufen deutlich stärker aus.*

## VO2max-Verlauf

| Datum | VO2max | Quelle | Notiz |
|---|---|---|---|
| 29.03.2026 | 44 | COROS (unzuverlässig) | Projektstart |
| 04.04.2026 | **59 ml/min/kg** | **Sentiero** | Metabolisches Profil – realistischer Wert |

## Lauf-Entwicklung

| Datum | Schwellenpace | 5km Prognose | Notiz |
|---|---|---|---|
| 29.03.2026 | 6:03/km | 29:11 | Projektstart – Schätzwert, nie durch einen Wettkampf belegt |
| 20.09.2026 | **6:28/km** | ~31:15 | 🏁 10km-Wettkampf 6:31/km @ Ø HF 183 (66min) → Schwellenpace 6:03 → **6:28**, LTHR 179 → **185** (TrainingPeaks-Erkennung, von Stefan freigegeben). Zonen in `profil.md`, `generate.py` und Coach-Skill umgestellt. In intervals.icu übernommen (20.9.). |

## Nächster FTP-Test

**Testfenster:** KW01/27 (4.–10.1.2027) – FTP-Test #2 + 5km-Zeitfahren · **am Wochenende** (Stefan, 1.10.2026: keine Tests mehr an Arbeitstagen, mental zu zehrend).
**Methode:** Sentiero 3+10min · Tarmac mit XCadey auf der Rolle, kein ERG · XCadey → DURA (Tacx-App parallel nur noch optional, Offset ≈ 1,0 ist bestimmt)
**Baseline:** 300W (1.10.2026, 10min geschätzt) · Winterziel +8–12 % → **~325–335W** bis KW09/27

**KW40-Baseline (1.10.2026) – Details:** Warmfahr-Stufen XCadey 147/174/205/237W · 3min All-Out **441W** (30s-Abschnitte 448·445·431·437·435·451 – sehr gleichmäßig) · 10min abgebrochen nach 2:01 @ 328W (HF 180), max HF 199 · Offset Tacx ÷ XCadey: Stufen 1,03–1,05, 3min 1,01, 10-min-Versuch 0,99, Ausfahren 0,99 → **Faktor 1,0** · Tacx-Aufzeichnung in intervals.icu gelöscht (DURA bleibt).

---

## Power-PR-Referenz (3/10/20min)

*Referenzwerte für PR-Erkennung im Coach-Skill. Wird automatisch aktualisiert wenn ein neuer PR erkannt und bestätigt wird.*

| Dauer | Bestwert (W) | Datum | FTP-Proxy | Notiz |
|---|---|---|---|---|
| 3min | **441W** | 01.10.2026 | – (anaerob, kein FTP-Proxy) | Baseline KW40 · XCadey/Rolle |
| 10min | – | – | – | KW40 nicht gefahren (Abbruch nach 2:01 @ 328W) · erster XCadey-Wert kommt mit dem nächsten Test |
| 20min | – | – | – | noch kein XCadey-Wert |

*Historisch (4iiii, nicht mit XCadey vergleichbar): 3min 461W / 10min 352W (04.04.2026) · 20min 341W (21.04.2025).*

**Schwellenwert für Ankündigung:** >2% über Referenzwert → Coach meldet PR und fragt ob FTP angepasst werden soll.

**Update-Logik:**
- Bei "ja" (FTP übernehmen): Bestwert + FTP in `athlete/profil.md` aktualisiert
- Bei "nein": Bestwert wird trotzdem hier aktualisiert, FTP bleibt
- Bei "warten": Bestwert wird hier aktualisiert → kein erneuter Hinweis beim nächsten /coach

---

## Lauf-PR-Referenz (1,5km / 5km / 10km)

*Referenzwerte für Distanz-PR-Erkennung im Coach-Skill (Check C). Quelle: intervals.icu Pace-Kurve (All-Time).*
*Schwellenwert: >2% schneller → Coach meldet PR.*

| Distanz | Bestzeit | Pace | Datum | Notiz |
|---|---|---|---|---|
| 1,5 km | 8:10 | 5:27/km | 22.02.2026 | All-Time aus intervals.icu |
| 5 km | 30:46 | 6:09/km | 22.02.2026 | All-Time aus intervals.icu |
| 10 km | **1:05:08** | **6:31/km** | **20.09.2026** | 🏁 Karlsfelder Seelauf – erster echter 10km-Wettkampf · Uhr-Split (offizielle Zeit nachtragen) · vorher 1:11:28 (18.03., Trainingslauf) |

**Kontext:** 5km-Pace 6:09/km stammt aus einem Trainingslauf (22.02.) und blieb im Seelauf unerreicht — die ersten 5 km liefen planmäßig bei ~6:40. Der 10km-Wert ist jetzt der einzige Wettkampf-Datenpunkt und damit die belastbarste Referenz der Lauf-Leistungsfähigkeit.

---

## CP/W'-Verlauf

*Wird automatisch nach jedem FTP-Test (Sentiero 3+10min) vom /coach-Skill aktualisiert.*
*Berechnung: CP = (P₂×t₂ − P₁×t₁)/(t₂−t₁), W' = (P₁−P₂)×t₁×t₂/(t₂−t₁)*

| Datum | CP [W] | W' [kJ] | 3min-Avg [W] | 10min-Avg [W] | FTP [W] |
|---|---|---|---|---|---|
| 04.04.2026 | 305W | 28,1 kJ | 461W | 352W | 305W (Sentiero · 4iiii) |
| 01.10.2026 | **~287W** | **~27,8 kJ** | 441W | (333W geschätzt) | **300W** (XCadey · 10min geschätzt) |

*CP = (352×600 − 461×180) / 420 = 305W · W' = (461−305) × 180 = 28.080 J*
*1.10.2026: CP = (333×600 − 441×180) / 420 = 287W · W' = (441−333) × 180 × 600 / 420 = 27,8 kJ – rechnerisch, weil der 10min-Wert geschätzt ist. Nächster Eintrag nach KW01/27.*
