# Coach Skill FTP Development Extension – Design Spec

*Datum: 23. April 2026*

## Ziel

Der Coach-Skill erhält eine strukturierte FTP-Entwicklungslogik: planmäßige Testfenster, Ankündigungen, automatisierte Testwoche und Power-PR-Erkennung als Proxy-Signal. Kein automatisches Überschreiben von Werten — Stefan entscheidet immer selbst.

## Architektur

Vier Komponenten, die zusammenwirken:

1. Testfenster im Langfristplan (Referenz)
2. Ankündigung 3 Wochen vor Testfenster (proaktiv, im Coach-Skill)
3. Testwoche-Struktur (automatisch generiert, wenn Test bestätigt)
4. Power-PR-Erkennung (via MCP, bei Planungsaufruf)

Alle FTP-Updates bleiben beim Athleten — der Skill schlägt vor, fragt, und wartet auf Bestätigung.

---

## Komponente 1: Testfenster im Langfristplan

**Wo:** `planung/langfristplan.md`

**Was:** Zwei feste Testfenster pro Saison werden im Langfristplan eingetragen:

| Testfenster | KW | Timing-Logik |
|---|---|---|
| Frühjahrstest | KW21 (18.–24. Mai 2026) | Vor RadRace 120 (KW24), nach HIT-Block (KW18–20) |
| Herbsttest | KW39 (Sep 2026) | Nach Sommerpause, Planungsgrundlage für Winterblock |

**Frühjahrtest-Rationale:** HIT-Block KW18–20 löst VO2max-Adaptationen aus (Rønnestad: +2–4% nach 4-Wochen-Block). FTP-Adaptationen kommen 2–4 Wochen nach VO2max-Gains — KW21 trifft dieses Fenster optimal. Danach 2 Wochen Taper (KW22–23) vor RadRace.

**Format im Langfristplan:**

```markdown
| KW21 | FTP-Test | 🔬 Sentiero 3+10min | Test → Taper-Vorbereitung RadRace |
```

---

## Komponente 2: Ankündigung 3 Wochen vor Test

**Wann:** Skill erkennt: aktuell = Testfenster − 3 Wochen → proaktiver Hinweis bei nächstem `/coach`-Aufruf

**Was der Skill ausgibt:**

```
📊 FTP-Test in 3 Wochen (KW21)
Voraussetzungen: ≥3 Tage ohne HIT in der Vorwoche, kein Wettkampf-Stress, volle Erholung (TSB > 0)
Soll ich die Testwoche bereits vorplanen? [ja / verschieben auf KW22]
```

**Entscheidungslogik:**
- Wenn ja → Komponente 3 (Testwoche generieren)
- Wenn verschieben → Testfenster im Langfristplan auf +1 KW verschoben, neuer Hinweis in 1 Woche

---

## Komponente 3: Testwoche-Struktur

**Protokoll:** Sentiero 3+10min (outdoor, 4iiii Powermeter)
FTP = 10min-Watt × 0,90

**Wochenstruktur (KW21 Beispiel):**

| Tag | Workout | Zweck |
|---|---|---|
| Mo | Ruhetag oder Spaziergang | Mini-Taper |
| Di | LIT 60–90min, locker | Beine frisch halten |
| Mi | 3×5min Z4 + Ausfahrt kurz | Neuromuskuläre Aktivierung |
| Do | **FTP-Test: 3+10min (outdoor, 4iiii)** | — |
| Fr | Ruhetag | Erholung |
| Sa | LIT 2h | Recovery-Ride |
| So | LIT 2h30 oder Ruhetag | Flexible Erholung |

**Post-Test:**

Nach Eingabe des Testergebnisses berechnet der Skill:
- Neuen FTP-Wert (10min × 0,90)
- Alle Zonenwatts (Prozentsätze × neuer FTP)
- Alle Workout-Zielwatts
- Zeigt alte und neue Werte im Vergleich
- Fragt: „Neue FTP übernehmen? [ja / nein]"
- Bei Bestätigung: `athlete/profil.md` aktualisieren

