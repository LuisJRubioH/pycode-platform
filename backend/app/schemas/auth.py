"""
Authentication and user schemas.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    username: str = Field(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_-]+$",
    )


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("password debe contener al menos un dígito")
        if not any(c.isalpha() for c in v):
            raise ValueError("password debe contener al menos una letra")
        return v


class LoginRequest(BaseModel):
    """Schema for user login (JSON body)."""

    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


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
    token_type: str
    user_id: int
    username: str


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: Optional[int] = None
