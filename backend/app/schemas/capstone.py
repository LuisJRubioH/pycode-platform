"""
Pydantic schemas para endpoints de capstone.

`hidden_tests` jamás aparece en estos schemas — solo se expone vía un
endpoint dedicado al evaluador (mismo patrón que `exercises.hidden_tests`).
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CapstoneRequirement(BaseModel):
    id: str
    text: str


class CapstoneFile(BaseModel):
    path: str
    content: str
    editable: bool = True


class CapstoneSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: int
    slug: str
    track: str
    title: str
    short_description: str
    estimated_hours: int
    difficulty: str
    order_index: int
    # Marca del usuario actual.
    completed: bool = False


class CapstoneDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: int
    slug: str
    track: str
    title: str
    short_description: str
    description: str
    requirements: list[CapstoneRequirement]
    starter_files: list[CapstoneFile]
    tests_total: int
    estimated_hours: int
    difficulty: str
    order_index: int


class CapstoneListOut(BaseModel):
    items: list[CapstoneSummary]
    total: int


class CapstoneSubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: int
    capstone_id: int
    status: str
    tests_passed: int
    tests_total: int
    test_results: Optional[list[dict]] = None
    created_at: datetime
