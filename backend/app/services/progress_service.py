"""Servicio único de completitud de lecciones.

Fuente de verdad de "lección completada" y del porcentaje de progreso.
Se aplica en UN solo lugar (este módulo) y el resto del backend/frontend solo
lo consume. Regla:

- Un ejercicio cuenta como *hecho* cuando el usuario tiene al menos una
  ``CodeSubmission`` con ``result == "success"`` para ese ejercicio (dedup por
  ``exercise_id``: N submissions exitosas cuentan una sola vez).
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

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning import CodeSubmission, Exercise, UserProgress


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
            select(Exercise.id, Exercise.points).where(
                Exercise.lesson_id == lesson_id
            )
        )
    ).all()
    total = len(ex_rows)
    points_by_ex = {row[0]: (row[1] or 0) for row in ex_rows}

    completed_ids: set[int] = set()
    if ex_rows:
        sub_rows = (
            await db.execute(
                select(CodeSubmission.exercise_id)
                .where(
                    CodeSubmission.user_id == user_id,
                    CodeSubmission.exercise_id.in_(points_by_ex.keys()),
                    CodeSubmission.result == "success",
                )
                .distinct()
            )
        ).all()
        completed_ids = {row[0] for row in sub_rows}

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
        progress = UserProgress(
            user_id=user_id, lesson_id=lesson_id, started_at=now
        )
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
