"""
Abstracción de proveedor LLM (sec. 5.5 del spec).
Default: Groq. Fallback: OpenAI. Stub si no hay API key configurada.
"""
from abc import ABC, abstractmethod

import structlog

logger = structlog.get_logger()


class LLMProvider(ABC):
    @abstractmethod
    async def chat(
        self,
        system: str,
        user: str,
        max_tokens: int = 700,
        temperature: float = 0.4,
    ) -> str:
        ...


class GroqProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        from groq import AsyncGroq

        self.client = AsyncGroq(api_key=api_key)
        self.model = model

    async def chat(self, system, user, max_tokens=700, temperature=0.4) -> str:
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content or ""


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        from openai import AsyncOpenAI

        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def chat(self, system, user, max_tokens=700, temperature=0.4) -> str:
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content or ""


class StubProvider(LLMProvider):
    """Fallback determinístico cuando no hay API key configurada."""

    async def chat(self, system, user, **kwargs) -> str:
        return ""


def get_provider(settings) -> LLMProvider:
    name = settings.LLM_PROVIDER.lower()
    if name == "groq":
        if not settings.GROQ_API_KEY:
            logger.warning("llm.no_api_key", provider="groq")
            return StubProvider()
        return GroqProvider(settings.GROQ_API_KEY, settings.LLM_MODEL)
    if name == "openai":
        if not settings.OPENAI_API_KEY:
            logger.warning("llm.no_api_key", provider="openai")
            return StubProvider()
        return OpenAIProvider(settings.OPENAI_API_KEY, settings.LLM_MODEL)
    raise ValueError(f"LLM_PROVIDER no soportado: {name}")
