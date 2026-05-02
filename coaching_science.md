# Coaching Science Reference

**Referenzdokument für den Claude Code Coaching-Skill**
Stand: April 2026 | Athlet: Stefan, FTP 305W, 3,47 W/kg, VO2max 59 ml/min/kg

---

## 1. Block-Periodisierung (Rønnestad et al.)

### Kernaussage der Forschung

Rønnestad et al. (2012, Scand J Med Sci Sports): 12 Wochen Block-Periodisierung vs. traditionelles Training bei Elite-Radfahrern → +4,6% VO2max und +2,1% FTP in der Block-Gruppe. Konzentrierte HIT-Blöcke (3 aufeinanderfolgende Wochen mit erhöhtem HIT-Anteil, gefolgt von 1 Erholungswoche) erzeugen durch kumulative neuromuskuläre und metabolische Erschöpfung einen stärkeren Supercompensations-Stimulus als dasselbe Trainingsvolumen gleichmäßig verteilt. Rønnestad et al. (2014, 2016): Bereits 3–4 HIT-Einheiten in einer Woche ("block week") reichen für deutliche Adaptationen. Hämatologische Marker (Hämoglobin, Hämatokrit) reagieren bereits nach 7 Tagen intensiver Blöcke.

### Praktische Umsetzung (Stefan)

- **Blockstruktur**: 2–3 Wochen intensiv (3× HIT/Woche), dann 1 Woche Regeneration (nur LIT + 1× moderate Einheit)
- **HIT im Block**: 4×4min @ 350–365W (115–120% FTP) oder 4×8min @ 320–335W (105–110% FTP)
- **LIT im Block reduzieren**: Volumen der lockeren Einheiten auf 60–70% drücken, damit HIT-Qualität erhalten bleibt
- **Nicht kombinieren**: Schwere Kraft- und HIT-Blöcke nicht in derselben Woche maximieren

### Studienzahlen

| Studie | Design | Ergebnis |
|---|---|---|
| Rønnestad 2012 (SJMSS) | 12W Block vs. Trad., Elite | +4,6% VO2max, +2,1% Wmax Block-Gruppe |
| Rønnestad 2014 (SJMSS) | 3-Wochen-Block, Elite | +8,7W Wmax, signifikant vs. Kontrolle |
| Rønnestad 2016 (EJAP) | Block mit 2× tägl. HIT | Hämatologische Anpassungen nach 7 Tagen |

---

## 2. Polarized Training vs. Pyramidal (Seiler et al.)

### Kernaussage der Forschung

Seiler & Kjerland (2006): ~80% der Einheiten unter der aeroben Schwelle (Z1), ~20% über der anaeroben Schwelle (Z3), wenig bis kein Zone-2-Schwellentraining. Seiler et al. (2013): Polarized > Schwellentraining in VO2max-Zuwachs (+6,8% vs. +2,1%) und Zeitfahrperformance über 9 Wochen. Das Pyramidal-Modell ist für Athleten mit <10h/Woche oder niedrigerem Ausgangsniveau praktikabler. Polarized entfaltet seinen Vorteil vor allem bei >12h/Woche.

### Entscheidungsmatrix

| Kriterium | Polarized | Pyramidal |
|---|---|---|
| Volumen/Woche | >10–12h | 6–10h |
| Erfahrungslevel | Fortgeschritten | Einsteiger/Mittel |
| Saisonphase | Basis + Aufbau | Grundlage |

### Praktische Umsetzung (Stefan)

- **Verteilung**: 4–5 LIT-Einheiten : 1–2 HIT-Einheiten/Woche (nach Einheiten, nicht Zeit)
- **LIT definieren**: <210–230W (70–75% FTP), Laktat <2 mmol/L, Sprechen möglich
- **HIT definieren**: ≥115% FTP (≥350W), klar über dem Knickpunkt
- **Zone 3 (260–285W) vermeiden** als Default – nur gezielt in Clearance-Einheiten

---

## 3. HRV-gesteuertes Training

### Metrik: RMSSD (nächtlich)

Coros, Whoop und die Sportwissenschaft verwenden **RMSSD** (Root Mean Square of Successive Differences) als HRV-Metrik. RMSSD ist stabil, wenig von der Atmung beeinflusst und sensitiv für autonome Veränderungen. Stefan's Coros misst RMSSD automatisch während des Schlafs — diese Werte fließen in das Dashboard ein.

### Normalbereich: 30-Tage-Baseline

**Kritisch:** Der Normalbereich ist individuell und muss aus den eigenen Daten berechnet werden. Stefan's Normalbereich: ~40–50 ms RMSSD. Berechnung: Mittelwert ± 1 Standardabweichung der letzten 30 Tage.

**Beide Richtungen sind relevant** (laut Coros-Klassifikation):

| Status | Kriterium | Bedeutung | Konsequenz |
|---|---|---|---|
| Erhöht | > Normalbereich (+1σ) | Entspannt, aber Ursache prüfen | Mit Vorsicht trainieren |
| Normal | Innerhalb Normalbereich (±1σ) | Guter Zustand | Plan wie vorgesehen |
| Reduziert | Leicht unter Normalbereich (−1–2σ) | Körper unter Stress | Zusätzliche Erholung erwägen |
| Niedrig | Deutlich unter Normalbereich (<−2σ) | Stark gestresst | Ruhetag empfohlen |

**Frühere Fehleinschätzung korrigiert:** Nur höhere HRV als gut zu werten ist falsch — auch deutlich erhöhte HRV (>1σ über Baseline) kann auf physiologischen Stress hinweisen (z.B. beginnende Krankheit, parasympathische Überreaktion).

### Kernaussage der Forschung

Kiviniemi et al. (2007): HRV-gesteuertes Training > fixer Plan in Ausdauerleistung. Plews et al. (2012–2016): 7-Tage-Trend des RMSSD als Entscheidungsanker. Buchheit (2014): Absolute Tagesschwankungen (±10–15% RMSSD) sind normal – erst Trends über 5–7 Tage sind handlungsrelevant. Meta-Analyse Duking et al. (2021): HRV-gesteuertes Training → ~5–7% mehr Leistungszuwachs als vorprogrammierte Pläne.

### Entscheidungsregeln (Plews-Protokoll)

**Messung**: Nächtlich automatisch via Coros (RMSSD-Durchschnitt über gesamten Schlaf).

| 7-Tage-Trend | Signal | Konsequenz |
|---|---|---|
| Steigend (>3% über 7 Tage) | Adaptation läuft | HIT wie geplant |
| Stabil (±3%) | Normal | Plan beibehalten |
| Fallend (<−5%) | Kumulative Erschöpfung | 1 HIT → LIT ersetzen |
| Stark fallend (<−10%) | Overtraining-Risiko | 2–3 Tage nur LIT |

**Tageswert** (ergänzend, relativ zum 30-Tage-Schnitt):
- Innerhalb ±1σ: Normal, Plan wie vorgesehen
- > +1σ (erhöht): Vorsichtig trainieren, andere Faktoren beobachten
- −1 bis −2σ (reduziert): Intensität reduzieren
- < −2σ (niedrig): Ruhetag

---

## 4. VO2max-Entwicklung – Intervallformate

### Kernaussage der Forschung

Billat et al. (1999–2001): "Zeit bei VO2max" (Tlim) ist der entscheidende Trainingsreiz. Rønnestad et al. (2015): 4×4min @ ~90–95% VO2max liefert nachhaltigsten Stimulus. Buchheit & Laursen (2013, Sports Medicine): Kurze Intervalle (30/15s) ermöglichen mehr Gesamtzeit bei VO2max bei geringerer neuromuskulärer Erschöpfung.

