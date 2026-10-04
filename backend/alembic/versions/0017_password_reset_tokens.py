"""0017_password_reset_tokens

Revision ID: 0017
Revises: 0016
Create Date: 2026-10-04

Tabla de tokens de recuperación de contraseña.

Nota sobre RLS: esta tabla es "por usuario" pero NO se le habilita Row Level
Security, al contrario que `refresh_tokens` y compañía en la migración 0004.
Las políticas de 0004 filtran por `current_setting('app.current_user_id')`, y
esa variable la setea `get_current_user` (`core/security.py`) a partir del JWT.
Todo el flujo de recuperación ocurre *sin* sesión iniciada —justamente porque
el usuario no puede entrar—, así que no hay `app.current_user_id` que setear y
una política `FORCE ROW LEVEL SECURITY` dejaría la tabla ilegible para el
propio backend. La defensa aquí no es RLS sino el diseño del token: se guarda
hasheado, es de un solo uso y caduca.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0017"
down_revision: Union[str, None] = "0016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("used_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_password_reset_tokens_token_hash"),
        "password_reset_tokens",
        ["token_hash"],
        unique=True,
    )
    op.create_index(
        op.f("ix_password_reset_tokens_user_id"),
        "password_reset_tokens",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_password_reset_tokens_user_used",
        "password_reset_tokens",
        ["user_id", "used_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_password_reset_tokens_user_used", table_name="password_reset_tokens"
    )
    op.drop_index(
        op.f("ix_password_reset_tokens_user_id"), table_name="password_reset_tokens"
    )
    op.drop_index(
        op.f("ix_password_reset_tokens_token_hash"), table_name="password_reset_tokens"
    )
    op.drop_table("password_reset_tokens")
