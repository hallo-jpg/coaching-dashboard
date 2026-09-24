# Coach-Memory – gelernte Regeln & Korrekturen

*Führende Quelle für alles, was der Coach über Stefan gelernt hat und das nicht aus den Daten ableitbar ist.*
*Gilt in jeder Session – lokal wie in der Claude-App. Stand: 24. September 2026 (bereinigt).*

**Pflegeregel:** Ein Thema = ein Eintrag. Neue Erkenntnis **ersetzt** den bestehenden Eintrag, statt einen
zweiten danebenzustellen. Die Vorgeschichte (wer hat wann was korrigiert) gehört in `COACHING_AKTE.md`,
hier steht nur die gültige Regel + ein Satz Begründung. Offene Fragen stehen ausschließlich in Abschnitt 8.

---

## 1. Steuerung & Physiologie

### ⚠️ Lauf-HF liegt 25–30 bpm über Rad – Easy-Run-Cap nie unter 160
Belegte Easy-Run-Werte 2026: **155–163 bpm bei 7:10–7:35/km**, auch bei CTL 40–48 (6.5. 42min @ 7:30 → 163 ·
20.5. 45min @ 7:30 → 161 · 18.3. 73min @ 7:10 → 156). Die Laufzonen wurden früher dreimal fälschlich aus der
Rad-HFmax abgeleitet – Stefan hat jedes Mal zu Recht widersprochen.
**Anwenden:** Easy-Cap **165**, nie unter 160. Erhöhte Lauf-HF nie als Detraining oder Krankheit deuten. Aus
**einem** Datenpunkt nach ungewohnter Belastung keine Fitnessdiagnose – erst ab 3–4 vergleichbaren Einheiten.

### 🏁 Lauf-Referenz: 10 km in 1:05:08 @ Ø HF 183 (Seelauf 20.9.2026)
6:31/km über 66min, max HF 196, RPE 8, 41% der Zeit über 184 bpm. Alter Bestwert 1:11:28.
**Anwenden:** Ankerpunkt für jede Lauf-Leistungsaussage – kein Trainingslauf mit Confoundern überstimmt ihn.
Daraus gesetzt und **in intervals.icu übernommen**: Schwellenpace **6:28/km**, LTHR **185**, HFmax 205.
HF-Obergrenzen in Rennplänen nie unter 185.
- **Tempozonen intervals.icu (Schwelle 6:28):** Z1 >8:21 · Z2 7:22–8:20 · Z3 6:51–7:21 · Z4 6:28–6:50 ·
  Z5a 6:15–6:27 · Z5b 5:48–6:14 · Z5c <5:47. Unser Z1 Easy (7:25–8:40) = deren Z1+Z2 · unser Z2 Aerob =
  deren Z3 · unser Z3 Schwelle = deren Z4+Z5a · unser Z4 VO2max = deren Z5b+Z5c.
- **HF-Zonen dort (LTHR 185):** Z1 ≤156 · Z2 157–165 · Z3 166–174 · Z4 175–184 · Z5 185–189 · Z6 190–195 · Z7 196–205.

### Rennpace nie aus einem Intervalllauf mit Confoundern ableiten
Vor dem Seelauf leitete der Coach aus 3×7min (mit Trabpausen, ACWR 1,7, TSB −15, 2 Tage nach 5,5h Rad) 6:50/km
ab. Stefan lief 6:31 – der Coach lag 20 sek/km daneben.
**Anwenden:** Aus Intervallen mit Pausen, unter Ermüdung oder nach Fremdbelastung keine Wettkampfpace ableiten.
Nennt Stefan eine ehrgeizigere Zielzeit: nicht kleinrechnen, sondern mit einem **Entscheidungspunkt im Rennen**
absichern (Split + HF bei Halbdistanz). Gate-Schwellen aus Wettkampf-HF ableiten, nicht aus Trainings-LTHR.

