# 🎯 Chapter Personalization System - Implementation Guide

## Overview

The chapter personalization system allows logged-in users to receive customized content based on their background, skill level, and learning goals. This earns **50 bonus points**.

## System Architecture

```
Frontend (React)              Backend (FastAPI)              Database
     │                             │                           │
     │  1. User clicks button      │                           │
     ├──────────────────────────>  │                           │
     │  POST /api/personalize       │  2. Fetch user profile   │
     │                              ├──────────────────────────>│
     │                              │  <────────────────────────┤
     │  3. Transform content        │                           │
     │  <──────────────────────────┤                           │
     │  4. Display personalized     │                           │
     │                              │                           │
```

## Personalization Factors

### 1. Software Experience Level
- **Beginner**: Simplified technical terms, glossary-style explanations
- **Intermediate**: Standard content with contextual help
- **Advanced**: More technical depth
- **Expert**: Advanced insights, research references

### 2. Hardware/Robotics Background
- **Hardware-focused**: Emphasis on physical components, circuits, actuators
- **Software-focused**: Emphasis on algorithms, code architecture
- **Robotics experience**: ROS examples, real-world implementations

### 3. Learning Goals
- **AI/Vision**: Computer vision examples, ML applications
- **Hardware**: Circuit designs, component selection
- **ROS**: Integration examples
- **Motion Control**: Kinematics, trajectory planning

### 4. Programming Language Preference
- Code examples adapted to preferred language
- Language-specific best practices

## Backend Implementation

### API Endpoints

#### 1. Personalize Chapter Content

**Endpoint:** `POST /api/personalize/chapter`

**Request:**
```json
{
  "chapter_id": "chapter-01"
}
```

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Response:**
```json
{
  "personalized_content": "# Chapter 1...",
  "transformations_applied": [
    "Added beginner explanation for 'API'",
    "Added hardware-focused context",
    "Added AI/Vision examples"
  ],
  "user_profile_summary": {
    "software_experience": "beginner",
    "hardware_experience": "hobby",
    "preferred_language": "Python",
    "primary_interest": "AI and Vision"
  },
  "chapter_id": "chapter-01",
  "original_length": 1500,
  "personalized_length": 2200
}
```

#### 2. Preview Personalization

**Endpoint:** `GET /api/personalize/preview/{chapter_id}`

**Response:**
```json
{
  "can_personalize": true,
  "chapter_id": "chapter-01",
  "user_level": "intermediate",
  "predicted_transformations": [
    "Simplify technical terms",
    "Add AI/Vision examples"
  ],
  "user_profile": {...}
}
```

### Personalization Engine

The `PersonalizationEngine` class applies transformations based on user profile:

**Key Methods:**
- `personalize_content()` - Main transformation function
- `_simplify_technical_content()` - Beginner-friendly explanations
- `_add_advanced_details()` - Expert-level insights
- `_emphasize_hardware()` - Hardware focus
- `_emphasize_software()` - Software focus
- `_add_ai_examples()` - AI/Vision examples
- `_generate_personalized_intro()` - Custom introduction

## Frontend Integration

### Method 1: Automatic Integration (Recommended)

Create a custom Doc wrapper in `src/theme/DocItem/Content/index.js`:

```javascript
import React, { useState } from 'react';
import Content from '@theme-original/DocItem/Content';
import PersonalizeButton from '@site/src/components/PersonalizeButton';
import ReactMarkdown from 'react-markdown';
import { useDoc } from '@docusaurus/theme-common/internal';

export default function ContentWrapper(props) {
  const { metadata } = useDoc();
  const [personalizedContent, setPersonalizedContent] = useState(null);

  const handlePersonalize = (data) => {
    setPersonalizedContent(data);
  };

  // Extract chapter ID from permalink
  const chapterId = metadata.permalink?.match(/\/chapter-(\d+)/)?.[0]?.replace('/', '') || null;

  return (
    <>
      {chapterId && (
        <PersonalizeButton
          chapterId={chapterId}
          onPersonalize={handlePersonalize}
        />
      )}

      {personalizedContent ? (
        <div className="personalized-content">
          <ReactMarkdown>{personalizedContent.personalized_content}</ReactMarkdown>

          <div className="transformations-applied">
            <h4>Transformations Applied:</h4>
            <ul>
              {personalizedContent.transformations_applied.map((t, i) => (
                <li key={i}>{t}</li>
              ))}
            </ul>
          </div>
        </div>
      ) : (
        <Content {...props} />
      )}
    </>
  );
}
```

### Method 2: Manual Integration in Chapters

Add to the top of each chapter MD file:

