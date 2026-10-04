"""
Recuperación de contraseña: emisión y canje de tokens de un solo uso.
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import quote

import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.password_reset import PasswordResetToken
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.services.email_provider import get_email_provider

logger = structlog.get_logger()

#: 32 bytes de CSPRNG -> 43 caracteres url-safe. Lo bastante ancho para que
#: adivinarlo no sea una estrategia, y corto para caber en una URL sin romperse
#: al pegarlo desde el cliente de correo.
TOKEN_BYTES = 32

#: Ventana mínima entre dos correos al mismo usuario. El rate limit del endpoint
#: es por IP y no frena a quien pida el reset de una víctima desde varias; esto
#: sí, porque cuelga del usuario destino.
ESPERA_ENTRE_ENVIOS = timedelta(minutes=2)


def hash_token(token: str) -> str:
    """SHA-256 en hex. Ver el porqué en `models/password_reset.py`."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _ahora() -> datetime:
    # datetime.utcnow() naive, como el resto de columnas DateTime del proyecto.
    return datetime.utcnow()


async def _envio_demasiado_reciente(db: AsyncSession, user_id: int) -> bool:
    corte = _ahora() - ESPERA_ENTRE_ENVIOS
    result = await db.execute(
        select(PasswordResetToken.id).where(
            PasswordResetToken.user_id == user_id,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.created_at > corte,
        )
    )
    return result.first() is not None


async def crear_token(db: AsyncSession, user: User) -> Optional[str]:
    """Emite un token nuevo e invalida los anteriores del mismo usuario.

    Devuelve el token en claro (el único momento en que existe) o None si se
    pidió otro antes de que pasara `ESPERA_ENTRE_ENVIOS`.
    """
    if await _envio_demasiado_reciente(db, user.id):
        logger.info("password_reset_throttled", user_id=user.id)
        return None

    # Pedir un enlace nuevo invalida el anterior: si no, cada petición dejaría
    # otra llave válida suelta en otro buzón.
    await db.execute(
        update(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        )
        .values(used_at=_ahora())
    )

    token = secrets.token_urlsafe(TOKEN_BYTES)
    db.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=hash_token(token),
            expires_at=_ahora()
            + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_TTL_MINUTES),
        )
    )
    await db.commit()
    return token


async def token_valido(db: AsyncSession, token: str) -> Optional[PasswordResetToken]:
    """La fila del token si sirve ahora mismo; None si no existe, ya se usó o caducó."""
    result = await db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == hash_token(token)
        )
    )
    fila = result.scalar_one_or_none()
    if fila is None or fila.used_at is not None or fila.expires_at < _ahora():
        return None
    return fila


async def consumir_token(
    db: AsyncSession, token: str, nueva_password_hash: str
) -> bool:
    """Canjea el token: cambia la contraseña, lo marca usado y cierra las sesiones.

    Revocar los refresh tokens es parte del arreglo, no un extra: si alguien se
    había metido en la cuenta, cambiar la contraseña sin echarlo lo dejaría
    dentro con su sesión viva.
    """
    fila = await token_valido(db, token)
    if fila is None:
        return False

    result = await db.execute(select(User).where(User.id == fila.user_id))
    user = result.scalar_one_or_none()
    if user is None:  # cuenta borrada entre la petición y el canje
        return False

    user.hashed_password = nueva_password_hash
    fila.used_at = _ahora()
    await db.execute(
        update(RefreshToken)
        .where(
            RefreshToken.user_id == user.id,
            RefreshToken.revoked == False,  # noqa: E712
        )
        .values(revoked=True)
    )
    await db.commit()
    logger.info("password_reset_consumido", user_id=user.id)
    return True


def _enlace(token: str) -> str:
    base = settings.FRONTEND_URL.rstrip("/")
    return f"{base}/reset-password?token={quote(token)}"


def construir_correo(username: str, token: str) -> tuple[str, str, str]:
    """(asunto, html, texto) del correo de recuperación."""
    enlace = _enlace(token)
    minutos = settings.PASSWORD_RESET_TOKEN_TTL_MINUTES
    asunto = "Recupera tu contraseña de PyCode"
    texto = (
        f"Hola {username}:\n\n"
        "Pediste recuperar la contraseña de tu cuenta en PyCode. "
        f"Abre este enlace para elegir una nueva:\n\n{enlace}\n\n"
        f"El enlace caduca en {minutos} minutos y solo se puede usar una vez.\n\n"
        "Si no fuiste tú, no hace falta que hagas nada: tu contraseña sigue "
        "siendo la misma.\n"
    )
    html = f"""<!doctype html>
<html lang="es">
  <body style="font-family: system-ui, sans-serif; color: #1e293b; line-height: 1.6;">
    <p>Hola <strong>{username}</strong>:</p>
    <p>
      Pediste recuperar la contraseña de tu cuenta en PyCode.
      Pulsa el botón para elegir una nueva:
    </p>
    <p>
      <a href="{enlace}"
         style="display: inline-block; padding: 12px 20px; background: #2563eb;
                color: #ffffff; text-decoration: none; border-radius: 6px;">
        Elegir contraseña nueva
      </a>
    </p>
    <p style="font-size: 14px; color: #475569;">
      O copia este enlace: <br /><a href="{enlace}">{enlace}</a>
    </p>
    <p style="font-size: 14px; color: #475569;">
      El enlace caduca en {minutos} minutos y solo se puede usar una vez.
    </p>
    <p style="font-size: 14px; color: #475569;">
      Si no fuiste tú, no hace falta que hagas nada: tu contraseña sigue siendo
      la misma.
    </p>
  </body>
</html>"""
    return asunto, html, texto


async def enviar_correo_de_recuperacion(user: User, token: str) -> bool:
    asunto, html, texto = construir_correo(user.username, token)
    proveedor = get_email_provider(settings)
    return await proveedor.send(to=user.email, subject=asunto, html=html, text=texto)
