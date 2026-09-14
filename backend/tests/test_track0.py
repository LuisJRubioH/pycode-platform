"""Track 0: corrección en backend de los ejercicios que no se ejecutan.

Cubre las cinco reglas de `docs/TRACK_0.md`:

1. validación determinista, sin Pyodide y sin LLM;
2. aprobar emite el mismo evento de completitud que un ejercicio de Python;
3. la `answer_key` **no** viaja al cliente (guard rail de no-leak);
4. reintentos permitidos y XP idempotente;
5. un tipo nuevo no obliga a tocar el endpoint.
"""

import pytest
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.learning import CodeSubmission, Exercise, Lesson, UserProgress
from app.services import track0_service
from app.services.progress_service import XP_POR_PUNTO

TRAZA_SPEC = {
    "pseudocodigo": (
        "Algoritmo Suma\n"
        "    suma <- 0\n"
        "    Para i <- 1 Hasta 3 Hacer\n"
        "        suma <- suma + i\n"
        "    FinPara\n"
        "FinAlgoritmo"
    ),
    "columnas": ["i", "suma"],
    "filas": [{"etiqueta": "Antes del bucle"}, {"etiqueta": "Vuelta 1"}],
}
TRAZA_KEY = {
    "columnas": ["i", "suma"],
    "etiquetas_filas": ["Antes del bucle", "Vuelta 1"],
    "celdas": [["-", "0"], ["1", "1"]],
}


async def _seed(exercise_type="trace_table", spec=None, answer_key=None, points=10):
    async with async_session_maker() as session:
        lesson = Lesson(
            title=f"T0 {exercise_type}",
            description="d",
            content="c",
            track="track-0",
            category="fundamentos",
        )
        session.add(lesson)
        await session.flush()
        ex = Exercise(
            lesson_id=lesson.id,
            title="Traza",
            description="d",
            instructions="i",
            exercise_type=exercise_type,
            spec=spec if spec is not None else TRAZA_SPEC,
            answer_key=answer_key if answer_key is not None else TRAZA_KEY,
            points=points,
            difficulty="easy",
            order=0,
        )
        session.add(ex)
        await session.commit()
        await session.refresh(ex)
        return ex.id, lesson.id


# --------------------------------------------------------------- validadores


def test_traza_correcta_y_su_primer_fallo():
    v = track0_service.validar(
        "trace_table", TRAZA_KEY, {"celdas": [["-", "0"], ["1", "1"]]}
    )
    assert v.passed is True

    v = track0_service.validar(
        "trace_table", TRAZA_KEY, {"celdas": [["-", "0"], ["1", "2"]]}
    )
    assert v.passed is False
    assert v.detalle == {"fila": 1, "columna": 1}
    # Señala dónde, pero no dice cuál era el valor.
    assert "Vuelta 1" in v.feedback and "suma" in v.feedback
    assert "1" not in v.feedback.replace("Vuelta 1", "")


def test_traza_normaliza_espacios_pero_no_admite_otro_valor():
    v = track0_service.validar(
        "trace_table", TRAZA_KEY, {"celdas": [[" - ", "0"], ["1", " 1 "]]}
    )
    assert v.passed is True
    v = track0_service.validar("trace_table", TRAZA_KEY, {"celdas": [["-", "0"]]})
    assert v.passed is False and "filas" in v.feedback


def test_predict_output_normaliza_lineas():
    clave = {"salida": "3\n6\n"}
    assert track0_service.validar("predict_output", clave, {"salida": "3\n6"}).passed
    assert track0_service.validar(
        "predict_output", clave, {"salida": " 3 \n6\n\n"}
    ).passed
    v = track0_service.validar("predict_output", clave, {"salida": "3"})
    assert v.passed is False and "líneas" in v.feedback
    v = track0_service.validar("predict_output", clave, {"salida": "3\n7"})
    assert v.passed is False and v.detalle == {"linea": 1}


def test_mcq_exacta_y_sin_revelar_la_correcta():
    clave = {
        "correcta": 2,
        "motivo": "Porque el bucle no llega a entrar.",
        "pista": "Mira la condición.",
    }
    v = track0_service.validar("mcq", clave, {"opcion": 2})
    assert v.passed is True and v.feedback == clave["motivo"]
    v = track0_service.validar("mcq", clave, {"opcion": 0})
    assert v.passed is False and v.feedback == clave["pista"]
    assert clave["motivo"] not in (v.feedback or "")
    # True es un int en Python: no puede colarse como opción 1.
    assert track0_service.validar("mcq", clave, {"opcion": True}).passed is False


def test_tipo_desconocido_o_sin_clave_es_error_de_configuracion():
    with pytest.raises(track0_service.EjercicioInvalido):
        track0_service.validar("flowchart_fill", {"x": 1}, {})
    with pytest.raises(track0_service.EjercicioInvalido):
        track0_service.validar("trace_table", {}, {"celdas": []})


