---
description: "Task list for AI-driven Book Creation Workflow implementation"
---

# Tasks: AI-driven Book Creation Workflow

**Feature**: 002-ai-book-workflow
**Branch**: `002-ai-book-workflow`
**Input**: Design documents from `/specs/002-ai-book-workflow/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Tests**: Not explicitly requested in spec - focusing on manual validation and automated linting/testing tools

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a **web static site** project using Docusaurus:
- **Content**: `docs/` (Markdown files)
- **Config**: Root directory (`docusaurus.config.js`, `sidebars.js`, `package.json`)
- **Static assets**: `static/img/`
- **Custom components**: `src/components/`, `src/pages/`
- **Spec-Kit Plus**: `.specify/`, `specs/`
- **History**: `history/prompts/`, `history/adr/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Node.js/Docusaurus structure

- [X] T001 Install Node.js 20.x LTS and verify installation with `node --version`
- [X] T002 Initialize Docusaurus v3 project in repository root with `npx create-docusaurus@latest . classic --typescript`
- [X] T003 [P] Install testing dependencies: markdownlint-cli2, markdown-link-check, @axe-core/cli in package.json devDependencies
- [X] T004 [P] Create .gitignore file with node_modules/, build/, .docusaurus/, .env
- [X] T005 [P] Create .nvmrc file with Node.js version 20 to lock Node version

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Docusaurus configuration and project structure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Configure docusaurus.config.js with project metadata: title="Physical AI & Humanoid Robotics Coursebook", tagline, GitHub repo URL
- [X] T007 Create directory structure: docs/chapter-01/ through docs/chapter-06/, static/img/chapter-01/ through static/img/chapter-06/
- [X] T008 Configure sidebars.js with chapter navigation structure (6 chapters: Foundations, Perception, Motion & Control, Learning, Integration, Applications)
- [X] T009 [P] Add test scripts to package.json: test:lint (markdownlint-cli2), test:links (markdown-link-check), test:build (docusaurus build), test:all
- [X] T010 [P] Create .markdownlint.json configuration file with Docusaurus-compatible rules
- [X] T011 [P] Update package.json scripts: start (docusaurus start), build (docusaurus build), deploy (docusaurus deploy)
- [X] T012 Create docs/intro.md with coursebook introduction and overview per constitution requirements

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create a new AI-driven book project (Priority: P1) 🎯 MVP

**Goal**: A user can successfully set up a complete Docusaurus project with Spec-Kit Plus integration, configured for the Physical AI & Humanoid Robotics coursebook, with all prerequisites installed and basic structure ready.

**Independent Test**:
- Run `npm start` and verify Docusaurus site loads at http://localhost:3000
- Verify all 6 chapter directories exist in docs/
- Verify Spec-Kit Plus templates are present in .specify/
- Verify constitution.md exists with coursebook governance
- Verify GitHub repository is initialized with correct remote

**Acceptance Criteria** (from spec.md):
- Given: User has Node.js, Git, and GitHub account
- When: User follows initial setup steps
- Then: New Docusaurus project initialized, GitHub repository created, Spec-Kit Plus configured

### Implementation for User Story 1

- [ ] T013 [P] [US1] Copy Spec-Kit Plus infrastructure: clone spec-kit-plus repo temporarily, copy .specify/ and .claude/ directories to project root, delete temporary clone
- [ ] T014 [P] [US1] Create README.md with project overview, setup instructions, and links to constitution and quickstart guide
- [ ] T015 [US1] Verify .specify/memory/constitution.md exists with Physical AI & Humanoid Robotics coursebook constitution (already created)
- [ ] T016 [US1] Initialize Git repository with `git init` and create initial commit with message "docs: initial Docusaurus setup with Spec-Kit Plus"
- [ ] T017 [US1] Create GitHub repository using `gh repo create hack_book --public --source=. --remote=origin` (or manual creation)
- [ ] T018 [US1] Push initial commit to GitHub: `git push -u origin 002-ai-book-workflow`
- [ ] T019 [US1] Verify local development server works: run `npm start`, open http://localhost:3000, check navigation
- [ ] T020 [US1] Run initial validation: `npm run test:lint` and `npm run test:build` to ensure no errors

**Checkpoint**: At this point, User Story 1 should be fully functional - complete project setup ready for content generation

---

## Phase 4: User Story 2 - Generate book content using Claude Code (Priority: P1)

**Goal**: A user can leverage Claude Code to automatically generate well-structured, technically accurate book content (chapters, sections, exercises) based on specifications defined with Spec-Kit Plus.

**Independent Test**:
- Run `/sp.specify` to create a chapter specification
- Run `/sp.plan` to generate chapter plan
- Run `/sp.tasks` to break down chapter tasks
- Run `/sp.implement` to generate chapter content
- Verify generated content appears in docs/chapter-XX/ with proper structure
- Verify generated content passes `npm run test:lint` and `npm run test:links`
- Manually review one section for technical accuracy and completeness

