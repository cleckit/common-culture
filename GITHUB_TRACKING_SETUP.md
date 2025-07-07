# GitHub Repository Configuration for Common Code Tracking
# This file helps configure your repo to leverage GitHub's built-in tracking tools

## 🎯 Enable These GitHub Features:

### 1. **Repository Insights**
Navigate to: `https://github.com/your-org/your-repo/pulse`
- **Pulse**: Shows recent activity including changes to `sth/robert_common/`
- **Contributors**: See who's contributing to your common code
- **Traffic**: Monitor who's viewing your common files (requires push access)
- **Network**: Visualize forks and dependencies

### 2. **Dependency Graph** 
Navigate to: `https://github.com/your-org/your-repo/network/dependencies`
- Automatically tracks what depends on your code
- Shows security vulnerabilities in dependencies
- Maps package relationships

### 3. **Code Search & GitHub CLI**
Use these commands to track usage:

```bash
# Search for usage across your organization
gh search code "sth.robert_common" --owner your-org

# Find files importing your modules
gh search code "from sth.robert_common" language:python

# Monitor repository activity
gh repo view your-org/your-repo --json createdAt,pushedAt,languages
```

### 4. **GitHub Actions for Automated Tracking**
The workflow in `.github/workflows/track-common-usage.yml` provides:
- Automatic usage tracking on commits
- Cross-repository dependency analysis
- Regular reporting via GitHub Issues

### 5. **Repository Labels for Organization**
Add these labels to categorize issues and PRs:
- `common-code-tracking`: For tracking reports
- `shared-utility`: For code that other teams might want
- `team-extension`: For your team's specific extensions

### 6. **GitHub API Endpoints for Custom Analysis**

```bash
# Repository traffic (requires push access)
gh api repos/:owner/:repo/traffic/popular/paths

# Commit activity
gh api repos/:owner/:repo/stats/commit_activity

# Code frequency
gh api repos/:owner/:repo/stats/code_frequency

# Search across organization
gh api search/code -f q="sth.robert_common language:python"
```

## 🚀 Advanced GitHub Features:

### **GitHub Copilot Usage Insights**
- Track how often your common code is suggested by Copilot
- Monitor adoption patterns across teams

### **Security & Dependabot**
- Automatically detect vulnerabilities in your extensions
- Track which teams are affected by security updates

### **GitHub Pages for Documentation**
Create a documentation site that tracks:
- Usage examples
- API references
- Adoption metrics

## 📊 Metrics You Can Track with GitHub:

1. **Code Views**: How often files in `sth/robert_common/` are viewed
2. **Clone Activity**: When teams clone/fork your repository
3. **Issue References**: Teams filing issues about your common code
4. **PR Mentions**: Pull requests that modify or reference your code
5. **Search Activity**: How often your modules appear in code searches

## 🔧 Setup Commands:

```bash
# Make the tracking script executable
chmod +x scripts/github-track-usage.sh

# Run the tracking script
./scripts/github-track-usage.sh

# Set up GitHub CLI if not already done
gh auth login

# Enable Actions if they're not enabled
gh api repos/:owner/:repo --method PATCH -f has_projects=true
```

This approach leverages GitHub's existing infrastructure instead of building custom tracking from scratch!
