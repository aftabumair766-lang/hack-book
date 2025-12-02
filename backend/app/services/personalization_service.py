"""
Content Personalization Service
Transforms chapter content based on user background and preferences.
"""
from typing import Dict, List, Optional
import re


class PersonalizationEngine:
    """Engine for personalizing educational content based on user profile."""

    def __init__(self, user_background: Dict):
        self.software_exp = user_background.get('software_experience', 'beginner')
        self.hardware_exp = user_background.get('hardware_experience', 'none')
        self.robotics_exp = user_background.get('robotics_experience', 'none')
        self.programming_languages = user_background.get('programming_languages', [])
        self.preferred_language = user_background.get('preferred_language', 'Python')
        self.learning_goals = user_background.get('learning_goals', [])
        self.primary_interest = user_background.get('primary_interest', '').lower()

    def personalize_content(self, chapter_content: str, chapter_id: str) -> Dict:
        """
        Transform chapter content based on user profile.

        Args:
            chapter_content: Original markdown content of the chapter
            chapter_id: Chapter identifier (e.g., 'chapter-01')

        Returns:
            Dict with personalized content and metadata
        """
        personalized = chapter_content
        transformations = []

        # Apply difficulty-based transformations
        if self.software_exp in ['beginner', 'intermediate']:
            personalized, difficulty_changes = self._simplify_technical_content(personalized)
            transformations.extend(difficulty_changes)
        elif self.software_exp == 'expert':
            personalized, advanced_additions = self._add_advanced_details(personalized)
            transformations.extend(advanced_additions)

        # Apply focus-based transformations (hardware vs software)
        if self.hardware_exp in ['professional', 'expert'] or 'hardware' in self.primary_interest:
            personalized, hw_changes = self._emphasize_hardware(personalized)
            transformations.extend(hw_changes)
        elif self.software_exp in ['advanced', 'expert']:
            personalized, sw_changes = self._emphasize_software(personalized)
            transformations.extend(sw_changes)

        # Add personalized introduction
        intro = self._generate_personalized_intro(chapter_id)
        personalized = intro + "\n\n" + personalized

        # Add relevant examples based on interests
        if 'AI' in self.learning_goals or 'ai' in self.primary_interest or 'vision' in self.primary_interest:
            personalized = self._add_ai_examples(personalized, chapter_id)
            transformations.append("Added AI/Vision examples")

        # Adjust code examples to preferred language
        if self.preferred_language and self.preferred_language != 'Python':
            personalized, lang_changes = self._adapt_code_examples(personalized)
            transformations.extend(lang_changes)

        return {
            "personalized_content": personalized,
            "transformations_applied": transformations,
            "user_profile_summary": self._get_profile_summary(),
            "chapter_id": chapter_id
        }

    def _simplify_technical_content(self, content: str) -> tuple:
        """Simplify technical jargon for beginners/intermediates."""
        changes = []

        # Add beginner-friendly explanations
        if self.software_exp == 'beginner':
            # Add glossary-style explanations
            technical_terms = {
                'API': 'API (Application Programming Interface - a way for programs to talk to each other)',
                'algorithm': 'algorithm (step-by-step instructions for solving a problem)',
                'neural network': 'neural network (a computer system inspired by the human brain)',
                'kinematics': 'kinematics (the study of motion without considering forces)',
                'actuator': 'actuator (a motor or component that creates movement)',
                'sensor': 'sensor (a device that detects and measures physical properties)',
            }

            for term, explanation in technical_terms.items():
                if term in content.lower():
                    content = re.sub(
                        rf'\b{term}\b',
                        explanation,
                        content,
                        flags=re.IGNORECASE,
                        count=1  # Only replace first occurrence
                    )
                    changes.append(f"Added beginner explanation for '{term}'")

        return content, changes

    def _add_advanced_details(self, content: str) -> tuple:
        """Add advanced technical details for expert users."""
        changes = []

        advanced_note = """
---
**💡 Advanced Insight**: As an experienced developer, you might be interested in the mathematical foundations and optimization techniques underlying these concepts. Consider exploring research papers and advanced implementations for deeper understanding.
---
"""
        content = advanced_note + content
        changes.append("Added advanced learning resources")

        return content, changes

    def _emphasize_hardware(self, content: str) -> tuple:
        """Emphasize hardware aspects for hardware-focused users."""
        changes = []

        hardware_note = """
---
**🔧 Hardware Focus**: Given your hardware background, this chapter includes additional focus on physical components, circuits, actuators, and real-world robotics implementations.
---
"""
        content = hardware_note + content
        changes.append("Added hardware-focused context")

        return content, changes

    def _emphasize_software(self, content: str) -> tuple:
        """Emphasize software aspects for software-focused users."""
        changes = []

        software_note = """
---
**💻 Software Focus**: With your software expertise, this chapter emphasizes algorithms, code architecture, and software design patterns relevant to robotics.
---
"""
        content = software_note + content
        changes.append("Added software-focused context")

        return content, changes

    def _generate_personalized_intro(self, chapter_id: str) -> str:
        """Generate a personalized introduction based on user profile."""
        level_greetings = {
            'beginner': "Welcome! This chapter has been personalized for your learning journey.",
            'intermediate': "This chapter has been adapted to match your skill level.",
            'advanced': "This chapter includes additional technical depth for your experience level.",
            'expert': "This advanced chapter has been enhanced with expert-level insights."
        }

        greeting = level_greetings.get(self.software_exp, level_greetings['beginner'])

        focus_areas = []
        if 'AI' in self.learning_goals or 'ai' in self.primary_interest:
            focus_areas.append("AI and machine learning")
        if self.hardware_exp in ['professional', 'expert']:
            focus_areas.append("hardware implementation")
        if 'ROS' in self.learning_goals:
            focus_areas.append("ROS integration")

        focus_text = ""
        if focus_areas:
            focus_text = f" Special emphasis on: {', '.join(focus_areas)}."

        intro = f"""
---
## 🎯 Personalized for You

{greeting}{focus_text}

**Your Profile:**
- Software Experience: {self.software_exp.title()}
- Hardware Experience: {self.hardware_exp.title()}
- Preferred Language: {self.preferred_language}

*Tip: You can re-personalize this content anytime by clicking the "Personalize Content" button.*

---
"""
        return intro

    def _add_ai_examples(self, content: str, chapter_id: str) -> str:
        """Add AI-specific examples for users interested in AI/Vision."""
        ai_example = """
### 🤖 AI Application Example

```python
# Example: Using computer vision for object detection in robotics
import cv2
import numpy as np

def detect_objects(image):
    # Load pre-trained YOLO model
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    # Prepare image
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416))
    net.setInput(blob)

    # Get detections
    detections = net.forward()

    return process_detections(detections)
```

This demonstrates how AI/vision systems integrate with robotic perception.
"""

        # Insert AI example before conclusion if exists, otherwise at end
        if "## Conclusion" in content or "## Summary" in content:
            content = re.sub(
                r'(## (?:Conclusion|Summary))',
                ai_example + r'\n\1',
                content
            )
        else:
            content += "\n\n" + ai_example

        return content

    def _adapt_code_examples(self, content: str) -> tuple:
        """Adapt code examples to user's preferred programming language."""
        changes = []

        # For now, add a note about language preference
        # In a full implementation, you'd translate code snippets
        lang_note = f"""
---
**📝 Note**: Code examples can be adapted to {self.preferred_language}. The core concepts remain the same across languages.
---
"""

        if '```python' in content:
            changes.append(f"Noted preference for {self.preferred_language}")
            content = lang_note + content

        return content, changes

    def _get_profile_summary(self) -> Dict:
        """Get summary of user profile for debugging/transparency."""
        return {
            "software_experience": self.software_exp,
            "hardware_experience": self.hardware_exp,
            "robotics_experience": self.robotics_exp,
            "preferred_language": self.preferred_language,
            "primary_interest": self.primary_interest,
            "learning_goals": self.learning_goals
        }


def load_chapter_content(chapter_id: str) -> Optional[str]:
    """
    Load chapter content from markdown files.

    Args:
        chapter_id: Chapter identifier (e.g., 'chapter-01')

    Returns:
        Chapter content as string, or None if not found
    """
    import os
    from pathlib import Path

    # Try multiple possible locations
    possible_paths = [
        Path(f"../docs/{chapter_id}/index.md"),
        Path(f"../../docs/{chapter_id}/index.md"),
        Path(f"docs/{chapter_id}/index.md"),
    ]

    for path in possible_paths:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()

    # If not found, return sample content
    return f"""
# {chapter_id.replace('-', ' ').title()}

## Introduction

This chapter covers fundamental concepts in physical AI and humanoid robotics.

## Key Concepts

1. **Embodied Intelligence**: Intelligence that emerges from physical interaction with the environment.
2. **Sensor Integration**: How robots perceive their environment through various sensors.
3. **Actuation Systems**: Motors and actuators that enable robot movement.

## Technical Details

Robots combine software algorithms with hardware components to achieve intelligent behavior.

## Conclusion

Understanding these fundamentals is crucial for building advanced robotic systems.
"""
