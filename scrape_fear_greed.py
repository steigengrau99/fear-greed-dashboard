import requests
import json
from datetime import datetime
import sys

URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.cnn.com/",
}

response = requests.get(URL, headers=headers, timeout=15)

if response.status_code != 200:
    print("HTTP ERROR:", response.status_code)
    print(response.text[:500])
    sys.exit(1)

try:
    data = response.json()
except Exception as e:
    print("FAILED TO PARSE JSON")
    print(response.text[:500])
    sys.exit(1)

fg = data.get("fear_and_greed")

if not fg:
    print("Missing fear_and_greed field")
    print(data)
    sys.exit(1)

output = {
    "timestamp": datetime.utcnow().isoformat(),
    "score": fg.get("score"),
    "rating": fg.get("rating"),
    "previous_close": fg.get("previous_close"),
    "one_week_ago": fg.get("last_week"),
    "one_month_ago": fg.get("last_month")
}

with open("fear_greed.json", "w") as f:
    json.dump(output, f, indent=2)
