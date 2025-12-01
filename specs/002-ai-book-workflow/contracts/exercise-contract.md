# Content Contract: Exercise

**Version**: 1.0.0
**Purpose**: Define the required structure and format for coursebook exercises

## Contract Overview

This contract specifies the mandatory structure and content requirements for exercises. All exercises MUST conform to this contract to ensure educational value and safety.

---

## Exercise Structure

### File Location

```
docs/chapter-XX/exercises.md
```

All exercises for a chapter are contained in a single `exercises.md` file.

---

## Exercise Template

Each exercise MUST follow this structure:

```markdown
### Exercise X.Y: [Exercise Title]

**Type**: [programming | simulation | hardware | conceptual]
**Difficulty**: [beginner | intermediate | advanced]
**Estimated Time**: [X] minutes

#### Objective

[Clear statement of what students will learn or accomplish]

#### Required Materials

- Material/tool 1
- Material/tool 2
- ...

#### Prerequisites

- Prerequisite knowledge 1
- Prerequisite knowledge 2

#### Instructions

1. Step 1 with detailed description
2. Step 2 with detailed description
3. ...

#### Expected Outcome

[Description of what success looks like, including expected outputs, results, or understanding]

#### Verification

[How to verify the exercise was completed correctly]
- [ ] Checkpoint 1
- [ ] Checkpoint 2
- [ ] Checkpoint 3

#### Safety Notes

[REQUIRED for hardware exercises, OPTIONAL for others]
- Safety consideration 1
- Safety consideration 2

#### Troubleshooting

**Problem**: [Common issue]
**Solution**: [How to resolve]

**Problem**: [Another common issue]
**Solution**: [How to resolve]

#### Extensions

[Optional advanced variations or additional challenges]
- Extension idea 1
- Extension idea 2

#### Related Resources

- [Resource title](URL)
- [Another resource](URL)

---
```

---

## Required Fields

### Exercise Header

| Field | Format | Constraints | Example |
|-------|--------|-------------|---------|
| **Exercise Number** | X.Y | X = chapter number, Y = exercise number within chapter | `1.3` |
| **Title** | String | 5-60 characters, descriptive | `"Implement PID Controller in Python"` |
| **Type** | Enum | One of: programming, simulation, hardware, conceptual | `programming` |
| **Difficulty** | Enum | One of: beginner, intermediate, advanced | `intermediate` |
| **Estimated Time** | Integer | 15-180 minutes | `60` |

### Required Sections

| Section | Min Length | Description |
|---------|-----------|-------------|
| **Objective** | 50-200 words | Clear learning goal, starts with action verb |
| **Required Materials** | 2-15 items | List of tools, software, hardware needed |
| **Prerequisites** | 1-5 items | Prior knowledge or skills required |
| **Instructions** | 5-20 steps | Step-by-step guide, numbered list |
| **Expected Outcome** | 100-300 words | What success looks like |
| **Verification** | 3-10 checkpoints | Testable criteria for completion |

### Conditional Sections

| Section | When Required | Min Length |
|---------|--------------|-----------|
| **Safety Notes** | ALWAYS for hardware exercises | 50-200 words |
| **Troubleshooting** | RECOMMENDED for all | At least 2 problem-solution pairs |
| **Extensions** | RECOMMENDED for all | At least 1 extension idea |

---

## Exercise Types

### 1. Programming Exercise

**Type**: `programming`

**Must Include**:
- Programming language specification
- Code template or starter code
- Expected output or behavior
- Test cases to validate solution

**Example**:

