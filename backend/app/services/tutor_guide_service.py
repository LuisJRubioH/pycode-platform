"""Tutor de Q&A multi-turn (Fase 1).

Distinto del AITutorService (que es el evaluador): este responde dudas
conceptuales sin asumir que hay código del estudiante adjunto. Mantiene
historial conversacional dentro de una sesión.
"""

# flake8: noqa: E501

from pathlib import Path
from typing import Iterable

import structlog

from app.core.config import settings
from app.services.llm_provider import StubProvider, get_provider

logger = structlog.get_logger()


_FALLBACK_PROMPT = (
    "Eres un tutor de Python para principiantes en español. Responde "
    "dudas conceptuales con claridad, ejemplos cortos y tono cálido. "
    "No evalúas código (eso vive en otro endpoint)."
)

# Cap defensivo del historial para evitar prompts gigantes y costo
# desproporcionado. Mantenemos los últimos N pares pregunta/respuesta.
_HISTORY_TURN_CAP = 12


class TutorGuideService:
    def __init__(self):
        self.provider = get_provider(settings)
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        prompt_path = Path(settings.tutor_guide_prompt_path)
        try:
            text = prompt_path.read_text(encoding="utf-8").strip()
            if text:
                return text
        except OSError:
            pass
        return _FALLBACK_PROMPT

    @staticmethod
    def _format_history(history: Iterable[dict]) -> str:
        """Aplana el historial a un bloque de texto consumible por el LLM.

        Cada entrada del historial tiene shape `{"role": "user"|"bot",
        "content": str}`. Se ignoran entradas con role distinto.
        """
        lines: list[str] = []
        for turn in history:
            role = turn.get("role")
            content = (turn.get("content") or "").strip()
            if not content:
                continue
            if role == "user":
                lines.append(f"Estudiante: {content}")
            elif role == "bot":
                lines.append(f"Tutor: {content}")
        return "\n\n".join(lines)

    async def reply(self, history: list[dict], message: str) -> str:
        """Genera la siguiente respuesta del tutor.

        `history` contiene los turns previos (excluye el `message` actual).
        Devuelve el texto de respuesta del tutor.
        """
        message = message.strip()
        if not message:
            return "Cuéntame tu pregunta concreta sobre Python para poder ayudarte."

        if isinstance(self.provider, StubProvider):
            return self._fallback_response(message)

        recent_history = list(history)[-_HISTORY_TURN_CAP * 2 :]
        history_block = self._format_history(recent_history)

        if history_block:
            user_prompt = (
                f"Conversación previa:\n{history_block}\n\n"
                f"Estudiante (turno actual):\n{message}"
            )
        else:
            user_prompt = f"Estudiante:\n{message}"

        try:
            content = await self.provider.chat(
                system=self.system_prompt,
                user=user_prompt,
                max_tokens=600,
                temperature=0.5,
            )
        except Exception as exc:
            logger.error("tutor_guide.call_failed", error=str(exc))
            return self._fallback_response(message)

        cleaned = content.strip()
        return cleaned or self._fallback_response(message)

    @staticmethod
    def _fallback_response(message: str) -> str:
        return (
            "No tengo conexión con el modelo en este momento, pero puedo "
            "intentar guiarte con preguntas: ¿qué parte de "
            f'"{message[:80]}" sientes que no te queda claro y qué has '
            "intentado hasta ahora?"
        )
