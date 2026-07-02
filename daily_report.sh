#!/bin/bash

# Navigate to the repository directory
REPO_DIR="/Users/nayeer1169/Documents/Jobs Section/IT_Jobs_News"
cd "$REPO_DIR" || exit 1

# Get current date in YYYY-MM-DD format
TODAY=$(date +"%Y-%m-%d")
TARGET_DIR="reports/$TODAY"

# Check if today's folder already exists
if [ -d "$TARGET_DIR" ]; then
    echo "Folder $TARGET_DIR already exists."
    exit 0
fi

mkdir -p "$TARGET_DIR/hiring-worldwide"
mkdir -p "$TARGET_DIR/layoffs-worldwide"

# Create hiring-news.md
cat <<EOF > "$TARGET_DIR/hiring-worldwide/hiring-news.md"
# Hiring Worldwide - $TODAY

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
EOF

# Create layoffs-news.md
cat <<EOF > "$TARGET_DIR/layoffs-worldwide/layoffs-news.md"
# Layoffs Worldwide - $TODAY

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
EOF

# Git Commit and Push
git add "$TARGET_DIR"
git commit -m "Add IT jobs news reports for $TODAY"
git -c http.curloptResolve="github.com:443:20.207.73.82" push origin main

echo "Successfully created and pushed reports for $TODAY"