```markdown
### Exercise 1.1: Implement Forward Kinematics

**Type**: programming
**Difficulty**: beginner
**Estimated Time**: 45 minutes

#### Objective

Implement a forward kinematics function for a 2-link planar robot arm using NumPy.

#### Required Materials

- Python 3.10 or higher
- NumPy library (`pip install numpy`)
- Matplotlib for visualization (`pip install matplotlib`)
- Code editor (VS Code, PyCharm, etc.)

#### Instructions

1. Create a new Python file named `forward_kinematics.py`
2. Import NumPy: `import numpy as np`
3. Define a function `forward_kinematics(theta1, theta2, L1, L2)` that:
   - Takes joint angles theta1, theta2 (in radians)
   - Takes link lengths L1, L2 (in meters)
   - Returns end-effector position (x, y)
4. Use the equations:
   - `x = L1 * cos(theta1) + L2 * cos(theta1 + theta2)`
   - `y = L1 * sin(theta1) + L2 * sin(theta1 + theta2)`
5. Test with: theta1=π/4, theta2=π/6, L1=1.0, L2=0.8

#### Expected Outcome

Your function should return approximately:
- `x = 1.532`
- `y = 1.207`

#### Verification

- [ ] Function accepts 4 parameters and returns a tuple (x, y)
- [ ] Test case produces correct output (within 0.01 tolerance)
- [ ] Code includes docstring explaining purpose
- [ ] No errors when run with valid inputs
```

---

### 2. Simulation Exercise

**Type**: `simulation`

**Must Include**:
- Simulation environment specification
- Installation instructions for simulator
- Parameters to configure
- Expected simulation behavior

**Example**:

```markdown
### Exercise 2.3: Simulate Mobile Robot Navigation

**Type**: simulation
**Difficulty**: intermediate
**Estimated Time**: 90 minutes

#### Objective

Simulate a differential drive mobile robot navigating to a goal position while avoiding obstacles using ROS 2 and Gazebo.

#### Required Materials

- Ubuntu 22.04 (or Docker container)
- ROS 2 Humble installed
- Gazebo Classic 11
- TurtleBot3 simulation packages
- At least 4GB RAM

#### Instructions

1. Install TurtleBot3 packages:
   ```bash
   sudo apt install ros-humble-turtlebot3*
   ```
2. Set TurtleBot3 model:
   ```bash
   export TURTLEBOT3_MODEL=burger
   ```
3. Launch Gazebo simulation:
   ```bash
   ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
   ```
4. In a new terminal, run navigation:
   ```bash
   ros2 launch turtlebot3_navigation2 navigation2.launch.py
   ```
5. In RViz, set a goal position using "2D Goal Pose" tool
6. Observe robot navigating to goal while avoiding obstacles

#### Expected Outcome

- Gazebo window shows TurtleBot3 in simulated environment
- RViz displays robot model, sensor data, and costmaps
- Robot successfully navigates to goal without collisions
- Path planning is visible in RViz

#### Verification

- [ ] Simulation launches without errors
- [ ] Robot model visible in Gazebo and RViz
- [ ] Robot moves when goal is set
- [ ] Robot avoids obstacles (does not collide)
- [ ] Robot reaches goal position (within 0.5m)

#### Safety Notes

N/A (simulation only)
```

---

### 3. Hardware Exercise

**Type**: `hardware`

**Must Include**:
- Complete hardware list with part numbers
- Wiring diagrams or connection instructions
- Safety warnings (electrical, mechanical, thermal)
- Troubleshooting for hardware issues

**SAFETY NOTES SECTION IS MANDATORY**

**Example**:

```markdown
### Exercise 3.2: Build and Control a Servo Motor

**Type**: hardware
**Difficulty**: beginner
**Estimated Time**: 60 minutes

#### Objective

Connect and control a servo motor using an Arduino, learning PWM control principles.

#### Required Materials

- Arduino Uno (or compatible board)
- SG90 micro servo motor
- Jumper wires (male-to-male, at least 3)
- USB cable for Arduino
- 5V power supply (optional, for external power)
- Breadboard (optional)

#### Prerequisites

- Basic understanding of Arduino IDE
- Familiarity with uploading sketches to Arduino
- Understanding of analog vs digital signals

#### Instructions

1. Connect servo motor to Arduino:
   - Servo RED wire → Arduino 5V
   - Servo BROWN/BLACK wire → Arduino GND
   - Servo ORANGE/YELLOW wire → Arduino Pin 9
2. Open Arduino IDE and install Servo library (if not already installed)
3. Create a new sketch and include: `#include <Servo.h>`
4. Declare servo object: `Servo myServo;`
5. In `setup()`, attach servo to pin 9: `myServo.attach(9);`
6. In `loop()`, sweep servo from 0° to 180° and back:
   ```cpp
   for (int pos = 0; pos <= 180; pos++) {
     myServo.write(pos);
     delay(15);
   }
   for (int pos = 180; pos >= 0; pos--) {
     myServo.write(pos);
     delay(15);
   }
   ```
