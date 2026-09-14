"""0016_exercise_types

Revision ID: 0016
Revises: 0015
Create Date: 2026-09-14 12:00:00.000000

Abre `exercises` a los ejercicios que **no se ejecutan**, que es lo que pide
Track 0 (pseudocódigo, trazas y diagramas de flujo no corren en Pyodide):

- `exercise_type`: "code" para todo lo que ya existe (los 198 ejercicios de
  Tracks 1-6 se quedan igual por el server_default) y los tipos de Track 0
  para lo nuevo (`trace_table`, `predict_output`, `mcq`...).
- `spec`: el enunciado estructurado (pseudocódigo, columnas de la traza,
  opciones). Es **público**: viaja al cliente para pintar el ejercicio.
- `answer_key`: la respuesta correcta. **Nunca** sale de la API; la corrección
  la hace el backend en `POST /exercises/{id}/check`. Mismo guard rail de
  no-leak que `hidden_tests`, con su test.

El contenido lo rellena el seed (`lesson_seed.py`), no esta migración.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0016"
down_revision: Union[str, None] = "0015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("exercises") as batch:
        batch.add_column(
            sa.Column(
                "exercise_type",
                sa.String(length=32),
                nullable=False,
                server_default="code",
            )
        )
        batch.add_column(
            sa.Column("spec", sa.JSON(), nullable=True, server_default=sa.text("'{}'"))
        )
        batch.add_column(
            sa.Column(
                "answer_key", sa.JSON(), nullable=True, server_default=sa.text("'{}'")
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("exercises") as batch:
        batch.drop_column("answer_key")
        batch.drop_column("spec")
        batch.drop_column("exercise_type")
