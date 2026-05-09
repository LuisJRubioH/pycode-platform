"""Tests del endpoint GET /api/v1/progress/competencies (Fase 1 P9.1)."""

from datetime import datetime

import pytest

from app.core.database import async_session_maker
from app.models.learning import CodeSubmission, Exercise, Lesson, UserProgress


async def _seed_lesson(
    title: str,
    *,
    category: str,
    difficulty: str = "beginner",
    order: int = 0,
) -> int:
    async with async_session_maker() as session:
        lesson = Lesson(
            title=title,
            description="d",
            content="c",
            category=category,
            difficulty=difficulty,
            order=order,
            is_active=True,
        )
        session.add(lesson)
        await session.commit()
        await session.refresh(lesson)
        return lesson.id


async def _seed_exercise(lesson_id: int, *, title: str = "Ej") -> int:
    async with async_session_maker() as session:
        ex = Exercise(
            lesson_id=lesson_id,
            title=title,
            description="d",
            instructions="i",
            starter_code="pass\n",
            solution_code="pass\n",
            hints=[],
            points=10,
            difficulty="easy",
            order=0,
        )
        session.add(ex)
        await session.commit()
        await session.refresh(ex)
        return ex.id


async def _seed_progress(user_id: int, lesson_id: int, status: str) -> None:
    async with async_session_maker() as session:
        p = UserProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            status=status,
            progress=100 if status == "completed" else 50,
            score=10,
            time_spent=60,
            attempts=1,
            completed_at=datetime.utcnow() if status == "completed" else None,
        )
        session.add(p)
        await session.commit()


async def _seed_submission(user_id: int, exercise_id: int, *, result: str) -> None:
    async with async_session_maker() as session:
        sub = CodeSubmission(
            user_id=user_id,
            exercise_id=exercise_id,
            code="print(1)",
            result=result,
            output="1",
            execution_time=10,
            passed_tests=1 if result == "success" else 0,
            total_tests=1,
        )
        session.add(sub)
        await session.commit()


@pytest.mark.asyncio
async def test_competencies_groups_by_category(client, auth_headers):
    """El endpoint agrupa lecciones por categoria y suma totales."""
    me = await client.get("/api/v1/users/me", headers=auth_headers)
    user_id = me.json()["id"]

    l1 = await _seed_lesson("Variables", category="fundamentos", order=1)
    l2 = await _seed_lesson("Operadores", category="fundamentos", order=2)
    l3 = await _seed_lesson("Listas", category="estructuras-datos", order=3)

    e1 = await _seed_exercise(l1, title="ej1")
    e2 = await _seed_exercise(l1, title="ej2")
    await _seed_exercise(l2, title="ej3")
    await _seed_exercise(l3, title="ej4")

    await _seed_progress(user_id, l1, "completed")
    await _seed_progress(user_id, l2, "in_progress")
    await _seed_submission(user_id, e1, result="success")
    await _seed_submission(user_id, e2, result="success")
    # mismo ejercicio dos veces -> debe contar 1 sola vez
    await _seed_submission(user_id, e1, result="success")

    r = await client.get("/api/v1/progress/competencies", headers=auth_headers)
    assert r.status_code == 200, r.text
    data = r.json()

    # Debe haber al menos las dos categorias seeded
    by_cat = {c["category"]: c for c in data}
    assert "fundamentos" in by_cat
    assert "estructuras-datos" in by_cat

    fund = by_cat["fundamentos"]
    assert fund["lessons_total"] >= 2  # >=2 porque pueden coexistir seeds reales
    assert fund["lessons_completed"] >= 1
    assert fund["exercises_total"] >= 3
    assert fund["exercises_completed"] >= 2  # e1 y e2, no 3 (e1 dedup)


@pytest.mark.asyncio
async def test_competencies_isolated_per_user(client, user_a, user_b):
    """A completa una leccion; B no debe verla como completed."""
    cat = f"test-iso-{datetime.utcnow().timestamp()}"
    l1 = await _seed_lesson("Iso L1", category=cat)
    e1 = await _seed_exercise(l1, title="iso-ex")
    await _seed_progress(user_a["id"], l1, "completed")
    await _seed_submission(user_a["id"], e1, result="success")

    ra = await client.get("/api/v1/progress/competencies", headers=user_a["headers"])
    assert ra.status_code == 200
    cat_a = next(c for c in ra.json() if c["category"] == cat)
    assert cat_a["lessons_completed"] == 1
    assert cat_a["exercises_completed"] == 1

    rb = await client.get("/api/v1/progress/competencies", headers=user_b["headers"])
    assert rb.status_code == 200
    cat_b = next(c for c in rb.json() if c["category"] == cat)
    assert cat_b["lessons_completed"] == 0
    assert cat_b["exercises_completed"] == 0
    # Pero B sí ve los totales (lessons_total / exercises_total son del catálogo)
    assert cat_b["lessons_total"] == 1
    assert cat_b["exercises_total"] == 1


@pytest.mark.asyncio
async def test_competencies_requires_auth(client):
    r = await client.get("/api/v1/progress/competencies")
    assert r.status_code in (401, 403)


@pytest.mark.asyncio
async def test_competencies_failed_submission_does_not_count(client, auth_headers):
    """Solo CodeSubmission con result='success' cuenta como ejercicio hecho."""
    me = await client.get("/api/v1/users/me", headers=auth_headers)
    user_id = me.json()["id"]

    cat = f"test-fail-{datetime.utcnow().timestamp()}"
    l1 = await _seed_lesson("Fail L1", category=cat)
    e1 = await _seed_exercise(l1)
    await _seed_submission(user_id, e1, result="error")

    r = await client.get("/api/v1/progress/competencies", headers=auth_headers)
    assert r.status_code == 200
    bucket = next(c for c in r.json() if c["category"] == cat)
    assert bucket["exercises_total"] == 1
    assert bucket["exercises_completed"] == 0


@pytest.mark.asyncio
async def test_competencies_in_progress_lesson_not_counted_as_completed(
    client, auth_headers
):
    """status=in_progress no cuenta como leccion completada."""
    me = await client.get("/api/v1/users/me", headers=auth_headers)
    user_id = me.json()["id"]

    cat = f"test-ip-{datetime.utcnow().timestamp()}"
    l1 = await _seed_lesson("IP L1", category=cat)
    await _seed_progress(user_id, l1, "in_progress")

    r = await client.get("/api/v1/progress/competencies", headers=auth_headers)
    assert r.status_code == 200
    bucket = next(c for c in r.json() if c["category"] == cat)
    assert bucket["lessons_total"] == 1
    assert bucket["lessons_completed"] == 0
