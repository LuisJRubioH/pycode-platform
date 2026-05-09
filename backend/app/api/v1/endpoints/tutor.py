"""
AI Tutor endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.core.security import get_current_active_user
from app.models.code_evaluation import CodeEvaluation
from app.models.user import User
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse
from app.services.ai_tutor import AITutorService
from app.services.evaluation_service import EvaluationService

router = APIRouter()
tutor_service = AITutorService()
evaluation_service = EvaluationService(tutor_service)


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


@router.post(
    "/evaluate",
    response_model=EvaluationResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/hour")
async def evaluate_code(
    request: Request,
    payload: EvaluationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Evalúa un intento de código del estudiante de forma atómica.

    A diferencia del WS `/ws/tutor`, este endpoint NO mantiene historial
    conversacional: cada llamada produce una `CodeEvaluation` con su
    verdict, persistida en la DB para construir métricas de progreso.
    """
    try:
        verdict = await evaluation_service.evaluate(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"El evaluador no pudo procesar el codigo: {exc}",
        )

    record = CodeEvaluation(
        user_id=current_user.id,
        exercise_id=payload.exercise_id,
        problem_description=payload.problem_description,
        code=payload.code,
        expected_output=payload.expected_output,
        actual_output=payload.actual_output,
        verdict=verdict.model_dump(),
        model_used=evaluation_service.model_used,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


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
