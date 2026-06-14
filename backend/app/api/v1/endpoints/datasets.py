"""Endpoints de datasets curados (Track 2 - Data Science).

GET /datasets/ y /datasets/{slug} requieren auth (para que solo
estudiantes registrados los vean en /datasets como pagina indice).

GET /datasets/{slug}/csv es PUBLICO: el worker Pyodide lo fetchea sin
token cuando el alumno corre `pycode.load_dataset(slug)`. Los datos son
publicos por diseno (datasets clasicos o sinteticos sin PII), pero el
endpoint nunca devuelve csv via los otros dos handlers — el cliente
hace una request extra explicita al `/csv`.
"""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.dataset import Dataset
from app.models.user import User
from app.schemas.dataset import DatasetDetail, DatasetSummary

router = APIRouter()


@router.get("/", response_model=list[DatasetSummary])
async def list_datasets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Lista los datasets activos con metadata. NO incluye csv_content."""
    result = await db.execute(
        select(Dataset).where(Dataset.is_active).order_by(Dataset.slug)
    )
    items = result.scalars().all()
    return [
        DatasetSummary(
            slug=d.slug,
            name=d.name,
            description=d.description,
            license=d.license,
            row_count=d.row_count,
            column_count=len(d.columns_schema or []),
        )
        for d in items
    ]


@router.get("/{slug}", response_model=DatasetDetail)
async def get_dataset(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Detalle del dataset con sample_rows. NO incluye csv_content."""
    result = await db.execute(
        select(Dataset).where(Dataset.slug == slug, Dataset.is_active)
    )
    dataset = result.scalar_one_or_none()
    if dataset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found"
        )
    return DatasetDetail(
        slug=dataset.slug,
        name=dataset.name,
        description=dataset.description,
        source_url=dataset.source_url,
        license=dataset.license,
        columns_schema=dataset.columns_schema or [],
        sample_rows=dataset.sample_rows or [],
        row_count=dataset.row_count,
        created_at=dataset.created_at,
    )


@router.get("/{slug}/csv")
async def get_dataset_csv(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """PUBLICO sin auth. Sirve el CSV completo para Pyodide.

    Pyodide corre en un Worker sin acceso al JWT del usuario; los
    datasets son contenido publico curado, asi que se exponen sin auth
    para que `pycode.load_dataset(slug)` pueda hacer pyfetch directo.
    """
    result = await db.execute(
        select(Dataset).where(Dataset.slug == slug, Dataset.is_active)
    )
    dataset = result.scalar_one_or_none()
    if dataset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found"
        )
    return Response(
        content=dataset.csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'inline; filename="{dataset.slug}.csv"',
            "Cache-Control": "public, max-age=86400",
        },
    )
