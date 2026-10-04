"""
Los tres proveedores de email y el despacho entre ellos.

Ninguno sale a la red: se sustituye el cliente HTTP por uno falso que guarda
la petición que se habría hecho. Lo que se comprueba es que cada uno manda el
payload con la forma que espera SU API — que es justo lo que no se puede
verificar a ojo y lo que rompe un envío en silencio.
"""

from dataclasses import dataclass, field
from typing import Any, Optional

import httpx
import pytest

from app.services.email_provider import (
    BrevoProvider,
    ConsoleProvider,
    MailjetProvider,
    SendGridProvider,
    get_email_provider,
)


@dataclass
class RespuestaFalsa:
    status_code: int = 202
    text: str = ""


@dataclass
class ClienteFalso:
    """Sustituye a httpx.AsyncClient y registra la llamada."""

    respuesta: RespuestaFalsa
    excepcion: Optional[Exception] = None
    llamadas: list[dict[str, Any]] = field(default_factory=list)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        return False

    async def post(self, url, json=None, headers=None, auth=None):
        self.llamadas.append(
            {"url": url, "json": json, "headers": headers, "auth": auth}
        )
        if self.excepcion is not None:
            raise self.excepcion
        return self.respuesta


def _instrumentar(proveedor, status=202, texto="", excepcion=None):
    """Hace que el proveedor use un cliente falso y lo devuelve."""
    cliente = ClienteFalso(RespuestaFalsa(status, texto), excepcion)
    proveedor._crear_cliente = lambda: cliente
    return cliente


async def _enviar(proveedor):
    return await proveedor.send(
        to="alumno@example.com",
        subject="Recupera tu contraseña de PyCode",
        html="<p>hola</p>",
        text="hola",
    )


# --- la forma del payload de cada API -------------------------------------


@pytest.mark.asyncio
async def test_brevo_manda_el_payload_que_espera_brevo():
    p = BrevoProvider("clave-brevo", "yo@example.com", "PyCode Platform")
    cliente = _instrumentar(p, status=201)

    assert await _enviar(p) is True

    llamada = cliente.llamadas[0]
    assert llamada["url"] == "https://api.brevo.com/v3/smtp/email"
    assert llamada["headers"]["api-key"] == "clave-brevo"
    cuerpo = llamada["json"]
    assert cuerpo["sender"] == {"email": "yo@example.com", "name": "PyCode Platform"}
    assert cuerpo["to"] == [{"email": "alumno@example.com"}]
    assert cuerpo["htmlContent"] == "<p>hola</p>"
    assert cuerpo["textContent"] == "hola"


@pytest.mark.asyncio
async def test_sendgrid_manda_el_payload_que_espera_sendgrid():
    p = SendGridProvider("clave-sg", "yo@example.com", "PyCode Platform")
    cliente = _instrumentar(p, status=202)

    assert await _enviar(p) is True

    llamada = cliente.llamadas[0]
    assert llamada["url"] == "https://api.sendgrid.com/v3/mail/send"
    assert llamada["headers"]["Authorization"] == "Bearer clave-sg"
    cuerpo = llamada["json"]
    assert cuerpo["personalizations"] == [{"to": [{"email": "alumno@example.com"}]}]
    assert cuerpo["from"]["email"] == "yo@example.com"
    # SendGrid exige text/plain ANTES que text/html; al revés responde 400.
    assert [c["type"] for c in cuerpo["content"]] == ["text/plain", "text/html"]


@pytest.mark.asyncio
async def test_mailjet_manda_el_payload_y_usa_basic_auth():
    p = MailjetProvider("clave", "secreto", "yo@example.com", "PyCode Platform")
    cliente = _instrumentar(p, status=200)

    assert await _enviar(p) is True

    llamada = cliente.llamadas[0]
    assert llamada["url"] == "https://api.mailjet.com/v3.1/send"
    # Mailjet autentica con clave pública + secreta, no con cabecera.
    assert llamada["auth"] == ("clave", "secreto")
    mensaje = llamada["json"]["Messages"][0]
    assert mensaje["From"]["Email"] == "yo@example.com"
    assert mensaje["To"] == [{"Email": "alumno@example.com"}]
    assert mensaje["TextPart"] == "hola"
    assert mensaje["HTMLPart"] == "<p>hola</p>"


# --- ningún fallo puede propagarse ----------------------------------------


@pytest.mark.parametrize(
    "proveedor",
    [
        BrevoProvider("k", "yo@example.com", "PyCode"),
        SendGridProvider("k", "yo@example.com", "PyCode"),
        MailjetProvider("k", "s", "yo@example.com", "PyCode"),
    ],
    ids=["brevo", "sendgrid", "mailjet"],
)
@pytest.mark.asyncio
async def test_un_rechazo_devuelve_false_y_no_lanza(proveedor):
    """Remitente sin verificar, cuota agotada, cuenta sin aprobar..."""
    _instrumentar(proveedor, status=400, texto="sender not verified")
    assert await proveedor.send("a@b.com", "s", "<p>h</p>", "t") is False


@pytest.mark.parametrize(
    "proveedor",
    [
        BrevoProvider("k", "yo@example.com", "PyCode"),
        SendGridProvider("k", "yo@example.com", "PyCode"),
        MailjetProvider("k", "s", "yo@example.com", "PyCode"),
    ],
    ids=["brevo", "sendgrid", "mailjet"],
)
@pytest.mark.asyncio
async def test_una_caida_de_red_devuelve_false_y_no_lanza(proveedor):
    """Si esto lanzara, un timeout del proveedor tumbaría el endpoint."""
    _instrumentar(proveedor, excepcion=httpx.ConnectError("sin red"))
    assert await proveedor.send("a@b.com", "s", "<p>h</p>", "t") is False


# --- el despacho ----------------------------------------------------------


class AjustesFalsos:
    EMAIL_FROM = "yo@example.com"
    EMAIL_FROM_NAME = "PyCode Platform"
    BREVO_API_KEY = ""
    SENDGRID_API_KEY = ""
    MAILJET_API_KEY = ""
    MAILJET_API_SECRET = ""

    def __init__(self, proveedor, **claves):
        self.EMAIL_PROVIDER = proveedor
        for k, v in claves.items():
            setattr(self, k, v)


@pytest.mark.parametrize(
    "proveedor,claves,esperado",
    [
        ("brevo", {"BREVO_API_KEY": "k"}, BrevoProvider),
        ("sendgrid", {"SENDGRID_API_KEY": "k"}, SendGridProvider),
        (
            "mailjet",
            {"MAILJET_API_KEY": "k", "MAILJET_API_SECRET": "s"},
            MailjetProvider,
        ),
        ("SendGrid", {"SENDGRID_API_KEY": "k"}, SendGridProvider),  # sin distinguir
        ("console", {}, ConsoleProvider),
    ],
)
def test_el_despacho_elige_el_proveedor(proveedor, claves, esperado):
    assert isinstance(get_email_provider(AjustesFalsos(proveedor, **claves)), esperado)


@pytest.mark.parametrize(
    "proveedor,claves",
    [
        ("brevo", {}),
        ("sendgrid", {}),
        ("mailjet", {}),
        ("mailjet", {"MAILJET_API_KEY": "k"}),  # falta el secreto
        ("inventado", {}),
    ],
)
def test_sin_credenciales_cae_a_consola_en_vez_de_reventar(proveedor, claves):
    """Que falte una variable de entorno no puede tumbar el registro."""
    assert isinstance(
        get_email_provider(AjustesFalsos(proveedor, **claves)), ConsoleProvider
    )
