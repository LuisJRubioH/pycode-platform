"""
Pydantic schemas for learning models.
"""

from typing import List, Optional, Any
from pydantic import BaseModel, field_validator
from datetime import datetime


class LessonListResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    difficulty: str
    category: Optional[str]
    track: str = "track-1"
    estimated_duration: int
    # Orden curricular dentro del track (Lesson.order).
    order: int = 0
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
    # "code" = se resuelve en el editor y lo valida Pyodide. Los tipos de
    # Track 0 (trace_table, predict_output, mcq...) los corrige el backend en
    # POST /exercises/{id}/check.
    exercise_type: str = "code"
    # Enunciado estructurado del ejercicio no-código. Público a propósito.
    # `answer_key` NO está aquí y no debe añadirse: hay un test de no-leak.
    spec: Optional[dict] = None
    # Derivado de las CodeSubmission del usuario (regla única de
    # progress_service). Nunca se persiste en la tabla Exercise.
    completed: bool = False

    @field_validator("spec")
    @classmethod
    def _spec_vacia_es_nula(cls, v: Optional[dict]) -> Optional[dict]:
        """Un ejercicio de código no tiene enunciado estructurado.

        En la tabla la columna nace como `{}`, y sin esto un endpoint
        devolvería `{}` y otro `None` para el mismo ejercicio.
        """
        return v or None

    class Config:
        from_attributes = True


class LessonResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    content: Optional[str]
    difficulty: str
    category: Optional[str]
    track: str = "track-1"
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


class ExerciseCheckRequest(BaseModel):
    """Respuesta del alumno a un ejercicio no-código de Track 0.

    La forma de `respuesta` depende del `exercise_type` (celdas de la traza,
    salida escrita, opción elegida). La valida `track0_service`, no el schema:
    así un tipo nuevo no toca la API.
    """

    respuesta: dict


class ExerciseCheckResponse(BaseModel):
    passed: bool
    # Dice DÓNDE falla, nunca cuál era el valor correcto.
    feedback: Optional[str] = None
    detalle: dict = {}
    # Si el ejercicio queda hecho tras este intento (o ya lo estaba).
    completed: bool = False