### Intervallformat-Vergleich

| Format | Intensität (Stefan) | Zeit @ VO2max | Einsatz |
|---|---|---|---|
| 4×4min | 350–365W | ~8–12min | Aufbau, Hauptphase |
| 4×8min | 320–335W | ~24–28min | VO2max-Ausdauer |
| 30/15s (×15–20) | 400W / 180W | ~12–18min | Erhalt, bei suboptimaler Form |
| 40/20s | ~395W | ~12min | VO2max-Erhalt |

### Praktische Umsetzung (Stefan)

- **Hauptprotokoll**: 4×4min @ 355W, Pause 4min @ 150W – 1–2×/Woche im Block
- **Erhaltungsprotokoll**: 30/15s-Intervalle – flexibel einsetzbar, auch bei leichter Müdigkeit
- **FTP/VO2max-Ratio**: Derzeit ~305/406 = 75%, Ziel 77–79%

---

## 5. Kraftausdauer / Low-Cadence Training (Rønnestad et al.)

### Kernaussage der Forschung

Rønnestad et al. (2010, 2014): Niedertouriges Bergfahren (50–60 rpm) bei 65–75% FTP erhöht Muskelaktivierung (EMG), fördert Typ-II-Faser-Rekrutierung, steigert Kraftausdauer. Pedersen et al. (2020): Low-Cadence verbessert mechanische Effizienz ("gross efficiency") – bei gleicher Leistung weniger O2-Verbrauch. Rønnestad 2010: +4,8% Wmax nach 10-wöchigem Low-Cadence-Training.

### Praktische Umsetzung (Stefan)

- **Protokoll**: 3–5×10min @ **91% FTP (277W)** @ 50–60 rpm (Sweetspot-Leistung + niedrige Kadenz)
- **Pause**: 5min @ 55% FTP, Kadenz 65rpm
- **Warmup-Staircase**: 3min@60% → 3min@70% → 3min@80% → 3min@90% (neuromuskuläre Aktivierung)
- **Phase**: Ausschließlich Grundlagenphase – nicht kombinieren mit HIT-Blöcken
- **Kadenz**: 55rpm auf Intervallen, 65rpm auf Pausen – keine separate Kadenz-Progression
- **Ernährung**: So wenig KH wie möglich, Koffein vorher, Recovery-Shake danach
- **Kontraindikation**: Bei Knieproblemen – erhöht patellofemorale Belastung

---

## 6. Tapering

### Kernaussage der Forschung

Bosquet et al. (2007, Meta-Analyse n=27, Med Sci Sports Exerc): Optimales Tapering reduziert Volumen um 41–60%, hält Intensität konstant (≥90% der HIT-Einheiten), dauert 8–14 Tage. Progressive Taper > Step-Taper. Leistungsgewinn: Ø +2–3% im Zeitfahren. Pyne et al. (2009): >21 Tage = Detraining, <5 Tage = insuffizient. Intensitätserhalt ist der kritischste Einzelfaktor.

### 14-Tage-Taper vor Zeitfahren (Stefan)

| Tage vor Rennen | Volumen | Training |
|---|---|---|
| 14–10 (5 Tage) | −40% | 1× 4×4min @ 355W, Rest LIT |
| 9–7 (3 Tage) | −50% | 1× 3×4min @ 360W oder 20×30s @ 400W |
| 6–4 (3 Tage) | −55% | 1× 3×5min @ 295W (Aktivierung), Rest LIT |
| 3–2 | −60% | 45–60min @ 180–210W, locker |
| 1 (Vortag) | minimal | Aktivierun.zwo: 20–30min + kurze Intensität |

**TSB-Ziel**: +10 bis +20 am Renntag. Keine neuen Belastungsreize in letzten 10 Tagen.

### Carb-Loading-Protokoll (vor Ausdauerevents >2h)

Wissenschaftliche Basis: Bergström et al. (1967) – Glykogensupercompensation. Burke et al. (2011, IJSNEM): 10g KH/kg/Tag für 24–48h vor Event maximiert Glykogenspeicher auf ~750mmol/kg DM. Jeukendrup (2017): Bei gut trainierten Athleten reichen 24–36h Carb-Loading.

**Stefan-spezifisch (88kg):**

| Zeitraum | KH-Ziel | Beispielquellen | Hinweise |
|---|---|---|---|
| T-3 (3 Tage vor Rennen) | 7g/kg = 616g | Normal essen + extra Pasta/Reis | Fett und Protein normal |
| T-2 | 8g/kg = 704g | Pasta, Reis, Brot, Bananen, Gels | Ballaststoffe reduzieren |
| T-1 | 10g/kg = 880g | Weißer Reis, Weißbrot, Maltodextrin | Kein Salat, kein Rohkost |
| Renntag-Frühstück (3h vor Start) | 150–200g KH | Reis + Honig, Weißbrot + Marmelade, Gels | Fett und Protein minimal |
| 30min vor Start | 30–40g KH | Gel + Wasser | Koffein-Gel wenn gewünscht |

**Wichtig:** Während des Carb-Loadings +500–700ml mehr Wasser/Tag trinken (Glykogen bindet Wasser ~3:1).

### Renntag Warm-up (Zeitfahren)

Wissenschaftliche Basis: Burnley et al. (2005, JAP): VO2-Kinetik-Priming durch Warm-up reduziert O2-Deficit in den ersten Minuten des Zeitfahrens. Bishop (2003): 15–20min progressives Warm-up + kurze Intensität optimiert Muskeltemperatur und metabolische Bereitschaft.

**Standardprotokoll Zeitfahren (35–40min gesamt):**

```
1. 10min @ 160–180W (Z1, locker einkurbeln)
2. 5min @ 200–230W (Z2, Aerob aufwärmen)
3. 2× 1min @ 300–320W (FTP-Bereich), 2min Pause dazwischen
4. 1× 20s @ 400–430W (neurales Priming)
5. 5min @ 160W (Auskurbeln, klar werden)
→ Start: 3–5min nach Ende des Warm-ups
```

Bei Massenstart-Rennen (kein Zeitfahren): Warm-up 20min, weniger Intensität, mehr Aerob.

---

## 7. Laktat-Clearance Training (MCT-Transporter)

### Kernaussage der Forschung

MCT1 und MCT4 (Monocarboxylat-Transporter) ermöglichen Laktattransport zwischen Muskelzellen und Oxidationsgewebe. Pilegaard et al. (1999), Bonen et al. (2000), Dubouchaud et al. (2000): Ausdauertraining erhöht MCT1 um 30–80% und MCT4 um 20–50%. Effektive Laktatclearance erfordert Training in der "Shuttle-Zone" (Laktat 2–4 mmol/L). Juel & Halestrap (2004): molekulare Basis des Transportsystems.

### Transportweg

Typ-II-Faser → MCT4 → Blut → MCT1 → Typ-I-Faser / Herzmuskel (Oxidation) / Leber (Gluconeogenese)

### Praktische Protokolle

**Protokoll 1 – Steady-State Shuttle** (MCT1-Fokus):
2×20min @ 250–265W (82–87% FTP), Pause 5min @ 150W

**Protokoll 2 – Over-Under Intervalle** (MCT1 + MCT4):
3×(5min @ 320W + 5min @ 260W) – Überlaktat wird in Unterschwellen-Minuten geclearet

**Protokoll 3 – Lactate Flush** (nach HIT):
10–15min @ 240–260W direkt nach VO2max-Einheit – MCT-System unter Ermüdung trainieren

