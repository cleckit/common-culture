# Azure DevOps Setup for GitHub Integration

## 🔐 Required Azure DevOps Configuration

### 1. **Service Connections** (Required)
Go to: `Project Settings → Service connections`

**Create GitHub Service Connection:**
1. Click "New service connection"
2. Select "GitHub"
3. Choose "Personal Access Token"
4. Enter your GitHub PAT with these scopes:
   - `repo` (repository access)
   - `read:org` (organization access)
   - `read:project` (project access)

### 2. **Variable Groups** (Recommended)
Go to: `Pipelines → Library → Variable groups`

**Create Variable Group "GitHubIntegration":**
```yaml
Variables:
  GITHUB_TOKEN: $(github-pat)  # Link to GitHub PAT
  GITHUB_ORG: your-organization-name
  REPO_NAME: common-culture
```

### 3. **Pipeline Permissions**
Go to: `Project Settings → Security`

**Required Pipeline Permissions:**
- ✅ View build definition
- ✅ Edit build pipeline
- ✅ Queue builds
- ✅ View releases

## 🚀 Updated Azure Pipeline Configuration

Here's the production-ready pipeline configuration:

```yaml
# Azure DevOps Pipeline for GitHub-based Common Code Tracking
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - sth/robert_common/**  # Only trigger when your team's code changes

pool:
  vmImage: ubuntu-latest

variables:
- group: GitHubIntegration  # Links to the variable group you created
- name: COMMON_DIRECTORY
  value: "sth/robert_common"
- name: TRACKING_FILE
  value: "usage_report.md"

stages:
  - stage: TrackCommonReuse
    displayName: Track Common Code Usage
    jobs:
      - job: GitHubAnalysis
        displayName: GitHub-based Usage Analysis
        steps:
          # STEP 1: Checkout with full history
          - checkout: self
            fetchDepth: 0
            displayName: "Checkout Repository with Full History"

          # STEP 2: Install GitHub CLI
          - script: |
              echo "Installing GitHub CLI..."
              curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
              echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
              sudo apt update && sudo apt install gh -y
              gh --version
            displayName: "Install GitHub CLI"

          # STEP 3: Authenticate with GitHub
          - script: |
              echo "Configuring GitHub authentication..."
              if [ -z "$(GITHUB_TOKEN)" ]; then
                echo "⚠️  GITHUB_TOKEN not configured. Some features will be limited."
              else
                echo "$(GITHUB_TOKEN)" | gh auth login --with-token
                gh auth status
                echo "✅ GitHub authentication successful"
              fi
            displayName: "Setup GitHub Authentication"
            env:
              GITHUB_TOKEN: $(GITHUB_TOKEN)

          # STEP 4: Generate comprehensive usage report
          - script: |
              echo "Generating comprehensive usage report..."
              
              # Create report header
              echo "# 🔄 Common Code Usage Report $(date +%Y-%m-%d)" > $(TRACKING_FILE)
              echo "Generated from Azure DevOps Pipeline" >> $(TRACKING_FILE)
              echo "" >> $(TRACKING_FILE)
              
              # Basic statistics
              echo "## 📊 Basic Statistics" >> $(TRACKING_FILE)
              echo "" >> $(TRACKING_FILE)
              
              total_files=$(find $(COMMON_DIRECTORY) -name "*.py" 2>/dev/null | wc -l || echo "0")
              echo "- **Total Python files in $(COMMON_DIRECTORY):** $total_files" >> $(TRACKING_FILE)
              
              usage_count=$(grep -r "from sth.robert_common" . --include="*.py" 2>/dev/null | wc -l || echo "0")
              echo "- **Internal import statements:** $usage_count" >> $(TRACKING_FILE)
              
              recent_commits=$(git log --oneline --since="30 days ago" -- $(COMMON_DIRECTORY)/ 2>/dev/null | wc -l || echo "0")
              echo "- **Commits in last 30 days:** $recent_commits" >> $(TRACKING_FILE)
              
              echo "" >> $(TRACKING_FILE)
              
              # Recent activity
              echo "## 📈 Recent Activity (Last 7 Days)" >> $(TRACKING_FILE)
              echo "" >> $(TRACKING_FILE)
              echo "```" >> $(TRACKING_FILE)
              git log --oneline --since="7 days ago" -- $(COMMON_DIRECTORY)/ | head -10 >> $(TRACKING_FILE) 2>/dev/null || echo "No recent changes" >> $(TRACKING_FILE)
              echo "```" >> $(TRACKING_FILE)
              echo "" >> $(TRACKING_FILE)
              
              # Most imported modules
              echo "## 🏆 Most Used Modules" >> $(TRACKING_FILE)
              echo "" >> $(TRACKING_FILE)
              echo "```" >> $(TRACKING_FILE)
              grep -r "from sth.robert_common" . --include="*.py" 2>/dev/null | \
                cut -d':' -f2 | cut -d' ' -f2 | sort | uniq -c | sort -nr | head -5 >> $(TRACKING_FILE) || echo "No usage found" >> $(TRACKING_FILE)
              echo "```" >> $(TRACKING_FILE)
              echo "" >> $(TRACKING_FILE)
              
              # File-by-file usage
              echo "## 📂 Detailed Usage by File" >> $(TRACKING_FILE)
              echo "" >> $(TRACKING_FILE)
              grep -r "from sth.robert_common" . --include="*.py" 2>/dev/null | while IFS=':' read -r file import_line; do
                echo "- **$file**: \`$import_line\`" >> $(TRACKING_FILE)
              done || echo "No detailed usage found" >> $(TRACKING_FILE)
              
              echo "" >> $(TRACKING_FILE)
              echo "---" >> $(TRACKING_FILE)
              echo "*Report generated on $(date) by Azure DevOps Pipeline*" >> $(TRACKING_FILE)
              
              echo "✅ Usage report generated successfully"
            displayName: "Generate Usage Report"

          # STEP 5: GitHub Integration (if authenticated)
          - script: |
              echo "Attempting GitHub integration..."
              
              if gh auth status >/dev/null 2>&1; then
                echo "🔍 Searching GitHub for cross-repository usage..."
                
                echo "" >> $(TRACKING_FILE)
                echo "## 🌐 Cross-Repository Usage (GitHub Search)" >> $(TRACKING_FILE)
                echo "" >> $(TRACKING_FILE)
                
                # Search for usage in GitHub
                gh search code "sth.robert_common language:python" --json repository,path --limit 10 2>/dev/null | \
                  jq -r '.[] | "- [\(.path)](\(.repository.html_url)/blob/main/\(.path)) in \(.repository.full_name)"' >> $(TRACKING_FILE) || \
                  echo "- No cross-repository usage found (requires org-level access)" >> $(TRACKING_FILE)
                
                echo "✅ GitHub integration completed"
              else
                echo "⚠️  GitHub not authenticated - skipping cross-repo analysis"
                echo "" >> $(TRACKING_FILE)
                echo "## 🌐 Cross-Repository Usage" >> $(TRACKING_FILE)
                echo "*GitHub authentication required for cross-repository analysis*" >> $(TRACKING_FILE)
              fi
            displayName: "GitHub Cross-Repository Analysis"
            env:
              GITHUB_TOKEN: $(GITHUB_TOKEN)
            condition: succeededOrFailed()

          # STEP 6: Publish report as artifact
          - task: PublishBuildArtifacts@1
            inputs:
              pathToPublish: '$(TRACKING_FILE)'
              artifactName: 'common-code-usage-report'
              publishLocation: 'Container'
            displayName: "Publish Usage Report Artifact"

          # STEP 7: Display summary in pipeline logs
          - script: |
              echo "📋 USAGE TRACKING SUMMARY"
              echo "========================="
              echo ""
              cat $(TRACKING_FILE)
              echo ""
              echo "📄 Full report published as pipeline artifact: 'common-code-usage-report'"
              echo "🔗 Download the report from the pipeline run artifacts section"
            displayName: "Display Report Summary"
