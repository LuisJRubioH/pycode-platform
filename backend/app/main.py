"""
PyCode Platform - Backend Application

FastAPI backend for the Python learning platform with AI tutor.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine
from app.core.logging_config import configure_logging
from app.core.observability import init_sentry
from app.core.rate_limit import limiter, rate_limit_exceeded_handler
from app.core.security_headers import SecurityHeadersMiddleware
from app.models import capstone  # noqa: F401
from app.models import certificate  # noqa: F401
from app.models import challenge  # noqa: F401
from app.models import challenge_completion  # noqa: F401
from app.models import code_evaluation  # noqa: F401
from app.models import elo_models  # noqa: F401
from app.models import learning  # noqa: F401
from app.models import refresh_token  # noqa: F401
from app.models import user  # noqa: F401
from app.services.capstone_seed import seed_capstones_if_empty
from app.services.challenge_importer import import_external_challenges
from app.services.generated_bank import (
    seed_generated_challenges,
    seed_generated_puzzles,
)
from app.services.lesson_seed import seed_lessons_with_exercises
from app.services.puzzle_seed import seed_interview_puzzles, seed_puzzles_if_empty
from app.websockets.code_execution import code_execution_ws
from app.websockets.tutor_chat import tutor_chat_ws

configure_logging()
init_sentry()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    # Schema gestionado por Alembic. Aplica `alembic upgrade head` antes del startup.
    from app.core.database import async_session_maker

    async with async_session_maker() as session:
        await seed_puzzles_if_empty(session)
        await seed_interview_puzzles(session)
        await seed_generated_puzzles(session)
        await import_external_challenges(session)
        await seed_generated_challenges(session)
        await seed_lessons_with_exercises(session)
        await seed_capstones_if_empty(session)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(SecurityHeadersMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
    max_age=600,
)

# API routes
app.include_router(api_router, prefix="/api/v1")

# WebSocket routes
app.add_api_websocket_route("/ws/code", code_execution_ws)
app.add_api_websocket_route("/ws/tutor", tutor_chat_ws)


@app.get("/")
async def root():
    return {"message": "PyCode Platform"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