**Acceptance Criteria** (from spec.md):
- Given: Defined specification in Spec-Kit Plus
- When: User invokes Claude Code with appropriate prompts
- Then: Well-structured, technically accurate content generated and integrated into Docusaurus project

### Implementation for User Story 2

**Substep 2A: Chapter 1 Specification & Planning**

- [ ] T021 [US2] Create Chapter 1 specification: run `/sp.specify` with feature name "chapter-01-foundations" and description of chapter requirements
- [ ] T022 [US2] Generate Chapter 1 plan: run `/sp.plan` to create specs/chapter-01-foundations/plan.md with technical approach
- [ ] T023 [US2] Generate Chapter 1 tasks: run `/sp.tasks` to create specs/chapter-01-foundations/tasks.md with content generation breakdown

**Substep 2B: Chapter 1 Content Generation**

- [ ] T024 [P] [US2] Generate Chapter 1 introduction: use Claude Code to create docs/chapter-01/index.md with frontmatter, introduction, learning objectives per chapter-contract.md
- [ ] T025 [P] [US2] Generate Chapter 1 Section 1: create docs/chapter-01/what-is-physical-ai.md with key concepts, definitions, examples
- [ ] T026 [P] [US2] Generate Chapter 1 Section 2: create docs/chapter-01/embodied-intelligence.md with theory, applications, diagrams
- [ ] T027 [P] [US2] Generate Chapter 1 Section 3: create docs/chapter-01/system-components.md with architecture overview, block diagrams
- [ ] T028 [US2] Generate Chapter 1 exercises: create docs/chapter-01/exercises.md with 3-5 exercises following exercise-contract.md (mix of programming, conceptual, simulation)
- [ ] T029 [US2] Add Chapter 1 references section to docs/chapter-01/index.md with at least 5 IEEE/APA formatted citations
- [ ] T030 [US2] Update sidebars.js to include all Chapter 1 sections in navigation

**Substep 2C: Content Validation**

