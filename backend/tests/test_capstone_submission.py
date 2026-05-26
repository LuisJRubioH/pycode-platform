"""Tests del flujo de submission del capstone (Pieza D.3 backend).

Cubre:
- GET /api/v1/capstones/{slug}/hidden-tests -> tests para el worker
- POST /api/v1/capstones/{slug}/submissions -> persiste resultado
"""

import pytest

from app.core.database import async_session_maker
from app.models.capstone import Capstone


async def _ensure_capstone(slug: str, tests: list[dict]) -> int:
    from sqlalchemy import select

    async with async_session_maker() as session:
        existing = await session.execute(select(Capstone).where(Capstone.slug == slug))
        cap = existing.scalar_one_or_none()
        if cap is not None:
            return cap.id
        cap = Capstone(
            slug=slug,
            track="track-1",
            title="Capstone D3 fixture",
            short_description="Resumen.",
            description="## Desc.",
            requirements=[{"id": "R1", "text": "x"}],
            starter_files=[{"path": "main.py", "content": "# x\n", "editable": True}],
            hidden_tests=tests,
            estimated_hours=1,
            difficulty="easy",
            order_index=999,
        )
        session.add(cap)
        await session.commit()
        await session.refresh(cap)
        return cap.id


# ---------- hidden-tests endpoint ----------


