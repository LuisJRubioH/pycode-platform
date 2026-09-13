"""Retos por niveles (`generated_bank.CHALLENGE_TEMPLATES`).

El banco viejo generaba 3 variantes por dificultad que eran copias exactas
(solo cambiaba "Variante N"), filtraba al alumno instrucciones internas ("No
publiques la solucion final en el enunciado") y compartia un starter entre
niveles que piden funciones distintas. Estos tests evitan que vuelva:

- estructura: un reto por problema y nivel, sin frases internas, y la funcion
  que pide cada enunciado definida en SU starter;
- seed: actualiza el contenido conservando ids y borra los retos obsoletos
  (asi desaparecieron las v2/v3 en produccion);
- API: cada reto dice su nivel y el detalle trae la progresion del problema.
"""

import ast
import re

import pytest
from sqlalchemy import func, select

from app.core.database import async_session_maker
from app.models.challenge import CodingChallenge
from app.services.curated_retos import (
    CURATED_RETOS,
    RETOS_SOURCE,
    seed_curated_retos,
)
from app.services.retos_validacion import TESTS_CURADOS, VALIDACION_GENERADOS
from app.services.generated_bank import (
    CHALLENGE_TEMPLATES,
    CURATED_SOURCE,
    NIVELES,
    seed_generated_challenges,
    slug_nivel,
)

FRASES_INTERNAS = ("Variante", "No publiques", "documenta decisiones clave")


def _funcion_pedida(prompt: str) -> str | None:
    """Primer nombre que el enunciado pide implementar.

    Es el primer token entre backticks con forma de llamada (`nombre(...)`) o
    de clase (`Cuenta`); los demas tokens son datos, columnas o ejemplos.
    """
    for token in re.findall(r"`([^`]+)`", prompt):
        llamada = re.match(r"^([A-Za-z_]\w*)\(", token)
        if llamada:
            return llamada.group(1)
        if re.fullmatch(r"[A-Z][A-Za-z0-9]*", token):
            return token
    return None


def _definiciones(starter: str) -> set[str]:
    arbol = ast.parse(starter)
    return {
        nodo.name
        for nodo in arbol.body
        if isinstance(nodo, (ast.FunctionDef, ast.ClassDef))
    }


def test_un_reto_por_problema_y_nivel():
    slugs = [
        slug_nivel(t.slug_base, dslug)
        for t in CHALLENGE_TEMPLATES
        for _, dslug, _ in NIVELES
    ]
    assert len(slugs) == len(CHALLENGE_TEMPLATES) * 3
    assert len(slugs) == len(set(slugs))


@pytest.mark.parametrize("template", CHALLENGE_TEMPLATES, ids=lambda t: t.slug_base)
def test_cada_nivel_pide_una_funcion_que_su_starter_define(template):
    nombres = []
    for difficulty, _, _ in NIVELES:
        nivel = getattr(template, difficulty)
        for frase in FRASES_INTERNAS:
            assert frase not in nivel.prompt, f"{difficulty}: se colo '{frase}'"

        pedida = _funcion_pedida(nivel.prompt)
        assert pedida, f"{difficulty}: el enunciado no nombra que implementar"
        assert pedida in _definiciones(nivel.starter_code), (
            f"{difficulty}: el enunciado pide `{pedida}` y el starter define "
            f"{sorted(_definiciones(nivel.starter_code))}"
        )
        nombres.append(pedida)

    # Cada nivel es un ejercicio distinto, no el mismo con otro enunciado.
    assert len(set(nombres)) == 3, f"niveles con la misma funcion: {nombres}"


async def _generados() -> list[CodingChallenge]:
    async with async_session_maker() as session:
        rows = await session.execute(
            select(CodingChallenge).where(CodingChallenge.source == CURATED_SOURCE)
        )
        return list(rows.scalars().all())


@pytest.mark.asyncio
async def test_seed_actualiza_conserva_ids_y_borra_obsoletos():
    async with async_session_maker() as session:
        await seed_generated_challenges(session)
    antes = {c.slug: c.id for c in await _generados()}
    assert len(antes) == 60

    slug_two_sum_dificil = slug_nivel("arrays-two-sum", "dificil")
    async with async_session_maker() as session:
        # Una copia v2 como las que habia en produccion...
        session.add(
            CodingChallenge(
                title="Two Sum (v2)",
                slug=f"{CURATED_SOURCE}-arrays-two-sum-dificil-2",
                source=CURATED_SOURCE,
                source_path="x",
                difficulty="hard",
                topic="arrays",
                prompt="Variante 2: ...",
                starter_code="def two_sum(nums, target):\n    pass\n",
            )
        )
        # ...y un nivel existente con el contenido viejo.
        row = await session.execute(
            select(CodingChallenge).where(CodingChallenge.slug == slug_two_sum_dificil)
        )
        viejo = row.scalar_one()
        viejo.title = "Two Sum (v1)"
        viejo.starter_code = "def two_sum(nums, target):\n    pass\n"
        await session.commit()

    async with async_session_maker() as session:
        insertados = await seed_generated_challenges(session)
    assert insertados == 0

    despues = {c.slug: c for c in await _generados()}
    assert set(despues) == set(antes), "la copia v2 tenia que desaparecer"
    assert {s: c.id for s, c in despues.items()} == antes, "los ids no deben cambiar"
    actualizado = despues[slug_two_sum_dificil]
    assert actualizado.title == "Two Sum"
    assert "def two_sum_todos" in actualizado.starter_code


