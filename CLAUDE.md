# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

PyCode Platform — learning platform for Python with Monaco editor, sandboxed code execution, a Socratic AI tutor, and a Finxter-inspired ELO puzzle progression system. 

**Current Status (Fase 0 v2)**: ✅ **Fase 0 cerrada (30/30) — tag `fase-0-complete` (2026-05-08)**
- Postgres + Alembic + migraciones versionadas (sin SQLite ni `create_all` en prod)
- RLS habilitada por tabla con `current_setting('app.current_user_id')` + tests cross-user
- Pyodide en Web Worker reemplaza el subprocess executor; backend ya no ejecuta código
- Provider abstraction LLM (Groq default + OpenAI fallback + Stub)
- Headers seguros, CORS whitelist, rate limiting universal con SlowAPI
- JWT con refresh token rotation + endpoints GDPR (DELETE /me, GET /me/export)
- Logging structlog con redaction PII, Sentry con scrubbing, Dependabot semanal
- Deploy gratis configurado: Render (backend) + Vercel (frontend) + Supabase (Postgres)

**Producción**:
- Frontend: https://pycode-platform.vercel.app (Vercel Hobby)
- Backend: https://pycode-backend.onrender.com (Render Free, Docker)
- DB: Supabase Postgres `medutbqsurjnaaymmrin` (sa-east-1, RLS habilitada)
- Watchdog: UptimeRobot ping `/health` cada 5 min

**Próxima fase: Fase 1** — pulido del Track 1 + sistema ELO completo. Spec en `docs/superpowers/specs/2026-05-03-pycode-platform-v2-design.md`. Primer trabajo identificado: separar el evaluador de código del tutor de Q&A (dos roles, dos tablas, dos system prompts). Detalle en memoria persistente `project_fase1_tutor_redesign.md`.

See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for the vision and [PYCODE_SPEC.md](PYCODE_SPEC.md) for the phased implementation spec.

## Notas operativas (post-deploy)

- **Cold start de Render free**: el contenedor duerme tras 15 min de inactividad; UptimeRobot lo evita pingueando `/health` cada 5 min. Si UptimeRobot se cae, las primeras llamadas tras un período idle pueden tardar 30-60s o devolver 502.
- **WebSocket del Tutor IA**: Vercel Hobby no proxea WebSockets de forma confiable a través de los rewrites de `vercel.json`. `TutorChat.tsx` conecta directamente a `wss://pycode-backend.onrender.com/ws/tutor` cuando `import.meta.env.PROD` es true.
- **CORS_ORIGINS** en Render incluye el dominio Vercel exacto (`https://pycode-platform.vercel.app`). Si se cambia el dominio de Vercel (ej. dominio custom), hay que actualizar `CORS_ORIGINS` en Render Settings → Environment y redesplegar.
- **Rate limit de SlowAPI** guarda contadores en memoria del proceso de Render; un redeploy los resetea, útil si te bloqueas durante pruebas.

## Common commands

Backend (`backend/`, runs via `.venv311`):
```bash
# Activate venv (Windows): backend/.venv311/Scripts/activate
cd backend && alembic upgrade head             # aplica migraciones (obligatorio antes de levantar)
cd backend && uvicorn app.main:app --reload --port 8000
pip install -r ../requirements.txt
pytest                        # pytest-asyncio mode=auto; conftest aplica alembic upgrade head + resetea SlowAPI
pytest path/to/test.py::name  # single test
black . && flake8 . && mypy .
cd backend && python scripts/check_no_sqli.py  # lint anti-SQLi de Task 6 (corre también en CI)
```

Migraciones:
```bash
cd backend && alembic upgrade head
cd backend && alembic revision --autogenerate -m "descripcion"
```

Frontend (`frontend/`):
```bash
npm run dev       # vite on :5173 with /api + /ws proxy to :8000
npm run build     # tsc + vite build — TypeScript errors fail the build
npm run lint      # eslint, --max-warnings 0
npm run test      # vitest
```

Full stack via Docker: `docker-compose up` (brings up backend, frontend, postgres, redis, celery, celery-beat).

## Architecture

**Monorepo layout**: `backend/` (FastAPI) + `frontend/` (React/Vite) + `Elo_pycode/` (staging folder for ELO components not yet wired in — same filenames as the in-tree ones) + `external/Retos_Python/` (external challenge source imported at startup).

### Backend (FastAPI, async SQLAlchemy 2.0)

Entry point: [backend/app/main.py](backend/app/main.py). El `lifespan` ya **no** crea tablas — el schema lo gestiona Alembic. Antes de levantar el server hay que correr `alembic upgrade head` (el `Dockerfile` lo hace en su `CMD`; el `conftest` lo hace al cargar). El lifespan solo seedea puzzles, interview puzzles, generated puzzles/challenges, external challenges y lessons-with-exercises (todos idempotentes "if empty").

Cualquier modelo nuevo debe importarse en `main.py` Y en `backend/alembic/env.py` para que `Base.metadata` lo conozca.

DB: defaults a `sqlite+aiosqlite:///./pycode.db` solo en dev/test; producción es `postgresql+asyncpg://...?sslmode=require`. `_get_engine_args(db_url, environment)` en [backend/app/core/database.py](backend/app/core/database.py) **rechaza SQLite si `ENVIRONMENT=production`** y rechaza URLs no soportadas (sin fallback silencioso).

