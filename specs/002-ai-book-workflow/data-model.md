# Data Model: AI-driven Book Creation Workflow

**Feature**: 002-ai-book-workflow
**Date**: 2025-12-01
**Purpose**: Define entities, relationships, and state for the coursebook content structure

## Overview

This data model describes the content entities for the Physical AI & Humanoid Robotics coursebook. Since this is a static documentation site, the "data" is primarily file-based (Markdown) with metadata in frontmatter.

---

## Core Entities

### 1. Book

**Description**: The top-level container for the entire coursebook.

**Attributes**:
- `title`: String - "Physical AI & Humanoid Robotics Coursebook"
- `version`: Semver - Current version (e.g., "1.0.0")
- `authors`: Array<String> - List of primary authors
- `target_audience`: String - "Undergraduate and graduate engineering students, researchers, robotics engineers"
- `chapters`: Array<Chapter> - Ordered list of chapters
- `publication_date`: ISO Date
- `repository_url`: String - GitHub repository URL
- `site_url`: String - Deployed GitHub Pages URL

**Relationships**:
- Has many Chapters (1:N)

**File Location**: Root metadata in `docusaurus.config.js`

---

### 2. Chapter

**Description**: A major division of the coursebook covering a specific topic area.

**Attributes**:
- `chapter_number`: Integer (1-6)
- `title`: String
- `slug`: String - URL-friendly identifier
- `description`: String - Brief overview
- `learning_objectives`: Array<String>
- `estimated_reading_time`: Integer (minutes)
- `sections`: Array<Section>
- `exercises`: Array<Exercise>
- `references`: Array<Reference>

**Example**:
```yaml
chapter_number: 1
title: "Foundations of Physical AI"
slug: "chapter-01"
description: "Introduction to embodied intelligence and the intersection of AI with physical systems"
learning_objectives:
  - "Understand the principles of embodied intelligence"
  - "Differentiate between virtual and physical AI systems"
estimated_reading_time: 45
```

**Relationships**:
- Belongs to Book (N:1)
- Has many Sections (1:N)
- Has many Exercises (1:N)
- Has many References (1:N)

**File Location**: `docs/chapter-XX/index.md` (frontmatter + content)

**Validation Rules**:
- chapter_number must be unique and sequential
- slug must match directory name
- Must have at least 3 learning objectives
- Must have at least 1 section

---

### 3. Section

**Description**: A subdivision of a chapter focusing on a specific concept or topic.

**Attributes**:
- `section_number`: String (e.g., "1.1", "1.2")
- `title`: String
- `slug`: String
- `content`: Markdown - Main body text
- `subsections`: Array<Subsection> (optional)
- `code_examples`: Array<CodeExample>
- `diagrams`: Array<Diagram>

**Example**:
```yaml
section_number: "1.1"
title: "What is Physical AI?"
slug: "what-is-physical-ai"
```

**Relationships**:
- Belongs to Chapter (N:1)
- May have many Subsections (1:N)
- May have many CodeExamples (1:N)
- May have many Diagrams (1:N)

**File Location**: `docs/chapter-XX/section-YY.md`

**Validation Rules**:
- section_number must follow chapter numbering
- Content must be at least 200 words
- Technical terms must be defined or linked to glossary

---

### 4. Exercise

**Description**: A practical, hands-on activity for students to apply concepts.

**Attributes**:
- `exercise_number`: Integer
- `title`: String
- `type`: Enum ("programming", "simulation", "hardware", "conceptual")
- `difficulty`: Enum ("beginner", "intermediate", "advanced")
- `objective`: String - What students will learn
- `materials`: Array<String> - Required tools/software/hardware
- `instructions`: Markdown - Step-by-step guide
- `expected_outcome`: String - What success looks like
- `estimated_time`: Integer (minutes)
- `safety_notes`: String (optional) - For hardware exercises
- `extensions`: Array<String> - Optional advanced variations

**Example**:
```yaml
exercise_number: 1
title: "Implement PID Controller in Python"
type: "programming"
difficulty: "intermediate"
objective: "Implement and tune a PID controller for a simulated robotic arm"
materials:
  - "Python 3.10+"
  - "NumPy"
  - "Matplotlib"
estimated_time: 60
```

