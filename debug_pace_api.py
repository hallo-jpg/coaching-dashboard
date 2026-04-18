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

# Get one activity_id from power curves to test
print("=== GET one activity_id from power curves ===")
data = get("/power-curves?type=Ride&curves=all")
entries = data.get("list", []) if isinstance(data, dict) else data
act_id = None
for e in entries:
    ids = e.get("activity_id", [])
    if ids:
        act_id = ids[0]
        print(f"  Found activity_id: {act_id} from curve id={e.get('id')!r}")
        break

if act_id:
    print(f"\n=== GET /activities/{act_id} ===")
    result = get(f"/activities/{act_id}")
    if isinstance(result, list):
        print(f"  Response is a LIST of {len(result)} items")
        if result:
            print(f"  First item keys: {list(result[0].keys())[:10]}")
            print(f"  start_date_local: {result[0].get('start_date_local')}")
    elif isinstance(result, dict):
        print(f"  Response is a DICT, keys: {list(result.keys())[:10]}")
        print(f"  start_date_local: {result.get('start_date_local')}")
    else:
        print(f"  Unexpected type: {type(result)}")
