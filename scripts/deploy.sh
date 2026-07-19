#!/usr/bin/env bash
# deploy.sh - Push static site to remote (Vercel/Cloudflare via Git)
# Usage: ./scripts/deploy.sh [optional commit message]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE_DIR="$SCRIPT_DIR/../public-site"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
COMMIT_MSG="${1:-Site Update: $TIMESTAMP}"

echo "==> Navigating to public-site..."
cd "$SITE_DIR"

# Verify we're in a git repo
if [ ! -d ".git" ]; then
  echo "ERROR: public-site is not a git repository. Run 'git init' first."
  exit 1
fi

# Check for remote
REMOTE=$(git remote get-url origin 2>/dev/null || true)
if [ -z "$REMOTE" ]; then
  echo "ERROR: No 'origin' remote configured."
  echo "  Run: git remote add origin <your-repo-url>"
  exit 1
fi

echo "==> Remote: $REMOTE"
echo "==> Commit message: $COMMIT_MSG"

# Stage all changes
echo "==> Staging files..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
  echo "==> No changes to commit. Site is up to date."
  exit 0
fi

# Commit
echo "==> Committing..."
git commit -m "$COMMIT_MSG"

# Push
echo "==> Pushing to origin main..."
if ! git push origin main; then
  echo "ERROR: Push failed. Check your credentials and network."
  exit 1
fi

echo "==> Deploy complete! Site will build on your hosting platform."
