# Content Contract: Chapter

**Version**: 1.0.0
**Purpose**: Define the required structure and format for coursebook chapters

## Contract Overview

This contract specifies the mandatory structure, metadata, and content requirements for a valid coursebook chapter. All chapters MUST conform to this contract.

---

## File Structure

### Required Files

```
docs/chapter-XX/
├── index.md          # REQUIRED: Main chapter file
├── *.md              # REQUIRED: At least 1 section file
└── exercises.md      # REQUIRED: Exercises for the chapter
```

### Optional Files

```
docs/chapter-XX/
├── advanced-topics.md   # Optional: Advanced/supplementary content
├── references.md        # Optional: Separate references page
└── glossary.md          # Optional: Chapter-specific glossary
```

---

## Frontmatter Contract

### index.md Frontmatter (REQUIRED)

```yaml
---
id: chapter-XX                    # REQUIRED: String, pattern: "chapter-\d{2}"
title: "Chapter Title"            # REQUIRED: String, 5-80 characters
sidebar_label: "Ch X: Short"      # REQUIRED: String, max 30 characters
sidebar_position: X               # REQUIRED: Integer, matches chapter number
description: "Brief overview"     # REQUIRED: String, 50-200 characters
keywords:                         # REQUIRED: Array<String>, 3-10 keywords
  - keyword1
  - keyword2
status: "draft"                   # REQUIRED: Enum [draft, review, approved, published]
estimated_reading_time: 45        # REQUIRED: Integer, minutes
learning_objectives:              # REQUIRED: Array<String>, 3-7 objectives
  - "Objective 1"
  - "Objective 2"
  - "Objective 3"
authors:                          # REQUIRED: Array<String>, at least 1
  - "Author Name"
last_updated: "2025-12-01"        # REQUIRED: ISO Date (YYYY-MM-DD)
chapter_number: X                 # REQUIRED: Integer, 1-6
---
```

### Validation Rules

| Field | Type | Constraints | Example |
|-------|------|-------------|---------|
| `id` | String | Pattern: `chapter-\d{2}`, unique | `chapter-01` |
| `title` | String | 5-80 chars, title case | `"Foundations of Physical AI"` |
| `sidebar_label` | String | Max 30 chars | `"Ch 1: Foundations"` |
| `sidebar_position` | Integer | Matches chapter_number | `1` |
| `description` | String | 50-200 chars, sentence case | `"Introduction to embodied intelligence..."` |
| `keywords` | Array<String> | 3-10 keywords, lowercase | `["physical ai", "robotics"]` |
| `status` | Enum | One of: draft, review, approved, published | `"draft"` |
| `estimated_reading_time` | Integer | 15-120 minutes | `45` |
| `learning_objectives` | Array<String> | 3-7 items, start with verb | `["Understand...", "Identify..."]` |
| `authors` | Array<String> | At least 1 | `["Dr. Jane Smith"]` |
| `last_updated` | ISO Date | YYYY-MM-DD format | `"2025-12-01"` |
| `chapter_number` | Integer | 1-6, matches directory | `1` |

---

## Content Structure Contract

### Required Sections (in order)

1. **Introduction** (H2: `## Introduction`)
   - Minimum 200 words
   - Overview of chapter topics
   - Relevance to Physical AI/Robotics
   - Connection to previous/next chapters

2. **Key Concepts** (H2: `## Key Concepts` or topic-specific title)
   - At least 3 subsections (H3)
   - Each subsection minimum 300 words
   - Technical terms defined or linked
   - At least 1 code example or diagram per subsection

3. **Learning Objectives Revisited** (H2: `## Learning Objectives`)
   - Restate frontmatter objectives with context
   - Map objectives to sections

4. **Example Applications** (H2: `## Example Applications` or `## Case Studies`)
   - At least 1 real-world application
   - Minimum 400 words
   - Include diagrams or images where applicable

5. **Summary** (H2: `## Summary`)
   - Minimum 150 words
   - Recap key takeaways (3-5 bullet points)
   - Preview next chapter

6. **References** (H2: `## References`)
   - At least 5 citations
   - IEEE or APA format (consistent throughout book)
   - Include DOI or URL where available