**Stefan MCT-Zone**: 240–270W (79–89% FTP)

---

## 8. Ernährungsperiodisierung

### Kernaussage der Forschung

Impey et al. (2018, Sports Medicine) – "Fuel for the Work Required": Gezielte Abstimmung von KH-Verfügbarkeit auf den Trainingsreiz. Train-Low-Protokolle steigern Enzymaktivitäten der Fettoxidation (CPT-1, beta-HAD) via AMPK → PGC-1α → mitochondriale Biogenese. Hearris et al. (2018): Train-Low zeigt metabolische Vorteile, Wettkampfleistung nur bei adäquater KH-Verfügbarkeit gesichert. Jeukendrup (2017): "Nutritional periodization" als übergeordnetes Prinzip.

### KH-Timing um Trainingseinheiten

| Einheitstyp | Vor Einheit | Während | Nach Einheit |
|---|---|---|---|
| LIT <90min | Nüchtern möglich | Nicht nötig (Rad) | Normal essen |
| LIT 90–180min | 30–60g KH | 30–60g/h optional (Rad) | +1,0–1,2g KH/kg in 2h |
| Lauf (alle) | Normal essen | **Kein Fueling** (aktuell) | Normal essen |
| HIT | 60–90g KH, 2–3h vorher | 60–90g/h bei >60min (Rad) | +1,2–1,5g KH/kg in 4h |
| RadRace 120 | 150–200g KH in 24h davor | 80–90g/h (trainierter Darm) | — |

### Sentiero KH/Fett-Referenz (Stefan)

| Zone | Watt | KH g/h | Fett g/h |
|---|---|---|---|
| FatMax (Z2) | 189–212W | 75–96 | 47–48 |
| Tempo (Z3) | 213–283W | 97–212 | 48–23 |
| FTP (Z4) | 283–314W | 212–282 | 23–0 |
| VO2max (Z5) | 315–422W | 283–371 | 0 |

### Sleep-Low-Protokoll (nur Grundlagenphase, 1–2×/Woche)

1. Abendliche HIT-Einheit ohne KH-Refuel danach
2. Nacht: Nur Protein (keine KH)
3. Morgen: LIT 60–90min nüchtern
4. Dann normales Frühstück mit KH

⚠️ **In letzten 8 Wochen vor RadRace kein Sleep-Low** – immer vollständig KH-auffüllen.

---

## 9. CTL / ATL / TSB – Banister-Modell

### Kernaussage der Forschung

Banister et al. (1975): Impulse-Response-Modell – Trainingsreiz erzeugt Fitness (langsamer Aufbau, langer Abbau) und Ermüdung (schneller Aufbau, schneller Abbau). Netto-Performance = Fitness − Ermüdung. Coggan & Allen adaptieren zu CTL/ATL/TSB. Kritische Limitierungen (Borresen & Lambert 2009): Modell ist linear, individuell nicht validiert. Gleicher TSS bei LIT ≠ gleicher TSS bei HIT.

### Richtwerte

| Parameter | Wert | Bedeutung |
|---|---|---|
| CTL-Aufbau | Max. 5–7 TSS/Tag/Woche | Nachhaltig ohne Overtraining |
| TSB Wettkampf | +5 bis +25 | Optimale Form (individuell) |
| TSB Warnsignal | Dauerhaft < −30 | Overtraining-Risiko |
| Taper-Ziel | TSB von −10 auf +15 bis +20 | Über 10–14 Tage |

### Für Stefan (Ziel CTL ~80–90 bei Saisonhöhepunkt)

- **CTL-Aufbau**: Max. 5–8 CTL-Punkte/Woche über 4 Wochen
- **Regenerationswochen**: Alle 3–4 Wochen → 40–50% TSS-Reduktion
- **Limitierung beachten**: TSS-Korrektheit hängt von korrektem FTP-Wert ab. Immer mit HRV und RPE kombinieren – nie alleiniger Steuerungsfaktor.

---

## 10. Fueling-Strategie (Stefan-spezifisch, wissenschaftlich fundiert)

### 10.1 Wissenschaftliche Grundlage: Multiple Transportable Carbohydrates

**Kernproblem**: Ein einziger KH-Transporter ist sättigbar.

- **SGLT1** (intestinaler Natrium-Glucose-Cotransporter): transportiert Glucose und Maltodextrin → Kapazität **max. 60g/h**
- **GLUT5** (Fructose-spezifischer Transporter): unabhängig von SGLT1, parallele Kapazität → **max. 30–36g/h**
- **Kombiniert** mit trainiertem Darm: **bis 120g/h** oxidierbar

| Quelle | Design | Ergebnis |
|---|---|---|
| Currell & Jeukendrup (2008) Med Sci Sports Exerc 40:275 | 2:1 Glukose:Fruktose vs. Glukose allein, 100km TT | +8% Leistung mit Kombi-CHO |
| Wallis et al. (2005) J Physiol | Oxidationsraten bei Kombi-CHO | Fruktose-Oxidation 50% höher in Kombination |
| Jeukendrup (2010) Curr Opin Clin Nutr Metab Care | Review | SGLT1-Sättigung bei 60g/h bestätigt; Kombi löst Deckel |
| Costa et al. (2017) Int J Sport Nutr Exerc Metab | Gut-Training, 28 Tage | Signifikante Reduktion von GI-Symptomen, +20% CHO-Toleranz |
| Jeukendrup (2017) Sports Med | Nutritional periodization | CHO-Menge an Intensität und Phase anpassen |
| Stellingwerff & Cox (2014) BJSM | Systematic Review | >1,5:1 Glukose:Fruktose = optimale Oxidationsrate |

**Optimales Verhältnis**: **2:1 Maltodextrin:Fructose** (≈ 1,36:1 Glucose:Fructose äquivalent)  
Stefan hat trainierten Darm (110g/h ohne GI-Probleme, Sommer 2025) → Vollkapazität nutzbar.

### 10.2 Osmolalität & Konzentration

| Konzentration | Osmolalität | Effekt |
|---|---|---|
| 4–6% (40–60g/L) | ~220–330 mOsm/kg | Leicht hypoton bis isoton – optimale Magenentleerung |
| 8–10% (80–100g/L) | ~440–550 mOsm/kg | Hypertonic – etwas langsamere Magenentleerung, tolerierbar |
| 15–18% (150–180g/L) | ~825–990 mOsm/kg | Sehr hypertonic – nur mit parallelem Wasser |

**Maltodextrin-Vorteil**: Polysaccharid → weniger osmotisch aktiv pro g als Monosaccharide. 90g Maltodextrin ≈ Osmolalität wie 45g Glucose. Deshalb sind höhere Konzentrationen mit Maltodextrin verträglicher.

**Praxis-Empfehlung**: Bei >75g CHO/h immer eine zweite Flasche mit reinem Wasser mitführen.

### 10.3 Intensitäts-spezifische Fueling-Empfehlungen

| Einheitstyp | Intensität | Dauer | g/h Empfehlung | Mix |
|---|---|---|---|---|
| LIT nüchtern (FatMax) | Z1–Z2 | <90min | **0** – nicht fuelen | – |
| LIT kurz | Z1–Z2 | <90min | **0–30g/h** | Nur Malto |
| LIT lang | Z1–Z2 | 90–180min | **30–50g/h** | Nur Malto |
| LIT sehr lang | Z1–Z2 | >180min | **50–70g/h** | Malto + Fructose 2:1 |
| KA | ~91% FTP (Z3–4) | 90–150min | **40–60g/h** (bewusst niedrig) | Nur Malto |
| SwSp / MIT | 88–101% FTP | 60–90min | **50–70g/h** | Malto, ab 70g/h + Fructose |
| SwSp / MIT lang | 88–101% FTP | >90min | **70–90g/h** | 2:1 Malto:Fructose |
| HIT / VO2max | >106% FTP | beliebig | **60–80g/h** | 2:1 Malto:Fructose |
| Rennen / FRT | Gemischt | >2h | **90–110g/h** | 2:1 Malto:Fructose |

