# Coach-Memory – gelernte Regeln & Korrekturen

*Führende Quelle für alles, was der Coach über Stefan gelernt hat und das nicht aus den Daten ableitbar ist.*
*Gilt in jeder Session – lokal wie in der Claude-App. Bei neuen Erkenntnissen oder Korrekturen hier ergänzen, nicht nur im Chat bestätigen.*
*Stand: 20. September 2026*

---

## 1. Steuerung & Physiologie

### ⚠️ Lauf-HF liegt 25–30 bpm über Rad – Easy-Run-Cap nie unter 160
Belegte Easy-Run-Werte über die ganze Saison 2026: **155–163 bpm bei 7:10–7:35/km**, auch bei voller Fitness (CTL 40–48). Beispiele: 6.5. 42min @ 7:30 → 163 · 20.5. 45min @ 7:30 → 161 · 18.3. 73min @ 7:10 → 156.
**Warum:** Die Laufzonen in `athlete/profil.md` waren ursprünglich von der Rad-HFmax (205) abgeleitet (Z1 = 123–148) – dafür müsste Stefan gehen. Der Fehler wurde dreimal gemacht (KW18, KW19, 26.7.), Stefan hat jedes Mal widersprochen, die Daten geben ihm recht.
**Anwenden:** Easy-Run-Cap Standard **165**, nie unter 160. Fortschrittsmesser: „Pace bei HF 160" (Referenz 7:30/km @ 163 bei CTL 40). Erhöhte Lauf-HF **nie** als Detraining oder Krankheit deuten, ohne die Belegtabelle im Profil zu prüfen. Aus **einem** Datenpunkt nach ungewohnter Belastung keine Fitnessdiagnose – erst ab 3–4 vergleichbaren Einheiten.

### 🏁 Wettkampf-Referenz Laufen (20.9.2026): 10km in 1:05:08 @ Ø HF 183
Karlsfelder Seelauf, erster echter 10-km-Wettkampf: **6:31/km über 66min**, Ø HF **183**, max **196**, RPE 8 — 48% der Zeit in 164–184 bpm, **41% über 184 bpm**. Vorheriger 10-km-Bestwert 1:11:28 (Trainingslauf).
**Anwenden:** Das ist ab jetzt der Ankerpunkt für jede Lauf-Leistungsaussage — kein Trainingslauf mit Confoundern kann ihn überstimmen. Lauf-LTHR liegt real bei **183–185** (gespeichert: 179), Lauf-HFmax deutlich über 196. HF-Obergrenzen in Rennplänen nie unter 185 ansetzen. **Umgesetzt am 20.09.2026:** Schwellenpace **6:03 → 6:28/km**, LTHR **179 → 185** (Quelle LTHR: TrainingPeaks-Auto-Erkennung nach dem Seelauf, von Stefan freigegeben). Laufzonen in `athlete/profil.md`, `generate.py` und die Pacebänder im Coach-Skill sind darauf umgestellt.
**Offen — nur Stefan kann das:** dieselben Werte in **intervals.icu** hinterlegen (Settings → Sport Settings → Run: Threshold Pace 6:28/km, LTHR 185). Bis dahin rechnet intervals.icu rTSS, Zonenverteilung und die `pace_pct`-Ziele geplanter Workouts weiter gegen 6:03/km — geplante Läufe wären dann ~25 sek/km zu schnell. **Vor dem nächsten Anlegen von Lauf-Workouts prüfen und ggf. nachfragen.**

### Rennpace nie aus einem Intervalllauf mit Confoundern ableiten
Vor dem Seelauf leitete der Coach aus 3×7min vom 9.9. eine Rennpace von 6:50/km ab (Prognose 68:20). Stefan entschied sich gegen diese Ableitung für 6:30–6:40 und lief **6:31** — der Coach lag 20 sek/km daneben. Der Ableitungs-Datenpunkt war ein Intervalllauf **mit Trabpausen**, bei ACWR 1,7 und TSB −15, zwei Tage nach 5,5h Rad.
**Anwenden:** Aus Intervallen mit Pausen, unter Ermüdung oder nach Fremdbelastung wird **keine** Wettkampfpace abgeleitet. Wenn Stefan eine eigene Zielzeit nennt, die über der Coach-Schätzung liegt: nicht kleinrechnen, sondern **mit einem Entscheidungspunkt im Rennen absichern** (Split- und HF-Check bei Halbdistanz) — das hat hier funktioniert. Gate-Schwellen dabei aus Wettkampf-HF ableiten, nicht aus Trainings-LTHR: das km-5-Gate ">182 → langsamer" war zu eng und hätte das Rennen gebremst.