**Relationships**:
- Belongs to Chapter (N:1)
- May reference CodeExamples (N:M)

**File Location**: `docs/chapter-XX/exercises.md` (all exercises for chapter)

**Validation Rules**:
- Must include all required fields per constitution
- Safety notes REQUIRED for hardware exercises
- Instructions must be testable/verifiable

---

### 5. CodeExample

**Description**: A code snippet demonstrating a concept or solution.

**Attributes**:
- `language`: String (e.g., "python", "cpp", "bash")
- `title`: String (optional)
- `code`: String - Actual code content
- `explanation`: String - What the code does
- `runnable`: Boolean - Can be executed as-is

**Example**:
````markdown
```python title="forward_kinematics.py"
def forward_kinematics(joint_angles, link_lengths):
    """Calculate end-effector position from joint angles."""
    x = sum(l * cos(theta) for l, theta in zip(link_lengths, joint_angles))
    y = sum(l * sin(theta) for l, theta in zip(link_lengths, joint_angles))
    return (x, y)
```
````

**Relationships**:
- Belongs to Section or Exercise (N:1)

**File Location**: Inline in Markdown files as fenced code blocks

**Validation Rules**:
- Must specify language for syntax highlighting
- Runnable code must include imports and be self-contained

---

### 6. Diagram

**Description**: Visual representation of concepts (flowchart, architecture diagram, etc.).

**Attributes**:
- `filename`: String
- `alt_text`: String - Accessibility description
- `caption`: String
- `type`: Enum ("flowchart", "architecture", "graph", "photo", "illustration")
- `source_file`: String (optional) - Original editable file (e.g., .drawio)

**Example**:
```markdown
![Control loop diagram](../../static/img/chapter-01/control-loop.svg)
*Figure 1.1: Closed-loop control system architecture*
```

**Relationships**:
- Belongs to Section or Exercise (N:1)

**File Location**:
- Image file: `static/img/chapter-XX/`
- Reference: Inline in Markdown

**Validation Rules**:
- Alt text REQUIRED (accessibility)
- Caption REQUIRED for clarity
- Images must be optimized (<500KB per image)

---

### 7. Reference

**Description**: External source cited in the chapter.

**Attributes**:
- `citation_key`: String (e.g., "Smith2023")
- `type`: Enum ("journal", "book", "conference", "website", "video")
- `authors`: Array<String>
- `title`: String
- `year`: Integer
- `url`: String (optional)
- `doi`: String (optional)
- `formatted_citation`: String - IEEE or APA formatted

**Example**:
```markdown
[1] Brooks, R. A. (1991). "Intelligence without representation." *Artificial Intelligence*, 47(1-3), 139-159.
```

**Relationships**:
- Belongs to Chapter (N:1)

**File Location**: `docs/chapter-XX/index.md` (references section at bottom)

**Validation Rules**:
- Must follow constitution citation style (IEEE or APA)
- DOI or URL REQUIRED for accessibility
- At least 5 references per chapter

---

## Entity Relationships Diagram

```
Book (1)
 └─── has many ──→ Chapter (N)
                    ├─── has many ──→ Section (N)
                    │                  ├─── contains ──→ CodeExample (N)
                    │                  └─── contains ──→ Diagram (N)
                    ├─── has many ──→ Exercise (N)
                    │                  ├─── contains ──→ CodeExample (N)
                    │                  └─── may reference ──→ Diagram (N)
                    └─── has many ──→ Reference (N)
```

---

## Content Lifecycle States

### Chapter States

```
[Draft] → [Review] → [Approved] → [Published]
   ↓         ↓           ↓
 [Archived] ← ─ ─ ─ ─ ─ ┘
```

**State Definitions**:
- **Draft**: Content being written, not ready for review
- **Review**: Submitted for technical expert review
- **Approved**: Reviewed and validated, ready for publication
- **Published**: Live on the site, visible to users
- **Archived**: Deprecated or replaced content

**State Tracking**: Use frontmatter `status` field

```yaml
---
status: "review"
reviewed_by: "Dr. Jane Doe"
review_date: "2025-12-05"
---
```

---

## Validation Rules Summary

