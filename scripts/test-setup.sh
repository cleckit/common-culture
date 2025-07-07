#!/bin/bash
# Test script to verify your tracking setup is working

echo "🧪 Testing Common Code Tracking Setup"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

success_count=0
total_tests=0

test_result() {
    total_tests=$((total_tests + 1))
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
        success_count=$((success_count + 1))
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

echo ""
echo "🔍 Testing Local Environment..."

# Test 1: Check if we're in a git repository
git status >/dev/null 2>&1
test_result $? "Git repository detected"

# Test 2: Check if common directory exists
if [ -d "sth/robert_common" ]; then
    test_result 0 "Common directory (sth/robert_common) exists"
else
    test_result 1 "Common directory (sth/robert_common) exists"
fi

# Test 3: Check for Python files in common directory
python_files=$(find sth/robert_common -name "*.py" 2>/dev/null | wc -l)
if [ "$python_files" -gt 0 ]; then
    test_result 0 "Python files found in common directory ($python_files files)"
else
    test_result 1 "Python files found in common directory"
fi

# Test 4: Check for usage of common code
usage_count=$(grep -r "from sth.robert_common" . --include="*.py" 2>/dev/null | wc -l)
if [ "$usage_count" -gt 0 ]; then
    test_result 0 "Common code usage detected ($usage_count import statements)"
else
    test_result 1 "Common code usage detected"
fi

echo ""
echo "🔧 Testing GitHub Integration..."

# Test 5: Check GitHub CLI installation
if command -v gh >/dev/null 2>&1; then
    test_result 0 "GitHub CLI installed"
    
    # Test 6: Check GitHub authentication
    if gh auth status >/dev/null 2>&1; then
        test_result 0 "GitHub CLI authenticated"
        
        # Test 7: Check repository access
        if gh repo view >/dev/null 2>&1; then
            test_result 0 "GitHub repository access confirmed"
        else
            test_result 1 "GitHub repository access (not a GitHub repo or no access)"
        fi
    else
        test_result 1 "GitHub CLI authenticated"
        echo -e "${YELLOW}💡 Run 'gh auth login' to authenticate${NC}"
    fi
else
    test_result 1 "GitHub CLI installed"
    echo -e "${YELLOW}💡 Install GitHub CLI: https://cli.github.com/${NC}"
fi

echo ""
echo "📊 Testing Tracking Functionality..."

# Test 8: Generate sample usage report
echo "# Test Usage Report $(date)" > test_usage_report.md
echo "" >> test_usage_report.md

total_files=$(find sth/robert_common -name "*.py" 2>/dev/null | wc -l)
echo "- Total Python files: $total_files" >> test_usage_report.md

usage_count=$(grep -r "from sth.robert_common" . --include="*.py" 2>/dev/null | wc -l)
echo "- Import statements: $usage_count" >> test_usage_report.md

if [ -f "test_usage_report.md" ] && [ -s "test_usage_report.md" ]; then
    test_result 0 "Usage report generation works"
    rm test_usage_report.md
else
    test_result 1 "Usage report generation works"
fi

echo ""
echo "📋 Test Results Summary"
echo "======================"
echo -e "Passed: ${GREEN}$success_count${NC}/$total_tests tests"

if [ $success_count -eq $total_tests ]; then
    echo -e "${GREEN}🎉 All tests passed! Your tracking setup is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Set up GitHub Personal Access Token in Azure DevOps"
    echo "2. Configure Azure DevOps variable group"
    echo "3. Run your first pipeline"
elif [ $success_count -gt $((total_tests / 2)) ]; then
    echo -e "${YELLOW}⚠️  Most tests passed. Check the failed items above.${NC}"
    echo ""
    echo "See ACTIVATION_GUIDE.md for setup instructions"
else
    echo -e "${RED}❌ Several tests failed. Please complete the setup first.${NC}"
    echo ""
    echo "See ACTIVATION_GUIDE.md for detailed setup instructions"
fi

echo ""
echo "📖 For detailed setup instructions, see:"
echo "   - ACTIVATION_GUIDE.md"
echo "   - SETUP_GITHUB_PERMISSIONS.md" 
echo "   - SETUP_AZURE_DEVOPS.md"