# ----------------------------------------------------------------- endpoint


@pytest.mark.asyncio
async def test_check_aprueba_y_completa_el_ejercicio(client, auth_headers):
    ex_id, lesson_id = await _seed()

    r = await client.post(
        f"/api/v1/exercises/{ex_id}/check",
        json={"respuesta": {"celdas": [["-", "0"], ["1", "1"]]}},
        headers=auth_headers,
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["passed"] is True and body["completed"] is True

    # Regla 2: el mismo evento de completitud que un ejercicio de Python.
    lección = await client.get(f"/api/v1/lessons/{lesson_id}", headers=auth_headers)
    datos = lección.json()
    assert datos["exercises"][0]["completed"] is True
    assert datos["progress"] == 100


@pytest.mark.asyncio
async def test_check_falla_sin_completar_y_permite_reintentar(client, auth_headers):
    ex_id, lesson_id = await _seed()

    r = await client.post(
        f"/api/v1/exercises/{ex_id}/check",
        json={"respuesta": {"celdas": [["-", "0"], ["1", "9"]]}},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["passed"] is False and r.json()["completed"] is False

    r = await client.post(
        f"/api/v1/exercises/{ex_id}/check",
        json={"respuesta": {"celdas": [["-", "0"], ["1", "1"]]}},
        headers=auth_headers,
    )
    assert r.json()["passed"] is True and r.json()["completed"] is True


@pytest.mark.asyncio
async def test_xp_idempotente_al_aprobar_dos_veces(client, auth_headers):
    ex_id, lesson_id = await _seed(points=20)
    cuerpo = {"respuesta": {"celdas": [["-", "0"], ["1", "1"]]}}

    for _ in range(3):
        r = await client.post(
            f"/api/v1/exercises/{ex_id}/check", json=cuerpo, headers=auth_headers
        )
        assert r.json()["passed"] is True

    async with async_session_maker() as session:
        progreso = (
            await session.execute(
                select(UserProgress).where(UserProgress.lesson_id == lesson_id)
            )
        ).scalar_one()
        # 20 puntos = 200 XP, una sola vez.
        assert progreso.score == 20
        assert progreso.score * XP_POR_PUNTO == 200
        submissions = (
            (
                await session.execute(
                    select(CodeSubmission).where(CodeSubmission.exercise_id == ex_id)
                )
            )
            .scalars()
            .all()
        )
        # El primer acierto crea una submission; los reintentos no duplican.
        assert len(submissions) == 1


@pytest.mark.asyncio
async def test_check_rechaza_los_ejercicios_de_codigo(client, auth_headers):
    ex_id, _ = await _seed(exercise_type="code", spec={}, answer_key={})
    r = await client.post(
        f"/api/v1/exercises/{ex_id}/check",
        json={"respuesta": {"celdas": []}},
        headers=auth_headers,
    )
    assert r.status_code == 400
    assert "/submit" in r.json()["detail"]


@pytest.mark.asyncio
async def test_check_exige_autenticacion(client):
    ex_id, _ = await _seed()
    r = await client.post(
        f"/api/v1/exercises/{ex_id}/check", json={"respuesta": {"celdas": []}}
    )
    assert r.status_code in (401, 403)


# ------------------------------------------------------- guard rail no-leak


@pytest.mark.asyncio
async def test_answer_key_nunca_viaja_al_cliente(client, auth_headers):
    """Regla 3: la solución correcta no sale por ningún endpoint público."""
    ex_id, lesson_id = await _seed()

    respuestas = [
        await client.get(f"/api/v1/lessons/{lesson_id}", headers=auth_headers),
        await client.get(f"/api/v1/exercises/lesson/{lesson_id}", headers=auth_headers),
        await client.get("/api/v1/lessons", headers=auth_headers),
    ]
    for r in respuestas:
        assert r.status_code == 200, r.text
        crudo = r.text
        assert "answer_key" not in crudo
        # Las celdas de la solución tampoco, ni sueltas.
        assert '"celdas"' not in crudo
        assert "etiquetas_filas" not in crudo

    # Pero el enunciado estructurado sí llega: sin él no hay nada que pintar.
    detalle = (
        await client.get(f"/api/v1/lessons/{lesson_id}", headers=auth_headers)
    ).json()
    ejercicio = detalle["exercises"][0]
    assert ejercicio["exercise_type"] == "trace_table"
    assert ejercicio["spec"]["columnas"] == ["i", "suma"]
    assert "Algoritmo Suma" in ejercicio["spec"]["pseudocodigo"]


@pytest.mark.asyncio
async def test_los_ejercicios_de_codigo_siguen_igual(client, auth_headers):
    """Los 198 ejercicios de Tracks 1-6 no cambian de forma."""
    ex_id, lesson_id = await _seed(exercise_type="code", spec={}, answer_key={})
    r = await client.get(f"/api/v1/lessons/{lesson_id}", headers=auth_headers)
    ejercicio = r.json()["exercises"][0]
    assert ejercicio["exercise_type"] == "code"
    assert ejercicio["spec"] is None


# ------------------------------------------- guard rail del contenido seedeado


def test_todo_ejercicio_de_track0_es_corregible():
    """Ningún ejercicio de Track 0 puede quedar sin poder aprobarse.

    El equivalente de `check_hidden_tests_triviales.py` para los tipos que no
    se ejecutan: cada ejercicio tiene `spec` y `answer_key`, su clave se
    aprueba a sí misma, y una respuesta vacía no cuela.
    """
    from app.services.lesson_seed import LESSON_TEMPLATES

    ejercicios = [
        (leccion.title, ex)
        for leccion in LESSON_TEMPLATES
        if leccion.track == "track-0"
        for ex in leccion.exercises
    ]
    assert ejercicios, "Track 0 no tiene ejercicios seedeados"

    for leccion, ex in ejercicios:
        etiqueta = f"{leccion} / {ex.title}"
        assert ex.exercise_type in track0_service.TIPOS_VALIDABLES, etiqueta
        assert ex.spec, f"{etiqueta}: sin spec, no hay nada que pintar"
        assert ex.answer_key, f"{etiqueta}: sin answer_key, no se puede aprobar"
        assert not ex.hidden_tests, f"{etiqueta}: no se ejecuta, no lleva tests"

        if ex.exercise_type == "trace_table":
            respuesta = {"celdas": [list(f) for f in ex.answer_key["celdas"]]}
            vacia = {"celdas": [["" for _ in f] for f in ex.answer_key["celdas"]]}
        elif ex.exercise_type == "predict_output":
            respuesta = {"salida": ex.answer_key["salida"]}
            vacia = {"salida": ""}
        elif ex.exercise_type in ("flowchart_fill", "flowchart_match"):
            campo = "huecos" if ex.exercise_type == "flowchart_fill" else "asignaciones"
            respuesta = {campo: list(ex.answer_key[campo])}
            vacia = {campo: [None] * len(ex.answer_key[campo])}
        else:
            respuesta = {"opcion": ex.answer_key["correcta"]}
            vacia = {}

        assert track0_service.validar(
            ex.exercise_type, ex.answer_key, respuesta
        ).passed, f"{etiqueta}: su propia clave no aprueba"
        assert not track0_service.validar(
            ex.exercise_type, ex.answer_key, vacia
        ).passed, f"{etiqueta}: aprueba con una respuesta vacía"


def test_track0_va_delante_de_track1():
    """El orden curricular tiene que dejar Track 0 antes que Track 1."""
    from app.services.lesson_seed import LESSON_TEMPLATES

    fundamentos = [x.order for x in LESSON_TEMPLATES if x.track == "track-0"]
    python = [x.order for x in LESSON_TEMPLATES if x.track == "track-1"]
    assert fundamentos and python
    assert max(fundamentos) < min(python)


def test_ninguna_categoria_se_comparte_entre_tracks():
    """Una categoría no puede vivir en dos tracks a la vez.

    `Competencies.tsx` agrupa por `category` y mapea cada una a un track, así
    que una categoría compartida funde dos competencias en una tarjeta y la
    manda al track equivocado. Pasó de verdad: Track 0 nació usando
    `fundamentos`, que ya usaban cuatro lecciones de Track 1.
    """
    from collections import defaultdict

    from app.services.lesson_seed import LESSON_TEMPLATES

    tracks_por_categoria = defaultdict(set)
    for leccion in LESSON_TEMPLATES:
        tracks_por_categoria[leccion.category].add(leccion.track)

    compartidas = {
        categoria: sorted(tracks)
        for categoria, tracks in tracks_por_categoria.items()
        if len(tracks) > 1
    }
    assert not compartidas, f"categorías en más de un track: {compartidas}"


def test_el_orden_de_cada_leccion_de_track0_cuadra_con_su_numero():
    """Las 11 lecciones de Track 0 ocupan exactamente los órdenes -10..0.

    `Lesson.order` es global y monótono (Track 1 empieza en 1), así que Track 0
    vive en los negativos y cada lección tiene su hueco reservado: la número N
    va en `N - 11`. Sin esta cuenta es fácil dejar sin sitio a una lección que
    todavía no está escrita — pasó con la 6 (Diagramas de flujo), que se quedó
    sin hueco entre la 5 y la 7.
    """
    import re

    from app.services.lesson_seed import LESSON_TEMPLATES

    for leccion in LESSON_TEMPLATES:
        if leccion.track != "track-0":
            continue
        m = re.match(r"Fundamentos (\d+) ", leccion.title)
        assert m, f"título fuera de convención: {leccion.title}"
        numero = int(m.group(1))
        assert 1 <= numero <= 11, leccion.title
        assert (
            leccion.order == numero - 11
        ), f"{leccion.title}: order {leccion.order}, esperaba {numero - 11}"
