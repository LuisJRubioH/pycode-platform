"""0005_code_evaluations

Revision ID: 0005
Revises: 0004
Create Date: 2026-05-08 23:30:00.000000

Crea la tabla `code_evaluations` para persistir cada evaluación
socrática del código del estudiante. Independiente de
`tutor_sessions` (que queda para el chat de Q&A multi-turn).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0005"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == "postgresql"
    verdict_type = postgresql.JSONB(astext_type=sa.Text()) if is_postgres else sa.JSON()

    op.create_table(
        "code_evaluations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=True),
        sa.Column("problem_description", sa.Text(), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("expected_output", sa.Text(), nullable=True),
        sa.Column("actual_output", sa.Text(), nullable=True),
        sa.Column("verdict", verdict_type, nullable=False),
        sa.Column("model_used", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["exercise_id"], ["exercises.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_code_evaluations_user_id"),
        "code_evaluations",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_code_evaluations_exercise_id"),
        "code_evaluations",
        ["exercise_id"],
        unique=False,
    )
    op.create_index(
        "ix_code_evaluations_user_created",
        "code_evaluations",
        ["user_id", "created_at"],
        unique=False,
    )

    # RLS — solo en Postgres. La tabla guarda datos por usuario, así
    # que aplicamos las mismas políticas que las otras tablas con datos
    # de usuario (ver 0004): SELECT/INSERT/UPDATE/DELETE solo cuando
    # `user_id = current_setting('app.current_user_id')`.
    if is_postgres:
        op.execute("ALTER TABLE code_evaluations ENABLE ROW LEVEL SECURITY")
        op.execute(
            """
            CREATE POLICY code_evaluations_select_own ON code_evaluations
            FOR SELECT
            USING (user_id = current_setting('app.current_user_id', true)::int)
            """
        )
        op.execute(
            """
            CREATE POLICY code_evaluations_modify_own ON code_evaluations
            FOR ALL
            USING (user_id = current_setting('app.current_user_id', true)::int)
            WITH CHECK (user_id = current_setting('app.current_user_id', true)::int)
            """
        )


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute(
            "DROP POLICY IF EXISTS code_evaluations_modify_own ON code_evaluations"
        )
        op.execute(
            "DROP POLICY IF EXISTS code_evaluations_select_own ON code_evaluations"
        )
        op.execute("ALTER TABLE code_evaluations DISABLE ROW LEVEL SECURITY")

    op.drop_index("ix_code_evaluations_user_created", table_name="code_evaluations")
    op.drop_index(
        op.f("ix_code_evaluations_exercise_id"), table_name="code_evaluations"
    )
    op.drop_index(op.f("ix_code_evaluations_user_id"), table_name="code_evaluations")
    op.drop_table("code_evaluations")
