"""WebSocket /ws/tutor — chat de Q&A multi-turn (Fase 1).

Refactor: el WS dejó de ser evaluador. Ahora es un chat puro de
preguntas conceptuales:
- Autenticado por query param `?token=<jwt>` (FastAPI no soporta
  Depends sobre WebSocket de forma directa).
- Mantiene historial conversacional dentro de la sesión y lo persiste
  en `tutor_sessions.messages` para que el alumno pueda recuperar el
  hilo más adelante.
- Usa `TutorGuideService` con su propio system prompt
  (`tutor_guia_python.txt`), independiente del prompt evaluador.

Para evaluar código del editor existe el endpoint REST atómico
`POST /api/v1/tutor/evaluate`.
"""

# flake8: noqa: E501

import json
from datetime import datetime, timezone
from typing import Optional

import structlog
from fastapi import WebSocket, WebSocketDisconnect, status
from jose import JWTError, jwt
from sqlalchemy import select, text

from app.core.config import settings
from app.core.database import async_session_maker
from app.models.learning import TutorSession
from app.models.user import User
from app.services.tutor_guide_service import TutorGuideService

logger = structlog.get_logger()

_MAX_MESSAGE_CHARS = 4000


def _decode_token(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        sub = payload.get("sub")
        return int(sub) if sub is not None else None
    except (JWTError, ValueError):
        return None


async def _set_rls_user(db, user_id: int) -> None:
    bind = db.get_bind()
    if bind.dialect.name == "postgresql":
        await db.execute(
            text("SELECT set_config('app.current_user_id', :uid, true)"),
            {"uid": str(int(user_id))},
        )


async def _load_or_create_session(db, user_id: int) -> TutorSession:
    """Toma la sesión más reciente del usuario o crea una nueva.

    No abrimos sesiones nuevas por cada conexión WS para que el alumno
    pueda continuar la conversación donde la dejó al recargar la pestaña.
    """
    result = await db.execute(
        select(TutorSession)
        .where(TutorSession.user_id == user_id)
        .order_by(TutorSession.updated_at.desc())
        .limit(1)
    )
    sess = result.scalar_one_or_none()
    if sess is not None:
        return sess

    sess = TutorSession(user_id=user_id, messages=[])
    db.add(sess)
    await db.commit()
    await db.refresh(sess)
    return sess


async def tutor_chat_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    user_id = _decode_token(token) if token else None
    if user_id is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    async with async_session_maker() as db:
        await _set_rls_user(db, user_id)
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None or not user.is_active:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        session = await _load_or_create_session(db, user_id)
        history: list[dict] = list(session.messages or [])
        session_id = session.id

    await websocket.accept()
    await websocket.send_json(
        {
            "type": "history",
            "messages": history,
        }
    )

    guide = TutorGuideService()

    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json(
                    {"type": "error", "content": "Mensaje no es JSON valido"}
                )
                continue

            user_message = (payload.get("message") or "").strip()
            if not user_message:
                await websocket.send_json(
                    {"type": "error", "content": "El mensaje no puede ir vacio"}
                )
                continue
            if len(user_message) > _MAX_MESSAGE_CHARS:
                await websocket.send_json(
                    {
                        "type": "error",
                        "content": (
                            f"El mensaje supera {_MAX_MESSAGE_CHARS} "
                            "caracteres; resúmelo o divídelo."
                        ),
                    }
                )
                continue

            try:
                bot_reply = await guide.reply(history, user_message)
            except Exception as exc:
                logger.error("tutor_ws.guide_failed", error=str(exc))
                await websocket.send_json(
                    {
                        "type": "error",
                        "content": "El tutor no pudo responder ahora mismo, intenta de nuevo.",
                    }
                )
                continue

            now_iso = datetime.now(tz=timezone.utc).isoformat()
            history.append({"role": "user", "content": user_message, "ts": now_iso})
            history.append({"role": "bot", "content": bot_reply, "ts": now_iso})

            # Persistir despues de cada turno completo
            async with async_session_maker() as db:
                await _set_rls_user(db, user_id)
                fresh = await db.get(TutorSession, session_id)
                if fresh is not None:
                    fresh.messages = history
                    fresh.updated_at = datetime.utcnow()
                    await db.commit()

            await websocket.send_json({"type": "message", "content": bot_reply})

    except WebSocketDisconnect:
        logger.info("tutor_ws.client_disconnected", user_id=user_id)
    except Exception as exc:
        logger.error("tutor_ws.unhandled", error=str(exc))
        try:
            await websocket.close()
        except Exception:
            pass
