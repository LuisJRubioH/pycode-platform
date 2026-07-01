"""Tests del endpoint /progress/track-status (Pieza D.4 + O — multi-track)."""

import pytest

from app.core.database import async_session_maker
from app.models.capstone import Capstone, CapstoneSubmission
from app.services.capstone_seed import seed_capstones_if_empty


async def _ensure_seeded_capstones() -> dict[str, int]:
    """Siembra los capstones seedeados y devuelve {slug: id}."""
    async with async_session_maker() as session:
        await seed_capstones_if_empty(session)
        from sqlalchemy import select

        rows = await session.execute(select(Capstone))
        return {cap.slug: cap.id for cap in rows.scalars().all()}


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


def _by_track(body: list[dict], track: str) -> dict:
    """Localiza el item del track en la lista de track-status."""
    matches = [item for item in body if item["track"] == track]
    assert matches, f"track {track} no esta en la respuesta: {body}"
    return matches[0]


@pytest.mark.asyncio
async def test_track_status_returns_track1(client, auth_headers):
    """Devuelve Track 1 con conteos y capstone_status None sin submission."""
    await _ensure_seeded_capstones()
    r = await client.get("/api/v1/progress/track-status", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    t = _by_track(body, "track-1")
    assert t["title"].startswith("Track 1")
    assert t["lessons_total"] >= 0
    assert t["exercises_total"] >= 0
    assert t["capstone_slug"] == "track-1-cli-ventas"
    # Sin submission: status None y certificado bloqueado
    assert t["capstone_status"] is None
    assert t["certificate_unlocked"] is False


@pytest.mark.asyncio
async def test_track_status_includes_track2_capstone(client, auth_headers):
    """Track 2 aparece con su capstone EDA cuando hay capstones seedeados."""
    await _ensure_seeded_capstones()
    r = await client.get("/api/v1/progress/track-status", headers=auth_headers)
    body = r.json()
    t2 = _by_track(body, "track-2")
    assert t2["title"].startswith("Track 2")
    assert t2["capstone_slug"] == "track-2-eda-cafecito"
    assert t2["capstone_status"] is None
    assert t2["certificate_unlocked"] is False


@pytest.mark.asyncio
async def test_track_status_certificate_unlocked_when_passed(client, user_a):
    caps = await _ensure_seeded_capstones()
    await _seed_submission(user_a["id"], caps["track-1-cli-ventas"], status="passed")

    r = await client.get("/api/v1/progress/track-status", headers=user_a["headers"])
    assert r.status_code == 200
    t = _by_track(r.json(), "track-1")
    assert t["capstone_status"] == "passed"
    assert t["capstone_tests_passed"] == 8
    assert t["capstone_tests_total"] == 8
    assert t["certificate_unlocked"] is True


@pytest.mark.asyncio
async def test_track_status_track2_unlock_isolated(client, user_a):
    """Aprobar Track 1 no desbloquea el Track 2 y viceversa."""
    caps = await _ensure_seeded_capstones()
    await _seed_submission(user_a["id"], caps["track-1-cli-ventas"], status="passed")

    body = (
        await client.get("/api/v1/progress/track-status", headers=user_a["headers"])
    ).json()
    assert _by_track(body, "track-1")["certificate_unlocked"] is True
    assert _by_track(body, "track-2")["certificate_unlocked"] is False


@pytest.mark.asyncio
async def test_track_status_failed_does_not_unlock(client, user_a):
    caps = await _ensure_seeded_capstones()
    await _seed_submission(user_a["id"], caps["track-1-cli-ventas"], status="failed")

    r = await client.get("/api/v1/progress/track-status", headers=user_a["headers"])
    t = _by_track(r.json(), "track-1")
    assert t["capstone_status"] == "failed"
    assert t["certificate_unlocked"] is False


@pytest.mark.asyncio
async def test_track_status_cross_user_isolated(client, user_a, user_b):
    """B no debe ver certificate_unlocked=True solo porque A lo paso."""
    caps = await _ensure_seeded_capstones()
    await _seed_submission(user_a["id"], caps["track-1-cli-ventas"], status="passed")

    rb = await client.get("/api/v1/progress/track-status", headers=user_b["headers"])
    tb = _by_track(rb.json(), "track-1")
    assert tb["capstone_status"] is None
    assert tb["certificate_unlocked"] is False


@pytest.mark.asyncio
async def test_track_status_requires_auth(client):
    r = await client.get("/api/v1/progress/track-status")
    assert r.status_code in (401, 403)
