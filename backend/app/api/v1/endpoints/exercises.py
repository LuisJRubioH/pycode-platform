"""
Exercises endpoints.
"""

import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.code_evaluation import CodeEvaluation
from app.models.user import User
from app.models.learning import Exercise, CodeSubmission
from app.services.progress_service import (
    completed_exercise_ids,
    recompute_lesson_progress,
)
from app.schemas.evaluation import (
    EvaluationHistoryItem,
    EvaluationHistoryOut,
)
from app.schemas.learning import (
    CodeSubmissionCreate,
    CodeSubmissionResponse,
    ExerciseCheckRequest,
    ExerciseCheckResponse,
    HiddenTest,
    HiddenTestsResponse,
)
from app.services import track0_service

router = APIRouter()


async def _persistir_intento(
    db: AsyncSession,
    user_id: int,
    exercise: Exercise,
    *,
    code: str,
    is_success: bool,
    output: str | None = None,
    error_message: str | None = None,
    execution_time: int = 0,
    passed_tests: int = 0,
    total_tests: int = 0,
) -> tuple[CodeSubmission, bool]:
    """Registra un intento y recalcula el progreso de su lección.

    Único sitio donde se decide qué pasa con un intento, lo mande Pyodide
    (`/submit`) o lo corrija el backend (`/check`, Track 0): un tipo de
    ejercicio nuevo no puede acabar con su propia regla de idempotencia.

    Reintentar un ejercicio **ya aprobado** no crea otra submission ni duplica
    XP/intentos; solo re-sincroniza el progreso por si quedó desfasado
    (datos legacy). Devuelve la submission y si el ejercicio queda hecho.
    """
    ya_aprobado = exercise.id in await completed_exercise_ids(
        db, user_id, [exercise.id]
    )

    if ya_aprobado and is_success:
        anterior = (
            await db.execute(
                select(CodeSubmission)
                .where(
                    CodeSubmission.user_id == user_id,
                    CodeSubmission.exercise_id == exercise.id,
                    CodeSubmission.result == "success",
                )
                .order_by(CodeSubmission.created_at.desc())
                .limit(1)
            )
        ).scalar_one_or_none()
        await recompute_lesson_progress(db, user_id, exercise.lesson_id)
        await db.commit()
        return anterior, True

    submission = CodeSubmission(
        user_id=user_id,
        exercise_id=exercise.id,
        code=code,
        result="success" if is_success else "error",
        output=output,
        error_message=error_message,
        execution_time=execution_time,
        passed_tests=passed_tests,
        total_tests=total_tests,
    )
    db.add(submission)
    await db.flush()  # la submission entra en el cálculo de recompute

    progress = await recompute_lesson_progress(db, user_id, exercise.lesson_id)
    progress.attempts = (progress.attempts or 0) + 1

    await db.commit()
    await db.refresh(submission)
    return submission, is_success or ya_aprobado


