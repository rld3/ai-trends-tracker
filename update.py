#!/usr/bin/env python3
"""
AI Trends Tracker - Automated data collection and summarization script
"""

import os
import json
import feedparser
import requests
from datetime import datetime, timedelta
from anthropic import Anthropic
from pathlib import Path

# Configuration
RSS_FEEDS = {
    # Company Blogs (Direct Sources)
    "OpenAI": "https://openai.com/blog/rss",
    "Anthropic": "https://anthropic.com/news/rss",
    "Google AI": "https://blog.google/technology/ai/rss/",
    "Meta AI": "https://ai.meta.com/blog/rss/",
    "DeepMind": "https://deepmind.google/blog/rss.xml",

    # Tech News Sites
    "TechCrunch AI": "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "VentureBeat AI": "https://venturebeat.com/ai/feed/",
    "Hacker News AI": "https://hnrss.org/newest?q=AI+OR+artificial+intelligence+OR+GPT+OR+LLM",
    "MIT Tech Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "Ars Technica AI": "https://feeds.arstechnica.com/arstechnica/technology-lab",

    # Analysis & Commentary
    "Stratechery": "https://stratechery.com/feed/",

    # Podcasts
    "Lenny's Podcast": "https://api.substack.com/feed/podcast/10845.rss",
    "Exponent": "https://exponent.fm/feed/podcast/",
    "Stratechery Podcast": "https://stratechery.passport.online/feed/rss/CKPwgsS3gU25UpUSUBPAr",
    "Lex Fridman Podcast": "https://lexfridman.com/feed/podcast/",
    "NVIDIA AI Podcast": "https://feeds.soundcloud.com/users/soundcloud:users:264034133/sounds.rss",
    "Practical AI": "https://changelog.com/practicalai/feed",
    "The AI Daily Brief": "https://feeds.buzzsprout.com/2168220.rss",
}

DATA_DIR = Path("data")
SUMMARIES_FILE = DATA_DIR / "summaries.json"

def setup_directories():
    """Create necessary directories"""
    DATA_DIR.mkdir(exist_ok=True)

def fetch_recent_articles(days=2):
    """Fetch recent articles from all RSS feeds"""
    print("Fetching articles from RSS feeds...")
    articles = []
    podcast_articles = []  # Separate list for podcasts
    cutoff_date = datetime.now() - timedelta(days=days)

    # Temporarily disable proxy to avoid blocking RSS feeds
    # Save original proxy settings
    original_proxies = {}
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',
                  'ALL_PROXY', 'all_proxy', 'GRPC_PROXY', 'grpc_proxy']
    for var in proxy_vars:
        if var in os.environ:
            original_proxies[var] = os.environ[var]
            del os.environ[var]

    # Use proper headers to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    for source, feed_url in RSS_FEEDS.items():
        try:
            print(f"  - Fetching from {source}...")
            # Fetch with headers (proxy already disabled via environment)
            response = requests.get(feed_url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)

            is_podcast = 'Podcast' in source or source in ['Lenny\'s Podcast', 'Exponent']
            podcast_episodes_added = 0

            for entry in feed.entries[:15]:  # Get latest 15 entries
                # Try to parse published date
                try:
                    if hasattr(entry, 'published_parsed'):
                        pub_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed'):
                        pub_date = datetime(*entry.updated_parsed[:6])
                    else:
                        pub_date = datetime.now()
                except:
                    pub_date = datetime.now()

                article = {
                    'source': source,
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', '')[:500],  # Truncate long summaries
                    'published': pub_date.isoformat(),
                }

                # For podcasts: always include at least the 2 most recent episodes
                if is_podcast and podcast_episodes_added < 2:
                    podcast_articles.append(article)
                    podcast_episodes_added += 1
                # For regular news: only include if within date range
                elif not is_podcast and pub_date >= cutoff_date:
                    articles.append(article)
        except Exception as e:
            print(f"    Error fetching {source}: {e}")

    # Restore original proxy settings
    for var, value in original_proxies.items():
        os.environ[var] = value

    # Combine articles and podcasts (podcasts first so they appear in dashboard)
    all_content = podcast_articles + articles
    print(f"Fetched {len(articles)} recent articles and {len(podcast_articles)} podcast episodes")
    return all_content

