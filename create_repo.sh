#!/bin/bash
# Quick script to create GitHub repo and push code
# Usage: GITHUB_TOKEN=your_token ./create_repo.sh

set -e

if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable not set"
    echo ""
    echo "Quick setup:"
    echo "1. Get token from: https://github.com/settings/tokens/new"
    echo "2. Select 'repo' scope"
    echo "3. Run: GITHUB_TOKEN=your_token_here ./create_repo.sh"
    exit 1
fi

cd /scratch/bds9746/viz_evaluation_pipeline

echo "Creating GitHub repository..."
RESPONSE=$(curl -s -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name":"viz_evaluation_pipeline","description":"Visualization evaluation pipeline","private":false}')

if echo "$RESPONSE" | grep -q '"message"'; then
    echo "Error creating repository:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    exit 1
fi

echo "✓ Repository created successfully!"
echo "Pushing code to GitHub..."

git push -u origin main

echo ""
echo "✓ Success! Repository available at:"
echo "  https://github.com/Bhumika-Shetty/viz_evaluation_pipeline"

