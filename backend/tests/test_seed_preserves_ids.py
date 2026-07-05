"""Guard rail: el seeder de lecciones debe PRESERVAR los ids de los ejercicios
entre corridas (deploys). Antes hacia delete+recreate y los ids cambiaban en
cada arranque, dejando huerfanos los CodeSubmission -> el progreso se perdia.
"""

import pytest
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.learning import Exercise
from app.services.lesson_seed import seed_lessons_with_exercises


async def _snapshot_ids() -> dict[tuple[int, str], int]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(Exercise.id, Exercise.lesson_id, Exercise.title)
        )
        return {(lesson_id, title): ex_id for ex_id, lesson_id, title in result.all()}


@pytest.mark.asyncio
async def test_seeder_preserves_exercise_ids_across_runs():
    async with async_session_maker() as session:
        await seed_lessons_with_exercises(session)
    antes = await _snapshot_ids()
    assert antes, "el seeder deberia crear ejercicios"

    # Segunda corrida (simula un redeploy / cold start).
    async with async_session_maker() as session:
        await seed_lessons_with_exercises(session)
    despues = await _snapshot_ids()

    # Cada ejercicio (misma leccion+titulo) conserva su id exacto.
    for clave, ex_id in antes.items():
        assert clave in despues, f"desaparecio el ejercicio {clave}"
        assert (
            despues[clave] == ex_id
        ), f"el id del ejercicio {clave} cambio: {ex_id} -> {despues[clave]}"
