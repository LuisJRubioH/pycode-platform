"""
Rate limiting universal — SlowAPI con keyfunc por user_id (autenticado) o IP.
Tabla de límites consolidada en sec. 9.10 del spec.
"""

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request
from fastapi import Response, status
from fastapi.responses import JSONResponse


def _user_or_ip(request: Request) -> str:
    user_id = getattr(request.state, "user_id", None)
    if user_id:
        return f"user:{user_id}"
    return f"ip:{get_remote_address(request)}"


limiter = Limiter(key_func=_user_or_ip, default_limits=["100/minute"])


async def rate_limit_exceeded_handler(
    request: Request, exc: RateLimitExceeded
) -> Response:
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit excedido. Intenta más tarde."},
        headers={"Retry-After": "60"},
    )


def login_limit():
    return limiter.limit("5/minute")


def register_limit():
    return limiter.limit("3/hour")


def tutor_limit():
    return limiter.limit("50/day")


def submit_limit():
    return limiter.limit("30/minute")