7. Upload sketch to Arduino
8. Observe servo motor sweeping back and forth

#### Expected Outcome

- Servo motor sweeps from 0° to 180° smoothly
- No jittering or erratic movement
- Motion repeats continuously
- Servo responds to angle commands

#### Verification

- [ ] Servo physically connected correctly (no loose wires)
- [ ] Sketch compiles without errors
- [ ] Servo moves when powered on
- [ ] Servo sweeps full range (0° to 180°)
- [ ] Movement is smooth and controlled

#### Safety Notes

⚠️ **READ BEFORE STARTING**

- **Electrical Safety**: Ensure Arduino is powered off when making connections
- **Polarity**: Double-check servo wire connections (reversed polarity can damage servo)
- **Current Draw**: Single servo is safe with Arduino 5V, but multiple servos require external power supply
- **Moving Parts**: Keep fingers clear of servo horn when powered on
- **Heat**: Servo may become warm during extended use (this is normal)
- **Do NOT**:
  - Force servo beyond its range of motion
  - Apply external voltage >6V to servo
  - Short power and ground wires

#### Troubleshooting

**Problem**: Servo jitters or vibrates
**Solution**: Check power supply (may need external 5V source), ensure good connections

**Problem**: Servo doesn't move
**Solution**: Verify pin number matches code (Pin 9), check servo is functional (test with different servo)

**Problem**: Servo moves erratically
**Solution**: Add delay between movements, check for loose wires, ensure stable power

#### Extensions

1. Control servo with potentiometer (analog input)
2. Use Serial Monitor to send angle commands
3. Create a multi-servo robotic arm
4. Implement smooth acceleration/deceleration

#### Related Resources

