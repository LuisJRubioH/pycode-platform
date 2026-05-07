from app.core.logging_config import redact_pii


def test_redact_jwt():
    msg = "token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOjF9.signature"
    out = redact_pii(msg)
    assert "eyJ" not in out
    assert "[REDACTED_JWT]" in out


def test_redact_groq_key():
    msg = "key=gsk_abc123def456ghi789jkl012mno345pqr678stu"
    out = redact_pii(msg)
    assert "gsk_abc" not in out
    assert "[REDACTED_KEY]" in out


def test_redact_openai_key():
    msg = "key=sk-proj-abcdefghijklmnopqrstuvwxyz0123456789"
    out = redact_pii(msg)
    assert "sk-proj" not in out
    assert "[REDACTED_KEY]" in out


def test_redact_email():
    msg = "user logged in: alice@example.com"
    out = redact_pii(msg)
    assert "alice@example.com" not in out
    assert "[REDACTED_EMAIL]" in out


def test_does_not_redact_admin_email():
    msg = "admin notification to admin@pycode.app"
    out = redact_pii(msg, allowlist_emails=["admin@pycode.app"])
    assert "admin@pycode.app" in out
