"""
Snapshot de calidad de código para medir progresión en el tiempo.

Combina dos señales por cada evaluación:
- `logic_score` / `general_score`: del evaluador socrático LLM (juicio de
  lógica y enfoque).
- `static_score` + `metrics`: del análisis estático `ast` (forma objetiva del
  código: complejidad, longitud, anidamiento, docstrings).

Una fila por evento evaluado; `GET /progress/code-quality` arma la serie
temporal y las medias móviles.
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON

from app.core.database import Base


class CodeQualitySnapshot(Base):
    """Punto de medición de calidad/lógica del código de un usuario."""

    __tablename__ = "code_quality_snapshots"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Origen del snapshot ("evaluation", y a futuro "exercise"/"capstone").
    source = Column(String(40), nullable=False, default="evaluation")
    reference_id = Column(Integer, nullable=True)
    logic_score = Column(Integer, nullable=True)
    general_score = Column(Integer, nullable=True)
    static_score = Column(Integer, nullable=True)
    metrics = Column(JSONB().with_variant(JSON(), "sqlite"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (Index("ix_code_quality_user_created", "user_id", "created_at"),)
