"""Tests de persistencia de progreso al aprobar ejercicios (Bloque 1).

Cubre la causa raíz de los tres síntomas:
- idempotencia: reintentar un ejercicio ya aprobado no duplica XP/submissions.
- transición a lección completada al aprobar el último ejercicio.
- porcentaje de la barra = ejercicios_hechos / totales.
"""

import pytest
from sqlalchemy import func, select

from app.core.database import async_session_maker
from app.models.learning import CodeSubmission, Exercise, Lesson, UserProgress


async def _seed_lesson(num_exercises: int, points: int = 10):
    async with async_session_maker() as session:
        lesson = Lesson(title="Lesson Progress", description="d", content="c")
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
                hidden_tests=[{"name": "t", "code": "assert True"}],
                points=points,
                difficulty="easy",
                order=i,
            )
            session.add(ex)
            await session.flush()
            ex_ids.append(ex.id)
        await session.commit()
        return lesson.id, ex_ids


def _submit_payload(exercise_id: int):
    return {
        "exercise_id": exercise_id,
        "code": "print('ok')",
        "success": True,
        "passed_tests": 3,
        "total_tests": 3,
    }


async def _get_progress(user_id: int, lesson_id: int) -> UserProgress:
    async with async_session_maker() as session:
        return (
            await session.execute(
                select(UserProgress).where(
                    UserProgress.user_id == user_id,
                    UserProgress.lesson_id == lesson_id,
                )
            )
        ).scalar_one_or_none()


async def _count_submissions(user_id: int, exercise_id: int) -> int:
    async with async_session_maker() as session:
        return (
            await session.execute(
                select(func.count(CodeSubmission.id)).where(
                    CodeSubmission.user_id == user_id,
                    CodeSubmission.exercise_id == exercise_id,
                )
            )
        ).scalar()


@pytest.mark.asyncio
async def test_submit_marks_progress_and_percentage(client, user_a):
    """Aprobar 1 de 2 ejercicios deja la lección al 50% e in_progress."""
    lesson_id, ex_ids = await _seed_lesson(2)

    r = await client.post(
        f"/api/v1/exercises/{ex_ids[0]}/submit",
        json=_submit_payload(ex_ids[0]),
        headers=user_a["headers"],
    )
    assert r.status_code == 200, r.text
    assert r.json()["result"] == "success"

    progress = await _get_progress(user_a["id"], lesson_id)
    assert progress is not None
    assert progress.progress == 50
    assert progress.status == "in_progress"
    assert progress.score == 10  # solo 1 ejercicio hecho


@pytest.mark.asyncio
async def test_last_exercise_completes_lesson(client, user_a):
    """Aprobar el último ejercicio transiciona la lección a completed / 100%."""
    lesson_id, ex_ids = await _seed_lesson(2)

    for ex_id in ex_ids:
        r = await client.post(
            f"/api/v1/exercises/{ex_id}/submit",
            json=_submit_payload(ex_id),
            headers=user_a["headers"],
        )
        assert r.status_code == 200, r.text

    progress = await _get_progress(user_a["id"], lesson_id)
    assert progress.status == "completed"
    assert progress.progress == 100
    assert progress.completed_at is not None
    assert progress.score == 20

    # y el listado lo refleja
    lessons = (await client.get("/api/v1/lessons", headers=user_a["headers"])).json()
    row = next(item for item in lessons if item["id"] == lesson_id)
    assert row["progress"] == 100
    assert row["status"] == "completed"


@pytest.mark.asyncio
async def test_resubmit_is_idempotent(client, user_a):
    """Reintentar un ejercicio ya aprobado no duplica XP, intentos ni submissions."""
    lesson_id, ex_ids = await _seed_lesson(1)
    payload = _submit_payload(ex_ids[0])

    r1 = await client.post(
        f"/api/v1/exercises/{ex_ids[0]}/submit", json=payload, headers=user_a["headers"]
    )
    assert r1.status_code == 200
    progress1 = await _get_progress(user_a["id"], lesson_id)
    assert progress1.score == 10
    assert progress1.attempts == 1
    assert progress1.status == "completed"

    # segundo envío del mismo ejercicio ya aprobado
    r2 = await client.post(
        f"/api/v1/exercises/{ex_ids[0]}/submit", json=payload, headers=user_a["headers"]
    )
    assert r2.status_code == 200

    progress2 = await _get_progress(user_a["id"], lesson_id)
    assert progress2.score == 10  # NO se duplica
    assert progress2.attempts == 1  # NO se duplica
    assert progress2.progress == 100
    # no se creó una segunda submission
    assert await _count_submissions(user_a["id"], ex_ids[0]) == 1


@pytest.mark.asyncio
async def test_failed_attempt_records_but_no_completion(client, user_a):
    """Un intento fallido se registra pero no completa ni suma XP."""
    lesson_id, ex_ids = await _seed_lesson(1)

    r = await client.post(
        f"/api/v1/exercises/{ex_ids[0]}/submit",
        json={
            "exercise_id": ex_ids[0],
            "code": "x = 1",
            "success": False,
            "passed_tests": 1,
            "total_tests": 3,
        },
        headers=user_a["headers"],
    )
    assert r.status_code == 200
    assert r.json()["result"] == "error"

    progress = await _get_progress(user_a["id"], lesson_id)
    assert progress.status == "in_progress"
    assert progress.progress == 0
    assert progress.score == 0
    assert progress.attempts == 1
    assert await _count_submissions(user_a["id"], ex_ids[0]) == 1
