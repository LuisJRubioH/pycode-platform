"""0008_capstones

Revision ID: 0008
Revises: 0007
Create Date: 2026-05-25 18:00:00.000000

Crea las tablas `capstones` (definicional, seeded por Track) y
`capstone_submissions` (lo que envió cada usuario).

`capstone_submissions` lleva RLS en Postgres (datos por usuario);
`capstones` es público (todos los usuarios ven la lista del catálogo).
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0008"
down_revision: Union[str, None] = "0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _json_type(is_postgres: bool):
    return postgresql.JSONB(astext_type=sa.Text()) if is_postgres else sa.JSON()


def upgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == "postgresql"
    json_type = _json_type(is_postgres)

    op.create_table(
        "capstones",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("track", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("short_description", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requirements", json_type, nullable=False),
        sa.Column("starter_files", json_type, nullable=False),
        sa.Column(
            "hidden_tests",
            json_type,
            nullable=False,
            server_default=sa.text("'[]'"),
        ),
        sa.Column("estimated_hours", sa.Integer(), nullable=False, server_default="8"),
        sa.Column(
            "difficulty",
            sa.String(length=20),
            nullable=False,
            server_default="intermediate",
        ),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_capstones_slug"), "capstones", ["slug"], unique=True)
    op.create_index(op.f("ix_capstones_track"), "capstones", ["track"], unique=False)

    op.create_table(
        "capstone_submissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("capstone_id", sa.Integer(), nullable=False),
        sa.Column("files", json_type, nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("tests_passed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tests_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("test_results", json_type, nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["capstone_id"], ["capstones.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_capstone_submissions_user_id"),
        "capstone_submissions",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_capstone_submissions_capstone_id"),
        "capstone_submissions",
        ["capstone_id"],
        unique=False,
    )
    op.create_index(
        "ix_capstone_submissions_user_capstone",
        "capstone_submissions",
        ["user_id", "capstone_id"],
        unique=False,
    )

    if is_postgres:
        op.execute("ALTER TABLE capstone_submissions ENABLE ROW LEVEL SECURITY")
        op.execute("""
            CREATE POLICY capstone_submissions_select_own ON capstone_submissions
            FOR SELECT
            USING (user_id = current_setting('app.current_user_id', true)::int)
            """)
        op.execute("""
            CREATE POLICY capstone_submissions_modify_own ON capstone_submissions
            FOR ALL
            USING (user_id = current_setting('app.current_user_id', true)::int)
            WITH CHECK (user_id = current_setting('app.current_user_id', true)::int)
            """)


def downgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == "postgresql"

    if is_postgres:
        op.execute(
            "DROP POLICY IF EXISTS capstone_submissions_modify_own "
            "ON capstone_submissions"
        )
        op.execute(
            "DROP POLICY IF EXISTS capstone_submissions_select_own "
            "ON capstone_submissions"
        )
        op.execute("ALTER TABLE capstone_submissions DISABLE ROW LEVEL SECURITY")

    op.drop_index(
        "ix_capstone_submissions_user_capstone",
        table_name="capstone_submissions",
    )
    op.drop_index(
        op.f("ix_capstone_submissions_capstone_id"),
        table_name="capstone_submissions",
    )
    op.drop_index(
        op.f("ix_capstone_submissions_user_id"),
        table_name="capstone_submissions",
    )
    op.drop_table("capstone_submissions")

    op.drop_index(op.f("ix_capstones_track"), table_name="capstones")
    op.drop_index(op.f("ix_capstones_slug"), table_name="capstones")
    op.drop_table("capstones")