@pytest.mark.asyncio
async def test_get_hidden_tests_returns_tests(client, auth_headers):
    await _ensure_capstone(
        "test-cap-ht",
        [
            {"name": "t1", "code": "assert True"},
            {"name": "t2", "code": "assert 1 + 1 == 2"},
        ],
    )
    r = await client.get(
        "/api/v1/capstones/test-cap-ht/hidden-tests", headers=auth_headers
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["slug"] == "test-cap-ht"
    assert len(body["tests"]) == 2
    assert body["tests"][0]["name"] == "t1"
    assert body["tests"][0]["code"] == "assert True"


@pytest.mark.asyncio
async def test_get_hidden_tests_404(client, auth_headers):
    r = await client.get(
        "/api/v1/capstones/no-existe/hidden-tests", headers=auth_headers
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_get_hidden_tests_requires_auth(client):
    r = await client.get("/api/v1/capstones/test-cap-ht/hidden-tests")
    assert r.status_code in (401, 403)


@pytest.mark.asyncio
async def test_get_hidden_tests_skips_malformed(client, auth_headers):
    """Tests sin `code` o no-dict se filtran (no rompen el endpoint)."""
    await _ensure_capstone(
        "test-cap-mal",
        [
            {"name": "valido", "code": "assert True"},
            {"name": "sin_code"},
            "not-a-dict",
            {"name": "vacio", "code": ""},
        ],
    )
    r = await client.get(
        "/api/v1/capstones/test-cap-mal/hidden-tests", headers=auth_headers
    )
    assert r.status_code == 200
    tests = r.json()["tests"]
    assert len(tests) == 1
    assert tests[0]["name"] == "valido"


# ---------- POST submissions ----------


@pytest.mark.asyncio
async def test_post_submission_all_passed(client, auth_headers):
    await _ensure_capstone(
        "test-cap-sub",
        [{"name": "t1", "code": "assert True"}, {"name": "t2", "code": "assert True"}],
    )
    payload = {
        "files": [{"path": "main.py", "content": "x = 1\n"}],
        "tests_passed": 2,
        "tests_total": 2,
        "test_results": [
            {"name": "t1", "passed": True},
            {"name": "t2", "passed": True},
        ],
    }
    r = await client.post(
        "/api/v1/capstones/test-cap-sub/submissions",
        headers=auth_headers,
        json=payload,
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["status"] == "passed"
    assert body["tests_passed"] == 2
    assert body["tests_total"] == 2


@pytest.mark.asyncio
async def test_post_submission_partial_is_failed(client, auth_headers):
    await _ensure_capstone(
        "test-cap-partial",
        [{"name": "t1", "code": "assert True"}, {"name": "t2", "code": "assert True"}],
    )
    payload = {
        "files": [{"path": "main.py", "content": "x = 1\n"}],
        "tests_passed": 1,
        "tests_total": 2,
        "test_results": [
            {"name": "t1", "passed": True},
            {"name": "t2", "passed": False, "error_message": "AssertionError"},
        ],
    }
    r = await client.post(
        "/api/v1/capstones/test-cap-partial/submissions",
        headers=auth_headers,
        json=payload,
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["status"] == "failed"
    assert body["tests_passed"] == 1
    assert body["test_results"][1]["error_message"] == "AssertionError"


@pytest.mark.asyncio
async def test_post_submission_tests_total_mismatch_rejected(client, auth_headers):
    """No se acepta una submission con `tests_total` distinto al real."""
    await _ensure_capstone(
        "test-cap-mismatch",
        [{"name": "t1", "code": "assert True"}, {"name": "t2", "code": "assert True"}],
    )
    payload = {
        "files": [{"path": "main.py", "content": ""}],
        "tests_passed": 99,
        "tests_total": 99,  # real son 2
        "test_results": [],
    }
    r = await client.post(
        "/api/v1/capstones/test-cap-mismatch/submissions",
        headers=auth_headers,
        json=payload,
    )
    assert r.status_code == 400, r.text


@pytest.mark.asyncio
async def test_post_submission_passed_gt_total_rejected(client, auth_headers):
    await _ensure_capstone("test-cap-bad", [{"name": "t1", "code": "assert True"}])
    payload = {
        "files": [{"path": "main.py", "content": ""}],
        "tests_passed": 5,
        "tests_total": 1,
        "test_results": [{"name": "t1", "passed": True}],
    }
    r = await client.post(
        "/api/v1/capstones/test-cap-bad/submissions",
        headers=auth_headers,
        json=payload,
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_post_submission_requires_auth(client):
    r = await client.post(
        "/api/v1/capstones/test-cap-sub/submissions",
        json={
            "files": [],
            "tests_passed": 0,
            "tests_total": 0,
            "test_results": [],
        },
    )
    assert r.status_code in (401, 403)


@pytest.mark.asyncio
async def test_post_submission_404_on_unknown_slug(client, auth_headers):
    payload = {
        "files": [],
        "tests_passed": 0,
        "tests_total": 0,
        "test_results": [],
    }
    r = await client.post(
        "/api/v1/capstones/no-existe-slug/submissions",
        headers=auth_headers,
        json=payload,
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_post_submission_then_my_submission_returns_it(client, auth_headers):
    """Despues de un POST, el GET /my-submission devuelve la creada."""
    await _ensure_capstone(
        "test-cap-roundtrip",
        [{"name": "t1", "code": "assert True"}],
    )
    payload = {
        "files": [{"path": "main.py", "content": "ok\n"}],
        "tests_passed": 1,
        "tests_total": 1,
        "test_results": [{"name": "t1", "passed": True}],
    }
    r1 = await client.post(
        "/api/v1/capstones/test-cap-roundtrip/submissions",
        headers=auth_headers,
        json=payload,
    )
    assert r1.status_code == 201

    r2 = await client.get(
        "/api/v1/capstones/test-cap-roundtrip/my-submission",
        headers=auth_headers,
    )
    assert r2.status_code == 200
    assert r2.json()["status"] == "passed"
    assert r2.json()["tests_passed"] == 1


@pytest.mark.asyncio
async def test_post_submission_cross_user_isolated(client, user_a, user_b):
    """B no puede leer la submission de A — RLS app-layer."""
    await _ensure_capstone(
        "test-cap-iso-sub",
        [{"name": "t1", "code": "assert True"}],
    )
    payload = {
        "files": [{"path": "main.py", "content": "x\n"}],
        "tests_passed": 1,
        "tests_total": 1,
        "test_results": [{"name": "t1", "passed": True}],
    }
    ra = await client.post(
        "/api/v1/capstones/test-cap-iso-sub/submissions",
        headers=user_a["headers"],
        json=payload,
    )
    assert ra.status_code == 201

    rb = await client.get(
        "/api/v1/capstones/test-cap-iso-sub/my-submission",
        headers=user_b["headers"],
    )
    assert rb.status_code == 404
