# AI Trends Tracker

A lightweight web application that tracks the latest AI trends, features, and funding announcements from major companies like OpenAI, Anthropic, Google, Meta, and Perplexity.

## Features

- **Automated Data Collection**: Fetches articles from RSS feeds of major AI companies and tech news sites
- **Intelligent Summarization**: Uses Claude AI to generate concise daily summaries
- **Multiple Views**: Daily, weekly, and monthly aggregation views
- **Categories**: Tracks top features, Fintech/AI trends, and fundraising announcements
- **Clean Dashboard**: Beautiful, responsive interface built with Bootstrap

## Quick Start

### 1. Set Up Your API Key

You'll need an Anthropic API key to use Claude for summarization.

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Or add it to your shell profile (~/.zshrc or ~/.bashrc):
```bash
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

Get your API key from: https://console.anthropic.com/

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Generate Your First Summary

```bash
python3 update.py
```

This will:
- Fetch recent articles from AI company blogs and news sites
- Send them to Claude for intelligent analysis
- Generate summaries for top features, trends, and fundraising
- Save the results to `data/summaries.json`

### 4. View the Dashboard

Open `index.html` in your web browser:

```bash
open index.html
```

## Usage

### Manual Updates

Run the update script whenever you want fresh data:

```bash
python3 update.py
```

### Automated Updates (Optional)

Set up a cron job to run daily:

```bash
# Edit crontab
crontab -e

# Add this line to run at 9 AM daily:
0 9 * * * cd /Users/robertdixoniii/my-web-app && /usr/local/bin/python3 update.py
```

## Data Sources

The app fetches from:
- **OpenAI Blog** - Latest GPT and AI announcements
- **Anthropic News** - Claude updates and research
- **Google AI Blog** - Gemini and Google AI developments
- **Meta AI Blog** - LLaMA and Meta AI updates
- **Perplexity Blog** - Search AI innovations
- **TechCrunch AI** - Broad AI industry news
- **VentureBeat AI** - AI business and funding news

## Dashboard Views

- **Daily**: See individual daily summaries with detailed breakdowns
- **Weekly**: Aggregated view of each week's highlights
- **Monthly**: Month-by-month AI trends overview

## Cost Estimate

- **Anthropic API**: ~$0.10-0.50 per day (depending on article volume)
- **Hosting**: Free (static HTML file)
- **Total**: ~$3-15/month

## Customization

### Add More RSS Feeds

Edit `update.py` and add to the `RSS_FEEDS` dictionary:

```python
RSS_FEEDS = {
    "Your Source": "https://example.com/feed.xml",
    ...
}
```

### Adjust Article Timeframe

In `update.py`, change the `days` parameter:

```python
articles = fetch_recent_articles(days=3)  # Look back 3 days instead of 2
```

### Modify Summary Format

Edit the prompt in the `summarize_with_claude()` function to customize what Claude analyzes.

## Troubleshooting

**No articles found**: Try increasing the `days` parameter or check if RSS feeds are accessible

**Claude API error**: Verify your API key is set correctly and you have available credits

**Dashboard shows "No Data Yet"**: Make sure `update.py` ran successfully and created `data/summaries.json`

## Future Enhancements

- Email notifications for daily summaries
- More detailed company-specific tracking
- Integration with Twitter/X for real-time announcements
- Export summaries to PDF/Markdown
- Comparison tools between different companies

## License

MIT License - Feel free to modify and use as needed!
