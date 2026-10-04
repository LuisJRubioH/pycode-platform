"""
Abstracción de proveedor de email, con el mismo patrón que `llm_provider.py`:
un proveedor real y un stub determinista para desarrollo y tests.

Se usa la API HTTP de Brevo y no SMTP a propósito: Render free bloquea los
puertos SMTP salientes (25/465/587), así que un `smtplib` se quedaría colgado
hasta el timeout en producción mientras funciona de maravilla en local — el
peor modo de fallo posible, igual que el tutor caído del 2026-09-15.
"""

from abc import ABC, abstractmethod

import httpx
import structlog

logger = structlog.get_logger()

TIMEOUT_SEGUNDOS = 10.0


class EmailProvider(ABC):
    @abstractmethod
    async def send(self, to: str, subject: str, html: str, text: str) -> bool:
        """Devuelve True si el correo salió. Nunca lanza: el caller no debe
        revelar al usuario si el envío funcionó (ver `auth.password_reset`)."""
        ...


class BrevoProvider(EmailProvider):
    API_URL = "https://api.brevo.com/v3/smtp/email"

    def __init__(self, api_key: str, from_email: str, from_name: str):
        self.api_key = api_key
        self.from_email = from_email
        self.from_name = from_name

    async def send(self, to: str, subject: str, html: str, text: str) -> bool:
        payload = {
            "sender": {"email": self.from_email, "name": self.from_name},
            "to": [{"email": to}],
            "subject": subject,
            "htmlContent": html,
            "textContent": text,
        }
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT_SEGUNDOS) as client:
                resp = await client.post(
                    self.API_URL,
                    json=payload,
                    headers={
                        "api-key": self.api_key,
                        "accept": "application/json",
                        "content-type": "application/json",
                    },
                )
        except httpx.HTTPError as exc:
            logger.error("email_envio_fallido", motivo=str(exc), proveedor="brevo")
            return False

        if resp.status_code >= 400:
            # El cuerpo de Brevo trae el motivo (remitente sin verificar, cuota
            # agotada...). No lleva secretos: el api-key va en la cabecera.
            logger.error(
                "email_rechazado",
                proveedor="brevo",
                status=resp.status_code,
                cuerpo=resp.text[:300],
            )
            return False

        logger.info("email_enviado", proveedor="brevo", status=resp.status_code)
        return True


class ConsoleProvider(EmailProvider):
    """Sin API key no se envía nada: se registra en el log y se sigue.

    Es lo que corre en desarrollo y en los tests. Deja el enlace en el log para
    poder probar el flujo entero en local sin cuenta de Brevo.
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
    nombre = settings.EMAIL_PROVIDER.lower()
    if nombre == "brevo":
        if not settings.BREVO_API_KEY:
            logger.warning("brevo_sin_api_key_usando_consola")
            return ConsoleProvider()
        return BrevoProvider(
            api_key=settings.BREVO_API_KEY,
            from_email=settings.EMAIL_FROM,
            from_name=settings.EMAIL_FROM_NAME,
        )
    if nombre == "console":
        return ConsoleProvider()
    logger.warning("email_provider_desconocido", nombre=nombre)
    return ConsoleProvider()
