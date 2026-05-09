from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON

from app.core.database import Base


class CodeEvaluation(Base):
    """Resultado de una evaluación socrática de código.

    Atómica: una fila por cada pulsada de "Evaluar mi código". No
    mantiene historial conversacional (eso vive en `tutor_sessions`).
    """

    __tablename__ = "code_evaluations"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exercise_id = Column(
        Integer,
        ForeignKey("exercises.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    problem_description = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=True)
    actual_output = Column(Text, nullable=True)
    # JSONB en Postgres, JSON en SQLite (los tests corren con SQLite).
    verdict = Column(JSONB().with_variant(JSON(), "sqlite"), nullable=False)
    model_used = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_code_evaluations_user_created", "user_id", "created_at"),
    )
