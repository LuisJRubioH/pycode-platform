"""
Authentication and user schemas.
"""

import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

#: Nombre de usuario: letras SIN tilde, dígitos, guion bajo y guion.
_USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]+$")

USERNAME_MIN = 3
USERNAME_MAX = 32
PASSWORD_MIN = 8
PASSWORD_MAX = 128


def validar_username(v: str) -> str:
    """Reglas del nombre de usuario, con el motivo en español.

    Las restricciones NO van en `Field(min_length=..., pattern=...)` a propósito.
    Pydantic las reporta con su texto en inglés —"String should match pattern
    '^[a-zA-Z0-9_-]+$'"— y el formulario pintaba ese mensaje crudo en un aviso
    genérico, sin decir de qué campo hablaba: un alumno lo leyó como un problema
    de la contraseña y estuvo cambiándola intento tras intento mientras el campo
    que fallaba era este. Validándolo a mano controlamos el texto, y el `loc` del
    422 sigue diciendo `username` para que el front lo pinte en su campo.
    """
    if len(v) < USERNAME_MIN:
        raise ValueError(
            f"El nombre de usuario debe tener al menos {USERNAME_MIN} caracteres"
        )
    if len(v) > USERNAME_MAX:
        raise ValueError(
            f"El nombre de usuario no puede pasar de {USERNAME_MAX} caracteres"
        )
    if not _USERNAME_RE.match(v):
        raise ValueError(
            "El nombre de usuario solo admite letras sin tilde, números, "
            "guion bajo (_) y guion (-): no se permiten espacios, puntos, "
            "tildes ni la ñ"
        )
    return v


def validar_password(v: str) -> str:
    """Reglas de la contraseña, con el motivo en español. Ver `validar_username`."""
    if len(v) < PASSWORD_MIN:
        raise ValueError(f"La contraseña debe tener al menos {PASSWORD_MIN} caracteres")
    if len(v) > PASSWORD_MAX:
        raise ValueError(f"La contraseña no puede pasar de {PASSWORD_MAX} caracteres")
    if not any(c.isdigit() for c in v):
        raise ValueError("La contraseña debe contener al menos un número")
    if not any(c.isalpha() for c in v):
        raise ValueError("La contraseña debe contener al menos una letra")
    return v


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    username: str

    @field_validator("username")
    @classmethod
    def _username(cls, v: str) -> str:
        return validar_username(v)


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str

    @field_validator("password")
    @classmethod
    def _password(cls, v: str) -> str:
        return validar_password(v)


class LoginRequest(BaseModel):
    """Schema for user login (JSON body)."""

    email: EmailStr
    password: str = Field(..., min_length=1, max_length=PASSWORD_MAX)


class PasswordResetRequest(BaseModel):
    """Petición de enlace de recuperación."""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Canje del token por una contraseña nueva."""

    token: str = Field(..., min_length=16, max_length=256)
    password: str

    @field_validator("password")
    @classmethod
    def _password(cls, v: str) -> str:
        return validar_password(v)


class UserResponse(UserBase):
    """Schema for user response."""

    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    username: str


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: Optional[int] = None


class RefreshRequest(BaseModel):
    refresh_token: str
