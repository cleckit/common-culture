#!/bin/bash
# GitHub-native tracking script using GitHub CLI and built-in features

echo "🔍 GitHub-Native Common Code Tracking"
echo "======================================"

# Check if we're in a git repo with GitHub remote
if ! git remote get-url origin | grep -q github.com; then
    echo "❌ This script requires a GitHub repository"
    exit 1
fi

# Extract repo info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "📊 Analyzing repository: $REPO"

echo ""
echo "🏗️  Recent Activity in sth/robert_common:"
echo "==========================================="

# Show recent commits affecting your common directory
gh api "repos/$REPO/commits" \
    --jq '.[] | select(.commit.message | contains("sth/robert_common") or .files[].filename | contains("sth/robert_common")) | {
        sha: .sha[0:7],
        author: .commit.author.name,
        date: .commit.author.date,
        message: .commit.message
    }' --paginate | head -20

echo ""
echo "🔗 Pull Requests mentioning your common code:"
echo "=============================================="

# Find PRs that mention your common directory
gh pr list --state all --search "sth/robert_common" --json number,title,author,state | \
    jq -r '.[] | "PR #\(.number): \(.title) by \(.author.login) [\(.state)]"'

echo ""
echo "📈 File Traffic (GitHub Insights):"
echo "=================================="

# Use GitHub's traffic API if available (requires push access)
gh api "repos/$REPO/traffic/popular/paths" --jq '.[] | select(.path | contains("sth/robert_common")) | {
    path: .path,
    views: .count,
    unique_visitors: .uniques
}' 2>/dev/null || echo "Traffic data requires repository push access"

echo ""
echo "🔍 Cross-Repository Search (if you have org access):"
echo "===================================================="

# Search across organization for usage of your modules
gh search code "sth.robert_common language:python" --json repository,path | \
    jq -r '.[] | "\(.repository.nameWithOwner): \(.path)"' | head -10

echo ""
echo "📋 Summary Report:"
echo "=================="

# Generate a simple summary
total_files=$(find sth/robert_common -name "*.py" | wc -l)
echo "- Total Python files in sth/robert_common: $total_files"

usage_count=$(grep -r "from sth.robert_common" . --include="*.py" | wc -l)
echo "- Internal import statements: $usage_count"

recent_commits=$(git log --oneline --since="30 days ago" -- sth/robert_common/ | wc -l)
echo "- Commits in last 30 days: $recent_commits"

echo ""
echo "💡 Recommendation: Check your GitHub repository Insights tab for:"
echo "  - Traffic → Views (who's viewing your common code)"
echo "  - Network → Dependencies (what depends on your code)"
echo "  - Pulse → Overview (activity summary)"
