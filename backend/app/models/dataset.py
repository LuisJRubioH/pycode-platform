"""Datasets curados servidos a Pyodide via pycode.load_dataset(slug)."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String, Text

from app.core.database import Base


class Dataset(Base):
    """Dataset publico para ejercicios de Track 2 (Data Science).

    No tiene FK a users — son datos compartidos, no privados. Sin RLS.
    El endpoint /api/v1/datasets/{slug}/csv es publico (sin auth) para
    que Pyodide pueda fetcharlos desde el worker sin token.
    """

    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(80), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    source_url = Column(String(500), nullable=True)
    license = Column(String(100), nullable=False, default="public-domain")
    # columns_schema: [{"name": "sepal_length", "dtype": "float64"}, ...]
    columns_schema = Column(JSON, nullable=False, default=list)
    # sample_rows: primeras 5 filas como lista de dicts para preview
    sample_rows = Column(JSON, nullable=False, default=list)
    # csv_content: el CSV completo como texto. Solo se sirve via /{slug}/csv
    csv_content = Column(Text, nullable=False)
    row_count = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
