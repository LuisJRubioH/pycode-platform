"""Seeder de datasets curados para Track 2 (Data Science).

3 datasets pequenos servidos via /api/v1/datasets/{slug}/csv y cargables
desde Pyodide con `pycode.load_dataset(slug)`:

- **iris**: clasico de Fisher (1936), dominio publico. Subset de 30 filas
  (10 por especie) para que el ejercicio sea manejable.
- **ventas-pyme**: sintetico (seed=42), 60 filas. Practica de groupby por
  categoria/producto, agregaciones, formato de fecha.
- **encuestas**: sintetico (seed=43), 80 filas con missing values y
  categoricos. Practica de fillna, value_counts, crosstab.
"""

# flake8: noqa: E501 -- archivos de datasets con CSV inline largo

from __future__ import annotations

import csv
import io
import random
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dataset import Dataset


@dataclass(frozen=True)
class DatasetTemplate:
    slug: str
    name: str
    description: str
    source_url: str | None
    license: str
    csv_content: str


# ---------------------------------------------------------------------------
# iris (30 filas, dominio publico, Fisher 1936)
# ---------------------------------------------------------------------------

IRIS_CSV = """sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
7.0,3.2,4.7,1.4,versicolor
6.4,3.2,4.5,1.5,versicolor
6.9,3.1,4.9,1.5,versicolor
5.5,2.3,4.0,1.3,versicolor
6.5,2.8,4.6,1.5,versicolor
5.7,2.8,4.5,1.3,versicolor
6.3,3.3,4.7,1.6,versicolor
4.9,2.4,3.3,1.0,versicolor
6.6,2.9,4.6,1.3,versicolor
5.2,2.7,3.9,1.4,versicolor
6.3,3.3,6.0,2.5,virginica
5.8,2.7,5.1,1.9,virginica
7.1,3.0,5.9,2.1,virginica
6.3,2.9,5.6,1.8,virginica
6.5,3.0,5.8,2.2,virginica
7.6,3.0,6.6,2.1,virginica
4.9,2.5,4.5,1.7,virginica
7.3,2.9,6.3,1.8,virginica
6.7,2.5,5.8,1.8,virginica
7.2,3.6,6.1,2.5,virginica
"""


def _build_ventas_pyme_csv() -> str:
    """Genera CSV sintetico con seed fijo. Reproducible byte a byte."""
    rng = random.Random(42)
    productos = ["cafe", "te", "galletas", "torta", "sandwich"]
    categorias = {
        "cafe": "bebida",
        "te": "bebida",
        "galletas": "comida",
        "torta": "comida",
        "sandwich": "comida",
    }
    precios = {"cafe": 3.5, "te": 2.5, "galletas": 1.8, "torta": 4.5, "sandwich": 6.0}
    sucursales = ["centro", "norte", "sur"]

    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(
        [
            "fecha",
            "sucursal",
            "producto",
            "categoria",
            "unidades",
            "precio_unit",
            "ingreso",
        ]
    )
    for i in range(60):
        dia = 1 + (i % 30)
        mes = 1 + (i // 30)
        fecha = f"2026-{mes:02d}-{dia:02d}"
        sucursal = rng.choice(sucursales)
        producto = rng.choice(productos)
        categoria = categorias[producto]
        precio = precios[producto]
        unidades = rng.randint(1, 12)
        ingreso = round(precio * unidades, 2)
        writer.writerow(
            [fecha, sucursal, producto, categoria, unidades, precio, ingreso]
        )
    return buf.getvalue()


def _build_encuestas_csv() -> str:
    """Genera CSV con missing values intencionales para practica de fillna."""
    rng = random.Random(43)
    planes = ["basico", "pro", "enterprise"]
    paises = ["AR", "MX", "CO", "CL", "PE", "ES"]

    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["respuesta_id", "edad", "pais", "plan", "satisfaccion", "churn"])
    for i in range(80):
        edad = rng.randint(18, 70) if rng.random() > 0.10 else ""  # 10% missing
        pais = rng.choice(paises)
        plan = rng.choice(planes) if rng.random() > 0.05 else ""  # 5% missing
        # satisfaccion 1-5, sesgada por plan
        base = {"basico": 3.0, "pro": 3.8, "enterprise": 4.2}.get(plan, 3.5)
        sat_raw = base + rng.uniform(-1.5, 1.5)
        satisfaccion = max(1, min(5, round(sat_raw)))
        # churn: 30% si satisfaccion <=2, 8% si >=4
        if satisfaccion <= 2:
            churn = 1 if rng.random() < 0.30 else 0
        elif satisfaccion >= 4:
            churn = 1 if rng.random() < 0.08 else 0
        else:
            churn = 1 if rng.random() < 0.15 else 0
        writer.writerow([i + 1, edad, pais, plan, satisfaccion, churn])
    return buf.getvalue()


