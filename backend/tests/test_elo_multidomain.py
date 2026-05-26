"""Tests del ELO multidominio (Pieza I).

Verifica que cada *(dominio, scope)* lleva su rating propio:
- categorías distintas divergen y son filas separadas
- lazy-init: la primera vez una track hereda el ELO global del usuario
- el timeline (`EloHistory`) queda etiquetado por dominio y con el ELO de la track
- aislamiento por usuario
- `/elo/profile` (overall global) sigue funcionando
"""

import uuid

import pytest
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.elo_models import EloHistory, EloRating, Puzzle
from app.models.user import UserProfile


async def _make_puzzle(category: str, correct_output: str, *, elo: int = 1000) -> int:
    async with async_session_maker() as session:
        puzzle = Puzzle(
            title=f"P-{category}",
            slug=f"elo-md-{category}-{uuid.uuid4().hex[:8]}",
            category=category,
            topic=category,
            code_snippet="print(1)",
            correct_output=correct_output,
            explanation="exp",
            elo_rating=elo,
            elo_initial=elo,
            is_advanced=False,
            is_active=True,
        )
        session.add(puzzle)
        await session.commit()
        await session.refresh(puzzle)
        return puzzle.id


async def _attempt(client, headers, puzzle_id: int, answer: str):
    return await client.post(
        "/api/v1/elo/attempt",
        json={"puzzle_id": puzzle_id, "user_answer": answer},
        headers=headers,
    )


async def _ratings(user_id: int) -> dict[str, EloRating]:
    async with async_session_maker() as session:
        rows = await session.execute(
            select(EloRating).where(EloRating.user_id == user_id)
        )
        return {f"{r.domain}:{r.scope}": r for r in rows.scalars().all()}


@pytest.mark.asyncio
async def test_categories_have_separate_ratings(client, user_a):
    py = await _make_puzzle("python", "42")
    np = await _make_puzzle("numpy", "7")

    assert (await _attempt(client, user_a["headers"], py, "42")).status_code == 200
    assert (await _attempt(client, user_a["headers"], np, "WRONG")).status_code == 200

    ratings = await _ratings(user_a["id"])
    assert "puzzle:python" in ratings
    assert "puzzle:numpy" in ratings
    # Acertar sube; fallar baja → divergen.
    assert ratings["puzzle:python"].elo_rating > ratings["puzzle:numpy"].elo_rating
    assert ratings["puzzle:python"].correct == 1
    assert ratings["puzzle:numpy"].correct == 0


@pytest.mark.asyncio
async def test_lazy_init_inherits_global_elo(client, user_a):
    # Crea el profile y súbele el ELO global a 1300.
    await client.get("/api/v1/elo/profile", headers=user_a["headers"])
    async with async_session_maker() as session:
        prof = (
            await session.execute(
                select(UserProfile).where(UserProfile.user_id == user_a["id"])
            )
        ).scalar_one()
        prof.elo_rating = 1300
        await session.commit()

    pid = await _make_puzzle("pandas", "ok")
    assert (await _attempt(client, user_a["headers"], pid, "ok")).status_code == 200

    ratings = await _ratings(user_a["id"])
    # La track 'pandas' arrancó desde 1300 (no desde 1000) + delta por acierto.
    assert ratings["puzzle:pandas"].elo_rating >= 1300


@pytest.mark.asyncio
async def test_history_is_per_track_and_tagged(client, user_a):
    pid = await _make_puzzle("interview", "y")
    await _attempt(client, user_a["headers"], pid, "y")

    async with async_session_maker() as session:
        prof = (
            await session.execute(
                select(UserProfile).where(UserProfile.user_id == user_a["id"])
            )
        ).scalar_one()
        rows = (
            (
                await session.execute(
                    select(EloHistory).where(EloHistory.user_profile_id == prof.id)
                )
            )
            .scalars()
            .all()
        )
    interview_points = [h for h in rows if h.category == "interview"]
    assert interview_points
    assert all(h.domain == "puzzle" for h in interview_points)


@pytest.mark.asyncio
async def test_ratings_isolated_per_user(client, user_a, user_b):
    pid = await _make_puzzle("python", "1")
    await _attempt(client, user_a["headers"], pid, "1")

    assert "puzzle:python" in await _ratings(user_a["id"])
    assert await _ratings(user_b["id"]) == {}


@pytest.mark.asyncio
async def test_profile_endpoint_still_works(client, user_a):
    pid = await _make_puzzle("python", "1")
    await _attempt(client, user_a["headers"], pid, "1")

    r = await client.get("/api/v1/elo/profile", headers=user_a["headers"])
    assert r.status_code == 200, r.text
    assert "elo_rating" in r.json()


@pytest.mark.asyncio
async def test_ratings_endpoint_lists_tracks_and_domain_summary(client, user_a):
    py = await _make_puzzle("python", "42")
    np = await _make_puzzle("numpy", "7")
    await _attempt(client, user_a["headers"], py, "42")
    await _attempt(client, user_a["headers"], np, "7")

    r = await client.get("/api/v1/elo/ratings", headers=user_a["headers"])
    assert r.status_code == 200, r.text
    body = r.json()
    track_keys = {f"{t['domain']}:{t['scope']}" for t in body["tracks"]}
    assert {"puzzle:python", "puzzle:numpy"} <= track_keys
    domain_names = {d["domain"] for d in body["domains"]}
    assert "puzzle" in domain_names
    assert "global_elo" in body and "global_rank_color" in body


@pytest.mark.asyncio
async def test_ratings_endpoint_requires_auth(client):
    r = await client.get("/api/v1/elo/ratings")
    assert r.status_code in (401, 403)
