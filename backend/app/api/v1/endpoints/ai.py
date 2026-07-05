"""
Proxy LLM para el Track 5 (AI Engineering).

Permite que el codigo del estudiante (corriendo en Pyodide en el navegador)
haga una llamada real a un LLM **a traves del backend**, sin exponer API keys
en el cliente y con rate limiting + tope de tokens para controlar el costo.
Reutiliza el LLM provider ya configurado (Groq por defecto, ver
`llm_provider.py`).

Si no hay API key (`StubProvider`), devuelve una respuesta placeholder
determinista para que las lecciones y los tests funcionen sin proveedor real.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.security import get_current_active_user
from app.models.user import User
from app.services.llm_provider import StubProvider, get_provider

router = APIRouter()

# El provider se resuelve una vez (igual que en AITutorService).
_provider = get_provider(settings)

MAX_PROMPT_CHARS = 4000
MAX_TOKENS_CAP = 400

_STUB_COMPLETION = (
    "[LLM no configurado en este entorno. En produccion veras aqui la "
    "respuesta real del modelo; tu prompt se recibio correctamente.]"
)


class CompletionRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=MAX_PROMPT_CHARS)
    system: str = Field(default="Eres un asistente conciso y util.", max_length=2000)
    max_tokens: int = Field(default=256, ge=1, le=MAX_TOKENS_CAP)
    temperature: float = Field(default=0.4, ge=0.0, le=1.5)


class CompletionResponse(BaseModel):
    completion: str
    model: str
    stub: bool = False


@router.post("/complete", response_model=CompletionResponse)
@limiter.limit("40/day")
async def complete(
    request: Request,
    payload: CompletionRequest,
    current_user: User = Depends(get_current_active_user),
) -> CompletionResponse:
    """Proxy a una completion de LLM para ejercicios del Track 5.

    Auth requerida + rate limit (40/dia por usuario) + tope de `max_tokens`
    para acotar el costo. Nunca expone la API key del proveedor.
    """
    if isinstance(_provider, StubProvider):
        return CompletionResponse(completion=_STUB_COMPLETION, model="stub", stub=True)

    try:
        content = await _provider.chat(
            system=payload.system,
            user=payload.prompt,
            max_tokens=payload.max_tokens,
            temperature=payload.temperature,
        )
    except Exception as exc:  # pragma: no cover - depende del proveedor externo
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"El proveedor LLM fallo: {exc}",
        )

    return CompletionResponse(
        completion=content.strip(), model=settings.LLM_MODEL, stub=False
    )
