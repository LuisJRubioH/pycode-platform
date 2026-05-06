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
from app.services.docker_executor import DockerCodeExecutor

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
            "hints": ex.hints[:1] if ex.hints else [],  # Only show first hint
            "completed": submission_map.get(ex.id, {}).result == "success",
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
    """Submit code for an exercise."""
    # Get exercise
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    # Execute code
    executor = DockerCodeExecutor(user_id=str(current_user.id), timeout=30)
    exec_result = await executor.run_python_code(submission.code)

    # Run tests if available
    passed_tests = 0
    total_tests = len(exercise.test_cases) if exercise.test_cases else 0

    if exercise.test_cases and exec_result["success"]:
        # Simple test execution
        for test in exercise.test_cases:
            test_code = f"{submission.code}\n\n{test.get('test_code', '')}"
            test_result = await executor.run_python_code(test_code)
            if test_result["success"] and test_result["exit_code"] == 0:
                passed_tests += 1

    # Create submission record
    code_submission = CodeSubmission(
        user_id=current_user.id,
        exercise_id=exercise_id,
        code=submission.code,
        result="success"
        if exec_result["success"] and passed_tests == total_tests
        else "error",
        output=exec_result.get("stdout"),
        error_message=exec_result.get("stderr"),
        execution_time=exec_result.get("execution_time", 0),
        passed_tests=passed_tests,
        total_tests=total_tests,
    )

    db.add(code_submission)

    # Update progress if successful
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
