"""
Schemas Pydantic de certificados.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CertificateOut(BaseModel):
    """Certificado emitido para el usuario actual."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    track: str
    title: str
    recipient_name: str
    verification_code: str
    issued_at: datetime


class CertificateListOut(BaseModel):
    items: list[CertificateOut]
    total: int


class CertificateVerifyOut(BaseModel):
    """Resultado público de verificar un certificado por su código.

    `valid=False` cuando el código no existe; el resto de campos quedan en
    `None`. No expone identificadores internos (user_id, ids).
    """

    valid: bool
    recipient_name: Optional[str] = None
    title: Optional[str] = None
    track: Optional[str] = None
    issued_at: Optional[datetime] = None
