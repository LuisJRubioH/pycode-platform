"""
AI Tutor Service with OpenAI integration and a code-evaluation Socratic style.
"""

from pathlib import Path
from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings


class AITutorService:
    """AI tutor service that evaluates beginner Python code without giving full solutions."""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.system_prompt = self._load_system_prompt()

    async def get_response(self, message: str, context: dict | None = None) -> str:
        """Get a response from the tutor using the configured prompt and structured context."""
        normalized_context = self._normalize_context(context)

        if not self.client:
            return self._get_fallback_response(message, normalized_context)

        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"{self._build_context(normalized_context)}\n\n"
                        f"Consulta o comentario del estudiante:\n{message.strip()}"
                    ).strip(),
                },
            ]

            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=700,
                temperature=0.4,
            )

            content = response.choices[0].message.content or ""
            return content.strip() or self._get_fallback_response(message, normalized_context)

        except Exception as exc:
            print(f"Error calling OpenAI: {exc}")
            return self._get_fallback_response(message, normalized_context)

    def _load_system_prompt(self) -> str:
        """Load the tutor prompt from the configured file with a safe local fallback."""
        fallback_prompt = (
            "Actua como un maestro experto en Python especializado en evaluacion de codigo "
            "para principiantes. Nunca entregues la solucion completa. Evalua lo que el "
            "problema pide, usa tono alentador, enfocate en pocos conceptos clave y guia "
            "con preguntas socraticas."
        )

        prompt_path = Path(settings.tutor_prompt_path)
        try:
            prompt_text = prompt_path.read_text(encoding="utf-8").strip()
            if prompt_text:
                return prompt_text
        except OSError:
            pass

        return fallback_prompt

    def _normalize_context(self, context: dict[str, Any] | None) -> dict[str, Any]:
        """Normalize incoming context so different clients can send equivalent keys."""
        if not context:
            return {}

        aliases = {
            "problem_description": ("problem_description", "problem", "exercise", "enunciado"),
            "student_code": ("student_code", "code", "currentCode", "codigo"),
            "expected_output": ("expected_output", "expected", "expectedOutput"),
            "actual_output": ("actual_output", "output", "actualOutput"),
            "current_lesson": ("current_lesson", "currentLesson", "lesson"),
            "level": ("level", "student_level", "nivel"),
            "attempt_count": ("attempt_count", "attemptCount", "tries", "intentos"),
            "recent_errors": ("recent_errors", "recentErrors", "errors"),
            "weaknesses": ("weaknesses", "topics", "debilidades"),
        }

        normalized: dict[str, Any] = {}
        for canonical_key, possible_keys in aliases.items():
            for key in possible_keys:
                value = context.get(key)
                if value not in (None, "", [], {}):
                    normalized[canonical_key] = value
                    break

        for key, value in context.items():
            if key not in normalized and value not in (None, "", [], {}):
                normalized[key] = value

        return normalized

    def _build_context(self, context: dict[str, Any] | None = None) -> str:
        """Build the structured prompt context for the tutor."""
        if not context:
            return (
                "Contexto disponible:\n"
                "- Nivel del estudiante: beginner\n"
                "- Si falta el enunciado o el codigo, pide esos datos antes de evaluar."
            )

        context_parts = [f"- Nivel del estudiante: {context.get('level', 'beginner')}"]

        current_lesson = context.get("current_lesson")
        if current_lesson:
            context_parts.append(f"- Leccion o tema actual: {current_lesson}")

        attempt_count = context.get("attempt_count")
        if attempt_count is not None:
            context_parts.append(f"- Intentos acumulados en este problema: {attempt_count}")

        recent_errors = context.get("recent_errors")
        if recent_errors:
            if isinstance(recent_errors, list):
                context_parts.append(f"- Errores recientes: {', '.join(map(str, recent_errors))}")
            else:
                context_parts.append(f"- Errores recientes: {recent_errors}")

        weaknesses = context.get("weaknesses")
        if weaknesses:
            if isinstance(weaknesses, list):
                context_parts.append(f"- Debilidades detectadas: {', '.join(map(str, weaknesses))}")
            else:
                context_parts.append(f"- Debilidades detectadas: {weaknesses}")

        problem_description = context.get("problem_description")
        if problem_description:
            context_parts.append(f"\nEnunciado del problema:\n{problem_description}")

        student_code = context.get("student_code")
        if student_code:
            context_parts.append(f"\nCodigo del estudiante:\n```python\n{student_code}\n```")

        expected_output = context.get("expected_output")
        if expected_output:
            context_parts.append(f"\nSalida esperada o criterio objetivo:\n{expected_output}")

        actual_output = context.get("actual_output")
        if actual_output:
            context_parts.append(f"\nSalida actual del estudiante:\n{actual_output}")

        return "Contexto disponible:\n" + "\n".join(context_parts)

    def _get_fallback_response(self, message: str, context: dict[str, Any] | None = None) -> str:
        """Return a deterministic response when the model is unavailable."""
        problem_description = (context or {}).get("problem_description")
        student_code = (context or {}).get("student_code")
        actual_output = (context or {}).get("actual_output")
        expected_output = (context or {}).get("expected_output")

        if not problem_description or not student_code:
            return (
                "CALIFICACION:\n"
                "- Logica: 0/100 (aun no puedo evaluarla sin el enunciado y el codigo del estudiante)\n"
                "- Solucion General: 0/100 (necesito mas contexto para hacer una revision justa)\n\n"
                "ANALISIS DETALLADO:\n\n"
                "PUNTOS FUERTES:\n"
                "- Estas pidiendo retroalimentacion antes de seguir avanzando.\n"
                "- Hay intencion de aprender el razonamiento, no solo copiar una solucion.\n\n"
                "AREAS DE MEJORA:\n"
                "- Comparte el enunciado exacto del problema.\n"
                "- Comparte tambien tu codigo actual para poder revisar logica y claridad.\n\n"
                "RECOMENDACIONES:\n"
                "- Que resultado exacto te pide el ejercicio?\n"
                "- Que parte de tu intento sientes que funciona y cual te genera duda?\n"
            )

        matches_expected_output = (
            actual_output is not None
            and expected_output is not None
            and str(actual_output).strip() == str(expected_output).strip()
        )
        logic_score = 75 if matches_expected_output else 60
        general_score = 78 if len(student_code.splitlines()) <= 25 else 70
        output_note = ""
        if actual_output is not None and expected_output is not None:
            output_note = (
                f" La salida actual es `{actual_output}` y la esperada es `{expected_output}`."
            )

        return (
            "CALIFICACION:\n"
            f"- Logica: {logic_score}/100 (estimacion inicial basada en el contexto disponible.{output_note})\n"
            f"- Solucion General: {general_score}/100 (estimacion inicial segun claridad y tamano de la solucion)\n\n"
            "ANALISIS DETALLADO:\n\n"
            "PUNTOS FUERTES:\n"
            "- Ya hay una propuesta concreta de solucion para analizar.\n"
            "- Estas buscando mejorar tanto la logica como la claridad del codigo.\n\n"
            "AREAS DE MEJORA:\n"
            "- Revisa si cada parte del codigo responde exactamente a lo que pide el enunciado.\n"
            "- Valida al menos un caso borde adicional para confirmar que la solucion generaliza.\n\n"
            "RECOMENDACIONES:\n"
            "- Que pasaria si pruebas tu solucion con un caso pequeno y otro extremo?\n"
            "- Que nombres o estructuras podrias ajustar para que tu idea se entienda mas rapido?\n"
        )


tutor_service = AITutorService()
