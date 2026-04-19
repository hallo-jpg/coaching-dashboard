#!/usr/bin/env python3
"""Debug: letzte 3 Tage Wellness-Daten von intervals.icu ausgeben."""
import os, base64, json, requests
from datetime import date, timedelta

API_KEY    = os.environ["INTERVALS_API_KEY"]
ATHLETE_ID = os.environ["INTERVALS_ATHLETE_ID"]
BASE_URL   = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}"
AUTH       = "Basic " + base64.b64encode(f"API_KEY:{API_KEY}".encode()).decode()

today  = date.today()
oldest = (today - timedelta(3)).isoformat()
newest = today.isoformat()

print(f"=== Wellness {oldest} → {newest} ===")
r = requests.get(f"{BASE_URL}/wellness?oldest={oldest}&newest={newest}",
                 headers={"Authorization": AUTH})
print(f"Status: {r.status_code}")
data = r.json()
for entry in data:
    eid = entry.get("id")
    print(f"\n--- {eid} ---")
    for key in ["hrv", "sleepSecs", "sleepScore", "restingHR", "ctl", "atl", "score"]:
        print(f"  {key}: {entry.get(key)}")
    # Alle non-null Felder
    all_fields = {k: v for k, v in entry.items() if v is not None and v != 0}
    print(f"  [alle non-null/non-zero]: {json.dumps(all_fields, indent=4)}")
