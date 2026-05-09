"""0007_exercise_hidden_tests

Revision ID: 0007
Revises: 0006
Create Date: 2026-05-08 20:30:00.000000

Añade `exercises.hidden_tests` (JSON, default lista vacía) para el patrón
"tests ocultos Pyodide-based" de Fase 1: el cliente recibe los tests al
pulsar "Ejecutar tests" y los corre en el worker Pyodide; la UI no los
renderiza, solo muestra el verdict por test (pass/fail + mensaje de
excepción si falla).

`exercises.test_cases` se mantiene intacto (legacy: cuenta total de tests
en `code_submissions.total_tests`). Los `hidden_tests` son los que la
Pyodide ejecuta — formato esperado:
    [{"name": "suma básica", "code": "assert my_sum(2, 3) == 5"}, ...]

Cada test se concatena al código del estudiante en un namespace nuevo;
"no excepción" = pass, "excepción" = fail. Mismo patrón que se replicará
en Tracks 2-6 (Pandas/sklearn/PyTorch validators).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("exercises") as batch:
        batch.add_column(
            sa.Column(
                "hidden_tests",
                sa.JSON(),
                nullable=True,
                server_default=sa.text("'[]'"),
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("exercises") as batch:
        batch.drop_column("hidden_tests")