### 📊 Readiness-Score (Modell seit 23.9.2026, Stefans Wunsch)
HRV 35 % · Gefühl 25 % · Ruhepuls 20 % · Schlaf 20 %. HRV und RP jeweils **70 % 7-Tage-Schnitt vs.
30-Tage-Normalbereich + 30 % heute**, Schlaf = heute + 3-Nächte-Ø. **TSB zählt nicht** (steht im
Trainingsform-Ring). Warnsignal → Score max. 45 🔴: HRV < −2,5 SD (≈ unter 33) oder RP > +7 bpm über 30-Tage-Ø.
Identische Formel in `generate.py` und MCP `get_readiness_score`.
Grund: Stefans HRV/RP schwanken stark (HRV ±7 ms); das alte Tagesmodell mit TSB zeigte nach jedem Lastblock
gelb/rot, obwohl er erholt war.
**Anwenden:** Tiefer TSB bei grüner Readiness = produktive Ermüdung, kein Grund zu kürzen. Einzelne gelbe Tage
nicht überbewerten – der Trend über 3+ Tage zählt.

### HRV-Einbruch + Krank-Risiko-Flag → erst nach Alkohol fragen
Die HRV-Einbrüche gingen wiederholt auf Alkohol zurück (17.5. JGA · 2.8. HRV 54→34, RP 54→63 nach
Gruppenausfahrt mit Bier); intervals.icu meldete beide Male fälschlich 🔴 Krank-Risiko.
**Anwenden:** Zuerst nach dem Vorabend fragen. Alkoholsuppression klärt sich in 24–48h; bleibt die HRV danach
unten, das Signal *stärker* gewichten. Statt Pauschalpause ein Gate in den Plan: grün HRV ≥45 & RP ≤58 ·
gelb 38–44 gekürzt · rot <38 oder RP >60 Ruhetag. Qualitätseinheiten nie streichen, nur verschieben.

### Zonen-Mapping Rad: intervals.icu ↔ Sentiero
Gleiche Zonen, Sentiero zählt ab Z0 (Offset +1):
- **LIT** = Sentiero Z0+Z1+Z2 = intervals.icu **Z1+Z2+Z3** (Z3 = FatMax = LIT, kein Drift-Signal!)
- **Grauzone** = Sentiero Z3 = intervals.icu **Z4** (+ Sweetspot)
- **HIT** = Sentiero Z4+Z5+Z6 = intervals.icu **Z5+Z6+Z7**

### RPE 7–8 bei HIT/VO2max ist korrekt
Wird Überlastung oder Grauzone erkannt, liegt es am **Gesamtvolumen / fehlender Erholung**, nie an der
Intervallintensität. Formulierung: „Das Gesamtvolumen war zu hoch", nicht „die Einheiten waren zu intensiv".

### Rennwoche: Aktivierung IMMER auf T-1
Nie eigenmächtig auf T-2 oder früher verschieben. Bei Zeitkonflikt an T-1: nachfragen und **kürzen**
(30min statt 1:30h) – den Tag nie ändern.

---

## 2. Wade, Kadenz, Laufstil

### 🦵 Kadenz: Ziel 165–170 im Training, Rückmeldung **nach Gefühl**
- **Ausgangslage:** gewohnt ~140 spm, auch bei Tempo (ein Stilmerkmal). Bei 190 cm / ~94 kg heißt das lange
  Bodenkontaktzeit, Fußaufsatz vor dem Schwerpunkt, hohes Biegemoment auf die Tibia → sehr wahrscheinlich die
  Ursache des Wadenschmerzes am Soleus-Tibia-Übergang (MTSS-Verdacht seit 9.8.2026, schmerzte nur langsam).
- **Belegt:** Training mit bewusster Frequenz 160–163 · Wettkampf 20.9.: **154** über 66min.
  Unter Wettkampfstress driftet die Kadenz ~6 spm unter den Trainingswert → Trainingsziel liegt ~5 spm über dem,
  was im Wettkampf stehen soll. Daher **165–170 im Training**, damit im Wettkampf ~160 steht.
- **Werkzeug (Stefan, 24.9.2026): nach Gefühl** – schneller laufen, bewusst kurze Schritte, hohe Frequenz.
  Kein Metronom, keine Musik, kein Kadenzalarm vorschreiben. Pläne nennen nur die Zielzahl.
