"""Tests fuer formatIntervals() im intervals-MCP-Server (Tool get_activity_intervals).

Fixtures sind echte intervals.icu-Antworten (/activity/{id}/intervals, gekuerzt):
  * Lauf 26.10.2026 - Easy + 5 Steigerungen, Laps per Taste (alle als WORK markiert)
  * Rad 21.10.2026 - MyWhoosh SwSp 3x12min @ 267W

Wie test_mcp_workout_steps.py fuehrt der Test die echte Funktion aus server.js aus.
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SERVER_JS = ROOT / "intervals-mcp" / "server.js"
FIX = Path(__file__).resolve().parent / "fixtures"

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None or not SERVER_JS.exists(),
    reason="node oder intervals-mcp/server.js nicht verfuegbar",
)


def fmt(typ, fixture):
    src = SERVER_JS.read_text()
    start = src.index("function formatIntervals(")
    end = src.index("// ── Ende formatIntervals")
    body = src[start:end]
    data = json.loads((FIX / fixture).read_text())
    script = (
        body
        + "\nprocess.stdout.write(JSON.stringify(formatIntervals(process.argv[1], JSON.parse(process.argv[2]))));"
    )
    out = subprocess.run(
        ["node", "-e", script, typ, json.dumps(data)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)


def test_rad_drei_sweetspot_intervalle():
    rows = fmt("VirtualRide", "mcp_intervals_ride.json")
    work = [r for r in rows if r["typ"] == "WORK" and r["dauer_s"] > 600]
    assert len(work) == 3
    for r in work:
        assert r["watt"] == 270
        assert r["kadenz"] == 95          # Rad: rpm, nicht verdoppelt
        assert "pace_min_km" not in r
    assert [r["hf"] for r in work] == [169, 170, 174]


def test_lauf_steigerungen_pace_und_spm():
    rows = fmt("Run", "mcp_intervals_run.json")
    assert len(rows) == 12
    easy = rows[0]
    assert easy["dauer"] == "24:40"
    assert easy["pace_min_km"] == "7:21"
    assert easy["kadenz"] == 165          # 82,6 Doppelschritte -> spm
    stride3 = rows[5]
    assert stride3["dauer_s"] == 19
    assert stride3["distanz_m"] == 72
    assert stride3["pace_min_km"] == "4:24"
    assert stride3["hf_max"] == 182
    assert max(r["hf_max"] for r in rows) == 193


def test_nummerierung_fortlaufend():
    rows = fmt("Run", "mcp_intervals_run.json")
    assert [r["nr"] for r in rows] == list(range(1, 13))
