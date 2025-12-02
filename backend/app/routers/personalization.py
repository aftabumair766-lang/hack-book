"""
Personalization API Router
Handles chapter content personalization based on user profiles.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.models.database import get_db
from app.models.user import User, UserBackground
from app.models.auth_schemas import TokenData
from app.core.auth import decode_access_token
from app.services.personalization_service import PersonalizationEngine, load_chapter_content
from pydantic import BaseModel


router = APIRouter()


class PersonalizeRequest(BaseModel):
    """Request model for chapter personalization."""
    chapter_id: str


class PersonalizationResponse(BaseModel):
    """Response model for personalized content."""
    personalized_content: str
    transformations_applied: list
    user_profile_summary: dict
    chapter_id: str
    original_length: int
    personalized_length: int


def get_current_user(
    token: str,
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from token.

    Args:
        token: JWT access token (from Authorization header)
        db: Database session

    Returns:
        User object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Remove 'Bearer ' prefix if present
    if token.startswith('Bearer '):
        token = token[7:]

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    user_id = payload.get('user_id')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post("/api/personalize/chapter", response_model=PersonalizationResponse)
async def personalize_chapter(
    request: PersonalizeRequest,
    authorization: str,
    db: Session = Depends(get_db)
):
    """
    Personalize chapter content based on user's background and preferences.

    **Flow:**
    1. Validate user authentication
    2. Fetch user background from database
    3. Load original chapter content
    4. Apply personalization transformations
    5. Return personalized content

    **Personalization Factors:**
    - Software experience level (beginner → simpler, expert → advanced)
    - Hardware/robotics background (hardware → more physical examples)
    - Programming language preference (adapt code examples)
    - Learning goals (AI → vision examples, ROS → integration examples)
    - Primary interests (emphasize relevant aspects)

    Args:
        request: Contains chapter_id to personalize
        authorization: JWT token from Authorization header
        db: Database session

    Returns:
        PersonalizationResponse with transformed content

    Raises:
        HTTPException: If user not found, not authenticated, or chapter not found
    """
    # Get authenticated user
    user = get_current_user(authorization, db)

    # Check if user has completed questionnaire
    if not user.has_completed_questionnaire:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete the background questionnaire before personalizing content"
        )

    # Fetch user background
    background = db.query(UserBackground).filter(
        UserBackground.user_id == user.id
    ).first()

    if not background:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User background not found"
        )

    # Load chapter content
    chapter_content = load_chapter_content(request.chapter_id)
    if not chapter_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter '{request.chapter_id}' not found"
        )

    # Build user profile dict
    user_profile = {
        'software_experience': background.software_experience,
        'hardware_experience': background.hardware_experience,
        'robotics_experience': background.robotics_experience,
        'programming_languages': background.programming_languages,
        'preferred_language': background.preferred_language,
        'learning_goals': background.learning_goals,
        'primary_interest': background.primary_interest,
        'skill_level': background.skill_level,
    }

    # Personalize content
    engine = PersonalizationEngine(user_profile)
    result = engine.personalize_content(chapter_content, request.chapter_id)

    # Return response
    return PersonalizationResponse(
        personalized_content=result['personalized_content'],
        transformations_applied=result['transformations_applied'],
        user_profile_summary=result['user_profile_summary'],
        chapter_id=result['chapter_id'],
        original_length=len(chapter_content),
        personalized_length=len(result['personalized_content'])
    )


@router.get("/api/personalize/preview/{chapter_id}")
async def preview_personalization(
    chapter_id: str,
    authorization: str,
    db: Session = Depends(get_db)
):
    """
    Preview what transformations would be applied without returning full content.

    Args:
        chapter_id: Chapter to preview
        authorization: JWT token
        db: Database session

    Returns:
        Summary of transformations that would be applied
    """
    user = get_current_user(authorization, db)

    if not user.has_completed_questionnaire:
        return {
            "can_personalize": False,
            "reason": "Questionnaire not completed"
        }

    background = db.query(UserBackground).filter(
        UserBackground.user_id == user.id
    ).first()

    if not background:
        return {
            "can_personalize": False,
            "reason": "Background not found"
        }

    user_profile = {
        'software_experience': background.software_experience,
        'hardware_experience': background.hardware_experience,
        'robotics_experience': background.robotics_experience,
        'programming_languages': background.programming_languages,
        'preferred_language': background.preferred_language,
        'learning_goals': background.learning_goals,
        'primary_interest': background.primary_interest,
    }

    # Predict transformations
    transformations = []
    if background.software_experience in ['beginner', 'intermediate']:
        transformations.append("Simplify technical terms")
    elif background.software_experience == 'expert':
        transformations.append("Add advanced technical details")

    if background.hardware_experience in ['professional', 'expert']:
        transformations.append("Emphasize hardware implementation")

    if 'AI' in background.learning_goals or 'ai' in background.primary_interest.lower():
        transformations.append("Add AI/Vision examples")

    return {
        "can_personalize": True,
        "chapter_id": chapter_id,
        "user_level": background.software_experience,
        "predicted_transformations": transformations,
        "user_profile": user_profile
    }