**Warum KA bewusst niedrig?** Das KA-Protokoll arbeitet mit metabolischem Stress (hohe Intensität + niedrige Glykogenreserve). Zu viel exogenes CHO dämpft den AMPK-Reiz (Burke et al., 2011). 40–60g/h deckt Mindestbedarf ohne den Adaptationsstimulus zu blockieren.

**Warum LIT nüchtern bis 90min kein Fueling?** Fettoxidationsreiz (PGC-1α via AMPK). Über 90min kann Nüchternfahren auf Kosten der Qualität gehen – dann 30g/h Malto reicht als Minimumversorgung.

### 10.4 Stefan-Mischprotokoll (pro Flasche 500ml)

| Einheit | Malto | Fructose | Salz | Kalorien | g/h bei 1 Flasche/h |
|---|---|---|---|---|---|
| LIT 90–120min | 25g | – | 0.5g | 100 kcal | ~30g/h |
| LIT 2h+ | 40g | – | 0.75g | 160 kcal | ~45g/h |
| LIT 3h+ / Wochenendausfahrt | 40g | 20g | 1g | 240 kcal | ~60g/h |
| KA | 30g | – | 0.75g | 120 kcal | ~35g/h |
| SwSp / MIT | 40g | – | 1g | 160 kcal | ~45g/h |
| MIT lang / SwSp >90min | 50g | 25g | 1g | 300 kcal | ~75g/h |
| HIT / VO2max | 40g | 20g | 1g | 240 kcal | ~60g/h |
| HIT >90min / FRT | 50g | 25g | 1.5g | 300 kcal | ~75g/h |
| RadRace / Max-Ausdauer | 60g | 30g | 1.5g | 360 kcal | ~90g/h (+Wasser-Flasche) |
| Vollgas (trainierter Darm) | 70g | 35g | 2g | 420 kcal | ~105g/h (+Wasser-Flasche) |

**Flüssigkeit**: 500–750ml/h Standard, bei HIT im Sommer bis 1L/h (zweite Flasche Wasser zusätzlich bei >75g/h).

**Salz**: 1–2g NaCl/500ml = ~530–1050mg Natrium/L. Für Sommer/Hitze: oberes Ende (2g/500ml = ~1050mg Na/L). Wissenschaftliche Empfehlung: 500–1200mg Na/L (Shirreffs & Sawka, 2011, IJSNEM).

### 10.5 Pre-Exercise Ernährung nach Trainingstyp

#### LIT vor der Arbeit (früh morgens)

| Dauer | Empfehlung | Timing |
|---|---|---|
| <60min | Nüchtern, kein Essen | – |
| 60–90min | Nüchtern oder kleine Kleinigkeit (Banane, 1 Toast) | 20–30min vorher |
| 90–120min | Kleine Mahlzeit: Porridge 60g + Honig | 60–90min vorher |
| >2h | Richtiges Frühstück: 100–150g KH (Oats, Brot, Honig, Banane) | 90–120min vorher |

#### HIT nach der Arbeit (nachmittags/abends)

| Mahlzeit | Zeitpunkt | Inhalt |
|---|---|---|
| Mittagessen | 12–13 Uhr | Normal (KH + Protein), kein Frittiertes |
| Snack vor Training | 2–2.5h vor HIT | 60–80g KH: Reiswaffel + Banane + Sportgetränk oder Oats |
| Top-up | 30–45min vor HIT | Optional: Gel oder Banane (20–30g KH) |
| Während | Start in Warmup | 60–80g/h (2:1 Mix, erste Flasche schon in Warmup-Phase öffnen) |

#### MIT morgens (nach Schlaf)

| Mahlzeit | Zeitpunkt | Inhalt |
|---|---|---|
| Frühstück | 2–2.5h vor Start | 80–120g KH: Oats 80g trocken + Banane + Honig + Milch/Joghurt |
| Optional Snack | 30–45min vor Start | Banane oder 1–2 Reiswaffeln (20–30g KH) |
| Während | Ab ca. 20min | 50–70g/h (Malto oder 2:1 je nach Dauer) |

### 10.6 Koffein-Empfehlung

**Ergogene Dosis**: 3–6 mg/kg KG → bei 88kg = **264–528mg Koffein**  
**Timing**: Einnahme **45–60min vor Belastung** (maximaler Plasma-Peak nach 45–60min)  
**Quelle**: Goldstein et al. (2010) ISSN Position Stand; Doherty & Smith (2005) JSEP meta-analysis (+11% Ausdauerleistung)

| Einheitstyp | Empfehlung |
|---|---|
| LIT nüchtern | Kein Koffein (dämpft Fettoxidation via Insulin-unabhängige Pfade) |
| LIT standard | Kaffee in der Früh okay, aber keine Pflicht |
| KA | 1–2 Espresso (150–200mg), 45min vorher – im KA-Protokoll bereits verankert |
| HIT / VO2max | **Empfehlung: 200–300mg, 45min vorher** (1–2 Espresso oder Koffein-Gel) |
| MIT / SwSp | Optional: 1 Espresso 45min vorher wenn Training früh oder Ermüdung spürbar |
| RadRace | 300–400mg, 60min vor Start (Anpassung wenn Koffein-Pause 5–7 Tage davor) |

**Koffein-Sensitisierung**: Für maximale Wirkung am Renntag: **5–7 Tage Koffein-Pause** vor RadRace KW24, dann volle 300–400mg am Morgen. Bekanntes Konzept, hohe Evidenzlage (Burke 2008, Appl Physiol Nutr Metab).

### 10.7 RadRace Renntagsstrategie

| Zeitpunkt | Maßnahme |
|---|---|
| Abend davor | 400–500g KH über den Tag (Carb-Loading Light – kein Bloating) |
| Frühstück (3–4h vor Start) | Oats 120g trocken + 2 Bananen + Honig + Milch ≈ 180–200g KH |
| 60min vor Start | Koffein 300–400mg (nach 5-tägiger Pause) + 30g KH Snack |
| 30min vor Start | 1 Gel (20–25g CHO) |
| 0–60min Rennen | 60g/h (Einfahr- und Aufwärmphase, Darm aktivieren) |
| 60min+ | Auf 90–110g/h steigern (2:1 Malto:Fructose, +Wasser) |
| Verpflegungsstationen | Ergänzen, nicht ersetzen (eigene Flasche hat bekannte Konzentration) |

---

## Zonenmodell Stefan (Kombination Sentiero + Laktat-Referenz)

| Zone | Name | Watt | % FTP | Laktat ca. |
|---|---|---|---|---|
| Z0 | Recovery | <160W | <52% | <1,5 mmol/L |
| Z1 | Base | 160–188W | 52–62% | ~1,5 mmol/L |
| Z2 | FatMax | 189–212W | 62–70% | 1,5–2,0 mmol/L |
| Z3 | Tempo / MCT-Shuttle | 213–283W | 70–93% | 2,0–3,5 mmol/L |
| Z4 | FTP | 283–314W | 93–103% | 3,5–5,0 mmol/L |
| Z5 | VO2max | 315–422W | 103–138% | >5 mmol/L |
| Z6 | Anaerob | 423+W | >138% | >8 mmol/L |

