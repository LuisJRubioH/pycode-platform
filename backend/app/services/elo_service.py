"""
Core ELO logic for puzzle evaluation and ranking.
"""

from dataclasses import dataclass
from enum import Enum
import math


class EloRank(str, Enum):
    BASIC_KNOWLEDGE = "Basic Knowledge"
    BEGINNER = "Beginner"
    AUTODIDACT = "Autodidact"
    SCHOLAR = "Scholar"
    LEARNER = "Learner"
    EXPERIENCED_LEARNER = "Experienced Learner"
    INTERMEDIATE = "Intermediate"
    EXPERIENCED_INTERMEDIATE = "Experienced Intermediate"
    EXPERT = "Expert"
    PROFESSIONAL = "Professional"
    AUTHORITY = "Authority"
    MASTER_CANDIDATE = "Master Candidate"
    NATIONAL_MASTER = "National Master"
    MASTER = "Master"
    INTERNATIONAL_MASTER = "International Master"
    GRANDMASTER = "Grandmaster"
    WORLD_CLASS = "World Class"


ELO_DELTA_TABLE = [
    (0, 500, 43, -12),
    (500, 1000, 21, -34),
    (1000, 1500, 9, -46),
    (1500, 2000, 8, -47),
    (2000, 9999, 8, -47),
]

ELO_DELTA_TABLE_ADVANCED = [
    (0, 1500, 60, -4),
    (1500, 1600, 56, -8),
    (1600, 1700, 52, -12),
    (1700, 1800, 46, -18),
    (1800, 1900, 36, -28),
    (1900, 2000, 28, -36),
    (2000, 2100, 18, -46),
    (2100, 2200, 12, -52),
    (2200, 9999, 10, -60),
]


@dataclass
class EloResult:
    user_elo_before: int
    puzzle_elo_before: int
    correct: bool
    user_elo_after: int
    puzzle_elo_after: int
    delta_user: int
    delta_puzzle: int
    rank_before: EloRank
    rank_after: EloRank
    rank_changed: bool
    expected_probability: float


def get_rank(elo: int) -> EloRank:
    if elo >= 2500:
        return EloRank.WORLD_CLASS
    if elo >= 2400:
        return EloRank.GRANDMASTER
    if elo >= 2300:
        return EloRank.INTERNATIONAL_MASTER
    if elo >= 2200:
        return EloRank.MASTER
    if elo >= 2100:
        return EloRank.NATIONAL_MASTER
    if elo >= 2000:
        return EloRank.MASTER_CANDIDATE
    if elo >= 1900:
        return EloRank.AUTHORITY
    if elo >= 1800:
        return EloRank.PROFESSIONAL
    if elo >= 1700:
        return EloRank.EXPERT
    if elo >= 1600:
        return EloRank.EXPERIENCED_INTERMEDIATE
    if elo >= 1500:
        return EloRank.INTERMEDIATE
    if elo >= 1400:
        return EloRank.EXPERIENCED_LEARNER
    if elo >= 1300:
        return EloRank.LEARNER
    if elo >= 1200:
        return EloRank.SCHOLAR
    if elo >= 1100:
        return EloRank.AUTODIDACT
    if elo >= 1000:
        return EloRank.BEGINNER
    return EloRank.BASIC_KNOWLEDGE


def get_rank_color(rank: EloRank) -> str:
    return {
        EloRank.BASIC_KNOWLEDGE: "#6B7280",
        EloRank.BEGINNER: "#6B7280",
        EloRank.AUTODIDACT: "#3B82F6",
        EloRank.SCHOLAR: "#3B82F6",
        EloRank.LEARNER: "#06B6D4",
        EloRank.EXPERIENCED_LEARNER: "#06B6D4",
        EloRank.INTERMEDIATE: "#10B981",
        EloRank.EXPERIENCED_INTERMEDIATE: "#10B981",
        EloRank.EXPERT: "#F59E0B",
        EloRank.PROFESSIONAL: "#F59E0B",
        EloRank.AUTHORITY: "#EF4444",
        EloRank.MASTER_CANDIDATE: "#EF4444",
        EloRank.NATIONAL_MASTER: "#8B5CF6",
        EloRank.MASTER: "#8B5CF6",
        EloRank.INTERNATIONAL_MASTER: "#EC4899",
        EloRank.GRANDMASTER: "#EC4899",
        EloRank.WORLD_CLASS: "#F97316",
    }.get(rank, "#6B7280")


def expected_score(user_elo: int, puzzle_elo: int) -> float:
    return 1.0 / (1.0 + math.pow(10, (puzzle_elo - user_elo) / 400.0))


def get_elo_delta(user_elo: int, correct: bool, advanced: bool = False) -> int:
    table = ELO_DELTA_TABLE_ADVANCED if advanced else ELO_DELTA_TABLE
    for elo_min, elo_max, points_correct, points_incorrect in table:
        if elo_min <= user_elo < elo_max:
            return points_correct if correct else points_incorrect
    last_row = table[-1]
    return last_row[2] if correct else last_row[3]


def update_puzzle_elo(puzzle_elo: int, expected: float, actual_score: float, k: int = 32) -> int:
    delta = round(k * (actual_score - expected))
    return max(100, puzzle_elo + delta)


def process_attempt(user_elo: int, puzzle_elo: int, correct: bool, advanced: bool = False) -> EloResult:
    rank_before = get_rank(user_elo)
    probability = expected_score(user_elo, puzzle_elo)
    user_delta = get_elo_delta(user_elo, correct, advanced)
    puzzle_actual = 0.0 if correct else 1.0
    new_puzzle_elo = update_puzzle_elo(puzzle_elo, 1 - probability, puzzle_actual)
    puzzle_delta = new_puzzle_elo - puzzle_elo
    new_user_elo = max(0, user_elo + user_delta)
    rank_after = get_rank(new_user_elo)

    return EloResult(
        user_elo_before=user_elo,
        puzzle_elo_before=puzzle_elo,
        correct=correct,
        user_elo_after=new_user_elo,
        puzzle_elo_after=new_puzzle_elo,
        delta_user=user_delta,
        delta_puzzle=puzzle_delta,
        rank_before=rank_before,
        rank_after=rank_after,
        rank_changed=rank_before != rank_after,
        expected_probability=round(probability, 3),
    )


def win_probability_label(probability: float) -> str:
    if probability >= 0.85:
        return "Very likely to solve"
    if probability >= 0.65:
        return "Likely to solve"
    if probability >= 0.45:
        return "Even match"
    if probability >= 0.25:
        return "Challenging"
    return "Very challenging"
