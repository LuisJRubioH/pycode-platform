"""
Database configuration and connection.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, StaticPool

from app.core.config import settings


def _get_engine_args():
    """Get the correct engine arguments based on the database URL."""
    db_url = settings.DATABASE_URL

    # SQLite (development)
    if db_url.startswith("sqlite"):
        # Ensure we use the async driver
        if "+aiosqlite" not in db_url:
            db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://")
        return {
            "url": db_url,
            "poolclass": StaticPool,
            "echo": settings.DEBUG,
            "connect_args": {"check_same_thread": False},
        }

    # PostgreSQL (production)
    if db_url.startswith("postgresql"):
        # Ensure we use the async driver
        if "+asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
        return {
            "url": db_url,
            "poolclass": NullPool,
            "echo": settings.DEBUG,
        }

    # Fallback: use URL as-is
    return {
        "url": db_url,
        "poolclass": NullPool,
        "echo": settings.DEBUG,
    }


# Create async engine with correct settings for the database type
_engine_args = _get_engine_args()
engine = create_async_engine(**_engine_args)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create declarative base
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Get database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
