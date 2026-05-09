"""Schemas para evaluación de código (Fase 1 — separación tutor/evaluador)."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EvaluationRequest(BaseModel):
    """Request para POST /api/v1/tutor/evaluate.

    `problem_description` es obligatorio: forzamos al alumno a escribir
    qué intenta hacer su código antes de pulsar Evaluar.
    """

    model_config = ConfigDict(extra="forbid")

    problem_description: str = Field(..., min_length=10, max_length=5000)
    code: str = Field(..., min_length=1, max_length=20000)
    expected_output: Optional[str] = Field(None, max_length=10000)
    actual_output: Optional[str] = Field(None, max_length=10000)
    exercise_id: Optional[int] = Field(None, gt=0)


class EvaluationVerdict(BaseModel):
    """Estructura del verdict guardado en la columna JSONB.

    `raw` contiene el texto completo devuelto por el LLM (formato
    socrático con CALIFICACION/PUNTOS FUERTES/AREAS DE MEJORA/
    RECOMENDACIONES). `logic_score` y `general_score` se extraen del
    raw cuando es posible y sirven para queries de progreso.
    """

    raw: str
    logic_score: Optional[int] = None
    general_score: Optional[int] = None


class EvaluationResponse(BaseModel):
    # `model_used` choca con el namespace protegido `model_` de Pydantic;
    # lo deshabilitamos explícitamente.
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: int
    created_at: datetime
    verdict: EvaluationVerdict
    model_used: Optional[str] = None
