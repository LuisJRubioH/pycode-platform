"""
AI Tutor endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.core.security import get_current_active_user
from app.models.user import User
from app.services.ai_tutor import AITutorService

router = APIRouter()
tutor_service = AITutorService()


class TutorMessage(BaseModel):
    message: str
    context: dict = Field(default_factory=dict)


class TutorResponse(BaseModel):
    response: str


@router.post("/ask", response_model=TutorResponse)
@limiter.limit("50/day")
async def ask_tutor(
    request: Request,
    message: TutorMessage,
    current_user: User = Depends(get_current_active_user),
):
    """Ask the AI tutor a question (HTTP endpoint fallback)."""
    try:
        response = await tutor_service.get_response(message.message, message.context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting tutor response: {str(e)}",
        )


@router.post("/feedback")
async def submit_feedback(
    session_id: int,
    message_index: int,
    helpful_rating: int,
    feedback_text: str = "",
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit feedback for a tutor response."""
    # Store feedback in database
    from app.models.learning import AIFeedback

    feedback = AIFeedback(
        session_id=session_id,
        message_index=message_index,
        helpful_rating=helpful_rating,
        feedback_text=feedback_text,
    )
    db.add(feedback)
    await db.commit()

    return {"status": "success", "message": "Feedback recorded"}
