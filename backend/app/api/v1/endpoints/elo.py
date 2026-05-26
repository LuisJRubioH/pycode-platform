"""
FastAPI endpoints for the ELO puzzle system.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.elo_models import EloHistory, Puzzle, PuzzleAttempt
from app.models.user import User, UserProfile
from app.services.elo_rating_service import (
    DOMAIN_PUZZLE,
    apply_result_to_rating,
    get_or_init_rating,
)
from app.schemas.elo_schemas import (
    EloHistoryOut,
    EloHistoryPoint,
    EloProfileOut,
    EloRankTableOut,
    EloTableRow,
    PuzzleListOut,
    PuzzleAttemptHistoryItem,
    PuzzleAttemptHistoryOut,
    PuzzleAttemptIn,
    PuzzleAttemptOut,
    PuzzleOfTheDayOut,
    PuzzleOut,
)
from app.services.elo_service import (
    get_rank,
    get_rank_color,
    process_attempt,
    win_probability_label,
)
from app.services.puzzle_seed import seed_interview_puzzles

router = APIRouter()


async def _get_or_create_profile(db: AsyncSession, user_id: int) -> UserProfile:
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if profile:
        return profile

    profile = UserProfile(user_id=user_id)
    db.add(profile)
    await db.flush()
    return profile


@router.get("/profile", response_model=EloProfileOut)
async def get_elo_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    profile = await _get_or_create_profile(db, current_user.id)
    await db.commit()
    return EloProfileOut(
        elo_rating=profile.elo_rating,
        elo_peak=profile.elo_peak,
        rank=profile.rank,
        rank_color=get_rank_color(get_rank(profile.elo_rating)),
        puzzles_attempted=profile.puzzles_attempted,
        puzzles_correct=profile.puzzles_correct,
        accuracy=profile.accuracy,
        streak_current=profile.streak_current,
        streak_best=profile.streak_best,
    )


@router.get("/history", response_model=EloHistoryOut)
async def get_elo_history(
    limit: int = 50,
    domain: str | None = None,
    scope: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Timeline ELO del usuario. Opcionalmente filtra por track (`domain` +
    `scope`) para graficar la progresión de una categoría concreta. Sin
    filtros devuelve todos los puntos (compatibilidad con la UI anterior)."""
    profile = await _get_or_create_profile(db, current_user.id)
    query = select(EloHistory).where(EloHistory.user_profile_id == profile.id)
    if domain is not None:
        query = query.where(EloHistory.domain == domain)
    if scope is not None:
        query = query.where(EloHistory.category == scope)
    result = await db.execute(query.order_by(EloHistory.created_at).limit(limit))
    history = result.scalars().all()
    await db.commit()
    return EloHistoryOut(
        history=[EloHistoryPoint.model_validate(point) for point in history],
        total_points=len(history),
    )


