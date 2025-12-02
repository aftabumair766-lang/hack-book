---
id: chapter-04
title: "Chapter 4: Locomotion and Mobility"
sidebar_label: "Ch 4: Locomotion"
sidebar_position: 5
description: "Learn bipedal walking, balance, gait generation, and terrain adaptation"
keywords:
  - bipedal walking
  - gait generation
  - zero moment point
  - balance control
  - terrain adaptation
---

import TranslateButton from '@site/src/components/TranslateButton';

<TranslateButton chapterId="chapter-04" />

# Chapter 4: Locomotion and Mobility

## Introduction

Bipedal locomotion is one of the most challenging aspects of humanoid robotics. Walking on two legs requires dynamic balance, precise coordination, and robust control. This chapter explores the principles and techniques that enable humanoid robots to walk, run, and navigate complex terrains.

### What You'll Learn

- Bipedal walking fundamentals
- Gait generation and trajectory planning
- Balance and stability (ZMP, capture point)
- Terrain adaptation and footstep planning
- Running and dynamic locomotion

### Prerequisites

- Chapter 1: Kinematics and Dynamics
- Chapter 3: Control Systems
- Understanding of inverted pendulum dynamics

---

## Key Topics

### 4.1 Bipedal Walking Fundamentals

**Gait Cycle Phases**
1. **Double support**: Both feet on ground
2. **Single support**: One foot on ground, other swinging
3. **Impact**: Foot strikes ground (brief)

**Static vs Dynamic Walking**
- **Static**: Center of mass always above support polygon (slow, stable)
- **Dynamic**: Center of mass moves outside support (faster, more efficient, requires active balance)

**Challenges**
- High-dimensional state space (many joints)
- Underactuation (can't control all DOF independently)
- Hybrid dynamics (contact/no contact switches)
- Disturbances (uneven terrain, pushes)

### 4.2 Zero Moment Point (ZMP)

**Definition**: Point on ground where net moment from gravity and inertia is zero.

**ZMP Criterion**
- If ZMP is inside support polygon → stable
- If ZMP is outside → robot will tip over

**Mathematical Formulation**

The ZMP x-coordinate is calculated from the robot's mass distribution, accelerations, and gravity. (Full equation available in robotics textbooks like Kajita et al.)

**Applications**
- Trajectory planning (keep ZMP inside support)
- Balance verification
- Used in ASIMO, HRP series robots

### 4.3 Gait Generation

**Trajectory Planning Methods**

**1. Preview Control**
- Plan Center of Mass (CoM) trajectory
- Predict future reference trajectory
- Optimal control to track ZMP

**2. Inverted Pendulum Models**
- **LIPM** (Linear Inverted Pendulum Model)
- Simplify full dynamics to 3D point mass
- Analytical solutions for step planning

**3. Optimization-Based**
- Define cost function (energy, smoothness)
- Constraints (joint limits, ZMP, kinematics)
- Solve for optimal trajectory

**Footstep Planning**
- Discrete search (A*, RRT) for footstep locations
- Continuous optimization for step timing and placement

### 4.4 Balance and Stability

**Capture Point Theory**
- **Capture Point (CP)**: Location to step to in order to stop
- If robot steps on CP, it can come to rest
- Used for: Push recovery, step adjustment

**Push Recovery Strategies**
1. **Ankle strategy**: Torque at ankle (small disturbances)
2. **Hip strategy**: Hip torque to shift CoM (medium disturbances)
3. **Step strategy**: Take a step (large disturbances)

**Whole-Body Control**
- Control all joints simultaneously for balance
- Quadratic Programming (QP) to solve for joint torques
- Handle multiple objectives (balance, tracking, limits)

### 4.5 Terrain Adaptation

**Perception for Locomotion**
- Vision-based terrain classification
- Height maps from depth sensors
- Obstacle detection and avoidance

**Adaptive Footstep Planning**
- Adjust step length/width based on terrain
- Avoid obstacles and unsafe areas
- Online replanning for dynamic environments

**Stair Climbing and Rough Terrain**
- Higher foot clearance
- Precise foot placement
- Adapt gait parameters (step height, timing)

### 4.6 Dynamic Locomotion

**Running**
- Flight phase (both feet off ground)
- Higher impact forces
- More complex dynamics than walking

**Jumping**
- Generate large ground reaction forces
- Coordinate swing of arms and crouch
- Landing impact absorption

**Recent Advances**
- Reinforcement learning for robust locomotion
- Sim-to-real transfer (train in simulation)
- Adaptive controllers that learn from experience

---

## Learning Objectives

After completing this chapter, you will be able to:

1. **Explain** the phases of bipedal gait and their challenges
2. **Calculate** the Zero Moment Point for a given configuration
3. **Design** simple walking trajectories using inverted pendulum models
4. **Understand** balance strategies and push recovery
5. **Describe** footstep planning for terrain adaptation

---

## Summary

### Key Takeaways

- **Bipedal walking** requires dynamic balance and precise coordination
- **ZMP** is a key stability criterion: must stay inside support polygon
- **Gait generation** plans CoM and foot trajectories for stable walking
- **Inverted pendulum models** simplify dynamics for analytical solutions
- **Capture point** enables reactive balance and push recovery
- **Whole-body control** coordinates all joints for complex motions
- **Terrain adaptation** requires perception, planning, and adaptive control
- **Modern approaches** use learning-based methods for robust locomotion

---

## Case Studies

### Honda ASIMO
- ZMP-based walking (preview control)
- Smooth, stable walking at 2.7 km/h
- Stair climbing and running capabilities

### Boston Dynamics Atlas
- Model Predictive Control for locomotion
- Runs, jumps, and does backflips
- Robust push recovery and rough terrain navigation

### Cassie (Agility Robotics)
- Underactuated design for energy efficiency
- Reinforcement learning for adaptive walking
- Outdoor navigation on varied terrain

### Tesla Optimus
- Learning-based locomotion policies
- Sim-to-real transfer for rapid iteration
- Adaptive balance control

---

## Practical Exercises

### Exercise 4.1: ZMP Calculation
Calculate ZMP for a simple 2D model of a walking robot.

### Exercise 4.2: LIPM Simulation
Simulate a Linear Inverted Pendulum Model for a single step.

### Exercise 4.3: Footstep Planning
Implement A* search for footstep planning around obstacles.

### Exercise 4.4: Balance Controller
Design a controller to maintain balance under disturbances (simulated push).

---

## References

1. S. Kajita et al., *Introduction to Humanoid Robotics*. Springer, 2014.
2. T. Takenaka et al., "Real-time motion generation and control for biped robot," *IROS*, 2009.
3. J. Englsberger et al., "Three-dimensional bipedal walking control using Divergent Component of Motion," *IROS*, 2013.
4. X. Da and J. Grizzle, "Combining trajectory optimization, supervised machine learning, and model structure for mitigating the curse of dimensionality in the control of bipedal robots," *IJRR*, 2019.
5. J. Siekmann et al., "Blind Bipedal Stair Traversal via Sim-to-Real Reinforcement Learning," *RSS*, 2021.

---

**Estimated Reading Time**: 60 minutes

**Previous**: [Chapter 3: Control Systems](../chapter-03/index.md) | **Next**: [Chapter 5: Manipulation](../chapter-05/index.md)
