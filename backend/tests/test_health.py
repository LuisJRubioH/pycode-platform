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


@pytest.mark.asyncio
async def test_health_llm_ping_marca_respuesta_vacia_como_fallo(client, monkeypatch):
    """Contestar vacio no es estar sano.

    Los `openai/gpt-oss-*` gastan del mismo presupuesto razonando, y si no
    dejan tokens para la respuesta devuelven `content` vacio. El tutor trata
    ese vacio igual que una excepcion: texto de reserva. Para el alumno es el
    mismo fallo, asi que el health check tiene que verlo igual.
    """
    from app.main import settings
    from app.services import llm_provider

    class ProviderMudo(llm_provider.LLMProvider):
        async def chat(self, system, user, max_tokens=700, temperature=0.4):
            return "   "

    monkeypatch.setattr(settings, "GROQ_API_KEY", "gsk_x", raising=False)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "groq", raising=False)
    monkeypatch.setattr(llm_provider, "get_provider", lambda _s: ProviderMudo())

    r = await client.get("/health/llm?ping=1")
    assert r.status_code == 503
    assert r.json()["status"] == "unhealthy"


@pytest.mark.asyncio
async def test_groq_provider_baja_el_esfuerzo_de_razonamiento_en_gpt_oss():
    """Sin esto el tope de tokens se va entero en razonar y no queda respuesta."""
    from app.services.llm_provider import GroqProvider

    gpt_oss = GroqProvider.__new__(GroqProvider)
    gpt_oss.model = "openai/gpt-oss-120b"
    assert gpt_oss._extra_body() == {"reasoning_effort": "low"}

    otro = GroqProvider.__new__(GroqProvider)
    otro.model = "llama-3.1-8b-instant"
    assert otro._extra_body() == {}
