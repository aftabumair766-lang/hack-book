# Quickstart Guide: AI-driven Book Creation Workflow

**Feature**: 002-ai-book-workflow
**Date**: 2025-12-01
**Audience**: Beginners to AI-driven book creation with basic command-line knowledge

## Overview

This guide walks you through creating a technical coursebook using **Spec-Kit Plus**, **Claude Code**, and **Docusaurus**, then deploying it to **GitHub Pages**. You'll have a live book website in ~60 minutes.

---

## Prerequisites

Before starting, ensure you have:

### Required Software

1. **Node.js 20.x LTS** ([Download](https://nodejs.org/))
   - Verify: `node --version` (should show v20.x.x)

2. **Git** ([Download](https://git-scm.com/))
   - Verify: `git --version`

3. **GitHub Account** ([Sign up](https://github.com/signup))
   - Free account is sufficient

4. **Code Editor** (e.g., VS Code, Cursor)

5. **Claude Code CLI** ([Install](https://www.claude.com/product/claude-code))
   - Verify: `claude --version`

### Optional but Recommended

- **nvm** (Node Version Manager) for managing Node.js versions
- **GitHub CLI** (`gh`) for easier repository management

---

## Part 1: Project Setup (15 minutes)

### Step 1: Initialize Your Book Project

```bash
# Create project directory
mkdir my-coursebook
cd my-coursebook

# Initialize Git repository
git init
git branch -M main

# Initialize Node.js project
npm init -y
```

### Step 2: Install Docusaurus

```bash
# Install Docusaurus (choose "classic" template when prompted)
npx create-docusaurus@latest . classic

# If directory not empty, use --force flag
# npx create-docusaurus@latest . classic --force
```

**What this does**:
- Creates Docusaurus project structure
- Installs dependencies (React, Webpack, etc.)
- Generates default configuration files

### Step 3: Install Spec-Kit Plus

```bash
# Clone Spec-Kit Plus templates
git clone https://github.com/panaversity/spec-kit-plus.git .temp-spec-kit
cp -r .temp-spec-kit/.specify .
cp -r .temp-spec-kit/.claude .
rm -rf .temp-spec-kit

# Or manually download and extract to project root
```

**What this does**:
- Adds `.specify/` directory with templates
- Adds `.claude/` directory with slash commands
- Provides structured development workflow

### Step 4: Create Project Constitution

```bash
# Using Claude Code (if available)
claude /sp.constitution

# Or manually create .specify/memory/constitution.md
# Follow template in .specify/templates/constitution-template.md
```

**What to define**:
- Project purpose and scope
- Target audience
- Content standards (formatting, style, citations)
- Chapter structure
- Roles and responsibilities

---

## Part 2: Configure Your Book (10 minutes)

### Step 5: Customize Docusaurus Config

Edit `docusaurus.config.js`:

```javascript
module.exports = {
  title: 'Physical AI & Humanoid Robotics Coursebook',
  tagline: 'Learn embodied intelligence and robotics',
  url: 'https://YOUR_USERNAME.github.io',
  baseUrl: '/YOUR_REPO_NAME/',
  organizationName: 'YOUR_USERNAME',
  projectName: 'YOUR_REPO_NAME',

  themeConfig: {
    navbar: {
      title: 'Coursebook',
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Chapters',
        },
        {
          href: 'https://github.com/YOUR_USERNAME/YOUR_REPO_NAME',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
  },
};
```

**Replace**:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO_NAME` with your repository name

### Step 6: Set Up Content Structure

```bash
# Create chapter directories
mkdir -p docs/chapter-01
mkdir -p docs/chapter-02
mkdir -p docs/chapter-03
# ... (repeat for all chapters)

# Create image directories
mkdir -p static/img/chapter-01
mkdir -p static/img/chapter-02
# ... (repeat for all chapters)
```

### Step 7: Configure Sidebar Navigation

Edit `sidebars.js`:

```javascript
module.exports = {
  coursebookSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Chapter 1: Foundations',
      items: [
        'chapter-01/index',
        'chapter-01/what-is-physical-ai',
        'chapter-01/exercises',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: Perception',
      items: [
        'chapter-02/index',
        // ... add sections
      ],
    },
    // ... add remaining chapters
  ],
};
```

---

## Part 3: Generate Content with AI (20 minutes)

### Step 8: Create Chapter Specification

For each chapter, define what to create:

```bash
# Using Claude Code
claude /sp.specify

# Answer prompts:
# - Feature name: chapter-01-foundations
# - Description: Foundations of Physical AI chapter with intro, concepts, and exercises
```

**What this creates**:
- `specs/chapter-01-foundations/spec.md` with requirements
- User stories and acceptance criteria
- Success metrics

### Step 9: Plan Chapter Architecture

```bash
# Generate technical plan
claude /sp.plan

# This creates:
# - specs/chapter-01-foundations/plan.md
# - specs/chapter-01-foundations/research.md
# - specs/chapter-01-foundations/data-model.md
```

### Step 10: Generate Tasks

```bash
# Break down implementation into tasks
claude /sp.tasks

# This creates:
# - specs/chapter-01-foundations/tasks.md with actionable items
```

### Step 11: Implement Content

```bash
# Use Claude Code to generate chapter content
claude /sp.implement

# Or manually prompt Claude Code:
claude "Generate Chapter 1 content based on specs/chapter-01-foundations/spec.md"
```

**What to generate**:
- Chapter introduction (`docs/chapter-01/index.md`)
- Section content (`docs/chapter-01/what-is-physical-ai.md`, etc.)
- Exercises (`docs/chapter-01/exercises.md`)
- Diagrams (describe to Claude Code, then create in tool like draw.io)

### Step 12: Review and Validate Content

```bash
# Test local development server
npm start

# Opens browser at http://localhost:3000
# Verify:
# - Chapter appears in sidebar
# - Content renders correctly
# - Links work
# - Images load
```

**Manual review checklist**:
- [ ] Technical accuracy (have expert review if possible)
- [ ] Grammar and clarity
- [ ] Code examples are runnable
- [ ] Exercises have all required fields (objective, materials, instructions, outcome)
- [ ] Citations are properly formatted

---

## Part 4: Testing & Quality Assurance (10 minutes)

### Step 13: Install Testing Tools

```bash
# Markdown linting
npm install --save-dev markdownlint-cli2

# Link checking
npm install --save-dev markdown-link-check

# Accessibility testing
npm install --save-dev @axe-core/cli
```

### Step 14: Add Test Scripts to package.json

```json
{
  "scripts": {
    "start": "docusaurus start",
    "build": "docusaurus build",
    "test:lint": "markdownlint-cli2 \"docs/**/*.md\"",
    "test:links": "markdown-link-check docs/**/*.md",
    "test:build": "npm run build",
    "test:all": "npm run test:lint && npm run test:links && npm run test:build"
  }
}
```

### Step 15: Run Tests

```bash
# Run all tests
npm run test:all

# Or individually:
npm run test:lint     # Check markdown formatting
npm run test:links    # Verify no broken links
npm run test:build    # Ensure build succeeds
```

**Fix any errors** before proceeding to deployment.

---

## Part 5: Deployment to GitHub Pages (5 minutes)

### Step 16: Create GitHub Repository

```bash
# Using GitHub CLI (recommended)
gh repo create my-coursebook --public --source=. --remote=origin

# Or manually:
# 1. Go to https://github.com/new
# 2. Create repository "my-coursebook"
# 3. Follow instructions to add remote
```

### Step 17: Set Up GitHub Actions Deployment

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build website
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

### Step 18: Enable GitHub Pages

1. Go to repository Settings → Pages
2. Source: Select "Deploy from a branch"
3. Branch: Select `gh-pages` / `/ (root)`
4. Save

### Step 19: Push and Deploy

```bash
# Stage all files
git add .

# Commit with conventional commit message
git commit -m "docs: initial coursebook setup with chapter 1"

# Push to GitHub (triggers deployment)
git push -u origin main
```

**Wait ~2-5 minutes** for GitHub Actions to complete deployment.

### Step 20: Verify Live Site

Visit: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

✅ Your book is now live!

---

## Part 6: Iterative Content Generation (Ongoing)

### Adding More Chapters

Repeat Steps 8-12 for each chapter:

```bash
# For each chapter:
claude /sp.specify    # Define requirements
claude /sp.plan       # Plan architecture
claude /sp.tasks      # Break down work
claude /sp.implement  # Generate content

# Review, test, commit
npm run test:all
git add .
git commit -m "docs: add chapter 2 - perception"
git push
```

### Content Update Workflow

```bash
# Make changes to content
# (Edit docs/*.md files)

# Test locally
npm start

# Run tests
npm run test:all

# Commit and deploy
git add .
git commit -m "docs: update chapter 1 exercises"
git push
```

---

## Troubleshooting

### Common Issues

**Issue**: `npm start` fails with port error
```bash
# Solution: Kill process on port 3000 or use different port
npm start -- --port 3001
```

**Issue**: GitHub Pages shows 404
- Check `baseUrl` in `docusaurus.config.js` matches repo name
- Ensure `gh-pages` branch exists and is set as source
- Wait 5-10 minutes for DNS propagation

**Issue**: Images not loading
- Verify images are in `static/img/` directory
- Use correct path in Markdown: `![alt](../../static/img/chapter-01/image.png)`
- Or use absolute path: `![alt](/img/chapter-01/image.png)`

**Issue**: Build fails in GitHub Actions
- Check build logs in Actions tab
- Run `npm run build` locally to reproduce
- Common causes: broken links, invalid frontmatter, missing dependencies

**Issue**: Claude Code not generating accurate content
- Provide more detailed specifications in spec.md
- Include example content structure
- Review and edit generated content for technical accuracy
- Use `/sp.clarify` command to refine specifications

---

## Best Practices

### Version Control
- ✅ Commit frequently with descriptive messages
- ✅ Use conventional commits: `docs:`, `feat:`, `fix:`
- ✅ Create feature branches for major changes
- ✅ Tag releases: `git tag v1.0.0`

### Content Quality
- ✅ Have technical expert review each chapter
- ✅ Test all code examples in a real environment
- ✅ Include safety notes for hardware exercises
- ✅ Maintain consistent terminology throughout

### Performance
- ✅ Compress images before adding (<500KB each)
- ✅ Use WebP format where possible
- ✅ Lazy-load images below the fold
- ✅ Keep pages under 10,000 words

### Accessibility
- ✅ Provide alt text for all images
- ✅ Use semantic heading hierarchy (H1 → H2 → H3)
- ✅ Ensure sufficient color contrast
- ✅ Test with screen reader

---

## Next Steps

After completing the quickstart:

1. **Generate remaining chapters** using the workflow above
2. **Set up continuous integration** with automated tests
3. **Enable analytics** (Google Analytics or Plausible)
4. **Add search functionality** (Algolia DocSearch)
5. **Create PDF export** using Docusaurus PDF plugin
6. **Gather feedback** from students/reviewers
7. **Iterate and improve** content based on feedback

---

## Resources

### Documentation
- [Docusaurus Docs](https://docusaurus.io/docs)
- [Spec-Kit Plus GitHub](https://github.com/panaversity/spec-kit-plus)
- [Claude Code Guide](https://www.claude.com/docs/code)
- [GitHub Pages Docs](https://docs.github.com/en/pages)

### Templates
- `.specify/templates/spec-template.md` - Feature specification template
- `.specify/templates/plan-template.md` - Implementation plan template
- `.specify/templates/tasks-template.md` - Task breakdown template

### Community
- [Docusaurus Discord](https://discord.gg/docusaurus)
- [GitHub Discussions](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/discussions)

---

## Estimated Time Breakdown

| Phase | Estimated Time |
|-------|---------------|
| Part 1: Project Setup | 15 minutes |
| Part 2: Configuration | 10 minutes |
| Part 3: Content Generation | 20 minutes |
| Part 4: Testing | 10 minutes |
| Part 5: Deployment | 5 minutes |
| **Total** | **60 minutes** |

*Note: Time for additional chapters scales linearly (~20 min per chapter)*

---

## Success Criteria

You've successfully completed the quickstart when:

- ✅ Docusaurus site runs locally (`npm start`)
- ✅ At least one chapter is fully generated with content
- ✅ All tests pass (`npm run test:all`)
- ✅ Site is deployed and accessible via GitHub Pages URL
- ✅ Content follows constitution standards
- ✅ Navigation and links work correctly

**Congratulations!** You've built an AI-driven technical coursebook. 🎉