```

## 🎯 **Key Features of This Pipeline:**

1. **Triggers only on changes** to `sth/robert_common/**`
2. **Uses GitHub CLI** for cross-repository analysis
3. **Generates comprehensive reports** with statistics and usage details
4. **Publishes artifacts** that you can download
5. **Handles authentication failures** gracefully
6. **Provides detailed logging** for troubleshooting

## 🚨 **Common Issues & Solutions**

### **Issue: "No hosted parallelism has been purchased or granted"**

**This is a Microsoft limitation for Azure DevOps hosted agents.**

#### **Solution 1: Request Free Parallelism (Recommended)**
1. Fill out the form: https://aka.ms/azpipelines-parallelism-request
2. **Requirements:**
   - Valid Azure DevOps organization
   - Public project (recommended)
   - Brief explanation of your project
3. **Wait time:** Usually 2-3 business days for approval

#### **Solution 2: Use Self-Hosted Agent**
```yaml
# Replace the pool section in your pipeline with:
pool:
  name: 'Default'  # Use your self-hosted agent pool
  # OR
  name: 'your-self-hosted-pool-name'

# Instead of:
# pool:
#   vmImage: ubuntu-latest  # This requires hosted parallelism
```

#### **Solution 3: Switch to GitHub Actions (Alternative)**
Since you're already using GitHub, you can use the GitHub Actions workflow instead:
- File: `.github/workflows/track-common-usage.yml`
- GitHub provides 2000 free minutes/month for public repos
- No additional setup required

#### **Solution 4: Purchase Hosted Parallelism**
- Cost: ~$40/month for Microsoft-hosted agents
- Go to: `Organization Settings → Billing → Parallel jobs`

### **Recommended Approach:**

1. **Immediate:** Use GitHub Actions (already set up)
2. **Long-term:** Request free Azure DevOps parallelism for more integration options

### **GitHub Actions vs Azure DevOps Comparison:**

| Feature | GitHub Actions | Azure DevOps |
|---------|---------------|---------------|
| **Cost** | Free (2000 min/month) | Requires parallelism request |
| **Setup** | Already configured | Needs variable groups |
| **Integration** | Native GitHub features | More enterprise features |
| **Artifacts** | GitHub releases/pages | Azure DevOps artifacts |

## 🎯 **Immediate Fix - Use GitHub Actions:**

Your GitHub Actions workflow (`.github/workflows/track-common-usage.yml`) will work immediately without any parallelism restrictions!

```bash
# To trigger the GitHub Actions workflow:
git add .
git commit -m "feat: trigger GitHub Actions tracking workflow"
git push origin main
```

## 📋 **Prerequisites Checklist:**
