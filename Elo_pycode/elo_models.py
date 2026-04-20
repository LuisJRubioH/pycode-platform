"""
Modelos SQLAlchemy para el sistema ELO de PyCode Platform
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, Float,
    DateTime, ForeignKey, Text, Enum as SAEnum
)
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class UserProfile(Base):
    """Perfil del usuario con su ELO y estadísticas"""
    __tablename__ = "user_profiles"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    elo_rating    = Column(Integer, default=1000, nullable=False)
    elo_peak      = Column(Integer, default=1000, nullable=False)   # máximo histórico
    rank          = Column(String(50), default="Beginner")
    puzzles_attempted = Column(Integer, default=0)
    puzzles_correct   = Column(Integer, default=0)
    streak_current    = Column(Integer, default=0)
    streak_best       = Column(Integer, default=0)
    last_activity     = Column(DateTime, nullable=True)
    created_at        = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    elo_history   = relationship("EloHistory", back_populates="user_profile",
                                  order_by="EloHistory.created_at")
    user          = relationship("User", back_populates="profile")

    @property
    def accuracy(self) -> float:
        if self.puzzles_attempted == 0:
            return 0.0
        return round(self.puzzles_correct / self.puzzles_attempted * 100, 1)


class Puzzle(Base):
    """Un puzzle de código con su propio rating ELO"""
    __tablename__ = "puzzles"

    id            = Column(Integer, primary_key=True, index=True)
    title         = Column(String(200), nullable=False)
    slug          = Column(String(200), unique=True, nullable=False)
    category      = Column(String(50), nullable=False)      # python, numpy, pandas
    topic         = Column(String(100), nullable=False)     # loops, functions, etc.
    code_snippet  = Column(Text, nullable=False)
    correct_output = Column(Text, nullable=False)
    explanation   = Column(Text, nullable=False)
    hint          = Column(Text, nullable=True)

    # ELO del puzzle — converge a su dificultad real con el tiempo
    elo_rating    = Column(Integer, default=1200, nullable=False)
    # ELO inicial declarado por el autor (ancla de referencia)
    elo_initial   = Column(Integer, default=1200, nullable=False)

    times_attempted = Column(Integer, default=0)
    times_correct   = Column(Integer, default=0)
    is_advanced     = Column(Boolean, default=False)  # True → tabla NumPy/Pandas
    is_active       = Column(Boolean, default=True)

    # Finxter reference data (si el puzzle viene de los libros)
    finxter_id    = Column(Integer, nullable=True)
    source_book   = Column(String(100), nullable=True)  # "Coffee Break Python", etc.

    created_at    = Column(DateTime, default=datetime.utcnow)
    updated_at    = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attempts      = relationship("PuzzleAttempt", back_populates="puzzle")

    @property
    def solve_rate(self) -> float:
        if self.times_attempted == 0:
            return 0.0
        return round(self.times_correct / self.times_attempted * 100, 1)

    @property
    def difficulty_label(self) -> str:
        if self.elo_rating < 800:   return "Introductory"
        if self.elo_rating < 1100:  return "Easy"
        if self.elo_rating < 1400:  return "Medium"
        if self.elo_rating < 1700:  return "Hard"
        if self.elo_rating < 2000:  return "Expert"
        return "Master"


class PuzzleAttempt(Base):
    """Registro de cada intento usuario ↔ puzzle"""
    __tablename__ = "puzzle_attempts"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), nullable=False)
    puzzle_id       = Column(Integer, ForeignKey("puzzles.id"), nullable=False)

    correct         = Column(Boolean, nullable=False)
    user_answer     = Column(Text, nullable=True)

    # Snapshots de ELO antes y después
    user_elo_before    = Column(Integer, nullable=False)
    user_elo_after     = Column(Integer, nullable=False)
    puzzle_elo_before  = Column(Integer, nullable=False)
    puzzle_elo_after   = Column(Integer, nullable=False)
    elo_delta_user     = Column(Integer, nullable=False)   # puede ser negativo
    elo_delta_puzzle   = Column(Integer, nullable=False)

    expected_probability = Column(Float, nullable=False)   # prob. de éxito calculada
    time_spent_seconds   = Column(Integer, nullable=True)

    created_at      = Column(DateTime, default=datetime.utcnow)

    puzzle          = relationship("Puzzle", back_populates="attempts")


class EloHistory(Base):
    """
    Serie temporal del ELO del usuario — para graficar la curva de progreso
    Se registra un punto por cada puzzle resuelto.
    """
    __tablename__ = "elo_history"

    id             = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    puzzle_id      = Column(Integer, ForeignKey("puzzles.id"), nullable=False)
    attempt_id     = Column(Integer, ForeignKey("puzzle_attempts.id"), nullable=False)

    elo_value      = Column(Integer, nullable=False)     # ELO después del intento
    delta          = Column(Integer, nullable=False)     # cambio en este intento
    correct        = Column(Boolean, nullable=False)
    rank_label     = Column(String(50), nullable=False)
    puzzle_title   = Column(String(200), nullable=False)  # desnormalizado para queries rápidos
    category       = Column(String(50), nullable=False)

    created_at     = Column(DateTime, default=datetime.utcnow)

    user_profile   = relationship("UserProfile", back_populates="elo_history")
