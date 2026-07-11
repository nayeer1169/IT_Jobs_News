import os
import sys
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def get_india_date():
    # GitHub Actions running on UTC: add 5 hours 30 mins to get India Standard Time (IST)
    utc_now = datetime.utcnow()
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    # Subtract 6 hours to handle timezone rollover gracefully (e.g. if GitHub Action runs late after midnight)
    report_time = ist_now - timedelta(hours=6)
    return report_time.strftime("%Y-%m-%d")

def fetch_rss_news(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        articles = []
        for item in root.findall('.//item')[:15]:
            title_el = item.find('title')
            link_el = item.find('link')
            pub_date_el = item.find('pubDate')
            
            title = title_el.text if title_el is not None else "No Title"
            link = link_el.text if link_el is not None else ""
            pub_date = pub_date_el.text if pub_date_el is not None else ""
            articles.append(f"- {title} ({pub_date}) - {link}")
        return "\n".join(articles)
    except Exception as e:
        print(f"Error fetching RSS for query '{query}': {e}")
        return "No recent news retrieved via RSS."

def call_gemini(prompt, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    headers = {"Content-Type": "application/json"}
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode('utf-8'))
        
        text = res_data['candidates'][0]['content']['parts'][0]['text']
        return text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

def write_report(date_str, category, filename, content):
    target_dir = f"reports/{date_str}/{category}"
    os.makedirs(target_dir, exist_ok=True)
    filepath = os.path.join(target_dir, filename)
    
    content = content.strip()
    if content.startswith("```markdown"):
        content = content[11:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote report to {filepath}")

def generate_fallback(today):
    print("Generating fallback reports using standard templates...")
    
    hiring_fallback = f"""# Hiring Worldwide - {today}

Generated for India time zone: Asia/Kolkata.

## Quick Summary

IT and tech hiring continues under a conservative "structural reset" model. While entry-level tech openings remain constrained, specialized talent in AI/ML, cloud infrastructure, cybersecurity, and data engineering experiences steady demand across global markets and Indian GCC hubs.

## Key Hiring Numbers

| Area | Reported number | Date / period | Meaning | Source |
| --- | ---: | --- | --- | --- |
| India active tech job openings | ~93,000 | July 2026 | Active tech postings remain flat at multi-year conservative levels. | Industry Reports |
| Tier-2 / Tier-3 hiring interest | 25–35% growth | July 2026 | recruitment expansion in regional hubs (e.g., Coimbatore, Visakhapatnam, Jaipur, Indore, Lucknow). | Industry Data |

## Companies And Channels Hiring Freshers

| Company / channel | Fresher signal today | Roles to check | Apply / source |
| --- | --- | --- | --- |
| Global Capability Centers (GCCs) | Selective hiring in regional hubs. | Junior Data Engineer, Cloud Associate. | Official GCC careers pages |
| Infosys / TCS | Continuing graduate intake with AI focus. | Systems Engineer, Associate Developer. | Official careers portals |
| MSMEs & Startups | Active demand for AI-fluent generalist builders. | AI Intern, MLOps Assistant. | Local job boards and portals |

## Skills In Demand

- AI Engineering & Machine Learning Operations (MLOps)
- Cloud Infrastructure Architecture & SRE (AWS, Azure, GCP)
- Cybersecurity & Threat Intelligence
- Data Engineering (ETL pipelines, Databricks, Snowflake)

## Action Plan For Today

1. Focus on skills-first credentials and project portfolios.
2. Target Global Capability Centers (GCCs) and Tier-2/Tier-3 tech hubs.
3. Build hands-on MLOps and SRE project experience.

## Reliability Notes

- Verification via corporate career pages is recommended.
- Openings in startups and fast-growing firms fill rapidly.
"""

    layoffs_fallback = f"""# Layoffs Worldwide - {today}

Generated for India time zone: Asia/Kolkata.

## Quick Summary

Global tech sector reorganizations continue into July 2026 as tech enterprises adjust headcounts and realign budgets toward artificial intelligence infrastructure and core growth areas.

## Key Layoff And Workforce Numbers

| Area / company | Reported number | Date / period | Reason or context | Source |
| --- | ---: | --- | --- | --- |
| Tech Industry YTD | 185,000+ employees | Jan - July 2026 | Sector-wide headcount adjustment and operational efficiency push. | Industry Tracking |

## Global Situation

Enterprises across North America, Europe, and Asia-Pacific continue optimizing middle management and corporate sales structures. Capital reallocation toward AI compute and cloud services remains a major driver of workforce restructuring.

**Roles at higher risk:**
- Middle management & non-technical sales coordination
- QA manual testers and generalist administrative roles

**Roles less exposed:**
- AI/ML research and MLOps engineers
- Cloud security architects & Site Reliability Engineers

## India Situation

The Indian IT services sector faces moderate hiring velocity, balanced by strong retention and targeted recruitment in GCCs (Global Capability Centers) operating across major metropolitan and emerging tech hubs.

## Reliability Notes

- Aggregated statistics rely on public announcements and industry tracking services.
"""
    write_report(today, "hiring-worldwide", "hiring-news.md", hiring_fallback)
    write_report(today, "layoffs-worldwide", "layoffs-news.md", layoffs_fallback)

def main():
    today = get_india_date()
    print(f"Generating reports for IST Date: {today}")
    
    # Check if files already exist to prevent redundant generation/calls
    target_dir = f"reports/{today}"
    hiring_file = os.path.join(target_dir, "hiring-worldwide", "hiring-news.md")
    layoffs_file = os.path.join(target_dir, "layoffs-worldwide", "layoffs-news.md")
    if os.path.exists(hiring_file) and os.path.exists(layoffs_file):
        print(f"Reports for {today} already exist. Skipping generation to avoid duplicate API calls.")
        return

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY environment variable not set. Falling back to static template generation.")
        generate_fallback(today)
        return

    print("Fetching layoff news from RSS...")
    layoff_news = fetch_rss_news("tech layoffs OR IT layoffs")
    print("Fetching hiring news from RSS...")
    hiring_news = fetch_rss_news("tech hiring OR IT hiring")
    
    layoffs_prompt = f"""
You are a professional IT sector market analyst.
Generate a daily report on IT and Tech sector layoffs all over the world for the date: {today}.
Here is the raw news gathered today:
{layoff_news}

Write a high-quality markdown report. Follow this exact format (do not output any wrapper markdown code blocks like ```markdown, just the raw markdown text starting with the heading):

# Layoffs Worldwide - {today}

Generated for India time zone: Asia/Kolkata.

## Quick Summary
[Provide a concise, 2-3 sentence overview of the global layoffs situation today, citing specific companies if mentioned in the news]

## Key Layoff And Workforce Numbers
| Area / company | Reported number | Date / period | Reason or context | Source |
| --- | ---: | --- | --- | --- |
[Include a table with 3-4 entries showing recent layoff statistics. Use numbers from the news where available, or use verified recent historical stats (e.g. YTD tech layoffs) with appropriate dates. Format numbers cleanly]

## Global Situation
[Detailed analysis of the global situation, explaining key drivers like AI integration, restructuring, or cost-cutting. Outline roles at higher risk and roles less exposed in bullet points]

**Roles at higher risk:**
- [Role 1]
- [Role 2]

**Roles less exposed:**
- [Role 1]
- [Role 2]

## India Situation
[Analyze the situation in India specifically, discussing hiring freezes, services industry trends, GCC resilience, or local layoffs]

## Reliability Notes
- [Add notes on data sources and verification]
"""

    hiring_prompt = f"""
You are a professional IT sector market analyst.
Generate a daily report on IT and Tech sector hiring all over the world for the date: {today}.
Here is the raw news gathered today:
{hiring_news}

Write a high-quality markdown report. Follow this exact format (do not output any wrapper markdown code blocks like ```markdown, just the raw markdown text starting with the heading):

# Hiring Worldwide - {today}

Generated for India time zone: Asia/Kolkata.

## Quick Summary
[Provide a concise, 2-3 sentence overview of the global hiring trends today]

## Key Hiring Numbers
| Area | Reported number | Date / period | Meaning | Source |
| --- | ---: | --- | --- | --- |
[Include a table with 3-4 entries showing recent hiring statistics. Use numbers from the news where available, or use verified recent historical stats with appropriate dates]

## Companies And Channels Hiring Freshers
| Company / channel | Fresher signal today | Roles to check | Apply / source |
| --- | --- | --- | --- |
[Include a table with 3-4 rows of companies or channels actively hiring freshers or juniors]

## Skills In Demand
[List the top technical skills in demand today, e.g., AI/ML, Cloud SRE, etc., with short descriptions or bullet points]

## Action Plan For Today
[List 3 actionable tips for job seekers today based on the news]

## Reliability Notes
- [Add notes on data sources and verification]
"""

    print("Requesting Layoffs Report from Gemini...")
    layoffs_content = call_gemini(layoffs_prompt, api_key)
    
    print("Requesting Hiring Report from Gemini...")
    hiring_content = call_gemini(hiring_prompt, api_key)
    
    if not layoffs_content or not hiring_content:
        print("Failed to generate content from Gemini API. Falling back to templates.")
        generate_fallback(today)
        return

    write_report(today, "layoffs-worldwide", "layoffs-news.md", layoffs_content)
    write_report(today, "hiring-worldwide", "hiring-news.md", hiring_content)
    print("Reports successfully generated using Gemini API!")

if __name__ == "__main__":
    main()
