# Data Model: Chapter 1 - Foundations of Humanoid Robotics

**Feature**: 003-chapter-01-foundations
**Date**: 2025-12-01
**Purpose**: Define the content structure, entities, and relationships for Chapter 1

## Overview

This data model describes the content entities for Chapter 1 of the coursebook. Unlike software data models, this represents the structure of educational content (markdown files, sections, exercises, diagrams, references).

---

## Core Content Entities

### 1. Chapter

**Description**: The top-level container for Chapter 1 content

**Attributes**:
- `chapter_number`: Integer (1)
- `title`: String ("Foundations of Humanoid Robotics")
- `slug`: String ("chapter-01")
- `description`: String (brief overview)
- `learning_objectives`: Array<String> (3-7 measurable objectives)
- `estimated_reading_time`: Integer (45-60 minutes)
- `sections`: Array<Section> (3 major sections)
- `exercises`: Array<Exercise> (3-5 exercises)
- `references`: Array<Reference> (≥5 citations)
- `status`: Enum ("draft", "review", "approved", "published")

**File Location**: `docs/chapter-01/index.md`

**Front Matter Example**:
```yaml
---
id: chapter-01
title: "Chapter 1: Foundations of Humanoid Robotics"
sidebar_label: "Ch 1: Foundations"
sidebar_position: 1
description: "Learn the fundamental concepts of humanoid robotics: anatomy, sensors, actuators, kinematics, and dynamics"
keywords:
  - humanoid robotics
  - robot anatomy
  - sensors and actuators
  - kinematics
  - dynamics
status: "draft"
estimated_reading_time: 50
learning_objectives:
  - "Identify and describe the major anatomical components of humanoid robots"
  - "Explain the function and selection of sensors and actuators in humanoid systems"
  - "Solve basic forward kinematics problems for multi-link robot arms"
  - "Understand the difference between kinematics and dynamics"
authors:
  - "Generated with Claude Code"
last_updated: "2025-12-01"
---
```

---

### 2. Section

**Description**: A major subdivision of the chapter focusing on a specific topic

**Attributes**:
- `section_number`: String ("1.1", "1.2", "1.3")
- `title`: String
- `slug`: String
- `content`: Markdown (main body text)
- `learning_focus`: String (which user story this addresses)
- `subsections`: Array<Subsection> (optional)
- `diagrams`: Array<Diagram>
- `code_examples`: Array<CodeExample>
- `key_takeaways`: Array<String> (3-5 bullet points)

**Sections for Chapter 1**:

1. **Section 1.1**: Anatomy and Structure
   - File: `docs/chapter-01/anatomy-structure.md`
   - Focus: Understanding robot morphology, DOF, components
   - Diagrams: Humanoid anatomy diagram, DOF illustration

2. **Section 1.2**: Sensors and Actuators
   - File: `docs/chapter-01/sensors-actuators.md`
   - Focus: Types of sensors, types of actuators, selection criteria
   - Diagrams: Sensor types visual, actuator comparison chart

3. **Section 1.3**: Kinematics and Dynamics
   - File: `docs/chapter-01/kinematics-dynamics.md`
   - Focus: Forward/inverse kinematics, dynamics fundamentals
   - Diagrams: Forward kinematics example, dynamics forces diagram

**Front Matter Example**:
```yaml
---
id: anatomy-structure
title: "Robot Anatomy and Structure"
description: "Understanding the physical composition and morphology of humanoid robots"
section_number: "1.1"
---
```

---

### 3. Diagram

**Description**: Visual illustration supporting the text

**Attributes**:
- `filename`: String (e.g., "humanoid-anatomy-diagram.svg")
- `alt_text`: String (accessibility description)
- `caption`: String (figure caption)
- `figure_number`: String (e.g., "Figure 1.1")
- `referenced_in_section`: String (section ID)
- `format`: Enum ("svg", "png", "jpg")
- `source_file`: String (optional - original editable file)

**Required Diagrams for Chapter 1**:

