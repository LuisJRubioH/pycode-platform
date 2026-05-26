"""
Endpoints de capstones (proyectos finales por Track).

Lectura solamente en D.1: list, detail y my-submission. El POST de
submission + evaluacion via Pyodide va en D.3.

`hidden_tests` NUNCA aparece en estos endpoints (mismo gate que
`exercises.hidden_tests` — solo expuesto al evaluador dedicado).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.capstone import Capstone, CapstoneSubmission
from app.models.user import User
from app.schemas.capstone import (
    CapstoneDetail,
    CapstoneListOut,
    CapstoneSubmissionOut,
    CapstoneSummary,
)

router = APIRouter()


async def _completed_capstone_ids(
    db: AsyncSession, user_id: int, capstone_ids: list[int]
) -> set[int]:
    if not capstone_ids:
        return set()
    rows = await db.execute(
        select(CapstoneSubmission.capstone_id)
        .where(
            CapstoneSubmission.user_id == user_id,
            CapstoneSubmission.capstone_id.in_(capstone_ids),
            CapstoneSubmission.status == "passed",
        )
        .distinct()
    )
    return {row[0] for row in rows.all()}


@router.get("", response_model=CapstoneListOut)
async def list_capstones(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Lista todos los capstones activos ordenados por track + order_index."""
    result = await db.execute(
        select(Capstone)
        .where(Capstone.is_active.is_(True))
        .order_by(asc(Capstone.track), asc(Capstone.order_index))
    )
    capstones = result.scalars().all()

    completed_ids = await _completed_capstone_ids(
        db, current_user.id, [c.id for c in capstones]
    )

    items = [
        CapstoneSummary(
            id=c.id,
            slug=c.slug,
            track=c.track,
            title=c.title,
            short_description=c.short_description,
            estimated_hours=c.estimated_hours,
            difficulty=c.difficulty,
            order_index=c.order_index,
            completed=c.id in completed_ids,
        )
        for c in capstones
    ]
    return CapstoneListOut(items=items, total=len(items))


@router.get("/{slug}", response_model=CapstoneDetail)
async def get_capstone(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Detalle del capstone (sin hidden_tests, solo `tests_total`)."""
    result = await db.execute(
        select(Capstone).where(
            Capstone.slug == slug,
            Capstone.is_active.is_(True),
        )
    )
    capstone = result.scalar_one_or_none()
    if capstone is None:
        raise HTTPException(status_code=404, detail="Capstone not found")

    return CapstoneDetail(
        id=capstone.id,
        slug=capstone.slug,
        track=capstone.track,
        title=capstone.title,
        short_description=capstone.short_description,
        description=capstone.description,
        requirements=capstone.requirements or [],
        starter_files=capstone.starter_files or [],
        tests_total=len(capstone.hidden_tests or []),
        estimated_hours=capstone.estimated_hours,
        difficulty=capstone.difficulty,
        order_index=capstone.order_index,
    )


@router.get("/{slug}/my-submission", response_model=CapstoneSubmissionOut)
async def get_my_submission(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Ultima submission del usuario actual para este capstone."""
    capstone_row = await db.execute(
        select(Capstone.id).where(
            Capstone.slug == slug,
            Capstone.is_active.is_(True),
        )
    )
    capstone_id = capstone_row.scalar_one_or_none()
    if capstone_id is None:
        raise HTTPException(status_code=404, detail="Capstone not found")

    sub_row = await db.execute(
        select(CapstoneSubmission)
        .where(
            CapstoneSubmission.user_id == current_user.id,
            CapstoneSubmission.capstone_id == capstone_id,
        )
        .order_by(CapstoneSubmission.created_at.desc())
        .limit(1)
    )
    submission = sub_row.scalar_one_or_none()
    if submission is None:
        raise HTTPException(status_code=404, detail="No submission yet")

    return CapstoneSubmissionOut.model_validate(submission)
