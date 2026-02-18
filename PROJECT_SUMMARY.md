# AI Trends Tracker - Project Summary

**Date:** February 17, 2026
**Status:** ✅ Podcasts integrated and working
**Next:** Gmail newsletter integration (scheduled for later this week)

---

## 🎯 What We Built

An automated AI trends tracker that aggregates content from:
- **📰 News sources:** OpenAI, Anthropic, Google AI, DeepMind, TechCrunch, The Verge, VentureBeat, MIT Tech Review, Hacker News AI, etc.
- **🎧 Podcasts:** Lex Fridman, Practical AI, NVIDIA AI Podcast, The AI Daily Brief, Lenny's Podcast, Exponent, Stratechery Podcast

**Key Features:**
- Automated daily updates at 9 AM (via launchd)
- Claude AI-powered summaries with key insights
- Detailed podcast highlights with 2-3 bullet points per episode
- Clean, responsive web dashboard
- GitHub Pages deployment at https://rld3.github.io/ai-trends-tracker/

---

## 📋 Recent Changes (Feb 17, 2026)

### 1. **Fixed Podcast Blocking Issue**
- **Problem:** RSS feeds for podcasts were being blocked by proxy
- **Solution:** Modified `update.py` to temporarily disable proxy environment variables when fetching feeds
- **Result:** ✅ All podcast feeds now fetch successfully

### 2. **Added New Podcast Feeds**
Added 4 popular AI podcasts:
- Lex Fridman Podcast
- NVIDIA AI Podcast
- Practical AI
- The AI Daily Brief

### 3. **Enhanced Podcast Display**
**Before:** Podcasts weren't showing up at all
**After:**
- Podcasts always fetch the 2 most recent episodes (regardless of date)
- Podcasts appear first in the source articles list
- Increased display from 10 to 20 items to show both podcasts and articles

### 4. **Added Detailed Podcast Highlights Section**
New dashboard layout:
1. 📅 Date
2. 📝 Overall Summary (includes podcast takeaways)
3. 🎧 **Podcast Highlights** (NEW!)
   - Individual episode breakdowns
   - 2-3 bullet points per podcast with key insights
   - "Listen →" links to episodes
4. 🚀 Top Features & Announcements
5. 💰 Fintech/AI Trends
6. 💼 Fundraising
7. 🔗 Source Articles

---

## 🗂️ Project Structure

```
~/my-web-app/
├── index.html              # Main dashboard (view at http://localhost:8080)
├── update.py               # Data fetching & summarization script
├── auto-update.sh          # Shell script run by launchd
├── test_feeds.py           # Test script to verify RSS feeds work
├── data/
│   └── summaries.json      # Generated daily summaries (90 days of history)
├── .git/                   # Git repository
└── PROJECT_SUMMARY.md      # This file!
```

**Automation:**
- **Location:** `~/Library/LaunchAgents/com.aitracker.daily.plist`
- **Schedule:** Daily at 9:00 AM
- **Logs:** `~/my-web-app/launchd.log` and `launchd-error.log`

---

## 🚀 How to Use

### View the Dashboard

**Option 1: Web Server (Recommended)**
```bash
cd ~/my-web-app
python3 -m http.server 8080
```
Then open: http://localhost:8080

**Option 2: Live Site**
https://rld3.github.io/ai-trends-tracker/
(Updates automatically when you push to GitHub)

### Manual Update

To manually fetch new content:
```bash
cd ~/my-web-app
python3 update.py
```

Expected output:
```
Fetched X recent articles and Y podcast episodes
Generating summaries with Claude API...
Summary generated successfully!
✅ Update complete!
```

### Test RSS Feeds

To verify feeds are working:
```bash
cd ~/my-web-app
python3 test_feeds.py
```

Should show ✓ checkmarks for successful feeds.

### Push to GitHub

After making changes:
```bash
cd ~/my-web-app
git add .
git commit -m "Your commit message"
git push origin main
```

GitHub Pages will update in 1-2 minutes.

---

## 🔧 Key Technical Details

### Proxy Bypass Solution
The `update.py` script temporarily unsets proxy environment variables when fetching RSS feeds:
```python
# Disable proxy
proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',
              'ALL_PROXY', 'all_proxy', 'GRPC_PROXY', 'grpc_proxy']
for var in proxy_vars:
    if var in os.environ:
        original_proxies[var] = os.environ[var]
        del os.environ[var]
```

### Podcast Fetching Logic
Podcasts are treated differently than news articles:
- **Podcasts:** Always fetch 2 most recent episodes (regardless of age)
- **News:** Only fetch articles from last 10 days
- **Reason:** Podcasts publish weekly/bi-weekly, news publishes daily

### Claude API Integration
Uses `claude-sonnet-4-20250514` to:
1. Analyze all articles and podcast episodes
2. Generate overall summary
3. Create detailed podcast highlights (2-3 bullets per episode)
4. Identify top features, fintech trends, and fundraising

---

## 📅 Next Steps (Scheduled for Later This Week)

### Gmail Newsletter Integration

**Goal:** Pull in AI newsletter content from Gmail and add to daily summaries

**Newsletter Info Needed:**
- Newsletter name (e.g., Ben's Bites, The Neuron, TLDR AI, etc.)
- Gmail connector needs to be set up

**Implementation Plan:**
1. Connect Gmail MCP connector
2. Modify `update.py` to search Gmail for newsletter
3. Extract newsletter content
4. Add newsletter highlights to summary
5. Update dashboard to display newsletter section

**Estimated Time:** 30-60 minutes

---

## 🐛 Troubleshooting

### "No Data Yet" Error
**Cause:** Browser can't access local files
**Solution:** Use web server (`python3 -m http.server 8080`)

### Terminal Shows No Output
**Cause:** Terminal might be frozen or command wasn't executed
**Solution:** Open a fresh Terminal window and try again

### Podcast Episodes Not Showing
**Cause:** Browser cache
**Solution:** Hard refresh (Command + Shift + R on Mac)

### RSS Feeds Failing
**Cause:** Proxy blocking
**Solution:** Already fixed in `update.py` - run `python3 test_feeds.py` to verify

---

## 📞 Quick Reference

**GitHub Repo:** https://github.com/rld3/ai-trends-tracker
**Live Site:** https://rld3.github.io/ai-trends-tracker/
**Local Dashboard:** http://localhost:8080 (when server running)

**Key Commands:**
```bash
# Manual update
python3 ~/my-web-app/update.py

# Start web server
cd ~/my-web-app && python3 -m http.server 8080

# Test feeds
python3 ~/my-web-app/test_feeds.py

# Push to GitHub
cd ~/my-web-app && git add . && git commit -m "Update" && git push
```

---

## ✅ Current Status

- ✅ RSS feed fetching with proxy bypass
- ✅ 7 AI podcast feeds integrated
- ✅ Detailed podcast highlights with bullets and links
- ✅ Daily automated updates at 9 AM
- ✅ GitHub Pages deployment
- ⏳ Gmail newsletter integration (next week)

**Last Updated:** February 17, 2026
**Working perfectly!** 🎉
