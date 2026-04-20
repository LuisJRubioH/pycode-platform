"""
Router FastAPI — Sistema ELO
Endpoints para intentos de puzzles, perfil ELO e historial
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime

from app.models.elo_models import UserProfile, Puzzle, PuzzleAttempt, EloHistory
from app.schemas.elo_schemas import (
    PuzzleOut, PuzzleAttemptIn, PuzzleAttemptOut,
    EloProfileOut, EloHistoryOut, EloHistoryPoint,
    EloRankTableOut, EloTableRow,
)
from app.services.elo_service import (
    process_attempt, get_rank, get_rank_color,
    win_probability_label, expected_score,
)
from app.core.deps import get_db, get_current_user   # tus dependencias existentes

router = APIRouter(prefix="/elo", tags=["ELO System"])


# ─── Intentar un puzzle ───────────────────────────────────────────────────────

@router.post("/attempt", response_model=PuzzleAttemptOut)
async def submit_puzzle_attempt(
    payload: PuzzleAttemptIn,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    El usuario envía su respuesta a un puzzle.
    El sistema calcula el nuevo ELO y actualiza ambos ratings.
    """
    # 1. Cargar puzzle
    puzzle = await db.get(Puzzle, payload.puzzle_id)
    if not puzzle or not puzzle.is_active:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    # 2. Cargar perfil del usuario (crea uno si no existe)
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()
    if not profile:
        profile = UserProfile(user_id=current_user.id, elo_rating=1000)
        db.add(profile)
        await db.flush()

    # 3. Evaluar si es correcto (comparación exacta de output)
    user_answer = payload.user_answer.strip()
    correct_output = puzzle.correct_output.strip()
    is_correct = user_answer == correct_output

    # 4. Procesar ELO
    result = process_attempt(
        user_elo=profile.elo_rating,
        puzzle_elo=puzzle.elo_rating,
        correct=is_correct,
        advanced=puzzle.is_advanced,
    )

    # 5. Actualizar perfil del usuario
    rank_before = result.rank_before.value
    profile.elo_rating = result.user_elo_after
    profile.elo_peak = max(profile.elo_peak, result.user_elo_after)
    profile.rank = result.rank_after.value
    profile.puzzles_attempted += 1
    profile.last_activity = datetime.utcnow()
    if is_correct:
        profile.puzzles_correct += 1
        profile.streak_current += 1
        profile.streak_best = max(profile.streak_best, profile.streak_current)
    else:
        profile.streak_current = 0

    # 6. Actualizar ELO del puzzle
    puzzle.elo_rating = result.puzzle_elo_after
    puzzle.times_attempted += 1
    if is_correct:
        puzzle.times_correct += 1

    # 7. Registrar intento
    attempt = PuzzleAttempt(
        user_id=current_user.id,
        puzzle_id=puzzle.id,
        correct=is_correct,
        user_answer=user_answer,
        user_elo_before=result.user_elo_before,
        user_elo_after=result.user_elo_after,
        puzzle_elo_before=result.puzzle_elo_before,
        puzzle_elo_after=result.puzzle_elo_after,
        elo_delta_user=result.delta_user,
        elo_delta_puzzle=result.delta_puzzle,
        expected_probability=result.expected_probability,
        time_spent_seconds=payload.time_spent_seconds,
    )
    db.add(attempt)
    await db.flush()

    # 8. Registrar punto de historial ELO
    history_point = EloHistory(
        user_profile_id=profile.id,
        puzzle_id=puzzle.id,
        attempt_id=attempt.id,
        elo_value=result.user_elo_after,
        delta=result.delta_user,
        correct=is_correct,
        rank_label=result.rank_after.value,
        puzzle_title=puzzle.title,
        category=puzzle.category,
    )
    db.add(history_point)
    await db.commit()

    return PuzzleAttemptOut(
        correct=is_correct,
        correct_output=puzzle.correct_output,
        explanation=puzzle.explanation,
        user_elo_before=result.user_elo_before,
        user_elo_after=result.user_elo_after,
        elo_delta_user=result.delta_user,
        puzzle_elo_before=result.puzzle_elo_before,
        puzzle_elo_after=result.puzzle_elo_after,
        rank_before=rank_before,
        rank_after=result.rank_after.value,
        rank_changed=result.rank_changed,
        rank_color=get_rank_color(result.rank_after),
        expected_probability=result.expected_probability,
        win_probability_label=win_probability_label(result.expected_probability),
    )


# ─── Perfil ELO del usuario ───────────────────────────────────────────────────

