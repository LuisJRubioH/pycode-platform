"""Tests del ELO de retos por dificultad (Pieza J).

Al completar un reto (pasando todos sus tests) se otorga ELO a la track
`challenge:<dificultad>`; desmarcar lo revierte (sin farmear con toggle).
Idempotente.
"""

import uuid

import pytest
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.challenge import CodingChallenge
from app.models.elo_models import EloRating
from app.models.user import UserProfile

# Resultado de pasar los dos tests de los retos que crea _make_challenge.
RESUELTO = {"passed_tests": 2, "total_tests": 2}


async def _make_challenge(difficulty: str = "easy") -> int:
    async with async_session_maker() as session:
        ch = CodingChallenge(
            title=f"Reto {difficulty}",
            slug=f"chl-elo-{difficulty}-{uuid.uuid4().hex[:8]}",
            source="test",
            source_path="test.md",
            difficulty=difficulty,
            topic="logic",
            prompt="haz algo",
            starter_code="# todo\n",
            hidden_tests=[
                {"name": "uno", "code": "assert True"},
                {"name": "dos", "code": "assert True"},
            ],
        )
        session.add(ch)
        await session.commit()
        await session.refresh(ch)
        return ch.id


async def _rating(user_id: int, scope: str) -> EloRating | None:
    async with async_session_maker() as session:
        row = await session.execute(
            select(EloRating).where(
                EloRating.user_id == user_id,
                EloRating.domain == "challenge",
                EloRating.scope == scope,
            )
        )
        return row.scalar_one_or_none()


@pytest.mark.asyncio
async def test_complete_grants_elo(client, user_a):
    cid = await _make_challenge("easy")
    r = await client.post(
        f"/api/v1/challenges/{cid}/complete", headers=user_a["headers"], json=RESUELTO
    )
    assert r.status_code == 204

    rating = await _rating(user_a["id"], "easy")
    assert rating is not None
    assert rating.attempts == 1
    assert rating.correct == 1
    assert rating.elo_rating > 1000


@pytest.mark.asyncio
async def test_complete_is_idempotent(client, user_a):
    cid = await _make_challenge("easy")
    await client.post(
        f"/api/v1/challenges/{cid}/complete", headers=user_a["headers"], json=RESUELTO
    )
    first = await _rating(user_a["id"], "easy")
    elo_after_first = first.elo_rating

    await client.post(
        f"/api/v1/challenges/{cid}/complete", headers=user_a["headers"], json=RESUELTO
    )
    second = await _rating(user_a["id"], "easy")
    assert second.attempts == 1
    assert second.elo_rating == elo_after_first


@pytest.mark.asyncio
async def test_uncomplete_reverts_elo(client, user_a):
    cid = await _make_challenge("easy")
    await client.post(
        f"/api/v1/challenges/{cid}/complete", headers=user_a["headers"], json=RESUELTO
    )
    assert (await _rating(user_a["id"], "easy")).elo_rating > 1000

    r = await client.delete(
        f"/api/v1/challenges/{cid}/complete", headers=user_a["headers"]
    )
    assert r.status_code == 204
    reverted = await _rating(user_a["id"], "easy")
    assert reverted.elo_rating == 1000
    assert reverted.attempts == 0
    assert reverted.correct == 0


@pytest.mark.asyncio
async def test_difficulties_are_separate_tracks(client, user_a):
    easy = await _make_challenge("easy")
    hard = await _make_challenge("hard")
    await client.post(
        f"/api/v1/challenges/{easy}/complete", headers=user_a["headers"], json=RESUELTO
    )
    await client.post(
        f"/api/v1/challenges/{hard}/complete", headers=user_a["headers"], json=RESUELTO
    )

    assert await _rating(user_a["id"], "easy") is not None
    assert await _rating(user_a["id"], "hard") is not None


@pytest.mark.asyncio
async def test_lazy_init_inherits_global(client, user_a):
    await client.get("/api/v1/elo/profile", headers=user_a["headers"])
    async with async_session_maker() as session:
        prof = (
            await session.execute(
                select(UserProfile).where(UserProfile.user_id == user_a["id"])
            )
        ).scalar_one()
        prof.elo_rating = 1300
        await session.commit()

    cid = await _make_challenge("medium")
    await client.post(
        f"/api/v1/challenges/{cid}/complete", headers=user_a["headers"], json=RESUELTO
    )
    rating = await _rating(user_a["id"], "medium")
    assert rating.elo_rating >= 1300


@pytest.mark.asyncio
async def test_complete_exige_pasar_todos_los_tests(client, user_a):
    """Sin resultado, o con tests fallidos, no se completa ni se da ELO."""
    cid = await _make_challenge("medium")
    url = f"/api/v1/challenges/{cid}/complete"

    r = await client.post(url, headers=user_a["headers"])
    assert r.status_code == 422, "sin el resultado de los tests no se completa"
    for parcial in (
        {"passed_tests": 1, "total_tests": 2},
        {"passed_tests": 1, "total_tests": 1},
        {"passed_tests": 3, "total_tests": 3},
    ):
        r = await client.post(url, headers=user_a["headers"], json=parcial)
        assert r.status_code == 422, f"{parcial} no deberia completar el reto"
    assert await _rating(user_a["id"], "medium") is None, "se otorgo ELO sin resolver"

    r = await client.post(url, headers=user_a["headers"], json=RESUELTO)
    assert r.status_code == 204
    assert (await _rating(user_a["id"], "medium")).correct == 1


@pytest.mark.asyncio
async def test_reto_sin_tests_no_se_puede_completar(client, user_a):
    async with async_session_maker() as session:
        ch = CodingChallenge(
            title="Sin tests",
            slug=f"chl-sin-tests-{uuid.uuid4().hex[:8]}",
            source="test",
            source_path="test.md",
            difficulty="easy",
            topic="logic",
            prompt="haz algo",
            starter_code="# todo\n",
            hidden_tests=[],
        )
        session.add(ch)
        await session.commit()
        cid = ch.id
    r = await client.post(
        f"/api/v1/challenges/{cid}/complete",
        headers=user_a["headers"],
        json={"passed_tests": 0, "total_tests": 0},
    )
    assert r.status_code == 422
