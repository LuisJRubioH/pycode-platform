"""0012_code_quality_snapshots

Revision ID: 0012
Revises: 0011
Create Date: 2026-05-26 14:00:00.000000

Crea `code_quality_snapshots`: una fila por evaluación con los scores del
evaluador LLM (logic/general) + el score y métricas del análisis estático.
RLS en Postgres (datos por usuario).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0012"
down_revision: Union[str, None] = "0011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == "postgresql"
    json_type = postgresql.JSONB(astext_type=sa.Text()) if is_postgres else sa.JSON()

    op.create_table(
        "code_quality_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "source", sa.String(length=40), nullable=False, server_default="evaluation"
        ),
        sa.Column("reference_id", sa.Integer(), nullable=True),
        sa.Column("logic_score", sa.Integer(), nullable=True),
        sa.Column("general_score", sa.Integer(), nullable=True),
        sa.Column("static_score", sa.Integer(), nullable=True),
        sa.Column("metrics", json_type, nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_code_quality_snapshots_user_id"),
        "code_quality_snapshots",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_code_quality_user_created",
        "code_quality_snapshots",
        ["user_id", "created_at"],
        unique=False,
    )

    if is_postgres:
        op.execute("ALTER TABLE code_quality_snapshots ENABLE ROW LEVEL SECURITY")
        op.execute(
            """
            CREATE POLICY code_quality_select_own ON code_quality_snapshots
            FOR SELECT
            USING (user_id = current_setting('app.current_user_id', true)::int)
            """
        )
        op.execute(
            """
            CREATE POLICY code_quality_modify_own ON code_quality_snapshots
            FOR ALL
            USING (user_id = current_setting('app.current_user_id', true)::int)
            WITH CHECK (user_id = current_setting('app.current_user_id', true)::int)
            """
        )


def downgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == "postgresql"

    if is_postgres:
        op.execute(
            "DROP POLICY IF EXISTS code_quality_modify_own ON code_quality_snapshots"
        )
        op.execute(
            "DROP POLICY IF EXISTS code_quality_select_own ON code_quality_snapshots"
        )
        op.execute("ALTER TABLE code_quality_snapshots DISABLE ROW LEVEL SECURITY")

    op.drop_index("ix_code_quality_user_created", table_name="code_quality_snapshots")
    op.drop_index(
        op.f("ix_code_quality_snapshots_user_id"),
        table_name="code_quality_snapshots",
    )
    op.drop_table("code_quality_snapshots")
