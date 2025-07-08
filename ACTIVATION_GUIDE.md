# 🚀 Step-by-Step Activation Guide

## **Required Actions to Make the Tracking System Work**

### **Phase 1: GitHub Setup (5 minutes)**

#### 1. **Create GitHub Personal Access Token**
```bash
# Go to: https://github.com/settings/tokens
# Click "Generate new token (classic)"
# Select these scopes:
# ✅ repo (Full control of private repositories)  
# ✅ read:org (Read org membership)
# ✅ workflow (Update GitHub Action workflows)

# Save the token - you'll need it for Azure DevOps
```

#### 2. **Enable GitHub Actions in Your Repository**
```bash
# Go to your repository settings
# Navigate to: Settings → Actions → General
# Under "Actions permissions" select "Allow all actions and reusable workflows"
# Under "Workflow permissions" select "Read and write permissions"
# ✅ Check "Allow GitHub Actions to create and approve pull requests"
```

#### 3. **Create Required Labels** (Optional, for GitHub Actions workflow)
```bash
gh auth login  # Use your PAT from step 1
gh label create "common-code-tracking" --description "Issues tracking common code usage" --color "0E8A16"
gh label create "analytics" --description "Analytics and metrics" --color "1D76DB"
```

### **Phase 2: Azure DevOps Setup (10 minutes)**

#### 1. **Add GitHub Token to Azure DevOps**
```yaml
# Go to: Azure DevOps → Your Project → Pipelines → Library
# Click "Variable groups" → "New variable group"
# Name: "GitHubIntegration"
# Add variable:
#   Name: GITHUB_TOKEN
#   Value: [paste your GitHub PAT from Phase 1]
#   ✅ Keep this value secret: YES
```

#### 2. **Create Service Connection** (For advanced features)
```bash
# Go to: Project Settings → Service connections
# Click "New service connection" → "GitHub"
# Choose "Personal Access Token" 
# Paste your GitHub PAT
# Name: "GitHubConnection"
# ✅ Grant access permission to all pipelines
```

#### 3. **Update Pipeline YAML**
```yaml
# In your azure-pipeline.yml, add this to variables section:
variables:
  - group: GitHubIntegration  # Links to the variable group from step 1
  - name: COMMON_DIRECTORY
    value: "sth/robert_common"
  - name: TRACKING_FILE  
    value: "usage_report.md"
```

### **Phase 3: Test the Setup (2 minutes)**

#### 1. **Test GitHub Authentication**
```bash
# In your local terminal:
gh auth login
gh auth status
gh repo view YOUR_ORG/YOUR_REPO --json nameWithOwner
```

#### 2. **Run Pipeline Test**
```bash
# Commit and push any change to sth/robert_common/
echo "# Test change" >> sth/robert_common/test.md
git add sth/robert_common/test.md
git commit -m "Test: trigger usage tracking pipeline"
git push origin main

# Watch the pipeline run in Azure DevOps
# Check for artifacts: "common-code-usage-report"
```

### **Phase 4: Verify Results (1 minute)**

#### 1. **Check Azure DevOps Pipeline**
- ✅ Pipeline runs successfully
- ✅ "common-code-usage-report" artifact is created  
- ✅ Pipeline logs show usage statistics

#### 2. **Check GitHub Actions** (if using GitHub workflow)
- ✅ Workflow runs on changes to `sth/robert_common/**`
- ✅ Issues are created with tracking reports
- ✅ Cross-repository search works (if you have org access)

## **🚨 Troubleshooting Common Issues**

### **Issue: "GitHub authentication failed"**
```bash
# Solution: Check your PAT has correct scopes
gh auth status --show-token
# If expired, create new token with same scopes
```

### **Issue: "No cross-repository usage found"**
```bash
# This is normal if:
# - You don't have organization-level access
# - Your repositories are private
# - Your code isn't used in other repos yet
```

### **Issue: "Pipeline fails on GitHub CLI installation"**
```bash
# Solution: The pipeline handles this with fallbacks
# Check the "GitHub Cross-Repository Analysis" step
# It will skip if GitHub CLI fails to authenticate
```

## **🎯 Expected Outcomes**

After successful setup, you'll get:

1. **Automated Reports** every time you change `sth/robert_common/`
2. **Usage Statistics** showing which modules are most imported
3. **Activity Tracking** showing recent changes and commit history
4. **Cross-Repository Search** (if you have org access)
5. **Downloadable Artifacts** with detailed usage reports

## **📋 Verification Checklist**

- [ ] GitHub PAT created with correct scopes
- [ ] GitHub Actions enabled in repository
- [ ] Azure DevOps variable group created
- [ ] GITHUB_TOKEN added as secret variable
- [ ] Pipeline runs successfully
- [ ] Usage report artifact is generated
- [ ] Report contains actual usage statistics

**🎉 Once this checklist is complete, your tracking system is fully operational!**
