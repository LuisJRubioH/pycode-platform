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
from app.schemas.elo_schemas import (
    EloHistoryOut,
    EloHistoryPoint,
    EloProfileOut,
    EloRankTableOut,
    EloTableRow,
    PuzzleListOut,
    PuzzleAttemptIn,
    PuzzleAttemptOut,
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
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    profile = await _get_or_create_profile(db, current_user.id)
    result = await db.execute(
        select(EloHistory)
        .where(EloHistory.user_profile_id == profile.id)
        .order_by(EloHistory.created_at)
        .limit(limit)
    )
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
    _ = current_user
    query = (
        select(Puzzle)
        .where(and_(Puzzle.category == category, Puzzle.is_active.is_(True)))
        .order_by(Puzzle.elo_rating.asc(), Puzzle.id.asc())
        .limit(max(1, min(limit, 100)))
    )
    result = await db.execute(query)
    items = result.scalars().all()
    await db.commit()
    return PuzzleListOut(
        items=[PuzzleOut.model_validate(puzzle) for puzzle in items], total=len(items)
    )


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
        rank_before=result.rank_before.value,
        rank_after=result.rank_after.value,
        rank_changed=result.rank_changed,
        rank_color=get_rank_color(result.rank_after),
        expected_probability=result.expected_probability,
        win_probability_label=win_probability_label(result.expected_probability),
    )