**Format des Skill-Outputs (Post-Test):**

```
📊 FTP-Test Ergebnis
10min-Watt: 320W → FTP = 288W  ← Beispiel
(oder: 10min-Watt: 355W → FTP = 320W)

Vergleich:
  Alt: 305W (3,47 W/kg @ 88kg)
  Neu: 320W (3,64 W/kg @ 88kg) → +5,0%

Zonen (neu):
  LIT (55%): 176W
  SwSp (89%): 285W
  KA (91%): 291W
  MIT (101%): 323W

Übernehmen? [ja / nein]
```

---

## Komponente 4: Power-PR-Erkennung

**Wann:** Bei jedem `/coach`-Aufruf, der `get_recent_activities` auslöst

**Was der Skill prüft:**
Für die Dauern 5min, 10min, 20min: Ist der aktuelle Bestwert >2% über dem gespeicherten Wert in `athlete/fortschritt.md`?

**Schwellenwert:** >2% (bewusst konservativ — Tagesform-Schwankungen bis 3W werden damit gefiltert)

**Reaktion bei PR:**

```
💪 Neuer 10min-Power-PR erkannt: 341W (vorher: 333W, +2,4%)
Das deutet auf eine FTP von ~307W hin (341W × 0,90).
Aktuell gespeichert: 305W.

Soll ich die FTP auf 307W aktualisieren? [ja / nein / warten]
```

**Wenn „warten":** PR wird gespeichert, FTP nicht geändert. Beim nächsten `/coach` kein erneuter Hinweis (kein Spam).

**Wenn „ja":** Profil aktualisieren, Zonen neu berechnen (wie Komponente 3 Post-Test).

**Wenn „nein":** Nichts ändert sich. PR wird dennoch in `athlete/fortschritt.md` festgehalten.

**Implementierungsdetail:**
- `athlete/fortschritt.md` enthält aktuelle Bestwerte (5/10/20min) als Referenz
- Bei jedem PR-Update wird der Wert dort aktualisiert (unabhängig von FTP-Entscheidung)

---

## Abgrenzungen (Out of Scope)

- **Kein automatisches FTP-Update** ohne Bestätigung
- **Kein drittes Testfenster** — 2 Tests/Saison ist das Maximum (Rønnestad: zu häufiges Testen kostet Trainingszeit)
- **Keine Taper-Automatik** — Taper vor RadRace wird separat geplant (nicht durch diesen Skill ausgelöst)
- **Keine automatische HRV-basierte Test-Verschiebung** — Readiness wird vom Skill erwähnt, Entscheidung bleibt beim Athleten

---

## Dateiänderungen

| Datei | Art | Was |
|---|---|---|
| `planung/langfristplan.md` | Modify | Testfenster KW21 + Herbst eintragen |
| `.claude/skills/coach/SKILL.md` | Modify | Komponenten 2–4 als neue Abschnitte |
| `athlete/fortschritt.md` | Modify | Power-PR-Bestwerte (5/10/20min) als Referenz-Tabelle |

---

## Entscheidungsregeln (Zusammenfassung)

| Situation | Skill-Reaktion |
|---|---|
| 3 Wochen vor Testfenster | Ankündigung + Frage ob vorplanen |
| Stefan sagt „ja" | Testwoche generieren |
| Stefan sagt „verschieben" | +1 KW, neuer Hinweis in 7 Tagen |
| Power-PR >2% erkannt | Hinweis + FTP-Prognose + Frage |
| Stefan sagt „ja" zu FTP-Update | Profil + Zonen aktualisieren |
| Stefan sagt „nein" | PR festhalten, FTP bleibt |
| Stefan sagt „warten" | PR festhalten, kein erneuter Hinweis |
| Post-Test Ergebnis eingegeben | Vergleich zeigen + Frage |
