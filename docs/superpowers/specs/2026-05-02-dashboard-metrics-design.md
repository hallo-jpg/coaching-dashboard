# Dashboard-Metriken: Monotony, Ramprate, PMC Forward View (M1 · M2 · D1)

**Datum:** 2026-05-02  
**Status:** Approved

## Problem

Drei aussagekräftige Metriken fehlen im Dashboard:

1. **M1** – Training Monotony + Strain: Übertrainingsrisiko durch gleichförmiges Training ist unsichtbar
2. **M2** – ATL Ramprate: Zu schnell ansteigende Trainingslast (>7–8 ATL-Punkte/Woche) wird nicht angezeigt
3. **D1** – PMC Forward View: CTL-Kurve endet bei heute — die Projektion bis Renntag fehlt

## Ziel

Drei neue Anzeigeelemente in `generate.py` + `dashboard.template.html`. Alle basieren auf existierenden Daten (intervals.icu Wellness + geplante TSS aus `planung/kw[N].md` Dateien).

---

## M1: Training Monotony + Strain

### Datenbasis

Aus `get_wellness_range` der letzten 7 Tage: tatsächliche TSS-Werte pro Tag (aus `icu_training_load` der Aktivitäten, nicht aus Wellness — robuster).

Alternative falls Aktivitätsdaten nicht tagesgenau: TSS aus `get_weekly_review`.

### Berechnung in `generate.py`

```python
def calc_monotony_strain(daily_tss: list[float]) -> dict:
    # daily_tss: Liste mit 7 Werten (Mo–So), 0 für Ruhetage
    mean_tss = statistics.mean(daily_tss)
    stdev_tss = statistics.stdev(daily_tss) if len(set(daily_tss)) > 1 else 0.01
    monotony = round(mean_tss / stdev_tss, 2) if stdev_tss > 0 else 0
    strain = round(sum(daily_tss) * monotony, 0)
    return {"monotony": monotony, "strain": int(strain)}
```

### Ampel-Logik

| Monotony | Status | Farbe |
|---|---|---|
| < 1.5 | Gut variiert | 🟢 grün |
| 1.5 – 2.0 | Erhöhte Gleichförmigkeit | 🟡 gelb |
| > 2.0 | Übertrainingsrisiko | 🔴 rot |

| Strain | Status |
|---|---|
| < 500 | Niedrig |
| 500 – 800 | Moderat |
| > 800 | Hoch |

### Dashboard-Darstellung

**Neue Mini-Karte "Load Quality"** — wird nach der Trainingsform-Ring-Karte eingefügt.

```
┌─────────────────────┐
│  Load Quality       │
│                     │
│  Monotony  1.4  🟡  │
│  Strain    620      │
│                     │
│  ── letzte 7 Tage ──│
│  Mo Di Mi Do Fr Sa So│
│  ▓▓ ▓▓▓ ░ ▓▓ ░ ▓▓▓ ▓▓│ (Balken-Sparkline)
└─────────────────────┘
```

Tooltip bei Hover auf Monotony: "Wochenmittel / Standardabweichung TSS. <1.5 = gut variiert."

---

## M2: ATL Ramprate

### Datenbasis

Aus `get_current_fitness`: ATL-Wert heute + ATL-Wert vor 7 Tagen → `ramprate = atl_heute - atl_7d_ago`

### Berechnung

```python
def calc_ramprate(fitness_history: list[dict]) -> float:
    # fitness_history: Liste von {date, ctl, atl, tsb} — nach Datum sortiert
    if len(fitness_history) < 8:
        return 0.0
    atl_today = fitness_history[-1]["atl"]
    atl_7d = fitness_history[-8]["atl"]
    return round(atl_today - atl_7d, 1)
```

### Ampel-Logik

| Ramprate | Status | Farbe |
|---|---|---|
| < 5 | Moderat | ⚪ grau |
| 5 – 7 | Normal | 🟢 grün |
| 7 – 10 | Erhöht | 🟡 gelb |
| > 10 | Zu schnell | 🔴 rot |
| < −5 | Starker Rückgang (Taper/Krank) | 🔵 blau |

### Dashboard-Darstellung

**In der bestehenden Readiness-Card** als neue Zeile unter TSB:

```
ATL Δ7d   +9.2  ⚠️
```

Format: `ATL Δ7d  [±X.X]  [Ampel-Icon]`

Bei Ramprate im grünen Bereich: kein Icon (nur der Wert).

---

## D1: PMC Forward View – CTL-Projektion bis Renntag

### Datenbasis

- **Vergangene Fitness**: `get_current_fitness` → aktueller CTL, ATL, TSB
- **Geplante TSS**: Aus `planung/kw[N].md` bis `planung/kw24.md` — Total-Zeile aus Markdown parsen
- **Renntermin**: Aus `athlete/profil.md` oder hardcoded aus CLAUDE.md als Fallback

### Berechnung in `generate.py`