- **Anwenden:** In jeder Easy-Einheit ist die Kadenz die Hauptaufgabe, nicht die Pace. Nicht höher als 170
  ansetzen (Zielwert wurde schon zweimal falsch kalibriert). Wenn 165 nach 10min verkrampft wirkt → lieber
  konsequent 160 als verkrampft 170. Im Wettkampf kein Zahlenjagen, aber ein Cue alle 2–3 km („kürzere
  Schritte, Fuß unter den Körper"). Umstellung braucht 6–8 Wochen – wichtigstes Laufprojekt Herbst 2026.

### 🦵 „Langsames Laufen ist orthopädisch teuer" – Stefan hat recht
Spitzenkraft pro Schritt ist langsam zwar niedriger, aber Bodenkontaktzeit und Zeit-unter-Spannung des Soleus
steigen, und Knochenbelastung akkumuliert **hoch potenziert mit Dehnung × Zyklenzahl**. Bei ~140 spm heißt
langsam: maximaler Bremsimpuls, maximales Biegemoment auf die Tibia – deckt sich mit dem Befund.
Gegenmaßnahme ist aber **nicht** „mehr Tempo statt Easy": Tibia- und Achillessehnenlast skalieren mit dem Tempo.
**Die fünf Regeln:** (1) Kein langsames Trotten; Easy = 7:15–7:45/km @ HF 155–165. (2) Kadenz ist in jeder
Easy-Einheit die Hauptaufgabe (nach Gefühl, s.o.). (3) Aerobes Volumen kommt vom Rad. (4) Jeder Lauf hat einen
Zweck – keine Füllkilometer. (5) 2×/Woche Lauf-Athletik 15min, nicht optional.
Nie wieder mit „Spitzenkraft ist langsam niedriger" argumentieren – das ist die widerlegte Fassung.

### Stefan läuft ohne Auto-Lap – Rennpläne nicht auf km-Piepser bauen
Ohne Lap-Druck ist Rundenzeit = Gesamtzeit. Die Uhr misst auf Kursen typisch 1–2 % zu lang.
**Anwenden:** Checkpoints an die **km-Schilder der Strecke** hängen, dort Zeit gegen Soll-Splittabelle prüfen.
Zielkontrolle immer über Zeit am Schild, nie über Ø Pace oder Uhr-Distanz.

---

## 3. Wochenstruktur & Verfügbarkeit

### Zeitrahmen Winter 26/27 (Stefan, 21.9.2026)
- **Werktags max. 90min** (Ausnahme bis 2h), vor **oder** nach der Arbeit – Slot wird je Woche festgelegt.
- **Wochenende trägt die langen Einheiten.** **Ruhetag immer unter der Woche.** **5–6 Trainingstage.**
- Detailplanung **rollierend 1–2 Wochen im Voraus**, weiter hinten nur Blockstruktur (Stubs).
- Nov–Feb ist faktisch Rolle, auch die langen Wochenendeinheiten.

### 🎯 Kern-Einheiten statt TSS-Quote (Stefan, 24.9.2026)
Jede Woche hat **3 Kern-Einheiten**, der Rest ist ausdrücklich flexibel:
1. **Rad-Qualität** (Standard Di)
2. **Lauf-Qualität** (Standard Fr) – bis KW44 ist das der Easy-Lauf mit Kadenz-Fokus + Athletik
3. **Eine lange Einheit am Wochenende** – Sa **oder** So, Rad oder Lauf, egal welche
Im Wochenplan in der Notiz-Spalte mit **`🎯 Kern`** markieren – **das macht immer der Coach**, in jedem Wochenplan
und bei jeder Umplanung (Stefan, 24.9.: „dafür habe ich ja dich“). Stefan markiert nichts selbst und wird nicht
gefragt, welche Einheit Kern ist – der Coach entscheidet nach den drei Regeln und nennt es im Output. Fällt eine Kern-Einheit aus → **verschieben**,
nicht streichen. Fällt eine flexible Einheit aus → ersatzlos.
**Warum:** Plan und Ist weichen regelmäßig ab (KW38 Di 1h geplant / 2:16h gefahren, KW39 75 → 255 TSS,
KW31/32 an den Wochenenden gescheitert). Das ist Information, kein Fehlverhalten – bewertet wird, ob der Kern
steht, nicht wie nah die TSS-Summe am Plan liegt.

---

## 4. Kommunikation & Selbstbild

### HIT/VO2max nie als „Neuland" bezeichnen
Stefan hat 2025 den Ötztaler absolviert, mit intensivem HIT-Training indoor und outdoor. Intensität als
Progression beschreiben, auf Augenhöhe.

### Rad→Lauf-Transfer: die Lücke ist Volumen, nicht Talent
Rad-VO2max ≈ 48–50 ml/kg/min · Renn-VO2 beim 10km ≈ 31–35 → er lief mit 62–73% seiner Radkapazität.
2026: 40 Läufe, ~250 km = **6,5 km/Woche**, längster Lauf vor dem Rennen 6,9 km (Rechenweg: Akte, 20.9.2026).
Ursachen in dieser Reihenfolge: **1. Lauf-Volumen/Durability · 2. Körpergewicht · 3. Ökonomie/Kadenz (3–6%)**.
**Anwenden:** Nie bestätigen, dass Ökonomie „das Problem" ist, nie als Talentfrage rahmen. Mit der Volumenzahl
antworten. Zielkorridor bei 25–40 km/Woche über 6–12 Monate: 5:45–6:05/km (57:30–61:00).

### Realitätscheck statt Zuspruch
Nach ernüchternden Einheiten (Auslöser meist hohe absolute HF bei moderater Leistung) will Stefan einen
**Realitätscheck, keinen Zuspruch**.
**Anwenden:** Mit Langzeitzahlen aus `athlete/fortschritt.md` antworten (FTP 271W 11/2023 → 305–317W 2026,
VO2max 59, Ötztaler). HF als **HFmax-Frage** reframen. Confounder benennen (nüchtern, nach Pause, nach langer
Radtour) statt Fitness zu diagnostizieren. Lauf-Fortschritt nur über den standardisierten HF-160-Check.

### Gewicht
- **Quelle:** intervals.icu-Wellness, nie nachfragen. `get_current_fitness` liefert `Gewicht_schnitt_30d_kg`.
  Ab **0,5 kg** Abweichung vom Profilwert: Gewicht + W/kg in `profil.md`, `fortschritt.md`, `CLAUDE.md`
  nachziehen, eine Zeile im Output, Akte-Eintrag. Nie einen Tageswert übernehmen. Ohne Messung in 30 Tagen
  bleibt der alte Wert.
- **Kommunikation (Stefan, 20.9.2026):** sachlich erwähnen, wenn es für die Sache zählt (Leistungsanalysen,
  Pace-Prognosen, W/kg, deutlicher Trend über Wochen) – als eine Variable unter mehreren, mit Größenordnung
  statt Wertung. **Nicht:** bewerten, Ernährungstipps ohne Frage, Zielgewicht vorgeben, in jeder Planung
  wiederholen. Ein Hinweis pro Anlass, kein Nachfassen.
- **Stefans eigene Einordnung (21.9.2026):** „ggf. Richtung 90 kg, weniger nicht. Auf 190 cm ist das eine gute
  Basis." 90 kg ist **seine** Untergrenze, kein Coach-Ziel. Größenordnung bei Bedarf: 93,6 → 90 kg ≈ 1–1,5 min
  auf 10 km. Thema ist besprochen.

---

## 5. Arbeitsweise des Coaches

### ⛔ Nicht entscheiden, wenn Fakten fehlen – fragen (Stefan, 21.9.2026)
Der Coach hat aus einer Annahme über den ERG-Modus eine Planregel gemacht und in vier Dateien geschrieben –
Stefan fährt 30/30er seit Jahren auf der Rolle.
**Anwenden:** Bei Ausstattung, Gewohnheiten, Praxis (was funktioniert, was er fährt, wie er aufzeichnet)
**fragen, nicht beschließen**, auch wenn es plausibel klingt. Richtungsweisende Punkte gehen **vor** dem
Schreiben als Frage raus. Fachliche Einschätzungen bleiben erlaubt – als Vorschlag mit Begründung.

### Datum immer per `date` prüfen
Am 20.4.2026 wurde ein Montag als Sonntag angenommen → 10 Workouts neu angelegt.
**Immer** `date "+%A, %d. %B %Y – KW%V"` als erste Aktion; CLAUDE.md-Daten sind nie Tagesquelle.

### Am Ende jeder Planung committen und pushen – direkt auf `main`
Ohne Erinnerung: `git add` → `git commit` → `git pull --rebase` → `git push` auf `main`. Das Dashboard liest
aus `main`; alles andere ist für Stefan unsichtbar.

### Strava-Aktivitäten sind über die API leer
Nur über Strava importierte Aktivitäten liefern über die API alle Felder `null` (Lizenz). COROS/Garmin sind
vollständig. Leere Aktivitätszeilen als „Strava-Hülle" erkennen, nicht als fehlende Einheit.

---

## 6. Ausstattung & Setup

### Geräte
| Zweck | Gerät |
|---|---|
| Lauf | **COROS Pace 3** · Auto-Lap aus · 2 Paar Laufschuhe im Wechsel, je ~200 km (Stand 21.9.) |
| Rad outdoor | **S-Works Tarmac SL8** · Cybrei-Kurbel · **XCadey Spindle** = Referenz-Powermeter |
| Radcomputer | **COROS DURA** (kein Wahoo, der ELEMNT ROAM ist weg – **nie wieder vorschlagen**) |
| Rad indoor | **Canyon Aeroad ohne Powermeter und ohne Schaltung** auf **Tacx Flux S** → immer ERG |
| Indoor-App | **Tacx-App** bevorzugt, MyWhoosh alternativ · max. 4h am Stück · kein Laufband |
| Kraft | nur Eigengewicht + Widerstandsbänder, kein Kraftraum |

### Indoor: ERG ist kein Einschränkungsgrund
Stefan fährt seit Jahren alle strukturierten Formate in ERG, **30/30er inklusive**. Keine Sonderregeln für
Indoor-Formate. KA bei 55 rpm geht in ERG. Vor Indoor-Qualität: 10min warmfahren + Spindown in der Tacx-App.

### Zwei Radleistungsquellen – nie gegeneinander rechnen
Outdoor = Tarmac + XCadey · Indoor = Aeroad auf Tacx (Rollenleistung). Realistisch 5–15% Versatz
(Antriebsstrang, Rollen-Toleranz ±3%, Sitzposition). Fortschritt immer Quelle gegen sich selbst.
**Bis zum Baseline-Test:** alte Zonen **FTP 305** als Wattvorgabe (Stefan: „Als ob irgendwas passiert, wenn
ich 20 Watt zu viel trete."). Keine Doppelkorridore, keine Messversatz-Diskussion in Workouts – aber nie ganz
ohne Wattvorgabe planen.

### 🔬 FTP-Test-Setup (entschieden, Stefan 24.9.2026)
**Tarmac mit XCadey auf den Flux.** Aufzeichnung parallel: **XCadey → COROS DURA** (maßgeblich) und
**Rolle → Tacx-App**. **Kein ERG-Modus** (Ausbelastung unmöglich) – Level-/Standardmodus, geschaltet wird am
Tarmac. Ergebnis aus einer Einheit:
- **FTP = XCadey-10min-Ø × 0,90** (Sentiero 3+10min)
- **Offset-Faktor = Tacx ÷ XCadey** – aus den All-Outs und zusätzlich aus den Stufen des progressiven
  Warmfahrens (zeigt, ob der Versatz mit der Intensität schwankt). Gilt dann für die Aeroad-Einheiten.
- **Doppelzählung vermeiden:** Tacx-Datei in intervals.icu löschen oder von der Belastung ausnehmen.
- Danach neue FTP **überall** setzen: intervals.icu (305), **Garmin Connect (steht auf 325)**, COROS, MyWhoosh.

### Workout-Zustellung (verifiziert 21.9.2026)
intervals.icu → **Garmin Connect → Tacx-App** (Schritte, Balkengrafik, Startknopf kommen an) und
intervals.icu → **COROS** (Pace 3, DURA). Regeln daraus:
1. **Keine Emojis in intervals.icu-Workoutnamen** (Tacx zeigt `������`). Umlaute, `×`, `–` gehen.
   Emojis nur in `planung/kw*.md`.
2. **Nur Zeile 1 der Description kommt in der Tacx-App an** → dort steht die Steueranweisung.
3. **Absolute Watt in Zeile 1**, kurz, ohne Erklärbär.

### intervals.icu-Workouts: Fallen
- **`workout_steps` kann keine Leistungskorridore** – `power_pct_low/high` wird zu einem festen Wert
  (verifiziert: 56–68% → 55%). **Korridor ist Standard, überall** (Stefan, 21.9.2026) → dafür die
  **Description-Route** (`- 70m 52-69%`). `workout_doc` bleibt dann leer, bis Stefan das Workout **einmal in
  intervals.icu öffnet** – Hinweis dazu in die Beschreibung.
- **`workout_steps`** rundet auf ganze Minuten (20s → weg, 30/45s → 60s) → nur für Einheiten ohne Schritte <1min.
- **Strides/Antritte** über die Description-Route (`- 20s 120% Pace` gültig). Nie auf 60s strecken.
- **Distanzen:** `m` heißt in intervals.icu **Minuten** → Distanz immer in km (`0.4km`) bzw. `distance_m`.
  Freitext nie mit `- ` beginnen (wird als Schritt geparst) → `·` benutzen.
- `pace_pct` = % der Schwellen*geschwindigkeit*, **388 s/km (6:28) = 100%**: 75–87% = 8:40–7:25 (Easy),
  105% = 6:10, 119% = 5:25.
- Nach jedem Anlegen `get_planned_events` prüfen (`workout_doc.steps`, `moving_time`), bevor „fertig" gemeldet wird.
- Rad-Bibliothek: `.zwo` nur für `type: "Ride"`; Dateinamen exakt aus `planung/workout_index.md`.

---

## 7. Erledigte Rahmenentscheidungen – nicht erneut aufmachen

| Thema | Stand |
|---|---|
| **Events** | „**aktuell keine geplant**" (Stefans Formulierung) – es wird etwas kommen. Nicht danach suchen, nicht nachfassen; ein genanntes Event sofort in `athlete/profil.md` eintragen. Benchmarks bis dahin als eigene Zeitläufe auf Standardstrecke. |
| **Kraft** | Lauf-Athletik **2×15min Pflicht** und aktiv einplanen · Ganzkörper 1× optional · KA auf der Rolle bleibt der Kraftreiz fürs Rad (Bänder ersetzen das nicht – so auch sagen) |
| **Laufschuhe** | zwei Paar, reichlich Reserve – nicht ungefragt ansprechen |
| **Vitamin D** | Messung von Stefan verneint – erledigt |
| **Infekt-Muster** | keins erkennbar → nur strukturelle Prävention (Entlastungswochen, HRV-Gate, Reise-/Schlafregel, Fueling, Alkohol), Protokoll in `planung/langfristplan.md` |
| **Wade/Nacken-Tracking** | kein eigenes Wellness-Feld gewünscht (24.9.2026) – Stefan meldet Beschwerden selbst; bei Laufeinheiten die Abbruchregeln im Plan nennen |
| **Nacken** | Halswirbelfraktur 28.6. ausgeheilt (66min Wettkampf beschwerdefrei). Abbruchkriterien bleiben Standard: Nackenschmerz, Kopfschmerz, Ausstrahlung/Kribbeln in die Arme |
| **Rad:Lauf-Split** | dynamisch: Okt 70:30 → Nov 65:35 → ab Dez 60:40. Argument, das gezogen hat: die 7. Radstunde bringt fast nichts, die 3,5. Laufstunde entscheidet über sub-60 |
| **Rampe** | Ausgangslage ~3,2h/Woche → 9–10h. Die Rampe (+10–15%/Woche, jede 4. Woche −45%) ist wichtiger als der Zielwert |

---

## 8. Offene Punkte (nur hier führen)

- **ERG + Korridor:** Hält die Rolle bei einem Wattbereich den Mittelwert oder rampt sie über das Intervall
  hoch? Stefan schaut bei der ersten ERG-Einheit aufs Display. Rampt sie → Indoor-Einheiten auf feste Zielwerte,
  outdoor bleibt Korridor.
