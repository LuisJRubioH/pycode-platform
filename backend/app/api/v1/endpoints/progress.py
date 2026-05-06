"""
User progress endpoints.
"""

from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.learning import UserProgress, Lesson, CodeSubmission, Exercise
from app.schemas.learning import ProgressResponse, ProgressUpdate

router = APIRouter()


@router.get("/", response_model=List[ProgressResponse])
async def get_user_progress(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all progress for current user."""
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == current_user.id)
    )
    return result.scalars().all()


@router.get("/stats")
async def get_progress_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get user progress statistics."""
    # Get counts
    progress_result = await db.execute(
        select(
            func.count(UserProgress.id).label("total_lessons"),
            func.sum(UserProgress.score).label("total_score"),
        ).where(UserProgress.user_id == current_user.id)
    )
    stats = progress_result.one()

    completed_result = await db.execute(
        select(func.count(UserProgress.id)).where(
            UserProgress.user_id == current_user.id, UserProgress.status == "completed"
        )
    )
    completed_lessons = completed_result.scalar()

    # Get submissions count
    submissions_result = await db.execute(
        select(func.count(CodeSubmission.id)).where(
            CodeSubmission.user_id == current_user.id
        )
    )
    submissions_count = submissions_result.scalar()

    # Get streak (simplified - days with activity)
    # For now, return placeholder
    streak_days = 0

    return {
        "total_lessons": stats.total_lessons or 0,
        "completed_lessons": completed_lessons or 0,
        "total_score": stats.total_score or 0,
        "total_submissions": submissions_count or 0,
        "streak_days": streak_days,
        "level": "beginner",
        "xp_points": (stats.total_score or 0) * 10,
    }


@router.post("/update")
async def update_progress(
    update: ProgressUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update progress for a lesson."""
    result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == current_user.id,
            UserProgress.lesson_id == update.lesson_id,
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        # Create new progress
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=update.lesson_id,
            status=update.status,
            progress=update.progress,
            started_at=datetime.utcnow() if update.status == "in_progress" else None,
            completed_at=datetime.utcnow() if update.status == "completed" else None,
            time_spent=update.time_spent,
        )
        db.add(progress)
    else:
        # Update existing
        progress.status = update.status
        progress.progress = update.progress
        progress.time_spent += update.time_spent
        progress.last_accessed = datetime.utcnow()

        if update.status == "completed" and not progress.completed_at:
            progress.completed_at = datetime.utcnow()

    await db.commit()
    await db.refresh(progress)

    return progress


@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get recent user activity."""
    # Get recent submissions with lesson info
    result = await db.execute(
        select(CodeSubmission, Exercise, Lesson)
        .join(Exercise, CodeSubmission.exercise_id == Exercise.id)
        .join(Lesson, Exercise.lesson_id == Lesson.id)
        .where(CodeSubmission.user_id == current_user.id)
        .order_by(CodeSubmission.created_at.desc())
        .limit(limit)
    )

    activities = []
    for submission, exercise, lesson in result.all():
        activities.append(
            {
                "type": "exercise",
                "title": exercise.title,
                "lesson_title": lesson.title,
                "result": submission.result,
                "created_at": submission.created_at,
            }
        )

    return activities