- [ ] T031 [US2] Run markdown linting on Chapter 1: `npm run test:lint` and fix any formatting issues
- [ ] T032 [US2] Verify Chapter 1 links: `npm run test:links` for docs/chapter-01/*.md and fix broken links
- [ ] T033 [US2] Manual content review: verify Chapter 1 technical accuracy, completeness of learning objectives, exercise quality
- [ ] T034 [US2] Test Chapter 1 locally: run `npm start`, navigate to Chapter 1, verify all sections render correctly, images load, navigation works

**Substep 2D: Content Generation Workflow Documentation**

- [ ] T035 [P] [US2] Create content-generation-guide.md in specs/002-ai-book-workflow/ documenting the workflow: specify → plan → tasks → implement → validate
- [ ] T036 [P] [US2] Create chapter-template.md in .specify/templates/ with standard chapter frontmatter and structure for reuse
- [ ] T037 [P] [US2] Create exercise-template.md in .specify/templates/ with standard exercise format per exercise-contract.md

**Checkpoint**: At this point, User Story 2 should be fully functional - complete workflow for generating one chapter with AI, validated and integrated

---

## Phase 5: User Story 3 - Deploy the book to GitHub Pages (Priority: P2)

**Goal**: A user can publish their AI-generated Docusaurus book to GitHub Pages for public access.

**Independent Test**:
- Push changes to GitHub main branch
- Verify GitHub Actions workflow triggers automatically
- Check GitHub Actions logs for successful build and deployment
- Visit https://YOUR_USERNAME.github.io/hack_book/ and verify site is live
- Test navigation, links, and content rendering on deployed site
- Verify no console errors in browser developer tools

**Acceptance Criteria** (from spec.md):
- Given: Complete Docusaurus book project
- When: User follows deployment instructions
- Then: Book is published and accessible through GitHub Pages

### Implementation for User Story 3

**Substep 3A: GitHub Actions Workflow Setup**

- [ ] T038 [US3] Create .github/workflows/ directory in repository root
- [ ] T039 [US3] Create .github/workflows/deploy.yml with GitHub Actions workflow for Docusaurus deployment (Ubuntu latest, Node 20, npm ci, build, deploy to gh-pages)
- [ ] T040 [US3] Configure workflow to run on push to main branch and pull request to main
- [ ] T041 [US3] Add test steps to workflow before deployment: run npm run test:lint, test:links, test:build to catch errors

**Substep 3B: GitHub Pages Configuration**

- [ ] T042 [US3] Update docusaurus.config.js with correct GitHub Pages URLs: url (https://USERNAME.github.io), baseUrl (/hack_book/), organizationName, projectName
- [ ] T043 [US3] Configure GitHub repository settings: Settings → Pages → Source: Deploy from a branch → Branch: gh-pages / (root)
- [ ] T044 [US3] Add GitHub Pages URL to README.md for easy access

**Substep 3C: Deployment Execution & Validation**

- [ ] T045 [US3] Commit all changes with conventional commit message: "feat: add GitHub Actions deployment workflow"
- [ ] T046 [US3] Push to GitHub: `git push origin 002-ai-book-workflow` to trigger workflow
- [ ] T047 [US3] Monitor GitHub Actions run: check Actions tab, verify build and deploy steps succeed, review logs for any warnings
- [ ] T048 [US3] Wait for GitHub Pages deployment (2-5 minutes) and visit live site at https://USERNAME.github.io/hack_book/
- [ ] T049 [US3] Validate deployed site: test navigation, verify Chapter 1 content loads, check images render, test responsive design on mobile
- [ ] T050 [US3] Run accessibility check on live site: use @axe-core/cli or browser extension to verify WCAG 2.1 AA compliance

**Substep 3D: Continuous Deployment Documentation**

- [ ] T051 [P] [US3] Create deployment-guide.md in specs/002-ai-book-workflow/ with step-by-step deployment instructions, troubleshooting tips
- [ ] T052 [P] [US3] Update README.md with "View Live Book" badge linking to GitHub Pages URL
- [ ] T053 [P] [US3] Document deployment workflow in constitution.md under Version Control & Deployment section

**Checkpoint**: All user stories should now be independently functional - complete AI-driven book creation workflow with live deployment

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T054 [P] Update quickstart.md with any learnings or improvements from actual implementation
- [ ] T055 [P] Create CONTRIBUTING.md with guidelines for content contributors, review process, coding standards
- [ ] T056 [P] Add GitHub issue templates: bug report, feature request, content suggestion in .github/ISSUE_TEMPLATE/
- [ ] T057 [P] Add pull request template in .github/PULL_REQUEST_TEMPLATE.md with checklist for content PRs
- [ ] T058 Run complete validation suite: `npm run test:all` on entire project and fix any remaining issues
- [ ] T059 Performance audit: run Lighthouse on deployed site, ensure >90 scores for Performance, Accessibility, Best Practices, SEO
- [ ] T060 [P] Create maintenance-guide.md documenting how to add new chapters, update content, manage versions
- [ ] T061 [P] Set up Dependabot for automated dependency updates: create .github/dependabot.yml
- [ ] T062 Final commit: "docs: complete AI-driven book creation workflow implementation" and push to GitHub
- [ ] T063 Create release tag: `git tag -a v1.0.0 -m "First complete implementation of AI book workflow"` and push tag

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-5)**: All depend on Foundational phase completion
  - **User Story 1 (Phase 3)**: Can start after Foundational - Must complete first (prerequisite for US2 and US3)
  - **User Story 2 (Phase 4)**: Depends on User Story 1 completion (needs project setup)
  - **User Story 3 (Phase 5)**: Depends on User Story 2 completion (needs content to deploy)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

**Critical Path** (must be sequential):
1. **User Story 1 (P1)** → **User Story 2 (P1)** → **User Story 3 (P2)**

**Rationale**:
- US2 needs the project setup from US1 (Docusaurus installed, Git configured)
- US3 needs content from US2 (can't deploy empty site)

**Note**: While these stories have dependencies, within each story many tasks can run in parallel (marked with [P])

### Within Each User Story

**User Story 1**:
- T013-T015 can run in parallel (copying templates, creating README, verifying constitution)
- T016-T018 must be sequential (git init → create repo → push)
- T019-T020 run after push

**User Story 2**:
- T021-T023 must be sequential (specify → plan → tasks)
- T024-T027 can run in parallel (different section files)
- T028-T030 sequential after sections complete
- T031-T034 sequential validation
- T035-T037 can run in parallel (documentation)

**User Story 3**:
- T038-T041 sequential (workflow setup)
- T042-T044 can run in parallel (configuration files)
- T045-T050 sequential (deploy and validate)
- T051-T053 can run in parallel (documentation)

### Parallel Opportunities

**Setup Phase**:
- T003, T004, T005 can run in parallel (different files)

**Foundational Phase**:
- T007 (directory structure) can start after T006 (config)
- T009, T010, T011 can run in parallel (different config files)

**User Story 1**:
- T013, T014, T015 can run in parallel

**User Story 2**:
- T024, T025, T026, T027 can run in parallel (different section files)
- T035, T036, T037 can run in parallel (different template files)

**User Story 3**:
- T042, T043, T044 can run in parallel (different configuration tasks)
- T051, T052, T053 can run in parallel (different documentation files)

**Polish Phase**:
- T054, T055, T056, T057, T060, T061 can run in parallel (different files)

---

## Parallel Example: User Story 2 - Section Generation

```bash
# After T023 completes, launch all section generation tasks in parallel:
Task: "Generate Chapter 1 introduction in docs/chapter-01/index.md"
Task: "Generate Chapter 1 Section 1 in docs/chapter-01/what-is-physical-ai.md"
Task: "Generate Chapter 1 Section 2 in docs/chapter-01/embodied-intelligence.md"
Task: "Generate Chapter 1 Section 3 in docs/chapter-01/system-components.md"

# After sections complete, run validation:
Task: "Generate Chapter 1 exercises in docs/chapter-01/exercises.md"
Task: "Add references to docs/chapter-01/index.md"
Task: "Update sidebars.js"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T012) - CRITICAL
3. Complete Phase 3: User Story 1 (T013-T020)
4. **STOP and VALIDATE**:
   - Run `npm start` and verify site loads
   - Check all directories exist
   - Verify Git repository connected to GitHub
5. **MVP ACHIEVED**: Complete project setup ready for content generation

### Incremental Delivery

1. **Foundation**: Complete Setup + Foundational → Basic Docusaurus site running
2. **MVP (US1)**: Complete User Story 1 → Full project setup with Spec-Kit Plus
3. **Content (US2)**: Complete User Story 2 → One chapter generated and validated
4. **Published (US3)**: Complete User Story 3 → Live book on GitHub Pages
5. **Production Ready**: Complete Polish → Documented, tested, maintainable

Each increment adds value and is independently testable.

### Suggested Execution Order

**Week 1: Foundation & Setup**
- Day 1-2: Phase 1 + Phase 2 (T001-T012)
- Day 3-4: Phase 3 / User Story 1 (T013-T020)
- Day 5: Validate MVP, fix issues

**Week 2: Content Generation**
- Day 1-2: User Story 2 specification/planning (T021-T023)
- Day 3-4: User Story 2 content generation (T024-T034)
- Day 5: User Story 2 documentation (T035-T037)

**Week 3: Deployment & Polish**
- Day 1-2: User Story 3 deployment (T038-T050)
- Day 3: User Story 3 documentation (T051-T053)
- Day 4-5: Phase 6 Polish (T054-T063)

**Total Estimated Time**: 3 weeks for complete workflow implementation (single developer)

---

## Task Statistics

**Total Tasks**: 63
- **Setup (Phase 1)**: 5 tasks
- **Foundational (Phase 2)**: 7 tasks (CRITICAL PATH)
- **User Story 1 (Phase 3)**: 8 tasks
- **User Story 2 (Phase 4)**: 17 tasks (largest - content generation)
- **User Story 3 (Phase 5)**: 16 tasks
- **Polish (Phase 6)**: 10 tasks

**Parallel Opportunities**: 21 tasks marked [P] (33% of total)

**Independent Test Criteria Defined**: Yes, for all 3 user stories

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (20 tasks, ~40-60 minutes per quickstart goal)

---

## Notes

- **[P] tasks** = different files, no dependencies within phase
- **[Story] label** maps task to specific user story for traceability
- **Tests**: Not included as test tasks since spec doesn't explicitly request TDD; validation tasks (T031-T034, T049-T050) serve as acceptance testing
- **Commit strategy**: Commit after completing each user story phase
- **Verification**: Each user story has explicit "Independent Test" criteria
- **Time estimates**: Based on quickstart.md target of 60 minutes for basic setup (MVP = US1)
- **Extensibility**: After completing these tasks, repeat User Story 2 workflow for remaining chapters (2-6)

---

## Next Steps After Implementation

Once all tasks complete:

1. **Extend to remaining chapters**: Use User Story 2 workflow (T021-T037) as template to generate Chapters 2-6
2. **Add advanced features**:
   - Algolia DocSearch for search functionality
   - Blog for updates and tutorials
   - Versioned docs for multiple editions
   - PDF export for offline reading
3. **Community building**:
   - Set up GitHub Discussions
   - Add contributing guidelines for external contributors
   - Create issue templates for content suggestions
4. **Analytics & feedback**:
   - Add Google Analytics or Plausible
   - Create feedback forms
   - Monitor usage and iterate

---

## Format Validation

✅ **All tasks follow required format**: `- [ ] [ID] [P?] [Story?] Description with file path`
✅ **Sequential IDs**: T001-T063 in execution order
✅ **Story labels applied**: US1, US2, US3 correctly assigned to user story phases
✅ **Parallel markers**: [P] applied to 21 tasks with no dependencies
✅ **File paths included**: All implementation tasks specify exact file locations
✅ **Checkboxes present**: All tasks start with `- [ ]` for tracking