### Optional Sections

- **Advanced Topics** (H2: `## Advanced Topics`)
- **Common Pitfalls** (H2: `## Common Pitfalls`)
- **Further Reading** (H2: `## Further Reading`)

---

## Content Quality Requirements

### Technical Writing Standards

- **Clarity**: Avoid jargon without explanation
- **Consistency**: Use consistent terminology throughout
- **Accuracy**: All technical content must be factually correct
- **Completeness**: Cover all learning objectives stated in frontmatter

### Formatting Standards

```markdown
# Chapter Title (only one H1 per file, auto-generated from frontmatter)

## Section Title (H2 for major sections)

### Subsection Title (H3 for subsections)

#### Detail Title (H4 for fine-grained details)

**Bold** for emphasis
*Italic* for technical terms on first use
`code` for inline code
```

### Code Example Standards

- Must specify language for syntax highlighting
- Include comments explaining key concepts
- Runnable code must be self-contained
- Include title in code fence

```python title="example.py"
# Code with title and language
def example_function():
    """Docstring explaining purpose."""
    return True
```

### Diagram/Image Standards

```markdown
![Alt text describing image](../../static/img/chapter-XX/image-name.ext)

*Figure X.Y: Caption describing the diagram*
```

- Alt text REQUIRED (accessibility)
- Caption REQUIRED (clarity)
- Images optimized (<500KB)
- Prefer SVG for diagrams, WebP/JPEG for photos

---

## Exercises Contract

See [exercise-contract.md](./exercise-contract.md) for detailed requirements.

**Summary**:
- Minimum 3 exercises per chapter
- Mix of programming, simulation, and conceptual exercises
- All exercises must include: objective, materials, instructions, expected outcome

---

## Validation Checklist

Before marking chapter status as "approved", verify:

### Structure
- [ ] All required frontmatter fields present and valid
- [ ] All required sections present in correct order
- [ ] Heading hierarchy is correct (H1 → H2 → H3, no skips)
- [ ] File naming matches contract (`index.md`, `exercises.md`)

### Content
- [ ] Introduction ≥200 words
- [ ] At least 3 key concept subsections
- [ ] Each subsection ≥300 words
- [ ] At least 5 references in IEEE/APA format
- [ ] Summary ≥150 words with 3-5 key takeaways

### Quality
- [ ] All learning objectives covered in content
- [ ] Technical terms defined or linked
- [ ] Code examples are runnable and commented
- [ ] Images have alt text and captions
- [ ] No broken internal links
- [ ] No spelling or grammar errors

### Technical Accuracy
- [ ] Reviewed by technical expert (Robotics Expert role)
- [ ] Code examples tested and verified
- [ ] Mathematical equations correct
- [ ] Citations accurate and accessible

---

## Error Codes

| Code | Error | Resolution |
|------|-------|------------|
| `CH-001` | Missing required frontmatter field | Add missing field to frontmatter |
| `CH-002` | Invalid frontmatter value | Correct value to match contract constraints |
| `CH-003` | Missing required section | Add missing section (Introduction, Summary, etc.) |
| `CH-004` | Insufficient content length | Expand section to meet minimum word count |
| `CH-005` | Incorrect heading hierarchy | Fix heading levels (no H4 under H2, etc.) |
| `CH-006` | Insufficient references | Add more citations (minimum 5) |
| `CH-007` | Missing alt text on image | Add descriptive alt text |
| `CH-008` | Broken internal link | Fix link path or create missing file |
| `CH-009` | Learning objective not covered | Add content addressing objective or remove from frontmatter |
| `CH-010` | Status mismatch | Update status field to reflect review state |

---

## Example: Valid Chapter

See [chapter-example.md](./chapter-example.md) for a complete, contract-compliant chapter example.

---

## Versioning

This contract follows semantic versioning:
- **Major**: Breaking changes to structure (e.g., new required fields)
- **Minor**: Non-breaking additions (e.g., new optional fields)
- **Patch**: Clarifications or corrections

**Current Version**: 1.0.0
**Last Updated**: 2025-12-01
