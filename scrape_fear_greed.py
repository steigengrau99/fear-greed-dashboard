import requests, json, os, time

URL = "https://api.alternative.me/fng/?limit=1"

resp = requests.get(URL, timeout=10)
resp.raise_for_status()
new_data = resp.json()["data"][0]

history_file = "fear_greed.json"

if os.path.exists(history_file):
    with open(history_file, "r") as f:
        history = json.load(f)
else:
    history = []

# Avoid duplicates
if not history or history[-1]["timestamp"] != new_data["timestamp"]:
    history.append(new_data)

with open(history_file, "w") as f:
    json.dump(history, f, indent=2)
