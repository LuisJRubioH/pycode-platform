"""Tests del proxy LLM `POST /api/v1/ai/complete` (Track 5).

Cubre:
- requiere autenticacion
- en entorno de test (sin API key -> StubProvider) responde stub determinista
- valida el tope de max_tokens y la longitud del prompt
"""

import pytest


@pytest.mark.asyncio
async def test_complete_requires_auth(client):
    r = await client.post("/api/v1/ai/complete", json={"prompt": "hola"})
    assert r.status_code in (401, 403)


@pytest.mark.asyncio
async def test_complete_returns_stub_without_api_key(client, auth_headers):
    """Sin API key configurada (entorno de test) devuelve un stub determinista."""
    r = await client.post(
        "/api/v1/ai/complete",
        json={"prompt": "Resume que es RAG en una frase."},
        headers=auth_headers,
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["stub"] is True
    assert body["model"] == "stub"
    assert isinstance(body["completion"], str) and body["completion"]


@pytest.mark.asyncio
async def test_complete_rejects_max_tokens_over_cap(client, auth_headers):
    r = await client.post(
        "/api/v1/ai/complete",
        json={"prompt": "hola", "max_tokens": 99999},
        headers=auth_headers,
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_complete_rejects_empty_prompt(client, auth_headers):
    r = await client.post(
        "/api/v1/ai/complete",
        json={"prompt": ""},
        headers=auth_headers,
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_complete_accepts_optional_system_and_temperature(client, auth_headers):
    r = await client.post(
        "/api/v1/ai/complete",
        json={
            "prompt": "hola",
            "system": "Responde en una palabra.",
            "temperature": 0.1,
            "max_tokens": 50,
        },
        headers=auth_headers,
    )
    assert r.status_code == 200, r.text
    assert "completion" in r.json()
