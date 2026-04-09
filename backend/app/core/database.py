"""
Database configuration and connection.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    poolclass=NullPool,
    echo=settings.DEBUG,
)

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
