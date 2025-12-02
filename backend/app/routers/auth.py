"""
Authentication API endpoints (Signup, Signin, Profile, Questionnaire).
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.user import User, UserBackground, Base
from app.models.auth_schemas import (
    UserSignup, UserSignin, Token, UserResponse,
    BackgroundQuestionnaireSubmit, BackgroundQuestionnaireResponse,
    PersonalizedDashboard
)
from app.core.auth import (
    get_password_hash, verify_password, create_access_token, decode_access_token
)
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["authentication"])
security = HTTPBearer()

# Database setup
engine = create_engine(settings.database_url.replace('sqlite:///', 'sqlite:///./'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """
    Create a new user account.

    Returns JWT token and user information.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check username if provided
    if user_data.username:
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True,
        is_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create access token
    access_token = create_access_token(
        data={"user_id": new_user.id, "email": new_user.email}
    )

    # Check if questionnaire completed
    background = db.query(UserBackground).filter(UserBackground.user_id == new_user.id).first()

    user_response = UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        full_name=new_user.full_name,
        is_active=new_user.is_active,
        is_verified=new_user.is_verified,
        created_at=new_user.created_at,
        has_completed_questionnaire=background is not None
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.post("/signin", response_model=Token)
async def signin(credentials: UserSignin, db: Session = Depends(get_db)):
    """
    Sign in with email and password.

    Returns JWT token and user information.
    """
    # Find user
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Check if active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    # Create access token
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email}
    )

    # Check if questionnaire completed
    background = db.query(UserBackground).filter(UserBackground.user_id == user.id).first()

    user_response = UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        has_completed_questionnaire=background is not None
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user information."""
    background = db.query(UserBackground).filter(UserBackground.user_id == current_user.id).first()

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        has_completed_questionnaire=background is not None
    )


@router.post("/questionnaire", response_model=BackgroundQuestionnaireResponse, status_code=status.HTTP_201_CREATED)
async def submit_questionnaire(
    questionnaire: BackgroundQuestionnaireSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit background questionnaire after signup.

    This helps personalize the learning experience.
    """
    # Check if already submitted
    existing = db.query(UserBackground).filter(UserBackground.user_id == current_user.id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Questionnaire already submitted. Use PUT to update."
        )

    # Create background record
    background = UserBackground(
        user_id=current_user.id,
        software_experience=questionnaire.software_experience,
        years_coding=questionnaire.years_coding,
        hardware_experience=questionnaire.hardware_experience,
        robotics_experience=questionnaire.robotics_experience,
        programming_languages=questionnaire.programming_languages,
        preferred_language=questionnaire.preferred_language,
        learning_goals=questionnaire.learning_goals,
        primary_interest=questionnaire.primary_interest,
        skill_level=questionnaire.skill_level,
        education_level=questionnaire.education_level,
        industry=questionnaire.industry,
        project_goals=questionnaire.project_goals,
        time_commitment=questionnaire.time_commitment
    )

    db.add(background)
    db.commit()
    db.refresh(background)

    return BackgroundQuestionnaireResponse(
        id=background.id,
        user_id=background.user_id,
        software_experience=background.software_experience,
        years_coding=background.years_coding,
        hardware_experience=background.hardware_experience,
        robotics_experience=background.robotics_experience,
        programming_languages=background.programming_languages,
        preferred_language=background.preferred_language,
        learning_goals=background.learning_goals,
        primary_interest=background.primary_interest,
        skill_level=background.skill_level,
        education_level=background.education_level,
        industry=background.industry,
        project_goals=background.project_goals,
        time_commitment=background.time_commitment,
        completed_at=background.completed_at
    )


@router.get("/dashboard", response_model=PersonalizedDashboard)
async def get_personalized_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized dashboard based on user's background.

    Returns customized learning path and recommendations.
    """
    # Get user background
    background = db.query(UserBackground).filter(UserBackground.user_id == current_user.id).first()

    if not background:
        # Default dashboard for users without questionnaire
        return PersonalizedDashboard(
            welcome_message=f"Welcome, {current_user.full_name or current_user.email}! Complete your background questionnaire to get personalized recommendations.",
            recommended_chapters=[
                {"chapter": 1, "title": "Foundations of Humanoid Robotics", "reason": "Start with the basics"}
            ],
            learning_path=["Complete the background questionnaire", "Start with Chapter 1"],
            skill_level_badge="New Learner",
            quick_tips=["Complete your profile to get personalized content"],
            suggested_exercises=[]
        )

    # Generate personalized content based on background
    welcome_message = f"Welcome back, {current_user.full_name or current_user.email}! "

    if background.software_experience == "beginner":
        welcome_message += "We've curated a beginner-friendly learning path for you."
    elif background.software_experience in ["advanced", "expert"]:
        welcome_message += "Jump into advanced topics that match your expertise."
    else:
        welcome_message += "Your learning path is customized for intermediate learners."

    # Recommend chapters based on interests
    recommended_chapters = []
    if "perception" in background.primary_interest.lower():
        recommended_chapters.append({
            "chapter": 2,
            "title": "AI in Physical Systems",
            "reason": "Matches your interest in perception and computer vision"
        })
    if "control" in background.primary_interest.lower():
        recommended_chapters.append({
            "chapter": 3,
            "title": "Control Systems",
            "reason": "Perfect for learning robot control"
        })
    if "manipulation" in background.primary_interest.lower():
        recommended_chapters.append({
            "chapter": 5,
            "title": "Manipulation and Dexterity",
            "reason": "Learn about robotic grasping and manipulation"
        })

    if not recommended_chapters:
        recommended_chapters = [
            {"chapter": 1, "title": "Foundations", "reason": "Build a strong foundation"},
            {"chapter": 2, "title": "AI in Physical Systems", "reason": "Learn AI for robotics"}
        ]

    # Learning path
    learning_path = []
    if background.robotics_experience == "none":
        learning_path = [
            "Start with Chapter 1: Foundations",
            "Practice basic exercises",
            "Move to AI and perception",
            "Explore advanced topics"
        ]
    else:
        learning_path = [
            f"Focus on {background.primary_interest}",
            "Complete advanced exercises",
            "Work on real projects"
        ]

    # Skill badge
    skill_badges = {
        "student": "Student Learner",
        "professional": "Professional Engineer",
        "researcher": "Research Scholar",
        "hobbyist": "Robotics Enthusiast"
    }
    skill_level_badge = skill_badges.get(background.skill_level, "Learner")

    # Tips based on experience
    quick_tips = []
    if background.hardware_experience == "none":
        quick_tips.append("Consider getting an Arduino or Raspberry Pi to practice")
    if "Python" in background.programming_languages:
        quick_tips.append("Check out the Python code examples in each chapter")
    if background.time_commitment:
        quick_tips.append(f"With {background.time_commitment}, aim to complete 1-2 sections per week")

    # Suggested exercises
    suggested_exercises = [
        {"id": 1, "title": "Basic Kinematics", "difficulty": background.software_experience},
        {"id": 2, "title": "Computer Vision with OpenCV", "difficulty": background.software_experience}
    ]

    return PersonalizedDashboard(
        welcome_message=welcome_message,
        recommended_chapters=recommended_chapters,
        learning_path=learning_path,
        skill_level_badge=skill_level_badge,
        quick_tips=quick_tips,
        suggested_exercises=suggested_exercises
    )
