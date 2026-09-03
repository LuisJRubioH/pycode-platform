"""Tests del script de backfill del progreso legacy.

El script se ejecutó una vez contra producción vía SQL; estos tests fijan su
comportamiento para que siga siendo fiable la próxima vez que haga falta
recalcular filas de ``UserProgress`` desincronizadas.

Dos garantías:
- sin ``--apply`` NO escribe nada (simulación con rollback);
- con ``--apply`` deja el mismo valor que ``recompute_lesson_progress``.
"""

import importlib.util
import pathlib

import pytest
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.learning import Exercise, Lesson, UserProgress

_SCRIPT = (
    pathlib.Path(__file__).resolve().parents[1]
    / "scripts"
    / "backfill_legacy_progress.py"
)
_spec = importlib.util.spec_from_file_location("backfill_legacy_progress", _SCRIPT)
backfill = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(backfill)


async def _seed_legacy_row(num_exercises: int, aprobados: int, user_id: int):
    """Crea una lección + una fila UserProgress con el sentinel legacy."""
    from app.models.learning import CodeSubmission

    async with async_session_maker() as session:
        lesson = Lesson(title=f"Backfill {user_id}", description="d", content="c")
        session.add(lesson)
        await session.flush()

        ex_ids = []
        for i in range(num_exercises):
            ex = Exercise(
                lesson_id=lesson.id,
                title=f"Ej {i}",
                description="d",
                instructions="i",
                starter_code="pass",
                points=10,
                difficulty="easy",
                order=i,
            )
            session.add(ex)
            await session.flush()
            ex_ids.append(ex.id)

        for ex_id in ex_ids[:aprobados]:
            session.add(
                CodeSubmission(
                    user_id=user_id,
                    exercise_id=ex_id,
                    code="ok",
                    result="success",
                    passed_tests=1,
                    total_tests=1,
                )
            )

        # La fila legacy: el 5% fijo que escribía el código viejo, sin
        # relación con los ejercicios realmente aprobados.
        session.add(
            UserProgress(
                user_id=user_id,
                lesson_id=lesson.id,
                progress=backfill.LEGACY_SENTINEL,
                status="in_progress",
                score=0,
            )
        )
        await session.commit()
        return lesson.id


async def _read_row(user_id: int, lesson_id: int) -> UserProgress:
    async with async_session_maker() as session:
        return (
            await session.execute(
                select(UserProgress).where(
                    UserProgress.user_id == user_id,
                    UserProgress.lesson_id == lesson_id,
                )
            )
        ).scalar_one()


@pytest.mark.asyncio
async def test_sin_apply_no_escribe_nada():
    """La simulación imprime el recálculo pero hace rollback."""
    user_id = 90001
    lesson_id = await _seed_legacy_row(num_exercises=2, aprobados=1, user_id=user_id)

    afectadas = await backfill.report(apply=False)
    assert afectadas >= 1

    row = await _read_row(user_id, lesson_id)
    assert row.progress == backfill.LEGACY_SENTINEL  # intacto
    assert row.score == 0


@pytest.mark.asyncio
async def test_con_apply_recalcula_desde_las_submissions():
    """Con --apply el progreso pasa a ejercicios_hechos / totales."""
    user_id = 90002
    lesson_id = await _seed_legacy_row(num_exercises=4, aprobados=1, user_id=user_id)

    await backfill.report(apply=True)

    row = await _read_row(user_id, lesson_id)
    assert row.progress == 25  # 1 de 4
    assert row.status == "in_progress"
    assert row.score == 10  # solo el ejercicio aprobado


@pytest.mark.asyncio
async def test_apply_cierra_la_leccion_si_estaban_todos_hechos():
    """Una fila sentinel de una lección ya terminada pasa a completed/100."""
    user_id = 90003
    lesson_id = await _seed_legacy_row(num_exercises=2, aprobados=2, user_id=user_id)

    await backfill.report(apply=True)

    row = await _read_row(user_id, lesson_id)
    assert row.progress == 100
    assert row.status == "completed"
    assert row.completed_at is not None


@pytest.mark.asyncio
async def test_apply_es_idempotente():
    """Correrlo dos veces deja el mismo estado y ya no encuentra candidatas."""
    user_id = 90004
    lesson_id = await _seed_legacy_row(num_exercises=2, aprobados=1, user_id=user_id)

    await backfill.report(apply=True)
    primera = await _read_row(user_id, lesson_id)

    # Segunda pasada: esta fila ya no es candidata y nada la mueve.
    await backfill.report(apply=True)
    segunda = await _read_row(user_id, lesson_id)

    assert primera.progress == 50
    assert (primera.progress, primera.status, primera.score) == (
        segunda.progress,
        segunda.status,
        segunda.score,
    )
