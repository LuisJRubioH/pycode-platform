"""
Database configuration. Postgres + asyncpg en prod, SQLite solo en dev/test.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, StaticPool

from app.core.config import settings


def _get_engine_args(db_url: str | None = None, environment: str | None = None) -> dict:
    db_url = db_url or settings.DATABASE_URL
    environment = environment or settings.ENVIRONMENT

    if db_url.startswith("sqlite"):
        if environment == "production":
            raise RuntimeError("SQLite no permitido en producción — usar Postgres.")
        if "+aiosqlite" not in db_url:
            db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://")
        return {
            "url": db_url,
            "poolclass": StaticPool,
            "echo": settings.DEBUG,
            "connect_args": {"check_same_thread": False},
        }

    if db_url.startswith("postgresql"):
        if "+asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
        return {
            "url": db_url,
            "poolclass": NullPool,
            "echo": settings.DEBUG,
        }

    raise RuntimeError(f"DATABASE_URL no soportado: {db_url[:30]}...")


_engine_args = _get_engine_args()
engine = create_async_engine(**_engine_args)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
