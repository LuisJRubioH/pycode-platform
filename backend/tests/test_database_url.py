import pytest
from app.core.database import _get_engine_args


def test_postgres_url_keeps_sslmode():
    args = _get_engine_args("postgresql+asyncpg://u:p@host:5432/db?sslmode=require")
    assert "asyncpg" in args["url"]
    assert "sslmode=require" in args["url"]


def test_sqlite_rejected_in_production():
    with pytest.raises(RuntimeError, match="SQLite no permitido"):
        _get_engine_args("sqlite+aiosqlite:///./pycode.db", environment="production")


def test_sqlite_allowed_in_test_or_dev():
    args = _get_engine_args("sqlite+aiosqlite:///./test.db", environment="test")
    assert "sqlite" in args["url"]