**MCT-Shuttle-Zone**: 240–270W (unteres Z3)
**FatMax**: 189–212W (Z2)
**VO2max-Reiz**: ≥320W, Ziel ≥10min Gesamtzeit/Einheit

---

## 11. Concurrent Training: Laufen + Radfahren (Wissenschaftliche Grundlage)

*Ziel: Laufen als zweite ernstzunehmende Disziplin bei ~25–33% des Gesamtvolumens. Fundierte Integration ohne Interferenz mit Radleistung.*

### 11.1 Der Interferenzeffekt – klassisch und modern

**Hickson (1980, Eur J Appl Physiol):** Erste Demonstration des Interferenzeffekts: Gleichzeitiges Kraft- und Ausdauertraining hemmt Kraftadaptationen nach 7 Wochen – Ausdauerleistung bleibt aber erhalten. VO2max-Zuwächse durch kombinierten Radblock: +25% Rad, +20% Laufband – vergleichbar mit Ausdauer-only.

**Wilson et al. (2012, J Strength Cond Res):** Meta-Analyse, 21 Studien, 422 Effektgrößen: **Laufbasiertes** Concurrent Training hemmt Kraft/Hypertrophie erheblich (−26–40%); **radbasiertes** Concurrent Training zeigt minimale Interferenz. Für Stefan (Rad-Primärsportler): Laufen in das Rad-Programm integrieren erzeugt Interferenz in eine Richtung – Laufanpassung dauert länger als Radanpassung. Umgekehrte Interferenz (Lauf hemmt Rad) ist gering.

**Robineau et al. (2016, J Appl Physiol):** 0h/6h/24h Regeneration zwischen Einheiten:
- 0h (gleiche Session): neuromusk. Verbesserung −30–40%, VO2peak −20%
- 6h: 65–75% der Adaptation erhalten
- 24h: nahezu vollständige Adaptation in beiden Disziplinen

**Kernregel: Harte Rad + harte Lauf-Session → mind. 6h trennen, ideal 24h.**

### 11.2 VO2max-Transfer und Running Economy

**Bassett & Howley (2000):** VO2max transferiert zwischen Disziplinen partiell (70–85%). Radtrainierte Athleten zeigen auf Laufband 0–10% niedrigeren VO2max-Wert. Stefan: Rad-VO2max 59 ml/kg/min → erwarteter Lauf-VO2max initial ~52–54 ml/kg/min.

**Jones & Carter (2000):** Nicht VO2max, sondern **Running Economy** ist der primäre Limiter für Radfahrer die Laufen starten. Running Economy = Sauerstoffkosten pro km – hoch trainierbar, aber modellspezifisch:
- Rad: konzentrisches, nicht-gewichttragendes Training → kein Stretch-Shortening-Transfer
- Laufen: hohe exzentrische Last, Bodenreaktionskräfte 3× Körpergewicht, elastische Energie-Rückgewinnung

**Praktisch**: Erste 6–10 Wochen Laufeinheiten trotz guter Aerobkapazität "teuer" (schlechte Laufökonomie). In dieser Phase TSS-Schätzungen konservativ halten.

### 11.3 Verletzungsrisiko & Progression für Radfahrer

**Nielsen et al. (2014, JOSPT):** 874 Anfänger, 16 Wochen: Wöchentliche Steigerung >30% über 2 Wochen erhöht Verletzungsrisiko um Faktor 2,2. Real-Risikofaktor: Längster Einzellauf steigt >10% vs. letzten 30 Tagen.

**Buist et al. (2010, GRONORUN 2):** Vorbereitungsphase (4W Gehen + Hüpfen) vor strukturiertem Laufaufbau → 23% geringere Verletzungsrate.

**Spezifische Schwachstellen Radfahrer → Laufen:**
- Überdominante Quadrizeps, schwache Hamstring-Exzentrik → Knieschmerzen, Läuferknie
- Keine Impact-Belastung im Training → reduzierte Knochenbelastungstoleranz → Stressfrakturen möglich
- Tendenziell Überstrecken beim Laufen (overstride) nach Rad-Einheiten

**Präventionsmaßnahmen:**
- 2×/Woche Lauf-Athletik: Wadenheben, einbeinige Romanian Deadlifts, Hip-Thrust, Hüfte lateral
- Erste 4 Wochen KEIN Intensitätslauf – nur easy runs
- Single-leg Balance + Plyometrics einführen ab Woche 5+

### 11.4 Polarisierung gilt auch fürs Laufen (Seiler & Kjerland 2006)

**Stöggl & Sperlich (2014, Front Physiol):** 48 gut trainierte Ausdauersportler, 9 Wochen, 4 Trainingsverteilungen verglichen:
- Polarized (80/20): +11,7% VO2peak, +17,4% time-to-exhaustion
- Threshold: +7,2% VO2peak
- HIIT: +6,9% VO2peak
- High Volume: +5,5% VO2peak

**Ergebnis: Polarisierung schlägt alle anderen Modelle auch beim Laufen.**

**Intensitätszonen Laufen (Stefan, Schwellenpace 6:03/km):**

| Zone | Name | Pace | HF% | Beschreibung |
|---|---|---|---|---|
| Z1 | Easy | 7:00–7:45/km | 60–72% | Volle Unterhaltung möglich |
| Z2 | Aerob flott | 6:30–7:00/km | 72–82% | Leicht sprechen noch möglich |
| Z3 | Schwelle | 5:45–6:15/km | 82–92% | Nur kurze Sätze |
| Z4 | VO2max | 5:00–5:45/km | 92–100% | Sprechen nicht möglich |

**Faustregel:** 80% aller Laufminuten in Z1, max. 20% in Z3/Z4.

### 11.5 TSS-Berechnung Laufen (rTSS)

**Formel (identisch mit Rad-TSS):**
```
rTSS = (Dauer_Stunden × IF² × 100)
IF = Normalized Graded Pace / Schwellenpace
```
Schwellenpace Stefan: **6:03/km** = Basis (IF = 1.0)

**Orientierungswerte rTSS:**

| Einheit | Dauer | Pace | rTSS ca. |
|---|---|---|---|
| Easy Run 45min | 45 min | 7:30/km | 28–35 |
| Easy Run 60min | 60 min | 7:15/km | 38–45 |
| Schwelle 2×8min | 44 min | Mix | 45–55 |
| VO2max 3×5min | 50 min | Mix | 50–60 |
| Langer Easy Run 90min | 90 min | 7:30/km | 55–70 |

**Alternativ Session-RPE-Methode (Foster et al. 2001, Fallback):**
```
TSS-Äquivalent = RPE (0–10) × Dauer (h) × 10
```
Validiert auf ±10–15% vs. power/pace-Methode. Für alle Einheiten ohne Pacing-Device.

### 11.6 Optimale Laufeinheiten für Radfahrer

**Rangfolge nach Transfer-Effizienz:**

1. **Easy Runs (Z1)** – 75–80% des Laufvolumens
   - Baut Running Economy auf ohne Interferenz mit Rad-Intensitätstagen
   - 30–90 min, Pace konsequent unter aerober Schwelle halten

2. **VO2max-Intervalle (Z4)** – 10–15% des Laufvolumens
   - Hier transferiert Rad-VO2max am direktesten → schnellste Lauffortschritte
   - Format: 5×3min oder 4×5min @ ~5:10–5:30/km, Pause = 50% Arbeitszeit Trab
   - NICHT am selben Tag oder Tag nach hartem Rad-HIT

