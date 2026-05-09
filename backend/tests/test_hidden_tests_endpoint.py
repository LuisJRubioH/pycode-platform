"""Tests del endpoint GET /api/v1/exercises/{id}/hidden-tests (Fase 1 P6)."""

import pytest
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.learning import Exercise, Lesson


async def _seed_exercise_with_tests(hidden_tests):
    async with async_session_maker() as session:
        lesson = Lesson(title="Lesson HT", description="d", content="c")
        session.add(lesson)
        await session.flush()
        ex = Exercise(
            lesson_id=lesson.id,
            title="Sumar",
            description="d",
            instructions="i",
            starter_code="def my_sum(a, b):\n    pass\n",
            solution_code="def my_sum(a, b):\n    return a + b\n",
            hidden_tests=hidden_tests,
            hints=["pista 1", "pista 2"],
            points=10,
            difficulty="easy",
            order=0,
        )
        session.add(ex)
        await session.commit()
        await session.refresh(ex)
        return ex.id, lesson.id


@pytest.mark.asyncio
async def test_hidden_tests_returns_list_when_present(client, auth_headers):
    tests = [
        {"name": "suma básica", "code": "assert my_sum(2, 3) == 5"},
        {"name": "ceros", "code": "assert my_sum(0, 0) == 0"},
    ]
    ex_id, _ = await _seed_exercise_with_tests(tests)

    r = await client.get(
        f"/api/v1/exercises/{ex_id}/hidden-tests", headers=auth_headers
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["exercise_id"] == ex_id
    assert len(body["tests"]) == 2
    assert body["tests"][0]["name"] == "suma básica"
    assert body["tests"][0]["code"] == "assert my_sum(2, 3) == 5"


@pytest.mark.asyncio
async def test_hidden_tests_empty_when_none_seeded(client, auth_headers):
    ex_id, _ = await _seed_exercise_with_tests([])
    r = await client.get(
        f"/api/v1/exercises/{ex_id}/hidden-tests", headers=auth_headers
    )
    assert r.status_code == 200, r.text
    assert r.json()["tests"] == []


@pytest.mark.asyncio
async def test_hidden_tests_skips_malformed_entries(client, auth_headers):
    tests = [
        {"name": "valido", "code": "assert True"},
        {"name": "sin code"},
        {"code": "assert True", "name": ""},  # name vacío permitido pero code requerido
        "no es un dict",
        {"name": "code vacío", "code": ""},
    ]
    ex_id, _ = await _seed_exercise_with_tests(tests)
    r = await client.get(
        f"/api/v1/exercises/{ex_id}/hidden-tests", headers=auth_headers
    )
    assert r.status_code == 200
    body = r.json()
    # solo "valido" y el de name vacío con code → 2 entradas
    assert len(body["tests"]) == 2


@pytest.mark.asyncio
async def test_hidden_tests_requires_auth(client):
    r = await client.get("/api/v1/exercises/1/hidden-tests")
    assert r.status_code in (401, 403)


@pytest.mark.asyncio
async def test_hidden_tests_404_when_exercise_missing(client, auth_headers):
    r = await client.get("/api/v1/exercises/999999/hidden-tests", headers=auth_headers)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_lesson_endpoints_do_not_leak_hidden_tests(client, auth_headers):
    """Garantía clave: los endpoints públicos de lecciones/ejercicios NO
    incluyen hidden_tests en la respuesta. Solo el endpoint dedicado los
    devuelve, así un alumno no los ve hasta que pulsa "Ejecutar tests"."""
    tests = [{"name": "x", "code": "assert my_sum(1, 1) == 2"}]
    ex_id, lesson_id = await _seed_exercise_with_tests(tests)

    r1 = await client.get(f"/api/v1/lessons/{lesson_id}", headers=auth_headers)
    assert r1.status_code == 200
    assert "hidden_tests" not in r1.text
    assert "assert my_sum" not in r1.text

    r2 = await client.get(f"/api/v1/exercises/lesson/{lesson_id}", headers=auth_headers)
    assert r2.status_code == 200
    assert "hidden_tests" not in r2.text
    assert "assert my_sum" not in r2.text


@pytest.mark.asyncio
async def test_async_session_visible_after_test():
    """Sanity: la sesión de DB sigue funcionando tras los seeds del test."""
    async with async_session_maker() as session:
        rows = (await session.execute(select(Exercise))).scalars().all()
        assert isinstance(rows, list)
