"""
Users endpoints.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User, UserProfile
from app.schemas.auth import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user


@router.get("/profile")
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user profile with progress stats."""
    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "created_at": current_user.created_at,
        },
        "profile": {"level": "beginner", "xp_points": 0, "badges": []},
    }


def _row(o):
    return {c.name: getattr(o, c.name) for c in o.__table__.columns}


@router.get("/me/export")
async def export_my_data(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """GDPR: exporta todos los datos del usuario en JSON."""
    from app.models.learning import CodeSubmission, TutorSession, UserProgress

    profile = (
        await db.execute(
            select(UserProfile).where(UserProfile.user_id == current_user.id)
        )
    ).scalar_one_or_none()
    progress = (
        (
            await db.execute(
                select(UserProgress).where(UserProgress.user_id == current_user.id)
            )
        )
        .scalars()
        .all()
    )
    submissions = (
        (
            await db.execute(
                select(CodeSubmission).where(CodeSubmission.user_id == current_user.id)
            )
        )
        .scalars()
        .all()
    )
    tutor_msgs = (
        (
            await db.execute(
                select(TutorSession).where(TutorSession.user_id == current_user.id)
            )
        )
        .scalars()
        .all()
    )

    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "created_at": current_user.created_at.isoformat(),
        },
        "profile": _row(profile) if profile else None,
        "progress": [_row(p) for p in progress],
        "submissions": [_row(s) for s in submissions],
        "tutor_messages": [_row(t) for t in tutor_msgs],
        "exported_at": datetime.utcnow().isoformat() + "Z",
    }


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """GDPR: borra la cuenta. ON DELETE CASCADE limpia datos relacionados."""
    await db.execute(delete(User).where(User.id == current_user.id))
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
