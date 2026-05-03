# TSS-Übersicht · 8 Wochen – Erweiterung (Plan vs. Ist + Phasen + Compliance)

**Datum:** 2026-05-03  
**Status:** Approved

## Problem

Die Kachel "TSS-Übersicht · 8 Wochen" zeigt auf Desktop nur Balken-Chart + 3 Mini-Stats (Ø, Höchste, Niedrigste). Visuell zu leer — es fehlen:
1. Sichtbarkeit: Habe ich meinen Plan eingehalten?
2. Kontext: In welcher Trainingsphase liegt jede Woche?
3. Zusammenfassung: Wie gut war meine Plan-Compliance insgesamt?

## Ziel

Variante 2 umsetzen (im Brainstorming visuell bestätigt):
- **Plan-Umriss-Balken** hinter jedem Ist-Balken
- **Phasen-Labels** unter den Balken
- **Compliance-Balken** (Progress-Bar)
- **4. Stat** ersetzt "Niedrigste" → "Nächste KW Plan"

---

## Design

### Balken-Struktur (Template)

Neue HTML-Struktur pro Wochenspalte — saubere Baseline durch separaten `.barea`-Container:

```html
<div class="bw">
  <div class="bval">480</div>         <!-- Wert-Label oben -->
  <div class="barea">                 <!-- Balken-Bereich, flex:1 -->
    <div class="plan-outline" style="height:56%"></div>   <!-- Plan, absolut vom Boden -->
    <div class="bar-ist" style="height:52%;background:var(--green)"></div>  <!-- Ist, normal -->
  </div>
  <div class="bkw">KW11</div>         <!-- KW-Label -->
  <div class="bphase">Base</div>      <!-- Phasen-Label -->
</div>
```

**Positionierung Plan-Umriss:**
- `position: absolute; bottom: 0; left: 0; width: 100%`
- `border: 1.5px solid rgba(148,163,184,0.35); background: transparent`
- Zukünftige Wochen: `border-style: dashed` statt `solid`
- `z-index: 0`, Ist-Balken `z-index: 1` → Ist liegt immer vorne

**Verhalten Ist > Plan:** Ist-Balken ragt über Plan-Umriss hinaus — visuell korrekt, keine Überlagerungsprobleme da Ist vorne liegt.

**Verhalten Ist = 0:** Nur Plan-Umriss sichtbar (kein Ist-Balken) → sofort erkennbar als Ausfall.

### Plan-Balken-Höhe

`plan_bar_height_pct` wird mit demselben `bar_scale` berechnet wie `bar_height_pct`:

```python
plan_bar_height_pct = min(int(tss_plan / bar_scale * 100), 100)
```

### Phasen-Labels

Quelle: bestehende `SEASON_PHASES`-Liste in `generate.py` (autoritativ, kein File-Parsing nötig).

Neue Kurzbezeichnungen via `PHASE_ABBREV`-Dict:

| SEASON_PHASES name | Kurzlabel |
|---|---|
| Baseline | Base |
| Urlaub | Urlaub |
| Grundlage | Base |
| HIT-Aufbau | HIT |
| TT-Spezifik | TT |
| Tapering | Taper |
| 🏁 RadRace | Race |
| Erholung | Erhol. |
| 🗺️ Rosen. | Race |

Farbe des Phasen-Labels:
- HIT → `#f97316` (orange)
- Taper / Race → `#60a5fa` (blau)
- TT → `#a78bfa` (lila)
- alle anderen → `#94a3b8` (grau)

### Compliance-Berechnung

```python
def calc_compliance(weeks: list[dict]) -> int:
    """% abgeschlossener Wochen mit Ist >= 75% des Plans."""
    completed = [w for w in weeks if not w["is_current"] and not w["is_future"] and w["tss_plan"] > 50]
    if not completed:
        return 0
    ok = sum(1 for w in completed if w["tss_ist"] >= 0.75 * w["tss_plan"])
    return round(ok / len(completed) * 100)
```

### Stats-Grid (4 Spalten)

Ersetzt das bisherige 3-Spalten-Grid. "Niedrigste" entfällt:

| Slot | Label | Wert | Farbe |
|---|---|---|---|
| 1 | Ø 8 Wochen | avg_tss | text |
| 2 | Höchste | max_tss | yellow |
| 3 | Compliance | compliance_pct % | green wenn ≥80%, yellow wenn 60–79%, red wenn <60% |
| 4 | KW[N+1] Plan | next_kw_plan | blue, "–" wenn 0 |

Kein separater Compliance-Balken (das wäre V3 — nicht in Scope).

### next_kw_plan

`next_kw_plan` = `tss_plan` der ersten Woche mit `is_future=True`.  
Falls kein Plan vorhanden: `0` → Stat zeigt "–".

### Legende

Unter dem Chart, einzeilig:
```
□ Plan  ■ Ist  ■ Base  ■ HIT  ■ Deload/Taper  ▶ lfd. Woche  - - geplant
```

---

## Technische Änderungen

### `generate.py`

1. Neues Dict `PHASE_ABBREV` (top-level Konstante) mit Kurzbezeichnungen
2. Neue Hilfsfunktion `_phase_for_kw(kw: int) -> tuple[str, str]` → `(kurzlabel, css_farbe)`
3. `get_tss_overview_history()` erweitern:
   - Pro Woche: `tss_plan`, `plan_bar_height_pct`, `phase_short`, `phase_color` hinzufügen
   - `tss_summary` erweitern: `compliance_pct` (int), `next_kw_plan` (int) hinzufügen
4. Keine neuen API-Calls nötig — alle Daten aus vorhandenen Quellen

### `dashboard.template.html`

1. Bestehende Bar-Struktur im TSS-Übersicht-Block ersetzen durch `.barea`-Ansatz
2. Plan-Umriss-Div innerhalb `.barea` einfügen
3. `.bphase`-Label unter `.bkw` hinzufügen
4. Legende-Zeile einfügen (zwischen Chart und Stats)
5. Stats-Grid von 3 auf 4 Spalten: Ø | Höchste | Compliance% | KW[N+1] Plan

### `tests/test_generate.py`

- `test_calc_compliance_full()` — alle Wochen auf Plan → 100%
- `test_calc_compliance_partial()` — 2 von 4 Wochen unter 75% → 50%
- `test_calc_compliance_no_plan()` — Wochen ohne Plan (tss_plan ≤ 50) werden ignoriert
- `test_phase_for_kw()` — KW18 → ("HIT", "#f97316"), KW23 → ("Taper", "#60a5fa")
- `test_tss_weeks_has_plan_fields()` — jede Woche hat `tss_plan`, `plan_bar_height_pct`, `phase_short`

---

## Nicht in Scope

- Historische Compliance über mehrere Monate
- Interaktive Tooltips (reines Static HTML)
- Separate Compliance-Karte
- Änderungen an `SEASON_PHASES` selbst
