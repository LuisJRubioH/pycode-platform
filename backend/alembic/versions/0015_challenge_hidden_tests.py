"""0015_challenge_hidden_tests

Revision ID: 0015
Revises: 0014
Create Date: 2026-09-13 20:00:00.000000

Añade `coding_challenges.hidden_tests` (JSON, default lista vacía), el mismo
patrón que `exercises.hidden_tests` (0007): el cliente recibe los tests al
pulsar "Ejecutar tests" en el editor y los corre en Pyodide.

Hasta ahora un reto se completaba con un botón "Marcar como hecho" que además
otorgaba ELO; con esta columna, completarlo exige haber pasado sus tests. El
contenido lo rellena el seed (`retos_validacion.py`), no esta migración.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0015"
down_revision: Union[str, None] = "0014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("coding_challenges") as batch:
        batch.add_column(
            sa.Column(
                "hidden_tests",
                sa.JSON(),
                nullable=True,
                server_default=sa.text("'[]'"),
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("coding_challenges") as batch:
        batch.drop_column("hidden_tests")
