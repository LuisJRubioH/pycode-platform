"""Pydantic schemas para datasets curados."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class DatasetSummary(BaseModel):
    """Item en GET /api/v1/datasets/ — metadata sin csv_content ni sample_rows."""

    slug: str
    name: str
    description: Optional[str]
    license: str
    row_count: int
    column_count: int

    class Config:
        from_attributes = True


class DatasetColumn(BaseModel):
    name: str
    dtype: str


class DatasetDetail(BaseModel):
    """GET /api/v1/datasets/{slug} — incluye sample_rows pero NO csv_content."""

    slug: str
    name: str
    description: Optional[str]
    source_url: Optional[str]
    license: str
    columns_schema: list[DatasetColumn]
    sample_rows: list[dict[str, Any]]
    row_count: int
    created_at: datetime

    class Config:
        from_attributes = True