| Diagram | Filename | Alt Text | Caption |
|---------|----------|----------|---------|
| Humanoid Anatomy | `humanoid-anatomy-diagram.svg` | "Labeled diagram showing major components of a humanoid robot including head, torso, arms, and legs" | "Figure 1.1: Anatomical structure of a typical humanoid robot" |
| Degrees of Freedom | `degrees-of-freedom.svg` | "Illustration of robot joint degrees of freedom for shoulder, elbow, and wrist" | "Figure 1.2: Degrees of freedom in a humanoid arm" |
| Sensor Types | `sensor-types.svg` | "Visual comparison of common humanoid robot sensors: cameras, IMU, force sensors, encoders" | "Figure 1.3: Common sensor types in humanoid robotics" |
| Actuator Comparison | `actuator-comparison.svg` | "Comparison chart of servo motors, DC motors, and hydraulic actuators showing torque, speed, and power characteristics" | "Figure 1.4: Actuator types and their characteristics" |
| Forward Kinematics | `forward-kinematics.svg` | "Diagram of 2-DOF planar robot arm showing link lengths, joint angles, and end-effector position calculation" | "Figure 1.5: Forward kinematics example for 2-link arm" |
| Inverse Kinematics | `inverse-kinematics.svg` | "Illustration showing multiple joint configurations reaching the same end-effector position" | "Figure 1.6: Inverse kinematics: multiple solutions problem" |
| Dynamics Forces | `dynamics-forces.svg` | "Free body diagram showing forces, torques, and accelerations on robot links" | "Figure 1.7: Forces and torques in robot dynamics" |

**Markdown Usage Example**:
```markdown
![Labeled diagram showing major components of a humanoid robot](../../static/img/chapter-01/humanoid-anatomy-diagram.svg)

*Figure 1.1: Anatomical structure of a typical humanoid robot*
```

---

### 4. CodeExample

**Description**: Python code snippet demonstrating a concept