def summarize_with_claude(articles):
    """Use Claude to generate intelligent summaries"""
    print("\nGenerating summaries with Claude API...")

    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set!")
        print("Please set it with: export ANTHROPIC_API_KEY='your-key-here'")
        return None

    client = Anthropic(api_key=api_key)

    # Prepare article data for Claude
    articles_text = "\n\n".join([
        f"Source: {a['source']}\nTitle: {a['title']}\nLink: {a['link']}\nSummary: {a['summary']}"
        for a in articles
    ])

    prompt = f"""You are an AI trends analyst. Based on the following recent articles and podcast episodes from AI companies, tech news, and industry podcasts, provide a comprehensive daily summary.

Recent Articles & Podcast Episodes:
{articles_text}

Please provide:
1. **Overall Summary** - A 2-3 sentence summary of the day's AI news, including key takeaways from podcasts

2. **Podcast Highlights** - For each podcast episode included, provide:
   - Episode title
   - 2-3 bullet points with key insights, quotes, or takeaways
   - The episode link
   Focus on unique perspectives, interviews, or discussions that add depth beyond news articles.

3. **Top 3 Features/Announcements** - List the 3 most significant product features or announcements from major AI companies (OpenAI, Anthropic, Perplexity, Google, Meta). Include the company name and feature.

4. **Fintech/AI Trends** - Identify and summarize 2-3 key trends in the intersection of Fintech and AI based on the articles.

5. **Fundraising Highlights** - List any significant fundraising announcements or investment rounds mentioned (company name and amount).

Format your response as JSON with this structure:
{{
  "date": "{datetime.now().strftime('%Y-%m-%d')}",
  "summary": "A 2-3 sentence overall summary of the day's AI news including podcast takeaways",
  "podcast_highlights": [
    {{
      "title": "Episode title",
      "source": "Podcast name",
      "key_points": [
        "Key insight or takeaway 1",
        "Key insight or takeaway 2",
        "Key insight or takeaway 3"
      ],
      "link": "Episode URL"
    }},
    ...
  ],
  "top_features": [
    {{"company": "Company Name", "feature": "Brief description"}},
    ...
  ],
  "fintech_trends": [
    "Trend description...",
    ...
  ],
  "fundraising": [
    {{"company": "Company Name", "amount": "Amount", "details": "Brief details"}},
    ...
  ]
}}

If there's no relevant information for a category, use an empty array [] or empty string "". Be concise but informative."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract the JSON from Claude's response
        response_text = response.content[0].text

        # Try to parse JSON from response
        # Sometimes Claude wraps JSON in markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        summary_data = json.loads(response_text.strip())
        print("Summary generated successfully!")
        return summary_data

    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return None

def load_existing_summaries():
    """Load existing summaries from file"""
    if SUMMARIES_FILE.exists():
        with open(SUMMARIES_FILE, 'r') as f:
            return json.load(f)
    return {"summaries": []}

def save_summaries(new_summary):
    """Save new summary to file"""
    data = load_existing_summaries()

    # Check if we already have a summary for today
    today = datetime.now().strftime('%Y-%m-%d')
    data['summaries'] = [s for s in data['summaries'] if s.get('date') != today]

    # Add new summary
    data['summaries'].insert(0, new_summary)

    # Keep only last 90 days
    data['summaries'] = data['summaries'][:90]

    with open(SUMMARIES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Summary saved to {SUMMARIES_FILE}")

def main():
    """Main execution"""
    print("=== AI Trends Tracker - Update Script ===\n")

    setup_directories()

    # Fetch articles
    articles = fetch_recent_articles(days=10)

    if not articles:
        print("No recent articles found. Exiting.")
        return

    # Generate summary with Claude
    summary = summarize_with_claude(articles)

    if summary:
        # Add raw articles to summary
        summary['raw_articles'] = articles[:20]  # Keep top 20 for reference (includes podcasts)

        # Save to file
        save_summaries(summary)

        print("\n=== Summary Preview ===")
        print(json.dumps(summary, indent=2))
        print("\n✅ Update complete! Open index.html to view the dashboard.")
    else:
        print("\n❌ Failed to generate summary. Please check your API key and try again.")

if __name__ == "__main__":
    main()
