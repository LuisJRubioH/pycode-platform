"""
Endpoints for imported coding challenges.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.challenge import CodingChallenge
from app.models.challenge_completion import ChallengeCompletion
from app.models.elo_models import EloRating
from app.models.user import User, UserProfile
from app.schemas.challenge import (
    CodingChallengeDetail,
    CodingChallengeListOut,
    CodingChallengeSummary,
)
from app.services.challenge_importer import recommended_difficulty_for_elo
from app.services.elo_rating_service import (
    DOMAIN_CHALLENGE,
    apply_result_to_rating,
    get_or_init_rating,
    nominal_elo_for_difficulty,
)
from app.services.elo_service import get_rank, process_attempt

router = APIRouter()


async def _get_user_profile(db: AsyncSession, user_id: int) -> UserProfile | None:
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    return result.scalar_one_or_none()


async def _completed_ids_for_user(
    db: AsyncSession, user_id: int, challenge_ids: list[int]
) -> set[int]:
    if not challenge_ids:
        return set()
    rows = await db.execute(
        select(ChallengeCompletion.challenge_id).where(
            ChallengeCompletion.user_id == user_id,
            ChallengeCompletion.challenge_id.in_(challenge_ids),
        )
    )
    return {row[0] for row in rows.all()}


@router.get("", response_model=CodingChallengeListOut)
async def list_challenges(
    difficulty: str | None = Query(default=None),
    recommended: bool = Query(default=False),
    limit: int = Query(default=30, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    profile = await _get_user_profile(db, current_user.id)
    recommended_difficulty = recommended_difficulty_for_elo(
        profile.elo_rating if profile else 1000
    )
    target_difficulty = (
        recommended_difficulty if recommended and not difficulty else difficulty
    )

    query = select(CodingChallenge).where(CodingChallenge.is_active.is_(True))
    if target_difficulty:
        query = query.where(CodingChallenge.difficulty == target_difficulty)

    query = query.order_by(
        asc(CodingChallenge.order_index),
        asc(CodingChallenge.title),
    ).limit(limit)

    result = await db.execute(query)
    challenges = result.scalars().all()
    completed_ids = await _completed_ids_for_user(
        db, current_user.id, [c.id for c in challenges]
    )

    items = [
        CodingChallengeSummary(
            id=challenge.id,
            title=challenge.title,
            slug=challenge.slug,
            source=challenge.source,
            difficulty=challenge.difficulty,
            topic=challenge.topic,
            prompt_preview=challenge.prompt[:220],
            order_index=challenge.order_index,
            completed=challenge.id in completed_ids,
        )
        for challenge in challenges
    ]

    return CodingChallengeListOut(
        items=items,
        total=len(items),
        recommended_difficulty=recommended_difficulty,
    )


@router.get("/recommended", response_model=CodingChallengeListOut)
async def list_recommended_challenges(
    limit: int = Query(default=12, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await list_challenges(
        difficulty=None,
        recommended=True,
        limit=limit,
        db=db,
        current_user=current_user,
    )


@router.get("/{challenge_id}", response_model=CodingChallengeDetail)
async def get_challenge(
    challenge_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    challenge = await db.get(CodingChallenge, challenge_id)
    if not challenge or not challenge.is_active:
        raise HTTPException(status_code=404, detail="Challenge not found")

    return CodingChallengeDetail.model_validate(challenge)


@router.post("/{challenge_id}/complete", status_code=status.HTTP_204_NO_CONTENT)
async def mark_challenge_completed(
    challenge_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Marca el reto como hecho y otorga ELO a la track `challenge:<dificultad>`.

    Idempotente: si ya estaba marcado, no re-otorga. El ELO concedido se guarda
    en la completación para poder revertirlo exacto al desmarcar.
    """
    challenge = await db.get(CodingChallenge, challenge_id)
    if not challenge or not challenge.is_active:
        raise HTTPException(status_code=404, detail="Challenge not found")

    existing = await db.execute(
        select(ChallengeCompletion).where(
            ChallengeCompletion.user_id == current_user.id,
            ChallengeCompletion.challenge_id == challenge_id,
        )
    )
    if existing.scalar_one_or_none() is None:
        profile = await _get_user_profile(db, current_user.id)
        fallback = profile.elo_rating if profile else 1000
        rating = await get_or_init_rating(
            db,
            current_user.id,
            DOMAIN_CHALLENGE,
            challenge.difficulty,
            fallback_elo=fallback,
        )
        result = process_attempt(
            user_elo=rating.elo_rating,
            puzzle_elo=nominal_elo_for_difficulty(challenge.difficulty),
            correct=True,
        )
        apply_result_to_rating(rating, result)
        db.add(
            ChallengeCompletion(
                user_id=current_user.id,
                challenge_id=challenge_id,
                elo_delta=result.delta_user,
            )
        )
        await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{challenge_id}/complete", status_code=status.HTTP_204_NO_CONTENT)
async def unmark_challenge_completed(
    challenge_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Quita la marca de hecho y revierte el ELO otorgado al marcar."""
    row = await db.execute(
        select(ChallengeCompletion).where(
            ChallengeCompletion.user_id == current_user.id,
            ChallengeCompletion.challenge_id == challenge_id,
        )
    )
    completion = row.scalar_one_or_none()
    if completion is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    challenge = await db.get(CodingChallenge, challenge_id)
    if challenge is not None:
        rating_row = await db.execute(
            select(EloRating).where(
                EloRating.user_id == current_user.id,
                EloRating.domain == DOMAIN_CHALLENGE,
                EloRating.scope == challenge.difficulty,
            )
        )
        rating = rating_row.scalar_one_or_none()
        if rating is not None:
            rating.elo_rating = max(0, rating.elo_rating - (completion.elo_delta or 0))
            rating.attempts = max(0, rating.attempts - 1)
            rating.correct = max(0, rating.correct - 1)
            rating.streak_current = max(0, rating.streak_current - 1)
            rating.rank = get_rank(rating.elo_rating).value

    await db.delete(completion)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
