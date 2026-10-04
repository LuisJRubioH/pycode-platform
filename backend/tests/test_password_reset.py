"""
Recuperación de contraseña por email: emisión, canje y los filtrados que no
debe haber.
"""

import uuid
from datetime import timedelta

import pytest
from sqlalchemy import select

from app.core.config import settings
from app.core.database import async_session_maker
from app.models.password_reset import PasswordResetToken
from app.models.refresh_token import RefreshToken
from app.services import password_reset_service
from app.services.email_provider import EmailProvider


class ProveedorEspia(EmailProvider):
    """Guarda lo que se habría enviado en vez de enviarlo."""

    def __init__(self):
        self.enviados = []

    async def send(self, to, subject, html, text):
        self.enviados.append({"to": to, "subject": subject, "html": html, "text": text})
        return True


@pytest.fixture
def espia(monkeypatch):
    proveedor = ProveedorEspia()
    monkeypatch.setattr(
        password_reset_service, "get_email_provider", lambda _s: proveedor
    )
    return proveedor


async def _registrar(client, password="TestPass123"):
    suf = uuid.uuid4().hex[:8]
    datos = {
        "email": f"reset_{suf}@example.com",
        "username": f"reset{suf}",
        "password": password,
    }
    r = await client.post("/api/v1/auth/register", json=datos)
    assert r.status_code == 201, r.text
    return datos


def _token_del_correo(espia) -> str:
    assert espia.enviados, "no se envió ningún correo"
    texto = espia.enviados[-1]["text"]
    marca = "?token="
    inicio = texto.index(marca) + len(marca)
    return texto[inicio:].split()[0].strip()


async def _pedir_reset(client, email):
    return await client.post(
        "/api/v1/auth/password-reset/request", json={"email": email}
    )


# --- el flujo feliz -------------------------------------------------------


@pytest.mark.asyncio
async def test_flujo_completo_cambia_la_contrasena(client, espia):
    datos = await _registrar(client)

    assert (await _pedir_reset(client, datos["email"])).status_code == 204
    token = _token_del_correo(espia)

    r = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"token": token, "password": "NuevaClave456"},
    )
    assert r.status_code == 204, r.text

    vieja = await client.post(
        "/api/v1/auth/login",
        json={"email": datos["email"], "password": datos["password"]},
    )
    assert vieja.status_code == 401

    nueva = await client.post(
        "/api/v1/auth/login",
        json={"email": datos["email"], "password": "NuevaClave456"},
    )
    assert nueva.status_code == 200


@pytest.mark.asyncio
async def test_el_correo_va_al_titular_y_lleva_el_enlace(client, espia):
    datos = await _registrar(client)
    await _pedir_reset(client, datos["email"])

    correo = espia.enviados[-1]
    assert correo["to"] == datos["email"]
    assert "/reset-password?token=" in correo["text"]
    assert "/reset-password?token=" in correo["html"]


# --- lo que no se puede filtrar -------------------------------------------


@pytest.mark.asyncio
async def test_email_inexistente_responde_igual_y_no_envia(client, espia):
    """Mismo 204 que una cuenta real: el formulario no es un detector de emails."""
    r = await _pedir_reset(client, "no-existe-nadie@example.com")
    assert r.status_code == 204
    assert espia.enviados == []


@pytest.mark.asyncio
async def test_el_token_no_se_guarda_en_claro(client, espia):
    datos = await _registrar(client)
    await _pedir_reset(client, datos["email"])
    token = _token_del_correo(espia)

    async with async_session_maker() as session:
        filas = (await session.execute(select(PasswordResetToken))).scalars().all()
        hashes = [f.token_hash for f in filas]

    assert token not in hashes
    assert password_reset_service.hash_token(token) in hashes


# --- el token como llave de un solo uso -----------------------------------


@pytest.mark.asyncio
async def test_el_token_no_sirve_dos_veces(client, espia):
    datos = await _registrar(client)
    await _pedir_reset(client, datos["email"])
    token = _token_del_correo(espia)

    primero = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"token": token, "password": "NuevaClave456"},
    )
    assert primero.status_code == 204

    segundo = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"token": token, "password": "OtraMas789"},
    )
    assert segundo.status_code == 400


@pytest.mark.asyncio
async def test_token_caducado_no_sirve(client, espia, monkeypatch):
    monkeypatch.setattr(settings, "PASSWORD_RESET_TOKEN_TTL_MINUTES", -1)
    datos = await _registrar(client)
    await _pedir_reset(client, datos["email"])
    token = _token_del_correo(espia)

    r = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"token": token, "password": "NuevaClave456"},
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_token_inventado_no_sirve(client):
    r = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"token": "x" * 43, "password": "NuevaClave456"},
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_pedir_otro_enlace_invalida_el_anterior(client, espia, monkeypatch):
    """Si no, cada petición dejaría otra llave viva suelta en otro buzón."""
    monkeypatch.setattr(password_reset_service, "ESPERA_ENTRE_ENVIOS", timedelta(0))
    datos = await _registrar(client)

    await _pedir_reset(client, datos["email"])
    primer_token = _token_del_correo(espia)
    await _pedir_reset(client, datos["email"])
    segundo_token = _token_del_correo(espia)
    assert primer_token != segundo_token

    viejo = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"token": primer_token, "password": "NuevaClave456"},
    )
    assert viejo.status_code == 400

    nuevo = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"token": segundo_token, "password": "NuevaClave456"},
    )
    assert nuevo.status_code == 204


@pytest.mark.asyncio
async def test_dos_peticiones_seguidas_solo_mandan_un_correo(client, espia):
    """Para que nadie use el formulario para bombardear el buzón de otro."""
    datos = await _registrar(client)

    await _pedir_reset(client, datos["email"])
    await _pedir_reset(client, datos["email"])

    assert len(espia.enviados) == 1


@pytest.mark.asyncio
async def test_el_reset_cierra_las_sesiones_abiertas(client, espia):
    """Cambiar la contraseña sin echar al intruso lo dejaría dentro."""
    datos = await _registrar(client)
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": datos["email"], "password": datos["password"]},
    )
    refresh_token = login.json()["refresh_token"]
    user_id = login.json()["user_id"]

    await _pedir_reset(client, datos["email"])
    await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"token": _token_del_correo(espia), "password": "NuevaClave456"},
    )

    async with async_session_maker() as session:
        filas = (
            (
                await session.execute(
                    select(RefreshToken).where(RefreshToken.user_id == user_id)
                )
            )
            .scalars()
            .all()
        )
    assert filas and all(f.revoked for f in filas)

    r = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert r.status_code == 401


# --- la contraseña nueva pasa por las mismas reglas -----------------------


@pytest.mark.asyncio
async def test_la_contrasena_nueva_tambien_se_valida(client, espia):
    datos = await _registrar(client)
    await _pedir_reset(client, datos["email"])
    token = _token_del_correo(espia)

    r = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"token": token, "password": "corta1"},
    )
    assert r.status_code == 422
