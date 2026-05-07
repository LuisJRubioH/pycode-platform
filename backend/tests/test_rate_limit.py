import pytest


@pytest.mark.asyncio
async def test_login_rate_limited_after_5_attempts(client):
    payload = {"email": "x@y.com", "password": "wrongPass1"}
    for i in range(5):
        r = await client.post("/api/v1/auth/login", json=payload)
        assert r.status_code in (401, 422)
    r = await client.post("/api/v1/auth/login", json=payload)
    assert r.status_code == 429
    assert "rate limit" in r.text.lower() or "too many" in r.text.lower()
