"""Servicio único de completitud de lecciones.

Fuente de verdad de "lección completada" y del porcentaje de progreso.
Se aplica en UN solo lugar (este módulo) y el resto del backend/frontend solo
lo consume. Regla:

- Un ejercicio cuenta como *hecho* cuando el usuario tiene al menos una
  ``CodeSubmission`` con ``result == "success"`` para ese ejercicio (dedup por
  ``exercise_id``: N submissions exitosas cuentan una sola vez). Esa regla vive
  en ``completed_exercise_ids`` y **nadie la reimplementa**: la llaman este
  módulo, ``GET /lessons/{id}`` y ``GET /exercises/lesson/{id}``.
- ``progress`` (0-100) = ejercicios_hechos / ejercicios_totales de la lección.
- ``status`` = ``"completed"`` cuando *todos* los ejercicios de la lección
  están hechos; ``"in_progress"`` en cualquier otro caso una vez que hay fila.
- ``score`` = Σ ``points`` de los ejercicios hechos. Es un valor **derivado**
  (no un acumulador), así reintentar un ejercicio ya aprobado nunca duplica XP.

Nota de contenido: dos lecciones puramente conceptuales ("Testing con pytest"
y "Modulos, Paquetes y Entornos") tienen su único ejercicio SIN ``hidden_tests``,
por lo que el cliente nunca puede reportar ``success`` y no se auto-completan
(quedan en 0% / in_progress). Es una deuda de contenido: necesitan
``hidden_tests`` para poder cerrarse (pendiente Bloque 4).
"""

from datetime import datetime
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning import CodeSubmission, Exercise, UserProgress


async def completed_exercise_ids(
    db: AsyncSession, user_id: int, exercise_ids: Iterable[int]
) -> set[int]:
    """Cuáles de ``exercise_ids`` tiene *hechos* ``user_id``.

    Fuente de verdad única de "ejercicio completado": al menos una
    ``CodeSubmission`` con ``result == "success"``, deduplicado por
    ``exercise_id``. Un intento fallido posterior a uno exitoso NO lo
    des-completa.

    Cualquier endpoint que necesite el flag debe llamar aquí en vez de
    repetir la query: si la regla cambia (p. ej. ejercicios opcionales),
    cambia en un solo sitio.
    """
    ids = list(exercise_ids)
    if not ids:
        return set()
    rows = (
        await db.execute(
            select(CodeSubmission.exercise_id)
            .where(
                CodeSubmission.user_id == user_id,
                CodeSubmission.exercise_id.in_(ids),
                CodeSubmission.result == "success",
            )
            .distinct()
        )
    ).all()
    return {row[0] for row in rows}


async def recompute_lesson_progress(
    db: AsyncSession, user_id: int, lesson_id: int
) -> UserProgress:
    """Recalcula y persiste el progreso de ``user_id`` en ``lesson_id``.

    Crea la fila ``UserProgress`` si no existe. Idempotente: llamarla N veces
    con el mismo estado de submissions produce el mismo resultado. No hace
    commit (lo decide el caller).
    """
    ex_rows = (
        await db.execute(
            select(Exercise.id, Exercise.points).where(Exercise.lesson_id == lesson_id)
        )
    ).all()
    total = len(ex_rows)
    points_by_ex = {row[0]: (row[1] or 0) for row in ex_rows}

    completed_ids = await completed_exercise_ids(db, user_id, points_by_ex.keys())

    completed = len(completed_ids)
    score = sum(points_by_ex[eid] for eid in completed_ids)
    pct = 0 if total == 0 else round(completed / total * 100)
    is_complete = total > 0 and completed == total

    progress = (
        await db.execute(
            select(UserProgress).where(
                UserProgress.user_id == user_id,
                UserProgress.lesson_id == lesson_id,
            )
        )
    ).scalar_one_or_none()

    now = datetime.utcnow()
    if progress is None:
        progress = UserProgress(user_id=user_id, lesson_id=lesson_id, started_at=now)
        db.add(progress)

    progress.score = score
    progress.progress = pct
    progress.last_accessed = now
    if is_complete:
        progress.status = "completed"
        if progress.completed_at is None:
            progress.completed_at = now
    else:
        progress.status = "in_progress"

    return progress
