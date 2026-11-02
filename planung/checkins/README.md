# Morgen-Check-ins

Ein Eintrag pro Tag von der Routine „Morgen-Check-in“ (`checkin.py`, stündlich 8:20–13:20 Berlin,
sobald COROS die Nacht bestätigt hat und die gestrige Einheit in intervals.icu ist).

- **Datei = KW des bewerteten Tages** (gestern): der Montags-Check-in über den Sonntag steht noch in der
  Vorwochen-Datei, damit die Wochen-Retro ihn sieht.
- **Marker** `<!-- checkin JJJJ-MM-TT -->` vor jedem Eintrag = Datum des Check-ins. Daran erkennt die
  Routine, dass der Tag erledigt ist. Nicht entfernen.
- **Qualität** nur bei Einheiten mit Arbeits-Intervallen (aus `checkin.py` → `gestern.qualitaet`): Soll/Ist je
  Intervall, Erfüllung, Abfall erstes → letztes Intervall + ein Satz Einordnung. Die Wochen-Retro übernimmt das,
  statt die Intervalle neu auszuwerten.
- Planänderungen werden hier nur **vorgeschlagen** und erst nach Stefans „ok“ umgesetzt.

## Format

```
<!-- checkin 2026-11-04 -->
## Mi 4.11.
**Gestern (Di):** SwSp 3×15 🎯 ✅
**Qualität:** 2/3 im Ziel (265–275 W) · 271 ✅ · 268 ✅ · 259 ⬇️ · HF max 165 → 176 (+11) · Leistung −4 % → solider Erstreiz, 3. Block am Limit
**Nacht:** 7,6 h · Score 82 · HRV 51 (Normal 46–54) · RP 56 → Readiness 🟢 82 · TSB −3
**Heute:** SwSp 3×15 🎯 Kern
**Fragen:** 1. … 2. … 3. …
**Stefan:** RPE 6, Beine normal, Mi stressig
**Coach:** Passt. Vorschlag: Kraft B Mi → Do (Ruhetag tauschen) → ✅ umgesetzt 3.11.
```
