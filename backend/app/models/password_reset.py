"""
Token de recuperación de contraseña (un solo uso, con caducidad).
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String

from app.core.database import Base


class PasswordResetToken(Base):
    """Un enlace de recuperación emitido para un usuario.

    En la tabla se guarda el SHA-256 del token, nunca el token en claro: quien
    leyera un volcado de la base de datos tendría si no un pase directo a
    cualquier cuenta que hubiera pedido recuperación. Se usa SHA-256 y no bcrypt
    (que es lo correcto para contraseñas) porque el token hay que *buscarlo* por
    su valor, y con bcrypt habría que recorrer todas las filas probando una a
    una. Es seguro aquí porque el token no es una contraseña elegida por una
    persona sino 32 bytes de `secrets.token_urlsafe`: no hay diccionario que
    valga contra eso.
    """

    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash = Column(String(64), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    #: NULL mientras no se haya canjeado. Un token usado no vuelve a servir.
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_password_reset_tokens_user_used", "user_id", "used_at"),
    )
