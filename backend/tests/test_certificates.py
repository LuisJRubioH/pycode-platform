"""Tests de los endpoints de certificados (Pieza E).

Cubre:
- gate server-side: no se emite sin un capstone aprobado (403)
- emisión idempotente (mismo código al re-emitir)
- snapshot del nombre del destinatario
- descarga del PDF (bytes `%PDF`, gate aplicado)
- verificación PÚBLICA por código (sin auth)
- aislamiento por usuario en el listado
"""

import pytest
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.capstone import Capstone, CapstoneSubmission


async def _make_capstone(track: str, slug: str) -> int:
    """Crea un capstone activo para `track`; retorna su id."""
    async with async_session_maker() as session:
        existing = (
            await session.execute(select(Capstone).where(Capstone.slug == slug))
        ).scalar_one_or_none()
        if existing is not None:
            return existing.id
        cap = Capstone(
            slug=slug,
            track=track,
            title="Capstone de prueba",
            short_description="Resumen.",
            description="## Detalle",
            requirements=[{"id": "R1", "text": "Algo."}],
            starter_files=[
                {"path": "main.py", "content": "# todo\n", "editable": True}
            ],
            hidden_tests=[{"name": "t", "code": "assert True"}],
            estimated_hours=4,
            difficulty="intermediate",
            order_index=0,
        )
        session.add(cap)
        await session.commit()
        await session.refresh(cap)
        return cap.id


async def _seed_submission(
    user_id: int, capstone_id: int, *, status: str = "passed"
) -> None:
    async with async_session_maker() as session:
        session.add(
            CapstoneSubmission(
                user_id=user_id,
                capstone_id=capstone_id,
                files={"main.py": "print(1)\n"},
                status=status,
                tests_passed=1,
                tests_total=1,
                test_results=[{"name": "t", "passed": True}],
            )
        )
        await session.commit()


# ---------- gate ----------


@pytest.mark.asyncio
async def test_issue_blocked_without_passed_capstone(client, user_a):
    """Sin submission aprobada el gate cierra (403)."""
    track = "track-cert-gate"
    cap_id = await _make_capstone(track, "cap-cert-gate")
    await _seed_submission(user_a["id"], cap_id, status="failed")

    r = await client.post(
        f"/api/v1/certificates/{track}/issue", headers=user_a["headers"]
    )
    assert r.status_code == 403, r.text


@pytest.mark.asyncio
async def test_issue_succeeds_and_snapshots_name(client, user_a):
    track = "track-cert-ok"
    cap_id = await _make_capstone(track, "cap-cert-ok")
    await _seed_submission(user_a["id"], cap_id, status="passed")

    r = await client.post(
        f"/api/v1/certificates/{track}/issue", headers=user_a["headers"]
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["track"] == track
    assert body["recipient_name"] == user_a["username"]
    assert body["verification_code"].startswith("PYC-")


@pytest.mark.asyncio
async def test_issue_is_idempotent(client, user_a):
    track = "track-cert-idem"
    cap_id = await _make_capstone(track, "cap-cert-idem")
    await _seed_submission(user_a["id"], cap_id, status="passed")

    r1 = await client.post(
        f"/api/v1/certificates/{track}/issue", headers=user_a["headers"]
    )
    r2 = await client.post(
        f"/api/v1/certificates/{track}/issue", headers=user_a["headers"]
    )
    assert r1.status_code == 200 and r2.status_code == 200
    assert r1.json()["id"] == r2.json()["id"]
    assert r1.json()["verification_code"] == r2.json()["verification_code"]


# ---------- download ----------


@pytest.mark.asyncio
async def test_download_returns_pdf(client, user_a):
    track = "track-cert-pdf"
    cap_id = await _make_capstone(track, "cap-cert-pdf")
    await _seed_submission(user_a["id"], cap_id, status="passed")

    r = await client.get(
        f"/api/v1/certificates/{track}/download", headers=user_a["headers"]
    )
    assert r.status_code == 200, r.text
    assert r.headers["content-type"] == "application/pdf"
    assert "attachment" in r.headers.get("content-disposition", "")
    assert r.content[:4] == b"%PDF"


@pytest.mark.asyncio
async def test_download_blocked_without_passed_capstone(client, user_a):
    track = "track-cert-pdf-blocked"
    await _make_capstone(track, "cap-cert-pdf-blocked")  # sin submission

    r = await client.get(
        f"/api/v1/certificates/{track}/download", headers=user_a["headers"]
    )
    assert r.status_code == 403, r.text


# ---------- verify (público) ----------


@pytest.mark.asyncio
async def test_verify_valid_code_public(client, user_a):
    track = "track-cert-verify"
    cap_id = await _make_capstone(track, "cap-cert-verify")
    await _seed_submission(user_a["id"], cap_id, status="passed")
    issued = (
        await client.post(
            f"/api/v1/certificates/{track}/issue", headers=user_a["headers"]
        )
    ).json()
    code = issued["verification_code"]

    # Sin auth: la verificación es pública.
    r = await client.get(f"/api/v1/certificates/verify/{code}")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["valid"] is True
    assert body["recipient_name"] == user_a["username"]
    assert body["track"] == track


@pytest.mark.asyncio
async def test_verify_invalid_code_returns_valid_false(client):
    r = await client.get("/api/v1/certificates/verify/PYC-DEAD-BEEF")
    assert r.status_code == 200, r.text
    assert r.json()["valid"] is False


# ---------- list + aislamiento ----------


@pytest.mark.asyncio
async def test_list_requires_auth(client):
    r = await client.get("/api/v1/certificates")
    assert r.status_code in (401, 403)


@pytest.mark.asyncio
async def test_list_isolated_per_user(client, user_a, user_b):
    track = "track-cert-iso"
    cap_id = await _make_capstone(track, "cap-cert-iso")
    await _seed_submission(user_a["id"], cap_id, status="passed")
    await client.post(f"/api/v1/certificates/{track}/issue", headers=user_a["headers"])

    # A ve su certificado.
    ra = await client.get("/api/v1/certificates", headers=user_a["headers"])
    assert ra.status_code == 200
    assert any(c["track"] == track for c in ra.json()["items"])

    # B no ve nada de A.
    rb = await client.get("/api/v1/certificates", headers=user_b["headers"])
    assert rb.status_code == 200
    assert rb.json()["total"] == 0
