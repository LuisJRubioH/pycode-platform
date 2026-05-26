"""
Certificate model — credencial verificable que emite cada Track al
aprobar su capstone.

Patrón replicable a Tracks 2-6: cuando un usuario tiene una
`CapstoneSubmission` con `status="passed"` para el capstone del Track,
se emite (get-or-create) un `Certificate` con:
- `recipient_name`: snapshot del username al momento de emitir (el PDF
  no debe cambiar si el usuario renombra su cuenta después).
- `verification_code`: código público e impredecible que actúa como
  capacidad — cualquiera con el código puede verificar el certificado en
  el endpoint público `/certificates/verify/{code}`.
- `issued_at`: fecha de emisión (estable, no "ahora" en cada descarga).

La tabla es PÚBLICA (sin RLS, como `capstones`): un certificado es por
diseño una credencial compartible/verificable, no hay nada privado en él.
El listado "mis certificados" filtra por `user_id` en la capa de app.
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Certificate(Base):
    """Certificado de finalización de un Track (emitido al aprobar el capstone)."""

    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    capstone_id = Column(
        Integer,
        ForeignKey("capstones.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    track = Column(String(50), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    recipient_name = Column(String(120), nullable=False)
    verification_code = Column(String(40), unique=True, nullable=False, index=True)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")
    capstone = relationship("Capstone")

    __table_args__ = (
        # Un certificado por usuario por track (idempotente al re-emitir).
        UniqueConstraint("user_id", "track", name="uq_certificate_user_track"),
    )
