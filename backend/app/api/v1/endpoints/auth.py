"""
Authentication endpoints.
"""

from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    get_password_hash,
    get_current_active_user,
)
from app.core.config import settings
from app.models.refresh_token import RefreshToken
from app.models.user import User, UserProfile
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    Token,
    UserCreate,
    UserResponse,
)

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
@limiter.limit("3/hour")
async def register(
    request: Request, user_data: UserCreate, db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    # Check if user already exists
    result = await db.execute(
        select(User).where(
            (User.email == user_data.email) | (User.username == user_data.username)
        )
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una cuenta con este email",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este nombre de usuario ya está en uso",
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Create user profile
    profile = UserProfile(user_id=new_user.id)
    db.add(profile)
    await db.commit()

    return new_user


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request, login_data: LoginRequest, db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return JWT token."""
    # Find user by email
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()

    # Create access token + refresh token (rotación)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    rt, jti, exp = create_refresh_token(user.id)
    db.add(RefreshToken(user_id=user.id, jti=jti, expires_at=exp))
    await db.commit()

    return Token(
        access_token=access_token,
        refresh_token=rt,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
    )


@router.post("/refresh", response_model=Token)
@limiter.limit("60/hour")
async def refresh(
    request: Request,
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """Rota el refresh token: revoca el actual y emite uno nuevo."""
    try:
        payload = decode_refresh_token(body.refresh_token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh token inválido",
        )
    jti = payload["jti"]
    user_id = int(payload["sub"])

    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.jti == jti, RefreshToken.revoked == False  # noqa: E712
        )
    )
    rt = result.scalar_one_or_none()
    if not rt or rt.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh token revocado o expirado",
        )

    rt.revoked = True
    new_rt, new_jti, new_exp = create_refresh_token(user_id)
    db.add(RefreshToken(user_id=user_id, jti=new_jti, expires_at=new_exp))

    new_access = create_access_token(
        data={"sub": str(user_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one()
    await db.commit()
    return Token(
        access_token=new_access,
        refresh_token=new_rt,
        token_type="bearer",
        user_id=user_id,
        username=user.username,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    """Revoca el refresh token recibido. Idempotente para tokens inválidos."""
    try:
        payload = decode_refresh_token(body.refresh_token)
    except JWTError:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.jti == payload["jti"])
        .values(revoked=True)
    )
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user
