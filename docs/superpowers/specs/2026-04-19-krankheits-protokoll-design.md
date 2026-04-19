# Krankheits-Protokoll Design

**Ziel:** Wenn Stefan "ich bin krank" meldet, führt der Coach ein kurzes Symptom-Interview durch, berechnet das Rückkehrdatum und passt den laufenden Wochenplan an. Keine Diagnose — nur Coaching-Entscheidungen.

**Architektur:** Neuer `krank`-Modus in der Modus-Erkennung von `.claude/skills/coach/SKILL.md`. Eigener Abschnitt "Schritt K" (Krank-Modus), der bei Trigger-Wörtern statt des normalen Planungs-Ablaufs ausgeführt wird.

**Tech Stack:** Markdown-Edits an SKILL.md; schreibt in `planung/kw[N].md` und `COACHING_AKTE.md`.

---

## Trigger

Wörter im Aufruf: "krank", "Fieber", "Erkältung", "fühle mich nicht gut", "bin krank", "Halsweh", "Grippe" → Coach erkennt Krank-Modus.

---

## Ablauf (Schritt K)

### 1. Symptom-Interview (3 Fragen, einmalig)

Coach stellt alle 3 Fragen in einer Nachricht:

1. **Tag der Krankheit?** (Tag 1 = heute begonnen, Tag 3 = seit 3 Tagen krank)
2. **Fieber?** (ja + Temperatur wenn bekannt / nein)
3. **Symptome unterhalb des Halses?** Husten, Brustenge, Ganzkörperschmerzen → ja / nein

### 2. Rückkehr-Logik (Neck Check — Sportmedizin-Standard)

| Situation | Rückkehrstart |
|---|---|
| Nur oberhalb Hals (Schnupfen, Hals) | Symptomfrei + 24h → LIT möglich |
| Unterhalb Hals (Husten, Körperschmerzen) | Symptomfrei + 48h → Spaziergang; +72h → LIT |
| Fieber vorhanden | Fieberfrei + 24h → dann obige Regeln anwenden |

**Rückkehrdatum berechnen:** `heute + (noch kranke Tage geschätzt) + Wartefrist`

Schätzung verbleibende Kranktage:
- Tag 1–2, keine Komplikationen: noch ~3–5 Tage
- Tag 3+: Verlauf individuell, Schätzung ~2–3 Tage

### 3. Rampe nach Wiedereinstieg (immer gleich)

| Tag nach Rückkehrtag | Aktivität |
|---|---|
| +0 | Spaziergang / Mobilität ≤ 30 min |
| +1 | LIT 45 min, RPE ≤ 12, HF < 130 |
| +2 | LIT 60 min, Z1–Z2 normal |
| +3–4 | Normales LIT-Programm |
| +5+ | Volle Last möglich |

### 4. Plananpassung `planung/kw[N].md`

- Alle Einheiten bis zum Rückkehrtag → Status `❌ Krank`, TSS Ist = 0
- Verbleibende Tage der Woche → durch Rampe ersetzen (Spaziergang/LIT gemäß Tabelle)
- TSS-Wochenziel: Coach schreibt Notiz "TSS-Ziel entfällt — Krankheitswoche"
- Datei speichern (kein git commit — normaler Wochenplan-Flow)

### 5. Rückkehrwoche

Wird **nicht sofort** in `planung/kw[N+1].md` geschrieben. Beim nächsten Wochenplanungs-Aufruf:
- Schritt 0a (Wochen-Retro) erkennt Krankheitswoche aus COACHING_AKTE
- TSS-Compliance-Check in der Retro entfällt (Kommentar: "Krankheitswoche — kein TSS-Ziel")
- Schritt 0 liest aktuellen Fitness-Stand (CTL/ATL/TSB nach Krankheitspause)
- Neue Woche wird mit TSS-Ziel 50% des normalen Wertes geplant, nur LIT-Einheiten

### 6. COACHING_AKTE.md Eintrag

```markdown
## [Datum] Krankheit KW[N]
Krank ab [Datum] · [Verlauf: oberhalb/unterhalb Hals] · [Fieber: ja X°C / nein]
Rückkehrtag: [Datum] · [N] Trainingstage ausgefallen
→ Rückkehrwoche KW[N+1]: TSS-Ziel 50%, nur LIT
```

---

## Sonderfall: Nähe zum Rennen

- **< 3 Wochen bis RadRace (KW24):** Coach fügt Hinweis ein: "Taper-Phase — lieber 1 Extratag Pause als zu früh zurück. CTL-Verlust durch Krankheit wird nicht kompensiert."
- Taper-Logik (Schritt T) läuft beim nächsten Wochenplan-Aufruf normal weiter — keine manuelle Taper-Korrektur

---

## Output-Format im Chat

```
🤒 Krank-Modus

Rückkehrdatum: [Datum] (LIT) · [Datum] (volle Last)

Plananpassung KW[N]:
[angepasste Wochentabelle mit ❌ Krank und Rampe]

Hinweis: Beim nächsten Wochenplan (KW[N+1]) plane ich automatisch mit 50% TSS ein.
```

---

## Betroffene Dateien

| Datei | Änderung |
|---|---|
| `.claude/skills/coach/SKILL.md` | Neuer Abschnitt "Schritt K: Krank-Modus" + Trigger in Modus-Erkennung |
| `planung/kw[N].md` | Einheiten auf ❌ Krank setzen, Rampe eintragen |
| `COACHING_AKTE.md` | Krankheitseintrag anfügen |
