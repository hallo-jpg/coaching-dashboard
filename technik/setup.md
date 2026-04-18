# Technik & Setup

## Geräte & Verbindungen

| Gerät | Funktion | Protokoll | Verbunden mit |
|---|---|---|---|
| 4iiii Precision (Kurbel) | Powermeter – Referenz | ANT+ | Wahoo ELEMNT ROAM |
| Tacx Flux S | Smart Trainer Indoor | ANT+ FE-C | Wahoo (ERG-Steuerung) |
| Wahoo ELEMNT ROAM | Aufzeichnung + ERG-Steuerung | WiFi/BT | TrainingPeaks (auto) |
| COROS Uhr | Laufen + Schlaf + HRV | BT | COROS App |

## Datensync-Kette

```
Rad:   4iiii → Wahoo → TrainingPeaks (automatisch)
Lauf:  COROS → Strava → TrainingPeaks (automatisch)
```

## Indoor-Setup

1. Tacx per **ANT+ FE-C** mit Wahoo verbinden (nicht Bluetooth!)
2. 4iiii per ANT+ mit Wahoo verbinden
3. Wahoo steuert Tacx-Widerstand per ERG
4. 4iiii misst echte Watt → erscheint auf Wahoo-Display
5. Aufzeichnung läuft auf Wahoo → sync zu TrainingPeaks

**Wichtig:** Tacx per Bluetooth verbinden = kein ERG! Immer ANT+ nutzen.

## Powermeter-Vergleich (Test 31. März 2026)

| Zone | 4iiii (Referenz) | Tacx | Differenz |
|---|---|---|---|
| Z2 (<200W) | – | −7,7% | Tacx liest tiefer |
| Z3 (200–270W) | – | −8,4% | Größte Abweichung |
| Z4+ (>270W) | – | −3,3% | Konvergiert bei hoher Last |
| **Gesamt** | **Referenz** | **−5,5%** | Systematischer Offset |

→ Immer 4iiii als Messreferenz verwenden. Zonen basieren auf 4iiii-Werten.

## FTP in Geräten eintragen

| Gerät / Platform | Wo | Wert |
|---|---|---|
| TrainingPeaks | Einstellungen → Zonen → Cycling Power → FTP | **317W** |
| Wahoo ELEMNT App | Profil → FTP | **317W** |
| COROS App | Profil → Sport → Radfahren → FTP | **317W** |

## Zukunft: COROS DURA (optional, post RadRace)

Der COROS DURA würde TrainingPeaks vollständig ersetzen:
- Verbindet sich direkt mit Tacx Flux S per ANT+ FE-C (ERG)
- Liest 4iiii Kurbel-PM per ANT+
- Workouts direkt aus COROS App → kein TP mehr nötig
- Entscheidung nach RadRace Juni 2026