```python
def project_pmc(ctl_today: float, atl_today: float,
                planned_weekly_tss: list[tuple[date, float]],
                race_date: date) -> dict:
    # planned_weekly_tss: [(kw_monday_date, total_tss), ...]
    # Banister decay constants: CTL τ=42d, ATL τ=7d
    ctl = ctl_today
    atl = atl_today
    
    # Build day→TSS map (distribute weekly TSS evenly across 7 days)
    daily_tss_map: dict[str, float] = {}
    for (week_start, total_tss) in planned_weekly_tss:
        daily_avg = total_tss / 7
        for d in range(7):
            daily_tss_map[(week_start + timedelta(days=d)).isoformat()] = daily_avg
    
    # Iterate day by day from tomorrow until race_date (today already in ctl_today)
    current = date.today() + timedelta(days=1)
    while current <= race_date:
        daily_tss = daily_tss_map.get(current.isoformat(), 0)
        ctl = ctl * (1 - 1/42) + daily_tss / 42
        atl = atl * (1 - 1/7) + daily_tss / 7
        current += timedelta(days=1)
    
    tsb_race = round(ctl - atl, 1)
    return {
        "ctl_race": round(ctl, 1),
        "atl_race": round(atl, 1),
        "tsb_race": tsb_race,
        "race_date": race_date.isoformat(),
        "tsb_status": "on_track" if 5 <= tsb_race <= 25 else ("too_fresh" if tsb_race > 25 else "too_tired"),
    }
```

### Darstellung

**Neue Karte "Rennprognose KW24"** — unterhalb der bestehenden CTL/ATL/TSB-Karte.

```
┌─────────────────────────────────────────┐
│  Rennprognose  🏁 RadRace KW24          │
│                                         │
│  CTL Renntag    ~72.4                   │
│  TSB Renntag   +11.2  ✅ auf Kurs       │
│  (Ziel: TSB +5 bis +25)                 │
│                                         │
│  Basis: Plan KW19–23 wie vorgesehen     │
│  ─────────────────────────────────────  │
│  ↗ CTL                                  │
│  ···· Plan  —— Ist                      │
│  [Mini-Linienchart: CTL Ist + Projektion│
│   bis Renntag, mit Taper-Knick]         │
└─────────────────────────────────────────┘
```

**TSB-Status-Texte:**
- `✅ auf Kurs` wenn TSB +5 bis +25
- `⚠️ zu wenig getapert` wenn TSB < +5
- `⚠️ zu frisch — Taper zu lang` wenn TSB > +25
- `❌ kein Plan bis KW24 verfügbar` wenn nicht genug kw-Dateien vorhanden (Fallback: kein Block)

### Plan-TSS Parsing

In `generate.py` neue Funktion `parse_planned_tss_from_kw_files()`:
- Liest `planung/kw[N].md` für N = aktuelle KW bis KW24
- Extrahiert `**Total**`-Zeile aus Markdown-Tabelle → `~XXX` Wert
- Gibt Liste von `(montag_datum, tss_float)` zurück

---

## Technische Änderungen

### `generate.py`

1. Import `statistics` (stdlib) hinzufügen
2. Neue Funktion `calc_monotony_strain(daily_tss: list[float]) -> dict`
3. Neue Funktion `calc_ramprate(fitness_history: list[dict]) -> float`
4. Neue Funktion `parse_planned_tss_from_kw_files(current_kw: int, race_kw: int) -> list`
5. Neue Funktion `project_pmc(ctl, atl, planned_tss, race_date) -> dict`
6. In `generate_dashboard()`:
   - M1: Aktivitätsdaten der letzten 7 Tage zu Tages-TSS aggregieren → `calc_monotony_strain()` aufrufen
   - M2: Aus Fitness-History `calc_ramprate()` aufrufen
   - D1: `parse_planned_tss_from_kw_files()` + `project_pmc()` aufrufen
   - Alle Werte in Template-Context übergeben

### `dashboard.template.html`

1. **Load Quality Karte** (M1): neue Card-Sektion nach Trainingsform-Ring
2. **ATL Δ7d Zeile** (M2): in bestehende Readiness-Card einfügen
3. **Rennprognose Karte** (D1): neue Card-Sektion nach CTL/ATL/TSB-Karte

### Tests `tests/test_generate.py`

- `test_calc_monotony_strain_varied()` — variierte Woche → Monotony < 1.5
- `test_calc_monotony_strain_uniform()` — gleichförmige Woche → Monotony hoch
- `test_calc_ramprate_normal()` — normaler Anstieg
- `test_calc_ramprate_alert()` — Anstieg > 7 → korrekte Ampel
- `test_project_pmc_on_track()` — TSB im Zielbereich
- `test_parse_planned_tss_from_kw_files()` — Markdown-Parsing

---

## Nicht in Scope

- Separate CP/W' Dashboard-Visualisierung (folgt nach W1-Implementierung)
- Historische Monotony-Daten über mehrere Wochen
- Zweiter Renntermin (KW26 Rosenheimer) — Karte zeigt nur primäres Ziel (KW24); kann später ergänzt werden
- Änderungen am `/coach`-Skill (gehört zu Sub-Projekt C)
