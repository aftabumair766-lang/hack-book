"""
Pydantic schemas for authentication and user management.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# Authentication Schemas
class UserSignup(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    full_name: Optional[str] = None
    username: Optional[str] = None


class UserSignin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None


# User Response Schemas
class UserResponse(BaseModel):
    id: int
    email: str
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    has_completed_questionnaire: bool = False

    class Config:
        from_attributes = True


# Background Questionnaire Schemas
class BackgroundQuestionnaireSubmit(BaseModel):
    # Development experience
    software_experience: str = Field(..., description="beginner, intermediate, advanced, expert")
    years_coding: Optional[int] = Field(None, ge=0, le=50)

    # Hardware/Robotics
    hardware_experience: str = Field(..., description="none, hobby, professional, expert")
    robotics_experience: str = Field(..., description="none, beginner, intermediate, advanced")

    # Programming
    programming_languages: List[str] = Field(..., min_length=1)
    preferred_language: str

    # Learning goals
    learning_goals: List[str] = Field(..., min_length=1)
    primary_interest: str

    # Current status
    skill_level: str = Field(..., description="student, professional, researcher, hobbyist")
    education_level: str

    # Additional
    industry: Optional[str] = None
    project_goals: Optional[str] = None
    time_commitment: Optional[str] = None


class BackgroundQuestionnaireResponse(BaseModel):
    id: int
    user_id: int
    software_experience: str
    years_coding: Optional[int]
    hardware_experience: str
    robotics_experience: str
    programming_languages: List[str]
    preferred_language: str
    learning_goals: List[str]
    primary_interest: str
    skill_level: str
    education_level: str
    industry: Optional[str]
    project_goals: Optional[str]
    time_commitment: Optional[str]
    completed_at: datetime

    class Config:
        from_attributes = True


# Personalization Schema
class PersonalizedDashboard(BaseModel):
    welcome_message: str
    recommended_chapters: List[dict]
    learning_path: List[str]
    skill_level_badge: str
    quick_tips: List[str]
    suggested_exercises: List[dict]
