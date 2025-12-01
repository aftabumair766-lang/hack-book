---
id: exercises
title: "Chapter 1 Exercises"
description: "Hands-on exercises for Chapter 1: Foundations of Humanoid Robotics"
---

# Chapter 1: Exercises

## Exercise 1.1: Component Identification

**Type**: Conceptual | **Difficulty**: Beginner | **Time**: 20 minutes

### Objective
Identify and describe major anatomical components of humanoid robots.

### Instructions
1. Research images of Honda ASIMO, Boston Dynamics Atlas, and Tesla Optimus
2. For each robot, identify these components:
   - Head and sensor systems
   - Torso and power systems
   - Arms (shoulder, elbow, wrist, hand)
   - Legs (hip, knee, ankle, foot)
3. Estimate the total degrees of freedom (DOF) for one of the robots
4. Compare to human anatomy: What's similar? What's different?

### Success Criteria
- [ ] Identified at least 8 major components per robot
- [ ] Explained the function of each component
- [ ] Estimated DOF within 20% of actual value
- [ ] Compared at least 3 differences from human anatomy

---

## Exercise 1.2: Sensor Selection Challenge

**Type**: Design | **Difficulty**: Intermediate | **Time**: 30 minutes

### Objective
Select appropriate sensors for specific robot capabilities.

### Scenarios

**Scenario A**: Robot must walk on uneven outdoor terrain
*Question*: What sensors would you use and why?

**Scenario B**: Robot must grasp fragile objects (eggs, glassware)
*Question*: What sensors are critical?

**Scenario C**: Robot must navigate crowded indoor spaces
*Question*: Which sensors enable safe navigation?

### Required
For each scenario, specify:
1. At least 3 sensor types
2. Justification for each sensor
3. How sensors work together (sensor fusion)

### Success Criteria
- [ ] Selected appropriate sensors for each scenario
- [ ] Justified each selection with technical reasoning
- [ ] Described sensor fusion strategy
- [ ] Considered trade-offs (cost, weight, complexity)

---

## Exercise 1.3: Forward Kinematics Programming

**Type**: Programming | **Difficulty**: Intermediate | **Time**: 45 minutes

### Objective
Implement and test forward kinematics for a 3-DOF robot arm.

### Prerequisites
- Python 3.10+
- NumPy library
- Matplotlib (optional, for visualization)

### Instructions

1. **Extend the 2-DOF example** to 3 degrees of freedom:

```python
import numpy as np

def forward_kinematics_3dof(theta1, theta2, theta3, L1, L2, L3):
    """
    Calculate end-effector position for 3-DOF planar arm.

    Parameters:
    theta1, theta2, theta3: Joint angles (radians)
    L1, L2, L3: Link lengths (meters)

    Returns:
    (x, y): End-effector position
    """
    # TODO: Implement this function
    pass

# Test cases
print(forward_kinematics_3dof(0, 0, 0, 1.0, 0.8, 0.6))  # All straight
print(forward_kinematics_3dof(np.pi/2, 0, 0, 1.0, 0.8, 0.6))  # 90° at joint 1
```

2. **Plot the workspace**: Generate 100 random joint configurations and plot reachable positions

3. **Analyze**: What is the maximum reach? What shape is the workspace?

### Success Criteria
- [ ] Function correctly computes (x, y) for 3-DOF arm
- [ ] Test cases pass with correct values
- [ ] Workspace visualization shows reachable region
- [ ] Maximum reach calculated correctly

---

## Exercise 1.4: Inverse Kinematics Exploration

**Type**: Analysis | **Difficulty**: Advanced | **Time**: 60 minutes

### Objective
Explore inverse kinematics solutions and identify singularities.

### Instructions

1. **Multiple Solutions**: For a 2-DOF arm, find 2 different joint configurations that reach position (1.0, 1.0)

2. **No Solution**: Identify a target position that is **unreachable** for the arm (explain why)

3. **Singularity**: Find a configuration where the arm loses a degree of freedom (both links aligned)

### Hint
For 2-DOF, you can use geometry or numerical methods (scipy.optimize).

### Success Criteria
- [ ] Found at least 2 solutions for the given target
- [ ] Identified unreachable position with justification
- [ ] Described singularity configuration and its effects

---

## Exercise 1.5: Dynamics Simulation

**Type**: Simulation | **Difficulty**: Advanced | **Time**: 90 minutes

### Objective
Simulate simple pendulum dynamics and observe effects of mass and length.

### Prerequisites
- Python 3.10+
- NumPy, Matplotlib
- Optional: PyBullet or simple physics simulator

### Instructions

1. **Model a simple pendulum** with:
   - Length L = 1.0 m
   - Mass m = 1.0 kg
   - Initial angle θ₀ = 45°

2. **Simulate motion** using Euler integration or RK4

3. **Vary parameters**:
   - Double the mass: How does period change?
   - Double the length: How does period change?
   - Compare to theoretical period: `T = 2\pi\sqrt{L/g}`

### Success Criteria
- [ ] Pendulum simulation produces realistic oscillation
- [ ] Period matches theoretical value within 5%
- [ ] Correctly identified that mass doesn't affect period
- [ ] Correctly identified that period ∝ √L

---

## Solutions and Verification

Solutions and detailed explanations will be provided separately. Attempt all exercises before consulting solutions.

**Next Chapter**: [Chapter 2: Artificial Intelligence in Physical Systems](../chapter-02/index.md)