3. **Schwellenläufe (Z3)** – 5–10% des Laufvolumens
   - Verbessert Laktatchance und Laufökonomie auf Renntempo
   - Format: 15–25min kontinuierlich @ 5:45–6:15/km oder 3×5min mit 90s Trab

4. **Hügelläufe** – alternativ zu VO2max, gleichwertig
   - 4–10×1–2min bergauf @ 6–10% Steigung, volle Gehpause bergab
   - Aufbau exzentrischer Kraft (Hamstrings), Laufmechanik-Verbesserung
   - **Zusatznutzen:** Verbessert Bergfahren auf Rad (Beinkoordination)

5. **Strides / Läufe mit Antritten** – wöchentlich einbauen
   - 6–10× 20–30s beschleunigen auf ~5:00/km, vollständige Erholung
   - Neuromuskular, verbessert Lauffrequenz ohne Ermüdung

### 11.7 Concurrent Training vor Radevents (Taperingregeln)

**Bosquet et al. (2007, Meta-Analyse):** Fitness überlebt kurze Volumenreduktionen problemlos:
- 7–10 Tage Taper: keine messbaren Fitnessverluste
- 14 Tage: Fitness bei erhaltener Intensität stabil; 40–60% Volumensenkung tolerierbar
- >14 Tage ohne Laufen: erste Detraining-Signale

**Minimum-Erhaltungsdosis Laufen:**
- 1×/Woche Easy Run 20–30min erhält Lauf-VO2max für 4 Wochen
- 1× Schwelle + 1× Easy = volle Laufleistung für 6+ Wochen gehalten

**Konkrete Tapering-Strategie für Stefan (vor RadRace/Rosenheimer):**
- KW23 (Tapering): Rad-Intensität reduziert, Laufen: 2× Easy (je 25–30min) → kein Qualitätslauf
- KW24 (Rennwoche RadRace): Mo: Easy 20min; Do weg (Aktivierung Rad); kein Laufen rest
- KW25 (Recovery): Laufen ab Mi wieder einbauen: 1–2× Easy 30–40min
- KW26 (Rennwoche Rosenheimer): Do kein Laufen; Easy Sa entfällt (LIT Rad)

### 11.8 Wochenstruktur-Empfehlung (25–33% Laufen, Vollzeit berufstätig)

**Zielstruktur (HIT-Aufbaublock ab KW18 als Referenz):**

| Tag | Rad | Laufen | Notiz |
|---|---|---|---|
| Mo | – | Easy 35–45min | Ruhe/Aktiv-Erholung |
| Di | Rad HIT oder SwSp | – | Haupteinheit Rad |
| Mi | Rad LIT 1,5–2h | – | Grundlage |
| Do | – | Qualitätslauf (Schwelle od. VO2max) | Lauf-Schlüsseleinheit |
| Fr | Ruhetag | – | Recovery |
| Sa | Rad lang 2,5–3h | – | Wochenend-Haupteinheit |
| So | Rad LIT oder KA | Easy Lauf 45–60min (optional) | wenn Erholung gut |

**Grundsatz:** Ruhetag bleibt unter der Woche. Laufeinheiten auf Mo und Do/So verteilen. Nie Rad-HIT + Lauf-Qualität am selben Tag.

---

## 12. Critical Power / W' (Anaerobe Arbeitskapazität)

*Ergänzung zu FTP – relevant für Intervalldesign und Renn-Taktik*

### Modell und Unterschied zu FTP

**Moritani et al. (1981):** CP (Critical Power) ist der mathematische Asymptot der Power-Dauer-Kurve – die maximale aerob stabile Leistung. **W'** (W-Prime) ist der fixe anaerobe Energiespeicher oberhalb CP.

**Jones et al. (2010, Scand J Med Sci Sports):** CP und FTP sind nicht identisch:
- FTP = operationale Definition: 95% der max. 60-min-Leistung
- CP = mathematische Kurvenanpassung aus 2–3 Maximalversuchen
- CP liegt bei trainierten Radfahrern typischerweise **1–3% unter FTP**

**Stefan (geschätzt):** CP ≈ 297–303W | W' ≈ 19–23 kJ

### W' – Was es bedeutet

