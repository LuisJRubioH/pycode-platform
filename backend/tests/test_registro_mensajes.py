"""
Los errores de registro tienen que decir QUÉ campo falla y POR QUÉ, en español.

Regresión de un fallo real: un alumno vio "String should match pattern
'^[a-zA-Z0-9_-]+$'" en un aviso genérico encima del formulario y lo leyó como
un problema de la contraseña. El patrón era el del nombre de usuario. Estuvo
cambiando la contraseña intento tras intento sin tocar el campo que fallaba.
"""

import pytest


def _errores_por_campo(respuesta):
    """{campo: mensaje} a partir del 422 de FastAPI."""
    return {d["loc"][-1]: d["msg"] for d in respuesta.json()["detail"] if d.get("loc")}


async def _registrar(client, **sobrescribe):
    datos = {
        "email": "nuevo@example.com",
        "username": "usuariovalido",
        "password": "ClaveValida123",
    }
    datos.update(sobrescribe)
    return await client.post("/api/v1/auth/register", json=datos)


@pytest.mark.asyncio
async def test_el_username_invalido_no_acusa_a_la_contrasena(client):
    """El bug exacto que se reportó, en forma de test."""
    r = await _registrar(client, username="con espacio")
    assert r.status_code == 422

    errores = _errores_por_campo(r)
    assert "username" in errores
    assert "password" not in errores


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username",
    ["con espacio", "con.punto", "añoNuevo", "con@arroba", "con/barra"],
)
async def test_usernames_rechazados_explican_el_motivo(client, username):
    r = await _registrar(client, username=username)
    assert r.status_code == 422

    mensaje = _errores_por_campo(r)["username"]
    # Pydantic antepone "Value error, " al texto del validador.
    assert "nombre de usuario" in mensaje
    assert "pattern" not in mensaje, "se está filtrando la regex al alumno"


@pytest.mark.asyncio
async def test_username_corto_dice_cuantos_caracteres_faltan(client):
    r = await _registrar(client, username="ab")
    assert r.status_code == 422
    assert "al menos 3 caracteres" in _errores_por_campo(r)["username"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "password,esperado",
    [
        ("Corta1", "al menos 8 caracteres"),
        ("sinnumeros", "al menos un número"),
        ("12345678", "al menos una letra"),
    ],
)
async def test_contrasenas_rechazadas_explican_el_motivo(client, password, esperado):
    r = await _registrar(client, password=password)
    assert r.status_code == 422

    errores = _errores_por_campo(r)
    assert "password" in errores
    assert esperado in errores["password"]
    assert "username" not in errores


@pytest.mark.asyncio
async def test_los_mensajes_van_en_espanol(client):
    """Nada de texto crudo de Pydantic en inglés llegando al alumno."""
    r = await _registrar(client, username="x", password="corta")
    errores = _errores_por_campo(r)

    for mensaje in errores.values():
        assert "String should" not in mensaje
        assert "should have at least" not in mensaje


@pytest.mark.asyncio
async def test_el_422_no_devuelve_la_contrasena_enviada(client):
    """Pydantic mete un `input` con el valor rechazado en cada error.

    Para /auth/register eso es la contraseña en claro viajando de vuelta dentro
    del cuerpo del 422, que acaba en logs y en cualquier proxy del camino. El
    handler de `main.py` deja solo loc/msg/type.
    """
    secreta = "ClaveSecretisima"  # sin dígito: la rechaza el validador
    r = await _registrar(client, password=secreta)
    assert r.status_code == 422
    assert secreta not in r.text

    for error in r.json()["detail"]:
        assert set(error) == {"loc", "msg", "type"}


@pytest.mark.asyncio
async def test_el_mensaje_no_arrastra_el_prefijo_de_pydantic(client):
    r = await _registrar(client, username="con espacio")
    assert not _errores_por_campo(r)["username"].startswith("Value error")
