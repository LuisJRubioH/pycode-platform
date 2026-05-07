import pytest

from app.services.llm_provider import (
    GroqProvider,
    LLMProvider,
    OpenAIProvider,
    get_provider,
)


def test_factory_returns_groq_when_configured(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "gsk_test")
    from app.core.config import Settings

    p = get_provider(Settings())
    assert isinstance(p, GroqProvider)


def test_factory_returns_openai_when_configured(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    from app.core.config import Settings

    p = get_provider(Settings())
    assert isinstance(p, OpenAIProvider)


def test_factory_raises_on_unknown_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "cohere")
    from app.core.config import Settings

    with pytest.raises(ValueError, match="LLM_PROVIDER"):
        get_provider(Settings())


@pytest.mark.asyncio
async def test_provider_implements_chat_interface():
    class FakeProvider(LLMProvider):
        async def chat(self, system, user, **kwargs):
            return "stub-response"

    p = FakeProvider()
    out = await p.chat(system="s", user="u")
    assert out == "stub-response"
