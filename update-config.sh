#!/bin/bash
# Helper script to update docusaurus.config.js with your GitHub username

echo "================================================"
echo "  Update Docusaurus Config for Deployment"
echo "================================================"
echo ""

# Check if username is provided
if [ -z "$1" ]; then
    echo "Usage: ./update-config.sh YOUR_GITHUB_USERNAME"
    echo ""
    echo "Example: ./update-config.sh johndoe"
    echo ""
    echo "Or use: bash update-config.sh YOUR_GITHUB_USERNAME"
    exit 1
fi

GITHUB_USER="$1"

echo "Updating docusaurus.config.js..."
echo "GitHub Username: $GITHUB_USER"
echo ""

# Create backup
cp docusaurus.config.js docusaurus.config.js.backup
echo "✓ Created backup: docusaurus.config.js.backup"

# Replace YOUR_USERNAME with actual username
sed -i "s/YOUR_USERNAME/${GITHUB_USER}/g" docusaurus.config.js

# Count replacements
COUNT=$(grep -c "$GITHUB_USER" docusaurus.config.js)
echo "✓ Updated $COUNT instances"

echo ""
echo "================================================"
echo "  Configuration Updated Successfully!"
echo "================================================"
echo ""
echo "Your site will be:"
echo "  https://${GITHUB_USER}.github.io/hack_book/"
echo ""
echo "Next steps:"
echo "  1. Create GitHub repo: https://github.com/new"
echo "  2. Repository name: hack_book"
echo "  3. Make it Public"
echo "  4. Run: git remote add origin https://github.com/${GITHUB_USER}/hack_book.git"
echo "  5. Run: git push -u origin main"
echo "  6. Run: npm run deploy"
echo ""
