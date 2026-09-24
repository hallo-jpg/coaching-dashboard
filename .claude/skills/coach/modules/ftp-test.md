# Modul: FTP-Testwoche, Auswertung & FTP-Update

*Geladen aus `SKILL.md` – wenn eine Testwoche geplant wird (Check A „ja"), Stefan ein Testergebnis meldet
(„neues FTP", „10min: XXX W") oder ein PR-basiertes FTP-Update bestätigt wurde.*

## Setup (entschieden, Stefan 24.9.2026)

**Tarmac SL8 mit XCadey auf den Tacx Flux.** Parallel aufzeichnen: **XCadey → COROS DURA** (maßgebliche
Datei) und **Rolle → Tacx-App** (nur für den Offset-Faktor). **Kein ERG-Modus** – Level-/Standardmodus,
geschaltet wird am Tarmac. Ventilator an, XCadey vor dem Start nullen, Tacx-Spindown nach 10min Warmfahren.
Alle Wintertests (KW40, KW01, KW09) identisch aufbauen – nur die Differenz zählt.

## Testwoche (Mini-Taper)

| Tag | Einheit | TSS ca. |
|---|---|---|
| T-3 | Ruhetag | – |
| T-2 | LIT 1h locker | ~30 |
| T-1 | Easy-Lauf 30min **oder** LIT 45min mit 3×1min zügig | ~25 |
| **T-0** | **🔬 FTP-Test 3+10min** | ~75 |
| T+1 | Ruhetag | – |
| T+2/3 | LIT lang, Recovery-Charakter | ~40–55 |

Keine Qualität in den 3 Tagen davor. Readiness ≥ 70 am Testtag, sonst um 1–2 Tage schieben.

**Workout in intervals.icu:** `type: "Ride"`, Name ohne Emoji: „FTP-Test Sentiero 3+10min", Zeile 1 der
Description: „Kein ERG – Level-Modus. XCadey an DURA, Tacx-App zeichnet parallel." Schritte als Description-
Route (freie Fahrt in den All-Outs, keine Zielwatt).

## Protokoll Sentiero 3+10min

1. **20 min progressiv warmfahren** in Stufen à 5 min: ~50 / 60 / 70 / 80% FTP (alte FTP 305 bzw. letzte
   Baseline) – jede Stufe sauber gleichmäßig, die Stufen liefern die Offset-Punkte bei niedriger Last.
2. 3 min All-Out (nicht überpacen)
3. 5 min aktive Erholung
4. 10 min All-Out (gleichmäßig, letzte 2 min alles)
5. 10 min ausfahren

## Auswertung (wenn Stefan das Ergebnis meldet oder die Aktivität in intervals.icu liegt)

1. **FTP = XCadey-10min-Ø × 0,90** (aus der DURA-Datei).
2. **Offset-Faktor = Tacx-Ø ÷ XCadey-Ø** für: jede Warmfahr-Stufe, 3min, 10min. Liegen die Faktoren innerhalb
   ±2 % → ein Faktor (Mittel). Sonst Faktor je Intensitätsbereich (LIT / Schwelle) angeben.
3. **CP/W'** (wenn 3min-Ø bekannt): `CP = (P10 × 600 − P3 × 180) / 420` · `W' = (P3 − P10) × 180 × 600 / 420 / 1000` kJ.
4. **Doppelzählung:** Stefan erinnern, die Tacx-Aufzeichnung in intervals.icu zu löschen oder von der
   Belastungsrechnung auszunehmen.

```
📊 FTP-Test [Datum]
10min XCadey: [P10]W → FTP [FTP]W ([W/kg] W/kg @ [Gewicht aus profil.md]) · vorher [alt]W ([±%])
3min: [P3]W → CP ~[CP]W · W' ~[W'] kJ
Offset Tacx/XCadey: LIT [f1] · Schwelle [f2] → Indoor-Zielwatt = XCadey-Zielwatt × [f]

Neue Zonen (Sentiero): Z0 <[.52] · Z1 [.52–.62] · Z2 [.62–.70] · Z3 [.70–.93] · Z4 [.93–1.03] · Z5 [1.03–1.38] · Z6 >[1.38]
Zielwatt: LIT 55% [x] · SwSp 89% [x] · KA 91% [x] · MIT 101% [x]
Übernehmen? [ja / nein]
```

## FTP übernehmen (bei „ja")

1. `athlete/profil.md`: FTP, W/kg (Gewicht = aktueller 30d-Schnitt aus profil.md), Zonen, Workout-Zielwatt,
   Offset-Faktor, Hinweis „Zonen wieder trainingsleitend".
2. `athlete/fortschritt.md`: FTP-Verlauf (Methode „3+10 Rolle/XCadey"), Power-PR-Referenz auf die neuen
   XCadey-Werte **zurücksetzen** (alte 4iiii-Werte als historisch markieren), CP/W'-Verlauf.
3. `generate.py` → `get_zone_data()`: `"ftp"` + alle 7 Rad-Zonen (`round(ftp × Grenze)`, untere Grenze +1W).
4. `CLAUDE.md`: FTP-Zeile + Hinweis „nicht trainingsleitend" entfernen.
5. `COACH_MEMORY.md` → Abschnitt 6: „Bis zum Baseline-Test alte Zonen" ersetzen durch neue FTP + Offset.
6. `COACHING_AKTE.md` (oben): `## [Datum] – FTP-Test KW[N]` mit 10min/3min, FTP alt → neu, Offset, CP/W'.
7. **Stefan erinnern, die FTP überall zu setzen:** intervals.icu, **Garmin Connect (steht auf 325)**, COROS,
   MyWhoosh/Tacx-App.
8. Bereits angelegte Rad-Workouts der nächsten 2 Wochen prüfen: Zeile-1-Watt an die neue FTP anpassen.
9. Commit + push.

**Grundsatz:** FTP-Update nur nach formalem Test oder ausdrücklich bestätigtem PR (Check B) – nie wegen
„fühlt sich schwerer/leichter an". Auswirkung auf den laufenden Block kurz kommentieren.
