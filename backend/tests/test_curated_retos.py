"""Tests de los retos curados (Pieza H).

Cubre:
- invariantes estructurales (10 retos, slugs únicos, dificultad válida,
  campos no vacíos)
- cada `reference_solution` se ejecuta sin error y define su función
- el seeder es idempotente y los retos salen por el endpoint
- guard rail: `reference_solution` NUNCA se filtra en el detalle del reto
"""

import pytest
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.challenge import CodingChallenge
from app.services.curated_retos import (
    CURATED_RETOS,
    RETOS_SOURCE,
    seed_curated_retos,
)

VALID_DIFFICULTIES = {"easy", "medium", "hard"}

ENTRYPOINTS = {
    "fizzbuzz-lista": "fizzbuzz",
    "validador-password": "es_segura",
    "conteo-palabras": "contar_palabras",
    "media-movil": "media_movil",
    "total-por-categoria": "total_por_categoria",
    "outliers-iqr": "outliers",
    "normalizacion-minmax": "normaliza",
    "one-hot-encoding": "one_hot",
    "matriz-confusion": "matriz_confusion",
    "tf-term-frequency": "tf",
}


def test_there_are_ten_unique_retos():
    assert len(CURATED_RETOS) == 10
    suffixes = [r.slug_suffix for r in CURATED_RETOS]
    assert len(suffixes) == len(set(suffixes))


def test_retos_have_valid_fields():
    for r in CURATED_RETOS:
        assert r.difficulty in VALID_DIFFICULTIES
        assert r.prompt.strip()
        assert r.starter_code.strip()
        assert r.reference_solution.strip()


def test_reference_solutions_run_and_define_entrypoint():
    for r in CURATED_RETOS:
        ns: dict = {}
        exec(r.reference_solution, ns)  # noqa: S102 - contenido propio del repo
        entry = ENTRYPOINTS[r.slug_suffix]
        assert callable(ns.get(entry)), f"{r.slug_suffix} no define {entry}()"


@pytest.mark.asyncio
async def test_seed_is_idempotent():
    async with async_session_maker() as session:
        first = await seed_curated_retos(session)
    async with async_session_maker() as session:
        second = await seed_curated_retos(session)
    # La primera vez puede insertar 10 (o 0 si otro test ya sembró); la
    # segunda corrida nunca debe duplicar.
    assert first in (0, 10)
    assert second == 0

    async with async_session_maker() as session:
        rows = await session.execute(
            select(CodingChallenge).where(CodingChallenge.source == RETOS_SOURCE)
        )
        assert len(rows.scalars().all()) == 10


@pytest.mark.asyncio
async def test_retos_listed_via_endpoint(client, auth_headers):
    async with async_session_maker() as session:
        await seed_curated_retos(session)

    r = await client.get("/api/v1/challenges?limit=100", headers=auth_headers)
    assert r.status_code == 200, r.text
    slugs = {item["slug"] for item in r.json()["items"]}
    assert f"{RETOS_SOURCE}-fizzbuzz-lista" in slugs


@pytest.mark.asyncio
async def test_detail_never_leaks_reference_solution(client, auth_headers):
    async with async_session_maker() as session:
        await seed_curated_retos(session)
        row = await session.execute(
            select(CodingChallenge).where(
                CodingChallenge.slug == f"{RETOS_SOURCE}-matriz-confusion"
            )
        )
        reto = row.scalar_one()
        challenge_id = reto.id
        ref_solution = reto.reference_solution

    r = await client.get(f"/api/v1/challenges/{challenge_id}", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert "reference_solution" not in body
    # Una línea distintiva de la solución no debe aparecer en la respuesta.
    assert "tp = fp = fn = tn = 0" in ref_solution
    assert "tp = fp = fn = tn = 0" not in r.text
