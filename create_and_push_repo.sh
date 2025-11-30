#!/bin/bash

# Script to create GitHub repository and push code
# Usage: ./create_and_push_repo.sh <GITHUB_TOKEN>

set -e

REPO_NAME="viz_evaluation_pipeline"
GITHUB_USER="Bhumika-Shetty"

if [ -z "$1" ]; then
    echo "Error: GitHub personal access token required"
    echo "Usage: $0 <GITHUB_TOKEN>"
    echo ""
    echo "To create a token:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. Select 'repo' scope"
    echo "4. Copy the token and use it as the argument"
    exit 1
fi

GITHUB_TOKEN=$1

echo "Creating GitHub repository..."
RESPONSE=$(curl -s -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO_NAME\",\"description\":\"Visualization evaluation pipeline\",\"private\":false}")

# Check if repo was created successfully
if echo "$RESPONSE" | grep -q '"message"'; then
    echo "Error creating repository:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    exit 1
fi

echo "Repository created successfully!"
echo "Setting up remote and pushing code..."

# Add remote and push (using SSH)
git remote add origin git@github.com:$GITHUB_USER/$REPO_NAME.git 2>/dev/null || \
git remote set-url origin git@github.com:$GITHUB_USER/$REPO_NAME.git

git push -u origin main

echo ""
echo "Success! Repository is available at:"
echo "https://github.com/$GITHUB_USER/$REPO_NAME"

