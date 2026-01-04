import requests, json, os, time
from bs4 import BeautifulSoup

today = time.strftime("%Y-%m-%d")
file_path = "app_rankings.json"

# Apps to track
apps = [
    {"name": "Coinbase", "ios": True, "android": True},
    {"name": "Robinhood", "ios": True, "android": True}
]

history = []
if os.path.exists(file_path):
    history = json.load(open(file_path))

records = []

# ---------- iOS ----------
URL_IOS = "https://rss.applemarketingtools.com/api/v2/us/apps/top-free/100/apps.json"
resp = requests.get(URL_IOS, timeout=10)
resp.raise_for_status()
ios_apps = resp.json()["feed"]["results"]

for app in apps:
    rank = None
    if app["ios"]:
        for i, a in enumerate(ios_apps, start=1):
            if app["name"].lower() in a["name"].lower():
                rank = i
                break
        records.append({"date": today, "platform": "ios", "app": app["name"], "rank": rank})

# ---------- Android (Google Play / AppBrain workaround) ----------
def get_android_rank(app_name):
    # Safe: using AppBrain public page
    url_map = {
        "Coinbase": "https://www.appbrain.com/app/coinbase-bitcoin-crypto/com.coinbase.android",
        "Robinhood": "https://www.appbrain.com/app/robinhood-investing-stock-trading/com.robinhood.android"
    }
    url = url_map.get(app_name)
    if not url:
        return None
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        rank = None
        for div in soup.find_all("div"):
            text = div.get_text(strip=True)
            if "Ranked" in text and "#" in text:
                rank = text
                break
        return rank
    except:
        return None

for app in apps:
    if app["android"]:
        rank = get_android_rank(app["name"])
        records.append({"date": today, "platform": "android", "app": app["name"], "rank": rank})

# ---------- Append only new ----------
for r in records:
    # avoid duplicates
    if not any(h for h in history if h["date"] == r["date"] and h["platform"] == r["platform"] and h["app"] == r["app"]):
        history.append(r)

# Save
with open(file_path, "w") as f:
    json.dump(history, f, indent=2)
