# Coach unterwegs – Claude Code Web / Claude-App

Der Coach läuft in einer Cloud-Sandbox direkt gegen dieses Repo. Alles, was er lokal kann,
kann er dort auch – mit zwei Einschränkungen (siehe unten).

## Einmalige Einrichtung (ca. 5 Minuten)

1. **Repo verbinden** – <https://claude.ai/code> → GitHub verbinden → `hallo-jpg/coaching-dashboard` freigeben.
2. **Cloud-Umgebung konfigurieren** – auf claude.ai/code (oder in der App beim Session-Start) das
   **Wolken-Symbol / den Environment-Selector** öffnen → Umgebung „Default" bearbeiten (oder eine neue
   „Coaching" anlegen). Im Dialog drei Dinge:
   - **Network access → Custom**, Domain `intervals.icu` eintragen und
     **„Also include default list of common package managers" anhaken** (sonst kein `npm install`).
     Ohne diese Freigabe startet der MCP-Server, aber jeder Abruf scheitert.
   - **Environment variables** (nicht im Repo!):
     ```
     INTERVALS_API_KEY=5gxxxxxxxxxxxxxxxxxxxxxxx
     INTERVALS_ATHLETE_ID=i554154
     ```
     Der Key ist 25 Zeichen, nur Kleinbuchstaben/Ziffern (intervals.icu → Settings → Developer Settings,
     lokal in `intervals-mcp/.env`). **Ohne Klammern, Anführungszeichen oder Leerzeichen eintragen** –
     ein `<…>` drumherum ergibt „401 Auth failed".
     Hinweis der Doku: Werte sind für jeden lesbar, der diese Umgebung nutzt – das bist nur du.
   - **Setup script** – genau diese Zeile eintragen:
     ```
     npm ci --prefix intervals-mcp || true
     ```
     Grund: MCP-Server und SessionStart-Hook starten gleichzeitig. Ohne Setup script fehlen dem
     Server beim ersten Start die Node-Module („failed to connect at session start"), obwohl er
     manuell danach läuft. Das Setup script läuft **vor** Claude Code und wird gecacht.
   Speichern.
3. **Erste Session starten** – Repo auswählen, diese Umgebung auswählen. Claude fragt einmal, ob der
   MCP-Server aus `.mcp.json` erlaubt werden soll → **Ja**.
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

## Status

✅ Eingerichtet und getestet am 19.9.2026: MCP verbindet, `get_readiness_score` liefert Live-Daten, Push auf `main` läuft, Dashboard-Rebuild wird durch den Push ausgelöst.

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
