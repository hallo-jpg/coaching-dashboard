"""Regressionstests fuer den Lauf-Schritt-Generator im intervals-MCP-Server.

Die Bugs, die hier abgesichert werden, waren allesamt still: das Workout
wurde angelegt, sah im Kalender plausibel aus und war trotzdem falsch.

  * 400m wurde als "400m" geschrieben -> intervals.icu liest das als
    400 MINUTEN (24000s), weil "m" im Textformat Minuten bedeutet.
  * Dauern wurden auf ganze Minuten gerundet -> 90s Trabpause wurde 120s,
    alles unter 30s verschwand ganz.

Der Test fuehrt den echten Generator aus server.js aus, statt ihn
nachzubauen - sonst testet er nur die Kopie.
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

SERVER_JS = Path(__file__).resolve().parent.parent / "intervals-mcp" / "server.js"

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None or not SERVER_JS.exists(),
    reason="node oder intervals-mcp/server.js nicht verfuegbar",
)


def build_lines(steps):
    """Ruft den Zeilen-Generator aus server.js mit den gegebenen Schritten auf."""
    src = SERVER_JS.read_text()
    start, end = src.index("const amount = st =>"), src.index("const autoDesc")
    body = src[start:end]

    script = (
        "const build = new Function('workout_steps', "
        + json.dumps(body + "\n return lines;")
        + ");\n"
        "process.stdout.write(build(JSON.parse(process.argv[1])).join('\\n'));"
    )
    out = subprocess.run(
        ["node", "-e", script, json.dumps(steps)],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.split("\n")


def test_distanz_wird_in_km_geschrieben():
    # "0.4km", nicht "400m" - sonst liest intervals.icu 400 Minuten.
    assert build_lines([{"distance_m": 400, "pace_pct": 100}]) == ["- 0.4km 100% Pace"]


def test_distanz_1000er():
    assert build_lines([{"distance_m": 1000, "pace_pct": 95}]) == ["- 1km 95% Pace"]


def test_keine_zeile_endet_auf_meter_einheit():
    """Scharfe Absicherung gegen die Minuten/Meter-Falle."""
    for line in build_lines([{"distance_m": d, "pace_pct": 100} for d in (200, 400, 600, 1000)]):
        assert "km" in line, f"Distanzschritt ohne km-Einheit: {line}"


def test_sekunden_werden_nicht_auf_minuten_gerundet():
    # Frueher: Math.round(90/60) = 2 -> "- 2m 60% Pace"
    assert build_lines([{"duration_secs": 90, "pace_pct": 60}]) == ["- 90s 60% Pace"]


def test_kurze_pause_verschwindet_nicht():
    # Frueher: Math.round(20/60) = 0 -> "- 0m 60% Pace"
    assert build_lines([{"duration_secs": 20, "pace_pct": 60}]) == ["- 20s 60% Pace"]


def test_glatte_minuten_bleiben_minuten():
    assert build_lines([{"duration_secs": 720, "pace_pct_low": 62, "pace_pct_high": 76}]) == [
        "- 12m 62-76% Pace"
    ]


def test_verschachtelte_reps_behalten_pace_und_distanz():
    """pace_pct in Unterschritten wurde vom Schema stillschweigend verworfen."""
    lines = build_lines([{
        "reps": 3,
        "steps": [{"distance_m": 400, "pace_pct": 100},
                  {"duration_secs": 90, "pace_pct": 60}],
    }])
    assert lines == ["- 0.4km 100% Pace", "- 90s 60% Pace"] * 3


def test_komplettes_400er_workout():
    lines = build_lines([
        {"duration_secs": 720, "pace_pct_low": 62, "pace_pct_high": 76},
        {"reps": 8, "steps": [{"distance_m": 400, "pace_pct": 100},
                              {"duration_secs": 90, "pace_pct": 60}]},
        {"duration_secs": 480, "pace_pct_low": 58, "pace_pct_high": 66},
    ])
    assert len(lines) == 18
    assert lines.count("- 0.4km 100% Pace") == 8
    assert lines.count("- 90s 60% Pace") == 8
