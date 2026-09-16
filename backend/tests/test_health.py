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


@pytest.mark.asyncio
async def test_health_llm_reporta_degradado_sin_api_key(client, monkeypatch):
    """Sin API key el endpoint debe decirlo en vez de dar verde.

    Es el punto del endpoint: `/health` y `/health/db` seguian en verde
    mientras el tutor devolvia su texto de reserva.
    """
    from app.main import settings

    monkeypatch.setattr(settings, "GROQ_API_KEY", "", raising=False)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "groq", raising=False)

    r = await client.get("/health/llm")
    assert r.status_code == 503
    body = r.json()
    assert body["status"] == "degraded"
    assert body["api_key_configured"] is False


@pytest.mark.asyncio
async def test_health_llm_nunca_expone_la_api_key(client, monkeypatch):
    from app.main import settings

    secreta = "gsk_clave_que_no_debe_salir_nunca"
    monkeypatch.setattr(settings, "GROQ_API_KEY", secreta, raising=False)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "groq", raising=False)

    r = await client.get("/health/llm")
    assert secreta not in r.text
    assert r.json()["api_key_configured"] is True


@pytest.mark.asyncio
async def test_health_llm_ping_falla_con_modelo_retirado(client, monkeypatch):
    """Un modelo que ya no se sirve tiene que salir como `unhealthy`.

    Reproduce el fallo real: Groq retiro `llama-3.3-70b-versatile` el
    2026-08-16 y el tutor lo enmascaro durante semanas con su fallback.
    """
    from app.main import settings
    from app.services import llm_provider

    class ProviderMuerto(llm_provider.LLMProvider):
        async def chat(self, system, user, max_tokens=700, temperature=0.4):
            raise RuntimeError(
                "model_decommissioned: The model `llama-3.3-70b-versatile` "
                "has been decommissioned (key gsk_deberia_redactarse)"
            )

    monkeypatch.setattr(settings, "GROQ_API_KEY", "gsk_x", raising=False)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "groq", raising=False)
    monkeypatch.setattr(llm_provider, "get_provider", lambda _s: ProviderMuerto())

    r = await client.get("/health/llm?ping=1")
    assert r.status_code == 503
    body = r.json()
    assert body["status"] == "unhealthy"
    assert "model_decommissioned" in body["reason"]
    assert "gsk_deberia_redactarse" not in r.text
