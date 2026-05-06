# Homescreen Icon – Design Spec

**Datum:** 2026-05-06  
**Status:** Approved

## Entscheidung

Icon D1 „Clean Curve" ersetzt das bisherige Berggipfel-Icon in `docs/icon.svg`.

## Design

- **Form:** Ansteigende Bézier-Kurve, Ecke links-unten → Ecke rechts-oben
- **Gradient:** Purple `#a78bfa` (links, 35% opacity) → Purple `#a78bfa` (Mitte, voll) → Grün `#22c55e` (rechts)
- **Fill:** Subtile lila Fläche unter der Kurve (`#a78bfa`, max 13% opacity → 0%)
- **Glow:** Doppelter Layer — weicher Blur-Glow + scharfe Hauptlinie
- **Endpunkt:** Grüner Kreis mit weißem Kern + Glow (`#22c55e`)
- **Hintergrund:** `#070b11` mit `rx="115"` (iOS-Rundecken, 512×512 viewBox)

## Bedeutung

Steigende Performance-Kurve = FTP-Entwicklung über die Saison. Grüner Zielpunkt = Ziel erreicht. Passt zum Dashboard-Motiv (Purple-Akzent, dunkler Hintergrund).

## Änderungen

| Datei | Aktion |
|---|---|
| `docs/icon.svg` | Ersetzen |

manifest.json, sw.js, Dashboard: keine Änderung nötig.
