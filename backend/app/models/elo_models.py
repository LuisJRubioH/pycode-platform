"""
SQLAlchemy models for the ELO puzzle system.
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Puzzle(Base):
    """A code puzzle with its own dynamic ELO difficulty."""

    __tablename__ = "puzzles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False)
    topic = Column(String(100), nullable=False)
    code_snippet = Column(Text, nullable=False)
    correct_output = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    hint = Column(Text, nullable=True)
    elo_rating = Column(Integer, default=1200, nullable=False)
    elo_initial = Column(Integer, default=1200, nullable=False)
    times_attempted = Column(Integer, default=0, nullable=False)
    times_correct = Column(Integer, default=0, nullable=False)
    is_advanced = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    finxter_id = Column(Integer, nullable=True)
    source_book = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attempts = relationship("PuzzleAttempt", back_populates="puzzle", cascade="all, delete-orphan")

    @property
    def solve_rate(self) -> float:
        if self.times_attempted == 0:
            return 0.0
        return round(self.times_correct / self.times_attempted * 100, 1)

    @property
    def difficulty_label(self) -> str:
        if self.elo_rating < 800:
            return "Introductory"
        if self.elo_rating < 1100:
            return "Easy"
        if self.elo_rating < 1400:
            return "Medium"
        if self.elo_rating < 1700:
            return "Hard"
        if self.elo_rating < 2000:
            return "Expert"
        return "Master"


class PuzzleAttempt(Base):
    """Each user attempt against a puzzle."""

    __tablename__ = "puzzle_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    puzzle_id = Column(Integer, ForeignKey("puzzles.id"), nullable=False, index=True)
    correct = Column(Boolean, nullable=False)
    user_answer = Column(Text, nullable=True)
    user_elo_before = Column(Integer, nullable=False)
    user_elo_after = Column(Integer, nullable=False)
    puzzle_elo_before = Column(Integer, nullable=False)
    puzzle_elo_after = Column(Integer, nullable=False)
    elo_delta_user = Column(Integer, nullable=False)
    elo_delta_puzzle = Column(Integer, nullable=False)
    expected_probability = Column(Float, nullable=False)
    time_spent_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    puzzle = relationship("Puzzle", back_populates="attempts")


class EloHistory(Base):
    """Time series for the user's ELO progression."""

    __tablename__ = "elo_history"

    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False, index=True)
    puzzle_id = Column(Integer, ForeignKey("puzzles.id"), nullable=False)
    attempt_id = Column(Integer, ForeignKey("puzzle_attempts.id"), nullable=False)
    elo_value = Column(Integer, nullable=False)
    delta = Column(Integer, nullable=False)
    correct = Column(Boolean, nullable=False)
    rank_label = Column(String(50), nullable=False)
    puzzle_title = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_profile = relationship("UserProfile", back_populates="elo_history")
