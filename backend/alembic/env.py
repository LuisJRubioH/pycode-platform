import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.database import Base, _get_engine_args

# Importa todos los modelos para que Base.metadata los conozca
import app.models.user  # noqa: F401
import app.models.learning  # noqa: F401
import app.models.elo_models  # noqa: F401
import app.models.challenge  # noqa: F401
import app.models.refresh_token  # noqa: F401
import app.models.code_evaluation  # noqa: F401
import app.models.code_quality  # noqa: F401
import app.models.challenge_completion  # noqa: F401
import app.models.capstone  # noqa: F401
import app.models.certificate  # noqa: F401
import app.models.dataset  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    # Reusa _get_engine_args para que la traducción sslmode→ssl (asyncpg)
    # también aplique a las migraciones. Pasar la URL cruda a
    # async_engine_from_config falla en Postgres con `sslmode=require`.
    engine_args = _get_engine_args()
    engine_args["poolclass"] = pool.NullPool
    connectable = create_async_engine(**engine_args)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


run_migrations_online()
