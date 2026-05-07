"""enable RLS on per-user tables

Revision ID: 0004
Revises: 0003
Create Date: 2026-05-06

Habilita Row Level Security en todas las tablas con datos por usuario:
políticas USING (user_id = current_setting('app.current_user_id', true)::int)
para SELECT y FOR ALL (con WITH CHECK simétrico). Tabla users usa
id en vez de user_id. Tablas de catálogo público (lessons, exercises,
puzzles) tienen política FOR SELECT USING (true) para mantener
lectura abierta.

SQLite no soporta RLS — la migración es no-op en ese dialect. En tests
contra SQLite la defensa se mueve a la capa de aplicación
(cada endpoint filtra por current_user.id); contra Postgres real la
DB enforza la política aunque el código de aplicación olvide filtrar.

Decisión: usamos current_setting('app.current_user_id') en lugar de
auth.uid() de Supabase porque el backend FastAPI gestiona la auth
con su propio JWT. Cada request setea SET LOCAL app.current_user_id
antes de las queries. Cuando se migre a Supabase Auth (Fase 7) las
policies se reescriben para usar auth.uid().
"""
from typing import Sequence, Union

from alembic import op


revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


PER_USER_TABLES = [
    "user_profiles",
    "user_progress",
    "code_submissions",
    "tutor_sessions",
    "refresh_tokens",
    "puzzle_attempts",
]
PUBLIC_READ_TABLES = [
    "lessons",
    "exercises",
    "puzzles",
]


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    for t in PER_USER_TABLES:
        op.execute(f'ALTER TABLE "{t}" ENABLE ROW LEVEL SECURITY')
        op.execute(f'ALTER TABLE "{t}" FORCE ROW LEVEL SECURITY')
        op.execute(
            f'CREATE POLICY "{t}_select_own" ON "{t}" '
            f"FOR SELECT "
            f"USING (user_id = current_setting('app.current_user_id', true)::int)"
        )
        op.execute(
            f'CREATE POLICY "{t}_modify_own" ON "{t}" '
            f"FOR ALL "
            f"USING (user_id = current_setting('app.current_user_id', true)::int) "
            f"WITH CHECK ("
            f"user_id = current_setting('app.current_user_id', true)::int)"
        )

    op.execute('ALTER TABLE "users" ENABLE ROW LEVEL SECURITY')
    op.execute('ALTER TABLE "users" FORCE ROW LEVEL SECURITY')
    op.execute(
        'CREATE POLICY "users_select_self" ON "users" '
        "FOR SELECT "
        "USING (id = current_setting('app.current_user_id', true)::int)"
    )
    op.execute(
        'CREATE POLICY "users_modify_self" ON "users" '
        "FOR ALL "
        "USING (id = current_setting('app.current_user_id', true)::int) "
        "WITH CHECK (id = current_setting('app.current_user_id', true)::int)"
    )

    for t in PUBLIC_READ_TABLES:
        op.execute(f'ALTER TABLE "{t}" ENABLE ROW LEVEL SECURITY')
        op.execute(f'CREATE POLICY "{t}_public_read" ON "{t}" FOR SELECT USING (true)')


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    for t in PER_USER_TABLES + ["users"] + PUBLIC_READ_TABLES:
        op.execute(f'ALTER TABLE "{t}" DISABLE ROW LEVEL SECURITY')
        op.execute(f'DROP POLICY IF EXISTS "{t}_select_own" ON "{t}"')
        op.execute(f'DROP POLICY IF EXISTS "{t}_modify_own" ON "{t}"')
        op.execute(f'DROP POLICY IF EXISTS "{t}_public_read" ON "{t}"')
        op.execute(f'DROP POLICY IF EXISTS "{t}_select_self" ON "{t}"')
        op.execute(f'DROP POLICY IF EXISTS "{t}_modify_self" ON "{t}"')
