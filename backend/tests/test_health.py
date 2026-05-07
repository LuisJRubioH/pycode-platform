import pytest


@pytest.mark.asyncio
async def test_health_minimal_payload(client):
    r = await client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body == {"status": "healthy"} or set(body.keys()) <= {"status"}


@pytest.mark.asyncio
async def test_root_does_not_leak_version_or_db(client):
    r = await client.get("/")
    body = r.json()
    text = str(body).lower()
    assert "postgres" not in text
    assert "supabase" not in text
    assert "version" not in body or body.get("version", "") in ("", "1.0", "v1")
