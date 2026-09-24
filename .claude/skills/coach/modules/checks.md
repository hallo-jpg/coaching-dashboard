# Modul: Proaktive Checks (A–D)

*Geladen aus `SKILL.md` – bei jeder Wochenplanung nach dem Kontextladen.*
*Die Checks erzeugen keinen eigenen Modus. Ihr Output steht in Schritt 4 direkt nach 🎯 Standort,
in dieser Reihenfolge: D (Deload) → A (Test-Ankündigung) → B (Power-PR) → C (Lauf-PR). Kein Befund = kein Output.*

---

## Check A: Test-Ankündigung (FTP und Lauf-Benchmarks)

**Quelle:** `planung/periodisierung.md` → Tabelle „Testfenster" (FTP #1–#3, 5km, 10km-Benchmark, HF-160-Check).

1. Für jedes Testfenster: `tage_bis_test = Testtag − heute` (Testtag = der genannte Tag, sonst Do der KW).
2. Falls `14 < tage_bis_test ≤ 21` → Ankündigung:

```
📊 [Test] in ~3 Wochen (KW[N] · [Tag, Datum])
Voraussetzungen: ≥3 Tage ohne Qualität davor · Readiness ≥ 70 · kein Reisetag direkt davor
Soll ich die Testwoche jetzt vorplanen? → [ja] / [verschieben auf KW[N+1]]
```
- **ja** → Modul `modules/ftp-test.md` (FTP) bzw. Testwoche mit Mini-Taper (Lauf) planen.
- **verschieben** → Testfenster in `periodisierung.md` um 7 Tage verschieben (Zustimmung liegt mit der
  Antwort vor), Akte-Eintrag `→ [Test] KW[N] auf KW[N+1] verschoben`.

**HF-160-Check (monatlich):** Einmal pro Monat in eine Woche ohne Qualität am Vortag legen. Protokoll: gleiche
Strecke, morgens, gefrühstückt, ≥48h nach hart, 10min einlaufen + 30min @ HF 160 → Ø Pace notieren
(Referenz 7:30/km @ 163 bei CTL 40). Ergebnis in `athlete/fortschritt.md` → Lauf-Entwicklung.

---

## Check B: Power-PR-Erkennung

⚠️ **Nur Werte derselben Messquelle vergleichen.** Die Referenzen in `athlete/fortschritt.md` →
„Power-PR-Referenz" stammen bis 4.4.2026 vom 4iiii und sind nicht vergleichbar. **Ab der Baseline KW40**
werden sie auf XCadey-Werte zurückgesetzt. Rollenfahrten auf dem Aeroad (Tacx-Leistung) nie gegen
XCadey-Referenzen prüfen – dafür Tacx-Wert ÷ Offset-Faktor, und nur als Hinweis, nie als FTP-Update-Grundlage.

1. `pr_neu` = höchster 3/10/20min-Wert der letzten 4 Wochen (`get_power_curve` bzw. Aktivitäten).
2. `pr_neu > pr_ref × 1,02` → PR-Flag. Jede Dauer unabhängig; bei mehreren nur **ein** Hinweis
   (Priorität 10min → 20min → 3min), alle Werte trotzdem in `fortschritt.md` eintragen.
3. FTP-Proxy: 10min × 0,90 · 20min × 0,95 · 3min = kein Proxy (nur W'-Signal).

```
💪 Neuer [X]min-Power-PR: [pr_neu]W (vorher [pr_ref]W, +[delta]%) → deutet auf FTP ~[proxy]W.
Aktuell gespeichert: [FTP]W. FTP aktualisieren? → [ja] / [nein] / [warten]
```
- **ja** → FTP-Update wie in `modules/ftp-test.md`, Abschnitt „FTP übernehmen".
- **nein / warten** → nur PR-Wert in `fortschritt.md`, Akte-Eintrag. Kein erneuter Hinweis bis > 2% darüber.

Der formale Test bleibt der Standard für FTP-Updates (CLAUDE.md) – ein PR-basiertes Update nur mit
ausdrücklichem „ja" von Stefan.

---

## Check C: Lauf-PR-Erkennung

**Teil 1 – Schwellenpace:** Nur aus einem **Wettkampf oder formalen Zeitlauf** (≥ 5 km, Vollgas) ableiten –
nie aus Intervallen oder Trainingsläufen mit Confoundern (COACH_MEMORY, Abschnitt 1).
Zeitlauf 10 km: Schwellenpace ≈ 10km-Pace × 1,00 (bei ~60–66 min Dauer ≈ Schwellendauer) ·
5 km: ≈ 5km-Pace × 1,05. Liegt der neue Wert > 2% schneller als die gespeicherte Schwelle (6:28/km):

```
🏃 Neue Schwellenpace: [pace]/km (bisher 6:28) aus [Lauf, Datum].
Neue Zonen: Z1 Easy [S+57 … S+132] · Z2 Aerob [S+27 … S+57] · Z3 Schwelle [S−18 … S+12] · Z4 VO2max [S−63 … S−18]
Übernehmen? → [ja] / [nein]
```
**ja** → `athlete/profil.md` (Schwelle + Zonen), `generate.py` → `get_zone_data()` (Lauf-Zonen),
`athlete/fortschritt.md` (Lauf-Entwicklung), `CLAUDE.md` Zeile Lauf-Schwellenwerte, Akte-Eintrag.
**Stefan bitten, die Schwelle auch in intervals.icu zu setzen** – sonst zielen alle `pace_pct` falsch.
`COACH_MEMORY.md` → Tempozonen-Tabelle und `pace_pct`-Umrechnung aktualisieren.

**Teil 2 – Distanz-PR:** `get_pace_curve` (1,5 / 5 / 10 km) vs. „Lauf-PR-Referenz" in `fortschritt.md`.
> 2% schneller → Hinweis + Frage „PR speichern?". Priorität 5 km → 10 km → 1,5 km.

Keine Läufe in 4 Wochen → Check C überspringen.

---

## Check D: Deload-Signal & Test-Readiness

**Teil 1 – Deload-Signal** (erste zutreffende Zeile gewinnt):

| # | Bedingung | Schwere |
|---|---|---|
| 1 | TSB < −30 an ≥ 3 aufeinanderfolgenden Tagen | 🔴 |
| 2 | HRV 7d-Schnitt > 10% unter 30d-Basis an ≥ 5 Tagen | 🟡 |
| 3 | ACWR (ATL ÷ CTL) > 1,5 | 🟡 |
| 4 | Lauf-km zwei Wochen in Folge > +10% **und** Wade meldet sich | 🟡 |

```
⚠️ Deload-Signal: [Begründung]
Empfehlung: KW[N] als Entlastung (−40–50% TSS, keine Qualität, Laufvolumen −30%)
Soll ich KW[N] so planen? → [ja] / [nein]
```
Liegt ohnehin eine geplante Entlastungswoche an: nur erwähnen, keine Frage.

⚠️ Bei niedriger CTL (< 35) ist ACWR > 1,5 fast unvermeidlich, sobald die Rampe läuft – dann nur 🟡 ausgeben,
wenn zusätzlich Readiness < 60 oder HRV-Signal vorliegt.

**Teil 2 – Test-Readiness** (nur ohne Deload-Signal): TSB +5…+15 · HRV 7d ≥ 30d-Basis · ≥ 21 Tage seit
letztem Test · kein Event in 10 Tagen → Hinweis „gute Testbedingungen in den nächsten 3 Tagen – einplanen?".
Bei „nicht jetzt": Akte-Eintrag `→ Test-Readiness-Hinweis unterdrückt bis [heute + 14]`.
