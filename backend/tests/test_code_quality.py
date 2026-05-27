"""Tests del análisis estático de código + snapshot de calidad (Pieza L).

`analyze_code` no ejecuta el código (solo `ast.parse`); el score es
determinista. El endpoint /tutor/evaluate guarda un CodeQualitySnapshot que
combina los scores del LLM con el análisis estático.
"""

import pytest
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.code_quality import CodeQualitySnapshot
from app.services.code_quality_service import analyze_code

CLEAN = '''def suma(a, b):
    """Suma dos numeros."""
    return a + b
'''

NESTED_UNDOCUMENTED = """def f(x):
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                if i > 5:
                    print(i)
    return x
"""


def test_clean_code_scores_high():
    res = analyze_code(CLEAN)
    assert res.static_score == 100
    assert res.metrics["syntax_ok"] is True
    assert res.metrics["n_functions"] == 1
    assert res.metrics["cyclomatic_complexity"] == 1
    assert res.metrics["docstring_ratio"] == 1.0


def test_syntax_error_scores_zero():
    res = analyze_code("def f(:\n    pass\n")
    assert res.static_score == 0
    assert res.metrics["syntax_ok"] is False


def test_nested_undocumented_penalized():
    res = analyze_code(NESTED_UNDOCUMENTED)
    assert res.static_score < 100
    assert res.metrics["n_functions"] == 1
    assert res.metrics["max_nesting"] >= 5
    assert res.metrics["docstring_ratio"] == 0.0
    assert res.metrics["cyclomatic_complexity"] >= 4


def test_is_deterministic():
    assert analyze_code(CLEAN).static_score == analyze_code(CLEAN).static_score


@pytest.mark.asyncio
async def test_evaluate_creates_quality_snapshot(client, user_a):
    payload = {
        "problem_description": "Sumar dos numeros enteros y devolver el total.",
        "code": CLEAN,
    }
    r = await client.post(
        "/api/v1/tutor/evaluate", json=payload, headers=user_a["headers"]
    )
    assert r.status_code == 201, r.text

    async with async_session_maker() as session:
        rows = (
            (
                await session.execute(
                    select(CodeQualitySnapshot).where(
                        CodeQualitySnapshot.user_id == user_a["id"]
                    )
                )
            )
            .scalars()
            .all()
        )
    assert len(rows) == 1
    snap = rows[0]
    assert snap.source == "evaluation"
    assert snap.static_score == 100
    assert snap.metrics["n_functions"] == 1


@pytest.mark.asyncio
async def test_quality_snapshot_isolated_per_user(client, user_a, user_b):
    payload = {
        "problem_description": "Sumar dos numeros enteros y devolver el total.",
        "code": CLEAN,
    }
    await client.post("/api/v1/tutor/evaluate", json=payload, headers=user_a["headers"])

    async with async_session_maker() as session:
        rows_b = (
            (
                await session.execute(
                    select(CodeQualitySnapshot).where(
                        CodeQualitySnapshot.user_id == user_b["id"]
                    )
                )
            )
            .scalars()
            .all()
        )
    assert rows_b == []


@pytest.mark.asyncio
async def test_progress_code_quality_endpoint(client, user_a):
    payload = {
        "problem_description": "Sumar dos numeros enteros y devolver el total.",
        "code": CLEAN,
    }
    await client.post("/api/v1/tutor/evaluate", json=payload, headers=user_a["headers"])

    r = await client.get("/api/v1/progress/code-quality", headers=user_a["headers"])
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["summary"]["count"] == 1
    assert body["summary"]["avg_static"] == 100.0
    assert body["summary"]["latest_static"] == 100
    assert len(body["points"]) == 1


@pytest.mark.asyncio
async def test_progress_code_quality_empty(client, auth_headers):
    r = await client.get("/api/v1/progress/code-quality", headers=auth_headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["summary"]["count"] == 0
    assert body["points"] == []


@pytest.mark.asyncio
async def test_progress_code_quality_requires_auth(client):
    r = await client.get("/api/v1/progress/code-quality")
    assert r.status_code in (401, 403)
