import pytest


@pytest.mark.asyncio
async def test_register_rejects_oversized_password(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "a@b.com",
            "username": "user",
            "password": "x" * 256,
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_rejects_invalid_email(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "not-an-email",
            "username": "user",
            "password": "ValidPass123!",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_rejects_username_with_spaces(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "a@b.com",
            "username": "with space",
            "password": "ValidPass123!",
        },
    )
    assert response.status_code == 422
