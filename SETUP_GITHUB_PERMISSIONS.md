# GitHub Setup Checklist for Common Code Tracking

## 🔐 Required GitHub Permissions & Settings

### 1. **Repository Settings** (GitHub Web UI)
Go to: `Settings → Actions → General`

**Required Actions Permissions:**
- ✅ Allow GitHub Actions to create and approve pull requests
- ✅ Allow GitHub Actions to create issues
- ✅ Read and write permissions for:
  - Contents (to read code)
  - Issues (to create tracking issues)
  - Pull requests (to comment on PRs)
  - Metadata (to access repository info)

**Steps to Configure:**
1. Go to your repo: `https://github.com/YOUR_ORG/YOUR_REPO/settings/actions`
2. Under "Workflow permissions" select "Read and write permissions"
3. Check "Allow GitHub Actions to create and approve pull requests"

### 2. **GitHub CLI Authentication** (For Azure DevOps)
```bash
# In Azure DevOps, you need to authenticate GitHub CLI
# Add this as a secret in Azure DevOps:
GITHUB_TOKEN: your_github_personal_access_token
```

### 3. **Personal Access Token** (Required for cross-repo search)
Create at: `https://github.com/settings/tokens`

**Required Scopes:**
- ✅ `repo` (Full control of private repositories)
- ✅ `read:org` (Read org membership)
- ✅ `read:project` (Read project data)

### 4. **Organization Settings** (If you want cross-repo tracking)
Go to: `https://github.com/organizations/YOUR_ORG/settings/member_privileges`

**Required for Cross-Repo Search:**
- ✅ Allow members to see dependency insights for all repositories
- ✅ Enable dependency graph for private repositories

## 🚀 Immediate Actions to Take:

### Step 1: Enable Actions in Your Repository
```bash
# Check if Actions are enabled
gh api repos/OWNER/REPO --jq '.has_actions'

# If false, enable them (requires admin access)
gh api repos/OWNER/REPO --method PATCH -f has_actions=true
```

### Step 2: Create Required Labels
```bash
# Create labels for tracking
gh label create "common-code-tracking" --description "Issues tracking common code usage" --color "0E8A16"
gh label create "analytics" --description "Analytics and metrics" --color "1D76DB"
gh label create "shared-utility" --description "Code that other teams might want" --color "5319E7"
```

### Step 3: Test GitHub CLI Access
```bash
# Test authentication
gh auth status

# Test repository access
gh repo view --json nameWithOwner,hasActions,visibility

# Test search capabilities
gh search code "python" --repo YOUR_ORG/YOUR_REPO --limit 1
```

## 📋 Current Status Check:

Run these commands to verify your setup:

```bash
# 1. Check GitHub CLI authentication
gh auth status

# 2. Verify repository permissions
gh api user/repos --jq '.[] | select(.name=="YOUR_REPO_NAME") | {name, permissions}'

# 3. Test Actions workflow syntax
gh workflow list

# 4. Check if you can create issues
gh issue create --title "Test Issue" --body "Testing permissions" --dry-run
```
