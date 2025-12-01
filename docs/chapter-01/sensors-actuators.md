---
id: sensors-actuators
title: "Sensors and Actuators"
description: "Types of sensors and actuators used in humanoid robotics and their selection criteria"
section_number: "1.2"
---

# 1.2 Sensors and Actuators

## Introduction

Robots need **sensors** to perceive the world and **actuators** to take action. This section covers the main types used in humanoid systems.

## Sensor Types

### 1. Vision Sensors (Cameras)
- **RGB cameras**: Color images for object recognition
- **Depth cameras**: Distance measurement (stereo, ToF, structured light)
- **Use cases**: Navigation, object detection, gesture recognition

### 2. Inertial Measurement Units (IMUs)
- **Components**: Accelerometers + gyroscopes (+ magnetometers)
- **Measures**: Acceleration, angular velocity, orientation
- **Use cases**: Balance, fall detection, pose estimation

### 3. Force/Torque Sensors
- **Location**: Joints, feet, hands
- **Measures**: Contact forces and torques
- **Use cases**: Grasping control, ground contact detection, collision avoidance

### 4. Tactile Sensors
- **Types**: Pressure-sensitive skin, touch pads
- **Measures**: Contact location and pressure distribution
- **Use cases**: Delicate manipulation, human-robot interaction

### 5. Joint Encoders
- **Types**: Optical, magnetic, absolute/incremental
- **Measures**: Joint angle position and velocity
- **Use cases**: Motor control, kinematics calculations

## Sensor Fusion

**Concept**: Combining data from multiple sensors for better accuracy.

**Example**: Maintaining balance
- IMU provides orientation
- Force sensors detect foot contact
- Vision provides environmental context
- Controller fuses all data for stable walking

## Actuator Types

### 1. Servo Motors
- **Characteristics**: High precision, position control, moderate torque
- **Power**: Electric (DC brushless common)
- **Use**: Arms, hands, lightweight robots
- **Pros**: Accurate, controllable, quiet
- **Cons**: Limited torque, moderate cost

### 2. DC Motors
- **Characteristics**: High speed, continuous rotation
- **Power**: Electric with gearboxes for torque
- **Use**: Wheels, continuous motion tasks
- **Pros**: Simple, cost-effective, reliable
- **Cons**: Less precise without feedback control

### 3. Hydraulic Actuators
- **Characteristics**: Very high force/torque, robust
- **Power**: Pressurized hydraulic fluid
- **Use**: Large humanoids (Atlas), heavy-duty applications
- **Pros**: Extreme power-to-weight ratio, fast response
- **Cons**: Complex, noisy, requires pumps/fluid management

## Selection Criteria

| Application | Recommended Actuator | Key Reason |
|-------------|---------------------|------------|
| Fine manipulation | Servo motors | Precision and control |
| Bipedal locomotion | Hydraulic or high-torque electric | Power for dynamic walking |
| Low-cost hobby robot | DC motors with encoders | Cost-effectiveness |
| High-speed motion | Hydraulic | Fast response time |

## Key Takeaways

:::tip Key Points
- **5 main sensor types**: Vision, IMU, force/torque, tactile, encoders
- **Sensor fusion** combines multiple sensors for robust perception
- **3 main actuator types**: Servo (precision), DC (speed), hydraulic (power)
- Selection depends on **application requirements**: cost, precision, force, speed
- Modern humanoids use **sensor fusion** for balance and navigation
:::

**Previous**: [Robot Anatomy](./anatomy-structure.md) | **Next**: [Kinematics and Dynamics](./kinematics-dynamics.md)
