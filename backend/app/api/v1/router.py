"""
Main API router for version 1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    lessons,
    exercises,
    code_execution,
    tutor,
    progress,
    elo,
    challenges,
    capstones,
    certificates,
    datasets,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
api_router.include_router(
    code_execution.router, prefix="/execute", tags=["code execution"]
)
api_router.include_router(tutor.router, prefix="/tutor", tags=["AI tutor"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_router.include_router(elo.router, prefix="/elo", tags=["elo"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
api_router.include_router(capstones.router, prefix="/capstones", tags=["capstones"])
api_router.include_router(
    certificates.router, prefix="/certificates", tags=["certificates"]
)
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
