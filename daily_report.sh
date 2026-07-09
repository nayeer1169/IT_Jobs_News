#!/bin/bash

# Navigate to the repository directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Get current date in YYYY-MM-DD format (Asia/Kolkata timezone)
TODAY=$(TZ="Asia/Kolkata" date +"%Y-%m-%d")
TARGET_DIR="reports/$TODAY"

# Check if today's folder already exists and has files
if [ -d "$TARGET_DIR" ] && [ -f "$TARGET_DIR/hiring-worldwide/hiring-news.md" ] && [ -f "$TARGET_DIR/layoffs-worldwide/layoffs-news.md" ]; then
    echo "Folder $TARGET_DIR already exists with reports for $TODAY."
    exit 0
fi

# Run the python generator
python3 generate_report.py

# Git Commit and Push (if not in GitHub Actions workflow runner)
if [ -z "$GITHUB_ACTIONS" ]; then
    git add "$TARGET_DIR"
    git commit -m "Add IT jobs news reports for $TODAY" || true
    if git push origin main 2>/dev/null; then
        echo "Successfully created and pushed reports for $TODAY"
    else
        git -c http.curloptResolve="github.com:443:20.207.73.82" push origin main
        echo "Successfully created and pushed reports for $TODAY with curloptResolve"
    fi
else
    echo "Report files generated for $TODAY. GitHub Action will handle git commit and push."
fi