@router.get("/profile", response_model=EloProfileOut)
async def get_elo_profile(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Devuelve el perfil ELO completo del usuario autenticado."""
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        # Usuario nuevo — devolver perfil vacío con ELO inicial
        return EloProfileOut(
            elo_rating=1000,
            elo_peak=1000,
            rank="Beginner",
            rank_color=get_rank_color(get_rank(1000)),
            puzzles_attempted=0,
            puzzles_correct=0,
            accuracy=0.0,
            streak_current=0,
            streak_best=0,
        )

    rank = get_rank(profile.elo_rating)
    return EloProfileOut(
        elo_rating=profile.elo_rating,
        elo_peak=profile.elo_peak,
        rank=profile.rank,
        rank_color=get_rank_color(rank),
        puzzles_attempted=profile.puzzles_attempted,
        puzzles_correct=profile.puzzles_correct,
        accuracy=profile.accuracy,
        streak_current=profile.streak_current,
        streak_best=profile.streak_best,
    )


# ─── Historial ELO (serie temporal) ──────────────────────────────────────────

@router.get("/history", response_model=EloHistoryOut)
async def get_elo_history(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Devuelve la serie temporal del ELO del usuario.
    Usada para renderizar la gráfica de progreso en el dashboard.
    """
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()
    if not profile:
        return EloHistoryOut(history=[], total_points=0)

    history_result = await db.execute(
        select(EloHistory)
        .where(EloHistory.user_profile_id == profile.id)
        .order_by(EloHistory.created_at)
        .limit(limit)
    )
    points = history_result.scalars().all()

    return EloHistoryOut(
        history=[EloHistoryPoint.model_validate(p) for p in points],
        total_points=len(points),
    )


# ─── Tabla de rankings ────────────────────────────────────────────────────────

@router.get("/rank-table", response_model=EloRankTableOut)
async def get_rank_table(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Devuelve la tabla de rangos ELO con el rango actual del usuario marcado.
    Idéntica a la Tabla 3.1 de Coffee Break Python.
    """
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()
    user_elo = profile.elo_rating if profile else 1000

    ranks_table = [
        (2500, None,  "World Class"),
        (2400, 2500,  "Grandmaster"),
        (2300, 2400,  "International Master"),
        (2200, 2300,  "Master"),
        (2100, 2200,  "National Master"),
        (2000, 2100,  "Master Candidate"),
        (1900, 2000,  "Authority"),
        (1800, 1900,  "Professional"),
        (1700, 1800,  "Expert"),
        (1600, 1700,  "Experienced Intermediate"),
        (1500, 1600,  "Intermediate"),
        (1400, 1500,  "Experienced Learner"),
        (1300, 1400,  "Learner"),
        (1200, 1300,  "Scholar"),
        (1100, 1200,  "Autodidact"),
        (1000, 1100,  "Beginner"),
        (0,    1000,  "Basic Knowledge"),
    ]

    from app.services.elo_service import EloRank
    rows = []
    for elo_min, elo_max, rank_name in ranks_table:
        rank_enum = get_rank(elo_min)
        color = get_rank_color(rank_enum)
        is_current = (
            user_elo >= elo_min and
            (elo_max is None or user_elo < elo_max)
        )
        rows.append(EloTableRow(
            elo_min=elo_min,
            elo_max=elo_max,
            rank=rank_name,
            color=color,
            is_current=is_current,
        ))

    current_rank = get_rank(user_elo)
    return EloRankTableOut(
        rows=rows,
        user_elo=user_elo,
        user_rank=current_rank.value,
    )


# ─── Puzzle recomendado ───────────────────────────────────────────────────────

@router.get("/next-puzzle", response_model=PuzzleOut)
async def get_next_puzzle(
    category: str = "python",
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Recomienda el siguiente puzzle óptimo para el usuario.
    Estrategia: puzzle cuyo ELO esté ~100-200 puntos por encima del usuario
    (probabilidad de éxito ~40-50% — zona de máximo aprendizaje).
    """
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()
    user_elo = profile.elo_rating if profile else 1000

    # Zona óptima: puzzle entre user_elo - 200 y user_elo + 300
    target_min = max(0, user_elo - 200)
    target_max = user_elo + 300

    from sqlalchemy import and_, func
    result = await db.execute(
        select(Puzzle)
        .where(
            and_(
                Puzzle.category == category,
                Puzzle.is_active == True,
                Puzzle.elo_rating >= target_min,
                Puzzle.elo_rating <= target_max,
            )
        )
        .order_by(func.random())
        .limit(1)
    )
    puzzle = result.scalar_one_or_none()

    if not puzzle:
        # Fallback: cualquier puzzle de la categoría
        result = await db.execute(
            select(Puzzle)
            .where(and_(Puzzle.category == category, Puzzle.is_active == True))
            .order_by(func.random())
            .limit(1)
        )
        puzzle = result.scalar_one_or_none()

    if not puzzle:
        raise HTTPException(status_code=404, detail="No puzzles available")

    return PuzzleOut.model_validate(puzzle)