@router.get("/rank-table", response_model=EloRankTableOut)
async def get_rank_table(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    profile = await _get_or_create_profile(db, current_user.id)
    user_elo = profile.elo_rating
    await db.commit()

    rows_source = [
        (2500, None, "World Class"),
        (2400, 2500, "Grandmaster"),
        (2300, 2400, "International Master"),
        (2200, 2300, "Master"),
        (2100, 2200, "National Master"),
        (2000, 2100, "Master Candidate"),
        (1900, 2000, "Authority"),
        (1800, 1900, "Professional"),
        (1700, 1800, "Expert"),
        (1600, 1700, "Experienced Intermediate"),
        (1500, 1600, "Intermediate"),
        (1400, 1500, "Experienced Learner"),
        (1300, 1400, "Learner"),
        (1200, 1300, "Scholar"),
        (1100, 1200, "Autodidact"),
        (1000, 1100, "Beginner"),
        (0, 1000, "Basic Knowledge"),
    ]

    rows = []
    for elo_min, elo_max, rank_name in rows_source:
        current_rank = get_rank(elo_min)
        rows.append(
            EloTableRow(
                elo_min=elo_min,
                elo_max=elo_max,
                rank=rank_name,
                color=get_rank_color(current_rank),
                is_current=user_elo >= elo_min
                and (elo_max is None or user_elo < elo_max),
            )
        )

    return EloRankTableOut(
        rows=rows, user_elo=user_elo, user_rank=get_rank(user_elo).value
    )


@router.get("/puzzle-of-the-day", response_model=PuzzleOfTheDayOut)
async def get_puzzle_of_the_day(db: AsyncSession = Depends(get_db)):
    """Puzzle del día PÚBLICO (sin auth).

    Selección determinista por fecha UTC sobre los puzzles activos no
    avanzados: cambia cada día y es estable durante todo el día. Sirve de
    gancho en la landing — cualquiera lo ve, pero para resolverlo y ganar
    ELO hay que registrarse.

    Guard rail: la respuesta NUNCA incluye `correct_output`/`explanation`.
    """
    result = await db.execute(
        select(Puzzle)
        .where(Puzzle.is_active.is_(True), Puzzle.is_advanced.is_(False))
        .order_by(Puzzle.id.asc())
    )
    puzzles = result.scalars().all()
    if not puzzles:
        raise HTTPException(status_code=404, detail="No puzzles available")

    today = datetime.utcnow().date()
    puzzle = puzzles[today.toordinal() % len(puzzles)]
    return PuzzleOfTheDayOut(
        id=puzzle.id,
        date=today,
        title=puzzle.title,
        category=puzzle.category,
        topic=puzzle.topic,
        code_snippet=puzzle.code_snippet,
        difficulty_label=puzzle.difficulty_label,
        elo_rating=puzzle.elo_rating,
        solve_rate=puzzle.solve_rate,
    )


@router.get("/next-puzzle", response_model=PuzzleOut)
async def get_next_puzzle(
    category: str = "python",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    profile = await _get_or_create_profile(db, current_user.id)
    user_elo = profile.elo_rating

    target_min = max(0, user_elo - 200)
    target_max = user_elo + 300

    result = await db.execute(
        select(Puzzle)
        .where(
            and_(
                Puzzle.category == category,
                Puzzle.is_active.is_(True),
                Puzzle.elo_rating >= target_min,
                Puzzle.elo_rating <= target_max,
            )
        )
        .order_by(func.random())
        .limit(1)
    )
    puzzle = result.scalar_one_or_none()

    if not puzzle:
        fallback_result = await db.execute(
            select(Puzzle)
            .where(and_(Puzzle.category == category, Puzzle.is_active.is_(True)))
            .order_by(func.random())
            .limit(1)
        )
        puzzle = fallback_result.scalar_one_or_none()

    await db.commit()

    if not puzzle:
        raise HTTPException(status_code=404, detail="No puzzles available")

    return PuzzleOut.model_validate(puzzle)


@router.get("/puzzles", response_model=PuzzleListOut)
async def list_puzzles(
    category: str = "python",
    limit: int = 24,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    query = (
        select(Puzzle)
        .where(and_(Puzzle.category == category, Puzzle.is_active.is_(True)))
        .order_by(Puzzle.elo_rating.asc(), Puzzle.id.asc())
        .limit(max(1, min(limit, 100)))
    )
    result = await db.execute(query)
    items = result.scalars().all()

    # Progreso del user actual: una query plana y agregamos en Python para
    # ser cross-dialect (bool_or no existe en SQLite y los tests corren
    # contra SQLite). El conjunto está acotado por `limit` puzzles.
    puzzle_ids = [p.id for p in items]
    attempted_ids: set[int] = set()
    solved_ids: set[int] = set()
    if puzzle_ids:
        progress_rows = await db.execute(
            select(PuzzleAttempt.puzzle_id, PuzzleAttempt.correct).where(
                and_(
                    PuzzleAttempt.user_id == current_user.id,
                    PuzzleAttempt.puzzle_id.in_(puzzle_ids),
                )
            )
        )
        for puzzle_id, correct in progress_rows:
            attempted_ids.add(puzzle_id)
            if correct:
                solved_ids.add(puzzle_id)

    await db.commit()

    out_items: list[PuzzleOut] = []
    for puzzle in items:
        po = PuzzleOut.model_validate(puzzle)
        po.attempted = puzzle.id in attempted_ids
        po.solved = puzzle.id in solved_ids
        out_items.append(po)
    return PuzzleListOut(items=out_items, total=len(out_items))


@router.get("/interview-problems", response_model=PuzzleListOut)
async def list_interview_problems(
    limit: int = 24,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = await list_puzzles(
        category="interview",
        limit=limit,
        db=db,
        current_user=current_user,
    )
    if result.total > 0:
        return result

    # Self-heal: if interview bank is empty, try seeding and return again.
    await seed_interview_puzzles(db)
    return await list_puzzles(
        category="interview",
        limit=limit,
        db=db,
        current_user=current_user,
    )


@router.get("/puzzles/{puzzle_id}/attempts", response_model=PuzzleAttemptHistoryOut)
async def get_puzzle_attempts(
    puzzle_id: int,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Historial de intentos del usuario actual sobre este puzzle ELO.

    Filtro por user_id; un usuario nunca ve intentos de otro.
    """
    limit = max(1, min(limit, 100))
    result = await db.execute(
        select(PuzzleAttempt)
        .where(
            and_(
                PuzzleAttempt.user_id == current_user.id,
                PuzzleAttempt.puzzle_id == puzzle_id,
            )
        )
        .order_by(PuzzleAttempt.created_at.desc())
        .limit(limit)
    )
    items = result.scalars().all()
    return PuzzleAttemptHistoryOut(
        items=[PuzzleAttemptHistoryItem.model_validate(a) for a in items],
        total=len(items),
    )


@router.post("/attempt", response_model=PuzzleAttemptOut)
async def submit_puzzle_attempt(
    payload: PuzzleAttemptIn,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    puzzle = await db.get(Puzzle, payload.puzzle_id)
    if not puzzle or not puzzle.is_active:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    profile = await _get_or_create_profile(db, current_user.id)
    user_answer = payload.user_answer.strip()
    correct_output = puzzle.correct_output.strip()
    is_correct = user_answer == correct_output

    result = process_attempt(
        user_elo=profile.elo_rating,
        puzzle_elo=puzzle.elo_rating,
        correct=is_correct,
        advanced=puzzle.is_advanced,
    )

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

    puzzle.elo_rating = result.puzzle_elo_after
    puzzle.times_attempted += 1
    if is_correct:
        puzzle.times_correct += 1

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

    # Rating por track (dominio "puzzle", scope = categoría del puzzle).
    # Calcula independiente del overall global: usa el ELO de la track como
    # user_elo y el ELO del puzzle ANTES del intento. Lazy-init heredando el
    # ELO global para dar continuidad al separar.
    track = await get_or_init_rating(
        db,
        current_user.id,
        DOMAIN_PUZZLE,
        puzzle.category,
        fallback_elo=result.user_elo_before,
    )
    track_result = process_attempt(
        user_elo=track.elo_rating,
        puzzle_elo=result.puzzle_elo_before,
        correct=is_correct,
        advanced=puzzle.is_advanced,
    )
    apply_result_to_rating(track, track_result)

    # El timeline vive por track: elo_value/delta/rank son los de la track.
    history_point = EloHistory(
        user_profile_id=profile.id,
        puzzle_id=puzzle.id,
        attempt_id=attempt.id,
        elo_value=track_result.user_elo_after,
        delta=track_result.delta_user,
        correct=is_correct,
        rank_label=track_result.rank_after.value,
        puzzle_title=puzzle.title,
        category=puzzle.category,
        domain=DOMAIN_PUZZLE,
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
        rank_before=result.rank_before.value,
        rank_after=result.rank_after.value,
        rank_changed=result.rank_changed,
        rank_color=get_rank_color(result.rank_after),
        expected_probability=result.expected_probability,
        win_probability_label=win_probability_label(result.expected_probability),
    )
