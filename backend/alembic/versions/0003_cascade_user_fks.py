"""0003_cascade_user_fks

Revision ID: 0003
Revises: 0002
Create Date: 2026-05-06

Habilita ON DELETE CASCADE en FKs hacia users.id para que DELETE
/users/me purgue datos relacionados sin orphans (sec. 9.13 del spec,
GDPR).

SQLite no soporta DROP/CREATE CONSTRAINT, así que la migración es
no-op en ese dialect. Para tests SQLite el cascade lo provee
SQLAlchemy ORM relationships; para Postgres prod la constraint queda
enforced en DB.
"""
from typing import Sequence, Union

from alembic import op


revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_USER_FK_TABLES = [
    ("code_submissions", "code_submissions_user_id_fkey"),
    ("puzzle_attempts", "puzzle_attempts_user_id_fkey"),
    ("tutor_sessions", "tutor_sessions_user_id_fkey"),
    ("user_profiles", "user_profiles_user_id_fkey"),
    ("user_progress", "user_progress_user_id_fkey"),
]


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return
    for table, fk_name in _USER_FK_TABLES:
        op.drop_constraint(fk_name, table, type_="foreignkey")
        op.create_foreign_key(
            fk_name,
            table,
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE",
        )


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return
    for table, fk_name in _USER_FK_TABLES:
        op.drop_constraint(fk_name, table, type_="foreignkey")
        op.create_foreign_key(
            fk_name,
            table,
            "users",
            ["user_id"],
            ["id"],
        )
