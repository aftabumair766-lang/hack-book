"""
Translation API Router
Handles chapter content translation to different languages.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import openai
from app.models.database import get_db
from app.models.user import User
from app.core.auth import decode_access_token
from app.core.config import settings

router = APIRouter()


class TranslateRequest(BaseModel):
    """Request model for chapter translation."""
    chapter_id: str
    target_language: str = "urdu"  # Default to Urdu


class TranslationResponse(BaseModel):
    """Response model for translated content."""
    translated_content: str
    source_language: str
    target_language: str
    chapter_id: str
    original_length: int
    translated_length: int


def get_current_user(
    token: str,
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from token."""
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


def load_chapter_content(chapter_id: str) -> Optional[str]:
    """Load chapter content from markdown files."""
    from pathlib import Path

    # Try multiple possible locations
    possible_paths = [
        Path(f"../docs/{chapter_id}/index.md"),
        Path(f"../docs/{chapter_id}/index.mdx"),
        Path(f"../../docs/{chapter_id}/index.md"),
        Path(f"../../docs/{chapter_id}/index.mdx"),
        Path(f"docs/{chapter_id}/index.md"),
        Path(f"docs/{chapter_id}/index.mdx"),
    ]

    for path in possible_paths:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Remove frontmatter (YAML between ---)
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        return parts[2].strip()
                return content

    # If not found, return sample content
    return f"""
# {chapter_id.replace('-', ' ').title()}

This chapter covers fundamental concepts in physical AI and humanoid robotics.

## Introduction

Learn about the core principles and practical applications.
"""


def translate_content_with_openai(content: str, target_language: str) -> str:
    """
    Translate content using OpenAI API.

    Args:
        content: Original text in English
        target_language: Target language (e.g., 'urdu', 'arabic', 'spanish')

    Returns:
        Translated text
    """
    # Initialize OpenAI client
    openai.api_key = settings.openai_api_key

    # Language name mapping
    language_names = {
        'urdu': 'Urdu',
        'arabic': 'Arabic',
        'spanish': 'Spanish',
        'french': 'French',
        'german': 'German',
        'hindi': 'Hindi',
        'chinese': 'Chinese (Simplified)',
    }

    target_lang_name = language_names.get(target_language.lower(), target_language.title())

    # Create translation prompt
    prompt = f"""Translate the following educational content from English to {target_lang_name}.

IMPORTANT INSTRUCTIONS:
1. Maintain all markdown formatting (headers, lists, code blocks, etc.)
2. Keep code blocks in English (do not translate code)
3. Keep mathematical equations unchanged
4. Preserve links and image references
5. Maintain the technical accuracy
6. Use appropriate technical terminology in {target_lang_name}
7. Keep the structure and formatting identical

CONTENT TO TRANSLATE:

{content}

TRANSLATED CONTENT IN {target_lang_name.upper()}:"""

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional translator specializing in technical and educational content. Translate accurately while preserving formatting and technical terms."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent translation
            max_tokens=4000
        )

        translated_text = response.choices[0].message.content.strip()
        return translated_text

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )


@router.post("/api/translate/chapter", response_model=TranslationResponse)
async def translate_chapter(
    request: TranslateRequest,
    authorization: str,
    db: Session = Depends(get_db)
):
    """
    Translate chapter content to specified language.

    **Supported Languages:**
    - urdu (اردو)
    - arabic (العربية)
    - spanish (Español)
    - french (Français)
    - german (Deutsch)
    - hindi (हिन्दी)
    - chinese (中文)

    **Flow:**
    1. Validate user authentication
    2. Load original chapter content
    3. Translate using OpenAI API
    4. Return translated content with metadata

    Args:
        request: Contains chapter_id and target_language
        authorization: JWT token from Authorization header
        db: Database session

    Returns:
        TranslationResponse with translated content

    Raises:
        HTTPException: If user not found, not authenticated, or translation fails
    """
    # Get authenticated user
    user = get_current_user(authorization, db)

    # Load chapter content
    chapter_content = load_chapter_content(request.chapter_id)
    if not chapter_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter '{request.chapter_id}' not found"
        )

    # Translate content
    translated_content = translate_content_with_openai(
        content=chapter_content,
        target_language=request.target_language
    )

    # Return response
    return TranslationResponse(
        translated_content=translated_content,
        source_language="english",
        target_language=request.target_language,
        chapter_id=request.chapter_id,
        original_length=len(chapter_content),
        translated_length=len(translated_content)
    )


@router.get("/api/translate/languages")
async def get_supported_languages():
    """
    Get list of supported translation languages.

    Returns:
        List of supported languages with codes and native names
    """
    return {
        "supported_languages": [
            {"code": "urdu", "name": "Urdu", "native": "اردو"},
            {"code": "arabic", "name": "Arabic", "native": "العربية"},
            {"code": "spanish", "name": "Spanish", "native": "Español"},
            {"code": "french", "name": "French", "native": "Français"},
            {"code": "german", "name": "German", "native": "Deutsch"},
            {"code": "hindi", "name": "Hindi", "native": "हिन्दी"},
            {"code": "chinese", "name": "Chinese", "native": "中文"},
        ]
    }