@router.get("/lesson/{lesson_id}", response_model=List[dict])
async def get_lesson_exercises(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all exercises for a lesson."""
    result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson_id).order_by(Exercise.order)
    )
    exercises = result.scalars().all()

    exercise_ids = [ex.id for ex in exercises]

    # `completed` sale de la regla única de progress_service. Antes se miraba
    # solo la ÚLTIMA submission, así que un intento fallido posterior a uno
    # exitoso des-completaba el ejercicio aquí pero no en el progreso: dos
    # respuestas distintas para la misma pregunta.
    completed_ids = await completed_exercise_ids(db, current_user.id, exercise_ids)

    # Los intentos sí son un conteo bruto de submissions.
    attempts_rows = (
        await db.execute(
            select(CodeSubmission.exercise_id, func.count(CodeSubmission.id))
            .where(
                CodeSubmission.user_id == current_user.id,
                CodeSubmission.exercise_id.in_(exercise_ids),
            )
            .group_by(CodeSubmission.exercise_id)
        )
    ).all()
    attempts_by_ex = {row[0]: row[1] for row in attempts_rows}

    return [
        {
            "id": ex.id,
            "title": ex.title,
            "description": ex.description,
            "difficulty": ex.difficulty,
            "points": ex.points,
            "starter_code": ex.starter_code,
            "hints": ex.hints[:1] if ex.hints else [],
            "exercise_type": ex.exercise_type,
            "spec": ex.spec or None,
            "completed": ex.id in completed_ids,
            "attempts": attempts_by_ex.get(ex.id, 0),
        }
        for ex in exercises
    ]


@router.post("/{exercise_id}/submit", response_model=CodeSubmissionResponse)
async def submit_exercise(
    exercise_id: int,
    submission: CodeSubmissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Persiste el resultado que el cliente Pyodide reporta para un ejercicio.

    El backend ya no ejecuta código del estudiante (ver Task 14 del plan
    Fase 0). El cliente corre el código en Pyodide y envía success / output
    / passed_tests; aquí registramos la submission y recalculamos el progreso
    de la lección con la regla única de ``progress_service``.

    Idempotente: reintentar un ejercicio **ya aprobado** no crea una nueva
    submission ni duplica XP/intentos; solo re-sincroniza el progreso por si
    quedó desfasado (datos legacy). El score de la lección es derivado
    (Σ points de ejercicios hechos), así que nunca se duplica.
    """
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    total_tests = submission.total_tests or (
        len(exercise.test_cases) if exercise.test_cases else 0
    )
    passed_tests = submission.passed_tests
    is_success = submission.success and (
        total_tests == 0 or passed_tests == total_tests
    )

    code_submission, _ = await _persistir_intento(
        db,
        current_user.id,
        exercise,
        code=submission.code,
        is_success=is_success,
        output=submission.output,
        error_message=submission.error_message,
        execution_time=submission.execution_time_ms or 0,
        passed_tests=passed_tests,
        total_tests=total_tests,
    )
    return code_submission


@router.post("/{exercise_id}/check", response_model=ExerciseCheckResponse)
async def check_exercise(
    exercise_id: int,
    payload: ExerciseCheckRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Corrige un ejercicio que no se ejecuta (Track 0).

    El pseudocódigo y los diagramas no corren en Pyodide, así que la
    corrección la hace el backend con `track0_service`: determinista, sin
    ejecutar nada y sin LLM. La `answer_key` no sale de aquí; lo que vuelve es
    si acertó y **dónde** falla, nunca el valor correcto.

    Aprobar emite el mismo evento que un ejercicio de Python —una
    `CodeSubmission` con `result="success"`—, así que XP, progreso, ELO y
    competencias no se ramifican por tipo de ejercicio.
    """
    exercise = (
        await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    ).scalar_one_or_none()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    if exercise.exercise_type not in track0_service.TIPOS_VALIDABLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Este ejercicio se resuelve escribiendo código: usa "
                "/submit con el resultado de los tests."
            ),
        )

    try:
        veredicto = track0_service.validar(
            exercise.exercise_type, exercise.answer_key, payload.respuesta
        )
    except track0_service.EjercicioInvalido as exc:
        # El ejercicio está mal seedeado: es culpa nuestra, no del alumno.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ejercicio mal configurado: {exc}",
        )

    _, completado = await _persistir_intento(
        db,
        current_user.id,
        exercise,
        code=json.dumps(payload.respuesta, ensure_ascii=False, sort_keys=True),
        is_success=veredicto.passed,
        output=veredicto.feedback,
        error_message=None if veredicto.passed else veredicto.feedback,
        passed_tests=1 if veredicto.passed else 0,
        total_tests=1,
    )

    return ExerciseCheckResponse(
        passed=veredicto.passed,
        feedback=veredicto.feedback,
        detalle=veredicto.detalle,
        completed=completado,
    )


@router.get("/{exercise_id}/hidden-tests", response_model=HiddenTestsResponse)
async def get_hidden_tests(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Tests ocultos del ejercicio para que el worker Pyodide los corra.

    El cliente los recibe solo al pulsar "Ejecutar tests" y los pasa al
    worker; la UI nunca los renderiza, solo muestra verdict por test.
    Otros endpoints (lesson list, lesson detail) NO los exponen.
    """
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    raw_tests = exercise.hidden_tests or []
    tests = [
        HiddenTest(name=t.get("name", ""), code=t.get("code", ""))
        for t in raw_tests
        if isinstance(t, dict) and t.get("code")
    ]
    return HiddenTestsResponse(exercise_id=exercise_id, tests=tests)


@router.get("/{exercise_id}/evaluations", response_model=EvaluationHistoryOut)
async def get_exercise_evaluations(
    exercise_id: int,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Historial de evaluaciones del usuario actual sobre este ejercicio.

    Filtra por user_id para que A nunca vea evaluaciones de B; las RLS
    en Postgres son una segunda línea de defensa pero esta capa app
    impide cualquier filtración antes incluso de tocar la DB.
    """
    limit = max(1, min(limit, 100))
    result = await db.execute(
        select(CodeEvaluation)
        .where(
            CodeEvaluation.user_id == current_user.id,
            CodeEvaluation.exercise_id == exercise_id,
        )
        .order_by(CodeEvaluation.created_at.desc())
        .limit(limit)
    )
    items = result.scalars().all()
    return EvaluationHistoryOut(
        items=[EvaluationHistoryItem.model_validate(e) for e in items],
        total=len(items),
    )


@router.get("/{exercise_id}/hints")
async def get_hints(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all hints for an exercise."""
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    return {"hints": exercise.hints or []}
