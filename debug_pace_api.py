#!/usr/bin/env python3
"""Debug script: dumps raw pace-curves API response to understand structure."""
import os
import base64
import json
import requests

API_KEY    = os.environ["INTERVALS_API_KEY"]
ATHLETE_ID = os.environ["INTERVALS_ATHLETE_ID"]
BASE_URL   = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}"
AUTH       = "Basic " + base64.b64encode(f"API_KEY:{API_KEY}".encode()).decode()

DISTANCES = "400,800,1500,1609,3000,5000,10000"

def get(path):
    r = requests.get(f"{BASE_URL}{path}", headers={"Authorization": AUTH}, timeout=15)
    print(f"  Status: {r.status_code}")
    return r.json()

POWER_TARGETS = [1, 5, 30, 60, 180, 480, 1200, 3600]

def dump_curve_fields(label, entry, index_fields):
    """Print parallel arrays for a given set of seconds/distance indices."""
    print(f"\n--- {label} (id={entry.get('id')!r}) ---")
    print(f"  keys: {list(entry.keys())}")
    for field in list(entry.keys()):
        val = entry.get(field)
        if isinstance(val, list) and len(val) > 0:
            print(f"  {field}[0:3] = {val[:3]}")

print("=== POWER CURVES (Ride) ===")
data = get("/power-curves?type=Ride")
entries = data.get("list", []) if isinstance(data, dict) else data
for e in entries:
    dump_curve_fields("Power", e, POWER_TARGETS)

print("\n=== PACE CURVES (Run, curves=all) ===")
data2 = get(f"/pace-curves?type=Run&curves=all&distances={DISTANCES}")
entries2 = data2.get("list", []) if isinstance(data2, dict) else data2
for e in entries2:
    dump_curve_fields("Pace", e, [])
