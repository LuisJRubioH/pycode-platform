"""Tests de los endpoints de capstones (Pieza D.1).

Cubre los tres endpoints de lectura:
- GET /api/v1/capstones -> lista con marca `completed` por usuario
- GET /api/v1/capstones/{slug} -> detalle SIN hidden_tests
- GET /api/v1/capstones/{slug}/my-submission -> ultima submission del user

Verifica el guard rail clave: `hidden_tests` no debe filtrarse en
list ni en detail (mismo patron que `exercises.hidden_tests`).
"""

from datetime import datetime, timedelta

import pytest

from app.core.database import async_session_maker
from app.models.capstone import Capstone, CapstoneSubmission
from app.services.capstone_seed import seed_capstones_if_empty


async def _ensure_real_seeded() -> None:
    """Corre el seeder real (idempotente) para que `track-1-cli-ventas` exista.

    En tests, `ASGITransport` no dispara el lifespan, asi que los seeders del
    `main.py` no corren. Los tests que dependen de los capstones seedeados los
    invocan explicitamente con este helper.
    """
    async with async_session_maker() as session:
        await seed_capstones_if_empty(session)


async def _ensure_capstone(slug: str = "test-cap-1") -> int:
    """Crea un capstone de prueba si no existe; retorna su id."""
    async with async_session_maker() as session:
        from sqlalchemy import select

        existing = await session.execute(select(Capstone).where(Capstone.slug == slug))
        cap = existing.scalar_one_or_none()
        if cap is not None:
            return cap.id

        cap = Capstone(
            slug=slug,
            track="track-1",
            title="Capstone de prueba",
            short_description="Resumen corto.",
            description="## Detalle\n\nLargo en markdown.",
            requirements=[{"id": "R1", "text": "Hacer algo."}],
            starter_files=[
                {"path": "main.py", "content": "# todo\n", "editable": True}
            ],
            hidden_tests=[
                {"name": "test secreto", "code": "assert True"},
                {"name": "otro test secreto", "code": "assert 1 + 1 == 2"},
            ],
            estimated_hours=4,
            difficulty="intermediate",
            order_index=99,
        )
        session.add(cap)
        await session.commit()
        await session.refresh(cap)
        return cap.id


async def _seed_submission(
    user_id: int,
    capstone_id: int,
    *,
    status: str = "passed",
    tests_passed: int = 2,
    tests_total: int = 2,
    created_at: datetime | None = None,
) -> int:
    async with async_session_maker() as session:
        sub = CapstoneSubmission(
            user_id=user_id,
            capstone_id=capstone_id,
            files={"main.py": "print(1)\n"},
            status=status,
            tests_passed=tests_passed,
            tests_total=tests_total,
            test_results=[{"name": "x", "passed": True}],
        )
        if created_at is not None:
            sub.created_at = created_at
        session.add(sub)
        await session.commit()
        await session.refresh(sub)
        return sub.id


# ---------- list ----------