| Entity | Required Fields | Constraints |
|--------|----------------|-------------|
| **Chapter** | chapter_number, title, slug, description, learning_objectives | ≥3 learning objectives, ≥1 section |
| **Section** | section_number, title, content | ≥200 words, technical terms defined |
| **Exercise** | All 9 core fields per constitution | Safety notes for hardware, testable instructions |
| **CodeExample** | language, code | Runnable code must be self-contained |
| **Diagram** | filename, alt_text, caption | Alt text required, <500KB size |
| **Reference** | citation_key, authors, title, year | DOI or URL required, ≥5 per chapter |

---

## Metadata Schema (Frontmatter)

### Chapter Frontmatter

```yaml
---
id: chapter-01
title: "Foundations of Physical AI"
sidebar_label: "Ch 1: Foundations"
sidebar_position: 1
description: "Introduction to embodied intelligence and physical AI systems"
keywords:
  - physical ai
  - embodied intelligence
  - robotics
  - humanoid robots
status: "draft"
estimated_reading_time: 45
learning_objectives:
  - "Understand embodied intelligence principles"
  - "Differentiate virtual vs physical AI"
  - "Identify key components of physical AI systems"
authors:
  - "Primary Author Name"
last_updated: "2025-12-01"
---
```

### Section Frontmatter

```yaml
---
id: what-is-physical-ai
title: "What is Physical AI?"
description: "Defining physical AI and its distinction from traditional AI"
---
```

### Exercise Frontmatter

```yaml
---
exercise_number: 1
title: "Implement PID Controller"
type: "programming"
difficulty: "intermediate"
estimated_time: 60
---
```

---

## File Naming Conventions

| Entity | Pattern | Example |
|--------|---------|---------|
| Chapter | `docs/chapter-XX/index.md` | `docs/chapter-01/index.md` |
| Section | `docs/chapter-XX/section-YY.md` or `docs/chapter-XX/descriptive-name.md` | `docs/chapter-01/what-is-physical-ai.md` |
| Exercises | `docs/chapter-XX/exercises.md` | `docs/chapter-01/exercises.md` |
| Images | `static/img/chapter-XX/descriptive-name.ext` | `static/img/chapter-01/control-loop.svg` |

---

## Data Flow

### Content Generation Flow

```
1. Spec (specs/chapter-XX/spec.md)
   └─→ Defines: objectives, topics, exercise requirements

2. Plan (specs/chapter-XX/plan.md)
   └─→ Defines: section breakdown, technical approach

3. Tasks (specs/chapter-XX/tasks.md)
   └─→ Defines: specific implementation tasks

4. Implementation (Claude Code generation)
   └─→ Generates: docs/chapter-XX/*.md files

5. Review (Human validation)
   └─→ Updates: status to "approved"

6. Integration (Copy to docs/)
   └─→ Triggers: Build and deployment

7. Publication (GitHub Pages)
   └─→ Output: Live website
```

---

## Search & Discovery

**Docusaurus Search Configuration**:
- **Local Search**: lunr.js plugin for client-side search
- **Algolia DocSearch**: For production (requires application)

**Searchable Fields**:
- Chapter titles and descriptions
- Section headings and content
- Exercise titles and objectives
- Code example titles

**SEO Metadata**:
- Each page must have unique title and description
- Keywords in frontmatter
- Open Graph tags for social sharing

---

## Content Versioning

**Version Strategy**:
- Major version (X.0.0): Complete coursebook with all 6 chapters
- Minor version (1.X.0): New chapter or major chapter revision
- Patch version (1.0.X): Content corrections, typo fixes

**Git Tags**: Create tag for each released version
```bash
git tag -a v1.0.0 -m "Complete coursebook - first edition"
```

**Docusaurus Versioning**:
- Use Docusaurus docs versioning for major editions
- `npm run docusaurus docs:version 1.0`
- Maintains historical versions accessible to users

---

## Performance Considerations

**Content Limits** (to maintain performance):
- Maximum chapter size: 10,000 words
- Maximum images per chapter: 20
- Maximum code examples per section: 5
- Target page weight: <2MB (with images)

**Optimization Strategies**:
- Lazy-load images below fold
- Compress images (WebP format, 80% quality)
- Split large chapters into multiple pages
- Use Docusaurus code block lazy loading
