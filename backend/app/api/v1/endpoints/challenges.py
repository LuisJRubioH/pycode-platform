"""
Endpoints for imported coding challenges.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.challenge import CodingChallenge
from app.models.user import User, UserProfile
from app.schemas.challenge import (
    CodingChallengeDetail,
    CodingChallengeListOut,
    CodingChallengeSummary,
)
from app.services.challenge_importer import recommended_difficulty_for_elo

router = APIRouter()


async def _get_user_profile(db: AsyncSession, user_id: int) -> UserProfile | None:
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    return result.scalar_one_or_none()


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
