"""
AI Tutor Service with OpenAI integration and a code-evaluation Socratic style.
"""

# flake8: noqa: E501 -- prompts y respuestas del tutor en espanol; partir las cadenas degrada la salida visible al usuario.

from pathlib import Path
from typing import Any

import structlog

from app.core.config import settings
from app.services.llm_provider import StubProvider, get_provider

logger = structlog.get_logger()


class AITutorService:
    """AI tutor service that evaluates beginner Python code without giving full solutions."""

    def __init__(self):
        self.provider = get_provider(settings)
        self.system_prompt = self._load_system_prompt()

    async def get_response(self, message: str, context: dict | None = None) -> str:
        """Get a response from the tutor using the configured prompt and structured context."""
        normalized_context = self._normalize_context(context)

        if isinstance(self.provider, StubProvider):
            return self._get_fallback_response(message, normalized_context)

        try:
            user_block = (
                f"{self._build_context(normalized_context)}\n\n"
                f"Consulta o comentario del estudiante:\n{message.strip()}"
            ).strip()
            content = await self.provider.chat(
                system=self.system_prompt,
                user=user_block,
                max_tokens=700,
                temperature=0.4,
            )
            return content.strip() or self._get_fallback_response(
                message, normalized_context
            )

        except Exception as exc:
            logger.error("llm.call_failed", error=str(exc))
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
            "problem_description": (
                "problem_description",
                "problem",
                "exercise",
                "enunciado",
            ),
            "student_code": ("student_code", "code", "currentCode", "codigo"),
            "expected_output": ("expected_output", "expected", "expectedOutput"),
            "actual_output": ("actual_output", "output", "actualOutput"),
            "current_lesson": ("current_lesson", "currentLesson", "lesson"),
            "level": ("level", "student_level", "nivel"),
            "attempt_count": ("attempt_count", "attemptCount", "tries", "intentos"),
            "recent_errors": ("recent_errors", "recentErrors", "errors"),
            "weaknesses": ("weaknesses", "topics", "debilidades"),
            "track": ("track", "pista"),
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

    #: Track 0 no enseña Python: el alumno razona algoritmos en pseudocodigo.
    #: Sin esto el tutor le corrige sintaxis que nadie le ha enseñado todavia,
    #: que es justo lo que `docs/TRACK_0.md` pide evitar.
    _INSTRUCCIONES_TRACK_0 = (
        "IMPORTANTE - este estudiante esta en Track 0 (Fundamentos), donde "
        "todavia NO se programa en Python:\n"
        "- Lo que ves abajo es PSEUDOCODIGO o una tabla de traza, no codigo "
        "Python. No lo corrijas como si lo fuera y no menciones sintaxis de "
        "Python (dos puntos, sangria, print, len...).\n"
        "- Pregunta por la TRAZA: cuanto vale una variable en una vuelta "
        "concreta, que condicion hizo que el bucle terminara, que rama del Si "
        "se tomo con esos datos.\n"
        "- La notacion es: `<-` asigna, `=` compara, `Si/Entonces/SiNo/FinSi`, "
        "`Mientras/Hacer/FinMientras`, `Para <- Hasta Hacer/FinPara`, "
        "`Escribir`, `Leer`, `Longitud(v)`, y los arreglos empiezan en 0.\n"
        "- No le des la respuesta: devuelvele una pregunta que le haga seguir "
        "el algoritmo a mano hasta el punto donde se equivoco."
    )

    def _build_context(self, context: dict[str, Any] | None = None) -> str:
        """Build the structured prompt context for the tutor."""
        if not context:
            return (
                "Contexto disponible:\n"
                "- Nivel del estudiante: beginner\n"
                "- Si falta el enunciado o el codigo, pide esos datos antes de evaluar."
            )

        es_track_0 = str(context.get("track") or "").strip() == "track-0"

        context_parts = [f"- Nivel del estudiante: {context.get('level', 'beginner')}"]
        if es_track_0:
            context_parts.append("- Track: 0 (Fundamentos, en pseudocodigo)")

        current_lesson = context.get("current_lesson")
        if current_lesson:
            context_parts.append(f"- Leccion o tema actual: {current_lesson}")

        attempt_count = context.get("attempt_count")
        if attempt_count is not None:
            context_parts.append(
                f"- Intentos acumulados en este problema: {attempt_count}"
            )

        recent_errors = context.get("recent_errors")
        if recent_errors:
            if isinstance(recent_errors, list):
                context_parts.append(
                    f"- Errores recientes: {', '.join(map(str, recent_errors))}"
                )
            else:
                context_parts.append(f"- Errores recientes: {recent_errors}")

        weaknesses = context.get("weaknesses")
        if weaknesses:
            if isinstance(weaknesses, list):
                context_parts.append(
                    f"- Debilidades detectadas: {', '.join(map(str, weaknesses))}"
                )
            else:
                context_parts.append(f"- Debilidades detectadas: {weaknesses}")

        problem_description = context.get("problem_description")
        if problem_description:
            context_parts.append(f"\nEnunciado del problema:\n{problem_description}")

        student_code = context.get("student_code")
        if student_code:
            if es_track_0:
                context_parts.append(
                    "\nLo que tiene delante el estudiante (pseudocodigo, NO "
                    f"Python):\n```\n{student_code}\n```"
                )
            else:
                context_parts.append(
                    f"\nCodigo del estudiante:\n```python\n{student_code}\n```"
                )

        expected_output = context.get("expected_output")
        if expected_output:
            context_parts.append(
                f"\nSalida esperada o criterio objetivo:\n{expected_output}"
            )

        actual_output = context.get("actual_output")
        if actual_output:
            context_parts.append(f"\nSalida actual del estudiante:\n{actual_output}")

        cabecera = (
            f"{self._INSTRUCCIONES_TRACK_0}\n\nContexto disponible:\n"
            if es_track_0
            else "Contexto disponible:\n"
        )
        return cabecera + "\n".join(context_parts)

    def _get_fallback_response(
        self, message: str, context: dict[str, Any] | None = None
    ) -> str:
        """Return a deterministic response when the model is unavailable."""
        problem_description = (context or {}).get("problem_description")
        student_code = (context or {}).get("student_code")

        # En Track 0 no hay codigo que puntuar: el alumno esta siguiendo un
        # algoritmo a mano. Devolverle una CALIFICACION con notas sobre
        # "claridad del codigo" no solo no ayuda, es que habla de otra cosa.
        if str((context or {}).get("track") or "").strip() == "track-0":
            return (
                "Vamos a seguirlo juntos, sin mirar la respuesta.\n\n"
                "- Empieza por el estado inicial: que valor tiene cada variable "
                "ANTES de entrar al bucle?\n"
                "- Haz una vuelta entera a mano y anota los valores al terminarla. "
                "Coinciden con lo que esperabas?\n"
                "- Mira la condicion: que tendria que pasar para que dejara de "
                "ser cierta, y que linea de dentro lo acerca?\n\n"
                "Cuando llegues a la primera fila donde tu tabla y el algoritmo "
                "no coinciden, ahi esta el fallo. Cuentame que encuentras."
            )
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
            output_note = f" La salida actual es `{actual_output}` y la esperada es `{expected_output}`."

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
