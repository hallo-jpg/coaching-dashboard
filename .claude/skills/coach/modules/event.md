# Modul: Event – Tapering, Rennwoche, Pacing, Recovery

*Geladen aus `SKILL.md`, sobald `tage_bis_event ≤ 14` (Taper/Rennwoche), 1–14 Tage nach einem Event
(Recovery) oder bei einer Pacing-Frage. Events kommen ausschließlich aus `athlete/profil.md` →
„Event-Kalender". Aktuell ist kein Event geplant – dann wird dieses Modul nur für Zeitläufe/Benchmarks
(5km, 10km) in verkürzter Form genutzt (Mini-Taper 3 Tage, Pacing-Plan, keine Rennwoche).*

Zusätzlich laden: `coaching_science.md` Sektionen **6** (Tapering) · **10** (Fueling) · bei Rad-Rennen **13**
(Pacing) · bei Hitze **16**.

---

## Tapering (7–14 Tage vor Event)

**Grundregel (Mujika & Padilla):** Volumen runter, **Intensität halten**. Nie > 4 Tage ohne Reiz über Schwelle.

| Zeitraum | Volumen | Training |
|---|---|---|
| T-14 bis T-9 | −40% ggü. Vorwoche | 1× kurze Aktivierung in der Hauptsportart, Rest locker |
| T-8 bis T-7 | −55% | 1× kurze Aktivierung, Rest locker |
| T-6 bis T-0 | −55–60% | → Rennwoche |

**TSB-Ziel am Renntag +10 bis +20.** Prognose immer ausgeben: CTL × 0,976/Tag (42d), ATL × 0,867/Tag (7d),
geplante TSS addieren → `Prognose TSB Renntag: +XX (Ziel +10…+20) → auf Kurs / zu niedrig / zu hoch`.

**Taper-Anxiety** („schlapp", „reicht das", „sollte ich mehr trainieren"): Gefühl als normal einordnen,
TSB-Prognose zeigen, **kein Extra-Training**. Fitness verliert man in 14 Tagen nicht.

## Rennwoche (T-6 bis T-0)

Drei Intensitäts-Touches, Volumen minimal:
- **T-5:** kurze Schärfung (Rad 3–4 × 2min @ 105% FTP · Lauf 4 × 2min @ Rennpace)
- **T-3:** Openers (Rad 4–5 × 30s @ > 120% FTP · Lauf 5 × 30s zügig)
- **T-1:** Aktivierung – **immer T-1** (COACH_MEMORY), bei Zeitnot kürzen, nie verschieben
- Ruhetage dazwischen, KH ab T-2 hoch (Lauf-10km: 6–7 g/kg reichen; Rad > 3h: 8–10 g/kg)
- **Beine flach / neuromuskuläre Stille:** 4–6 × 30s zügig, auch an T-2 noch wirksam.

**Taper-Checkliste** (bei ≤ 7 Tagen immer ausgeben): Tag · Training · Ernährung (KH in g **mit dem aktuellen
Gewicht aus profil.md** rechnen) · Schlaf · ☐.

**Lauf-Rennplan:** Checkpoints an die km-Schilder, nicht an Auto-Lap (COACH_MEMORY). Entscheidungspunkt bei
Halbdistanz (Split + HF), HF-Gates aus Wettkampf-HF (LTHR 185), nie darunter. Kadenz-Cue alle 2–3 km.

## Pacing (Rad-Events mit GPX, manuell oder automatisch bei T ≤ 7)

GPX in `athlete/routes/` · Logik aus `generate_pacing.py` (Gradient × CP × Typ-Faktor → Zielwatt,
Newton-Solver → Geschwindigkeit). Ohne GPX: aus Distanz, Hm, Ø-Steigung schätzen und das sagen.

| Steigung | Zielwatt |
|---|---|
| Abfahrt | 60% CP |
| 0–2% | 92% CP |
| 2–4% | 97% CP |
| 4–6% | 100% CP |
| 6–8% | 105% CP |
| > 8% | 108% CP |

TT-Faktor × 1,03 · Gran-Fondo × 0,95 · Gran Fondo zusätzlich Energie-Budget (60–90 g KH/h).
Vollanalyse bei Bedarf: `python3 generate_pacing.py` erzeugt `docs/pacing.html` (nicht Teil des automatischen Builds), danach https://hallo-jpg.github.io/coaching-dashboard/pacing.html

## Recovery (1–14 Tage nach Event)

- Tage 1–4: Pause oder locker, keine Intensität. Nach Lauf-Wettkampf: erster Lauf frühestens Tag 2–3,
  Wadenregel (diffuser Muskelkater ok · punktueller Schienbeinschmerz → kein Lauf, melden).
- Tage 5–10: aufbauen, Rad-Intensität früher möglich als Lauf-Intensität (kein Impact).
- Danach entscheidet die Readiness. Zweites Event ≤ 14 Tage später: keine formelle Recovery, sondern Taper
  für Event B mit mindestens einer Schärfungseinheit ab T+5.
