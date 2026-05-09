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
from app.schemas.learning import (
    CompetencyLessonItem,
    CompetencyOut,
    ProgressResponse,
    ProgressUpdate,
)

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


@router.get("/competencies", response_model=List[CompetencyOut])
async def get_competencies(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Mapa de competencias del Track 1 (Python).

    Agrupa todas las lecciones activas por `category` y, para el usuario
    actual, calcula:
    - lecciones completadas (UserProgress.status == "completed").
    - ejercicios completados (CodeSubmission.result == "success",
      deduplicado por exercise_id; un ejercicio cuenta una sola vez aun
      si el alumno tiene N submissions exitosas).

    Filtro por user_id en queries de progreso/submissions; un usuario
    nunca ve datos de otro.
    """
    lessons_q = select(Lesson).where(Lesson.is_active).order_by(Lesson.order)
    lessons = (await db.execute(lessons_q)).scalars().all()

    progress_rows = (
        (
            await db.execute(
                select(UserProgress).where(UserProgress.user_id == current_user.id)
            )
        )
        .scalars()
        .all()
    )
    progress_map = {p.lesson_id: p for p in progress_rows}

    ex_rows = (
        await db.execute(
            select(Exercise.lesson_id, Exercise.id).order_by(Exercise.lesson_id)
        )
    ).all()
    lesson_ex_ids: dict[int, list[int]] = {}
    for lesson_id, ex_id in ex_rows:
        lesson_ex_ids.setdefault(lesson_id, []).append(ex_id)

    sub_rows = (
        await db.execute(
            select(CodeSubmission.exercise_id)
            .where(
                CodeSubmission.user_id == current_user.id,
                CodeSubmission.result == "success",
            )
            .distinct()
        )
    ).all()
    successful_ex_ids = {row[0] for row in sub_rows}

    by_category: dict[str, dict] = {}
    for lesson in lessons:
        category = lesson.category or "otros"
        bucket = by_category.setdefault(
            category,
            {
                "category": category,
                "lessons_total": 0,
                "lessons_completed": 0,
                "exercises_total": 0,
                "exercises_completed": 0,
                "lessons": [],
            },
        )
        bucket["lessons_total"] += 1
        prog = progress_map.get(lesson.id)
        is_done = bool(prog and prog.status == "completed")
        if is_done:
            bucket["lessons_completed"] += 1
        ex_ids = lesson_ex_ids.get(lesson.id, [])
        bucket["exercises_total"] += len(ex_ids)
        completed_in_lesson = sum(1 for eid in ex_ids if eid in successful_ex_ids)
        bucket["exercises_completed"] += completed_in_lesson
        bucket["lessons"].append(
            CompetencyLessonItem(
                id=lesson.id,
                title=lesson.title,
                difficulty=lesson.difficulty,
                completed=is_done,
                exercises_completed=completed_in_lesson,
                exercises_total=len(ex_ids),
            )
        )

    return [CompetencyOut(**bucket) for bucket in by_category.values()]


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
