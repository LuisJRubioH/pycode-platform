"""0006_challenge_completions

Revision ID: 0006
Revises: 0005
Create Date: 2026-05-08 23:55:00.000000

Tabla `challenge_completions`: marca manual de "hecho" sobre un reto.
Una fila por (user, challenge), idempotente vía UNIQUE.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "challenge_completions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("challenge_id", sa.Integer(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["challenge_id"], ["coding_challenges.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "challenge_id", name="uq_challenge_completion"),
    )
    op.create_index(
        op.f("ix_challenge_completions_user_id"),
        "challenge_completions",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_challenge_completions_challenge_id"),
        "challenge_completions",
        ["challenge_id"],
        unique=False,
    )

    # RLS solo en Postgres; mismo patrón que migraciones anteriores.
    if op.get_bind().dialect.name == "postgresql":
        op.execute("ALTER TABLE challenge_completions ENABLE ROW LEVEL SECURITY")
        op.execute(
            """
            CREATE POLICY challenge_completions_select_own ON challenge_completions
            FOR SELECT
            USING (user_id = current_setting('app.current_user_id', true)::int)
            """
        )
        op.execute(
            """
            CREATE POLICY challenge_completions_modify_own ON challenge_completions
            FOR ALL
            USING (user_id = current_setting('app.current_user_id', true)::int)
            WITH CHECK (user_id = current_setting('app.current_user_id', true)::int)
            """
        )


def downgrade() -> None:
    if op.get_bind().dialect.name == "postgresql":
        op.execute(
            "DROP POLICY IF EXISTS challenge_completions_modify_own"
            " ON challenge_completions"
        )
        op.execute(
            "DROP POLICY IF EXISTS challenge_completions_select_own"
            " ON challenge_completions"
        )
        op.execute("ALTER TABLE challenge_completions DISABLE ROW LEVEL SECURITY")

    op.drop_index(
        op.f("ix_challenge_completions_challenge_id"),
        table_name="challenge_completions",
    )
    op.drop_index(
        op.f("ix_challenge_completions_user_id"),
        table_name="challenge_completions",
    )
    op.drop_table("challenge_completions")
