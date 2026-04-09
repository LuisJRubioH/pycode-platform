"""
Main API router for version 1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, lessons, exercises, code_execution, tutor, progress

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
api_router.include_router(code_execution.router, prefix="/execute", tags=["code execution"])
api_router.include_router(tutor.router, prefix="/tutor", tags=["AI tutor"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
