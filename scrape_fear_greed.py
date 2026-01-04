import requests, json, os

URL = "https://api.alternative.me/fng/?limit=1"

resp = requests.get(URL, timeout=10)
resp.raise_for_status()
new_data = resp.json()["data"][0]

history_file = "fear_greed.json"

history = []

if os.path.exists(history_file):
    with open(history_file, "r") as f:
        try:
            existing = json.load(f)

            # If old format (single object), convert to list
            if isinstance(existing, dict):
                history = [existing]
            elif isinstance(existing, list):
                history = existing

        except json.JSONDecodeError:
            history = []

# Append only if new
if not history or history[-1].get("timestamp") != new_data.get("timestamp"):
    history.append(new_data)

with open(history_file, "w") as f:
    json.dump(history, f, indent=2)
