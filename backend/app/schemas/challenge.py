"""
Pydantic schemas for coding challenge endpoints.
"""

from pydantic import BaseModel


class CodingChallengeSummary(BaseModel):
    id: int
    title: str
    slug: str
    source: str
    difficulty: str
    topic: str
    prompt_preview: str
    order_index: int
    # Marca manual del user actual (Fase 1, completaciones).
    completed: bool = False
    # 1, 2 o 3 si el reto es un nivel de un problema con progresion; None si
    # es un reto suelto (los curados).
    level: int | None = None

    model_config = {"from_attributes": True}


class ChallengeLevel(BaseModel):
    """Uno de los niveles del mismo problema, para pintar la progresion."""

    id: int
    level: int
    difficulty: str
    completed: bool = False


class CodingChallengeDetail(BaseModel):
    id: int
    title: str
    slug: str
    source: str
    source_path: str
    difficulty: str
    topic: str
    prompt: str
    starter_code: str
    order_index: int
    level: int | None = None
    # Los niveles del mismo problema (incluido este), en orden. Vacio en retos
    # sueltos.
    levels: list[ChallengeLevel] = []

    model_config = {"from_attributes": True}


class CodingChallengeListOut(BaseModel):
    items: list[CodingChallengeSummary]
    total: int
    recommended_difficulty: str
