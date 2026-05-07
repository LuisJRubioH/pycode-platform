import pytest


@pytest.mark.asyncio
async def test_health_includes_security_headers(client):
    r = await client.get("/health")
    h = r.headers
    assert "strict-transport-security" in h
    assert "max-age=31536000" in h["strict-transport-security"]
    assert h["x-content-type-options"] == "nosniff"
    assert h["x-frame-options"] == "DENY"
    assert "referrer-policy" in h
    assert "content-security-policy" in h
    assert "geolocation=()" in h.get("permissions-policy", "")


@pytest.mark.asyncio
async def test_csp_allows_pyodide_cdn(client):
    r = await client.get("/health")
    csp = r.headers["content-security-policy"]
    assert "https://cdn.jsdelivr.net" in csp
    assert "wasm-unsafe-eval" in csp
