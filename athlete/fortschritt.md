# Fortschritts-Log

## FTP-Verlauf

| Datum | FTP | W/kg | Gewicht | Methode | Notiz |
|---|---|---|---|---|---|
| vor Projektstart | 324W | 3,34 | 97 kg | – | Historischer Wert |
| 29.03.2026 | 310W (geschätzt) | 3,48 | 89 kg | Schätzung | Projektstart |
| 04.04.2026 | 317W | 3,60 | 88 kg | 3+10min outdoor (Coggan 90%) | Feldtest, 10min Avg 352W |
| 04.04.2026 | **305W** | **3,47** | **88 kg** | **Sentiero metabolisches Modell** | **Aktiver Referenzwert** |

## Historischer Vergleich

| | Früher | Jetzt | Δ |
|---|---|---|---|
| FTP absolut | 324W | 305W | −19W (−5,9%) |
| Gewicht | 97 kg | 88 kg | −9 kg (−9,3%) |
| W/kg | 3,34 | 3,47 | +0,13 (+3,9%) |

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

**Testfenster:** KW21 (18.–24. Mai 2026)
**Methode:** 3+10min Protokoll, outdoor, 4iiii Referenz
**Danach:** Sentiero-Eingabe für aktualisiertes metabolisches Profil

---

## Power-PR-Referenz (5/10/20min)

*Referenzwerte für PR-Erkennung im Coach-Skill. Wird automatisch aktualisiert wenn ein neuer PR erkannt und bestätigt wird.*

| Dauer | Bestwert (W) | Datum | FTP-Proxy (×0,90) | Notiz |
|---|---|---|---|---|
| 5min | – | – | – | Noch nicht erfasst |
| 10min | 352W | 04.04.2026 | 317W | Feldtest KW14 (Coggan) |
| 20min | – | – | – | Noch nicht erfasst |

**Schwellenwert für Ankündigung:** >2% über Referenzwert → Coach meldet PR und fragt ob FTP angepasst werden soll.

**Update-Logik:**
- Bei "ja" (FTP übernehmen): Bestwert + FTP in `athlete/profil.md` aktualisiert
- Bei "nein": Bestwert wird trotzdem hier aktualisiert, FTP bleibt
- Bei "warten": Bestwert wird hier aktualisiert → kein erneuter Hinweis beim nächsten /coach