W' ist der "Akku" für Arbeit oberhalb CP. Sobald er leer ist, muss Intensität unter CP sinken damit er sich wieder auffüllt ("W'-Rekonstituierung"). Entscheidend bei:
- 3–10 Minuten Intervallen (W' beeinflusst Erholung zwischen Sätzen mehr als TSS)
- Rennataktik (Spurts, Attacken, steile Bergpassagen)

**Praktische Konsequenz:** Wenn Stefan nach 4×4min noch deutlich Körner hat, liegt CP höher als angenommen – FTP-Test nötig. Wenn die letzten 30s der 4. Einheit nicht mehr haltbar, ist W' erschöpft.

### W' schätzen (ohne Labor)

**3-Minuten All-Out Test:** 3min maximal fahren; die letzten 30s mitteln ≈ CP. Gesamtarbeit über CP = W'.
**Zwei Maximalversuche:** Z.B. 5min-Maximalleistung + 3min-Maximalleistung → hyperbolische Kurvenanpassung.

### Einsatz im Training (Hybridansatz)

| Aufgabe | Modell |
|---|---|
| Zonen-Definition, TSS, Periodisierung | FTP (305W) |
| Design 3–10min Intervalle | CP (~300W) als Zielleistung |
| Erholungszeit zwischen kurzen Sätzen | W'-Modell (mind. 50% Arbeitszeit Pause) |
| Rennpacing Kurzabschnitte | W' taktisch einkalkulieren |

### CP/W' aus Sentiero-Testergebnissen berechnen

**Kein separater Testtermin nötig** – der Sentiero 3+10min-Test liefert zwei Datenpunkte auf der
Power-Dauer-Kurve und ist ausreichend für eine valide CP/W'-Schätzung (±5% Fehler).

**Formel (linearisiertes Moritani-Modell):**

| Variable | Wert |
|---|---|
| P₁ | 3min-Durchschnittsleistung [W] |
| t₁ | 180 s |
| P₂ | 10min-Durchschnittsleistung [W] |
| t₂ | 600 s |

```
CP  = (P₂ × t₂ − P₁ × t₁) / (t₂ − t₁)    [W]
W'  = (P₁ − P₂) × t₁ × t₂ / (t₂ − t₁)    [J] → in kJ: ÷ 1000
```

**Beispiel Stefan (FTP 305W, Sentiero-Daten geschätzt):**
- Annahme: 3min-Avg ≈ 380W, 10min-Avg ≈ 310W
- CP = (310 × 600 − 380 × 180) / (600 − 180) = (186000 − 68400) / 420 ≈ **280W**
- W' = (380 − 310) × 180 × 600 / 420 ≈ **18 000 J = 18 kJ**

**Genauigkeit verbessern:** Ein optionaler 5min-Maximalversuch (separater Tag, frisch) als dritter
Datenpunkt reduziert den Fehler auf ±2–3% (drei-Punkte-Kurvenanpassung).

**Speicherung nach dem Test:** CP und W' in `athlete/fortschritt.md` → Abschnitt "CP/W'-Verlauf"
eintragen. Der `/coach`-Skill erledigt das automatisch nach jedem FTP-Test.

---

## 13. Zeitfahren-Spezifik: Pacing-Wissenschaft

### Even vs. Variable Pacing (Abbiss & Laursen 2008, Int J Sports Physiol Perform)

**Flaches TT:** Leicht negativ-split (start 95–98% CP, Ende 103–105% CP) ist optimal. Positives Pacing (zu schneller Start) kostet 2–5% Leistung durch frühe W'-Erschöpfung.

**Hügeliges TT (wie RadRace 120):** Variable Leistung ist biomechanisch unvermeidbar. Optimale Verteilung:
- **Bergauf**: 103–108% CP (W' gezielt einsetzen wo Widerstand hoch)
- **Bergab**: 60–80% CP (Erholung, W' rekonstituiert)
- **Variability Index (VI = Normalized Power / Avg Power): Zielwert 1.04–1.08**

Jede 0.01 VI-Erhöhung kostet ~0.5–1% Performance. VI 1.10 vs. 1.05 → 2–4 Minuten Zeitverlust auf 60km.

### Leistungsverteilung RadRace TT (Stefan)

| Phase | Dauer | Zielleistung |
|---|---|---|
| Einfahren 0–10min | ~10 min | 95–98% CP (284–295W) |
| Hauptphase 10–75min | ~65 min | 99–103% CP (298–312W) |
| Endspurt 75min–Ende | ~15 min | 103–107% CP (312–324W) – wenn W' erlaubt |

**Pacing-Anpassung nach TSB:**
- TSB +15 (gut getapert): Plan-Leistung
- TSB +5–8: Plan −2%
- TSB negativ (zu wenig getapert): Plan −5%, Disziplin über Absolute setzen

### Rosenheimer (197km / 3550hm) – anderes Spiel

Kein TT sondern Ausdauer-Rennen: W' ist bei 5–7h irrelevant (erschöpft und rekonstituiert sich hunderte Male). FTP-basiertes Pacing dominiert:
- KM 0–50: **95–100% FTP** (Anfahrt/Einfahr-Zone)
- KM 50–150: **88–95% FTP** (metabolische Ermüdung einplanen)
- KM 150–197: **Auf Gefühl** – Rest des W' kontrolliert verbrennen

---

## 14. Neuromuskuläre Kraft / Sprint-Training für Ausdauerradfahrer

### Hilft Sprint-Training Ausdauerradfahrern?

**Boullosa et al. (2022, Scand J Med Sci Sports):** Meta-Analyse, Sprint-Intervall-Training bei trainierten Radfahrern:
- VO2max +3,2% (KI: +1,2–5,2%)
- Anaerobe Peakleistung +6,4%
- Time-to-Exhaustion VO2max +4,1%
- **Kein Verlust aerober Fitness** – auch nicht wenn parallel HIT-Training

**Fazit:** Sprint-Training verbessert Ausdauerleistung messbar ohne Risiko.

### Mechanismus: Typ-IIx → Typ-IIa Shift

Sprint-Training (maximal, ≥150% FTP) rekrutiert Type-II-Fasern vollständig. Nach 4–6 Wochen: IIx → IIa (höhere oxidative Kapazität, mehr Mitochondrien). Nebeneffekt: bessere Laktatchance und Sauerstoffaufnahme in schnell-zuckenden Fasern.

### Protokoll (Stefan)

| Format | Dauer | Leistung | TSS | Frequenz |
|---|---|---|---|---|
| 6×10s maximal | ~20min gesamt | >180% FTP (>549W) | ~10–15 | 1×/Woche Grundlagenphase |
| 8×30s/20s | ~25min gesamt | 130% FTP (~397W) | ~20–25 | 1–2×/Woche Aufbauphase |

**Platzierung in der Woche:**
- Sprint-Session: Mo oder Do (48h nach/vor nächstem HIT)
- Nie am selben Tag wie VO2max-Block (neuromusk. Interferenz)
- Taper KW23: Sprint-Sessions raus; in KW22 letzte Sprint-Einheit

---

## 15. Übertraining / Non-Functional Overreaching (NFOR)

### Definitionen (Meeusen et al. 2013, ECSS/ACSM Consensus, Med Sci Sports Exerc)

| Zustand | Dauer | Leistungsverlust | Erholung |
|---|---|---|---|
| Functional Overreaching (FOR) | <2 Wochen | Kurz, dann verbessert | 2–10 Tage |
| **Non-Functional Overreaching (NFOR)** | 2–4 Wochen | Anhaltend, trotz Ruhe | 2–4 Wochen |
| Overtraining Syndrome (OTS) | >4 Wochen | Persistierend, ggf. verschlechtert | Monate |

**Für Stefan:** NFOR ist die relevante Bedrohung – nicht OTS. FOR ist erwünscht (Trainingsreiz).

### HRV als Frühindikator (Buchheit & Garvican-Lewis 2016)

- 7-Tage-RMSSD-Rollend sinkt >10%: Aktionsschwelle
- Einzeltag −15%: beobachten, nicht sofort handeln
- 5+ Tage konsekutiv sinkend: Trainingsbelastung −20%

### Mehrdimensionaler Alarm (3 Indikatoren gleichzeitig → sofort handeln)

| Indikator | Normbereich | Alarm |
|---|---|---|
| HRV 7d-Schnitt | Individuell ±5% | >10% unter Baseline |
| Ruhepuls | ~45–52 bpm | +5–7 bpm für 5+ Tage |
| Mood / Motivation | 7–10/10 | <5/10, Lust auf Einheiten fehlt |
| Leistung | Stabile FTP | Unerklärter Einbruch >3% |
| Schlaf | 7–8h, Qualität gut | Frühes Aufwachen + tagsüber müde |

### Präventionsregeln jenseits TSB

1. **Echte Erholungstage**: HF <120 bpm, RPE <4, max. 60min – keine "leichten 2h Runden"
2. **Deload jede 4. Woche**: TSS −40–50%, HIT auf 1× reduzieren
3. **Nie 3 harte Tage in Folge** ohne Erholungstag dazwischen
4. **TSB allein reicht nicht**: TSS-basierte Modelle unterschätzen neuromusk. Ermüdung

---

## 16. Hitzeanpassung (Heat Acclimation) – relevant für Juni-Events

### Kernbefund (Lorenzo et al. 2010, J Appl Physiol)

12 trainierte Radfahrer, 10 Tage Hitzetraining @40°C, getestet in kühler Umgebung (13°C):
- **VO2max +5% (kühle Bedingungen)**, +8% in Hitze
- **TT-Leistung +6%** auch in kühlen 13°C
- **Plasmavolumen +6,5%**, Herzminutenvolumen +9,1%
- Adaptationen halten **14–21 Tage nach Ende der Wärmeexposition**

**Für Stefan:** RadRace + Rosenheimer im Juni (15–25°C); Heat Acclimation verbessert Leistung auch in gemäßigten Temperaturen – entspricht ~+18–24W FTP.

### Protokoll (ohne Klimakammer, praktisch umsetzbar)

| KW | Maßnahme | Dauer | Intensität |
|---|---|---|---|
| KW21–22 | Outdoor Nachmittagsrunden 14–16 Uhr | 40–45min | 50–60% FTP (155–200W) |
| KW22 | 3× Indoor ohne Ventilator | 35–40min | 160–200W |
| KW23 | 2× Indoor/Outdoor warm | 25–30min | Easy, leichte Intensitätsspitzen |
| KW24 | Voll adaptiert | – | – |

**Monitoring:** RHR sollte nach 7–10 Tagen 2–3 bpm sinken. Bei gleicher Leistung sinkendes RPE = gute Adaptation.

---

## 17. Kadenz-Optimierung nach Intensitätszone

*Ergänzung zu Sektion 5 (KA) – gilt auch für normale Intensitätsbereiche*

### Optimale Kadenz nach Zone (Marsh & Martin 1997, Foss & Hallén 2004)

| Zone Stefan | Watt | Zielkadenz | Begründung |
|---|---|---|---|
| Z1 Easy | <188W | 70–80 rpm | Muskuläre Erholung, FatMax |
| Z2 FatMax | 189–212W | 75–85 rpm | Ökonomisch für diese Intensität |
| Z3 Schwelle/SwSp | 213–283W | 85–95 rpm | Natürlich selbst gewählt |
| Z4 FTP | 283–314W | 88–97 rpm | Selbst wählen lassen |
| Z5 VO2max | 315–422W | **100–110 rpm** | **Reduziert Kraft/Pedaltritt → weniger Laktat** |
| Kraft/KA | 91% FTP | **55 rpm** | Maximal-Drehmomentbelastung |

### Warum Z5 bewusst hochkadenzig fahren?

Bei Z5-Leistungen limitiert nicht VO2max sondern muskuläre Erschöpfung (Laktat, H+-Akkumulation). Höhere Kadenz reduziert Kraft pro Pedaltritt → weniger anaerobe Beanspruchung → längere Haltbarkeit der Intensität.

**Umsetzung für Stefan:** HIT-EB 4×4min und 4×6min bewusst auf 105–110 rpm fahren. Erste 2–3 Wochen fühlt sich "spinnig" an, HF +2–3 bpm höher; nach Anpassung normalisiert sich alles.

---

## 18. FTP-Plateau überwinden

### Mechanismus (warum FTP stagniert)

Nach 4–6 Wochen gleichem Trainingsreiz:
- **Peripher**: Mitochondrienenzyme (PGC-1α) maximal hochreguliert → kein weiterer Reiz
- **Zentral**: VO2max-Decke erreicht; kardiale Adaptationen saturieren nach 6–12 Wochen
- **Psychologisch**: Keine neuen Reize → subjektiv "unveränderliche Leistung"

### Plateau-Durchbrecher-Protokoll (4 Wochen)

| Woche | Maßnahme |
|---|---|
| 1 | Intervallformat wechseln: 4×8min @ 320–335W statt 4×4min; Kadenz 105–110 rpm erzwingen |
| 2 | Over-Under einführen: 3×(3min@325W + 3min@265W); LIT-Samstag +30min länger |
| 3 | Gleich; Sprint-Session ergänzen (6×10s maximal); HRV beobachten |
| 4 | Deload: TSS −45%, nur 1× moderate Einheit (25min@260W), Rest LIT |
| 5 | Supercompensation-Fenster: Neues FTP-Test-Format; +2–6W realistisch |

**Checkliste vor Annahme eines echten Plateaus:**

| Check | Frage |
|---|---|
| Test-Konsistenz | Gleiche Strecke, gleiches Gerät, gleiche Tageszeit? |
| Z1 wirklich leicht? | Alle "leichten" Einheiten <210W? |
| HRV stabil? | NFOR ausschließen |
| Fueling ausreichend? | 40–50 kcal/kg/Tag? |
| Intensiv genug? | Z5 wirklich ≥115% FTP (≥350W)? |

---

## Zonen-Referenz: intervals.icu vs. Stefan's Coaching-Zonen

*Praxisreferenz für die Interpretation von Wochendaten aus intervals.icu*

### Problem

intervals.icu (Free Version) verwendet ein 7-Zonen-Modell mit festen Prozentbändern und eigenen Schwelleneinstellungen, die nicht vollständig dem Sentiero-Zonenmodell entsprechen. Beim Lesen des Weekly Review müssen die Zonendaten korrekt interpretiert werden.

### Radfahren: Zonen-Mapping

| intervals.icu Zone | Prozent FTP (305W) | Watt | Sentiero-Entsprechung |
|---|---|---|---|
| Z1 Active Recovery | <55% | <168W | Z0 Recovery |
| Z2 Endurance | 56–75% | 171–229W | Z1 Base + Z2 FatMax |
| Z3 Tempo | 76–90% | 232–275W | Z3 Tempo / MCT-Zone unterer Teil |
| Z4 Threshold | 91–105% | 278–320W | Z3 oberer Teil + Z4 FTP |
| Z5 VO2max | 106–120% | 323–366W | Z5 VO2max |
| Z6 Anaerobic | 121–150% | 369–458W | Z5 + Z6 Anaerob |
| Z7 Neuromuscular | >150% | >458W | Z6 Spitze |

**Zonen-Nummerierung: Sentiero vs. intervals.icu**

Sentiero und intervals.icu verwenden **identische Zonen**, aber unterschiedliche Startnummern:

| Bedeutung | Sentiero | intervals.icu |
|---|---|---|
| Recovery | Z0 | Z1 |
| Base / Easy | Z1 | Z2 |
| FatMax | Z2 | Z3 |
| Tempo / Grauzone | Z3 | Z4 |
| FTP / Schwelle | Z4 | Z5 |
| VO2max | Z5 | Z6 |
| Anaerob | Z6 | Z7 |

**Für Polarisationsmonitor-Auswertung:**
- **LIT** = Sentiero Z0+Z1+Z2 = intervals.icu **Z1+Z2+Z3**
- **Grauzone** = Sentiero Z3 = intervals.icu **Z4** (+ SS) — **nicht HIT, aber vermeiden wenn ungeplant**
- **HIT** = Sentiero Z4+Z5+Z6 = intervals.icu **Z5+Z6+Z7** — ausschließlich diese Zonen

> ⚠️ intervals.icu Z4 niemals als HIT zählen. HIT = nur Z5+Z6+Z7.
> ⚠️ intervals.icu Z3 (= Sentiero Z2 = FatMax) ist LIT, nicht Grauzone.

### Laufen: Zonen-Mapping (Stand: intervals.icu Schwelle 6:03/km)

> **Action:** Stefan sollte in intervals.icu Lauf-Schwellentempo auf **6:03/km** setzen (nicht 5:59).

| intervals.icu Zone | Pace (bei 6:03 Schwelle) | Coaching-Zone |
|---|---|---|
| Z1 (< 77.5%) | > 7:48/km | Z1 Easy ✓ |
| Z2 (78.5–87.7%) | 6:54–7:47/km | Z1 Easy (noch) ✓ |
| Z3 (88.7–94.3%) | 6:26–6:53/km | Z2 Aerob |
| Z4 (95.3–100%) | 6:04–6:25/km | Z3 Schwelle |
| Z5 (101–103.4%) | 5:51–6:03/km | Z3 Schwelle / Übergang |
| Z6 (104.4–111.5%) | 5:26–5:50/km | Z4 VO2max ✓ |
| Z7 (112.5%+) | < 5:25/km | Z4 VO2max ✓ |

**Für Polarisationsmonitor Laufen:**
- **Easy (Z1–Z2 Seiler)** = intervals.icu Z1 + Z2 (beide Easy)
- **Qualitätslauf** = intervals.icu Z4 + Z5 (Schwelle) oder Z6 + Z7 (VO2max)
- **Grauzone vermeiden** = intervals.icu Z3 maximal (6:26–6:53/km ist aerob, noch akzeptabel in Maßen)

### Praktische Empfehlung

1. **intervals.icu Lauf-Schwelle auf 6:03/km setzen** (Einstellungen → Schwellentempo)
2. **intervals.icu Rad-FTP auf 305W prüfen** (sollte korrekt sein)
3. Beim Lesen von Wochendaten: Z1+Z2 = LIT, Z4–Z7 = Qualitätsminuten – Grauzone (Z3) minimal halten

---

*Stand April 2026 · Wissensbasis bis August 2025 · Kein Ersatz für sportmedizinische Beratung*
