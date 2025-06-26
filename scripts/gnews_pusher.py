#!/usr/bin/env python3
"""
Fetch headlines from GNews and push to iOS via Bark.
"""

import os
import sys
import textwrap
from datetime import datetime
from dateutil import tz

import requests

# === Required secrets ========================================================
GNEWS_TOKEN = os.getenv("GNEWS_TOKEN")
BARK_KEY    = os.getenv("BARK_KEY")

if not (GNEWS_TOKEN and BARK_KEY):
    sys.exit("❌ Missing GNEWS_TOKEN or BARK_KEY environment variable")

# === Query parameters ========================================================
KEYWORDS = "stock market OR AI OR technology"
LANG     = "en"
LIMIT    = 5

url = (
    "https://gnews.io/api/v4/top-headlines?"
    f"token={GNEWS_TOKEN}&lang={LANG}&max={LIMIT}&q={KEYWORDS}"
)

resp = requests.get(url, timeout=15)
resp.raise_for_status()
articles = resp.json().get("articles", [])

if not articles:
    sys.exit("⚠️ No matching news today")

# === Compose Bark notification ==============================================
bullet_list = "\n".join(
    f"• {a['title']} ({a['source']['name']})" for a in articles
)

title = f"Daily News {datetime.now(tz.gettz('Asia/Shanghai')).strftime('%m-%d')}"
body  = textwrap.shorten(bullet_list, width=200, placeholder=" …")

bark_url = (
    f"https://api.day.app/{BARK_KEY}/"
    f"{requests.utils.quote(title)}/"
    f"{requests.utils.quote(body)}"
    "?group=news&isArchive=1"
)

push_resp = requests.get(bark_url, timeout=15)
push_resp.raise_for_status()

print(f"✅ [GNews Pusher] Pushed {len(articles)} news items")
