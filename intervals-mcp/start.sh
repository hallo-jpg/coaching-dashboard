#!/usr/bin/env bash
# Startet den intervals-icu MCP-Server selbstständig – unabhängig von Setup-Script oder Hooks.
# Installiert node_modules bei Bedarf und protokolliert jeden Start in .start.log (Diagnose für Cloud-Sessions).
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$DIR/.start.log"

{
  echo "=== $(date -u +%FT%TZ) start.sh cwd=$PWD remote=${CLAUDE_CODE_REMOTE:-} node=$(node -v 2>&1) npm=$(npm -v 2>&1)"
  echo "    key_len=${#INTERVALS_API_KEY} athlete=${INTERVALS_ATHLETE_ID:-<leer>} env_file=$([ -f "$DIR/.env" ] && echo ja || echo nein)"
} >> "$LOG" 2>&1

if [ ! -d "$DIR/node_modules/@modelcontextprotocol" ]; then
  echo "    node_modules fehlen → npm ci ($(date -u +%T))" >> "$LOG"
  ( cd "$DIR" && { npm ci --silent --no-audit --no-fund || npm install --silent --no-audit --no-fund; } ) >> "$LOG" 2>&1
  echo "    npm fertig ($(date -u +%T)) exit=$? modules=$([ -d "$DIR/node_modules/@modelcontextprotocol" ] && echo ja || echo nein)" >> "$LOG"
fi

echo "    exec node server.js" >> "$LOG"
exec node "$DIR/server.js" 2> >(tee -a "$LOG" >&2)
