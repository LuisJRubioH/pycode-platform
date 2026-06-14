"""0013_lesson_track

Revision ID: 0013
Revises: 0012
Create Date: 2026-06-14 18:30:00.000000

Anade `lessons.track` para empezar a separar contenido por track
(Track 1 Python, Track 2 Data Science, etc.). Default 'track-1' para
backfill no destructivo de las lecciones existentes. Backward-compatible:
sin filtro, los endpoints devuelven todas las lecciones; con `?track=`
filtran. Patron replicable a Tracks 3-6.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0013"
down_revision: Union[str, None] = "0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("lessons") as batch:
        batch.add_column(
            sa.Column(
                "track",
                sa.String(length=50),
                nullable=False,
                server_default="track-1",
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("lessons") as batch:
        batch.drop_column("track")
