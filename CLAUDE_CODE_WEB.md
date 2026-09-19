# Coach unterwegs – Claude Code Web / Claude-App

Der Coach läuft in einer Cloud-Sandbox direkt gegen dieses Repo. Alles, was er lokal kann,
kann er dort auch – mit zwei Einschränkungen (siehe unten).

## Einmalige Einrichtung (ca. 5 Minuten)

1. **Repo verbinden** – <https://claude.ai/code> → GitHub verbinden → `hallo-jpg/coaching-dashboard` freigeben.
2. **Umgebungsvariablen setzen** – in den Environment-Einstellungen der Sandbox (nicht im Repo!):
   ```
   INTERVALS_API_KEY=<Key aus intervals.icu → Settings → Developer>
   INTERVALS_ATHLETE_ID=i554154
   ```
3. **Erste Session starten** – Claude fragt einmal, ob der MCP-Server aus `.mcp.json` erlaubt werden soll → **Ja**.
   Der SessionStart-Hook installiert die Node-Abhängigkeiten automatisch (~10 s beim ersten Mal).

## Funktionstest

In der ersten Session eingeben:

```
/coach Status-Check: rufe get_readiness_score ab und sag mir den Score
```

Erwartung: ein Readiness-Score mit HRV/Schlaf/TSB. Kommt stattdessen „Tool nicht verfügbar":
Umgebungsvariablen prüfen (Schritt 2) und ob die MCP-Freigabe (Schritt 3) erteilt wurde.

Dann ein Push-Test: eine Notiz in `COACHING_AKTE.md` ergänzen lassen und pushen. Nach ~2 Minuten
muss der Actions-Lauf „regenerate dashboard" durch sein und das Dashboard die Änderung zeigen.

## Was in der Web-Session anders ist

| | lokal (Mac) | Web / App |
|---|---|---|
| `/coach`-Skill, CLAUDE.md, Akte, Pläne, Workout-Library | ✅ | ✅ |
| intervals.icu lesen + Workouts anlegen | ✅ | ✅ (nach Einrichtung) |
| Git-Push → Dashboard-Rebuild | ✅ | ✅ |
| Coach-Memory (Korrekturen, Regeln aus Sessions) | ✅ lokal | ⚠️ nur, wenn ins Repo übernommen (`COACH_MEMORY.md`) |
| Entwickler-Plugins (Superpowers, context-mode) | ✅ | ❌ nicht nötig für Coaching |

## Typische Aufrufe vom Handy

```
/coach KW40 planen
/coach Mittwoch fällt aus, Umplanung
/coach bin krank
Dashboard: Kachel X nach oben verschieben
```

Alles endet mit Commit + Push. Das Dashboard baut sich alle 30 Minuten neu – und sofort,
wenn ein Push `planung/`, `athlete/`, `generate.py` oder das Template berührt.
