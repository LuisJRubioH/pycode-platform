"""
Endpoints de certificados verificables.

Un certificado se emite (get-or-create idempotente) cuando el usuario tiene
una `CapstoneSubmission` con `status="passed"` para el capstone del Track.
El gate se computa server-side; el cliente nunca puede forzar la emisión.

- GET    /certificates                -> mis certificados emitidos
- POST   /certificates/{track}/issue  -> emite (o devuelve) el certificado del track
- GET    /certificates/{track}/download -> PDF descargable (emite si hace falta)
- GET    /certificates/verify/{code}  -> verificación PÚBLICA por código

La tabla `certificates` es pública (sin RLS): un certificado es una
credencial compartible. El `verification_code` impredecible es la capacidad
de acceso a la verificación; el listado filtra por `user_id` en la app.
"""

import secrets

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.tracks import track_title
from app.models.capstone import Capstone, CapstoneSubmission
from app.models.certificate import Certificate
from app.models.user import User
from app.schemas.certificate import (
    CertificateListOut,
    CertificateOut,
    CertificateVerifyOut,
)
from app.services.certificate_pdf import render_certificate_pdf

router = APIRouter()


def _generate_verification_code() -> str:
    """Código público impredecible, legible: `PYC-XXXX-XXXX` (hex mayúsculas)."""
    raw = secrets.token_hex(4).upper()  # 8 hex chars
    return f"PYC-{raw[:4]}-{raw[4:]}"


async def _passed_capstone_for_track(
    db: AsyncSession, user_id: int, track: str
) -> Capstone | None:
    """Capstone del track que el usuario aprobó (status=passed), o None.

    Si el track tiene varios capstones, devuelve el primero aprobado por
    `order_index`. None significa que el gate del certificado NO está abierto.
    """
    cap_rows = await db.execute(
        select(Capstone)
        .where(Capstone.track == track, Capstone.is_active.is_(True))
        .order_by(Capstone.order_index.asc())
    )
    capstones = cap_rows.scalars().all()
    if not capstones:
        return None
    cap_by_id = {c.id: c for c in capstones}

    passed_rows = await db.execute(
        select(CapstoneSubmission.capstone_id)
        .where(
            CapstoneSubmission.user_id == user_id,
            CapstoneSubmission.capstone_id.in_(list(cap_by_id.keys())),
            CapstoneSubmission.status == "passed",
        )
        .distinct()
    )
    passed_ids = {row[0] for row in passed_rows.all()}
    for cap in capstones:  # respeta order_index
        if cap.id in passed_ids:
            return cap
    return None


async def _get_or_issue_certificate(
    db: AsyncSession, user: User, track: str
) -> Certificate:
    """Devuelve el certificado del track para el usuario, emitiéndolo si el
    capstone está aprobado. Lanza 403 si el gate no está abierto."""
    existing = (
        await db.execute(
            select(Certificate).where(
                Certificate.user_id == user.id,
                Certificate.track == track,
            )
        )
    ).scalar_one_or_none()
    if existing is not None:
        return existing

    capstone = await _passed_capstone_for_track(db, user.id, track)
    if capstone is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Certificado bloqueado: aún no apruebas el capstone del track.",
        )

    cert = Certificate(
        user_id=user.id,
        capstone_id=capstone.id,
        track=track,
        title=track_title(track),
        recipient_name=user.username,
        verification_code=_generate_verification_code(),
    )
    db.add(cert)
    try:
        await db.commit()
    except IntegrityError:
        # Carrera: otro request lo emitió (unique user+track o code). Re-lee.
        await db.rollback()
        existing = (
            await db.execute(
                select(Certificate).where(
                    Certificate.user_id == user.id,
                    Certificate.track == track,
                )
            )
        ).scalar_one_or_none()
        if existing is None:
            raise
        return existing
    await db.refresh(cert)
    return cert


@router.get("", response_model=CertificateListOut)
async def list_my_certificates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Certificados ya emitidos para el usuario actual."""
    rows = await db.execute(
        select(Certificate)
        .where(Certificate.user_id == current_user.id)
        .order_by(Certificate.issued_at.desc())
    )
    items = [CertificateOut.model_validate(c) for c in rows.scalars().all()]
    return CertificateListOut(items=items, total=len(items))


@router.get("/verify/{code}", response_model=CertificateVerifyOut)
async def verify_certificate(
    code: str,
    db: AsyncSession = Depends(get_db),
):
    """Verificación PÚBLICA (sin auth) de un certificado por su código."""
    cert = (
        await db.execute(
            select(Certificate).where(Certificate.verification_code == code)
        )
    ).scalar_one_or_none()
    if cert is None:
        return CertificateVerifyOut(valid=False)
    return CertificateVerifyOut(
        valid=True,
        recipient_name=cert.recipient_name,
        title=cert.title,
        track=cert.track,
        issued_at=cert.issued_at,
    )


@router.post("/{track}/issue", response_model=CertificateOut)
async def issue_certificate(
    track: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Emite (o devuelve) el certificado del track. Idempotente."""
    cert = await _get_or_issue_certificate(db, current_user, track)
    return CertificateOut.model_validate(cert)


@router.get("/{track}/download")
async def download_certificate(
    track: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Descarga el PDF del certificado del track (lo emite si hace falta)."""
    cert = await _get_or_issue_certificate(db, current_user, track)
    verify_url = f"{settings.FRONTEND_URL.rstrip('/')}/verify/{cert.verification_code}"
    pdf_bytes = render_certificate_pdf(
        recipient_name=cert.recipient_name,
        track_title=cert.title,
        issued_at=cert.issued_at,
        verification_code=cert.verification_code,
        verify_url=verify_url,
    )
    filename = f"certificado-pycode-{cert.track}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
