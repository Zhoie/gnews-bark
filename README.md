# GNEWS-BARK

Automated workflow that fetches top headlines from **GNews** and sends them to your iPhone via **Bark**, powered by GitHub Actions.

## Setup
1. Register at <https://gnews.io> and copy your API key.  
2. Install Bark on iOS (<https://day.app>) and copy your device key.  
3. In your GitHub repo, add two secrets:  
   - `GNEWS_TOKEN` – the GNews API key  
   - `BARK_KEY` – your Bark device key  
4. Commit the files, push, and the workflow will run at 08:00 & 20:00 Beijing time.

You can adjust keywords, language, frequency, or notification text by editing
`gnews_pusher.py` and `gnews_push.yml`.
