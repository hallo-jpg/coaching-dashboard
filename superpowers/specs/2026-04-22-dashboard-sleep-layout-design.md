# Dashboard-Erweiterung: Schlaf-Chart + Layout-Umbau

*Erstellt: 2026-04-22*

## Ziel

Zwei unabhängige Änderungen am Coaching-Dashboard:

1. **Neues Widget:** Schlaf-Verlauf der letzten 30 Tage (Linienchart)
2. **Layout-Umbau:** Reihenfolge und Spaltenstruktur der Karten anpassen

---

## 1. Schlaf-Chart Widget

### Datenquelle

- `get_wellness_range()` MCP-Tool, letzte 30 Tage
- Feld: `sleepSecs` (Sekunden → in Stunden umrechnen: ÷ 3600)
- Fallback: fehlende Tage werden übersprungen (kein 0-Wert eintragen)

### Neue Funktion in `generate.py`

Neue Funktion `get_sleep_history(days=30)` nach dem Muster von `get_ctl_history(weeks=26)`:

```python
def get_sleep_history(days=30):
    # wellness_range für letzte 30 Tage abrufen
    # sleepSecs -> Stunden umrechnen
    # SVG path + fill_path berechnen (Y-Achse: 0h unten, 10h oben)
    # Rückgabe: {
    #   path: str,           # SVG <path d="..."> für Linie
    #   fill_path: str,      # SVG <path d="..."> für Füllfläche
    #   sleep_today: float,  # Heutiger Schlaf in Stunden (None wenn fehlt)
    #   avg_30d: float,      # 30-Tage-Durchschnitt in Stunden
    #   day_labels: list,    # Labels für X-Achse (z.B. ["25. Mär", "1. Apr", ...])
    # }
```

### SVG-Gestaltung

- **Farbe:** `#7986cb` (identisch mit Readiness-Karte, lila/indigo)
- **Gradient-Fill:** `rgba(121,134,203,0.4)` → `rgba(121,134,203,0.0)` (wie CTL-Chart)
- **Ziel-Linie:** gestrichelt bei 8h, Farbe `#4fc3f7` (cyan), Label "8h Ziel"
- **Heute-Marker:** gefüllter Kreis am letzten Datenpunkt
- **X-Achse:** ca. 4 Labels (1 pro Woche), z.B. "25. Mär", "1. Apr", "8. Apr", "15. Apr"
- **Y-Achse:** 0–10h (keine Achsenbeschriftung, nur Ziel-Linie)
- **ViewBox:** `0 0 300 80` (identisch mit CTL-Chart)

### Anzeige unter dem Chart

Zwei Werte nebeneinander (wie CTL-Chart aktuell):

- Links: **Heutiger Schlaf** in Stunden (z.B. `8.9h`), Farbe `#7986cb`
- Rechts: **Ø 30 Tage** in Stunden, Farbe `#81c784` wenn ≥ 7h, `#ef4444` wenn < 7h

### Template-Variablen in `build_context()`

```python
context['sleep_path']       = sleep['path']
context['sleep_fill_path']  = sleep['fill_path']
context['sleep_today']      = sleep['sleep_today']   # float oder None
context['sleep_avg_30d']    = sleep['avg_30d']        # float
context['sleep_day_labels'] = sleep['day_labels']     # list[str]
```

---

## 2. Layout-Umbau (`dashboard.template.html`)

### Neues Layout (in Reihenfolge)

| Position | Inhalt | Desktop | Mobil |
|---|---|---|---|
| 1 | Recovery · Trainingsform · Wochenziel | 3 Ringe nebeneinander | gestapelt |
| 2 | Wochenplan + Ernährung | 2 Spalten | gestapelt |
| 3 | CTL-Verlauf (6 Mon.) + Schlaf-Verlauf (30 Tage) | 2 Spalten | gestapelt |
| 4 | Readiness Score + TSS-Übersicht (8 Wo.) | 2 Spalten | gestapelt |
| 5 | Polarisations-Monitor | 1 Spalte | — |
| 6 | Ausblick 4 Wochen | 1 Spalte | — |
| 7 | Power Bestwerte + Lauf Bestwerte | 2 Spalten | gestapelt |

### Was sich ändert

**Aus dem alten `main-grid` (links/rechts) herauslösen:**
- Wochenplan (war: links)
- Readiness Score (war: rechts)

**Ernährung hochziehen:**
- War: ganz unten (nach Power/Lauf)
- Neu: Position 2, neben Wochenplan

**Neues CSS-Muster für 2-Spalten-Blöcke:**
```css
.two-col-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}
@media (max-width: 700px) {
  .two-col-grid { grid-template-columns: 1fr; }
}
```

Dieses Muster wird für alle 4 zweispaltigen Zeilen verwendet (Positionen 2–4 und 7).

### Schlaf-Chart Template-Block

Neue Karte `card-sleep` analog zu `card-ctl`, eingefügt in das zweispaltige Grid an Position 3:

```html
<div class="two-col-grid">
  <!-- vorhandene CTL-Karte (unverändert) -->
  <div class="card card-ctl">...</div>
  <!-- neue Schlaf-Karte -->
  <div class="card card-sleep">
    <div class="card-title">😴 Schlaf-Verlauf · 30 Tage</div>
    <svg viewBox="0 0 300 80" ...>
      <!-- fill + line + Ziel-Linie + Heute-Marker -->
    </svg>
    <!-- X-Achsen-Labels -->
    <!-- Heute-Wert + 30-Tage-Schnitt -->
  </div>
</div>
```

---

## 3. Nicht im Scope

- Keine anderen neuen Charts (HRV, RHR, FTP, Heatmap, TSB-Prognose) — separate Entscheidung
- Keine Änderungen an `generate.py` außer `get_sleep_history()` und `build_context()`
- Keine Änderungen an SKILL.md oder Planungsdateien

---

## 4. Dateien, die sich ändern

| Datei | Änderung |
|---|---|
| `generate.py` | Neue Funktion `get_sleep_history(days=30)`, Aufruf in `build_context()` |
| `dashboard.template.html` | Layout-Umbau, neuer Sleep-Chart-Block |

---

## 5. Erfolgskriterien

- Dashboard zeigt Schlaf-Chart mit korrekten Daten der letzten 30 Tage
- Ziel-Linie bei 8h sichtbar
- Heutiger Schlafwert + 30-Tage-Schnitt unter dem Chart
- Desktop: CTL und Schlaf-Chart nebeneinander
- Desktop: Wochenplan und Ernährung nebeneinander
- Mobil: alle Karten gestapelt
- Bestehende Karten (Ringe, Polarisation, Ausblick, Power, Lauf) unverändert
