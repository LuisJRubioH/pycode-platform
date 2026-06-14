"""0010_elo_ratings

Revision ID: 0010
Revises: 0009
Create Date: 2026-05-26 12:00:00.000000

Crea `elo_ratings` (un rating ELO por (usuario, dominio, scope)) y añade la
columna `domain` a `elo_history` para separar el timeline por track.

`elo_ratings` lleva RLS en Postgres (datos por usuario). El add de columna en
`elo_history` usa batch_alter_table para ser no-op-safe en SQLite (los tests
corren con SQLite).
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0010"
down_revision: Union[str, None] = "0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == "postgresql"

    op.create_table(
        "elo_ratings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("domain", sa.String(length=40), nullable=False),
        sa.Column("scope", sa.String(length=40), nullable=False),
        sa.Column("elo_rating", sa.Integer(), nullable=False, server_default="1000"),
        sa.Column("elo_peak", sa.Integer(), nullable=False, server_default="1000"),
        sa.Column(
            "rank", sa.String(length=50), nullable=False, server_default="Beginner"
        ),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("correct", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("streak_current", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("streak_best", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_activity", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "domain", "scope", name="uq_elo_rating_track"),
    )
    op.create_index(
        op.f("ix_elo_ratings_user_id"), "elo_ratings", ["user_id"], unique=False
    )
    op.create_index(
        "ix_elo_ratings_user_domain", "elo_ratings", ["user_id", "domain"], unique=False
    )

    with op.batch_alter_table("elo_history") as batch_op:
        batch_op.add_column(
            sa.Column(
                "domain",
                sa.String(length=40),
                nullable=False,
                server_default="puzzle",
            )
        )

    if is_postgres:
        op.execute("ALTER TABLE elo_ratings ENABLE ROW LEVEL SECURITY")
        op.execute("""
            CREATE POLICY elo_ratings_select_own ON elo_ratings
            FOR SELECT
            USING (user_id = current_setting('app.current_user_id', true)::int)
            """)
        op.execute("""
            CREATE POLICY elo_ratings_modify_own ON elo_ratings
            FOR ALL
            USING (user_id = current_setting('app.current_user_id', true)::int)
            WITH CHECK (user_id = current_setting('app.current_user_id', true)::int)
            """)


def downgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == "postgresql"

    if is_postgres:
        op.execute("DROP POLICY IF EXISTS elo_ratings_modify_own ON elo_ratings")
        op.execute("DROP POLICY IF EXISTS elo_ratings_select_own ON elo_ratings")
        op.execute("ALTER TABLE elo_ratings DISABLE ROW LEVEL SECURITY")

    with op.batch_alter_table("elo_history") as batch_op:
        batch_op.drop_column("domain")

    op.drop_index("ix_elo_ratings_user_domain", table_name="elo_ratings")
    op.drop_index(op.f("ix_elo_ratings_user_id"), table_name="elo_ratings")
    op.drop_table("elo_ratings")
