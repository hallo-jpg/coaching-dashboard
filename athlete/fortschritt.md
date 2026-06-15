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
| Gewicht | 97 kg | 91 kg | −6 kg (−6,2%) |
| W/kg | 3,34 | 3,35 | +0,01 (+0,3%) |

## VO2max-Verlauf

| Datum | VO2max | Quelle | Notiz |
|---|---|---|---|
| 29.03.2026 | 44 | COROS (unzuverlässig) | Projektstart |
| 04.04.2026 | **59 ml/min/kg** | **Sentiero** | Metabolisches Profil – realistischer Wert |

## Lauf-Entwicklung

| Datum | Schwellenpace | 5km Prognose | Notiz |
|---|---|---|---|
| 29.03.2026 | 6:03/km | 29:11 | Projektstart |

## Nächster FTP-Test

**Testfenster:** KW39 (21.–27. Sep 2026) – Herbsttest nach Sommerpause + Herbstaufbau
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
| 10 km | 1:11:28 | 7:09/km | 18.03.2026 | All-Time aus intervals.icu |

**Kontext:** 5km-Pace 6:09/km liegt über der Schwellenpace (6:03/km) — typisch für Trainingsläufe ohne Wettkampf-Effort. Echtes 5km-Rennen würde deutlich schneller sein.

---

## CP/W'-Verlauf

*Wird automatisch nach jedem FTP-Test (Sentiero 3+10min) vom /coach-Skill aktualisiert.*
*Berechnung: CP = (P₂×t₂ − P₁×t₁)/(t₂−t₁), W' = (P₁−P₂)×t₁×t₂/(t₂−t₁)*

| Datum | CP [W] | W' [kJ] | 3min-Avg [W] | 10min-Avg [W] | FTP [W] |
|---|---|---|---|---|---|
| 04.04.2026 | **305W** | **28,1 kJ** | 461W | 352W | 305W (Sentiero) |

*CP = (352×600 − 461×180) / 420 = 305W · W' = (461−305) × 180 = 28.080 J*
*Nächster Eintrag nach KW39 Herbst-Test.*
