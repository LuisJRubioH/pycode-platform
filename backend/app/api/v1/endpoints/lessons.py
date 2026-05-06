"""
Lessons endpoints.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.learning import Lesson, UserProgress
from app.schemas.learning import LessonResponse, LessonListResponse

router = APIRouter()


@router.get("/", response_model=List[LessonListResponse])
async def list_lessons(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all lessons with optional filtering."""
    query = select(Lesson).where(Lesson.is_active).order_by(Lesson.order)

    if category:
        query = query.where(Lesson.category == category)
    if difficulty:
        query = query.where(Lesson.difficulty == difficulty)

    result = await db.execute(query)
    lessons = result.scalars().all()

    # Get user progress for each lesson
    lesson_ids = [lesson.id for lesson in lessons]
    progress_query = select(UserProgress).where(
        UserProgress.user_id == current_user.id, UserProgress.lesson_id.in_(lesson_ids)
    )
    progress_result = await db.execute(progress_query)
    progress_map = {p.lesson_id: p for p in progress_result.scalars().all()}

    response_lessons = []
    for lesson in lessons:
        progress = progress_map.get(lesson.id)
        progress_value = (
            progress.progress if progress and progress.progress is not None else 0
        )
        response_lessons.append(
            {
                "id": lesson.id,
                "title": lesson.title,
                "description": lesson.description,
                "difficulty": lesson.difficulty,
                "category": lesson.category,
                "estimated_duration": lesson.estimated_duration,
                "progress": progress_value,
                "status": progress.status if progress else "not_started",
            }
        )

    return response_lessons


@router.get("/categories", response_model=List[str])
async def list_categories(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all lesson categories."""
    result = await db.execute(
        select(Lesson.category).where(Lesson.is_active).distinct()
    )
    categories = [cat for cat in result.scalars().all() if cat]
    return categories


@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific lesson by ID."""
    result = await db.execute(
        select(Lesson)
        .options(selectinload(Lesson.exercises))
        .where(Lesson.id == lesson_id, Lesson.is_active)
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found"
        )

    # Get or create user progress
    progress_result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == current_user.id, UserProgress.lesson_id == lesson_id
        )
    )
    progress = progress_result.scalar_one_or_none()

    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            status="in_progress",
            progress=5,
            started_at=datetime.utcnow(),
        )
        db.add(progress)
        await db.commit()
        await db.refresh(progress)

    sorted_exercises = sorted(lesson.exercises, key=lambda exercise: exercise.order)

    return {
        "id": lesson.id,
        "title": lesson.title,
        "description": lesson.description,
        "content": lesson.content,
        "difficulty": lesson.difficulty,
        "category": lesson.category,
        "estimated_duration": lesson.estimated_duration,
        "prerequisites": lesson.prerequisites or [],
        "exercises": sorted_exercises,
        "progress": progress.progress or 0,
        "status": progress.status,
    }
