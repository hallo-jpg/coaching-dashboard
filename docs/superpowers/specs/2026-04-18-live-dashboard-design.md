# Live Coaching Dashboard — Design Spec
*Erstellt: 2026-04-18*

## Ziel

Das bestehende statische `dashboard.html` wird zu einem live-aktualisierten Dashboard, das automatisch nach jedem Workout-Upload auf intervals.icu aktualisiert wird. Stefan öffnet die PWA auf dem iPhone und sieht immer den aktuellen Stand — Plan vs. Ist, TSS, CTL/ATL/TSB, HRV, Schlaf.

---

## Architektur

```
intervals.icu
    │ ACTIVITY_ANALYZED Webhook
    ▼
GitHub API (repository_dispatch)
    │ triggert
    ▼
GitHub Actions: generate.py
    ├── liest: planung/kw[N].md   → Wochenplan
    ├── liest: COACHING_AKTE.md   → Kontext/Notizen
    └── ruft ab: intervals.icu API
            ├── /activities       → absolvierte Workouts
            ├── /wellness         → HRV, Schlaf, Gewicht, Ruhepuls
            └── /athlete/fitness  → CTL, ATL, TSB
    │
    ▼
dashboard.html (alle Werte eingebaut, kein Client-JS-Fetch)
    │
    ▼
GitHub Pages (privates Repo + JS-Passwortschutz)
    │
    ▼
PWA auf iPhone (installiert, offline-fähig via sw.js)
```

**Trigger:**
- Primär: intervals.icu `ACTIVITY_ANALYZED` Webhook → GitHub `repository_dispatch` → Build
- Fallback: Täglicher GitHub Actions Schedule um 07:00 CEST

**Latenz:** Workout hochgeladen → Dashboard aktualisiert in ~2–3 Minuten

---

## Daten-Mapping

| Dashboard-Element | Quelle | Bemerkung |
|---|---|---|
| CTL / ATL / TSB + Ringe | intervals.icu `/athlete/{id}/fitness` | Aktueller Tageswert |
| Readiness-Score (Ring) | intervals.icu `/wellness` | `ctl_score` / eigener Score falls vorhanden, sonst gewichteter Mittelwert HRV + Schlaf + TSB |
| Wochenplan Mo–So | `planung/kw[N].md` | Geplante Workouts per Tag |
| Workout erledigt ✓ / offen ❌ | Abgleich kw[N].md vs. `/activities` | Match via Datum + Sporttyp (Rad/Lauf/Kraft); kein exakter Namensabgleich |
| TSS pro Tag + Wochensumme | intervals.icu `/activities` | `training_load` Feld |
| HRV, Schlaf, Ruhepuls | intervals.icu `/wellness` | Tageswerte |
| Readiness-Balken (4 Felder) | intervals.icu `/wellness` | HRV, Schlaf, TSB, Puls |
| HRV-Sparkline | intervals.icu `/wellness` (7 Tage) | Letzte 7 Einträge |
| Polarisation (Z1/Z2/Z3) | intervals.icu `/activities` | Zonenverteilung aus Workouts |
| Phase, KW, Countdown | Berechnet aus Systemdatum | Keine API nötig |
| 4-Wochen-Ausblick | `planung/kw[N+1..N+3].md` | Kommende Wochen |

---

## Komponenten

### `generate.py`
- Liest aktuelle KW aus Datum → lädt `planung/kw[N].md`
- Ruft intervals.icu API ab (API-Key aus Umgebungsvariable)
- Parsed Markdown-Wochenplan → extrahiert Workouts pro Tag
- Matched Aktivitäten: Datum + Sporttyp → markiert als erledigt/offen
- Rendert `dashboard.html` aus Template (`dashboard.template.html`)
- Gibt fertiges HTML aus (alle Werte hardcodiert im Output)

### `dashboard.template.html`
- Identisch mit aktuellem `dashboard.html` optisch
- Statische Werte ersetzt durch Template-Platzhalter (z.B. `{{ctl}}`, `{{tss_ist}}`)
- Enthält weiterhin: manifest.json Link, sw.js Registrierung, JS-Passwortschutz

### `.github/workflows/build.yml`
- Trigger: `repository_dispatch` (Webhook) + `schedule` (07:00 CEST)
- Steps: Python Setup → `generate.py` ausführen → Output nach `docs/` → GitHub Pages deploy

### Webhook-Kette
- intervals.icu Webhook sendet POST an einen Empfänger-Endpunkt
- **Option A (bevorzugt):** intervals.icu unterstützt Custom Headers → direkt an GitHub API `POST /repos/{owner}/{repo}/dispatches` mit PAT im `Authorization`-Header
- **Option B (Fallback):** intervals.icu unterstützt keine Custom Headers → kostenloser Cloudflare Worker empfängt Webhook, leitet mit PAT an GitHub API weiter (< 10 Zeilen Code)
- PAT mit minimalem Scope (`workflow`) — nie im Code oder Dashboard sichtbar

---

## Sicherheit & Datenschutz

| Aspekt | Lösung |
|---|---|
| intervals.icu API-Key | GitHub Actions Secret — nie im HTML/Code |
| GitHub PAT (Webhook-Trigger) | intervals.icu Webhook-Config — minimale Rechte (nur `repo` scope) |
| Dashboard-Zugang | JS-Passwortschutz: Passwort in `localStorage` gespeichert, einmalige Eingabe |
| Repo-Inhalt | Privates GitHub Repo — Coaching-Dateien nicht öffentlich |
| GitHub Pages URL | Nicht indexiert, obscure URL — kein öffentlicher Zugang ohne Passwort |

---

## Einmaliger Setup (Reihenfolge)

1. Privates GitHub Repo erstellen, Coaching-Dateien pushen
2. `dashboard.template.html` aus bestehendem `dashboard.html` ableiten
3. `generate.py` schreiben und testen
4. GitHub Secrets anlegen: `INTERVALS_API_KEY`, `INTERVALS_ATHLETE_ID`
5. `.github/workflows/build.yml` einrichten
6. GitHub Pages aktivieren (Branch: `main`, Ordner: `docs/`)
7. Personal Access Token erstellen → in intervals.icu Webhook eintragen
8. Webhook in intervals.icu konfigurieren (`ACTIVITY_ANALYZED` Event)
9. JS-Passwortschutz ins Template einbauen
10. PWA auf iPhone installieren ("Zum Home-Bildschirm hinzufügen")

---

## Out of Scope

- Detailansicht einzelner Workouts (Leistungskurve, Segmente)
- Push-Notifications auf iPhone
- Mehrbenutzer-Support
- Echte Authentifizierung (Cloudflare Access o.ä.)
- Bearbeitung des Plans über das Dashboard
