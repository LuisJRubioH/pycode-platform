"""Tests del endpoint /progress/track-status (Pieza D.4 — gate del certificado)."""

import pytest

from app.core.database import async_session_maker
from app.models.capstone import Capstone, CapstoneSubmission
from app.services.capstone_seed import seed_capstones_if_empty


async def _ensure_seeded_capstone() -> int:
    async with async_session_maker() as session:
        await seed_capstones_if_empty(session)
        from sqlalchemy import select

        row = await session.execute(
            select(Capstone).where(Capstone.slug == "track-1-cli-ventas")
        )
        cap = row.scalar_one()
        return cap.id


async def _seed_submission(user_id: int, capstone_id: int, status: str) -> None:
    async with async_session_maker() as session:
        sub = CapstoneSubmission(
            user_id=user_id,
            capstone_id=capstone_id,
            files={"main.py": "ok"},
            status=status,
            tests_passed=8 if status == "passed" else 3,
            tests_total=8,
            test_results=[],
        )
        session.add(sub)
        await session.commit()


@pytest.mark.asyncio
async def test_track_status_returns_track1(client, auth_headers):
    """Devuelve Track 1 con conteos y capstone_status None sin submission."""
    await _ensure_seeded_capstone()
    r = await client.get("/api/v1/progress/track-status", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert len(body) == 1
    t = body[0]
    assert t["track"] == "track-1"
    assert t["title"].startswith("Track 1")
    assert t["lessons_total"] >= 0
    assert t["exercises_total"] >= 0
    assert t["capstone_slug"] == "track-1-cli-ventas"
    # Sin submission: status None y certificado bloqueado
    assert t["capstone_status"] is None
    assert t["certificate_unlocked"] is False


@pytest.mark.asyncio
async def test_track_status_certificate_unlocked_when_passed(client, user_a):
    cap_id = await _ensure_seeded_capstone()
    await _seed_submission(user_a["id"], cap_id, status="passed")

    r = await client.get(
        "/api/v1/progress/track-status", headers=user_a["headers"]
    )
    assert r.status_code == 200
    t = r.json()[0]
    assert t["capstone_status"] == "passed"
    assert t["capstone_tests_passed"] == 8
    assert t["capstone_tests_total"] == 8
    assert t["certificate_unlocked"] is True


@pytest.mark.asyncio
async def test_track_status_failed_does_not_unlock(client, user_a):
    cap_id = await _ensure_seeded_capstone()
    await _seed_submission(user_a["id"], cap_id, status="failed")

    r = await client.get("/api/v1/progress/track-status", headers=user_a["headers"])
    t = r.json()[0]
    assert t["capstone_status"] == "failed"
    assert t["certificate_unlocked"] is False


@pytest.mark.asyncio
async def test_track_status_cross_user_isolated(client, user_a, user_b):
    """B no debe ver certificate_unlocked=True solo porque A lo paso."""
    cap_id = await _ensure_seeded_capstone()
    await _seed_submission(user_a["id"], cap_id, status="passed")

    rb = await client.get("/api/v1/progress/track-status", headers=user_b["headers"])
    tb = rb.json()[0]
    assert tb["capstone_status"] is None
    assert tb["certificate_unlocked"] is False


@pytest.mark.asyncio
async def test_track_status_requires_auth(client):
    r = await client.get("/api/v1/progress/track-status")
    assert r.status_code in (401, 403)