def _build_templates() -> list[DatasetTemplate]:
    return [
        DatasetTemplate(
            slug="iris",
            name="Iris (Fisher 1936)",
            description=(
                "Dataset clasico de flores Iris. 30 filas (10 por especie: setosa, versicolor, virginica). "
                "4 features numericas (sepal y petal length/width) + 1 target categorico. "
                "Ideal para introducir Pandas: tipos, describe(), groupby por species, scatter plots."
            ),
            source_url="https://archive.ics.uci.edu/ml/datasets/iris",
            license="public-domain",
            csv_content=IRIS_CSV,
        ),
        DatasetTemplate(
            slug="ventas-pyme",
            name="Ventas de cafeteria PyME",
            description=(
                "Dataset sintetico (seed fijo, reproducible). 60 dias de ventas de una cafeteria "
                "con 3 sucursales y 5 productos. Columnas: fecha, sucursal, producto, categoria, "
                "unidades, precio_unit, ingreso. Practica de groupby por sucursal/producto, "
                "agregaciones, parseo de fechas con pd.to_datetime."
            ),
            source_url=None,
            license="cc0-sintetico",
            csv_content=_build_ventas_pyme_csv(),
        ),
        DatasetTemplate(
            slug="encuestas",
            name="Encuestas de satisfaccion (con missing)",
            description=(
                "Dataset sintetico (seed fijo). 80 respuestas con valores faltantes intencionales en "
                "edad (10%) y plan (5%). Columnas: respuesta_id, edad, pais, plan, satisfaccion, churn. "
                "Practica de fillna, dropna, value_counts, crosstab y correlacion satisfaccion-churn."
            ),
            source_url=None,
            license="cc0-sintetico",
            csv_content=_build_encuestas_csv(),
        ),
    ]


def _parse_columns_schema_and_sample(
    csv_text: str,
) -> tuple[list[dict], list[dict], int]:
    """Lee el CSV y devuelve (columns_schema, sample_rows_5, row_count)."""
    reader = csv.reader(io.StringIO(csv_text))
    header = next(reader)
    rows = list(reader)
    row_count = len(rows)

    def infer_dtype(values: list[str]) -> str:
        non_empty = [v for v in values if v != ""]
        if not non_empty:
            return "object"
        try:
            [int(v) for v in non_empty]
            return "int64"
        except ValueError:
            pass
        try:
            [float(v) for v in non_empty]
            return "float64"
        except ValueError:
            pass
        return "object"

    columns_schema = []
    for i, col in enumerate(header):
        values = [r[i] for r in rows if i < len(r)]
        columns_schema.append({"name": col, "dtype": infer_dtype(values)})

    sample_rows = []
    for r in rows[:5]:
        sample_rows.append({header[i]: r[i] for i in range(min(len(header), len(r)))})

    return columns_schema, sample_rows, row_count


async def seed_datasets_if_empty(db: AsyncSession) -> int:
    """Upsert idempotente por slug. Devuelve cantidad insertada nueva."""
    inserted = 0
    for template in _build_templates():
        existing = await db.execute(
            select(Dataset).where(Dataset.slug == template.slug)
        )
        dataset = existing.scalar_one_or_none()

        columns_schema, sample_rows, row_count = _parse_columns_schema_and_sample(
            template.csv_content
        )

        if dataset is None:
            db.add(
                Dataset(
                    slug=template.slug,
                    name=template.name,
                    description=template.description,
                    source_url=template.source_url,
                    license=template.license,
                    columns_schema=columns_schema,
                    sample_rows=sample_rows,
                    csv_content=template.csv_content,
                    row_count=row_count,
                    is_active=True,
                )
            )
            inserted += 1
        else:
            dataset.name = template.name
            dataset.description = template.description
            dataset.source_url = template.source_url
            dataset.license = template.license
            dataset.columns_schema = columns_schema
            dataset.sample_rows = sample_rows
            dataset.csv_content = template.csv_content
            dataset.row_count = row_count
            dataset.is_active = True

    await db.commit()
    return inserted