### HRV-Einbruch + Krank-Risiko-Flag → erst nach Alkohol fragen
Stefans HRV-Einbrüche gingen wiederholt auf Alkohol zurück, nicht auf Training oder Infekt (17.5. JGA · 2.8. HRV 54→34, Ruhepuls 54→63 nach Gruppenausfahrt mit Bier). Beide Male meldete intervals.icu fälschlich 🔴 Krank-Risiko.
**Anwenden:** Bei HRV-Einbruch mit Krank-Flag zuerst nach dem Vorabend fragen – besonders nach Wochenende, sozialem Anlass, Gruppenausfahrt. Alkoholsuppression klärt sich in 24–48h; bleibt die HRV danach unten, ist das Signal *stärker* zu gewichten. Statt Pauschalpause ein Gate in den Plan: grün HRV ≥45 & RP ≤58 · gelb 38–44 gekürzt · rot <38 oder RP >60 Ruhetag. Qualitätseinheiten nie streichen, nur verschieben.

### Zonen-Mapping intervals.icu ↔ Sentiero
Gleiche Zonen, andere Nummerierung (Sentiero ab Z0, intervals.icu ab Z1 → Offset +1):
- **LIT** = Sentiero Z0+Z1+Z2 = intervals.icu **Z1+Z2+Z3** (Z3 = FatMax = LIT, kein Drift-Signal!)
- **Grauzone** = Sentiero Z3 = intervals.icu **Z4** (+ Sweetspot)
- **HIT** = Sentiero Z4+Z5+Z6 = intervals.icu **Z5+Z6+Z7**
Fehler entstanden durch Verwechslung von Watt-Grenzen mit Zonennummern.

### RPE 7–8 bei HIT/VO2max ist korrekt
Stefan hat explizit korrigiert (KW18 Retro): Berg-HIT mit RPE 7–8 ist genau richtig. Wenn Überlastung oder Grauzone erkannt wird, liegt es am **Gesamtvolumen / fehlender Erholung**, nie an der Intervallintensität. Formulierung: „Das Gesamtvolumen war zu hoch", nicht „die Einheiten waren zu intensiv".

### Rennwoche: Aktivierung IMMER auf T-1
Nie eigenmächtig auf T-2 oder früher verschieben, auch wenn Stefan an T-1 keinen Slot nennt. Neuromuskuläres Priming wirkt 24h vor Start, nicht 48h. Bei Zeitkonflikt an T-1: nachfragen, **kürzen** (30min statt 1:30h) – den Tag nie ändern.

---

## 2. Wade, Kadenz, Laufstil

