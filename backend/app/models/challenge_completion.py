"""Tabla de completaciones manuales de retos (Fase 1)."""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint

from app.core.database import Base


class ChallengeCompletion(Base):
    """Marca de 'hecho' que el alumno pone manualmente sobre un reto.

    Una fila por (user, challenge); volver a marcar es un no-op idempotente.
    """

    __tablename__ = "challenge_completions"
    __table_args__ = (
        UniqueConstraint("user_id", "challenge_id", name="uq_challenge_completion"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    challenge_id = Column(
        Integer,
        ForeignKey("coding_challenges.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
