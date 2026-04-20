"""
Pydantic schemas for the ELO API.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PuzzleOut(BaseModel):
    id: int
    title: str
    category: str
    topic: str
    code_snippet: str
    difficulty_label: str
    elo_rating: int
    solve_rate: float
    source_book: Optional[str] = None

    model_config = {"from_attributes": True}


class PuzzleListOut(BaseModel):
    items: list[PuzzleOut]
    total: int


class PuzzleAttemptIn(BaseModel):
    puzzle_id: int
    user_answer: str
    time_spent_seconds: Optional[int] = None


class PuzzleAttemptOut(BaseModel):
    correct: bool
    correct_output: str
    explanation: str
    user_elo_before: int
    user_elo_after: int
    elo_delta_user: int
    puzzle_elo_before: int
    puzzle_elo_after: int
    rank_before: str
    rank_after: str
    rank_changed: bool
    rank_color: str
    expected_probability: float
    win_probability_label: str


class EloProfileOut(BaseModel):
    elo_rating: int
    elo_peak: int
    rank: str
    rank_color: str
    puzzles_attempted: int
    puzzles_correct: int
    accuracy: float
    streak_current: int
    streak_best: int


class EloHistoryPoint(BaseModel):
    elo_value: int
    delta: int
    correct: bool
    rank_label: str
    puzzle_title: str
    category: str
    created_at: datetime

    model_config = {"from_attributes": True}


class EloHistoryOut(BaseModel):
    history: list[EloHistoryPoint]
    total_points: int


class EloTableRow(BaseModel):
    elo_min: int
    elo_max: Optional[int]
    rank: str
    color: str
    is_current: bool = False


class EloRankTableOut(BaseModel):
    rows: list[EloTableRow]
    user_elo: int
    user_rank: str
