import pytest


@pytest.mark.asyncio
async def test_export_returns_user_data(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "exp@example.com",
            "username": "expuser",
            "password": "TestPass123",
        },
    )
    tok = (
        await client.post(
            "/api/v1/auth/login",
            json={"email": "exp@example.com", "password": "TestPass123"},
        )
    ).json()["access_token"]
    h = {"Authorization": f"Bearer {tok}"}

    r = await client.get("/api/v1/users/me/export", headers=h)
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["email"] == "exp@example.com"
    assert "profile" in data
    assert "progress" in data
    assert "submissions" in data
    assert "tutor_messages" in data
    assert "exported_at" in data


@pytest.mark.asyncio
async def test_delete_me_purges_account(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "del@example.com",
            "username": "deluser",
            "password": "TestPass123",
        },
    )
    tok = (
        await client.post(
            "/api/v1/auth/login",
            json={"email": "del@example.com", "password": "TestPass123"},
        )
    ).json()["access_token"]
    h = {"Authorization": f"Bearer {tok}"}

    r = await client.delete("/api/v1/users/me", headers=h)
    assert r.status_code == 204

    r2 = await client.post(
        "/api/v1/auth/login",
        json={"email": "del@example.com", "password": "TestPass123"},
    )
    assert r2.status_code == 401
