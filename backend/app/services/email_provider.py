"""
Abstracción de proveedor de email, con el mismo patrón que `llm_provider.py`:
varios proveedores reales intercambiables y un stub determinista para
desarrollo y tests.

Todos van por **API HTTP y no por SMTP** a propósito: Render free bloquea los
puertos SMTP salientes (25/465/587), así que un `smtplib` se quedaría colgado
hasta el timeout en producción mientras funciona de maravilla en local — el
peor modo de fallo posible, igual que el tutor caído del 2026-09-15.

Hay tres porque **ninguno garantiza que te deje abrir la cuenta**: uno pide
verificación por SMS, otro exige dominio propio, otro rechaza remitentes de
Gmail. Cambiar de uno a otro es una variable de entorno (`EMAIL_PROVIDER`), no
un cambio de código, precisamente para que un registro atascado no bloquee la
plataforma.

Todos comparten el mismo contrato: enviar desde `EMAIL_FROM` (una dirección
verificada en el proveedor) y **nunca lanzar** — el caller no debe revelar al
usuario si el envío funcionó.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

import httpx
import structlog

logger = structlog.get_logger()

TIMEOUT_SEGUNDOS = 10.0


class EmailProvider(ABC):
    @abstractmethod
    async def send(self, to: str, subject: str, html: str, text: str) -> bool:
        """Devuelve True si el correo salió. Nunca lanza."""
        ...


class _ProveedorHttp(EmailProvider):
    """Base de los proveedores que mandan por API HTTP.

    Cada uno solo define su URL, sus cabeceras y la forma de su payload: el
    envío, el timeout y el tratamiento de errores son idénticos y viven aquí.
    """

    #: Nombre para los logs.
    nombre = "http"
    #: URL del endpoint de envío.
    api_url = ""

    def __init__(self, from_email: str, from_name: str):
        self.from_email = from_email
        self.from_name = from_name

    def _cabeceras(self) -> dict[str, str]:
        raise NotImplementedError

    def _payload(self, to: str, subject: str, html: str, text: str) -> dict[str, Any]:
        raise NotImplementedError

    def _auth(self) -> Optional[tuple[str, str]]:
        """Basic auth, para los proveedores que lo usan en vez de cabecera."""
        return None

    def _crear_cliente(self) -> httpx.AsyncClient:
        # Método aparte para que los tests lo sustituyan sin tocar la red.
        return httpx.AsyncClient(timeout=TIMEOUT_SEGUNDOS)

    async def send(self, to: str, subject: str, html: str, text: str) -> bool:
        try:
            async with self._crear_cliente() as client:
                resp = await client.post(
                    self.api_url,
                    json=self._payload(to, subject, html, text),
                    headers=self._cabeceras(),
                    auth=self._auth(),
                )
        except httpx.HTTPError as exc:
            logger.error("email_envio_fallido", motivo=str(exc), proveedor=self.nombre)
            return False

        if resp.status_code >= 400:
            # El cuerpo trae el motivo real (remitente sin verificar, cuota
            # agotada, cuenta sin aprobar...). No lleva secretos: la clave va
            # en la cabecera o en el auth, nunca en la respuesta.
            logger.error(
                "email_rechazado",
                proveedor=self.nombre,
                status=resp.status_code,
                cuerpo=resp.text[:300],
            )
            return False

        logger.info("email_enviado", proveedor=self.nombre, status=resp.status_code)
        return True


class BrevoProvider(_ProveedorHttp):
    """Brevo (ex-Sendinblue). 300 correos/día gratis.

    Permite verificar un remitente individual sin dominio propio, pero **exige
    verificar el teléfono por SMS** antes de dejarte crear una clave API.
    """

    nombre = "brevo"
    api_url = "https://api.brevo.com/v3/smtp/email"

    def __init__(self, api_key: str, from_email: str, from_name: str):
        super().__init__(from_email, from_name)
        self.api_key = api_key

    def _cabeceras(self) -> dict[str, str]:
        return {
            "api-key": self.api_key,
            "accept": "application/json",
            "content-type": "application/json",
        }

    def _payload(self, to: str, subject: str, html: str, text: str) -> dict[str, Any]:
        return {
            "sender": {"email": self.from_email, "name": self.from_name},
            "to": [{"email": to}],
            "subject": subject,
            "htmlContent": html,
            "textContent": text,
        }


class SendGridProvider(_ProveedorHttp):
    """SendGrid (Twilio). 100 correos/día gratis, sin caducidad.

    Su *Single Sender Verification* está pensada justo para quien no tiene
    dominio: verificas una dirección suelta (un Gmail vale) pulsando un enlace.
    El 2FA obligatorio de la cuenta se puede resolver con una app de
    autenticación, sin SMS.
    """

    nombre = "sendgrid"
    api_url = "https://api.sendgrid.com/v3/mail/send"

    def __init__(self, api_key: str, from_email: str, from_name: str):
        super().__init__(from_email, from_name)
        self.api_key = api_key

    def _cabeceras(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _payload(self, to: str, subject: str, html: str, text: str) -> dict[str, Any]:
        # El orden de `content` importa: SendGrid exige text/plain antes que
        # text/html y responde 400 si van al revés.
        return {
            "personalizations": [{"to": [{"email": to}]}],
            "from": {"email": self.from_email, "name": self.from_name},
            "subject": subject,
            "content": [
                {"type": "text/plain", "value": text},
                {"type": "text/html", "value": html},
            ],
        }


class MailjetProvider(_ProveedorHttp):
    """Mailjet. 200 correos/día (6.000/mes) gratis.

    Se autentica con Basic auth: clave pública como usuario y clave secreta
    como contraseña. Por eso necesita dos variables y no una.
    """

    nombre = "mailjet"
    api_url = "https://api.mailjet.com/v3.1/send"

    def __init__(self, api_key: str, api_secret: str, from_email: str, from_name: str):
        super().__init__(from_email, from_name)
        self.api_key = api_key
        self.api_secret = api_secret

    def _cabeceras(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}

    def _auth(self) -> Optional[tuple[str, str]]:
        return (self.api_key, self.api_secret)

    def _payload(self, to: str, subject: str, html: str, text: str) -> dict[str, Any]:
        return {
            "Messages": [
                {
                    "From": {"Email": self.from_email, "Name": self.from_name},
                    "To": [{"Email": to}],
                    "Subject": subject,
                    "TextPart": text,
                    "HTMLPart": html,
                }
            ]
        }


class ConsoleProvider(EmailProvider):
    """Sin credenciales no se envía nada: se registra en el log y se sigue.

    Es lo que corre en desarrollo y en los tests. Deja el enlace en el log para
    poder probar el flujo entero en local sin cuenta en ningún proveedor.
    """

    async def send(self, to: str, subject: str, html: str, text: str) -> bool:
        logger.warning(
            "email_no_enviado_sin_proveedor",
            destinatario=to,
            asunto=subject,
            cuerpo=text,
        )
        return True


def get_email_provider(settings) -> EmailProvider:
    """Despacha por `EMAIL_PROVIDER`.

    Si al proveedor elegido le faltan credenciales se cae al `ConsoleProvider`
    en vez de reventar: que falte una variable de entorno no debe tumbar el
    registro ni el login. Queda en el log, que es donde se diagnostica.
    """
    nombre = settings.EMAIL_PROVIDER.lower()
    from_email = settings.EMAIL_FROM
    from_name = settings.EMAIL_FROM_NAME

    if nombre == "brevo":
        if not settings.BREVO_API_KEY:
            logger.warning("email_sin_credenciales_usando_consola", proveedor=nombre)
            return ConsoleProvider()
        return BrevoProvider(settings.BREVO_API_KEY, from_email, from_name)

    if nombre == "sendgrid":
        if not settings.SENDGRID_API_KEY:
            logger.warning("email_sin_credenciales_usando_consola", proveedor=nombre)
            return ConsoleProvider()
        return SendGridProvider(settings.SENDGRID_API_KEY, from_email, from_name)

    if nombre == "mailjet":
        if not (settings.MAILJET_API_KEY and settings.MAILJET_API_SECRET):
            logger.warning("email_sin_credenciales_usando_consola", proveedor=nombre)
            return ConsoleProvider()
        return MailjetProvider(
            settings.MAILJET_API_KEY,
            settings.MAILJET_API_SECRET,
            from_email,
            from_name,
        )

    if nombre == "console":
        return ConsoleProvider()

    logger.warning("email_provider_desconocido", nombre=nombre)
    return ConsoleProvider()
