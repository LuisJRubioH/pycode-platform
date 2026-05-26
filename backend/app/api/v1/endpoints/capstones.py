"""
Endpoints de capstones (proyectos finales por Track).

Lectura solamente en D.1: list, detail y my-submission. El POST de
submission + evaluacion via Pyodide va en D.3.

`hidden_tests` NUNCA aparece en estos endpoints (mismo gate que
`exercises.hidden_tests` — solo expuesto al evaluador dedicado).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.capstone import Capstone, CapstoneSubmission
from app.models.user import User
from app.schemas.capstone import (
    CapstoneDetail,
    CapstoneHiddenTest,
    CapstoneHiddenTestsResponse,
    CapstoneListOut,
    CapstoneSubmissionCreate,
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


@router.get("/{slug}/hidden-tests", response_model=CapstoneHiddenTestsResponse)
async def get_capstone_hidden_tests(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Tests ocultos del capstone para que el worker Pyodide los corra.

    El cliente los recibe solo al pulsar "Enviar capstone" y los pasa al
    worker; la UI nunca los renderiza, solo muestra verdict por test.
    Otros endpoints (list, detail) NO los exponen.
    """
    result = await db.execute(
        select(Capstone).where(
            Capstone.slug == slug,
            Capstone.is_active.is_(True),
        )
    )
    capstone = result.scalar_one_or_none()
    if capstone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Capstone not found",
        )

    raw_tests = capstone.hidden_tests or []
    tests = [
        CapstoneHiddenTest(name=t.get("name", ""), code=t.get("code", ""))
        for t in raw_tests
        if isinstance(t, dict) and t.get("code")
    ]
    return CapstoneHiddenTestsResponse(
        capstone_id=capstone.id, slug=capstone.slug, tests=tests
    )


@router.post(
    "/{slug}/submissions",
    response_model=CapstoneSubmissionOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_capstone_submission(
    slug: str,
    payload: CapstoneSubmissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Persiste una submission del capstone con el resultado de los tests.

    El estado se computa en backend a partir de `tests_passed == tests_total`,
    asi no depende de lo que envie el cliente.
    """
    result = await db.execute(
        select(Capstone).where(
            Capstone.slug == slug,
            Capstone.is_active.is_(True),
        )
    )
    capstone = result.scalar_one_or_none()
    if capstone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Capstone not found",
        )

    if payload.tests_total < 0 or payload.tests_passed < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="tests counters must be non-negative",
        )
    if payload.tests_passed > payload.tests_total:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="tests_passed cannot exceed tests_total",
        )

    expected_total = len(capstone.hidden_tests or [])
    if payload.tests_total != expected_total:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"tests_total mismatch: expected {expected_total}, "
                f"got {payload.tests_total}"
            ),
        )

    final_status = (
        "passed"
        if payload.tests_total > 0 and payload.tests_passed == payload.tests_total
        else "failed"
    )

    files_payload = {f.path: f.content for f in payload.files}
    results_payload = [v.model_dump() for v in payload.test_results]

    submission = CapstoneSubmission(
        user_id=current_user.id,
        capstone_id=capstone.id,
        files=files_payload,
        status=final_status,
        tests_passed=payload.tests_passed,
        tests_total=payload.tests_total,
        test_results=results_payload,
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    return CapstoneSubmissionOut.model_validate(submission)