**Attributes**:
- `language`: String ("python")
- `title`: String (optional, used in code fence)
- `code`: String (actual code)
- `explanation`: String (what the code does)
- `purpose`: String (why it's relevant to learning objective)
- `runnable`: Boolean (true if self-contained and executable)

**Code Examples for Chapter 1**:

#### Example 1: Forward Kinematics (2-DOF Arm)

```python
import numpy as np

def forward_kinematics_2dof(theta1, theta2, L1, L2):
    """
    Calculate end-effector position for a 2-DOF planar robot arm.

    Parameters:
    -----------
    theta1 : float
        Joint angle 1 (shoulder) in radians
    theta2 : float
        Joint angle 2 (elbow) in radians
    L1 : float
        Length of link 1 (upper arm) in meters
    L2 : float
        Length of link 2 (forearm) in meters

    Returns:
    --------
    tuple
        (x, y) position of end-effector in meters
    """
    x = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    y = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
    return (x, y)

# Example usage
theta1 = np.pi / 4  # 45 degrees
theta2 = np.pi / 6  # 30 degrees
L1 = 1.0  # 1 meter
L2 = 0.8  # 0.8 meters

position = forward_kinematics_2dof(theta1, theta2, L1, L2)
print(f"End-effector position: ({position[0]:.3f}, {position[1]:.3f}) meters")
# Expected output: (1.532, 1.207) meters
```

**Purpose**: Demonstrates forward kinematics calculation, reinforces mathematical concepts

**Runnable**: Yes (requires NumPy)

---

### 5. Exercise

**Description**: Practical activity for students to apply knowledge

**Attributes**:
- `exercise_number`: Integer
- `title`: String
- `type`: Enum ("programming", "simulation", "hardware", "conceptual")
- `difficulty`: Enum ("beginner", "intermediate", "advanced")
- `objective`: String (learning goal)
- `materials`: Array<String> (required tools/software)
- `prerequisites`: Array<String> (prior knowledge needed)
- `instructions`: Markdown (step-by-step guide)
- `expected_outcome`: String (success criteria)
- `verification_checklist`: Array<String> (testable checkpoints)
- `estimated_time`: Integer (minutes)
- `safety_notes`: String (for hardware exercises)
- `troubleshooting`: Array<{problem: String, solution: String}>
- `extensions`: Array<String> (advanced variations)

**Exercises for Chapter 1** (3-5 total):

#### Exercise 1.1: Identify Humanoid Robot Components (Beginner, Conceptual)
- **Type**: Conceptual
- **Difficulty**: Beginner
- **Time**: 20 minutes
- **Objective**: Identify and describe major anatomical components of humanoid robots
- **Materials**: Chapter diagrams, reference images of real robots
- **Instructions**: Given labeled and unlabeled diagrams, identify components and explain their functions

#### Exercise 1.2: Sensor Selection Challenge (Intermediate, Conceptual)
- **Type**: Conceptual
- **Difficulty**: Intermediate
- **Time**: 30 minutes
- **Objective**: Select appropriate sensors for specific robot capabilities
- **Materials**: Sensor specification sheets (provided)
- **Instructions**: For given scenarios (e.g., "robot must walk on uneven terrain"), select and justify sensor choices

#### Exercise 1.3: Forward Kinematics Calculation (Intermediate, Programming)
- **Type**: Programming
- **Difficulty**: Intermediate
- **Time**: 45 minutes
- **Objective**: Implement forward kinematics for a 3-DOF robot arm
- **Materials**: Python 3.10+, NumPy, Matplotlib (for visualization)
- **Instructions**: Extend the 2-DOF example to 3-DOF, plot workspace, analyze reachability

#### Exercise 1.4: Inverse Kinematics Exploration (Advanced, Programming)
- **Type**: Programming
- **Difficulty**: Advanced
- **Time**: 60 minutes
- **Objective**: Explore inverse kinematics solutions and singularities
- **Materials**: Python 3.10+, NumPy, SciPy (for numerical solving)
- **Instructions**: Given target position, find multiple joint configurations, identify singularities

#### Exercise 1.5: Dynamics Simulation (Advanced, Programming/Simulation)
- **Type**: Programming/Simulation
- **Difficulty**: Advanced
- **Time**: 90 minutes
- **Objective**: Simulate robot dynamics and observe effects of mass/inertia
- **Materials**: Python 3.10+, PyBullet or similar physics simulator
- **Instructions**: Create simple pendulum simulation, vary parameters, analyze behavior

**File Location**: `docs/chapter-01/exercises.md`

---

### 6. Reference

**Description**: Academic citation for external sources

**Attributes**:
- `citation_key`: String (e.g., "Lynch2017")
- `type`: Enum ("book", "journal", "conference", "website", "video")
- `authors`: Array<String>
- `title`: String
- `year`: Integer
- `publication`: String (journal, conference, publisher)
- `url`: String (optional)
- `doi`: String (optional)
- `formatted_citation_ieee`: String
- `formatted_citation_apa`: String

**Required References for Chapter 1** (≥5):

1. **Lynch & Park (2017)**: "Modern Robotics: Mechanics, Planning, and Control" - Primary textbook reference for notation and theory
2. **Craig (2005)**: "Introduction to Robotics: Mechanics and Control" - Classic robotics textbook for fundamentals
3. **Siciliano et al. (2016)**: "Springer Handbook of Robotics" - Comprehensive reference for humanoid robotics
4. **Kajita et al. (2014)**: "Introduction to Humanoid Robotics" - Specific focus on humanoid systems
5. **Boston Dynamics / Honda / Tesla**: Technical documentation/whitepapers for real-world examples

**IEEE Format Example**:
```
[1] K. M. Lynch and F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*. Cambridge University Press, 2017.
```

**File Location**: Included in `docs/chapter-01/index.md` references section

---

## Content Structure Hierarchy

```
Chapter 1 (index.md)
│
├── Introduction
│   ├── What are Humanoid Robots?
│   ├── Why Study Humanoid Robotics?
│   └── Chapter Roadmap
│
├── Section 1.1: Anatomy and Structure (anatomy-structure.md)
│   ├── Human vs. Robot Anatomy
│   ├── Major Components
│   │   ├── Head and Sensors
│   │   ├── Torso and Power
│   │   ├── Arms and Manipulation
│   │   └── Legs and Locomotion
│   ├── Degrees of Freedom
│   └── Design Trade-offs
│
├── Section 1.2: Sensors and Actuators (sensors-actuators.md)
│   ├── Sensor Types
│   │   ├── Vision (Cameras, Depth Sensors)
│   │   ├── Inertial (IMUs, Gyroscopes)
│   │   ├── Force/Torque Sensors
│   │   ├── Tactile Sensors
│   │   └── Joint Encoders
│   ├── Sensor Fusion
│   ├── Actuator Types
│   │   ├── Servo Motors
│   │   ├── DC Motors
│   │   └── Hydraulic/Pneumatic
│   └── Selection Criteria
│
├── Section 1.3: Kinematics and Dynamics (kinematics-dynamics.md)
│   ├── Kinematics Fundamentals
│   │   ├── Forward Kinematics
│   │   ├── Denavit-Hartenberg Parameters
│   │   ├── Inverse Kinematics
│   │   └── Singularities
│   ├── Dynamics Fundamentals
│   │   ├── Newton-Euler Equations
│   │   ├── Joint Torques
│   │   └── Mass and Inertia Effects
│   └── Workspace Analysis
│
├── Exercises (exercises.md)
│   ├── Exercise 1.1: Component Identification
│   ├── Exercise 1.2: Sensor Selection
│   ├── Exercise 1.3: Forward Kinematics
│   ├── Exercise 1.4: Inverse Kinematics
│   └── Exercise 1.5: Dynamics Simulation
│
├── Summary
│   └── Key Takeaways (5-7 bullet points)
│
└── References
    └── Formatted citations (IEEE/APA)
```

---

## File-Based Data Storage

| Entity | Storage Format | Location |
|--------|---------------|----------|
| Chapter metadata | YAML frontmatter in Markdown | `docs/chapter-01/index.md` |
| Section content | Markdown | `docs/chapter-01/*.md` |
| Diagrams | SVG files | `static/img/chapter-01/*.svg` |
| Code examples | Fenced code blocks in Markdown | Embedded in section files |
| Exercises | Markdown | `docs/chapter-01/exercises.md` |
| References | Markdown list | `docs/chapter-01/index.md` (References section) |

---

## Content Validation Rules

### Chapter-Level Validation

- [ ] Chapter number is 1
- [ ] Title matches spec ("Foundations of Humanoid Robotics")
- [ ] 3 major sections present
- [ ] 3-5 exercises present
- [ ] ≥5 references present
- [ ] All sections referenced in chapter index
- [ ] Estimated reading time 45-60 minutes

### Section-Level Validation

- [ ] Section frontmatter complete
- [ ] Content ≥500 words per section
- [ ] At least 1 diagram per section
- [ ] Key takeaways box at end
- [ ] Cross-references to other sections where appropriate

### Exercise-Level Validation

- [ ] All required fields present (objective, materials, instructions, outcome)
- [ ] Difficulty progression (beginner → intermediate → advanced)
- [ ] At least 1 programming exercise
- [ ] At least 1 conceptual exercise
- [ ] Verification checklist included
- [ ] Estimated time reasonable

### Diagram-Level Validation

- [ ] SVG format (or PNG/JPG with justification)
- [ ] Alt text present (accessibility)
- [ ] Caption present with figure number
- [ ] Referenced in text
- [ ] File size <500KB

---

## Next Phase

This data model defines the content structure for Chapter 1. Next steps:
1. Create section and exercise templates (contracts/)
2. Generate quickstart guide for content creation
3. Update agent context
4. Proceed to task generation (`/sp.tasks`)
