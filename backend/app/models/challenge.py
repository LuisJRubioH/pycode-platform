"""
Models for imported coding challenges.
"""

from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class CodingChallenge(Base):
    """A challenge imported from an external repository or local collection."""

    __tablename__ = "coding_challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    source = Column(String(120), nullable=False)
    source_path = Column(String(500), nullable=False)
    difficulty = Column(String(20), nullable=False, index=True)
    topic = Column(String(120), nullable=False, default="logic")
    prompt = Column(Text, nullable=False)
    starter_code = Column(Text, nullable=False, default="# Escribe tu solucion aqui\n")
    reference_solution = Column(Text, nullable=True)
    # [{name, code}] que el editor corre en Pyodide; completar el reto exige
    # pasarlos todos (ver POST /challenges/{id}/complete).
    hidden_tests = Column(JSON, default=list)
    order_index = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
