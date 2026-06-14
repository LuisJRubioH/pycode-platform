"""0014_datasets

Revision ID: 0014
Revises: 0013
Create Date: 2026-06-14 19:30:00.000000

Crea la tabla `datasets` para servir CSVs curados a Pyodide via
`pycode.load_dataset(slug)`. Tabla publica sin RLS — son datos
compartidos, no privados; el endpoint /api/v1/datasets/{slug}/csv es
publico (sin auth) para que el worker pueda fetcharlos sin token.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0014"
down_revision: Union[str, None] = "0013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "datasets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=80), nullable=False, unique=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column(
            "license",
            sa.String(length=100),
            nullable=False,
            server_default="public-domain",
        ),
        sa.Column(
            "columns_schema",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'"),
        ),
        sa.Column(
            "sample_rows",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'"),
        ),
        sa.Column("csv_content", sa.Text(), nullable=False),
        sa.Column(
            "row_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_datasets_slug", "datasets", ["slug"])


def downgrade() -> None:
    op.drop_index("ix_datasets_slug", table_name="datasets")
    op.drop_table("datasets")
