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
    ) -> str: ...


class GroqProvider(LLMProvider):
    #: Los `openai/gpt-oss-*` razonan antes de contestar y esos tokens salen del
    #: MISMO presupuesto que la respuesta. Con el esfuerzo por defecto, el tope
    #: de 700 tokens del tutor se puede gastar entero razonando y devolver
    #: `content` vacio — que es exactamente lo que dispara `_fallback_response`,
    #: el texto generico que tenemos que evitar. Se vio en `/health/llm?ping=1`:
    #: la llamada iba bien y aun asi el `sample` volvia vacio.
    #: `reasoning_effort` no es un kwarg del SDK instalado (groq 0.5.0), asi que
    #: viaja por `extra_body`, que si pasa cualquier version.
    _MODELOS_QUE_RAZONAN = ("gpt-oss",)

    def __init__(self, api_key: str, model: str = "openai/gpt-oss-120b"):
        from groq import AsyncGroq

        self.client = AsyncGroq(api_key=api_key)
        self.model = model

    def _extra_body(self) -> dict:
        if any(m in self.model for m in self._MODELOS_QUE_RAZONAN):
            return {"reasoning_effort": "low"}
        return {}

    async def chat(self, system, user, max_tokens=700, temperature=0.4) -> str:
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            extra_body=self._extra_body(),
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
