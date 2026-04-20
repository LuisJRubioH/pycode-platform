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

    model_config = {"from_attributes": True}


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

    model_config = {"from_attributes": True}


class CodingChallengeListOut(BaseModel):
    items: list[CodingChallengeSummary]
    total: int
    recommended_difficulty: str
