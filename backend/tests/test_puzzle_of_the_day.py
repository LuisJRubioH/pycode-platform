"""Tests del endpoint público `GET /api/v1/elo/puzzle-of-the-day` (Pieza F).

Cubre:
- es público (sin auth) y devuelve la forma esperada
- guard rail: NUNCA expone la respuesta (`correct_output`/`explanation`)
- selección determinista dentro del mismo día (misma id en llamadas seguidas)
- solo selecciona puzzles activos y no avanzados
"""

import uuid

import pytest
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.elo_models import Puzzle

SECRET_OUTPUT = "RESPUESTA_SECRETA_42"


async def _make_puzzle(*, is_advanced: bool = False, is_active: bool = True) -> int:
    async with async_session_maker() as session:
        puzzle = Puzzle(
            title="Puzzle de prueba",
            slug=f"potd-{uuid.uuid4().hex[:10]}",
            category="python",
            topic="listas",
            code_snippet="print(sum([1, 2, 3]))",
            correct_output=SECRET_OUTPUT,
            explanation="Explicación secreta que no debe filtrarse.",
            hint="Pista secreta.",
            elo_rating=900,
            is_advanced=is_advanced,
            is_active=is_active,
        )
        session.add(puzzle)
        await session.commit()
        await session.refresh(puzzle)
        return puzzle.id


@pytest.mark.asyncio
async def test_potd_is_public_and_shaped(client):
    await _make_puzzle()
    r = await client.get("/api/v1/elo/puzzle-of-the-day")  # sin auth
    assert r.status_code == 200, r.text
    body = r.json()
    for key in (
        "id",
        "date",
        "title",
        "category",
        "topic",
        "code_snippet",
        "difficulty_label",
        "elo_rating",
        "solve_rate",
    ):
        assert key in body


@pytest.mark.asyncio
async def test_potd_never_leaks_answer(client):
    await _make_puzzle()
    r = await client.get("/api/v1/elo/puzzle-of-the-day")
    assert r.status_code == 200
    assert SECRET_OUTPUT not in r.text
    assert "correct_output" not in r.text
    assert "explanation" not in r.text
    assert "hint" not in r.text


@pytest.mark.asyncio
async def test_potd_is_deterministic_same_day(client):
    await _make_puzzle()
    r1 = await client.get("/api/v1/elo/puzzle-of-the-day")
    r2 = await client.get("/api/v1/elo/puzzle-of-the-day")
    assert r1.json()["id"] == r2.json()["id"]


@pytest.mark.asyncio
async def test_potd_only_active_non_advanced(client):
    # Hay al menos un avanzado y un inactivo en la mezcla.
    await _make_puzzle(is_advanced=True)
    await _make_puzzle(is_active=False)
    await _make_puzzle()

    r = await client.get("/api/v1/elo/puzzle-of-the-day")
    assert r.status_code == 200
    chosen_id = r.json()["id"]

    async with async_session_maker() as session:
        chosen = (
            await session.execute(select(Puzzle).where(Puzzle.id == chosen_id))
        ).scalar_one()
        assert chosen.is_advanced is False
        assert chosen.is_active is True
