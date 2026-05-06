"""
Code execution endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

from app.core.security import get_current_active_user
from app.models.user import User
from app.services.docker_executor import DockerCodeExecutor

router = APIRouter()


class CodeExecutionRequest(BaseModel):
    """Request to execute Python code."""

    code: str = Field(..., min_length=1, max_length=10000)
    language: str = "python"
    timeout: Optional[int] = 30


class CodeExecutionResponse(BaseModel):
    """Response from code execution."""

    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float
    memory_used: Optional[int] = None


@router.post("/run", response_model=CodeExecutionResponse)
async def execute_code(
    request: CodeExecutionRequest, current_user: User = Depends(get_current_active_user)
):
    """Execute Python code in secure Docker container."""
    try:
        executor = DockerCodeExecutor(
            user_id=str(current_user.id), timeout=request.timeout
        )

        result = await executor.run_python_code(request.code)

        return CodeExecutionResponse(
            success=result["success"],
            output=result.get("stdout", ""),
            error=result.get("stderr", None),
            execution_time=result.get("execution_time", 0.0),
            memory_used=result.get("memory_used"),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code execution failed: {str(e)}",
        )
