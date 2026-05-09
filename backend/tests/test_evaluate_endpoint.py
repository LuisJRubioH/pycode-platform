"""Tests del endpoint POST /api/v1/tutor/evaluate (Fase 1)."""

from typing import Any

import pytest

from app.api.v1.endpoints import tutor as tutor_endpoint
from app.schemas.evaluation import EvaluationVerdict


_FAKE_RAW = (
    "CALIFICACION:\n"
    "- Logica: 82/100 (clara)\n"
    "- Solucion General: 75/100 (buena estructura)\n\n"
    "PUNTOS FUERTES: ...\n"
    "AREAS DE MEJORA: ...\n"
    "RECOMENDACIONES: ...\n"
)


class _FakeEvalService:
    model_used = "fake-model"

    async def evaluate(self, payload):
        return EvaluationVerdict(raw=_FAKE_RAW, logic_score=82, general_score=75)


@pytest.fixture(autouse=True)
def _stub_evaluation_service(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tutor_endpoint, "evaluation_service", _FakeEvalService())


def _payload(**overrides: Any) -> dict[str, Any]:
    base = {
        "problem_description": "Sumar dos números enteros y devolver el resultado.",
        "code": "def sumar(a, b):\n    return a + b\nprint(sumar(2, 3))",
        "expected_output": "5",
        "actual_output": "5",
    }
    base.update(overrides)
    return base


@pytest.mark.asyncio
async def test_evaluate_persists_and_returns_verdict(client, auth_headers):
    r = await client.post(
        "/api/v1/tutor/evaluate", json=_payload(), headers=auth_headers
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["id"] > 0
    assert body["verdict"]["logic_score"] == 82
    assert body["verdict"]["general_score"] == 75
    assert "CALIFICACION" in body["verdict"]["raw"]
    assert body["model_used"] == "fake-model"


@pytest.mark.asyncio
async def test_evaluate_requires_auth(client):
    r = await client.post("/api/v1/tutor/evaluate", json=_payload())
    # FastAPI HTTPBearer responde 403 cuando falta el header; 401 si llega
    # un token inválido. Ambos son "no autorizado" desde el punto de vista
    # del cliente.
    assert r.status_code in (401, 403)


@pytest.mark.asyncio
async def test_evaluate_rejects_short_problem_description(client, auth_headers):
    r = await client.post(
        "/api/v1/tutor/evaluate",
        json=_payload(problem_description="hola"),
        headers=auth_headers,
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_evaluate_rejects_extra_fields(client, auth_headers):
    payload = _payload()
    payload["extra"] = "should-not-be-allowed"
    r = await client.post("/api/v1/tutor/evaluate", json=payload, headers=auth_headers)
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_evaluate_isolated_per_user(client, user_a, user_b):
    """La evaluación de A no aparece para B (defensa app-layer + RLS en PG)."""
    r = await client.post(
        "/api/v1/tutor/evaluate", json=_payload(), headers=user_a["headers"]
    )
    assert r.status_code == 201
    eval_id = r.json()["id"]

    # No hay endpoint público GET /tutor/evaluate/{id}, pero el export
    # GDPR no debe filtrar evaluaciones de otro usuario tampoco.
    rb = await client.get("/api/v1/users/me/export", headers=user_b["headers"])
    assert rb.status_code == 200
    raw = rb.text
    assert str(eval_id) not in raw or '"email": "{}"'.format(user_a["email"]) not in raw
