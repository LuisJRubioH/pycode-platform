"""
Sentry init con scrubbing de PII en `before_send`.
"""
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from app.core.config import settings
from app.core.logging_config import redact_pii


def _scrub_event(event, hint):
    if "request" in event and "headers" in event["request"]:
        for header in ("authorization", "cookie"):
            event["request"]["headers"].pop(header, None)
            event["request"]["headers"].pop(header.title(), None)
    msg = event.get("message")
    if isinstance(msg, str):
        event["message"] = redact_pii(msg)
    for exc in event.get("exception", {}).get("values", []):
        val = exc.get("value")
        if isinstance(val, str):
            exc["value"] = redact_pii(val)
    return event


def init_sentry() -> None:
    if not settings.SENTRY_DSN:
        return
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        integrations=[StarletteIntegration(), FastApiIntegration()],
        traces_sample_rate=0.1 if settings.ENVIRONMENT == "production" else 1.0,
        send_default_pii=False,
        before_send=_scrub_event,
    )
