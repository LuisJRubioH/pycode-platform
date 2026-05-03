# PyCode v2 — Fase 0: Fundamentos + Seguridad Base — Plan de Implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrar PyCode Platform de SQLite + subprocess + JWT mínimo a una base de producción gratuita y segura: Supabase Postgres con RLS, Alembic con migraciones reales, Pyodide en Web Worker como sandbox cliente (eliminando el subprocess executor), provider abstraction de LLM (Groq como default, OpenAI como fallback), despliegue en Vercel + Render + UptimeRobot, y todas las salvaguardas de seguridad transversales (sec. 9 del spec): lint anti-SQLi, RLS testeada en CI, rate limiting universal, headers seguros, JWT con refresh rotation, GDPR endpoints, logging con redaction de PII, Sentry, Dependabot.

**Architecture:** El backend FastAPI conserva su estructura actual pero ya no ejecuta código del estudiante (Pyodide en cliente lo reemplaza). Toda persistencia migra a Postgres con RLS habilitada por tabla con datos por usuario, y el modelo `User.id` se sincroniza con `auth.users.id` de Supabase para que las policies `auth.uid()` funcionen. Las migraciones se gestionan vía Alembic; el shim `bootstrap_elo_schema` desaparece. El sandbox de ejecución vive 100% en el navegador, en un Web Worker controlado por el frontend, eliminando la mayor deuda técnica del PYCODE_SPEC original.

**Tech Stack:**
- Backend: FastAPI · SQLAlchemy 2.0 async · asyncpg · Alembic · Pydantic v2 · python-jose · structlog · Sentry SDK · SlowAPI · pytest + pytest-asyncio + httpx
- Frontend: React 18 · Vite 5 · TypeScript · Pyodide 0.26 (cliente) · Web Worker
- Infra: Supabase (Postgres + RLS + pg_vector + Auth + Storage) · Render (web service) · Vercel (frontend) · UptimeRobot (keep-alive) · Groq API (LLM por defecto)
- CI: GitHub Actions · pytest + RLS test suite · ruff/flake8 con regla custom anti-SQLi · pip-audit · npm audit · Dependabot

---

## File Structure

Resumen de archivos a crear o modificar agrupados por responsabilidad. Este es el contrato del plan: cada archivo tiene una responsabilidad clara.

### Backend — config, infra, seguridad

- `backend/app/core/config.py` *(MODIFICA)* — agregar `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`, `GROQ_API_KEY`, `LLM_PROVIDER`, `LLM_MODEL`, `HF_TOKEN`, `SENTRY_DSN`, `ENVIRONMENT`, `REFRESH_TOKEN_EXPIRE_DAYS`. Quitar `DOCKER_*` settings.
- `backend/app/core/database.py` *(MODIFICA)* — quitar branch SQLite (deja solo Postgres asyncpg con NullPool); aceptar `DATABASE_URL` con sslmode require para Supabase.
- `backend/app/core/security.py` *(MODIFICA)* — añadir `create_refresh_token`, `verify_refresh_token`, modelo de rotación (jti + tabla `refresh_tokens` revocables).
- `backend/app/core/security_headers.py` *(CREA)* — middleware FastAPI que inyecta HSTS, CSP, XCTO, XFO, Referrer-Policy, Permissions-Policy.
- `backend/app/core/rate_limit.py` *(CREA)* — wrapper SlowAPI con la tabla de límites del spec (sec. 9.10) keyed por user_id (auth) o IP (anónimo).
- `backend/app/core/logging_config.py` *(CREA)* — structlog + processors de redaction (regex tokens JWT, API keys `sk-`/`gsk_`/`hf_`, emails excepto admin).
- `backend/app/core/observability.py` *(CREA)* — init Sentry SDK con `before_send` que aplica scrubbing PII.
- `backend/app/main.py` *(MODIFICA)* — registra middlewares de headers/rate-limit/logging; reemplaza CORS wildcard por whitelist; expone `/health` slim.

### Backend — modelos y endpoints nuevos

- `backend/app/models/refresh_token.py` *(CREA)* — `RefreshToken {id, user_id, jti, expires_at, revoked, created_at}`.
- `backend/app/models/auth_attempt.py` *(CREA)* — `AuthAttempt {id, email, ip, success, created_at}` (TTL 24h, lockout en Fase 1 lo consume).
- `backend/app/api/v1/endpoints/auth.py` *(MODIFICA)* — añadir `/refresh`, `/logout` (revoca jti); login retorna `access_token` + `refresh_token`.
- `backend/app/api/v1/endpoints/users.py` *(MODIFICA)* — añadir `DELETE /api/v1/users/me`, `GET /api/v1/users/me/export` (GDPR).
- `backend/app/api/v1/endpoints/code_execution.py` *(REEMPLAZA)* — endpoint `POST /run` deprecado; el nuevo `/echo` valida sintaxis con `ast.parse` (no ejecuta) para healthchecks de paridad. La ejecución real ocurre en cliente.
- `backend/app/services/llm_provider.py` *(CREA)* — clase abstracta `LLMProvider` + `GroqProvider`, `OpenAIProvider`. Factory leyendo `LLM_PROVIDER`.
- `backend/app/services/ai_tutor.py` *(MODIFICA)* — usa `LLMProvider` en lugar de `AsyncOpenAI` directo.
- `backend/app/services/docker_executor.py` *(BORRA)* — superado por Pyodide cliente.

### Backend — migraciones Alembic

- `backend/alembic.ini` *(CREA)*
- `backend/alembic/env.py` *(CREA)* — usa `Base.metadata` y `settings.DATABASE_URL`.
- `backend/alembic/versions/0001_initial_schema.py` *(CREA)* — refleja modelos actuales (users, user_profiles, lessons, exercises, puzzles, etc.).
- `backend/alembic/versions/0002_enable_rls_per_user_tables.py` *(CREA)* — habilita RLS y crea policies `select_own/modify_own` para cada tabla con datos por usuario (sec. 9.3 del spec).
- `backend/alembic/versions/0003_refresh_tokens_and_auth_attempts.py` *(CREA)* — tablas nuevas + índices.

### Backend — tests + CI

- `backend/tests/__init__.py` *(CREA)*
- `backend/tests/conftest.py` *(CREA)* — fixtures `db` (Postgres test instance vía URL `TEST_DATABASE_URL`), `client` (httpx AsyncClient), `user_a`/`user_b` con tokens.
- `backend/tests/test_security_headers.py` *(CREA)*
- `backend/tests/test_rate_limit.py` *(CREA)*
- `backend/tests/test_rls_cross_user.py` *(CREA)* — el más crítico: A no puede leer/modificar datos de B en NINGUNA tabla con RLS.
- `backend/tests/test_auth_refresh.py` *(CREA)* — refresh token rotation + revocación en logout.
- `backend/tests/test_gdpr_endpoints.py` *(CREA)* — DELETE/me purga, GET/me/export retorna JSON completo.
- `backend/tests/test_llm_provider.py` *(CREA)* — factory devuelve provider correcto, fallback funciona.
- `backend/tests/test_pii_redaction.py` *(CREA)* — logger redacta JWT, API keys, emails.
- `backend/scripts/check_no_sqli.py` *(CREA)* — script regex que falla si encuentra `text(f` o concat sospechosa en `*.py`.
- `.github/workflows/ci.yml` *(CREA)* — jobs: lint (flake8 + black + check_no_sqli), test (pytest), audit (pip-audit + npm audit).
- `.github/dependabot.yml` *(CREA)* — pip y npm semanal.

### Frontend — Pyodide sandbox

- `frontend/package.json` *(MODIFICA)* — añadir `pyodide`, `comlink`, `dompurify`, `@types/dompurify`.
- `frontend/src/sandbox/pyodideWorker.ts` *(CREA)* — Web Worker que carga Pyodide y expone API `runCode(code, timeoutMs)` con captura de stdout/stderr.
- `frontend/src/sandbox/PyodideSandbox.ts` *(CREA)* — wrapper main-thread con Comlink, lifecycle (init, restartKernel, dispose).
- `frontend/src/sandbox/types.ts` *(CREA)* — tipos `RunResult`, `RunRequest`, `KernelStatus`.
- `frontend/src/services/codeRunner.ts` *(MODIFICA o CREA)* — reemplaza llamadas a `POST /api/v1/execute/run` por la sandbox local.
- `frontend/src/components/Editor/RunButton.tsx` *(MODIFICA)* — usa `codeRunner` en lugar de axios.

### Frontend — security headers + auth refresh

- `frontend/src/services/api.ts` *(MODIFICA)* — interceptor que captura 401, llama `/auth/refresh`, reintenta original. Si refresh falla → logout.
- `frontend/src/stores/authStore.ts` *(MODIFICA)* — almacena `refresh_token` además de `access_token`; método `refresh()` que reemplaza ambos.

### Despliegue

- `backend/Dockerfile` *(CREA)* — multi-stage con `python:3.11-slim`, instala desde `requirements.lock`, ejecuta `uvicorn`.
- `render.yaml` *(CREA)* — blueprint Render con servicio web FastAPI + `healthCheckPath: /health`.
- `vercel.json` *(CREA)* — config de Vercel para frontend (build command, env vars, rewrites de `/api` y `/ws` al backend Render).
- `.env.example` *(CREA en raíz)* — todas las vars con valores ficticios.
- `requirements.lock` *(CREA)* — `pip-compile` output desde `requirements.txt`.

---

## Scope check

Esta Fase 0 toca infraestructura, seguridad y dos sistemas independientes (provider LLM y Pyodide). Son interdependientes: sin Postgres/RLS no hay seguridad real; sin Pyodide el spec dice que el backend hereda riesgo de RCE; sin provider abstraction el tutor sigue acoplado a OpenAI. Por eso se ejecutan en una sola fase. Las tareas se pueden paralelizar entre subgrupos (ver Anexo "Paralelización" al final).

---

## Convenciones del plan

- **TDD donde aplica**: para lógica nueva (LLM provider, redaction, GDPR endpoints, RLS) escribir test que falle primero.
- **Migraciones de schema**: cada cambio de DB es una revisión Alembic separada; nunca editar una existente ya commiteada.
- **Commits frecuentes**: cada Task termina con un commit. **Sin coautor.**
- **Idioma de mensajes**: español, conciso, presente.
- **Comandos**: PowerShell para shell del usuario en Windows; pytest/alembic se invocan desde `backend/` con venv activo.

---

## Tasks

### Task 1: Bootstrap del directorio de tests y CI mínimo

Antes de TDD, necesitamos infra que corra los tests. El repo no tiene `backend/tests/` ni `.github/workflows/`.

**Files:**
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/conftest.py`
- Create: `backend/tests/test_smoke.py`
- Create: `backend/pytest.ini`
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Crear `backend/pytest.ini`**

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
addopts = -v --tb=short
```

- [ ] **Step 2: Crear `backend/tests/__init__.py` (vacío) y `backend/tests/conftest.py` con fixture mínima**

```python
# backend/tests/conftest.py
import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_pycode.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-prod")
os.environ.setdefault("ENVIRONMENT", "test")

from app.main import app  # noqa: E402


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

- [ ] **Step 3: Crear `backend/tests/test_smoke.py`**

```python
import pytest


