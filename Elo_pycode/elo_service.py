"""
Sistema ELO para PyCode Platform
Basado en la metodología de Coffee Break Python / Finxter (Christian Mayer)

Filosofía:
- Usuario y puzzle tienen rating ELO independiente
- Ganar contra puzzle difícil → mucho ELO
- Ganar contra puzzle fácil → poco ELO
- Perder contra puzzle fácil → mucho ELO perdido
- Perder contra puzzle difícil → poco ELO perdido
"""

from dataclasses import dataclass
from enum import Enum
import math


# ─── Ranks según tabla de Coffee Break Python ─────────────────────────────────

class EloRank(str, Enum):
    BASIC_KNOWLEDGE      = "Basic Knowledge"
    BEGINNER             = "Beginner"
    AUTODIDACT           = "Autodidact"
    SCHOLAR              = "Scholar"
    LEARNER              = "Learner"
    EXPERIENCED_LEARNER  = "Experienced Learner"
    INTERMEDIATE         = "Intermediate"
    EXPERIENCED_INTER    = "Experienced Intermediate"
    EXPERT               = "Expert"
    PROFESSIONAL         = "Professional"
    AUTHORITY            = "Authority"
    MASTER_CANDIDATE     = "Master Candidate"
    NATIONAL_MASTER      = "National Master"
    MASTER               = "Master"
    INTL_MASTER          = "International Master"
    GRANDMASTER          = "Grandmaster"
    WORLD_CLASS          = "World Class"


# ─── Tabla de puntos ELO por rango del usuario ────────────────────────────────
# Extraída directamente de Coffee Break Python y Coffee Break NumPy
# Formato: (elo_min, elo_max, puntos_correcto, puntos_incorrecto)

ELO_DELTA_TABLE = [
    (0,    500,  43, -12),
    (500,  1000, 21, -34),
    (1000, 1500,  9, -46),
    (1500, 2000,  8, -47),
    (2000, 9999,  8, -47),
]

