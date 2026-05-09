"""Servicio de evaluación socrática de código (Fase 1).

Atómico: una llamada al LLM por evaluación, sin historial conversacional.
Independiente del tutor de Q&A (`AITutorService`), aunque por ahora
comparte el mismo system prompt evaluador.
"""

# flake8: noqa: E501

import re
from typing import Optional

import structlog

from app.schemas.evaluation import EvaluationRequest, EvaluationVerdict
from app.services.ai_tutor import AITutorService
from app.services.llm_provider import StubProvider

logger = structlog.get_logger()


_LOGIC_RE = re.compile(r"L[oó]gica\s*:?\s*(\d{1,3})\s*/\s*100", re.IGNORECASE)
_GENERAL_RE = re.compile(
    r"Soluci[oó]n\s*General\s*:?\s*(\d{1,3})\s*/\s*100", re.IGNORECASE
)


def _extract_score(pattern: re.Pattern[str], text: str) -> Optional[int]:
    match = pattern.search(text)
    if not match:
        return None
    try:
        value = int(match.group(1))
    except ValueError:
        return None
    return value if 0 <= value <= 100 else None


class EvaluationService:
    """Wrapper alrededor de AITutorService que devuelve un verdict atómico."""

    def __init__(self, tutor: Optional[AITutorService] = None):
        self.tutor = tutor or AITutorService()

    @property
    def model_used(self) -> Optional[str]:
        provider = self.tutor.provider
        if isinstance(provider, StubProvider):
            return "stub"
        # Provedores reales tienen `.model`; lo exponen para telemetria.
        return getattr(provider, "model", None)

    async def evaluate(self, payload: EvaluationRequest) -> EvaluationVerdict:
        """Ejecuta la evaluación y devuelve el verdict listo para persistir."""
        context = {
            "problem_description": payload.problem_description,
            "student_code": payload.code,
            "expected_output": payload.expected_output,
            "actual_output": payload.actual_output,
            "level": "beginner",
        }
        message = (
            "Evalúa este intento siguiendo el formato CALIFICACION / PUNTOS "
            "FUERTES / AREAS DE MEJORA / RECOMENDACIONES."
        )
        raw = await self.tutor.get_response(message, context)
        return EvaluationVerdict(
            raw=raw,
            logic_score=_extract_score(_LOGIC_RE, raw),
            general_score=_extract_score(_GENERAL_RE, raw),
        )
