# Dashboard Redesign – Design Spec
*2026-05-04 · Coaching Dashboard · Stefan*

## Ausgangslage

Das aktuelle `dashboard.template.html` wirkt flat und generisch ("typisch AI"). Layout-Struktur und Kartenanordnung sind gut — nur Look & Feel muss sich verändern.

## Design-Entscheidung

**Glassmorphism + Glow Rings**

Erarbeitet in iterativem Browser-Mockup-Prozess (Vergleich Athletic/Sport vs. Glassmorphism vs. Premium Noir → Glassmorphism gewählt; Ringe: 3D-Effekt abgelehnt → nur Glow).

---

## Design-System

### Hintergrund

Farbige Radial-Lichtquellen über tiefem Dunkelblau — kein flat black:

```css
background:
  radial-gradient(ellipse 80% 60% at 15%  8%, rgba(99,70,210,0.26)  0%, transparent 55%),
  radial-gradient(ellipse 55% 45% at 88% 18%, rgba(34,197,94,0.13)  0%, transparent 50%),
  radial-gradient(ellipse 50% 55% at 50% 85%, rgba(45,212,191,0.11) 0%, transparent 55%),
  radial-gradient(ellipse 65% 35% at  8% 75%, rgba(96,165,250,0.09) 0%, transparent 50%),
  #070b11;
```

### Glasskarten (alle Kacheln)

```css
background: rgba(255,255,255,0.048);
backdrop-filter: blur(20px);
border: 1px solid rgba(255,255,255,0.10);
border-radius: 18px;
box-shadow: 0 1px 0 rgba(255,255,255,0.07) inset, 0 8px 32px rgba(0,0,0,0.35);
```

### Farb-Tokens (unverändert, nur Kontext ändert sich)

| Token | Hex | Einsatz |
|---|---|---|
| `--green` | `#22c55e` | Readiness OK, LIT, positiv |
| `--yellow` | `#f59e0b` | Warnung, TSB negativ, Countdown |
| `--red` | `#ef4444` | Kritisch, HIT-Anteil |
| `--orange` | `#ff6b35` | Ernährung |
| `--purple` | `#a78bfa` | CTL, Phase-Pill, Ausblick-KW |
| `--teal` | `#2dd4bf` | TSS-Ring, Ausblick-Icon |
| `--blue` | `#60a5fa` | Schlaf, Polarisation |
| `--muted` | `rgba(180,210,240,0.42)` | Alle Labels/Subtext |
| `--border` | `rgba(255,255,255,0.08)` | Trennlinien |

### Typografie

Keine Änderung an Schriftfamilie. Änderungen:
- **Eyebrows/Labels:** `font-weight: 700`, `text-transform: uppercase`, `letter-spacing: 0.7–1px`
- **Große Zahlen:** `letter-spacing: -2px` bis `-4px` für Kompaktheit
- **Pills:** `border-radius: 99px` (Capsule-Form, nicht eckig)

### Karten-Header

Jede Karte bekommt ein kleines farbiges Icon-Kästchen als visuellen Anker:

```html
<div class="chard">
  <div class="chard-icon" style="background:rgba(34,197,94,0.12)">💚</div>
  Readiness Detail
</div>
```

```css
.chard-icon { width:22px; height:22px; border-radius:6px; font-size:.75rem; }
```

---

## Ringe (kritische Änderung)

**Prinzip:** Drei Lagen — Track, Glow-Clone (blur), Arc — kein 3D, kein Groove, kein Highlight-Ring.

```svg
<!-- 1. Track (semitransparent) -->
<circle r="52" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="9"/>

<!-- 2. Glow-Clone (identischer Arc, blur-gefiltert, hinter dem Arc) -->
<circle r="52" fill="none" stroke="#22c55e" stroke-width="9"
        stroke-linecap="round"
        stroke-dasharray="[filled] [total]"
        transform="rotate(-90,65,65)"
        opacity="0.45"
        filter="url(#glow)"/>  <!-- feGaussianBlur stdDeviation="5" -->

<!-- 3. Haupt-Arc mit Gradient -->
<circle r="52" fill="none"
        stroke="url(#gradient)" stroke-width="9"
        stroke-linecap="round"
        stroke-dasharray="[filled] [total]"
        transform="rotate(-90,65,65)"/>
```

### Ring-Mapping

| Ring | Farbe | Gradient | Daten |
|---|---|---|---|
| Readiness | Grün | `#16a34a → #86efac` | `score/100 × 327` |
| Trainingsform | Doppelring: Lila (außen r=52) + Rot (innen r=37) | `#5b21b6 → #c4b5fd` / `#991b1b → #fca5a5` | CTL/CTLmax · ATL/ATLmax |
| Wochenziel | Teal | `#0d9488 → #5eead4` | `tss_ist/tss_plan × 327` |

Circumference: `r=52 → 327px`, `r=37 → 232px`
Arc-Länge: `dasharray="[pct × circ] [circ]"`

---

## Betroffene Kacheln (alle)

Alle Kacheln in `dashboard.template.html` erhalten das neue Design-System. Reihenfolge bleibt unverändert:

1. Header + Phase-Pill
2. Countdown-Row (RadRace + Rosenheimer)
3. Phase-Bar (KW14–26)
4. Rings-Row (Readiness · Trainingsform · Wochenziel)
5. 2-Col: Wochenplan · Ernährung
6. 2-Col: Readiness-Detail · Polarisation + Load Quality
7. CTL-Verlauf 30 Tage *(Chart-Farben + Glasskarte)*
8. 2-Col: Power Bestwerte · Schlaf-Verlauf
9. Lauf Bestwerte *(Glasskarte + Gradient-Bars)*
10. Rennprognose / PMC *(Glasskarte)*
11. Ausblick 4 Wochen

---

## Was sich NICHT ändert

- Jinja2-Template-Struktur (`{% for %}`, `{{ }}`) bleibt unverändert
- Alle CSS-Klassen-Namen die `generate.py` oder andere Skripte referenzieren
- Layout-Reihenfolge der Kacheln
- Datei-Pfad `dashboard.template.html`
- Mobile-Breakpoints (nur visuelles Restyling, keine strukturellen Änderungen)

---

## Umsetzung

Änderungen ausschließlich in `dashboard.template.html`:
- `:root` CSS-Variablen aktualisieren
- `body` Background ersetzen
- Alle `.ring-card`, `.week-card`, `.readiness-card` etc. auf `.g` (Glasskarte) umstellen
- SVG-Ringe neu schreiben (3 Lagen wie oben)
- Karten-Header auf `chard`-Pattern umstellen
- Pills auf `border-radius: 99px`
- `generate.py` bleibt unverändert (nur Template ändert sich)

---

## Mockup-Referenz

Finaler Mockup: `.superpowers/brainstorm/96274-1778007792/content/final-mockup-v2.html`
