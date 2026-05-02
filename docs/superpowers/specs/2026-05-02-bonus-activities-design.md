# Bonus-Aktivitäten im Wochenplan

**Datum:** 2026-05-02  
**Status:** Approved

## Problem

Der Wochenplan im Dashboard zeigt pro Tag nur die erste aufgezeichnete Aktivität. Nicht geplante Aktivitäten (z.B. Wandern an einem Ruhetag, oder Wandern morgens + Radfahren nachmittags) werden ignoriert oder falsch zugeordnet.

## Ziel

Alle aufgezeichneten Aktivitäten einer Woche erscheinen im Wochenplan. Nicht geplante Aktivitäten werden dezent als "Bonus" kenntlich gemacht.

## Design

### Darstellungsregeln

| Fall | Linke Seite | TSS-Spalte (rechts) |
|---|---|---|
| Trainingstag, nur geplante Aktivität ✅ | Workout-Name | `✅ 88 TSS` |
| Trainingstag + Bonus-Aktivität | Workout · dashed-Separator · `+ 🥾 Wandern` | `✅ 120 TSS` / klein: `88 + 32` |
| Ruhetag + Aktivität | ~~Ruhetag~~ · `+ 🥾 Wandern` | `+32 TSS` (orange) |
| Ruhetag ohne Aktivität | Ruhetag (grau) | `–` |

- Bonus-Badge: kleines orangenes `+`-Label (wie im Mockup)  
- Split-Anzeige: Gesamt-TSS prominent (grün, ✅), darunter `88 + 32` in klein (grau + orange)  
- Ruhetag mit Aktivität: "Ruhetag" durchgestrichen, Aktivität darunter, nur `+XX TSS` in Orange  
- TSS-Compliance-Ring: keine Änderung nötig, zählt bereits alle TSS korrekt

### Sport-Typ-Matching

Primäre Aktivität = diejenige, deren Typ zum Plan passt:

| Plan-Flag | Erwarteter Typ | intervals.icu Types |
|---|---|---|
| `is_run = True` | `run` | Run, TrailRun |
| `is_kraft = True` | `strength` | WeightTraining, Workout |
| sonst (Standard) | `ride` | Ride, VirtualRide, GravelRide |

**Matching-Logik pro Tag:**
1. Alle Aktivitäten des Tages nach `start_date_local` sortieren (zeitlich)
2. Erste Aktivität, deren Sporttyp zum Plan-Typ passt → **primär** (Name + TSS für Plan-Spalte)
3. Alle anderen Aktivitäten des Tages → **Bonus** (Liste mit Name + TSS)
4. Ruhetag: alle Aktivitäten → Bonus (kein primärer Match)

Mehrere gleichartige Aktivitäten an einem Tag (z.B. zwei Rides) → erste = primär, zweite = Bonus. Zu selten für eigene Logik.

## Technische Änderungen

### 1. `match_activities()` in `generate.py`

Rückgabe-Struktur pro Tag von:
```python
{"tss_ist": 0, "done": False, "activity_name": ""}
```
auf:
```python
{
  "primary": None,         # {name, tss, type} oder None
  "bonus": [],             # [{name, tss, type}, ...]
  "tss_ist": 0,            # Summe aller TSS
  "done": False,
}
```

`done = True` sobald mindestens eine Aktivität vorhanden (auch an Ruhetagen).

### 2. `build_day_rows()` in `generate.py`

Neue Felder im Row-Dict:
```python
{
  ...bestehende Felder...,
  "activity_name":   str,   # Name der primären Aktivität (für Kompatibilität)
  "bonus_activities": [],   # [{name, tss}, ...]
  "tss_primary":     int,   # TSS der primären Aktivität
  "tss_bonus":       int,   # Summe Bonus-TSS
}
```

### 3. `dashboard.template.html`

**Trainingstag mit Bonus:**
```
🚴 Workout-Name
── dashed separator ──
[+] 🥾 Wandern          ✅ 120 TSS
                            88 + 32
```

**Ruhetag mit Aktivität:**
```
~~Ruhetag~~
[+] 🥾 Wandern          +32 TSS
```

Der Dot-Typ bleibt unverändert (rest = leerer Kreis, ride = blau, etc.) – der Dot gibt den Plan wieder, nicht die Realität.

## Nicht in Scope

- Aktivitäten außerhalb der aktuellen Woche
- Emoji-Mapping für alle Sportarten (Wandern = 🥾 wird aus dem Aktivitätsnamen übernommen, kein automatisches Mapping)
- Änderungen am Ausblick (4-Wochen-Karte) oder anderen Dashboard-Karten
