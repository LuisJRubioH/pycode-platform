"""
Pydantic schemas for learning models.
"""

from typing import List, Optional, Any
from pydantic import BaseModel
from datetime import datetime


class LessonListResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    difficulty: str
    category: Optional[str]
    estimated_duration: int
    progress: int = 0
    status: str = "not_started"

    class Config:
        from_attributes = True


class ExerciseResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    description: Optional[str]
    instructions: Optional[str]
    starter_code: Optional[str]
    difficulty: str
    points: int
    order: int
    hints: List[str] = []

    class Config:
        from_attributes = True


class LessonResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    content: Optional[str]
    difficulty: str
    category: Optional[str]
    estimated_duration: int
    prerequisites: List[Any] = []
    exercises: List[ExerciseResponse] = []
    progress: int = 0
    status: str = "not_started"

    class Config:
        from_attributes = True


class CodeSubmissionCreate(BaseModel):
    exercise_id: int
    code: str
    success: bool = False
    output: Optional[str] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[int] = None
    passed_tests: int = 0
    total_tests: int = 0


class CodeSubmissionResponse(BaseModel):
    id: int
    exercise_id: int
    code: str
    result: str
    output: Optional[str]
    error_message: Optional[str]
    execution_time: Optional[int]
    passed_tests: int
    total_tests: int
    created_at: datetime

    class Config:
        from_attributes = True


class HiddenTest(BaseModel):
    name: str
    code: str


class HiddenTestsResponse(BaseModel):
    exercise_id: int
    tests: List[HiddenTest]


class ProgressUpdate(BaseModel):
    lesson_id: int
    progress: int
    status: str
    time_spent: int = 0


class ProgressResponse(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    status: str
    score: int
    time_spent: int
    attempts: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    progress: int

    class Config:
        from_attributes = True


class CompetencyLessonItem(BaseModel):
    """Lección dentro de una competencia (Track 1)."""

    id: int
    title: str
    difficulty: str
    completed: bool
    exercises_completed: int
    exercises_total: int


class CompetencyOut(BaseModel):
    """Competencia agregada por categoría con progreso del usuario actual."""

    category: str
    lessons_total: int
    lessons_completed: int
    exercises_total: int
    exercises_completed: int
    lessons: List[CompetencyLessonItem]


class TrackStatusItem(BaseModel):
    """Estado agregado de un Track para el usuario actual.

    El `certificate_unlocked` es la decision gate: queda True cuando
    `capstone_status == "passed"`. El certificado PDF en si se genera
    en una pieza posterior, pero la condicion de desbloqueo ya esta aqui.
    """

    track: str
    title: str
    lessons_total: int
    lessons_completed: int
    exercises_total: int
    exercises_completed: int
    capstone_slug: Optional[str] = None
    capstone_title: Optional[str] = None
    capstone_status: Optional[str] = None
    capstone_tests_passed: Optional[int] = None
    capstone_tests_total: Optional[int] = None
    certificate_unlocked: bool = False


class CodeQualityPoint(BaseModel):
    """Un punto de la progresión de calidad de código."""

    created_at: datetime
    logic_score: Optional[int] = None
    general_score: Optional[int] = None
    static_score: Optional[int] = None


class CodeQualitySummary(BaseModel):
    """Resumen agregado de la calidad de código del usuario."""

    count: int
    avg_logic: Optional[float] = None
    avg_general: Optional[float] = None
    avg_static: Optional[float] = None
    latest_static: Optional[int] = None


class CodeQualityProgressOut(BaseModel):
    points: List[CodeQualityPoint]
    summary: CodeQualitySummary
