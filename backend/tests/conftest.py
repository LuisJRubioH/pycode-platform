# backend/tests/conftest.py
import os
import pathlib
import uuid
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

from app.core.rate_limit import limiter  # noqa: E402
from app.main import app  # noqa: E402

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    limiter.reset()
    yield


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def auth_headers(client):
    """Registra un usuario único y devuelve los headers Authorization."""
    suffix = uuid.uuid4().hex[:8]
    email = f"test_{suffix}@example.com"
    username = f"u{suffix}"
    password = "TestPass123"

    rr = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "username": username, "password": password},
    )
    rl = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    body = rl.json()
    if "access_token" not in body:
        raise RuntimeError(
            f"auth_headers login falló: register={rr.status_code} "
            f"{rr.text[:200]} | login={rl.status_code} {rl.text[:200]}"
        )
    return {"Authorization": f"Bearer {body['access_token']}"}
