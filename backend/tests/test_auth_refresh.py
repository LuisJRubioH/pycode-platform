import pytest


@pytest.mark.asyncio
async def test_login_returns_refresh_token(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "rt@example.com",
            "username": "rtuser",
            "password": "TestPass123",
        },
    )
    r = await client.post(
        "/api/v1/auth/login",
        json={"email": "rt@example.com", "password": "TestPass123"},
    )
    body = r.json()
    assert "refresh_token" in body
    assert "access_token" in body


@pytest.mark.asyncio
async def test_refresh_rotates_token(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "rot@example.com",
            "username": "rotuser",
            "password": "TestPass123",
        },
    )
    login = (
        await client.post(
            "/api/v1/auth/login",
            json={"email": "rot@example.com", "password": "TestPass123"},
        )
    ).json()
    rt1 = login["refresh_token"]

    r1 = await client.post("/api/v1/auth/refresh", json={"refresh_token": rt1})
    assert r1.status_code == 200
    rt2 = r1.json()["refresh_token"]
    assert rt2 != rt1

    r2 = await client.post("/api/v1/auth/refresh", json={"refresh_token": rt1})
    assert r2.status_code == 401


@pytest.mark.asyncio
async def test_logout_revokes_refresh_token(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "lo@example.com",
            "username": "louser",
            "password": "TestPass123",
        },
    )
    login = (
        await client.post(
            "/api/v1/auth/login",
            json={"email": "lo@example.com", "password": "TestPass123"},
        )
    ).json()
    rt = login["refresh_token"]

    r_logout = await client.post("/api/v1/auth/logout", json={"refresh_token": rt})
    assert r_logout.status_code == 204

    r = await client.post("/api/v1/auth/refresh", json={"refresh_token": rt})
    assert r.status_code == 401
