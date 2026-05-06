def test_settings_reads_new_env_vars(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://abc.supabase.co")
    monkeypatch.setenv("GROQ_API_KEY", "gsk_test")
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("LLM_MODEL", "llama-3.3-70b-versatile")

    from app.core.config import Settings

    s = Settings()
    assert s.SUPABASE_URL == "https://abc.supabase.co"
    assert s.GROQ_API_KEY == "gsk_test"
    assert s.LLM_PROVIDER == "groq"
    assert s.LLM_MODEL == "llama-3.3-70b-versatile"
    assert s.ACCESS_TOKEN_EXPIRE_MINUTES == 60  # nuevo default
    assert s.REFRESH_TOKEN_EXPIRE_DAYS == 7
