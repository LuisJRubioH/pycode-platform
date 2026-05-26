"""
Capstone models — proyecto final por Track.

Patrón replicable a Tracks 2-6:
- `Capstone` es definicional (seedeado): enunciado en markdown, requisitos
  estructurados, archivos starter del proyecto y tests ocultos Pyodide.
- `CapstoneSubmission` guarda lo que el usuario subió (archivos modificados),
  el verdict de los tests ocultos y el resumen pass/fail.

Los tests ocultos NUNCA se exponen en los endpoints de detalle (mismo gate
que `exercises.hidden_tests`: solo accesibles vía endpoint dedicado al
evaluador). El cliente recibe los tests al pulsar "Enviar capstone" y los
corre en el worker Pyodide; la UI nunca renderiza el código del test.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

from app.core.database import Base


class Capstone(Base):
    """Proyecto capstone de un Track (definicional, seedeado)."""

    __tablename__ = "capstones"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(120), unique=True, nullable=False, index=True)
    track = Column(String(50), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    short_description = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(JSONB().with_variant(JSON(), "sqlite"), nullable=False)
    starter_files = Column(JSONB().with_variant(JSON(), "sqlite"), nullable=False)
    hidden_tests = Column(
        JSONB().with_variant(JSON(), "sqlite"),
        nullable=False,
        default=list,
        server_default="[]",
    )
    estimated_hours = Column(Integer, default=8, nullable=False)
    difficulty = Column(String(20), default="intermediate", nullable=False)
    order_index = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    submissions = relationship(
        "CapstoneSubmission",
        back_populates="capstone",
        cascade="all, delete-orphan",
    )


class CapstoneSubmission(Base):
    """Submission del usuario para un capstone (1+ por usuario por capstone)."""

    __tablename__ = "capstone_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    capstone_id = Column(
        Integer,
        ForeignKey("capstones.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    files = Column(JSONB().with_variant(JSON(), "sqlite"), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    tests_passed = Column(Integer, default=0, nullable=False)
    tests_total = Column(Integer, default=0, nullable=False)
    test_results = Column(JSONB().with_variant(JSON(), "sqlite"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")
    capstone = relationship("Capstone", back_populates="submissions")

    __table_args__ = (
        Index(
            "ix_capstone_submissions_user_capstone",
            "user_id",
            "capstone_id",
        ),
    )