@pytest.mark.asyncio
async def test_list_capstones_returns_seeded(client, auth_headers):
    """La lista incluye al menos el capstone seedeado en main lifespan."""
    await _ensure_real_seeded()
    r = await client.get("/api/v1/capstones", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["total"] >= 1
    slugs = [item["slug"] for item in body["items"]]
    assert "track-1-cli-ventas" in slugs


@pytest.mark.asyncio
async def test_list_capstones_no_hidden_tests(client, auth_headers):
    """El payload de la lista nunca contiene `hidden_tests`."""
    await _ensure_capstone()
    r = await client.get("/api/v1/capstones", headers=auth_headers)
    body = r.json()
    for item in body["items"]:
        assert "hidden_tests" not in item


@pytest.mark.asyncio
async def test_list_capstones_marks_completed(client, user_a):
    cap_id = await _ensure_capstone()
    await _seed_submission(user_a["id"], cap_id, status="passed")

    r = await client.get("/api/v1/capstones", headers=user_a["headers"])
    body = r.json()
    target = next(item for item in body["items"] if item["id"] == cap_id)
    assert target["completed"] is True


@pytest.mark.asyncio
async def test_list_capstones_completed_only_for_passed(client, user_a):
    """Una submission con status=failed NO marca completed=True."""
    cap_id = await _ensure_capstone(slug="test-cap-failed")
    await _seed_submission(user_a["id"], cap_id, status="failed")

    r = await client.get("/api/v1/capstones", headers=user_a["headers"])
    body = r.json()
    target = next(item for item in body["items"] if item["id"] == cap_id)
    assert target["completed"] is False


@pytest.mark.asyncio
async def test_list_capstones_isolated_per_user(client, user_a, user_b):
    """B no debe ver completed=True solo porque A lo paso."""
    cap_id = await _ensure_capstone(slug="test-cap-iso")
    await _seed_submission(user_a["id"], cap_id, status="passed")

    rb = await client.get("/api/v1/capstones", headers=user_b["headers"])
    body_b = rb.json()
    target_b = next(item for item in body_b["items"] if item["id"] == cap_id)
    assert target_b["completed"] is False


@pytest.mark.asyncio
async def test_list_capstones_requires_auth(client):
    r = await client.get("/api/v1/capstones")
    assert r.status_code in (401, 403)


# ---------- detail ----------


@pytest.mark.asyncio
async def test_get_capstone_detail_basic(client, auth_headers):
    await _ensure_real_seeded()
    r = await client.get("/api/v1/capstones/track-1-cli-ventas", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["slug"] == "track-1-cli-ventas"
    assert body["track"] == "track-1"
    assert isinstance(body["requirements"], list)
    assert isinstance(body["starter_files"], list)
    assert body["tests_total"] >= 1


@pytest.mark.asyncio
async def test_get_capstone_detail_no_hidden_tests(client, auth_headers):
    """El detalle expone `tests_total` pero NUNCA `hidden_tests`."""
    await _ensure_capstone(slug="test-cap-leak")
    r = await client.get("/api/v1/capstones/test-cap-leak", headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert body["tests_total"] == 2
    assert "hidden_tests" not in body
    # Tambien chequea que no este por dentro de algun campo serializado.
    raw = r.text
    assert "test secreto" not in raw
    assert "otro test secreto" not in raw


@pytest.mark.asyncio
async def test_get_capstone_detail_404(client, auth_headers):
    r = await client.get("/api/v1/capstones/no-existe-este-slug", headers=auth_headers)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_get_capstone_detail_requires_auth(client):
    r = await client.get("/api/v1/capstones/track-1-cli-ventas")
    assert r.status_code in (401, 403)


# ---------- my-submission ----------


@pytest.mark.asyncio
async def test_get_my_submission_returns_latest(client, user_a):
    cap_id = await _ensure_capstone(slug="test-cap-latest")
    base = datetime(2026, 5, 20, 12, 0, 0)
    await _seed_submission(user_a["id"], cap_id, tests_passed=1, created_at=base)
    await _seed_submission(
        user_a["id"],
        cap_id,
        tests_passed=2,
        created_at=base + timedelta(hours=1),
    )

    r = await client.get(
        "/api/v1/capstones/test-cap-latest/my-submission",
        headers=user_a["headers"],
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["tests_passed"] == 2


@pytest.mark.asyncio
async def test_get_my_submission_cross_user_isolated(client, user_a, user_b):
    """B no debe ver la submission de A (404, no leak)."""
    cap_id = await _ensure_capstone(slug="test-cap-cross")
    await _seed_submission(user_a["id"], cap_id, status="passed")

    rb = await client.get(
        "/api/v1/capstones/test-cap-cross/my-submission",
        headers=user_b["headers"],
    )
    assert rb.status_code == 404, rb.text


@pytest.mark.asyncio
async def test_get_my_submission_404_when_none(client, auth_headers):
    await _ensure_capstone(slug="test-cap-empty")
    r = await client.get(
        "/api/v1/capstones/test-cap-empty/my-submission",
        headers=auth_headers,
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_get_my_submission_requires_auth(client):
    r = await client.get("/api/v1/capstones/track-1-cli-ventas/my-submission")
    assert r.status_code in (401, 403)
