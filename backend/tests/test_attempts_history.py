"""Tests del historial de intentos (Fase 1 Pieza 8.1).

Cubre dos endpoints:
- GET /api/v1/exercises/{id}/evaluations -> CodeEvaluation por usuario
- GET /api/v1/elo/puzzles/{id}/attempts -> PuzzleAttempt por usuario

Ambos deben filtrar por user_id; un usuario nunca puede ver historial
de otro.
"""

from datetime import datetime, timedelta

import pytest

from app.core.database import async_session_maker
from app.models.code_evaluation import CodeEvaluation
from app.models.elo_models import Puzzle, PuzzleAttempt
from app.models.learning import Exercise, Lesson


async def _seed_exercise() -> int:
    async with async_session_maker() as session:
        lesson = Lesson(title="Lesson hist", description="d", content="c")
        session.add(lesson)
        await session.flush()
        ex = Exercise(
            lesson_id=lesson.id,
            title="Ej hist",
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


async def _seed_evaluation(
    user_id: int,
    exercise_id: int,
    *,
    code: str = "print('hola')",
    logic_score: int | None = 80,
    created_at: datetime | None = None,
) -> int:
    async with async_session_maker() as session:
        ev = CodeEvaluation(
            user_id=user_id,
            exercise_id=exercise_id,
            problem_description="problema",
            code=code,
            expected_output="hola",
            actual_output="hola",
            verdict={
                "raw": f"CALIFICACION: {logic_score}",
                "logic_score": logic_score,
                "general_score": logic_score,
            },
            model_used="fake",
        )
        if created_at is not None:
            ev.created_at = created_at
        session.add(ev)
        await session.commit()
        await session.refresh(ev)
        return ev.id


async def _seed_puzzle() -> int:
    async with async_session_maker() as session:
        p = Puzzle(
            title="Puzzle hist",
            slug=f"puzzle-hist-{datetime.utcnow().timestamp()}",
            category="python",
            topic="basics",
            code_snippet="print(1+1)",
            correct_output="2",
            explanation="suma",
            elo_rating=1200,
        )
        session.add(p)
        await session.commit()
        await session.refresh(p)
        return p.id


async def _seed_attempt(
    user_id: int,
    puzzle_id: int,
    *,
    correct: bool = True,
    user_answer: str = "2",
    delta: int = 12,
    created_at: datetime | None = None,
) -> int:
    async with async_session_maker() as session:
        a = PuzzleAttempt(
            user_id=user_id,
            puzzle_id=puzzle_id,
            correct=correct,
            user_answer=user_answer,
            user_elo_before=1000,
            user_elo_after=1000 + delta,
            puzzle_elo_before=1200,
            puzzle_elo_after=1200 - delta,
            elo_delta_user=delta,
            elo_delta_puzzle=-delta,
            expected_probability=0.5,
            time_spent_seconds=42,
        )
        if created_at is not None:
            a.created_at = created_at
        session.add(a)
        await session.commit()
        await session.refresh(a)
        return a.id


# ---------- evaluations history ----------


@pytest.mark.asyncio
async def test_get_evaluations_returns_user_only(client, user_a, user_b):
    """A guarda 2 evaluaciones; B no debe ver ninguna."""
    ex_id = await _seed_exercise()
    await _seed_evaluation(user_a["id"], ex_id, code="print('a1')")
    await _seed_evaluation(user_a["id"], ex_id, code="print('a2')")
    await _seed_evaluation(user_b["id"], ex_id, code="print('b1')")

    ra = await client.get(
        f"/api/v1/exercises/{ex_id}/evaluations", headers=user_a["headers"]
    )
    assert ra.status_code == 200, ra.text
    body_a = ra.json()
    assert body_a["total"] == 2
    codes_a = [item["code"] for item in body_a["items"]]
    assert "print('a1')" in codes_a
    assert "print('a2')" in codes_a
    assert "print('b1')" not in codes_a

    rb = await client.get(
        f"/api/v1/exercises/{ex_id}/evaluations", headers=user_b["headers"]
    )
    assert rb.status_code == 200
    body_b = rb.json()
    assert body_b["total"] == 1
    assert body_b["items"][0]["code"] == "print('b1')"


@pytest.mark.asyncio
async def test_get_evaluations_ordered_desc(client, auth_headers):
    """El historial vuelve más recientes primero."""
    ex_id = await _seed_exercise()
    base = datetime(2026, 5, 1, 12, 0, 0)
    # buscar el user_id que vino con auth_headers leyendo /users/me
    me = await client.get("/api/v1/users/me", headers=auth_headers)
    user_id = me.json()["id"]
    await _seed_evaluation(user_id, ex_id, code="viejo", created_at=base)
    await _seed_evaluation(
        user_id, ex_id, code="medio", created_at=base + timedelta(hours=1)
    )
    await _seed_evaluation(
        user_id, ex_id, code="nuevo", created_at=base + timedelta(hours=2)
    )

    r = await client.get(f"/api/v1/exercises/{ex_id}/evaluations", headers=auth_headers)
    assert r.status_code == 200
    items = r.json()["items"]
    assert [it["code"] for it in items] == ["nuevo", "medio", "viejo"]


@pytest.mark.asyncio
async def test_get_evaluations_requires_auth(client):
    r = await client.get("/api/v1/exercises/1/evaluations")
    assert r.status_code in (401, 403)


@pytest.mark.asyncio
async def test_get_evaluations_empty_when_none(client, auth_headers):
    ex_id = await _seed_exercise()
    r = await client.get(f"/api/v1/exercises/{ex_id}/evaluations", headers=auth_headers)
    assert r.status_code == 200
    assert r.json() == {"items": [], "total": 0}


# ---------- puzzle attempts history ----------


@pytest.mark.asyncio
async def test_get_puzzle_attempts_returns_user_only(client, user_a, user_b):
    puzzle_id = await _seed_puzzle()
    await _seed_attempt(user_a["id"], puzzle_id, user_answer="A1")
    await _seed_attempt(
        user_a["id"], puzzle_id, correct=False, user_answer="A2", delta=-8
    )
    await _seed_attempt(user_b["id"], puzzle_id, user_answer="B1")

    ra = await client.get(
        f"/api/v1/elo/puzzles/{puzzle_id}/attempts", headers=user_a["headers"]
    )
    assert ra.status_code == 200, ra.text
    body_a = ra.json()
    assert body_a["total"] == 2
    answers_a = [item["user_answer"] for item in body_a["items"]]
    assert "A1" in answers_a
    assert "A2" in answers_a
    assert "B1" not in answers_a

    rb = await client.get(
        f"/api/v1/elo/puzzles/{puzzle_id}/attempts", headers=user_b["headers"]
    )
    assert rb.status_code == 200
    body_b = rb.json()
    assert body_b["total"] == 1
    assert body_b["items"][0]["user_answer"] == "B1"


@pytest.mark.asyncio
async def test_get_puzzle_attempts_ordered_desc(client, auth_headers):
    me = await client.get("/api/v1/users/me", headers=auth_headers)
    user_id = me.json()["id"]
    puzzle_id = await _seed_puzzle()
    base = datetime(2026, 5, 1, 12, 0, 0)
    await _seed_attempt(user_id, puzzle_id, user_answer="viejo", created_at=base)
    await _seed_attempt(
        user_id,
        puzzle_id,
        user_answer="medio",
        created_at=base + timedelta(hours=1),
    )
    await _seed_attempt(
        user_id,
        puzzle_id,
        user_answer="nuevo",
        created_at=base + timedelta(hours=2),
    )

    r = await client.get(
        f"/api/v1/elo/puzzles/{puzzle_id}/attempts", headers=auth_headers
    )
    assert r.status_code == 200
    items = r.json()["items"]
    assert [it["user_answer"] for it in items] == ["nuevo", "medio", "viejo"]


@pytest.mark.asyncio
async def test_get_puzzle_attempts_requires_auth(client):
    r = await client.get("/api/v1/elo/puzzles/1/attempts")
    assert r.status_code in (401, 403)


@pytest.mark.asyncio
async def test_get_puzzle_attempts_empty_when_none(client, auth_headers):
    puzzle_id = await _seed_puzzle()
    r = await client.get(
        f"/api/v1/elo/puzzles/{puzzle_id}/attempts", headers=auth_headers
    )
    assert r.status_code == 200
    assert r.json() == {"items": [], "total": 0}
