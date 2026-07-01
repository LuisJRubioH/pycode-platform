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
from app.core.tracks import TRACK_TITLES
from app.models.user import User
from app.models.capstone import Capstone, CapstoneSubmission
from app.models.code_quality import CodeQualitySnapshot
from app.models.learning import UserProgress, Lesson, CodeSubmission, Exercise
from app.schemas.learning import (
    CodeQualityPoint,
    CodeQualityProgressOut,
    CodeQualitySummary,
    CompetencyLessonItem,
    CompetencyOut,
    ProgressResponse,
    ProgressUpdate,
    TrackStatusItem,
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


@router.get("/track-status", response_model=List[TrackStatusItem])
async def get_track_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Estado agregado por Track para el usuario actual.

    Itera los tracks conocidos (TRACK_TITLES) filtrando lecciones por
    `Lesson.track` y eligiendo el capstone canonico del track por
    `Capstone.track == track` con `order_index` ascendente.

    Devuelve solo los tracks que tengan al menos una leccion activa o un
    capstone activo, para no exponer placeholders vacios de tracks futuros.

    El gate del certificado (`certificate_unlocked`) se computa server-side:
    queda True solo cuando existe una `CapstoneSubmission` del usuario
    actual con `status="passed"` para el capstone del track.
    """
    lessons_all = (
        (await db.execute(select(Lesson).where(Lesson.is_active.is_(True))))
        .scalars()
        .all()
    )
    lessons_by_track: dict[str, list[Lesson]] = {}
    for lesson in lessons_all:
        lessons_by_track.setdefault(lesson.track or "track-1", []).append(lesson)

    cap_rows = (
        (
            await db.execute(
                select(Capstone)
                .where(Capstone.is_active.is_(True))
                .order_by(Capstone.order_index.asc())
            )
        )
        .scalars()
        .all()
    )
    capstones_by_track: dict[str, Capstone] = {}
    for cap in cap_rows:
        # order_index asc + dict.setdefault => primer capstone por track
        capstones_by_track.setdefault(cap.track, cap)

    items: list[TrackStatusItem] = []
    for track_key, track_title_value in TRACK_TITLES.items():
        lessons = lessons_by_track.get(track_key, [])
        capstone = capstones_by_track.get(track_key)
        if not lessons and capstone is None:
            continue  # no exponer tracks vacios (3-6 hoy)

        lesson_ids = [lesson.id for lesson in lessons]
        lessons_total = len(lesson_ids)

        completed_lessons = 0
        if lesson_ids:
            result = await db.execute(
                select(func.count(UserProgress.id)).where(
                    UserProgress.user_id == current_user.id,
                    UserProgress.lesson_id.in_(lesson_ids),
                    UserProgress.status == "completed",
                )
            )
            completed_lessons = result.scalar() or 0

        exercise_ids: list[int] = []
        if lesson_ids:
            ex_rows = (
                await db.execute(
                    select(Exercise.id).where(Exercise.lesson_id.in_(lesson_ids))
                )
            ).all()
            exercise_ids = [row[0] for row in ex_rows]
        exercises_total = len(exercise_ids)

        completed_exercises = 0
        if exercise_ids:
            sub_rows = (
                await db.execute(
                    select(CodeSubmission.exercise_id)
                    .where(
                        CodeSubmission.user_id == current_user.id,
                        CodeSubmission.exercise_id.in_(exercise_ids),
                        CodeSubmission.result == "success",
                    )
                    .distinct()
                )
            ).all()
            completed_exercises = len({row[0] for row in sub_rows})

        capstone_slug = None
        capstone_title = None
        capstone_status = None
        capstone_tests_passed = None
        capstone_tests_total = None
        certificate_unlocked = False

        if capstone is not None:
            capstone_slug = capstone.slug
            capstone_title = capstone.title
            sub_row = await db.execute(
                select(CapstoneSubmission)
                .where(
                    CapstoneSubmission.user_id == current_user.id,
                    CapstoneSubmission.capstone_id == capstone.id,
                )
                .order_by(CapstoneSubmission.created_at.desc())
                .limit(1)
            )
            submission = sub_row.scalar_one_or_none()
            if submission is not None:
                capstone_status = submission.status
                capstone_tests_passed = submission.tests_passed
                capstone_tests_total = submission.tests_total
                certificate_unlocked = submission.status == "passed"

        items.append(
            TrackStatusItem(
                track=track_key,
                title=track_title_value,
                lessons_total=lessons_total,
                lessons_completed=completed_lessons,
                exercises_total=exercises_total,
                exercises_completed=completed_exercises,
                capstone_slug=capstone_slug,
                capstone_title=capstone_title,
                capstone_status=capstone_status,
                capstone_tests_passed=capstone_tests_passed,
                capstone_tests_total=capstone_tests_total,
                certificate_unlocked=certificate_unlocked,
            )
        )

    return items


@router.get("/code-quality", response_model=CodeQualityProgressOut)
async def get_code_quality_progress(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Progresión de calidad de código del usuario.

    Serie temporal de snapshots (logic/general del evaluador LLM + static del
    análisis estático) + medias agregadas. Filtro por user_id; un usuario
    nunca ve datos de otro.
    """
    limit = max(1, min(limit, 200))
    rows = (
        (
            await db.execute(
                select(CodeQualitySnapshot)
                .where(CodeQualitySnapshot.user_id == current_user.id)
                .order_by(CodeQualitySnapshot.created_at)
                .limit(limit)
            )
        )
        .scalars()
        .all()
    )

    def avg(values: list) -> float | None:
        nums = [v for v in values if v is not None]
        return round(sum(nums) / len(nums), 1) if nums else None

    points = [
        CodeQualityPoint(
            created_at=r.created_at,
            logic_score=r.logic_score,
            general_score=r.general_score,
            static_score=r.static_score,
        )
        for r in rows
    ]
    summary = CodeQualitySummary(
        count=len(rows),
        avg_logic=avg([r.logic_score for r in rows]),
        avg_general=avg([r.general_score for r in rows]),
        avg_static=avg([r.static_score for r in rows]),
        latest_static=rows[-1].static_score if rows else None,
    )
    return CodeQualityProgressOut(points=points, summary=summary)


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