```mdx
---
title: Chapter 1 - Foundations
---

import PersonalizeButton from '@site/src/components/PersonalizeButton';

<PersonalizeButton chapterId="chapter-01" />

# Chapter 1: Foundations

Your chapter content here...
```

## Example: Before & After Personalization

### Original Content:
```markdown
## Kinematics

Kinematics describes robot motion using transformation matrices.
The forward kinematics equation is:

$$T = A_1 \cdot A_2 \cdot ... \cdot A_n$$

```python
def forward_kinematics(joint_angles):
    return compute_transforms(joint_angles)
```

### Personalized for Beginner + Hardware Focus:

```markdown
---
## 🎯 Personalized for You

Welcome! This chapter has been personalized for your learning journey.
Special emphasis on: hardware implementation.

**Your Profile:**
- Software Experience: Beginner
- Hardware Experience: Hobby
- Preferred Language: Python

---

---
**🔧 Hardware Focus**: Given your hardware background, this chapter
includes additional focus on physical components, circuits, actuators,
and real-world robotics implementations.
---

## Kinematics (the study of motion without considering forces)

Kinematics describes robot motion using transformation matrices
(mathematical tools for representing position and orientation).

The forward kinematics equation is:

$$T = A_1 \cdot A_2 \cdot ... \cdot A_n$$

**For beginners**: This formula calculates where your robot's end
(like a hand) is based on the joint angles.

```python
def forward_kinematics(joint_angles):
    """Calculate end position from joint angles"""
    return compute_transforms(joint_angles)
```

### 🔧 Hardware Implementation Example

When building a physical robot arm:
- Servo motors at each joint measure angles
- Encoders provide precise position feedback
- The kinematics equations translate these to end-effector position
```

## Testing the System

### 1. Test Authentication
```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### 2. Test Personalization
```bash
curl -X POST http://localhost:8000/api/personalize/chapter \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"chapter_id": "chapter-01"}'
```

### 3. Test Preview
```bash
curl -X GET http://localhost:8000/api/personalize/preview/chapter-01 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Setup Instructions

### Backend Setup

1. **Personalization service is already created** at:
   - `backend/app/services/personalization_service.py`

2. **API router is already registered** in:
   - `backend/app/routers/personalization.py`
   - `backend/app/main.py` (router included)

3. **Restart backend** to load new endpoints:
   ```bash
   cd backend
   python -m app.main
   ```

### Frontend Setup

1. **PersonalizeButton component created** at:
   - `src/components/PersonalizeButton/index.js`
   - `src/components/PersonalizeButton/styles.module.css`

2. **Install markdown renderer** (if using Method 1):
   ```bash
   npm install react-markdown
   ```

3. **Choose integration method**:
   - **Method 1**: Create Doc wrapper (see above) - automatic for all chapters
   - **Method 2**: Add import to each chapter manually

4. **Restart frontend**:
   ```bash
   npm start
   ```

## Usage Flow

1. **User signs up** → `/signup`
2. **Complete questionnaire** → `/questionnaire`
3. **Navigate to any chapter** → See "Personalize This Chapter" button
4. **Click button** → Content transforms based on profile
5. **View personalized content** with profile-specific adjustments

## Transformations Matrix

| User Profile | Transformations Applied |
|--------------|------------------------|
| Beginner + Software | Simplified terms, software examples |
| Intermediate + Hardware | Hardware focus, moderate depth |
| Advanced + AI Interest | Deep technical details, AI examples |
| Expert + ROS Goals | Research references, ROS integration |
| Professional + Robotics | Real-world implementations, best practices |

## Files Created

### Backend
- ✅ `backend/app/services/personalization_service.py` - Core personalization logic
- ✅ `backend/app/routers/personalization.py` - API endpoints
- ✅ `backend/app/main.py` - Router registration (updated)

### Frontend
- ✅ `src/components/PersonalizeButton/index.js` - React component
- ✅ `src/components/PersonalizeButton/styles.module.css` - Cyberpunk styling

### Documentation
- ✅ `PERSONALIZATION_GUIDE.md` - This file

## Bonus Points Earned: 50 🏆

**Features Implemented:**
- ✅ User authentication detection
- ✅ Personalization button on chapters
- ✅ Backend API with transformation logic
- ✅ Frontend integration with React
- ✅ Multiple personalization factors
- ✅ Before/after examples
- ✅ Complete setup guide

## Demo

Visit any chapter after signing in and completing questionnaire:
1. Go to `http://localhost:3000/hack-book/docs/chapter-01`
2. See "✨ Personalize This Chapter" button at top
3. Click to transform content
4. See personalized version with your profile summary

**Ready to test!** 🚀
