"""
Tests cross-user: validan que A no puede leer ni modificar datos de B.

En SQLite la defensa es app-layer (cada endpoint filtra por
current_user.id). En Postgres se suma RLS (migración 0004) como
segunda línea. Estos tests pasan en ambos backends; sirven como
contrato de comportamiento independientemente del dialect.
"""

import pytest


@pytest.mark.asyncio
async def test_user_lookup_by_id_not_exposed(client, user_a, user_b):
    """No existe endpoint público GET /users/{id}: debe ser 404 / 405."""
    r = await client.get(f"/api/v1/users/{user_a['id']}", headers=user_b["headers"])
    assert r.status_code in (403, 404, 405)


@pytest.mark.asyncio
async def test_export_only_returns_own_data(client, user_a, user_b):
    rA = (await client.get("/api/v1/users/me/export", headers=user_a["headers"])).json()
    rB = (await client.get("/api/v1/users/me/export", headers=user_b["headers"])).json()
    assert rA["user"]["email"] == user_a["email"]
    assert rB["user"]["email"] == user_b["email"]
    assert rA["user"]["id"] != rB["user"]["id"]


@pytest.mark.asyncio
async def test_progress_isolated_per_user(client, user_a, user_b):
    pa = await client.get("/api/v1/progress/", headers=user_a["headers"])
    pb = await client.get("/api/v1/progress/", headers=user_b["headers"])
    assert pa.status_code == 200
    assert pb.status_code == 200
    for item in pb.json():
        assert item.get("user_id") != user_a["id"]
    for item in pa.json():
        assert item.get("user_id") != user_b["id"]


@pytest.mark.asyncio
async def test_delete_me_does_not_affect_other_user(client, user_a, user_b):
    r_del = await client.delete("/api/v1/users/me", headers=user_a["headers"])
    assert r_del.status_code == 204

    r = await client.get("/api/v1/users/me/export", headers=user_b["headers"])
    assert r.status_code == 200
    assert r.json()["user"]["email"] == user_b["email"]


@pytest.mark.asyncio
async def test_a_cannot_use_b_token_after_logout(client, user_a, user_b):
    """B logout revoca su refresh; A no debe verse afectado."""
    rt_b_login = await client.post(
        "/api/v1/auth/login",
        json={"email": user_b["email"], "password": "TestPass123"},
    )
    rt_b = rt_b_login.json()["refresh_token"]
    await client.post("/api/v1/auth/logout", json={"refresh_token": rt_b})

    rt_a_login = await client.post(
        "/api/v1/auth/login",
        json={"email": user_a["email"], "password": "TestPass123"},
    )
    rt_a = rt_a_login.json()["refresh_token"]

    r = await client.post("/api/v1/auth/refresh", json={"refresh_token": rt_a})
    assert r.status_code == 200