### 🦵 Kadenz ~140 spm ist die Ursache – Arbeitsziel 155–165
Stefans gewohnte Laufkadenz liegt bei **~140 spm, auch bei Tempo** (bestätigt 6.9.: 140 bei 7:47/km *und* bei ~6:15/km – ein Stilmerkmal, kein Artefakt). Bei 91 kg heißt das lange Bodenkontaktzeit, Fußaufsatz vor dem Schwerpunkt, hohes Biegemoment auf die Tibia → mit hoher Wahrscheinlichkeit **die** Ursache des Wadenschmerzes am Soleus-Tibia-Übergang (MTSS-Verdacht ab 9.8.2026; tat nur beim *langsamen* Laufen weh). Mit Konzentration erreichte er am 6.9. Ø 161 / max 179, Wade beschwerdefrei.
**Anwenden:** Arbeitsziel **155–165** (Metronom 160), nach dem Seelauf konsolidieren auf 165–170. Nicht höher ansetzen – der Zielwert wurde zweimal falsch kalibriert (170–175 auf Schätzung; 165–170 mit den 161 als vermeintlicher Basis). Bei jeder Easy-Einheit ist die Kadenz die Hauptaufgabe, nicht die Pace. Wenn 160 nach 10min unnatürlich bleibt → 155, lieber konsequent 155 als verkrampft 165. Im Wettkampf kein Zahlenjagen, aber ein Cue alle 2–3 km („kürzere Schritte, Fuß unter den Körper") – dort ist Kadenz Verletzungsschutz. Die Umstellung 140 → stabile 165–170 braucht 6–8 Wochen und ist das **wichtigste Laufprojekt nach dem Zielrennen**.

### Stefan läuft ohne Auto-Lap – Rennpläne nicht auf km-Piepser bauen
Auto-Lap ist auf der COROS **aus**. Ohne Lap-Druck läuft eine einzige Runde über die
gesamte Einheit, dadurch gilt: **Rundenzeit = Gesamtzeit**, Ø Pace der Runde = Ø Pace
gesamt. Ein Zeitfeld extra braucht es also nicht.
**Anwenden:** Checkpoints in Rennplänen nie an einen automatischen km-Piepser hängen,
sondern an die **km-Schilder der Strecke** – dort Rundenzeit gegen die Soll-Splittabelle
prüfen. Das ist ohnehin genauer: die Uhr misst auf dem Kurs typisch **1–2 % zu lang**
(keine Ideallinie, GPS-Rauschen), auf 10 km also 100–200 m. Folge: Uhr-Distanz läuft dem
Schild voraus und die angezeigte Ø Pace liegt über der offiziellen. Zielkontrolle
deshalb immer über Zeit am Schild, nie über Ø Pace oder Uhr-Distanz.

---

## 3. Wochenstruktur & Verfügbarkeit

### Lauf-Block (seit KW33): Kern Mo/Mi/Fr früh, Wochenende nur Bonus
KW31 und KW32 sind **beide am Wochenende gescheitert** (Hitze, private Termine, spontane Radausfahrt) – der Longrun und zweimal der 2km-Kalibrierungscheck fielen aus. Werktags früh hat zuverlässig funktioniert.
**Anwenden:** Im Lauf-Block Schlüsseleinheiten nie aufs Wochenende legen; Sa/So als „Bonus – ersatzlos streichbar" kennzeichnen. Im Sommer: früh morgens erste Wahl, spät abends zweite.
**Rad-Regel (gilt wieder bei Rad-Fokus):** Ruhetag immer unter der Woche, Wochenende beide Tage Training (lange Ausfahrten). Vollzeit berufstätig: wochentags max. 2h, Wochenende 2,5–4h.

---

## 4. Kommunikation & Selbstbild

### HIT/VO2max nie als „Neuland" bezeichnen
Stefan hat 2025 den Ötztaler Radmarathon absolviert, mit intensivem HIT/VO2max-Training indoor und outdoor. Formulierungen wie „neues Terrain" oder „wenig Erfahrung" fühlen sich für ihn falsch und herabsetzend an. Intensität als Progression beschreiben, auf Augenhöhe.

### Realitätscheck statt Zuspruch
Nach einzelnen ernüchternden Einheiten (z.B. 14.9., T-6) äußert Stefan das Gefühl, „seit Jahren keinen Fortschritt" zu machen und „schwach" zu sein. Auslöser fast immer: hohe absolute HF bei moderater Leistung. Er will dann explizit einen **Realitätscheck, keinen Zuspruch**.
**Anwenden:** Mit Langzeitzahlen aus `athlete/fortschritt.md` antworten (FTP 271W/2,8 W/kg 11/2023 → 305–317W/3,35–3,6 W/kg 2026, VO2max 59, Ötztaler). HF-Vergleich als **HFmax-Frage** reframen (Rad 202 beobachtet, Lauf vermutlich 210+ → absolute HF höher als bei anderen, relativ normal). Auf fehlende vergleichbare Datenpunkte hinweisen (Confounder: nüchtern, nach Pause, nach langer Radtour) statt Fitness zu diagnostizieren. Lauf-Fortschritt nur über standardisierten Check: gleiche Strecke, morgens, gefrühstückt, ≥48h nach harter Einheit, 30min @ HF 160 → Pace.

---

## 5. Arbeitsweise des Coaches

### Datum immer per `date` prüfen
Am 20.4.2026 wurde der 20. April als Sonntag angenommen, weil CLAUDE.md „KW16 = 14.–20. April" zeigte – er war ein Montag. 10 Workouts mussten gelöscht und neu angelegt werden. **Immer** `date "+%A, %d. %B %Y – KW%V"` als erste Aktion; CLAUDE.md-Datumsangaben sind Orientierung, nie Tagesquelle.

### Am Ende jeder Planung committen und pushen
Ohne Erinnerung durch Stefan: `git add` → `git commit` → `git pull --rebase` → `git push` auf `main`. Das Dashboard liest aus dem Repo; lokal geschriebene Dateien sind bis zum Push unsichtbar – auch für die nächste Session am Handy.

### intervals.icu-Workouts: zwei Wege, zwei Fallen
- **`workout_steps`** rundet auf ganze Minuten: 20s → verworfen, 30s/45s → 60s. Nur für Einheiten ohne Schritte <1min.
- **Description-Route** (Schrittliste als Text am Ende der `description`, `- 20s 120% Pace` gültig) für Strides/Antritte. `workout_doc` bleibt dabei leer – **Stefan muss das Workout einmal öffnen und OK klicken**, Hinweis oben in die Beschreibung.
- Strides nie auf 60s strecken, um Weg A zu erzwingen (ab ~40s kippt der Reiz von neuromuskulär zu anaerob).
- `pace_pct` = % der Schwellen*geschwindigkeit* — **seit 20.09.2026: 388s/km (6:28) = 100%** (vorher 363s/km): 55% = 11:45 (Gehen), 75–87% = 8:40–7:25 (Easy), 100% = 6:28, 105% = 6:10, 119% = 5:25. Gilt nur, wenn die Schwellenpace **in intervals.icu** ebenfalls auf 6:28 steht.
- Nach jedem Anlegen `get_planned_events` prüfen (`workout_doc.steps`, `moving_time`), bevor „fertig" gemeldet wird.
- Rad-Bibliothek: `.zwo` nur für `type: "Ride"`; Dateinamen exakt aus `planung/workout_index.md`.

### Strava-Aktivitäten sind über die API leer
Aktivitäten, die nur über Strava in intervals.icu ankommen, liefern über die API (MCP, Dashboard) **alle Felder `null`** – Strava-Lizenz. In der intervals.icu-Oberfläche sind sie sichtbar, für den Coach nicht. COROS- und Garmin-Quellen sind vollständig. Leere Aktivitätszeilen daher als „Strava-Hülle" erkennen, nicht als fehlende Einheit.

---

## 6. Aktueller Kontext (Stand 19.9.2026)

- **Halswirbelfraktur 28.6.2026** (Rosenheimer, km 45,8) → 4 Wochen Pause, seit 26.7. Wiedereinstieg mit ärztlicher Freigabe für Laufen und Rad. Nacken-Abbruchkriterien bei jeder Einheit: Nackenschmerz, Kopfschmerz, Ausstrahlung/Kribbeln in die Arme.
- **Rad-Setup neu seit Sept. 2026:** Outdoor S-Works Tarmac SL8 · Cybrei-Kurbel · XCadey Spindle-Powermeter. Indoor altes Canyon Aeroad ohne PM auf Tacx Flux S → Rollenleistung ist Indoor-Quelle. **FTP 305W stammt vom alten 4iiii-Setup** → Rad-Zonen erst nach neuem 3+10min-Test am Tarmac wieder trainingsleitend; bis dahin Rad nach HF/RPE. Indoor- und Outdoor-Watt nie gleichsetzen.
- **Zielevent erreicht:** Karlsfelder Seelauf 10km am 20.9.2026 — **1:05:08 / 6:31/km**, Ziel (6:30–6:40) getroffen, PR von 1:11:28 um 6:20 verbessert. Saison-Zielrennen abgeschlossen.
- **KW39:** Stefan in Kroatien, Mo/Di Arbeit, Mi–Fr Urlaub, Planung im Laufe der Woche. Recovery nach dem Rennen: Mo/Di Pause, erste lockere Einheit frühestens Mi.
- **Danach:** KW40 FTP-Herbsttest (Sentiero 3+10min, **erster Test am Tarmac/XCadey**) → danach Neuaufbau mit dem Kadenz-Projekt als wichtigstem Laufthema. Kein neues Zielrennen gesetzt — bei der nächsten Planung nach Events für Herbst/Winter fragen.
