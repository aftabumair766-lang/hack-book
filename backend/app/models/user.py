"""
User authentication and profile models.
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User account model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)


class UserBackground(Base):
    """User background questionnaire responses."""
    __tablename__ = "user_backgrounds"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, unique=True, index=True)

    # Development experience
    software_experience = Column(String(50), nullable=True)  # beginner, intermediate, advanced, expert
    years_coding = Column(Integer, nullable=True)

    # Hardware/Robotics background
    hardware_experience = Column(String(50), nullable=True)  # none, hobby, professional, expert
    robotics_experience = Column(String(50), nullable=True)  # none, beginner, intermediate, advanced

    # Programming languages
    programming_languages = Column(JSON, nullable=True)  # List of languages
    preferred_language = Column(String(50), nullable=True)

    # Learning goals
    learning_goals = Column(JSON, nullable=True)  # List of goals
    primary_interest = Column(String(100), nullable=True)  # perception, control, manipulation, etc.

    # Current skill level
    skill_level = Column(String(50), nullable=True)  # student, professional, researcher, hobbyist
    education_level = Column(String(100), nullable=True)

    # Additional info
    industry = Column(String(100), nullable=True)
    project_goals = Column(Text, nullable=True)
    time_commitment = Column(String(50), nullable=True)  # hours per week

    # Metadata
    completed_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
