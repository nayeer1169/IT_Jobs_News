#!/bin/bash

# Navigate to the repository directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Run the python generator
python3 generate_report.py

# Git Commit and Push (if not in GitHub Actions workflow runner)
if [ -z "$GITHUB_ACTIONS" ]; then
    git add reports/
    if git diff --cached --quiet; then
        echo "No new reports or changes to commit."
    else
        git commit -m "Add/Update daily IT jobs news reports"
        if git push origin main 2>/dev/null; then
            echo "Successfully created and pushed reports"
        else
            git -c http.curloptResolve="github.com:443:20.207.73.82" push origin main
            echo "Successfully created and pushed reports with curloptResolve"
        fi
    fi
else
    echo "Report files generated. GitHub Action will handle git commit and push."
fi