# Tabla extendida para puzzles avanzados (NumPy/Pandas style — más granular)
ELO_DELTA_TABLE_ADVANCED = [
    (0,    1500, 60,  -4),
    (1500, 1600, 56,  -8),
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
    """Resultado de una interacción usuario ↔ puzzle"""
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
    expected_probability: float   # probabilidad de que usuario resuelva el puzzle


# ─── Funciones núcleo ─────────────────────────────────────────────────────────

def get_rank(elo: int) -> EloRank:
    """Devuelve el rank según el ELO actual (tabla Coffee Break Python)"""
    if elo >= 2500: return EloRank.WORLD_CLASS
    if elo >= 2400: return EloRank.GRANDMASTER
    if elo >= 2300: return EloRank.INTL_MASTER
    if elo >= 2200: return EloRank.MASTER
    if elo >= 2100: return EloRank.NATIONAL_MASTER
    if elo >= 2000: return EloRank.MASTER_CANDIDATE
    if elo >= 1900: return EloRank.AUTHORITY
    if elo >= 1800: return EloRank.PROFESSIONAL
    if elo >= 1700: return EloRank.EXPERT
    if elo >= 1600: return EloRank.EXPERIENCED_INTER
    if elo >= 1500: return EloRank.INTERMEDIATE
    if elo >= 1400: return EloRank.EXPERIENCED_LEARNER
    if elo >= 1300: return EloRank.LEARNER
    if elo >= 1200: return EloRank.SCHOLAR
    if elo >= 1100: return EloRank.AUTODIDACT
    if elo >= 1000: return EloRank.BEGINNER
    return EloRank.BASIC_KNOWLEDGE


def get_rank_color(rank: EloRank) -> str:
    """Color hex para el rank (para el frontend)"""
    colors = {
        EloRank.BASIC_KNOWLEDGE:     "#6B7280",
        EloRank.BEGINNER:            "#6B7280",
        EloRank.AUTODIDACT:          "#3B82F6",
        EloRank.SCHOLAR:             "#3B82F6",
        EloRank.LEARNER:             "#06B6D4",
        EloRank.EXPERIENCED_LEARNER: "#06B6D4",
        EloRank.INTERMEDIATE:        "#10B981",
        EloRank.EXPERIENCED_INTER:   "#10B981",
        EloRank.EXPERT:              "#F59E0B",
        EloRank.PROFESSIONAL:        "#F59E0B",
        EloRank.AUTHORITY:           "#EF4444",
        EloRank.MASTER_CANDIDATE:    "#EF4444",
        EloRank.NATIONAL_MASTER:     "#8B5CF6",
        EloRank.MASTER:              "#8B5CF6",
        EloRank.INTL_MASTER:         "#EC4899",
        EloRank.GRANDMASTER:         "#EC4899",
        EloRank.WORLD_CLASS:         "#F97316",
    }
    return colors.get(rank, "#6B7280")


def expected_score(user_elo: int, puzzle_elo: int) -> float:
    """
    Probabilidad esperada de que el usuario resuelva el puzzle.
    Fórmula estándar ELO (Elo 1978).
    """
    return 1.0 / (1.0 + math.pow(10, (puzzle_elo - user_elo) / 400.0))


def get_elo_delta(user_elo: int, correct: bool, advanced: bool = False) -> int:
    """
    Devuelve los puntos a sumar/restar según el ELO actual del usuario.
    Implementación directa de las tablas de Coffee Break Python/NumPy.
    """
    table = ELO_DELTA_TABLE_ADVANCED if advanced else ELO_DELTA_TABLE
    for elo_min, elo_max, pts_correct, pts_incorrect in table:
        if elo_min <= user_elo < elo_max:
            return pts_correct if correct else pts_incorrect
    # fallback para bordes
    last = table[-1]
    return last[2] if correct else last[3]


def update_puzzle_elo(puzzle_elo: int, expected: float, actual_score: float, k: int = 32) -> int:
    """
    Actualiza el ELO del puzzle usando la fórmula estándar.
    actual_score: 1.0 si el usuario FALLÓ (puzzle ganó), 0.0 si el usuario acertó.
    K=32 es el factor estándar para partidas online.
    """
    delta = round(k * (actual_score - expected))
    return max(100, puzzle_elo + delta)  # piso de 100 para evitar puzzles con ELO 0


def process_attempt(
    user_elo: int,
    puzzle_elo: int,
    correct: bool,
    advanced: bool = False,
) -> EloResult:
    """
    Procesa un intento del usuario en un puzzle y devuelve el resultado completo.

    Args:
        user_elo:   ELO actual del usuario
        puzzle_elo: ELO actual del puzzle
        correct:    True si el usuario resolvió correctamente
        advanced:   True para puzzles NumPy/Pandas (tabla extendida)

    Returns:
        EloResult con todos los deltas y el nuevo estado
    """
    rank_before = get_rank(user_elo)

    # Probabilidad esperada de éxito
    prob = expected_score(user_elo, puzzle_elo)

    # Delta del usuario (tabla Finxter)
    user_delta = get_elo_delta(user_elo, correct, advanced)

    # Delta del puzzle (fórmula estándar — el puzzle "juega" contra el usuario)
    # Si el usuario acertó → puzzle perdió → score del puzzle = 0
    puzzle_actual = 0.0 if correct else 1.0
    new_puzzle_elo = update_puzzle_elo(puzzle_elo, 1 - prob, puzzle_actual)
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
        rank_changed=(rank_before != rank_after),
        expected_probability=round(prob, 3),
    )


def initial_elo(level: str = "beginner") -> int:
    """
    ELO inicial según nivel autodeclarado del usuario.
    Igual que recomienda Coffee Break Python.
    """
    return {"beginner": 1000, "intermediate": 1500, "advanced": 2000}.get(level, 1000)


def puzzle_difficulty_label(puzzle_elo: int) -> str:
    """Etiqueta de dificultad del puzzle según su ELO"""
    if puzzle_elo < 800:   return "Introductory"
    if puzzle_elo < 1100:  return "Easy"
    if puzzle_elo < 1400:  return "Medium"
    if puzzle_elo < 1700:  return "Hard"
    if puzzle_elo < 2000:  return "Expert"
    return "Master"


def win_probability_label(prob: float) -> str:
    """Descripción legible de la probabilidad de éxito"""
    if prob >= 0.85: return "Very likely to solve"
    if prob >= 0.65: return "Likely to solve"
    if prob >= 0.45: return "Even match"
    if prob >= 0.25: return "Challenging"
    return "Very challenging"
