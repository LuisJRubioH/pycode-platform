"""
structlog + redaction de PII (sec. 9.11 del spec).
"""

import logging
import re
from typing import Iterable

import structlog

JWT_PAT = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")
GROQ_PAT = re.compile(r"gsk_[A-Za-z0-9]{20,}")
OPENAI_PAT = re.compile(r"sk-[A-Za-z0-9_-]{20,}")
HF_PAT = re.compile(r"hf_[A-Za-z0-9]{20,}")
EMAIL_PAT = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")


def redact_pii(text: str, allowlist_emails: Iterable[str] = ()) -> str:
    if not isinstance(text, str):
        return text
    out = JWT_PAT.sub("[REDACTED_JWT]", text)
    out = GROQ_PAT.sub("[REDACTED_KEY]", out)
    out = OPENAI_PAT.sub("[REDACTED_KEY]", out)
    out = HF_PAT.sub("[REDACTED_KEY]", out)

    allowlist = set(allowlist_emails)

    def _email_repl(m):
        return m.group(0) if m.group(0) in allowlist else "[REDACTED_EMAIL]"

    out = EMAIL_PAT.sub(_email_repl, out)
    return out


def _redact_processor(logger, method_name, event_dict):
    for key, value in list(event_dict.items()):
        if isinstance(value, str):
            event_dict[key] = redact_pii(value)
    return event_dict


def configure_logging() -> None:
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            _redact_processor,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


logger = structlog.get_logger()
