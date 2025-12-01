---
id: kinematics-dynamics
title: "Kinematics and Dynamics"
description: "Mathematical foundations of robot motion: kinematics and dynamics"
section_number: "1.3"
---

# 1.3 Kinematics and Dynamics

## Introduction

**Kinematics** describes robot motion geometry (positions, velocities) without considering forces.
**Dynamics** includes forces and torques that cause motion.

## Kinematics Fundamentals

### Forward Kinematics

**Problem**: Given joint angles, find end-effector position.

**2-DOF Planar Arm Example**:

$$
x = L_1 \cos(\theta_1) + L_2 \cos(\theta_1 + \theta_2)
$$

$$
y = L_1 \sin(\theta_1) + L_2 \sin(\theta_1 + \theta_2)
$$

Where:
- L₁, L₂ = link lengths
- θ₁, θ₂ = joint angles
- (x, y) = end-effector position

**Python Example**:

```python
import numpy as np

def forward_kinematics_2dof(theta1, theta2, L1, L2):
    """Calculate end-effector position for 2-DOF planar arm."""
    x = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    y = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
    return (x, y)

# Example usage
theta1 = np.pi / 4  # 45 degrees
theta2 = np.pi / 6  # 30 degrees
L1, L2 = 1.0, 0.8   # meters

pos = forward_kinematics_2dof(theta1, theta2, L1, L2)
print(f"End-effector: ({pos[0]:.3f}, {pos[1]:.3f}) m")
# Output: (1.532, 1.207) m
```

### Denavit-Hartenberg (DH) Parameters

A standard convention for describing robot kinematics with 4 parameters per link:
- a = link length
- α = link twist
- d = link offset
- θ = joint angle

(Full DH derivation covered in advanced courses)

### Inverse Kinematics

**Problem**: Given desired end-effector position, find joint angles.

**Challenges**:
1. **Multiple solutions**: Same position, different joint configurations
2. **No solution**: Position outside reachable workspace
3. **Singularities**: Infinite solutions or loss of DOF

**Solution methods**: Analytical (closed-form), numerical (iterative)

## Dynamics Fundamentals

### Newton-Euler Equations

Robot dynamics governed by Newton's laws:

```
τ = I × α + (other forces)
```

Where:
- τ (tau) = joint torque
- I = moment of inertia
- α (alpha) = angular acceleration

### Joint Torques

To move a robot link, motors must provide torque to:
1. Overcome gravity (weight of links)
2. Accelerate links (inertial forces)
3. Overcome friction

### Mass and Inertia Effects

- **Heavier links** require more torque to accelerate
- **Distribution of mass** affects rotational inertia
- **Payload** (carried object) changes dynamics
- Controllers must account for these effects for smooth motion

## Workspace Analysis

**Workspace**: Set of all reachable positions for the end-effector.

**Types**:
- **Reachable workspace**: All positions the end-effector can reach
- **Dexterous workspace**: Positions reachable with any orientation

**Factors**:
- Link lengths
- Joint limits (mechanical constraints)
- Singularities (lose degrees of freedom)

## Key Takeaways

:::tip Key Points
- **Forward kinematics**: Joint angles → End-effector position (straightforward)
- **Inverse kinematics**: End-effector position → Joint angles (challenging)
- **DH parameters**: Standard way to describe robot kinematics
- **Dynamics**: Accounts for forces, torques, mass, inertia
- **Singularities**: Configurations where robot loses DOF
- **Workspace**: Set of all positions robot can reach
:::

**Previous**: [Sensors and Actuators](./sensors-actuators.md) | **Next**: [Exercises](./exercises.md)