@pytest.mark.asyncio
async def test_niveles_en_listado_y_progresion_en_detalle(client, auth_headers):
    async with async_session_maker() as session:
        await seed_generated_challenges(session)
        await seed_curated_retos(session)
        ids = {}
        for difficulty, dslug, _ in NIVELES:
            row = await session.execute(
                select(CodingChallenge.id).where(
                    CodingChallenge.slug == slug_nivel("arrays-two-sum", dslug)
                )
            )
            ids[difficulty] = row.scalar_one()
        reto_suelto = await session.execute(
            select(func.min(CodingChallenge.id)).where(
                CodingChallenge.source == RETOS_SOURCE
            )
        )
        id_suelto = reto_suelto.scalar_one()

    r = await client.get(
        "/api/v1/challenges?difficulty=medium&limit=100", headers=auth_headers
    )
    assert r.status_code == 200, r.text
    por_id = {item["id"]: item for item in r.json()["items"]}
    assert por_id[ids["medium"]]["level"] == 2
    assert por_id[ids["medium"]]["title"] == "Two Sum"

    # Resolver el nivel 1 (todos sus tests) se refleja en la progresion vista
    # desde el nivel 2.
    tests_facil = await client.get(
        f"/api/v1/challenges/{ids['easy']}/hidden-tests", headers=auth_headers
    )
    total = len(tests_facil.json()["tests"])
    r = await client.post(
        f"/api/v1/challenges/{ids['easy']}/complete",
        headers=auth_headers,
        json={"passed_tests": total, "total_tests": total},
    )
    assert r.status_code == 204, r.text

    r = await client.get(f"/api/v1/challenges/{ids['medium']}", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["level"] == 2
    assert [
        (n["level"], n["difficulty"], n["id"], n["completed"]) for n in body["levels"]
    ] == [
        (1, "easy", ids["easy"], True),
        (2, "medium", ids["medium"], False),
        (3, "hard", ids["hard"], False),
    ]

    r = await client.get(f"/api/v1/challenges/{id_suelto}", headers=auth_headers)
    assert r.status_code == 200, r.text
    assert r.json()["level"] is None
    assert r.json()["levels"] == []


def test_cada_reto_tiene_tests_y_solucion():
    """Los 70 retos se validan con tests. Que aprueben con la solucion y no con
    el starter lo comprueba el barrido de CI (test_hidden_tests_no_triviales)."""
    for template in CHALLENGE_TEMPLATES:
        for difficulty, _, _ in NIVELES:
            validacion = VALIDACION_GENERADOS.get((template.slug_base, difficulty))
            assert validacion, f"{template.slug_base}/{difficulty} sin validacion"
            assert validacion.hidden_tests
            assert validacion.reference_solution.strip()
    for reto in CURATED_RETOS:
        assert len(TESTS_CURADOS.get(reto.slug_suffix, [])) >= 2, reto.slug_suffix
    # Y ninguna validacion huerfana de un reto que ya no existe.
    assert len(VALIDACION_GENERADOS) == len(CHALLENGE_TEMPLATES) * 3
    assert set(TESTS_CURADOS) == {r.slug_suffix for r in CURATED_RETOS}


@pytest.mark.asyncio
async def test_hidden_tests_salen_por_su_endpoint_y_no_por_el_detalle(
    client, auth_headers
):
    async with async_session_maker() as session:
        await seed_generated_challenges(session)
        row = await session.execute(
            select(CodingChallenge).where(
                CodingChallenge.slug == slug_nivel("arrays-two-sum", "medio")
            )
        )
        reto = row.scalar_one()
        cid, solucion, tests = reto.id, reto.reference_solution, reto.hidden_tests

    r = await client.get(f"/api/v1/challenges/{cid}/hidden-tests", headers=auth_headers)
    assert r.status_code == 200, r.text
    assert [t["name"] for t in r.json()["tests"]] == [t["name"] for t in tests]

    # Una linea distintiva de la solucion, y el codigo de los tests, no salen
    # ni por el detalle ni por el listado.
    assert "vistos.setdefault(x, j)" in solucion
    primera_linea_test = tests[0]["code"].strip().splitlines()[0]
    for url in (f"/api/v1/challenges/{cid}", "/api/v1/challenges?limit=100"):
        r = await client.get(url, headers=auth_headers)
        assert r.status_code == 200, r.text
        assert "hidden_tests" not in r.text
        assert "reference_solution" not in r.text
        assert "vistos.setdefault(x, j)" not in r.text
        assert primera_linea_test not in r.text
