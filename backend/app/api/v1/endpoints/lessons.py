"""
Lessons endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.learning import Lesson, UserProgress
from app.schemas.learning import (
    ExerciseResponse,
    LessonResponse,
    LessonListResponse,
)
from app.services.progress_service import (
    completed_exercise_ids,
    recompute_lesson_progress,
)

router = APIRouter()


# Se sirve en ambas rutas (sin y con slash final): el rewrite de Vercel
# (`/api/:path*`) NO proxea rutas con slash final y caían al fallback SPA
# (devolvía index.html en vez del JSON). El frontend llama la versión sin
# slash; la variante con slash se mantiene para compatibilidad/tests.
@router.get("", response_model=List[LessonListResponse])
@router.get("/", response_model=List[LessonListResponse], include_in_schema=False)
async def list_lessons(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    track: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all lessons with optional filtering."""
    query = select(Lesson).where(Lesson.is_active).order_by(Lesson.order)

    if category:
        query = query.where(Lesson.category == category)
    if difficulty:
        query = query.where(Lesson.difficulty == difficulty)
    if track:
        query = query.where(Lesson.track == track)

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
                "track": lesson.track,
                "estimated_duration": lesson.estimated_duration,
                # Orden curricular explícito: el cliente no debe asumir que
                # el orden de la respuesta es el del temario.
                "order": lesson.order or 0,
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

    # Recalcula (y crea si falta) el progreso con la regla única de
    # progress_service: % = ejercicios_hechos / totales, en vez del 5% fijo
    # que quedaba clavado. Abrir la lección la marca "in_progress".
    progress = await recompute_lesson_progress(db, current_user.id, lesson_id)
    await db.commit()

    sorted_exercises = sorted(lesson.exercises, key=lambda exercise: exercise.order)

    # Qué ejercicios tiene ya aprobados el usuario, con la regla única de
    # progress_service. La UI la usa para el badge "Hecho" de cada tarjeta y
    # para marcar el ejercicio activo del editor.
    completed_ids = await completed_exercise_ids(
        db, current_user.id, [exercise.id for exercise in sorted_exercises]
    )

    # El payload sale del propio schema, no de un dict campo por campo: así
    # un campo nuevo en ExerciseResponse no se pierde en silencio aquí.
    exercises_payload = [
        ExerciseResponse.model_validate(exercise).model_copy(
            update={"completed": exercise.id in completed_ids}
        )
        for exercise in sorted_exercises
    ]

    return {
        "id": lesson.id,
        "title": lesson.title,
        "description": lesson.description,
        "content": lesson.content,
        "difficulty": lesson.difficulty,
        "category": lesson.category,
        "track": lesson.track,
        "estimated_duration": lesson.estimated_duration,
        "prerequisites": lesson.prerequisites or [],
        "exercises": exercises_payload,
        "progress": progress.progress or 0,
        "status": progress.status,
    }
