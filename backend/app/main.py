"""
PyCode Platform - Backend Application

FastAPI backend for the Python learning platform with AI tutor.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine
from app.core.security_headers import SecurityHeadersMiddleware
from app.models import challenge  # noqa: F401
from app.models import elo_models  # noqa: F401
from app.models import learning  # noqa: F401
from app.models import user  # noqa: F401
from app.services.challenge_importer import import_external_challenges
from app.services.generated_bank import (
    seed_generated_challenges,
    seed_generated_puzzles,
)
from app.services.lesson_seed import seed_lessons_with_exercises
from app.services.puzzle_seed import seed_interview_puzzles, seed_puzzles_if_empty
from app.websockets.code_execution import code_execution_ws
from app.websockets.tutor_chat import tutor_chat_ws


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

app.add_middleware(SecurityHeadersMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(api_router, prefix="/api/v1")

# WebSocket routes
app.add_api_websocket_route("/ws/code", code_execution_ws)
app.add_api_websocket_route("/ws/tutor", tutor_chat_ws)


@app.get("/")
async def root():
    return {
        "message": "Welcome to PyCode Platform API",
        "version": "0.1.0",
        "docs": "/docs" if settings.DEBUG else None,
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
