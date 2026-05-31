"""
Endpoint de validación de código (no ejecuta — la ejecución vive en cliente Pyodide).
"""

import ast
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from app.core.rate_limit import limiter
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()


class CodeValidateRequest(BaseModel):
    code: str = Field(min_length=1, max_length=20000)


class CodeValidateResponse(BaseModel):
    valid: bool
    error: str | None = None


@router.post("/run", status_code=410)
async def run_deprecated():
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail=(
            "Ejecución de código en backend deshabilitada. "
            "El cliente debe usar Pyodide para ejecutar localmente."
        ),
    )


@router.post("/validate", response_model=CodeValidateResponse)
@limiter.limit("60/minute")
async def validate_syntax(
    request: Request,
    body: CodeValidateRequest,
    current_user: User = Depends(get_current_active_user),
) -> CodeValidateResponse:
    try:
        ast.parse(body.code)
        return CodeValidateResponse(valid=True)
    except SyntaxError as e:
        return CodeValidateResponse(
            valid=False, error=f"SyntaxError: {e.msg} (line {e.lineno})"
        )
