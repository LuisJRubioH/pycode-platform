import pytest
from app.core.database import _get_engine_args


def test_postgres_url_translates_sslmode_to_connect_args():
    """sslmode=require (psycopg) se traduce a connect_args ssl=require (asyncpg)."""
    args = _get_engine_args("postgresql+asyncpg://u:p@host:5432/db?sslmode=require")
    assert "asyncpg" in args["url"]
    assert "sslmode" not in args["url"]
    assert args["connect_args"] == {"ssl": "require"}


def test_postgres_url_without_sslmode_has_no_connect_args():
    args = _get_engine_args("postgresql+asyncpg://u:p@host:5432/db")
    assert "connect_args" not in args


def test_postgres_url_adds_asyncpg_driver_when_missing():
    args = _get_engine_args("postgresql://u:p@host:5432/db?sslmode=require")
    assert args["url"].startswith("postgresql+asyncpg://")
    assert args["connect_args"] == {"ssl": "require"}


def test_sqlite_rejected_in_production():
    with pytest.raises(RuntimeError, match="SQLite no permitido"):
        _get_engine_args("sqlite+aiosqlite:///./pycode.db", environment="production")


def test_sqlite_allowed_in_test_or_dev():
    args = _get_engine_args("sqlite+aiosqlite:///./test.db", environment="test")
    assert "sqlite" in args["url"]
