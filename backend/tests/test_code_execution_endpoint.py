import pytest


@pytest.mark.asyncio
async def test_run_endpoint_returns_410_gone(client, auth_headers):
    r = await client.post(
        "/api/v1/execute/run",
        json={"code": "print(1)"},
        headers=auth_headers,
    )
    assert r.status_code == 410
    detail = r.json()["detail"].lower()
    assert "cliente" in detail or "pyodide" in detail


@pytest.mark.asyncio
async def test_validate_syntax_accepts_valid_python(client, auth_headers):
    r = await client.post(
        "/api/v1/execute/validate",
        json={"code": "x = 1\nprint(x)"},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["valid"] is True


@pytest.mark.asyncio
async def test_validate_syntax_rejects_invalid_python(client, auth_headers):
    r = await client.post(
        "/api/v1/execute/validate",
        json={"code": "def x(:"},
        headers=auth_headers,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["valid"] is False
    assert "syntax" in body["error"].lower()