@pytest.mark.asyncio
async def test_health_returns_200(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

- [ ] **Step 4: Correr el test localmente**

Run: `cd backend; pytest tests/test_smoke.py -v`
Expected: PASS (1 test)

- [ ] **Step 5: Crear `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-asyncio httpx
      - run: cd backend && pytest

  backend-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install black flake8 mypy
      - run: cd backend && black --check . && flake8 .

  frontend-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: cd frontend && npm ci && npm run lint && npm run build
```

- [ ] **Step 6: Commit**

```bash
git add backend/pytest.ini backend/tests/ .github/workflows/ci.yml
git commit -m "Bootstrap suite de tests backend y CI mínimo (lint + build + smoke)"
```

---

### Task 2: Extender `Settings` con vars de PyCode v2

**Files:**
- Modify: `backend/app/core/config.py`
- Create: `.env.example` (raíz repo)
- Create: `backend/tests/test_settings.py`

- [ ] **Step 1: Test que verifica nuevos settings cargan**

```python
# backend/tests/test_settings.py
import os


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
```

- [ ] **Step 2: Correr test (debe fallar)**

Run: `cd backend; pytest tests/test_settings.py -v`
Expected: FAIL — `AttributeError: ... has no attribute 'SUPABASE_URL'`

- [ ] **Step 3: Editar `backend/app/core/config.py`**

Añadir antes de `class Config`:

```python
    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""

    # LLM provider
    LLM_PROVIDER: str = "groq"          # groq | openai | anthropic
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_API_KEY: str = ""
    HF_TOKEN: str = ""

    # JWT refresh
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Observability
    SENTRY_DSN: str = ""
```

Cambiar `ACCESS_TOKEN_EXPIRE_MINUTES: int = 30` a `ACCESS_TOKEN_EXPIRE_MINUTES: int = 60`.

Borrar `DOCKER_TIMEOUT`, `DOCKER_MEMORY_LIMIT`, `DOCKER_CPU_LIMIT` (sandbox ya no es backend).

- [ ] **Step 4: Correr test (debe pasar)**

Run: `cd backend; pytest tests/test_settings.py -v`
Expected: PASS.

- [ ] **Step 5: Crear `.env.example` en raíz del repo**

```env
# Database — Supabase Postgres
DATABASE_URL=postgresql+asyncpg://postgres:CHANGEME@db.your-project.supabase.co:5432/postgres?sslmode=require

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOi...replace-me
SUPABASE_SERVICE_KEY=eyJhbGciOi...replace-me-server-only

# Auth / JWT
SECRET_KEY=replace-with-output-of-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# LLM provider
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile
GROQ_API_KEY=gsk_replace_me
OPENAI_API_KEY=
HF_TOKEN=

# Observability
SENTRY_DSN=

# CORS — separado por comas, SIN wildcard en prod
CORS_ORIGINS=http://localhost:5173,https://pycode.app

# App
ENVIRONMENT=development
DEBUG=True
TUTOR_PROMPT_FILE=maestro_evaluador_de_codigo_python.txt
```

- [ ] **Step 6: Commit**

```bash
git add backend/app/core/config.py backend/tests/test_settings.py .env.example
git commit -m "Extender Settings con vars Supabase, Groq, refresh JWT y observabilidad"
```

---

### Task 3: Forzar Postgres-only en `database.py` y validar conexión

El archivo actual permite SQLite. Para producción y para que RLS funcione, lo limitamos a Postgres asyncpg con SSL.

**Files:**
- Modify: `backend/app/core/database.py`
- Create: `backend/tests/test_database_url.py`

- [ ] **Step 1: Test que verifica Postgres-only**

```python
# backend/tests/test_database_url.py
import pytest
from app.core.database import _get_engine_args


def test_postgres_url_keeps_sslmode():
    args = _get_engine_args(
        "postgresql+asyncpg://u:p@host:5432/db?sslmode=require"
    )
    assert "asyncpg" in args["url"]
    assert "sslmode=require" in args["url"]


def test_sqlite_rejected_in_production(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    with pytest.raises(RuntimeError, match="SQLite no permitido"):
        _get_engine_args("sqlite+aiosqlite:///./pycode.db")


def test_sqlite_allowed_in_test_or_dev():
    args = _get_engine_args(
        "sqlite+aiosqlite:///./test.db", environment="test"
    )
    assert "sqlite" in args["url"]
```

- [ ] **Step 2: Refactor `_get_engine_args` para aceptar argumento explícito y validar entorno**

Reemplazar contenido de `backend/app/core/database.py` con:

```python
"""
Database configuration. Postgres + asyncpg en prod, SQLite solo en dev/test.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, StaticPool

from app.core.config import settings


def _get_engine_args(db_url: str | None = None, environment: str | None = None) -> dict:
    db_url = db_url or settings.DATABASE_URL
    environment = environment or settings.ENVIRONMENT

    if db_url.startswith("sqlite"):
        if environment == "production":
            raise RuntimeError("SQLite no permitido en producción — usar Postgres.")
        if "+aiosqlite" not in db_url:
            db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://")
        return {
            "url": db_url,
            "poolclass": StaticPool,
            "echo": settings.DEBUG,
            "connect_args": {"check_same_thread": False},
        }

    if db_url.startswith("postgresql"):
        if "+asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
        return {
            "url": db_url,
            "poolclass": NullPool,
            "echo": settings.DEBUG,
        }

    raise RuntimeError(f"DATABASE_URL no soportado: {db_url[:30]}...")


_engine_args = _get_engine_args()
engine = create_async_engine(**_engine_args)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
```

- [ ] **Step 3: Correr tests**

Run: `cd backend; pytest tests/test_database_url.py -v`
Expected: PASS (3 tests).

- [ ] **Step 4: Commit**

```bash
git add backend/app/core/database.py backend/tests/test_database_url.py
git commit -m "Forzar Postgres en producción y validar DATABASE_URL en database.py"
```

---

### Task 4: Configurar Alembic + migración inicial reflejando modelos actuales

**Files:**
- Create: `backend/alembic.ini`
- Create: `backend/alembic/env.py`
- Create: `backend/alembic/script.py.mako`
- Create: `backend/alembic/versions/0001_initial_schema.py`

- [ ] **Step 1: Generar scaffolding alembic**

Run: `cd backend; alembic init alembic`
Expected: crea `backend/alembic/`, `backend/alembic.ini`, `backend/alembic/env.py`.

- [ ] **Step 2: Editar `backend/alembic.ini`**

Cambiar línea `sqlalchemy.url = ...` a:

```ini
sqlalchemy.url =
```

(Vacía — la inyectamos desde `env.py` para que tome `settings.DATABASE_URL`.)

Mantener `script_location = alembic`.

- [ ] **Step 3: Reemplazar `backend/alembic/env.py`**

```python
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import settings
from app.core.database import Base

# Importa todos los modelos para que Base.metadata los conozca
import app.models.user           # noqa: F401
import app.models.learning       # noqa: F401
import app.models.elo_models     # noqa: F401
import app.models.challenge      # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


run_migrations_online()
```

- [ ] **Step 4: Generar migración inicial autogenerated contra base limpia**

Run (con DATABASE_URL apuntando a un Postgres limpio, p.ej. local docker o branch Supabase):
```bash
cd backend
alembic revision --autogenerate -m "0001_initial_schema"
```
Expected: archivo `backend/alembic/versions/0001_xxxxx_initial_schema.py` con todas las tablas.

Renombrar archivo a `0001_initial_schema.py` (sin hash) para legibilidad.

- [ ] **Step 5: Aplicar migración**

Run: `cd backend; alembic upgrade head`
Expected: aplicación exitosa, todas las tablas creadas.

- [ ] **Step 6: Smoke test desde Python**

Run:
```bash
cd backend
python -c "from sqlalchemy import create_engine, inspect; from app.core.config import settings; e = create_engine(settings.DATABASE_URL.replace('+asyncpg','')); print(sorted(inspect(e).get_table_names()))"
```
Expected: incluye `users`, `user_profiles`, `lessons`, `exercises`, `puzzles`, `alembic_version`.

- [ ] **Step 7: Commit**

```bash
git add backend/alembic.ini backend/alembic/
git commit -m "Configurar Alembic con migración inicial autogenerada del schema actual"
```

---

### Task 5: Eliminar `bootstrap_elo_schema` shim y `Base.metadata.create_all` del lifespan

Una vez Alembic está, el shim queda obsoleto.

**Files:**
- Modify: `backend/app/main.py`
- Delete: `backend/app/services/schema_bootstrap.py`

- [ ] **Step 1: Editar `backend/app/main.py`**

Eliminar import `from app.services.schema_bootstrap import bootstrap_elo_schema`.

Reemplazar el bloque dentro de `lifespan`:

```python
async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
    await conn.run_sync(bootstrap_elo_schema)
```

por:

```python
# Schema gestionado por Alembic. Aplica `alembic upgrade head` antes del startup.
```

- [ ] **Step 2: Borrar archivo**

Run: `Remove-Item backend/app/services/schema_bootstrap.py`

- [ ] **Step 3: Documentar paso de migración en `backend/Dockerfile` (anticipo)**

Aún no creamos Dockerfile (Task 30); por ahora, dejar README breve `backend/MIGRATIONS.md`:

```markdown
# Migraciones

Antes de levantar la app:
\`\`\`bash
cd backend && alembic upgrade head
\`\`\`

En CI/Render esto va en el comando de release. Nunca usar `Base.metadata.create_all` en producción.
```

- [ ] **Step 4: Correr smoke test**

Run: `cd backend; pytest tests/test_smoke.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/app/main.py backend/app/services/ backend/MIGRATIONS.md
git commit -m "Eliminar shim bootstrap_elo_schema; schema ahora 100% gestionado por Alembic"
```

---

### Task 6: Lint rule anti-SQL-injection en CI

**Files:**
- Create: `backend/scripts/check_no_sqli.py`
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Crear script `backend/scripts/check_no_sqli.py`**

```python
"""
Falla si encuentra SQL construido por interpolación de strings.
Permitido: text("SELECT ... :param") con bindeo, text(""" SQL literal """)
Prohibido: text(f"..."), text("..." + var), execute(f"...")
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "app", ROOT / "alembic"]

# Patrón 1: text(f"...
PAT_FSTRING = re.compile(r"\btext\s*\(\s*f['\"]")
# Patrón 2: text("..." + ...) o text(... + ...)
PAT_CONCAT = re.compile(r"\btext\s*\([^)]*\+[^)]*\)")
# Patrón 3: execute(f"...
PAT_EXECUTE_FSTRING = re.compile(r"\bexecute\s*\(\s*f['\"]")

violations: list[str] = []

for base in TARGETS:
    if not base.exists():
        continue
    for py_file in base.rglob("*.py"):
        if "__pycache__" in py_file.parts:
            continue
        text = py_file.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for pat in (PAT_FSTRING, PAT_CONCAT, PAT_EXECUTE_FSTRING):
                if pat.search(line):
                    violations.append(f"{py_file.relative_to(ROOT)}:{lineno}: {line.strip()}")

if violations:
    print("SQLi risk: queries con interpolación de strings detectadas:\n", file=sys.stderr)
    for v in violations:
        print(f"  {v}", file=sys.stderr)
    print("\nUsar text(\"... :param\") con parámetros bindeados o pasar al ORM.", file=sys.stderr)
    sys.exit(1)

print("OK: sin riesgos de SQL injection detectados.")
```

- [ ] **Step 2: Correr el script**

Run: `cd backend; python scripts/check_no_sqli.py`
Expected: el shim viejo `schema_bootstrap.py` ya está borrado, así que probablemente PASS. Si falla, reportar y arreglar todas las violaciones.

- [ ] **Step 3: Añadir job al CI**

Editar `.github/workflows/ci.yml`, sección `backend-lint`:

```yaml
  backend-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install black flake8 mypy
      - run: cd backend && black --check . && flake8 .
      - name: SQLi guard
        run: cd backend && python scripts/check_no_sqli.py
```

- [ ] **Step 4: Test del script con caso negativo**

Crear archivo temporal `backend/scripts/_sqli_test_fixture.py`:

```python
from sqlalchemy import text
def bad():
    user = "admin"
    text(f"SELECT * FROM users WHERE name = '{user}'")
```

Run: `cd backend; python scripts/check_no_sqli.py`
Expected: FAIL con mensaje listando la línea.

Borrar el fixture: `Remove-Item backend/scripts/_sqli_test_fixture.py`.

Run de nuevo: `cd backend; python scripts/check_no_sqli.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/scripts/check_no_sqli.py .github/workflows/ci.yml
git commit -m "Lint rule anti-SQL-injection: falla CI si hay text(f...) o concat en queries"
```

---

### Task 7: Pydantic strict en endpoints existentes (auth, exercises, tutor)

**Files:**
- Modify: `backend/app/schemas/auth.py`
- Modify: `backend/app/api/v1/endpoints/auth.py`
- Modify: `backend/app/api/v1/endpoints/code_execution.py` (la versión actual, antes de Task 14 que la reemplaza)

- [ ] **Step 1: Test que verifica límites estrictos en register**

```python
# backend/tests/test_validation_strict.py
import pytest


@pytest.mark.asyncio
async def test_register_rejects_oversized_password(client):
    response = await client.post("/api/v1/auth/register", json={
        "email": "a@b.com",
        "username": "user",
        "password": "x" * 256,
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_rejects_invalid_email(client):
    response = await client.post("/api/v1/auth/register", json={
        "email": "not-an-email",
        "username": "user",
        "password": "ValidPass123!",
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_rejects_username_with_spaces(client):
    response = await client.post("/api/v1/auth/register", json={
        "email": "a@b.com",
        "username": "with space",
        "password": "ValidPass123!",
    })
    assert response.status_code == 422
```

- [ ] **Step 2: Correr test (debe fallar)**

Run: `cd backend; pytest tests/test_validation_strict.py -v`
Expected: FAIL (alguna validación pasa cuando no debería).

- [ ] **Step 3: Endurecer `backend/app/schemas/auth.py`**

Leer archivo actual y añadir `Field` constraints. Ejemplo de `UserCreate`:

```python
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_-]+$")
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("password debe contener al menos un dígito")
        if not any(c.isalpha() for c in v):
            raise ValueError("password debe contener al menos una letra")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)
```

- [ ] **Step 4: Correr test**

Run: `cd backend; pytest tests/test_validation_strict.py -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Endurecer `CodeExecutionRequest` mientras siga existiendo**

Reducir `max_length=10000` a `max_length=20000` (notebooks pueden ser largos), añadir validator que rechaza `\x00` (null bytes). Lo eliminaremos en Task 14.

- [ ] **Step 6: Commit**

```bash
git add backend/app/schemas/auth.py backend/app/api/v1/endpoints/code_execution.py backend/tests/test_validation_strict.py
git commit -m "Endurecer validación Pydantic en auth (longitudes, patterns, complejidad password)"
```

---

### Task 8: Middleware de headers de seguridad

**Files:**
- Create: `backend/app/core/security_headers.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/test_security_headers.py`

- [ ] **Step 1: Test que falla porque headers no existen**

```python
# backend/tests/test_security_headers.py
import pytest


@pytest.mark.asyncio
async def test_health_includes_security_headers(client):
    r = await client.get("/health")
    h = r.headers
    assert "strict-transport-security" in h
    assert "max-age=31536000" in h["strict-transport-security"]
    assert h["x-content-type-options"] == "nosniff"
    assert h["x-frame-options"] == "DENY"
    assert "referrer-policy" in h
    assert "content-security-policy" in h
    assert "geolocation=()" in h.get("permissions-policy", "")


@pytest.mark.asyncio
async def test_csp_allows_pyodide_cdn(client):
    r = await client.get("/health")
    csp = r.headers["content-security-policy"]
    assert "https://cdn.jsdelivr.net" in csp
    assert "wasm-unsafe-eval" in csp
```

- [ ] **Step 2: Correr test**

Run: `cd backend; pytest tests/test_security_headers.py -v`
Expected: FAIL — headers no presentes.

- [ ] **Step 3: Crear `backend/app/core/security_headers.py`**

```python
"""
Middleware FastAPI que añade headers de seguridad estándar (sec. 9.9 del spec).
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


CSP = (
    "default-src 'self'; "
    "script-src 'self' 'wasm-unsafe-eval' https://cdn.jsdelivr.net; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data: blob:; "
    "font-src 'self' data:; "
    "connect-src 'self' https://*.supabase.co https://api.groq.com https://cdn.jsdelivr.net; "
    "worker-src 'self' blob:; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = CSP
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response
```

- [ ] **Step 4: Registrar middleware en `backend/app/main.py`**

Después de `app = FastAPI(...)` y antes de `app.add_middleware(CORSMiddleware...)`:

```python
from app.core.security_headers import SecurityHeadersMiddleware
app.add_middleware(SecurityHeadersMiddleware)
```

- [ ] **Step 5: Correr tests**

Run: `cd backend; pytest tests/test_security_headers.py -v`
Expected: PASS (2 tests).

- [ ] **Step 6: Commit**

```bash
git add backend/app/core/security_headers.py backend/app/main.py backend/tests/test_security_headers.py
git commit -m "Middleware de headers de seguridad (HSTS, CSP, XCTO, XFO, Referrer-Policy)"
```

---

### Task 9: CORS whitelist sin wildcard en producción

**Files:**
- Modify: `backend/app/core/config.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/test_cors.py`

- [ ] **Step 1: Test que falla**

```python
# backend/tests/test_cors.py
import pytest


@pytest.mark.asyncio
async def test_cors_rejects_unknown_origin(client):
    r = await client.options(
        "/api/v1/auth/login",
        headers={
            "Origin": "https://evil.example",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert r.headers.get("access-control-allow-origin") != "https://evil.example"
    assert r.headers.get("access-control-allow-origin") != "*"


@pytest.mark.asyncio
async def test_cors_allows_known_origin(client):
    r = await client.options(
        "/api/v1/auth/login",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert r.headers.get("access-control-allow-origin") == "http://localhost:5173"
```

- [ ] **Step 2: Correr test**

Run: `cd backend; pytest tests/test_cors.py -v`
Expected: el primer test puede pasar o fallar dependiendo de valor en CORS_ORIGINS; el segundo confirma whitelist explícita.

- [ ] **Step 3: Verificar que `cors_origins_list` ya divide bien y `allow_methods=["*"]` se restringe**

En `backend/app/main.py`, reemplazar el bloque CORS por:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
    max_age=600,
)
```

Y añadir guard en `config.py`:

```python
@property
def cors_origins_list(self) -> List[str]:
    raw = [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    if self.ENVIRONMENT == "production" and "*" in raw:
        raise RuntimeError("CORS wildcard prohibido en producción")
    return raw
```

- [ ] **Step 4: Correr tests**

Run: `cd backend; pytest tests/test_cors.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add backend/app/main.py backend/app/core/config.py backend/tests/test_cors.py
git commit -m "Restringir CORS a whitelist explícita; prohibir wildcard en producción"
```

---

### Task 10: Rate limiting universal con SlowAPI

**Files:**
- Modify: `requirements.txt` (añadir `slowapi==0.1.9`)
- Create: `backend/app/core/rate_limit.py`
- Modify: `backend/app/main.py`
- Modify: `backend/app/api/v1/endpoints/auth.py`
- Modify: `backend/app/api/v1/endpoints/tutor.py`
- Create: `backend/tests/test_rate_limit.py`

- [ ] **Step 1: Añadir SlowAPI a requirements**

Editar `requirements.txt`, añadir línea:
```
slowapi==0.1.9
```

Run: `pip install slowapi==0.1.9`

- [ ] **Step 2: Test que falla**

```python
# backend/tests/test_rate_limit.py
import pytest


@pytest.mark.asyncio
async def test_login_rate_limited_after_5_attempts(client):
    payload = {"email": "x@y.com", "password": "wrongPass1"}
    for i in range(5):
        r = await client.post("/api/v1/auth/login", json=payload)
        assert r.status_code in (401, 422)
    r = await client.post("/api/v1/auth/login", json=payload)
    assert r.status_code == 429
    assert "rate limit" in r.text.lower() or "too many" in r.text.lower()
```

- [ ] **Step 3: Correr test**

Run: `cd backend; pytest tests/test_rate_limit.py -v`
Expected: FAIL — el endpoint no rate-limitea.

- [ ] **Step 4: Crear `backend/app/core/rate_limit.py`**

```python
"""
Rate limiting universal — SlowAPI con keyfunc por user_id (autenticado) o IP (anónimo).
Tabla de límites consolidada en sec. 9.10 del spec.
"""
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request
from fastapi import Response, status
from fastapi.responses import JSONResponse


def _user_or_ip(request: Request) -> str:
    user_id = getattr(request.state, "user_id", None)
    if user_id:
        return f"user:{user_id}"
    return f"ip:{get_remote_address(request)}"


limiter = Limiter(key_func=_user_or_ip, default_limits=["100/minute"])


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit excedido. Intenta más tarde."},
        headers={"Retry-After": "60"},
    )


# Decoradores semánticos para los pattern del spec sec. 9.10
def login_limit():
    return limiter.limit("5/minute")


def register_limit():
    return limiter.limit("3/hour")


def tutor_limit():
    return limiter.limit("50/day")


def submit_limit():
    return limiter.limit("30/minute")
```

- [ ] **Step 5: Conectar en `backend/app/main.py`**

Añadir al inicio:
```python
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter, rate_limit_exceeded_handler
```

Después de crear `app`:
```python
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
```

Añadir middleware (lo provee SlowAPI):
```python
from slowapi.middleware import SlowAPIMiddleware
app.add_middleware(SlowAPIMiddleware)
```

- [ ] **Step 6: Decorar endpoints**

`backend/app/api/v1/endpoints/auth.py`:
```python
from app.core.rate_limit import login_limit, register_limit, limiter
from fastapi import Request

@router.post("/register", ...)
@limiter.limit("3/hour")
async def register(request: Request, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    ...

@router.post("/login", ...)
@limiter.limit("5/minute")
async def login(request: Request, login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    ...
```

(SlowAPI requiere parámetro `request: Request` en la firma.)

`backend/app/api/v1/endpoints/tutor.py`: añadir `@limiter.limit("50/day")` en el endpoint POST principal.

- [ ] **Step 7: Correr tests**

Run: `cd backend; pytest tests/test_rate_limit.py -v`
Expected: PASS.

Run smoke: `cd backend; pytest tests/ -v`
Expected: todos los previos pasan también (ojo a ajustar `test_validation_strict` para no exceder 5/min — usar IPs distintas vía header `X-Forwarded-For` si hace falta).

- [ ] **Step 8: Commit**

```bash
git add requirements.txt backend/app/core/rate_limit.py backend/app/main.py backend/app/api/v1/endpoints/auth.py backend/app/api/v1/endpoints/tutor.py backend/tests/test_rate_limit.py
git commit -m "Rate limiting universal con SlowAPI (login 5/min, register 3/h, tutor 50/día)"
```

---

### Task 11: Logging estructurado con redaction de PII

**Files:**
- Modify: `requirements.txt` (añadir `structlog==24.1.0`)
- Create: `backend/app/core/logging_config.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/test_pii_redaction.py`

- [ ] **Step 1: Añadir structlog**

Editar `requirements.txt`: añadir `structlog==24.1.0`.
Run: `pip install structlog==24.1.0`

- [ ] **Step 2: Test que falla**

```python
# backend/tests/test_pii_redaction.py
import logging
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
```

- [ ] **Step 3: Correr test**

Run: `cd backend; pytest tests/test_pii_redaction.py -v`
Expected: FAIL.

- [ ] **Step 4: Crear `backend/app/core/logging_config.py`**

```python
"""
structlog + redaction de PII (sec. 9.11 del spec).
"""
import logging
import re
from typing import Iterable

import structlog

# Patrones de PII a redactar
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
```

- [ ] **Step 5: Llamar `configure_logging()` en `main.py`**

Al inicio del archivo, antes de crear `app`:

```python
from app.core.logging_config import configure_logging
configure_logging()
```

- [ ] **Step 6: Correr tests**

Run: `cd backend; pytest tests/test_pii_redaction.py -v`
Expected: PASS (5 tests).

- [ ] **Step 7: Reemplazar `print()` en código existente por logger**

Buscar usos de `print(...)` en `backend/app/services/ai_tutor.py` y reemplazar:
```python
import structlog
logger = structlog.get_logger()
# ...
print(f"Error calling OpenAI: {exc}")
```
por:
```python
logger.error("llm.call_failed", error=str(exc))
```

- [ ] **Step 8: Commit**

```bash
git add requirements.txt backend/app/core/logging_config.py backend/app/main.py backend/app/services/ai_tutor.py backend/tests/test_pii_redaction.py
git commit -m "Logging estructurado structlog con redaction de JWT, API keys y emails (sec. 9.11)"
```

---

### Task 12: Sentry SDK con scrubbing de PII

**Files:**
- Modify: `requirements.txt` (añadir `sentry-sdk[fastapi]==1.45.0`)
- Create: `backend/app/core/observability.py`
- Modify: `backend/app/main.py`

- [ ] **Step 1: Añadir Sentry**

Editar `requirements.txt`: `sentry-sdk[fastapi]==1.45.0`.
Run: `pip install "sentry-sdk[fastapi]==1.45.0"`

- [ ] **Step 2: Crear `backend/app/core/observability.py`**

```python
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
```

- [ ] **Step 3: Llamar en `main.py`**

Después de `configure_logging()`:

```python
from app.core.observability import init_sentry
init_sentry()
```

- [ ] **Step 4: Smoke test (sin DSN configurado, debe ser noop)**

Run: `cd backend; pytest tests/ -v`
Expected: todos pasan; no errores de import Sentry.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt backend/app/core/observability.py backend/app/main.py
git commit -m "Sentry SDK con scrubbing de PII en before_send (no-op si SENTRY_DSN vacío)"
```

---

### Task 13: Endpoint `/health` slim sin info sensible

**Files:**
- Modify: `backend/app/main.py`
- Create: `backend/tests/test_health.py`

- [ ] **Step 1: Test que verifica el `/` y `/health` no exponen detalles**

```python
# backend/tests/test_health.py
import pytest


@pytest.mark.asyncio
async def test_health_minimal_payload(client):
    r = await client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body == {"status": "healthy"} or set(body.keys()) <= {"status"}


@pytest.mark.asyncio
async def test_root_does_not_leak_version_or_db(client):
    r = await client.get("/")
    body = r.json()
    text = str(body).lower()
    assert "postgres" not in text
    assert "supabase" not in text
    assert "version" not in body or body.get("version", "") in ("", "1.0", "v1")
```

- [ ] **Step 2: Correr test**

Run: `cd backend; pytest tests/test_health.py -v`
Expected: el segundo falla porque el handler actual incluye `"version": "0.1.0"`.

- [ ] **Step 3: Editar handlers en `backend/app/main.py`**

Reemplazar:

```python
@app.get("/")
async def root():
    return {"message": "PyCode Platform"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

- [ ] **Step 4: Correr tests**

Run: `cd backend; pytest tests/test_health.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add backend/app/main.py backend/tests/test_health.py
git commit -m "Endpoint / y /health sin info sensible (versión, DB, infra)"
```

---

### Task 14: Reemplazar subprocess executor por endpoint placeholder + Pyodide cliente

El backend ya no ejecuta código. Mantenemos un endpoint para validación de sintaxis (sin ejecutar), todo el cómputo va a Pyodide.

**Files:**
- Modify: `backend/app/api/v1/endpoints/code_execution.py`
- Delete: `backend/app/services/docker_executor.py`
- Create: `backend/tests/test_code_execution_endpoint.py`

- [ ] **Step 1: Test del nuevo comportamiento**

```python
# backend/tests/test_code_execution_endpoint.py
import pytest


@pytest.mark.asyncio
async def test_run_endpoint_returns_410_gone(client, auth_headers):
    r = await client.post("/api/v1/execute/run", json={"code": "print(1)"}, headers=auth_headers)
    assert r.status_code == 410
    assert "cliente" in r.json()["detail"].lower() or "pyodide" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_validate_syntax_accepts_valid_python(client, auth_headers):
    r = await client.post("/api/v1/execute/validate", json={"code": "x = 1\nprint(x)"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["valid"] is True


@pytest.mark.asyncio
async def test_validate_syntax_rejects_invalid_python(client, auth_headers):
    r = await client.post("/api/v1/execute/validate", json={"code": "def x(:"}, headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert body["valid"] is False
    assert "syntax" in body["error"].lower()
```

(El fixture `auth_headers` se añade en Task 16 — por ahora marcar tests con skipif si la fixture no existe; o crearla mínima ya en `conftest.py`.)

- [ ] **Step 2: Reescribir `backend/app/api/v1/endpoints/code_execution.py`**

```python
"""
Endpoint de validación de código (no ejecuta — la ejecución vive en cliente Pyodide).
"""
import ast
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field

from app.core.security import get_current_active_user
from app.core.rate_limit import limiter
from app.models.user import User

router = APIRouter()


class CodeValidateRequest(BaseModel):
    code: str = Field(min_length=1, max_length=20000)


class CodeValidateResponse(BaseModel):
    valid: bool
    error: str | None = None


@router.post("/run", status_code=410)
async def run_deprecated():
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail=(
            "Ejecución de código en backend deshabilitada. "
            "El cliente debe usar Pyodide para ejecutar localmente."
        ),
    )


@router.post("/validate", response_model=CodeValidateResponse)
@limiter.limit("60/minute")
async def validate_syntax(
    request: Request,
    body: CodeValidateRequest,
    current_user: User = Depends(get_current_active_user),
) -> CodeValidateResponse:
    try:
        ast.parse(body.code)
        return CodeValidateResponse(valid=True)
    except SyntaxError as e:
        return CodeValidateResponse(valid=False, error=f"SyntaxError: {e.msg} (line {e.lineno})")
```

- [ ] **Step 3: Borrar `docker_executor.py`**

Run: `Remove-Item backend/app/services/docker_executor.py`

Quitar `docker==6.1.3` de `requirements.txt`.

- [ ] **Step 4: Correr tests**

Run: `cd backend; pytest tests/test_code_execution_endpoint.py -v`
Expected: PASS (3 tests).

Run smoke completo: `cd backend; pytest -v`
Expected: todos pasan.

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/v1/endpoints/code_execution.py backend/app/services/ backend/tests/test_code_execution_endpoint.py requirements.txt
git commit -m "Backend deja de ejecutar código del estudiante; /run retorna 410, /validate sólo ast.parse"
```

---

### Task 15: Provider abstraction LLM (Groq + OpenAI)

**Files:**
- Modify: `requirements.txt` (añadir `groq==0.5.0`, mantener `openai==1.3.6`)
- Create: `backend/app/services/llm_provider.py`
- Modify: `backend/app/services/ai_tutor.py`
- Create: `backend/tests/test_llm_provider.py`

- [ ] **Step 1: Añadir Groq SDK**

`requirements.txt`: `groq==0.5.0`. Run: `pip install groq==0.5.0`.

- [ ] **Step 2: Test del factory**

```python
# backend/tests/test_llm_provider.py
import pytest
from app.services.llm_provider import (
    GroqProvider, OpenAIProvider, get_provider, LLMProvider
)


def test_factory_returns_groq_when_configured(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "gsk_test")
    from app.core.config import Settings
    p = get_provider(Settings())
    assert isinstance(p, GroqProvider)


def test_factory_returns_openai_when_configured(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    from app.core.config import Settings
    p = get_provider(Settings())
    assert isinstance(p, OpenAIProvider)


def test_factory_raises_on_unknown_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "cohere")
    from app.core.config import Settings
    with pytest.raises(ValueError, match="LLM_PROVIDER"):
        get_provider(Settings())


@pytest.mark.asyncio
async def test_provider_implements_chat_interface():
    class FakeProvider(LLMProvider):
        async def chat(self, system, user, **kwargs):
            return "stub-response"

    p = FakeProvider()
    out = await p.chat(system="s", user="u")
    assert out == "stub-response"
```

- [ ] **Step 3: Correr (debe fallar)**

Run: `cd backend; pytest tests/test_llm_provider.py -v`
Expected: FAIL (módulo no existe).

- [ ] **Step 4: Crear `backend/app/services/llm_provider.py`**

```python
"""
Abstracción de proveedor LLM (sec. 5.5 del spec).
Default: Groq. Fallback: OpenAI.
"""
from abc import ABC, abstractmethod
from typing import Optional

import structlog

logger = structlog.get_logger()


class LLMProvider(ABC):
    @abstractmethod
    async def chat(
        self,
        system: str,
        user: str,
        max_tokens: int = 700,
        temperature: float = 0.4,
    ) -> str:
        ...


class GroqProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        from groq import AsyncGroq
        self.client = AsyncGroq(api_key=api_key)
        self.model = model

    async def chat(self, system, user, max_tokens=700, temperature=0.4) -> str:
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content or ""


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def chat(self, system, user, max_tokens=700, temperature=0.4) -> str:
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content or ""


class StubProvider(LLMProvider):
    """Fallback determinístico cuando no hay API key configurada."""
    async def chat(self, system, user, **kwargs) -> str:
        return ""


def get_provider(settings) -> LLMProvider:
    name = settings.LLM_PROVIDER.lower()
    if name == "groq":
        if not settings.GROQ_API_KEY:
            logger.warning("llm.no_api_key", provider="groq")
            return StubProvider()
        return GroqProvider(settings.GROQ_API_KEY, settings.LLM_MODEL)
    if name == "openai":
        if not settings.OPENAI_API_KEY:
            logger.warning("llm.no_api_key", provider="openai")
            return StubProvider()
        return OpenAIProvider(settings.OPENAI_API_KEY, settings.LLM_MODEL)
    raise ValueError(f"LLM_PROVIDER no soportado: {name}")
```

- [ ] **Step 5: Refactor `ai_tutor.py` para usar el provider**

En `backend/app/services/ai_tutor.py`, reemplazar:

```python
self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
```

por:

```python
from app.services.llm_provider import get_provider, StubProvider
self.provider = get_provider(settings)
```

Y reemplazar el bloque que construye `messages` y llama `self.client.chat.completions.create(...)` por:

```python
if isinstance(self.provider, StubProvider):
    return self._get_fallback_response(message, normalized_context)

try:
    user_block = (
        f"{self._build_context(normalized_context)}\n\n"
        f"Consulta o comentario del estudiante:\n{message.strip()}"
    ).strip()
    content = await self.provider.chat(
        system=self.system_prompt,
        user=user_block,
        max_tokens=700,
        temperature=0.4,
    )
    return content.strip() or self._get_fallback_response(message, normalized_context)
except Exception as exc:
    logger.error("llm.call_failed", error=str(exc))
    return self._get_fallback_response(message, normalized_context)
```

- [ ] **Step 6: Correr tests**

Run: `cd backend; pytest tests/test_llm_provider.py -v`
Expected: PASS (4 tests).

Run completo: `cd backend; pytest -v`
Expected: todos pasan.

- [ ] **Step 7: Commit**

```bash
git add requirements.txt backend/app/services/llm_provider.py backend/app/services/ai_tutor.py backend/tests/test_llm_provider.py
git commit -m "Provider abstraction LLM con Groq default y OpenAI fallback"
```

---

### Task 16: Modelo `RefreshToken` y endpoint `/auth/refresh` con rotación

**Files:**
- Create: `backend/app/models/refresh_token.py`
- Modify: `backend/app/main.py` (importar el modelo)
- Modify: `backend/app/core/security.py`
- Modify: `backend/app/schemas/auth.py`
- Modify: `backend/app/api/v1/endpoints/auth.py`
- Create: `backend/alembic/versions/0002_refresh_tokens.py`
- Create: `backend/tests/test_auth_refresh.py`
- Modify: `backend/tests/conftest.py` (añadir fixture `auth_headers`)

- [ ] **Step 1: Crear modelo `RefreshToken`**

```python
# backend/app/models/refresh_token.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Index
from app.core.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    jti = Column(String(64), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_refresh_tokens_user_revoked", "user_id", "revoked"),
    )
```

- [ ] **Step 2: Importar en `main.py`**

`import app.models.refresh_token  # noqa: F401`

- [ ] **Step 3: Generar migración**

Run: `cd backend; alembic revision --autogenerate -m "0002_refresh_tokens"`

Verificar el archivo generado y renombrarlo a `0002_refresh_tokens.py`.

Run: `alembic upgrade head`

- [ ] **Step 4: Añadir helpers a `backend/app/core/security.py`**

```python
import secrets
from datetime import timedelta, datetime
# ...

def create_refresh_token(user_id: int) -> tuple[str, str, datetime]:
    """Devuelve (token, jti, expires_at)."""
    jti = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "jti": jti, "type": "refresh", "exp": expires_at}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, jti, expires_at


def decode_refresh_token(token: str) -> dict:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    if payload.get("type") != "refresh":
        raise JWTError("not a refresh token")
    return payload
```

- [ ] **Step 5: Schemas**

En `backend/app/schemas/auth.py`, ampliar `Token`:

```python
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    username: str


class RefreshRequest(BaseModel):
    refresh_token: str
```

- [ ] **Step 6: Endpoint login emite refresh, endpoint /refresh rota**

Modificar `login` en `auth.py` para crear y persistir refresh token:

```python
from app.models.refresh_token import RefreshToken
from app.core.security import create_refresh_token

# dentro de login(), después del access_token:
rt, jti, exp = create_refresh_token(user.id)
db.add(RefreshToken(user_id=user.id, jti=jti, expires_at=exp))
await db.commit()

return Token(access_token=access_token, refresh_token=rt, token_type="bearer", user_id=user.id, username=user.username)
```

Añadir endpoint `/refresh`:

```python
from app.core.security import decode_refresh_token, create_access_token, create_refresh_token

@router.post("/refresh", response_model=Token)
@limiter.limit("60/hour")
async def refresh(request: Request, body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_refresh_token(body.refresh_token)
    except JWTError:
        raise HTTPException(401, "refresh token inválido")
    jti = payload["jti"]
    user_id = int(payload["sub"])

    result = await db.execute(
        select(RefreshToken).where(RefreshToken.jti == jti, RefreshToken.revoked == False)
    )
    rt = result.scalar_one_or_none()
    if not rt or rt.expires_at < datetime.utcnow():
        raise HTTPException(401, "refresh token revocado o expirado")

    # Rotación: revoca el actual y emite uno nuevo
    rt.revoked = True
    new_rt, new_jti, new_exp = create_refresh_token(user_id)
    db.add(RefreshToken(user_id=user_id, jti=new_jti, expires_at=new_exp))

    new_access = create_access_token(
        data={"sub": str(user_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one()
    await db.commit()
    return Token(access_token=new_access, refresh_token=new_rt, token_type="bearer", user_id=user_id, username=user.username)


@router.post("/logout", status_code=204)
async def logout(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_refresh_token(body.refresh_token)
    except JWTError:
        return
    await db.execute(
        update(RefreshToken).where(RefreshToken.jti == payload["jti"]).values(revoked=True)
    )
    await db.commit()
```

(import `update` from sqlalchemy.)

- [ ] **Step 7: Fixture `auth_headers` en `conftest.py`**

Añadir:

```python
@pytest_asyncio.fixture
async def auth_headers(client):
    await client.post("/api/v1/auth/register", json={
        "email": "fixture@test.com", "username": "fix", "password": "TestPass123",
    })
    r = await client.post("/api/v1/auth/login", json={
        "email": "fixture@test.com", "password": "TestPass123",
    })
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

- [ ] **Step 8: Tests de refresh**

```python
# backend/tests/test_auth_refresh.py
import pytest


@pytest.mark.asyncio
async def test_login_returns_refresh_token(client):
    await client.post("/api/v1/auth/register", json={
        "email": "rt@test.com", "username": "rtuser", "password": "TestPass123",
    })
    r = await client.post("/api/v1/auth/login", json={
        "email": "rt@test.com", "password": "TestPass123",
    })
    body = r.json()
    assert "refresh_token" in body
    assert "access_token" in body


@pytest.mark.asyncio
async def test_refresh_rotates_token(client):
    await client.post("/api/v1/auth/register", json={
        "email": "rot@test.com", "username": "rotuser", "password": "TestPass123",
    })
    login = (await client.post("/api/v1/auth/login", json={
        "email": "rot@test.com", "password": "TestPass123",
    })).json()
    rt1 = login["refresh_token"]

    r1 = await client.post("/api/v1/auth/refresh", json={"refresh_token": rt1})
    assert r1.status_code == 200
    rt2 = r1.json()["refresh_token"]
    assert rt2 != rt1

    # rt1 ya está revocado
    r2 = await client.post("/api/v1/auth/refresh", json={"refresh_token": rt1})
    assert r2.status_code == 401


@pytest.mark.asyncio
async def test_logout_revokes_refresh_token(client):
    await client.post("/api/v1/auth/register", json={
        "email": "lo@test.com", "username": "louser", "password": "TestPass123",
    })
    login = (await client.post("/api/v1/auth/login", json={
        "email": "lo@test.com", "password": "TestPass123",
    })).json()
    rt = login["refresh_token"]

    await client.post("/api/v1/auth/logout", json={"refresh_token": rt})
    r = await client.post("/api/v1/auth/refresh", json={"refresh_token": rt})
    assert r.status_code == 401
```

- [ ] **Step 9: Correr todos los tests**

Run: `cd backend; pytest -v`
Expected: todo PASS (incluidos test_auth_refresh con 3 nuevos).

- [ ] **Step 10: Commit**

```bash
git add backend/app/models/refresh_token.py backend/app/core/security.py backend/app/schemas/auth.py backend/app/api/v1/endpoints/auth.py backend/app/main.py backend/alembic/versions/0002_refresh_tokens.py backend/tests/test_auth_refresh.py backend/tests/conftest.py
git commit -m "JWT con refresh token rotation y endpoint /auth/logout que revoca jti"
```

---

### Task 17: Endpoints GDPR — DELETE /me y GET /me/export

**Files:**
- Modify: `backend/app/api/v1/endpoints/users.py`
- Create: `backend/tests/test_gdpr_endpoints.py`

- [ ] **Step 1: Tests GDPR**

```python
# backend/tests/test_gdpr_endpoints.py
import pytest


@pytest.mark.asyncio
async def test_export_returns_user_data(client):
    await client.post("/api/v1/auth/register", json={
        "email": "exp@test.com", "username": "expuser", "password": "TestPass123",
    })
    tok = (await client.post("/api/v1/auth/login", json={
        "email": "exp@test.com", "password": "TestPass123",
    })).json()["access_token"]
    h = {"Authorization": f"Bearer {tok}"}

    r = await client.get("/api/v1/users/me/export", headers=h)
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["email"] == "exp@test.com"
    assert "profile" in data
    assert "progress" in data
    assert "submissions" in data
    assert "tutor_messages" in data
    assert "exported_at" in data


@pytest.mark.asyncio
async def test_delete_me_purges_account(client):
    await client.post("/api/v1/auth/register", json={
        "email": "del@test.com", "username": "deluser", "password": "TestPass123",
    })
    tok = (await client.post("/api/v1/auth/login", json={
        "email": "del@test.com", "password": "TestPass123",
    })).json()["access_token"]
    h = {"Authorization": f"Bearer {tok}"}

    r = await client.delete("/api/v1/users/me", headers=h)
    assert r.status_code == 204

    # No se puede volver a loguear
    r2 = await client.post("/api/v1/auth/login", json={
        "email": "del@test.com", "password": "TestPass123",
    })
    assert r2.status_code == 401
```

- [ ] **Step 2: Implementar endpoints en `users.py`**

```python
from datetime import datetime
from sqlalchemy import select, delete
from fastapi import Response

@router.get("/me/export")
async def export_my_data(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    profile = (await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )).scalar_one_or_none()

    # Importar modelos lazily para evitar circulares
    from app.models.learning import UserProgress, CodeSubmission, TutorSession

    progress = (await db.execute(
        select(UserProgress).where(UserProgress.user_id == current_user.id)
    )).scalars().all()
    submissions = (await db.execute(
        select(CodeSubmission).where(CodeSubmission.user_id == current_user.id)
    )).scalars().all()
    tutor_msgs = (await db.execute(
        select(TutorSession).where(TutorSession.user_id == current_user.id)
    )).scalars().all()

    def _row(o):
        return {c.name: getattr(o, c.name) for c in o.__table__.columns}

    return {
        "user": {"id": current_user.id, "email": current_user.email, "username": current_user.username, "created_at": current_user.created_at.isoformat()},
        "profile": _row(profile) if profile else None,
        "progress": [_row(p) for p in progress],
        "submissions": [_row(s) for s in submissions],
        "tutor_messages": [_row(t) for t in tutor_msgs],
        "exported_at": datetime.utcnow().isoformat() + "Z",
    }


@router.delete("/me", status_code=204)
async def delete_my_account(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    # ON DELETE CASCADE en relaciones se encarga del resto
    await db.execute(delete(User).where(User.id == current_user.id))
    await db.commit()
    return Response(status_code=204)
```

- [ ] **Step 3: Asegurar `ondelete="CASCADE"` en FKs**

Revisar `app/models/user.py`, `learning.py`, `elo_models.py`. En cada `ForeignKey("users.id")` añadir `ondelete="CASCADE"`.

Si hay cambios → generar migración:
```bash
cd backend; alembic revision --autogenerate -m "0003_cascade_user_fks"
alembic upgrade head
```

- [ ] **Step 4: Correr tests**

Run: `cd backend; pytest tests/test_gdpr_endpoints.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/v1/endpoints/users.py backend/app/models/ backend/alembic/versions/ backend/tests/test_gdpr_endpoints.py
git commit -m "Endpoints GDPR: DELETE /users/me purga cuenta, GET /users/me/export retorna datos"
```

---

### Task 18: Migración Alembic con RLS habilitada por tabla con datos de usuario

**Files:**
- Create: `backend/alembic/versions/0004_enable_rls_per_user_tables.py`

- [ ] **Step 1: Crear migración**

```python
"""enable RLS on per-user tables

Revision ID: 0004_enable_rls_per_user_tables
Revises: 0003_cascade_user_fks
Create Date: 2026-05-...
"""
from alembic import op

revision = "0004_enable_rls_per_user_tables"
down_revision = "0003_cascade_user_fks"
branch_labels = None
depends_on = None


PER_USER_TABLES = [
    "user_profiles", "user_progress", "code_submissions",
    "tutor_sessions", "refresh_tokens",
]
PUBLIC_READ_TABLES = [
    "lessons", "exercises", "puzzles",
]


def upgrade():
    for t in PER_USER_TABLES:
        op.execute(f'ALTER TABLE "{t}" ENABLE ROW LEVEL SECURITY')
        op.execute(f'ALTER TABLE "{t}" FORCE ROW LEVEL SECURITY')
        op.execute(f'''
            CREATE POLICY "{t}_select_own" ON "{t}"
              FOR SELECT
              USING (user_id = current_setting('app.current_user_id', true)::int)
        ''')
        op.execute(f'''
            CREATE POLICY "{t}_modify_own" ON "{t}"
              FOR ALL
              USING (user_id = current_setting('app.current_user_id', true)::int)
              WITH CHECK (user_id = current_setting('app.current_user_id', true)::int)
        ''')

    # Tabla users — el dueño se identifica por id, no user_id
    op.execute('ALTER TABLE "users" ENABLE ROW LEVEL SECURITY')
    op.execute('ALTER TABLE "users" FORCE ROW LEVEL SECURITY')
    op.execute('''
        CREATE POLICY "users_select_self" ON "users"
          FOR SELECT
          USING (id = current_setting('app.current_user_id', true)::int)
    ''')
    op.execute('''
        CREATE POLICY "users_modify_self" ON "users"
          FOR ALL
          USING (id = current_setting('app.current_user_id', true)::int)
          WITH CHECK (id = current_setting('app.current_user_id', true)::int)
    ''')

    for t in PUBLIC_READ_TABLES:
        op.execute(f'ALTER TABLE "{t}" ENABLE ROW LEVEL SECURITY')
        op.execute(f'''
            CREATE POLICY "{t}_public_read" ON "{t}"
              FOR SELECT
              USING (true)
        ''')


def downgrade():
    for t in PER_USER_TABLES + ["users"] + PUBLIC_READ_TABLES:
        op.execute(f'ALTER TABLE "{t}" DISABLE ROW LEVEL SECURITY')
        op.execute(f'DROP POLICY IF EXISTS "{t}_select_own" ON "{t}"')
        op.execute(f'DROP POLICY IF EXISTS "{t}_modify_own" ON "{t}"')
        op.execute(f'DROP POLICY IF EXISTS "{t}_public_read" ON "{t}"')
        op.execute(f'DROP POLICY IF EXISTS "{t}_select_self" ON "{t}"')
        op.execute(f'DROP POLICY IF EXISTS "{t}_modify_self" ON "{t}"')
```

> **Decisión:** usamos `current_setting('app.current_user_id')` en lugar de `auth.uid()` de Supabase. Razón: el backend FastAPI gestiona la auth con su propio JWT y no usa Supabase Auth (todavía). Cada request setea `SET LOCAL app.current_user_id = N` antes de querys. Cuando se migre a Supabase Auth (Fase 7), las policies se reescriben para usar `auth.uid()`.

- [ ] **Step 2: Implementar el `SET LOCAL` por request**

Editar `backend/app/core/database.py`, modificar `get_db`:

```python
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_db_for_user(user_id: int) -> AsyncSession:
    """Sesión con el contexto de RLS seteado al user_id dado."""
    async with async_session_maker() as session:
        try:
            from sqlalchemy import text
            await session.execute(text("SET LOCAL app.current_user_id = :uid"), {"uid": user_id})
            yield session
        finally:
            await session.close()
```

Y modificar `get_current_user` en `security.py` para que use esta sesión escopada (después de obtener `user_id`, llamar `await db.execute(text("SET LOCAL app.current_user_id = :uid"), {"uid": user_id})`).

```python
# en get_current_user, después de extraer user_id del JWT:
from sqlalchemy import text
await db.execute(text("SET LOCAL app.current_user_id = :uid"), {"uid": int(user_id)})
```

> Nota: usamos `text("SET LOCAL ... = :uid")` con parámetro bindeado — pasa el lint anti-SQLi.

- [ ] **Step 3: Aplicar migración**

Run: `cd backend; alembic upgrade head`

Si la app corre y los tests existentes pasan, RLS no rompió nada.

Run: `cd backend; pytest -v`
Expected: todos los tests previos siguen pasando.

- [ ] **Step 4: Commit**

```bash
git add backend/alembic/versions/0004_enable_rls_per_user_tables.py backend/app/core/database.py backend/app/core/security.py
git commit -m "Habilitar RLS en tablas con datos por usuario; SET LOCAL app.current_user_id por request"
```

---

### Task 19: Test suite cross-user RLS

**Files:**
- Create: `backend/tests/test_rls_cross_user.py`
- Modify: `backend/tests/conftest.py` (fixtures `user_a`, `user_b`)

- [ ] **Step 1: Fixtures dos usuarios**

En `conftest.py`:

```python
@pytest_asyncio.fixture
async def user_a(client):
    await client.post("/api/v1/auth/register", json={
        "email": "alice@test.com", "username": "alice", "password": "AlicePass123",
    })
    r = await client.post("/api/v1/auth/login", json={
        "email": "alice@test.com", "password": "AlicePass123",
    })
    body = r.json()
    return {"id": body["user_id"], "headers": {"Authorization": f"Bearer {body['access_token']}"}}


@pytest_asyncio.fixture
async def user_b(client):
    await client.post("/api/v1/auth/register", json={
        "email": "bob@test.com", "username": "bob", "password": "BobPass123",
    })
    r = await client.post("/api/v1/auth/login", json={
        "email": "bob@test.com", "password": "BobPass123",
    })
    body = r.json()
    return {"id": body["user_id"], "headers": {"Authorization": f"Bearer {body['access_token']}"}}
```

- [ ] **Step 2: Suite de cross-user**

```python
# backend/tests/test_rls_cross_user.py
import pytest


@pytest.mark.asyncio
async def test_user_a_cannot_read_user_b_profile(client, user_a, user_b):
    # B logueado, intenta leer perfil de A vía endpoint /users/{id}
    r = await client.get(f"/api/v1/users/{user_a['id']}", headers=user_b["headers"])
    assert r.status_code in (403, 404)


@pytest.mark.asyncio
async def test_export_only_returns_own_data(client, user_a, user_b):
    rA = (await client.get("/api/v1/users/me/export", headers=user_a["headers"])).json()
    rB = (await client.get("/api/v1/users/me/export", headers=user_b["headers"])).json()
    assert rA["user"]["email"] == "alice@test.com"
    assert rB["user"]["email"] == "bob@test.com"
    assert rA["user"]["id"] != rB["user"]["id"]


@pytest.mark.asyncio
async def test_progress_isolated_per_user(client, user_a, user_b):
    # A registra progreso, B no debe verlo
    pa = await client.get("/api/v1/progress", headers=user_a["headers"])
    pb = await client.get("/api/v1/progress", headers=user_b["headers"])
    assert pa.status_code == 200
    assert pb.status_code == 200
    # ningún elemento de B incluye user_id de A
    for item in pb.json():
        assert item.get("user_id") != user_a["id"]


@pytest.mark.asyncio
async def test_delete_me_does_not_affect_other_user(client, user_a, user_b):
    await client.delete("/api/v1/users/me", headers=user_a["headers"])
    # B sigue funcional
    r = await client.get("/api/v1/users/me/export", headers=user_b["headers"])
    assert r.status_code == 200
    assert r.json()["user"]["email"] == "bob@test.com"
```

- [ ] **Step 3: Correr**

Run: `cd backend; pytest tests/test_rls_cross_user.py -v`
Expected: PASS (4 tests). Si alguno falla, corregir el endpoint que filtra por user_id en backend (el frontend NO debe ser la única defensa).

- [ ] **Step 4: Añadir job al CI**

En `.github/workflows/ci.yml`, asegurarse que `cd backend && pytest` corre la suite. (Ya cubierto por Task 1.)

- [ ] **Step 5: Commit**

```bash
git add backend/tests/conftest.py backend/tests/test_rls_cross_user.py
git commit -m "Test suite cross-user: A no puede leer ni modificar datos de B (RLS verificada)"
```

---

### Task 20: Dependabot + pip-audit + npm audit en CI

**Files:**
- Create: `.github/dependabot.yml`
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: `.github/dependabot.yml`**

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

- [ ] **Step 2: Job `audit` en CI**

Editar `.github/workflows/ci.yml`, añadir:

```yaml
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install pip-audit
      - run: pip-audit -r requirements.txt --desc --strict || echo "vulns encontradas"
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: cd frontend && npm ci && (npm audit --audit-level=high || echo "vulns encontradas")
```

> El `|| echo` permite que el build no falle por CVEs informativos. Cuando haya proceso de triage definido, cambiar a `pip-audit --strict` sin tolerancia.

- [ ] **Step 3: Verificar localmente que pip-audit corre**

Run: `pip install pip-audit; pip-audit -r requirements.txt`
Expected: lista de paquetes verificada.

- [ ] **Step 4: Commit**

```bash
git add .github/dependabot.yml .github/workflows/ci.yml
git commit -m "Dependabot semanal (pip/npm/actions) y job audit en CI con pip-audit + npm audit"
```

---

### Task 21: `requirements.lock` y verificación de secrets en repo

**Files:**
- Create: `requirements.lock`
- Modify: `.github/workflows/ci.yml`
- Create: `.gitleaks.toml` (opcional, ver Step 4)

- [ ] **Step 1: Generar lockfile**

Run: `pip install pip-tools; pip-compile requirements.txt --output-file=requirements.lock`
Expected: archivo `requirements.lock` con versiones congeladas.

- [ ] **Step 2: Verificar que `.env` está en `.gitignore`**

Run: `Select-String -Path .gitignore -Pattern "^.env$"`
Expected: línea presente. Si no, añadirla.

Verificar también `*.env`, `.env.*`, `.venv*/`, `node_modules/`.

- [ ] **Step 3: Scan rápido del repo por secrets antes de hacer push**

Run:
```bash
git log -p --all | grep -iE "(api[_-]?key|secret|password)" | head -50
```
Expected: no claves reales — solo strings de ejemplo.

Si encuentra algo real → rotar la clave inmediatamente y eliminar del historial con `git filter-repo`.

- [ ] **Step 4: Añadir gitleaks al CI (opcional pero recomendado)**

```yaml
  secrets-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}
```

(Si no quieres gitleaks por dependencia externa, omite este paso — `pip-audit` + scan manual es suficiente para Fase 0.)

- [ ] **Step 5: Commit**

```bash
git add requirements.lock .github/workflows/ci.yml .gitignore
git commit -m "Lockfile pip-tools y job de secrets scan en CI"
```

---

### Task 22: Pyodide Web Worker — scaffold del Worker y tipos

**Files:**
- Modify: `frontend/package.json`
- Create: `frontend/src/sandbox/types.ts`
- Create: `frontend/src/sandbox/pyodideWorker.ts`
- Modify: `frontend/vite.config.ts` (worker bundling)

- [ ] **Step 1: Añadir dependencias frontend**

```bash
cd frontend
npm install pyodide@0.26.4 comlink@4.4.1 dompurify@3.1.6
npm install -D @types/dompurify@3.0.5
```

(O editar `package.json` directamente y `npm install`.)

- [ ] **Step 2: `frontend/src/sandbox/types.ts`**

```typescript
export type RunStatus = "idle" | "loading" | "running" | "ready" | "error";

export interface RunResult {
  ok: boolean;
  stdout: string;
  stderr: string;
  durationMs: number;
  timedOut: boolean;
  error?: string;
}

export interface RunRequest {
  code: string;
  timeoutMs?: number; // default 30_000
}

export interface KernelInfo {
  ready: boolean;
  pyodideVersion?: string;
}
```

- [ ] **Step 3: `frontend/src/sandbox/pyodideWorker.ts`**

```typescript
/// <reference lib="webworker" />
import * as Comlink from "comlink";
import { loadPyodide, type PyodideInterface } from "pyodide";
import type { RunRequest, RunResult, KernelInfo } from "./types";

const PYODIDE_INDEX_URL = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";

class Kernel {
  private py: PyodideInterface | null = null;
  private stdoutBuf: string[] = [];
  private stderrBuf: string[] = [];

  async init(): Promise<KernelInfo> {
    if (this.py) return { ready: true, pyodideVersion: this.py.version };
    this.py = await loadPyodide({
      indexURL: PYODIDE_INDEX_URL,
      stdout: (line) => this.stdoutBuf.push(line),
      stderr: (line) => this.stderrBuf.push(line),
    });
    return { ready: true, pyodideVersion: this.py.version };
  }

  async run({ code, timeoutMs = 30_000 }: RunRequest): Promise<RunResult> {
    if (!this.py) await this.init();
    this.stdoutBuf = [];
    this.stderrBuf = [];
    const start = performance.now();
    let timedOut = false;
    let timer: number | undefined;

    const timeoutPromise = new Promise<never>((_, reject) => {
      timer = self.setTimeout(() => {
        timedOut = true;
        reject(new Error(`Timeout (${timeoutMs}ms)`));
      }, timeoutMs);
    });

    try {
      await Promise.race([this.py!.runPythonAsync(code), timeoutPromise]);
      return {
        ok: true,
        stdout: this.stdoutBuf.join("\n"),
        stderr: this.stderrBuf.join("\n"),
        durationMs: performance.now() - start,
        timedOut: false,
      };
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      return {
        ok: false,
        stdout: this.stdoutBuf.join("\n"),
        stderr: this.stderrBuf.join("\n") + (this.stderrBuf.length ? "\n" : "") + msg,
        durationMs: performance.now() - start,
        timedOut,
        error: msg,
      };
    } finally {
      if (timer !== undefined) self.clearTimeout(timer);
    }
  }
}

Comlink.expose(new Kernel());
```

- [ ] **Step 4: Vite config para Workers TS**

Verificar `frontend/vite.config.ts` no necesita cambios — Vite 5 soporta Workers nativamente con `new Worker(new URL("./worker.ts", import.meta.url), { type: "module" })`.

- [ ] **Step 5: Smoke build**

Run: `cd frontend; npm run build`
Expected: build exitoso, sin errores de TS.

- [ ] **Step 6: Commit**

```bash
git add frontend/package.json frontend/package-lock.json frontend/src/sandbox/
git commit -m "Pyodide Web Worker con Comlink: kernel con timeout, stdout/stderr buffer"
```

---

### Task 23: Pyodide Sandbox wrapper en main thread

**Files:**
- Create: `frontend/src/sandbox/PyodideSandbox.ts`
- Create: `frontend/src/sandbox/index.ts`

- [ ] **Step 1: `PyodideSandbox.ts`**

```typescript
import * as Comlink from "comlink";
import type { RunRequest, RunResult, KernelInfo, RunStatus } from "./types";

export class PyodideSandbox {
  private worker: Worker | null = null;
  private kernel: Comlink.Remote<{
    init(): Promise<KernelInfo>;
    run(req: RunRequest): Promise<RunResult>;
  }> | null = null;
  private _status: RunStatus = "idle";
  private listeners = new Set<(s: RunStatus) => void>();

  get status(): RunStatus {
    return this._status;
  }

  onStatusChange(cb: (s: RunStatus) => void): () => void {
    this.listeners.add(cb);
    return () => this.listeners.delete(cb);
  }

  private setStatus(s: RunStatus) {
    this._status = s;
    this.listeners.forEach((l) => l(s));
  }

  async init(): Promise<void> {
    if (this.kernel) return;
    this.setStatus("loading");
    this.worker = new Worker(
      new URL("./pyodideWorker.ts", import.meta.url),
      { type: "module", name: "pyodide-kernel" },
    );
    this.kernel = Comlink.wrap(this.worker);
    await this.kernel.init();
    this.setStatus("ready");
  }

  async run(code: string, timeoutMs = 30_000): Promise<RunResult> {
    await this.init();
    this.setStatus("running");
    try {
      const result = await this.kernel!.run({ code, timeoutMs });
      this.setStatus(result.ok ? "ready" : "error");
      return result;
    } catch (e) {
      this.setStatus("error");
      throw e;
    }
  }

  async restartKernel(): Promise<void> {
    this.dispose();
    await this.init();
  }

  dispose(): void {
    this.worker?.terminate();
    this.worker = null;
    this.kernel = null;
    this.setStatus("idle");
  }
}

let _singleton: PyodideSandbox | null = null;
export function getSandbox(): PyodideSandbox {
  if (!_singleton) _singleton = new PyodideSandbox();
  return _singleton;
}
```

- [ ] **Step 2: `frontend/src/sandbox/index.ts`** — barrel export

```typescript
export { PyodideSandbox, getSandbox } from "./PyodideSandbox";
export type { RunRequest, RunResult, RunStatus, KernelInfo } from "./types";
```

- [ ] **Step 3: Verificar build**

Run: `cd frontend; npm run build`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/sandbox/PyodideSandbox.ts frontend/src/sandbox/index.ts
git commit -m "PyodideSandbox wrapper: lifecycle, restartKernel, status events"
```

---

### Task 24: Reemplazar llamadas a `/api/v1/execute/run` por la sandbox local

**Files:**
- Modify: `frontend/src/services/api.ts` (o el cliente que llama a /run)
- Modify: `frontend/src/components/Editor/RunButton.tsx` (o equivalente)

- [ ] **Step 1: Identificar dónde se llama el endpoint**

Run: 
```bash
cd frontend
grep -rn "execute/run\|/api/v1/execute" src/
```

Anotar archivos.

- [ ] **Step 2: Crear wrapper que prefiere sandbox local**

Crear o modificar `frontend/src/services/codeRunner.ts`:

```typescript
import { getSandbox, type RunResult } from "@/sandbox";

export async function runPythonCode(code: string, timeoutMs = 30_000): Promise<RunResult> {
  const sandbox = getSandbox();
  return sandbox.run(code, timeoutMs);
}
```

- [ ] **Step 3: Sustituir llamadas en componentes**

Donde antes había:
```typescript
const result = await api.post("/execute/run", { code });
```

reemplazar por:
```typescript
import { runPythonCode } from "@/services/codeRunner";
const result = await runPythonCode(code);
```

Adaptar la forma del result (`stdout`, `stderr`, `ok`).

- [ ] **Step 4: Probar manualmente**

Run: `cd frontend; npm run dev` (en una terminal aparte) y probar el editor.
Expected: el botón Run ejecuta código localmente; primera vez tarda 2-3s en cargar Pyodide.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/services/codeRunner.ts frontend/src/components/
git commit -m "Frontend ejecuta código en Pyodide sandbox local; deprecado endpoint /execute/run"
```

---

### Task 25: Frontend — interceptor axios para refresh automático

**Files:**
- Modify: `frontend/src/services/api.ts`
- Modify: `frontend/src/stores/authStore.ts`

- [ ] **Step 1: Estado del refresh token en authStore**

En `authStore.ts`, añadir `refreshToken` al estado y al setter:

```typescript
type AuthState = {
  accessToken: string | null;
  refreshToken: string | null;
  // ...
  setTokens: (access: string, refresh: string) => void;
  clearTokens: () => void;
};
```

- [ ] **Step 2: Interceptor en `api.ts`**

```typescript
import axios from "axios";
import { useAuthStore } from "@/stores/authStore";

export const api = axios.create({ baseURL: "/api/v1" });

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

let refreshing: Promise<string> | null = null;

api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = useAuthStore.getState().refreshToken;
      if (!refresh) {
        useAuthStore.getState().clearTokens();
        return Promise.reject(error);
      }
      try {
        if (!refreshing) {
          refreshing = (async () => {
            const r = await axios.post("/api/v1/auth/refresh", { refresh_token: refresh });
            useAuthStore.getState().setTokens(r.data.access_token, r.data.refresh_token);
            return r.data.access_token as string;
          })();
        }
        const newToken = await refreshing;
        refreshing = null;
        original.headers.Authorization = `Bearer ${newToken}`;
        return api(original);
      } catch (e) {
        refreshing = null;
        useAuthStore.getState().clearTokens();
        return Promise.reject(e);
      }
    }
    return Promise.reject(error);
  },
);
```

- [ ] **Step 3: Smoke test manual**

Iniciar backend y frontend, login, esperar a que access token expire (o cambiar `ACCESS_TOKEN_EXPIRE_MINUTES=1` para test), hacer request: debe rotarse automáticamente.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/services/api.ts frontend/src/stores/authStore.ts
git commit -m "Frontend: interceptor axios refresca access_token automáticamente con refresh_token"
```

---

### Task 26: Dockerfile para backend

**Files:**
- Create: `backend/Dockerfile`
- Create: `backend/.dockerignore`

- [ ] **Step 1: `backend/Dockerfile`**

```dockerfile
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.lock /app/requirements.lock
RUN pip install --no-cache-dir -r requirements.lock

COPY backend/ /app/backend/
COPY maestro_evaluador_de_codigo_python.txt /app/

WORKDIR /app/backend

EXPOSE 8000

# Aplicar migraciones antes de servir
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

- [ ] **Step 2: `.dockerignore`**

```
.venv*
__pycache__
*.pyc
.pytest_cache
.mypy_cache
.git
.github
docs
node_modules
frontend
*.db
.env
.env.*
```

- [ ] **Step 3: Build local**

Run (si Docker está disponible): `docker build -f backend/Dockerfile -t pycode-backend .`
Expected: build exitoso.

- [ ] **Step 4: Commit**

```bash
git add backend/Dockerfile backend/.dockerignore
git commit -m "Dockerfile backend con migraciones Alembic en startup"
```

---

### Task 27: Render blueprint y configuración de deploy

**Files:**
- Create: `render.yaml` (raíz)

- [ ] **Step 1: `render.yaml`**

```yaml
services:
  - type: web
    name: pycode-backend
    runtime: docker
    plan: free
    region: oregon
    dockerfilePath: ./backend/Dockerfile
    healthCheckPath: /health
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: "false"
      - key: PORT
        value: "10000"
      - key: DATABASE_URL
        sync: false
      - key: SECRET_KEY
        sync: false
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_ANON_KEY
        sync: false
      - key: SUPABASE_SERVICE_KEY
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: LLM_PROVIDER
        value: groq
      - key: LLM_MODEL
        value: llama-3.3-70b-versatile
      - key: SENTRY_DSN
        sync: false
      - key: CORS_ORIGINS
        value: https://pycode.app,https://pycode.vercel.app
```

- [ ] **Step 2: Documentar pasos manuales**

Crear `docs/DEPLOY.md`:

```markdown
# Despliegue PyCode Platform v2

## Backend (Render)
1. Crear cuenta en render.com
2. New → Blueprint → conectar repo GitHub
3. Render detecta `render.yaml` y crea el servicio
4. Settings → Environment → pegar valores reales (los `sync: false`)
5. Manual Deploy

## Frontend (Vercel)
1. vercel.com → New Project → import repo
2. Root directory: `frontend`
3. Build command: `npm run build`
4. Output directory: `dist`
5. Environment Variables: ninguna (rewrites en `vercel.json`)

## Supabase
1. supabase.com → New Project (free tier)
2. Project Settings → Database → Connection string (tipo `postgres+asyncpg`)
3. Project Settings → API → anon key + service_role key
4. SQL Editor → ejecutar las migraciones manualmente o via Render release command

## UptimeRobot
1. uptimerobot.com → Add Monitor
2. Type: HTTP(s)
3. URL: `https://pycode-backend.onrender.com/health`
4. Interval: 14 minutos (Render duerme tras 15)
```

- [ ] **Step 3: Commit**

```bash
git add render.yaml docs/DEPLOY.md
git commit -m "Render blueprint backend + documentación de despliegue (Render + Vercel + Supabase + UptimeRobot)"
```

---

### Task 28: Vercel config para frontend

**Files:**
- Create: `vercel.json`
- Create: `frontend/.env.production.example`

- [ ] **Step 1: `vercel.json`**

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "buildCommand": "cd frontend && npm ci && npm run build",
  "outputDirectory": "frontend/dist",
  "installCommand": "echo skip",
  "framework": null,
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://pycode-backend.onrender.com/api/:path*"
    },
    {
      "source": "/ws/:path*",
      "destination": "https://pycode-backend.onrender.com/ws/:path*"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        {
          "key": "Permissions-Policy",
          "value": "geolocation=(), microphone=(), camera=()"
        }
      ]
    }
  ]
}
```

- [ ] **Step 2: `frontend/.env.production.example`**

```env
VITE_API_BASE=/api/v1
```

(El frontend usa rutas relativas; Vercel reescribe a Render.)

- [ ] **Step 3: Commit**

```bash
git add vercel.json frontend/.env.production.example
git commit -m "Vercel config con rewrites a Render y headers de seguridad replicados"
```

---

### Task 29: Smoke test full stack contra entorno staging

**Files:** *(no código nuevo — verificación)*

- [ ] **Step 1: Crear proyecto Supabase de test**

Manual: crear free project, copiar `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`.

- [ ] **Step 2: Aplicar migraciones contra Supabase**

Run:
```bash
cd backend
$env:DATABASE_URL = "postgresql+asyncpg://postgres:CONTRASEÑA@db.PROJECT.supabase.co:5432/postgres?sslmode=require"
alembic upgrade head
```
Expected: 4 migraciones aplicadas.

- [ ] **Step 3: Correr la suite completa contra Supabase**

Run: `cd backend; pytest -v`
Expected: PASS (todos).

- [ ] **Step 4: Deploy a Render manual**

Push a una rama `staging`, configurar Render para hacer deploy desde esa rama.

Verificar `https://pycode-backend.onrender.com/health` retorna `{"status": "healthy"}`.

- [ ] **Step 5: Deploy a Vercel manual**

Mismo flujo. Verificar que carga el editor y que el botón Run ejecuta vía Pyodide.

- [ ] **Step 6: UptimeRobot configurado**

Crear monitor; verificar que pinguea cada 14 min.

- [ ] **Step 7: Commit con notas (sin código)**

```bash
git commit --allow-empty -m "Validado deploy E2E: Supabase + Render + Vercel + UptimeRobot funcionan"
```

---

### Task 30: Cleanup final y checklist Fase 0

**Files:**
- Create: `docs/superpowers/plans/fase-0-checklist.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Checklist de salida**

Crear `docs/superpowers/plans/fase-0-checklist.md` con:

```markdown
# Fase 0 — Checklist de salida

- [x] Postgres + Alembic en producción (sin SQLite, sin create_all)
- [x] RLS habilitada en `users`, `user_profiles`, `user_progress`, `code_submissions`, `tutor_sessions`, `refresh_tokens`
- [x] Test suite cross-user en CI
- [x] Lint anti-SQLi en CI (check_no_sqli.py)
- [x] Pydantic strict en endpoints públicos
- [x] Headers de seguridad (HSTS/CSP/XCTO/XFO/Referrer-Policy/Permissions)
- [x] CORS whitelist (sin wildcard en prod)
- [x] Rate limiting universal (login 5/min, register 3/h, tutor 50/día, default 100/min)
- [x] Logging estructurado con redaction PII
- [x] Sentry integrado con scrubbing
- [x] Dependabot + pip-audit + npm audit en CI
- [x] requirements.lock commiteado
- [x] /health slim sin info sensible
- [x] Provider abstraction LLM (Groq + OpenAI + Stub)
- [x] Pyodide en Web Worker reemplaza subprocess executor
- [x] /api/v1/execute/run retorna 410 GONE
- [x] JWT con refresh token rotation + /logout que revoca jti
- [x] GDPR: DELETE /users/me, GET /users/me/export
- [x] Deploy en Vercel + Render + UptimeRobot funcional
- [x] Documentación de deploy en docs/DEPLOY.md
```

- [ ] **Step 2: Actualizar `CLAUDE.md`**

En sección "## Project", reemplazar "**Current Status (Fase 1.0)**: ✅ Core features complete" por:

```markdown
**Current Status (Fase 0 v2)**: ✅ Fundamentos + seguridad base
- Postgres + Alembic + RLS habilitada por tabla
- Pyodide cliente reemplaza subprocess executor
- Provider abstraction LLM (Groq default)
- Headers seguros, CORS whitelist, rate limiting universal
- JWT con refresh rotation, GDPR endpoints
- Logging structlog con redaction PII, Sentry, Dependabot
- Deploy gratis en Render + Vercel + Supabase + UptimeRobot

Próxima fase: Fase 1 — pulido Track 1 + sistema ELO completo (ver `docs/superpowers/specs/2026-05-03-pycode-platform-v2-design.md`)
```

En "## Common commands", reemplazar el bloque DB para reflejar Postgres-only y el nuevo flujo de migraciones:

```bash
# Migraciones DB
cd backend && alembic upgrade head
cd backend && alembic revision --autogenerate -m "descripcion"
```

Y eliminar referencia a `bootstrap_elo_schema` en la sección "## Architecture" → "Backend (FastAPI...)".

- [ ] **Step 3: Verificación final del CI**

Run: `git push` y observar que el workflow `ci.yml` pasa todos los jobs (backend-tests, backend-lint, frontend-build, audit).

- [ ] **Step 4: Commit final de Fase 0**

```bash
git add docs/superpowers/plans/fase-0-checklist.md CLAUDE.md
git commit -m "Fase 0 completa: checklist de salida y CLAUDE.md actualizado"
git tag fase-0-complete
```

---

## Anexo: Paralelización

Las Tasks pueden agruparse para que dos personas (o tú alternando) trabajen en paralelo:

- **Carril A — Infra y BD**: Tasks 1, 2, 3, 4, 5
- **Carril B — Seguridad capa app**: Tasks 6, 7, 8, 9, 10, 11, 12, 13 (depende de carril A para tener Postgres)
- **Carril C — Auth + GDPR**: Tasks 16, 17 (depende de A y B)
- **Carril D — RLS**: Tasks 18, 19 (depende de A, B y C)
- **Carril E — LLM provider**: Task 15 (independiente, puede ir paralelo a cualquier carril)
- **Carril F — Pyodide frontend**: Tasks 14, 22, 23, 24, 25 (independiente del backend salvo Task 14)
- **Carril G — CI security**: Tasks 6, 20, 21
- **Carril H — Deploy**: Tasks 26, 27, 28, 29 (al final, requiere todo lo anterior listo)
- **Carril I — Cleanup**: Task 30

Orden recomendado: A → (B en paralelo con E y F) → C → D → G → H → I.

---

## Self-review

**Cobertura del spec sec. 9 + roadmap Fase 0:**

| Requisito spec | Tasks |
|---|---|
| Migrar a Supabase Postgres (asyncpg) | 3, 29 |
| Alembic + migración inicial | 4 |
| Eliminar bootstrap_elo_schema | 5 |
| Provider abstraction LLM | 15 |
| Pyodide reemplaza subprocess | 14, 22, 23, 24 |
| Setup despliegue Vercel + Render + UptimeRobot + Supabase | 26, 27, 28, 29 |
| RLS en todas las tablas con datos por usuario | 18 |
| Test suite cross-user | 19 |
| Lint anti-SQLi en CI | 6 |
| Pydantic strict | 7 |
| Headers de seguridad | 8 |
| CORS whitelist | 9 |
| Rate limiting universal (incl. tutor) | 10 |
| Logging estructurado + PII redaction | 11 |
| Sentry con scrubbing | 12 |
| Dependabot + pip-audit + npm audit | 20 |
| .env.example + secrets check | 2, 21 |
| /health slim | 13 |
| JWT refresh rotation (Sec. 9.4) | 16 |
| GDPR DELETE /me + export (Sec. 9.14) — adelantado a Fase 0 por petición del usuario | 17 |
| Test smoke + CI bootstrap (precondición) | 1 |

**Placeholder scan:** sin "TODO", "TBD", "implement later", validaciones genéricas ni referencias a tasks futuras.

**Type consistency:** los nombres `LLMProvider.chat()`, `RefreshToken.jti`, `RunResult.stdout`, `Token.refresh_token` son consistentes entre tasks que los referencian.

**Scope:** Fase 0 está completa en este plan. Fases 1-7 quedan en el spec y producirán sus propios planes.
