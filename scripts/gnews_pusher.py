#!/usr/bin/env python3
"""
Fetch top headlines from GNews and push each item to iOS via Bark.
"""

import os
import sys
import textwrap
from datetime import datetime
from urllib.parse import quote

import requests

# === Secrets (must be provided in GitHub Actions) ============================
GNEWS_TOKEN = os.getenv("GNEWS_TOKEN")
BARK_KEY    = os.getenv("BARK_KEY")

if not (GNEWS_TOKEN and BARK_KEY):
    sys.exit("❌ Missing GNEWS_TOKEN or BARK_KEY")

# === Query parameters ========================================================
KEYWORDS = "stock market OR AI OR technology"
LANG     = "en"
LIMIT    = 10  # ← Top 10
TIMEOUT  = 15

# === Fetch news from GNews ===================================================
url = (
    "https://gnews.io/api/v4/top-headlines?"
    f"token={GNEWS_TOKEN}&lang={LANG}&max={LIMIT}&q={KEYWORDS}"
)

try:
    resp = requests.get(url, timeout=TIMEOUT)
    resp.raise_for_status()
except requests.RequestException as e:
    sys.exit(f"❌ GNews request failed: {e}")

articles = resp.json().get("articles", [])

if not articles:
    sys.exit("⚠️ No matching news today")

# === Push each article via Bark =============================================
GROUP_TAG = "topnews"
SUCCESS   = 0

for idx, art in enumerate(articles, start=1):
    title = art["title"].strip()

    # Choose a concise body: prefer description, fallback to content
    raw_body = art.get("description") or art.get("content") or ""
    body = textwrap.shorten(raw_body.replace("\n", " "), width=300, placeholder=" …")

    # Build Bark URL
    bark_url = (
        f"https://api.day.app/{BARK_KEY}/{quote(title)}/{quote(body)}"
        f"?group={GROUP_TAG}"
        f"&url={quote(art['url'])}"
        "&isArchive=1"
    )

    try:
        push_resp = requests.get(bark_url, timeout=TIMEOUT)
        push_resp.raise_for_status()
        SUCCESS += 1
    except requests.RequestException as e:
        print(f"⚠️  Push failed for item {idx}: {e}")

print(f"✅ [GNews Pusher] Pushed {SUCCESS}/{len(articles)} news items")
