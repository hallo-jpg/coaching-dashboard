# Modul: Krank-Modus

*Geladen aus `SKILL.md`, sobald das Briefing auf Krankheit hindeutet („krank", „Fieber", „Erkältung",
„Halsweh", „Grippe", „fühle mich nicht gut"). Ersetzt den normalen Ablauf – nur `date`, `COACH_MEMORY.md`,
`planung/kw[N].md` und `get_readiness_score` vorher.*

⚠️ **Vorher prüfen (COACH_MEMORY):** Kommt der Hinweis nur aus einem HRV-Einbruch / Krank-Risiko-Flag ohne
Symptome → zuerst nach Alkohol am Vorabend fragen, nicht den Krank-Modus starten.

## Interview – alle drei Fragen in einer Nachricht

```
Verstanden – ich passe den Plan an. Drei kurze Fragen:
1. Seit wann? (Tag 1 = heute begonnen)
2. Fieber? (ja + Temperatur / nein)
3. Symptome unterhalb des Halses – Husten, Brustenge, Gliederschmerzen? (ja / nein)
```

## Rückkehr-Logik

1. **Fieber** → erst fieberfrei + 24h, dann weiter mit 2.
2. **Neck-Check:** nur oberhalb des Halses → symptomfrei + 24h → LIT möglich ·
   unterhalb des Halses → symptomfrei + 48h Spaziergang, + 72h LIT.
3. Restdauer schätzen: Tag 1–2 → noch ~3–5 Tage · Tag 3+ → noch ~2–3 Tage.
   `Rückkehrtag = heute + Restdauer + Wartefrist`.

## Rampe ab Rückkehrtag

| Tag | Einheit |
|---|---|
| +0 | Spaziergang / Mobilität ≤ 30 min |
| +1 | **Rad** LIT 45 min, HF-Deckel im Workout-Namen (< 148 bpm = 72% HFmax) · **kein Laufen** |
| +2 | Rad LIT 60 min, normale Wattvorgabe |
| +3–4 | normales LIT-Programm · erster Easy-Lauf frühestens +3 (HF-Cap 165 wie immer) |
| +5+ | volle Last, erste Qualität nur bei Readiness ≥ 70 |

Rückkehr läuft über das Rad (kein Impact). Keine Kompensation verlorener Einheiten, Kern-Einheiten der
Ausfallwoche verfallen (nicht nachholen). Ein Block wird nicht verlängert – jeder 3-Wochen-Block hat seinen
eigenen Abschluss (periodisierung.md).

## Dateien

1. `planung/kw[N].md`: Einheiten bis zum Tag vor Rückkehr → Status `❌` + Notiz „krank", TSS Ist 0 · Resttage
   durch die Rampe ersetzen · Total-Zeile bleibt (Parser!), TSS-Wert an die Rampe anpassen · darunter
   `> **Krankheitswoche** – Rückkehrtag [Datum], Rampe bis [Datum +5].`
2. Geplante intervals.icu-Workouts der Ausfalltage mit `delete_event` löschen, Rampe neu anlegen.
3. `COACHING_AKTE.md` (oben): `## [Datum] – Krankheit KW[N]` · Beginn · ober-/unterhalb Hals · Fieber ·
   Rückkehrtag · ausgefallene Tage · „Folgewoche: ~50% TSS, nur LIT".
4. `python3 validate_plans.py` → commit + push.

Liegt ein Event < 21 Tage entfernt: „Lieber 1 Tag länger Pause – verlorene CTL wird nicht kompensiert."

## Output

```
🤒 Krank-Modus
Rückkehr: [Datum] (LIT ab +1) · volle Last ab [Datum +5]
[angepasste Wochentabelle]
Nächste Woche plane ich mit ~50% TSS und nur LIT.
```
