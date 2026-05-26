"""0009_certificates

Revision ID: 0009
Revises: 0008
Create Date: 2026-05-26 10:00:00.000000

Crea la tabla `certificates` — credencial verificable que emite cada Track
al aprobar su capstone.

La tabla es PÚBLICA (sin RLS, igual que `capstones`): un certificado es por
diseño una credencial compartible/verificable. El `verification_code`
impredecible actúa como capacidad para el endpoint público de verificación;
el listado "mis certificados" filtra por `user_id` en la capa de app.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0009"
down_revision: Union[str, None] = "0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "certificates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("capstone_id", sa.Integer(), nullable=True),
        sa.Column("track", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("recipient_name", sa.String(length=120), nullable=False),
        sa.Column("verification_code", sa.String(length=40), nullable=False),
        sa.Column("issued_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["capstone_id"], ["capstones.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("verification_code"),
        sa.UniqueConstraint("user_id", "track", name="uq_certificate_user_track"),
    )
    op.create_index(
        op.f("ix_certificates_user_id"), "certificates", ["user_id"], unique=False
    )
    op.create_index(
        op.f("ix_certificates_capstone_id"),
        "certificates",
        ["capstone_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_certificates_track"), "certificates", ["track"], unique=False
    )
    op.create_index(
        op.f("ix_certificates_verification_code"),
        "certificates",
        ["verification_code"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_certificates_verification_code"), table_name="certificates")
    op.drop_index(op.f("ix_certificates_track"), table_name="certificates")
    op.drop_index(op.f("ix_certificates_capstone_id"), table_name="certificates")
    op.drop_index(op.f("ix_certificates_user_id"), table_name="certificates")
    op.drop_table("certificates")
