# Research: AI-driven Book Creation Workflow

**Feature**: 002-ai-book-workflow
**Date**: 2025-12-01
**Purpose**: Resolve technical unknowns identified in plan.md

## Research Questions

### 1. Node.js Version Selection

**Question**: What Node.js version should we use for Docusaurus?

**Research Findings**:
- **Docusaurus v3** (latest stable): Requires Node.js 18.0 or higher
- **Docusaurus v2** (previous stable): Requires Node.js 16.14 or higher
- **Recommendation**: Node.js 20.x LTS (Long Term Support)

**Decision**: Use Node.js 20.x LTS (currently 20.11+)

**Rationale**:
- Active LTS with long-term support until April 2026
- Compatible with both Docusaurus v2 and v3
- Better performance and security updates
- Wide ecosystem compatibility

**Alternatives Considered**:
- Node.js 18.x LTS: Shorter support window, older feature set
- Node.js 22.x (Current): Bleeding edge, less stable for production

---

### 2. Docusaurus Version Selection

**Question**: Should we use Docusaurus v2 or v3?

**Research Findings**:
- **Docusaurus v3**: Latest release (stable as of late 2023), React 18, better performance, improved MDX support
- **Docusaurus v2**: Mature, widely adopted, extensive plugin ecosystem
- Current ecosystem: v3 is production-ready

**Decision**: Use Docusaurus v3 (latest stable)

**Rationale**:
- Latest features and performance improvements
- React 18 support for better interactivity
- Improved MDX v3 support for richer content authoring
- Better TypeScript support
- Long-term viability (v2 will eventually be deprecated)

**Alternatives Considered**:
- Docusaurus v2: More conservative choice, but v3 is now stable enough

---

### 3. Automated Testing Strategy

**Question**: What automated testing should we implement for content validation?

**Research Findings**:
- **Link checking**: Broken link detection is critical for documentation
- **Markdown linting**: Ensures consistent formatting
- **Accessibility testing**: WCAG compliance validation
- **Build validation**: CI/CD pipeline to catch errors

**Decision**: Implement multi-layer testing:
1. **Markdown linting**: markdownlint-cli2 for style consistency
2. **Link checking**: markdown-link-check for internal/external links
3. **Accessibility**: @axe-core/cli for WCAG 2.1 AA validation
4. **Build testing**: GitHub Actions to validate `docusaurus build` succeeds

**Rationale**:
- Catches common errors early (broken links, formatting issues)
- Ensures accessibility compliance (constitution requirement)
- Automated via CI/CD reduces manual review burden
- Low overhead, high value

**Alternatives Considered**:
- Manual testing only: Too error-prone for 200+ pages
- Full end-to-end testing: Overkill for static documentation site

---

### 4. Content Generation Automation Details

**Question**: How should Claude Code integrate with the content generation workflow?

**Research Findings**:
- Claude Code can be invoked via CLI or API
- Spec-Kit Plus provides structured prompts for content generation
- Best practice: Use slash commands for repeatable workflows
- Content should be generated chapter-by-chapter with human review

**Decision**: Implement a multi-stage content generation workflow:

**Stage 1: Chapter Specification**
- Use `/sp.specify` to define chapter requirements
- Input: Chapter number, topic, learning objectives
- Output: Detailed specification in specs/chapter-XX/spec.md

**Stage 2: Chapter Planning**
- Use `/sp.plan` to design chapter architecture
- Define section breakdown, exercise types, resource needs
- Output: specs/chapter-XX/plan.md

**Stage 3: Content Generation**
- Use `/sp.implement` with Claude Code to generate:
  - Chapter introduction
  - Section content (with subsections)
  - Practical exercises
  - References
- Human review after each section for technical accuracy

**Stage 4: Integration**
- Copy generated content to docs/chapter-XX/
- Update sidebars.js for navigation
- Run validation tests (links, accessibility, build)

**Rationale**:
- Structured approach ensures consistency
- Chapter-by-chapter generation allows incremental progress
- Human-in-the-loop maintains technical accuracy (constitution requirement)
- Leverages Spec-Kit Plus workflow naturally

**Alternatives Considered**:
- Fully automated generation: Risks technical inaccuracy
- Manual writing only: Defeats purpose of AI-driven workflow

---

### 5. GitHub Pages Deployment Strategy

**Question**: What's the optimal deployment approach for GitHub Pages?

**Research Findings**:
- **GitHub Actions**: Automated CI/CD built into GitHub
- **Docusaurus Deployment**: Native support via `docusaurus deploy`
- **Branch strategy**: gh-pages branch or docs/ folder

