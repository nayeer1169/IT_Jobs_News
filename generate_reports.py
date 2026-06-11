import os
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import ssl
from datetime import datetime, timezone, timedelta

# Define India Standard Time (IST) offset
ist = timezone(timedelta(hours=5, minutes=30))
today_str = datetime.now(ist).strftime("%Y-%m-%d")

def fetch_rss_news(query):
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        # Create unverified context to avoid SSL errors on local setups
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        items = []
        for item in root.findall('.//item')[:5]:  # Get top 5 items
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            source = item.find('source').text if item.find('source') is not None else "Google News"
            items.append({
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "source": source
            })
        return items
    except Exception as e:
        print(f"Error fetching RSS for query {query}: {e}")
        return []

def main():
    print(f"Generating reports for {today_str}...")
    
    # Fetch layoffs and hiring news
    layoffs_news = fetch_rss_news("tech layoffs OR IT layoffs when:1d")
    hiring_news = fetch_rss_news("tech hiring OR IT hiring when:1d")
    
    # 1. Create layoffs report
    layoffs_dir = f"reports/{today_str}/layoffs-worldwide"
    os.makedirs(layoffs_dir, exist_ok=True)
    layoffs_file = os.path.join(layoffs_dir, "layoffs-news.md")
    
    layoffs_md = f"""# Layoffs Worldwide - {today_str}

Generated for India time zone: Asia/Kolkata.

## Quick Summary

Automated digest of the latest tech and IT sector layoffs reported over the past 24 hours.

## Key Layoff And Workforce Numbers / Recent Reports

| Source | Title / Details | Link |
| --- | --- | --- |
"""
    for item in layoffs_news:
        # Clean title (remove source suffix if present)
        title_cleaned = item['title'].rsplit(" - ", 1)[0]
        layoffs_md += f"| {item['source']} | {title_cleaned} | [Read Article]({item['link']}) |\n"
    if not layoffs_news:
        layoffs_md += "| No new layoffs reports found in the last 24h. | - | - |\n"
        
    layoffs_md += """
## Reliability Notes

- News reports are aggregated from Google News RSS and reflect public announcements.
- Subject to reporting lag and details from third-party sources.
"""
    with open(layoffs_file, "w", encoding="utf-8") as f:
        f.write(layoffs_md)
    print(f"Saved layoffs report to {layoffs_file}")
        
    # 2. Create hiring report
    hiring_dir = f"reports/{today_str}/hiring-worldwide"
    os.makedirs(hiring_dir, exist_ok=True)
    hiring_file = os.path.join(hiring_dir, "hiring-news.md")
    
    hiring_md = f"""# Hiring Worldwide - {today_str}

Generated for India time zone: Asia/Kolkata.

## Quick Summary

Automated digest of the latest tech and IT sector hiring announcements and trends reported over the past 24 hours.

## Recent Hiring News & Listings

| Source | Title / Details | Link |
| --- | --- | --- |
"""
    for item in hiring_news:
        title_cleaned = item['title'].rsplit(" - ", 1)[0]
        hiring_md += f"| {item['source']} | {title_cleaned} | [Read Article]({item['link']}) |\n"
    if not hiring_news:
        hiring_md += "| No new hiring reports found in the last 24h. | - | - |\n"
        
    hiring_md += """
## Reliability Notes

- Listings and news are aggregated from Google News RSS.
- Verify active jobs on official company portals before applying.
"""
    with open(hiring_file, "w", encoding="utf-8") as f:
        f.write(hiring_md)
    print(f"Saved hiring report to {hiring_file}")
        
    print("Reports generated successfully.")

if __name__ == "__main__":
    main()