- [Arduino Servo Library Reference](https://www.arduino.cc/reference/en/libraries/servo/)
- [SG90 Servo Datasheet](https://example.com/sg90-datasheet.pdf)
```

---

### 4. Conceptual Exercise

**Type**: `conceptual`

**Must Include**:
- Clear question or problem statement
- Guidance on how to approach the problem
- Example solution or rubric

**Example**:

```markdown
### Exercise 4.1: Design a Control System

**Type**: conceptual
**Difficulty**: advanced
**Estimated Time**: 45 minutes

#### Objective

Design a control system architecture for a quadruped robot that must navigate uneven terrain while maintaining balance.

#### Required Materials

- Pen and paper (or digital drawing tool)
- Access to course materials on control systems (Chapter 3)

#### Prerequisites

- Understanding of feedback control
- Familiarity with sensor types (IMU, force sensors)
- Knowledge of gait patterns in legged robots

#### Instructions

1. Define the control problem:
   - What are the inputs (sensors)?
   - What are the outputs (actuators)?
   - What are the disturbances?
2. Sketch a block diagram showing:
   - Sensor inputs
   - Control algorithms
   - Actuator outputs
   - Feedback loops
3. For each component, specify:
   - Type of controller (PID, MPC, etc.)
   - Update frequency
   - Key parameters to tune
4. Identify potential failure modes:
   - What happens if a sensor fails?
   - How to handle loss of balance?
5. Propose a testing strategy:
   - How would you validate this design?
   - What metrics would you use?

#### Expected Outcome

A comprehensive control system design document including:
- Annotated block diagram
- Justification for component choices
- Analysis of failure modes
- Testing plan

#### Verification

- [ ] Block diagram shows all major components
- [ ] Control algorithms are specified with rationale
- [ ] Feedback loops are clearly identified
- [ ] At least 3 failure modes analyzed
- [ ] Testing strategy includes quantitative metrics

#### Safety Notes

N/A (conceptual exercise)

#### Troubleshooting

N/A (conceptual exercise)

#### Extensions

1. Compare your design with an existing quadruped robot (e.g., Spot, ANYmal)
2. Simulate your control system using MATLAB/Simulink
3. Identify trade-offs between control complexity and computational cost

#### Related Resources

- Chapter 3: Motion Planning and Control
- [Boston Dynamics Spot Technical Overview](https://example.com)
- [Modern Robotics textbook Chapter 11](https://example.com)
```

---

## Validation Rules

### Pre-Submission Checklist

Before marking exercises as complete, verify:

#### Structure
- [ ] Exercise number matches format (X.Y)
- [ ] All required fields present
- [ ] All required sections present
- [ ] Markdown formatting correct (headings, lists, code blocks)

#### Content Quality
- [ ] Objective is clear and measurable
- [ ] Instructions are step-by-step and unambiguous
- [ ] Expected outcome is specific (not vague)
- [ ] Verification checklist is testable
- [ ] Difficulty level matches complexity

#### Type-Specific
- [ ] **Programming**: Code examples are runnable
- [ ] **Simulation**: Simulator specified with installation instructions
- [ ] **Hardware**: Safety notes present and comprehensive
- [ ] **Conceptual**: Evaluation rubric or example provided

#### Safety (Hardware Only)
- [ ] Safety notes section present
- [ ] Electrical hazards addressed
- [ ] Mechanical hazards addressed
- [ ] Clear "do NOT" warnings included

#### Accessibility
- [ ] Instructions assume beginner-level Linux/programming knowledge
- [ ] Jargon is explained
- [ ] External links are accessible (not paywalled)

---

## Difficulty Guidelines

### Beginner
- Target: Students new to robotics/programming
- Time: 15-60 minutes
- Prerequisites: Minimal (basic programming, high school physics)
- Scaffolding: Extensive guidance, starter code provided
- Example: "Control a servo motor with Arduino"

### Intermediate
- Target: Students with 1-2 courses in robotics
- Time: 45-120 minutes
- Prerequisites: Programming proficiency, understanding of key concepts
- Scaffolding: Moderate guidance, pseudocode or framework provided
- Example: "Implement inverse kinematics for 3-DOF arm"

### Advanced
- Target: Graduate students or experienced practitioners
- Time: 90-180 minutes
- Prerequisites: Strong theory and practice, multiple courses
- Scaffolding: Minimal guidance, open-ended problem
- Example: "Design and optimize a model predictive controller"

---

## Error Codes

| Code | Error | Resolution |
|------|-------|------------|
| `EX-001` | Missing required field | Add missing field (type, difficulty, etc.) |
| `EX-002` | Invalid field value | Correct value to match enum or constraints |
| `EX-003` | Missing required section | Add missing section (Objective, Instructions, etc.) |
| `EX-004` | Insufficient instructions | Expand instructions to at least 5 steps |
| `EX-005` | Vague expected outcome | Provide specific, measurable outcome |
| `EX-006` | Missing safety notes (hardware) | Add comprehensive safety section |
| `EX-007` | No verification checklist | Add at least 3 testable checkpoints |
| `EX-008` | Untested code example | Test code and verify it runs as described |
| `EX-009` | Missing materials list | List all required tools/software/hardware |
| `EX-010` | Difficulty mismatch | Adjust difficulty level to match complexity |

---

## Versioning

This contract follows semantic versioning:
- **Major**: Breaking changes to structure (e.g., new required sections)
- **Minor**: Non-breaking additions (e.g., new optional sections)
- **Patch**: Clarifications or corrections

**Current Version**: 1.0.0
**Last Updated**: 2025-12-01