**Decision**: Use GitHub Actions workflow with automated deployment

**Workflow**:
1. Push to `main` branch triggers GitHub Actions
2. Action runs: `npm ci && npm run build`
3. Action runs accessibility + link tests
4. Action deploys build/ to `gh-pages` branch
5. GitHub Pages serves from `gh-pages` branch

**Rationale**:
- Fully automated: No manual deployment steps
- CI validation: Catches errors before deployment
- Standard practice: Widely documented, well-supported
- Free for public repositories

**Alternatives Considered**:
- Manual `docusaurus deploy`: Error-prone, requires local builds
- Netlify/Vercel: Adds external dependency, GitHub Pages is sufficient

---

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Runtime** | Node.js | 20.x LTS | JavaScript execution environment |
| **Framework** | Docusaurus | v3 (latest) | Static site generator |
| **Content** | Markdown/MDX | MDX v3 | Content authoring |
| **Styling** | CSS Modules | - | Component styling |
| **Version Control** | Git/GitHub | - | Code management + hosting |
| **Deployment** | GitHub Pages | - | Static site hosting |
| **CI/CD** | GitHub Actions | - | Automated testing + deployment |
| **Development** | Spec-Kit Plus | latest | Structured development workflow |
| **AI Agent** | Claude Code | latest | Content generation |
| **Linting** | markdownlint-cli2 | latest | Markdown validation |
| **Link Checking** | markdown-link-check | latest | Broken link detection |
| **Accessibility** | @axe-core/cli | latest | WCAG compliance validation |

---

## Best Practices Identified

### 1. Version Control
- Use conventional commits: `docs: add chapter 1 intro`
- Feature branches for each chapter: `chapter-01-foundations`
- PR reviews for technical accuracy validation
- Tag releases: `v1.0.0` for major milestones

### 2. Content Organization
- One chapter per directory in docs/
- Each section as separate .md file for maintainability
- exercises.md separate from main content
- images in static/img/chapter-XX/

### 3. Testing Strategy
- Pre-commit hooks: Run markdown linting
- Pre-push: Run link checking
- CI/CD: Full test suite + build validation
- Post-deploy: Manual accessibility spot-check

### 4. Performance Optimization
- Compress images (WebP format where possible)
- Lazy-load heavy diagrams
- Enable Docusaurus search (Algolia or local)
- Minimize custom JavaScript

### 5. Security Considerations
- No API keys or secrets in repository
- Use GitHub Secrets for deployment tokens
- Enable Dependabot for dependency updates
- Regular security audits: `npm audit`

---

## Integration Points

### 1. Spec-Kit Plus ↔ Docusaurus
- specs/ directory: Development specifications
- docs/ directory: Published content
- Flow: spec → plan → tasks → implement → generate content → copy to docs/

### 2. Claude Code ↔ Content Generation
- Input: Chapter spec from specs/chapter-XX/spec.md
- Processing: Claude Code generates structured Markdown
- Output: Draft content for review and integration
- Human oversight: Technical expert reviews each section

### 3. GitHub Actions ↔ Deployment
- Trigger: Push to main branch
- Actions: Build → Test → Deploy
- Output: Live site at username.github.io/hack_book

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| AI-generated content inaccuracy | High | Medium | Mandatory technical expert review for each chapter |
| Broken links after content updates | Medium | High | Automated link checking in CI/CD |
| Accessibility violations | Medium | Medium | axe-core testing + manual spot-checks |
| Docusaurus build failures | High | Low | Pre-commit build validation, GitHub Actions fail-fast |
| GitHub Pages size limit (1GB) | Medium | Low | Monitor build size, compress images, lazy-load resources |
| Node.js version drift | Low | Medium | Lock Node version in .nvmrc + package.json engines |

---

## Open Questions (for User Input)

1. **Chapter prioritization**: Which chapter should we generate first? (Suggested: Chapter 1 - Foundations)
2. **Exercise complexity**: What ratio of beginner/intermediate/advanced exercises per chapter?
3. **Review process**: Who will serve as the Robotics Expert for technical validation?
4. **Deployment timeline**: Should we deploy incrementally (chapter by chapter) or wait for completion?
5. **Custom branding**: Any specific color scheme, logo, or styling requirements for the site?

---

## Next Steps

With research complete, proceed to **Phase 1**:
1. Generate data-model.md (content entities and relationships)
2. Generate API contracts (if applicable - likely N/A for static site)
3. Generate quickstart.md (setup guide)
4. Update agent context with final technology decisions
