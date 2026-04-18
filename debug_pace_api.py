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

print("=== /pace-curves?type=Run&distances=... ===")
data = get(f"/pace-curves?type=Run&distances={DISTANCES}")
print(json.dumps(data, indent=2)[:3000])

print("\n=== /pace-curves?type=Run (no distances filter) ===")
data2 = get("/pace-curves?type=Run")
# Only print top-level keys and first entry to avoid huge output
if isinstance(data2, dict):
    print("Top-level keys:", list(data2.keys()))
    entries = data2.get("list", [])
elif isinstance(data2, list):
    entries = data2
else:
    entries = []

print(f"Number of entries: {len(entries)}")
for e in entries:
    print(f"  id={e.get('id')!r:12}  keys={list(e.keys())}")
    secs = e.get("secs", [])
    dists = e.get("distances", e.get("m", []))
    print(f"    secs sample (first 5): {secs[:5]}")
    print(f"    distances sample (first 5): {dists[:5]}")
