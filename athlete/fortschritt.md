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
| 04.04.2026 | **305W** | **3,47** | **88 kg** | **Sentiero metabolisches Modell** | **Aktiver Referenzwert** |

## Historischer Vergleich

| | Früher | Jetzt | Δ |
|---|---|---|---|
| FTP absolut | 324W | 305W | −19W (−5,9%) |
| Gewicht | 97 kg | 93–94 kg | −3,5 kg (−3,6%) |
| W/kg | 3,34 | 3,26 | −0,08 (−2,4%) |

*Gewichtsverlauf: 97 kg (2023) → 91 kg (1.6.2026, Tiefstwert) → **93–94 kg (20.9.2026)**. Die Pause nach dem Unfall am 28.6. und das reduzierte Volumen im Sommer erklären den Wiederanstieg. Relevanz: beim Laufen wird jedes Kilo bei jedem Schritt getragen (~200 ml O₂/kg/km), auf dem flachen Rad zählen absolute Watt — Gewicht wirkt sich beim Laufen deutlich stärker aus.*

## VO2max-Verlauf

| Datum | VO2max | Quelle | Notiz |
|---|---|---|---|
| 29.03.2026 | 44 | COROS (unzuverlässig) | Projektstart |
| 04.04.2026 | **59 ml/min/kg** | **Sentiero** | Metabolisches Profil – realistischer Wert |

## Lauf-Entwicklung

| Datum | Schwellenpace | 5km Prognose | Notiz |
|---|---|---|---|
| 29.03.2026 | 6:03/km | 29:11 | Projektstart – Schätzwert, nie durch einen Wettkampf belegt |
| 20.09.2026 | **6:28/km** | ~31:15 | 🏁 10km-Wettkampf 6:31/km @ Ø HF 183 (66min) → Schwellenpace 6:03 → **6:28**, LTHR 179 → **185** (TrainingPeaks-Erkennung, von Stefan freigegeben). Zonen in `profil.md`, `generate.py` und Coach-Skill umgestellt. Offen: gleiche Werte in intervals.icu hinterlegen |

## Nächster FTP-Test

**Testfenster:** KW40 (28. Sep – 4. Okt 2026) – Herbsttest, von KW39 verschoben (≥11 Tage Abstand zum Seelauf). **Erster Test am neuen Setup** (Tarmac SL8 / XCadey) – FTP 305W stammt noch vom 4iiii.
**Methode:** 3+10min Protokoll, outdoor, 4iiii Referenz
**Hinweis:** KW21-Test gestrichen (03.05.2026) – Krankheit KW16 hat Trainingsgrundlage zu stark reduziert, Fokus auf Aufbau bis KW21

---

## Power-PR-Referenz (3/10/20min)

*Referenzwerte für PR-Erkennung im Coach-Skill. Wird automatisch aktualisiert wenn ein neuer PR erkannt und bestätigt wird.*

| Dauer | Bestwert (W) | Datum | FTP-Proxy | Notiz |
|---|---|---|---|---|
| 3min | 461W | 04.04.2026 | – (anaerob, kein FTP-Proxy) | Feldtest KW14 · W'-Signal |
| 10min | 352W | 04.04.2026 | ×0,90 → 317W | Feldtest KW14 (Sentiero-Protokoll) |
| 20min | 341W | 21.04.2025 | ×0,95 → 324W | All-Time aus intervals.icu Power-Kurve · Saison 2025 |

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
| 04.04.2026 | **305W** | **28,1 kJ** | 461W | 352W | 305W (Sentiero) |

*CP = (352×600 − 461×180) / 420 = 305W · W' = (461−305) × 180 = 28.080 J*
*Nächster Eintrag nach KW39 Herbst-Test.*
