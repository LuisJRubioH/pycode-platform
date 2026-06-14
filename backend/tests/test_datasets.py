"""Tests del sistema de datasets curados (Track 2 piloto N1)."""

import csv
import io

import pytest

from app.core.database import async_session_maker
from app.services.dataset_seed import seed_datasets_if_empty

_SEEDED = False


async def _ensure_seeded() -> None:
    global _SEEDED
    if _SEEDED:
        return
    async with async_session_maker() as session:
        await seed_datasets_if_empty(session)
    _SEEDED = True


@pytest.mark.asyncio
async def test_datasets_seeded_three(client, auth_headers):
    """Seeder deja exactamente los 3 datasets del piloto N1."""
    await _ensure_seeded()
    r = await client.get("/api/v1/datasets/", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    slugs = {d["slug"] for d in body}
    assert {"iris", "ventas-pyme", "encuestas"}.issubset(slugs)


@pytest.mark.asyncio
async def test_list_does_not_leak_csv_content(client, auth_headers):
    """GET / NUNCA expone csv_content ni sample_rows (eso es solo en detalle).

    Guard rail: si el listado leakeara el CSV completo, descargar TODO el
    catalogo seria 1 sola request. Queremos respuestas chicas y obligar
    al detalle/csv como pasos explicitos.
    """
    await _ensure_seeded()
    r = await client.get("/api/v1/datasets/", headers=auth_headers)
    assert r.status_code == 200
    for d in r.json():
        assert "csv_content" not in d, f"csv_content leak in /datasets/: {d}"
        assert "sample_rows" not in d, f"sample_rows leak en lista: {d}"


@pytest.mark.asyncio
async def test_detail_shows_sample_rows_no_csv(client, auth_headers):
    """GET /{slug} expone sample_rows (preview) pero NUNCA csv_content."""
    await _ensure_seeded()
    r = await client.get("/api/v1/datasets/iris", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["slug"] == "iris"
    assert body["row_count"] == 30
    assert len(body["columns_schema"]) == 5
    column_names = {c["name"] for c in body["columns_schema"]}
    assert "sepal_length" in column_names and "species" in column_names
    assert len(body["sample_rows"]) == 5
    assert body["sample_rows"][0]["species"] == "setosa"
    assert "csv_content" not in body, "csv_content NO debe estar en detail"


@pytest.mark.asyncio
async def test_csv_endpoint_is_public_and_returns_valid_csv(client):
    """GET /{slug}/csv es PUBLICO (sin auth) y devuelve text/csv parseable."""
    await _ensure_seeded()
    # Sin headers de auth — debe funcionar igual
    r = await client.get("/api/v1/datasets/iris/csv")
    assert r.status_code == 200, r.text
    assert r.headers["content-type"].startswith("text/csv")
    # Parseable como CSV con el header esperado
    reader = csv.reader(io.StringIO(r.text))
    header = next(reader)
    rows = list(reader)
    assert header == [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species",
    ]
    assert len(rows) == 30
    species = {r[4] for r in rows}
    assert species == {"setosa", "versicolor", "virginica"}


@pytest.mark.asyncio
async def test_unknown_slug_returns_404(client, auth_headers):
    """Slug invalido → 404 (detail y csv)."""
    await _ensure_seeded()
    r1 = await client.get("/api/v1/datasets/does-not-exist", headers=auth_headers)
    assert r1.status_code == 404
    r2 = await client.get("/api/v1/datasets/does-not-exist/csv")
    assert r2.status_code == 404