Migraciones Alembic en [backend/alembic/versions/](backend/alembic/versions/): `0001_initial_schema` (todas las tablas), `0002_refresh_tokens`, `0003_cascade_user_fks` (no-op en SQLite, aplica `ON DELETE CASCADE` en Postgres). La migración 0004 con políticas RLS está pendiente (Task 18).

API surface versionada en `/api/v1` via [backend/app/api/v1/router.py](backend/app/api/v1/router.py): `auth` (login/register/refresh/logout), `users` (me, me/export, DELETE me), `lessons`, `exercises`, `execute` (run→410, validate con `ast.parse`), `tutor`, `progress`, `elo`, `challenges`. WebSocket `/ws/code` está deprecado (envía mensaje y cierra); `/ws/tutor` sigue activo.

**Lessons & Exercises**: [backend/app/services/lesson_content.py](backend/app/services/lesson_content.py) contiene 25 `LessonTemplate` con contenido en español + 64 `ExerciseTemplate` (3 por lección en promedio, dificultad progresiva). Seeded vía [backend/app/services/lesson_seed.py](backend/app/services/lesson_seed.py) en startup (upsert idempotente por title). **Known issue fixed**: GET `/{lesson_id}` usa `selectinload(Lesson.exercises)` para evitar lazy-load errors en contexto async.

Code execution: el endpoint `POST /api/v1/execute/run` retorna **410 Gone**; toda la ejecución de código del estudiante vive en [Pyodide en Web Worker](frontend/src/sandbox/pyodideWorker.ts) en el cliente. `POST /api/v1/execute/validate` solo corre `ast.parse` para detectar errores de sintaxis sin ejecutar. El backend nunca toca código del estudiante.

**Seguridad transversal** (capa middleware): [security_headers.py](backend/app/core/security_headers.py) (HSTS/CSP/XCTO/XFO/Referrer-Policy/Permissions-Policy), [rate_limit.py](backend/app/core/rate_limit.py) (SlowAPI con `_user_or_ip` keyfunc), [logging_config.py](backend/app/core/logging_config.py) (structlog + redact_pii), [observability.py](backend/app/core/observability.py) (Sentry no-op si no hay DSN). Todos se montan en `main.py`.

LLM: [llm_provider.py](backend/app/services/llm_provider.py) abstrae Groq + OpenAI + Stub. `get_provider(settings)` despacha por `LLM_PROVIDER`. Stub se usa cuando no hay API key — devuelve `""` y deja que el caller use fallback.

ELO system: puzzles, attempts, ratings, and rank progression live in [backend/app/services/elo_service.py](backend/app/services/elo_service.py) + [backend/app/models/elo_models.py](backend/app/models/elo_models.py). Rank deltas use step tables keyed by rating range (`ELO_DELTA_TABLE`, `ELO_DELTA_TABLE_ADVANCED`). The tutor prompt lives in the repo-root file referenced by `TUTOR_PROMPT_FILE` (default `maestro_evaluador_de_codigo_python.txt`) and is resolved via `settings.tutor_prompt_path`.

### Frontend (React + TS + Vite + Tailwind + Zustand)

Vite dev server proxies `/api` and `/ws` to `localhost:8000` ([vite.config.ts](frontend/vite.config.ts)) — frontend code should call relative paths, not absolute `http://localhost:8000`. `@/*` alias points to `src/`.

Global state: un único Zustand store [frontend/src/stores/authStore.ts](frontend/src/stores/authStore.ts) que maneja `accessToken` + `refreshToken` + `user`. API calls van por [frontend/src/services/api.ts](frontend/src/services/api.ts) (fetch nativo, no axios) — incluye interceptor que ante un 401 intenta `POST /auth/refresh` con el refresh token y reintenta el request original; si falla, limpia tokens y redirect a `/login`.

Pyodide sandbox vive en [frontend/src/sandbox/](frontend/src/sandbox/): `pyodideWorker.ts` corre como Web Worker (cargado via `new URL(..., import.meta.url)` con `worker.format='es'` en `vite.config.ts`), `PyodideSandbox.ts` lo envuelve con Comlink. El runtime Pyodide se carga lazy desde `cdn.jsdelivr.net` (whitelisted en CSP).

## Conventions

- Language of user-facing strings, commit messages, docs, and most code comments is **Spanish**. Keep that tone when editing UI copy or writing new docs.
- Seeders are idempotent and run on every startup — when adding one, follow the "if empty" pattern already in `puzzle_seed.py` / `lesson_seed.py` and register it inside the `lifespan` block.
- **Schema changes go through Alembic**, no shortcuts. Si añades columnas o tablas: importa el modelo en `backend/alembic/env.py`, corre `alembic revision --autogenerate -m "descripcion"` contra Postgres limpio, renombra el archivo a `NNNN_descripcion.py` y verifica que el upgrade sea no-op-safe en SQLite (los tests corren con SQLite). Para DDL Postgres-only (RLS, constraints sin nombre estable) usa `if op.get_bind().dialect.name != "postgresql": return` al inicio del upgrade.
- Las FKs hacia `users.id` deben llevar `ondelete="CASCADE"` para que `DELETE /users/me` (GDPR) funcione sin orphans en Postgres.
- The `Elo_pycode/` folder is a **staging area**, not dead code — files there are meant to be integrated into `backend/app/...` and `frontend/src/...` per Fase 2 of the spec. Check both locations before assuming something is missing.
- Async SQLAlchemy: Always use eager loading (`selectinload`, `joinedload`) for relationships accessed in endpoints — lazy loading fails in async context (MissingGreenlet error).
- **No Co-Authored-By en commits** del proyecto (preferencia del usuario).
