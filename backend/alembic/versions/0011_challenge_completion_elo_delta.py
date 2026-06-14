"""0011_challenge_completion_elo_delta

Revision ID: 0011
Revises: 0010
Create Date: 2026-05-26 13:00:00.000000

Añade `elo_delta` a `challenge_completions` para guardar cuánto ELO otorgó
marcar el reto (rating `challenge:<difficulty>`) y poder revertirlo exacto al
desmarcar. batch_alter_table para ser no-op-safe en SQLite (tests).
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0011"
down_revision: Union[str, None] = "0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("challenge_completions") as batch_op:
        batch_op.add_column(
            sa.Column("elo_delta", sa.Integer(), nullable=False, server_default="0")
        )


def downgrade() -> None:
    with op.batch_alter_table("challenge_completions") as batch_op:
        batch_op.drop_column("elo_delta")
