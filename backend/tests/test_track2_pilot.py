"""Tests Track 2 piloto: leccion NumPy + filtro ?track= + hidden_tests no-leak."""

import pytest

from app.core.database import async_session_maker
from app.models.learning import Exercise, Lesson
from app.services.lesson_seed import seed_lessons_with_exercises

_SEEDED = False


async def _ensure_lessons_seeded() -> None:
    """Lifespan no corre bajo ASGITransport; seed manual idempotente."""
    global _SEEDED
    if _SEEDED:
        return
    async with async_session_maker() as session:
        await seed_lessons_with_exercises(session)
    _SEEDED = True


@pytest.mark.asyncio
async def test_numpy_lesson_seeded_with_track_2(client, auth_headers):
    """La leccion NumPy esta seedeada con track='track-2'."""
    await _ensure_lessons_seeded()
    async with async_session_maker() as session:
        from sqlalchemy import select

        result = await session.execute(
            select(Lesson).where(
                Lesson.title == "NumPy esencial: arrays y broadcasting"
            )
        )
        lesson = result.scalar_one_or_none()
        assert lesson is not None, "leccion NumPy no fue seedeada"
        assert lesson.track == "track-2"
        assert lesson.category == "numpy"
        assert lesson.is_active is True


@pytest.mark.asyncio
async def test_filter_track_2_returns_only_numpy(client, auth_headers):
    """GET /api/v1/lessons?track=track-2 devuelve solo la leccion NumPy del piloto."""
    await _ensure_lessons_seeded()
    r = await client.get("/api/v1/lessons/?track=track-2", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    titles = [item["title"] for item in body]
    assert "NumPy esencial: arrays y broadcasting" in titles
    assert "Pandas esencial: Series, DataFrame e indexing" in titles
    # Todas las lecciones devueltas deben ser de track-2
    assert all(item["track"] == "track-2" for item in body)
    # Las categorias del track-2 incluyen numpy y pandas
    categories = {item["category"] for item in body}
    assert {"numpy", "pandas"}.issubset(categories)


@pytest.mark.asyncio
async def test_no_filter_returns_both_tracks(client, auth_headers):
    """GET /api/v1/lessons sin filtro mantiene backward-compat: devuelve todas."""
    await _ensure_lessons_seeded()
    r = await client.get("/api/v1/lessons/", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    tracks = {item["track"] for item in body}
    assert "track-1" in tracks, "deben aparecer lecciones de Track 1"
    assert "track-2" in tracks, "debe aparecer la leccion del piloto Track 2"


@pytest.mark.asyncio
async def test_numpy_exercise_hidden_tests_not_in_lesson_get(client, auth_headers):
    """GET /api/v1/lessons/{id} NO expone hidden_tests de los ejercicios.

    Patrón anti-leak validado en Pieza 6 — los hidden_tests solo se
    sirven via /exercises/{id}/hidden-tests con auth. La leccion debe
    devolver el listado de ejercicios sin esa columna serializada.
    """
    await _ensure_lessons_seeded()
    async with async_session_maker() as session:
        from sqlalchemy import select

        lesson_row = await session.execute(
            select(Lesson).where(
                Lesson.title == "NumPy esencial: arrays y broadcasting"
            )
        )
        lesson = lesson_row.scalar_one()
        ex_row = await session.execute(
            select(Exercise).where(Exercise.lesson_id == lesson.id)
        )
        exercises = ex_row.scalars().all()
        assert len(exercises) == 3, "el piloto define 3 ejercicios"
        for ex in exercises:
            assert ex.hidden_tests, f"{ex.title} debe tener hidden_tests definidos"
        lesson_id = lesson.id

    r = await client.get(f"/api/v1/lessons/{lesson_id}", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["track"] == "track-2"
    assert len(body["exercises"]) == 3
    for ex in body["exercises"]:
        assert (
            "hidden_tests" not in ex
        ), f"hidden_tests no debe leak en /lessons/{{id}}: ex={ex.get('title')}"


@pytest.mark.asyncio
async def test_numpy_hidden_tests_endpoint_returns_tests(client, auth_headers):
    """GET /api/v1/exercises/{id}/hidden-tests devuelve los tests con auth."""
    await _ensure_lessons_seeded()
    async with async_session_maker() as session:
        from sqlalchemy import select

        ex_row = await session.execute(
            select(Exercise).where(Exercise.title == "Pares hasta 20")
        )
        ex = ex_row.scalar_one()
        ex_id = ex.id

    r = await client.get(
        f"/api/v1/exercises/{ex_id}/hidden-tests", headers=auth_headers
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["exercise_id"] == ex_id
    assert len(body["tests"]) == 3
    test_names = {t["name"] for t in body["tests"]}
    assert "es un ndarray de NumPy" in test_names
    # Verifica que el codigo importa numpy (la pieza clave del piloto)
    assert any("import numpy" in t["code"] for t in body["tests"])
