# Section Template: [Section Number] - [Section Title]

**Chapter**: Chapter 1 - Foundations of Humanoid Robotics
**Section Number**: [1.1, 1.2, 1.3]
**Estimated Reading Time**: [10-20 minutes]

---

## Front Matter (YAML)

```yaml
---
id: [section-slug]
title: "[Section Title]"
description: "[Brief 1-2 sentence description]"
section_number: "[1.1, 1.2, or 1.3]"
---
```

---

## Content Structure

### Introduction (1-2 paragraphs)
- Introduce the section topic
- Explain why this topic matters for humanoid robotics
- Preview what will be covered

### Main Content

#### Subsection 1: [Subsection Title]

**Learning Focus**: [What students should understand from this subsection]

[Content here - include:]
- Clear explanations with real-world analogies
- Technical definitions with context
- Examples from actual humanoid robots (ASIMO, Atlas, Optimus, etc.)
- Diagrams where helpful (reference figures)

#### Subsection 2: [Subsection Title]

**Learning Focus**: [What students should understand]

[Content here]

#### Subsection 3: [Subsection Title]

**Learning Focus**: [What students should understand]

[Content here]

### Mathematical Content (if applicable)

**Concept**: [Name of mathematical concept]

**Intuitive Explanation**: [Explain concept without math first]

**Mathematical Formulation**:

$$
[LaTeX equation using KaTeX syntax]
$$

Where:
- $variable$ = description
- $variable$ = description

**Worked Example**:

[Step-by-step numerical example with actual values]

### Code Examples (if applicable)

```python
# Brief description of what this code does
import numpy as np

def example_function(param1, param2):
    """
    Docstring explaining function purpose.

    Parameters:
    -----------
    param1 : type
        Description
    param2 : type
        Description

    Returns:
    --------
    type
        Description
    """
    # Implementation
    result = param1 + param2
    return result

# Example usage
output = example_function(1.0, 2.0)
print(f"Result: {output}")
```

**Expected Output**:
```
Result: 3.0
```

### Diagrams and Figures

**Figure [X.Y]**: [Caption describing the diagram]

![Alt text for accessibility - describe what the diagram shows](../../static/img/chapter-01/[diagram-filename].svg)

*Figure [X.Y]: [Detailed caption explaining the figure]*

### Key Takeaways

:::tip Key Takeaways
- **Takeaway 1**: [Concise summary point]
- **Takeaway 2**: [Concise summary point]
- **Takeaway 3**: [Concise summary point]
- **Takeaway 4**: [Concise summary point]
- **Takeaway 5**: [Concise summary point]
:::

### Cross-References

**Related Sections**:
- See [Section X.Y](./section-file.md) for [related topic]
- Prerequisites: [Section X.Y](./section-file.md)
- Next: [Section X.Y](./section-file.md)

**Related Concepts in Future Chapters**:
- Chapter [N]: [Brief description of related advanced topic]

---

## Content Quality Checklist

Before considering this section complete, verify:

- [ ] Front matter YAML is complete and correctly formatted
- [ ] Introduction clearly states section purpose and scope
- [ ] All technical terms are defined on first use
- [ ] Real-world examples from actual robots are included
- [ ] Diagrams are referenced in text with figure numbers
- [ ] All diagrams have descriptive alt text (accessibility)
- [ ] Mathematical content follows: intuition → formulation → example
- [ ] Code examples are complete, runnable, and commented
- [ ] Key takeaways box summarizes 3-5 main points
- [ ] Cross-references to other sections are accurate
- [ ] Content length is appropriate (500-1500 words per section)
- [ ] Estimated reading time is realistic (10-20 minutes)
- [ ] Writing style is clear, engaging, and appropriate for engineering students
- [ ] Technical accuracy has been verified (robotics expert review)

---

## Notes for Content Generation

- Use **Docusaurus admonitions** for callouts: `:::tip`, `:::note`, `:::warning`, `:::caution`
- Mathematical notation: Use KaTeX syntax within `$...$` (inline) or `$$...$$` (display)
- Code blocks: Specify language for syntax highlighting
- Internal links: Use relative paths (e.g., `./section-file.md`)
- Image paths: Use `../../static/img/chapter-01/filename.svg` from docs/chapter-01/
- Follow notation from "Modern Robotics" (Lynch & Park) for consistency
- Use IEEE format for any citations within sections
- Avoid implementation-specific details (ROS, specific libraries) - focus on concepts
