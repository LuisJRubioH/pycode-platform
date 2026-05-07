"""
Exercises endpoints.
"""

from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.learning import Exercise, CodeSubmission, UserProgress
from app.schemas.learning import CodeSubmissionCreate, CodeSubmissionResponse

router = APIRouter()


@router.get("/lesson/{lesson_id}", response_model=List[dict])
async def get_lesson_exercises(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all exercises for a lesson."""
    result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson_id).order_by(Exercise.order)
    )
    exercises = result.scalars().all()

    # Get submissions for these exercises
    exercise_ids = [ex.id for ex in exercises]
    submissions_result = await db.execute(
        select(CodeSubmission)
        .where(
            CodeSubmission.user_id == current_user.id,
            CodeSubmission.exercise_id.in_(exercise_ids),
        )
        .order_by(CodeSubmission.created_at.desc())
    )
    submissions = submissions_result.scalars().all()

    # Create submission map (exercise_id -> latest submission)
    submission_map = {}
    for sub in submissions:
        if sub.exercise_id not in submission_map:
            submission_map[sub.exercise_id] = sub

    return [
        {
            "id": ex.id,
            "title": ex.title,
            "description": ex.description,
            "difficulty": ex.difficulty,
            "points": ex.points,
            "starter_code": ex.starter_code,
            "hints": ex.hints[:1] if ex.hints else [],
            "completed": getattr(submission_map.get(ex.id), "result", None)
            == "success",
            "attempts": len([s for s in submissions if s.exercise_id == ex.id]),
        }
        for ex in exercises
    ]


@router.post("/{exercise_id}/submit", response_model=CodeSubmissionResponse)
async def submit_exercise(
    exercise_id: int,
    submission: CodeSubmissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Persiste el resultado que el cliente Pyodide reporta para un ejercicio.

    El backend ya no ejecuta código del estudiante (ver Task 14 del plan
    Fase 0). El cliente corre el código en Pyodide y envía success / output
    / passed_tests; aquí solo registramos la submission y actualizamos
    progreso.
    """
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    total_tests = submission.total_tests or (
        len(exercise.test_cases) if exercise.test_cases else 0
    )
    passed_tests = submission.passed_tests
    is_success = submission.success and (
        total_tests == 0 or passed_tests == total_tests
    )

    code_submission = CodeSubmission(
        user_id=current_user.id,
        exercise_id=exercise_id,
        code=submission.code,
        result="success" if is_success else "error",
        output=submission.output,
        error_message=submission.error_message,
        execution_time=submission.execution_time_ms or 0,
        passed_tests=passed_tests,
        total_tests=total_tests,
    )

    db.add(code_submission)

    if code_submission.result == "success":
        progress_result = await db.execute(
            select(UserProgress).where(
                UserProgress.user_id == current_user.id,
                UserProgress.lesson_id == exercise.lesson_id,
            )
        )
        progress = progress_result.scalar_one_or_none()

        if progress:
            progress.score += exercise.points
            progress.attempts += 1
            progress.last_accessed = datetime.utcnow()

    await db.commit()
    await db.refresh(code_submission)

    return code_submission


@router.get("/{exercise_id}/hints")
async def get_hints(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all hints for an exercise."""
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    return {"hints": exercise.hints or []}
