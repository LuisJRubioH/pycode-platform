# backend/tests/conftest.py
import os
import pathlib
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_pycode.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-prod")
os.environ.setdefault("ENVIRONMENT", "test")

_TEST_DB_PATH = pathlib.Path(__file__).resolve().parents[1] / "test_pycode.db"
if _TEST_DB_PATH.exists():
    _TEST_DB_PATH.unlink()

from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402

_ALEMBIC_INI = pathlib.Path(__file__).resolve().parents[1] / "alembic.ini"
_alembic_cfg = Config(str(_ALEMBIC_INI))
command.upgrade(_alembic_cfg, "head")

from app.main import app  # noqa: E402


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
