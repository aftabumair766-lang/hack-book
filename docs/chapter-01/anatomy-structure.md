---
id: anatomy-structure
title: "Robot Anatomy and Structure"
description: "Understanding the physical composition and morphology of humanoid robots"
section_number: "1.1"
---

# 1.1 Robot Anatomy and Structure

## Introduction

Humanoid robots are designed to mimic the human body's structure and capabilities. Understanding their anatomy is crucial for grasping how they perceive, process, and interact with the world.

## Human vs. Robot Anatomy

While humans have biological muscles and bones, robots use:
- **Rigid links** (metal/composite frames) instead of bones
- **Electric/hydraulic actuators** instead of muscles
- **Sensors** instead of biological senses
- **Electronic controllers** instead of nervous systems

## Major Components

### Head
- **Sensors**: Cameras (vision), microphones (audio), depth sensors
- **Processing**: Often houses main computer or vision processors
- **Communication**: Displays, speakers for human interaction

###Torso
- **Power systems**: Batteries, power management
- **Main computer**: Central processing unit
- **Structural support**: Connects upper and lower body

### Arms (Upper Limbs)
- **Shoulder**: 3 DOF (pitch, roll, yaw)
- **Elbow**: 1-2 DOF (flexion/extension)
- **Wrist**: 2-3 DOF (rotation, pitch, roll)
- **Hand/Gripper**: 1-5 DOF per finger

### Legs (Lower Limbs)
- **Hip**: 3 DOF (pitch, roll, yaw)
- **Knee**: 1 DOF (flexion)
- **Ankle**: 2 DOF (pitch, roll)
- **Foot**: Flat or articulated with force sensors

## Degrees of Freedom (DOF)

**Definition**: A degree of freedom is an independent direction of motion for a joint or robot.

**Examples**:
- **Revolute joint** (hinge): 1 DOF rotation
- **Prismatic joint** (slider): 1 DOF translation
- **Ball joint** (shoulder): 3 DOF rotation

**Typical humanoid DOF counts**:
- ASIMO: 57 DOF total
- Atlas: 28 DOF total
- Human body: ~244 DOF (much more complex!)

## Design Trade-offs

| Factor | Increasing... | Trade-off |
|--------|---------------|-----------|
| **DOF** | More dexterity | Higher complexity, cost, control difficulty |
| **Weight** | Stronger structure | Requires more powerful actuators, less efficient |
| **Size** | Greater reach/payload | Harder to balance, more expensive |
| **Material** | Lighter composites | Often more expensive, less durable |

## Key Takeaways

:::tip Key Points
- Humanoid robots mimic human anatomy with mechanical equivalents
- Each joint has 1-3 degrees of freedom (DOF)
- More DOF = more capability but also more complexity
- Design involves balancing weight, strength, cost, and complexity
- Modern humanoids have 20-60 DOF total
:::

**Next**: [Sensors and Actuators](./sensors-actuators.md)
