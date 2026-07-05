# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

PyCode Platform — learning platform for Python with Monaco editor, sandboxed code execution, a Socratic AI tutor, and a Finxter-inspired ELO puzzle progression system. 

**Norte estratégico**: PyCode **no** es "Python para principiantes". Track 1 (Python) es la rampa hacia el pipeline **Python → Data Science → ML → Deep Learning → AI Engineering → MLOps**. Toda feature nueva debe apoyar esa rampa (ver memoria `project_norte_ml_ai`).

**Estado actual (2026-07)**:
- ✅ **Fase 0 cerrada (30/30)** — tag `fase-0-complete` (2026-05-08). Infra: Postgres+Alembic+RLS, Pyodide Web Worker, LLM provider abstraction, seguridad transversal, JWT+GDPR, deploy gratis.
- ✅ **Fase 1 cerrada** — pulido Track 1 + ELO completo. Tutor separado en evaluador (REST) + Q&A (WS), tests ocultos Pyodide, **ELO multidominio** + snapshots de calidad de código, banco de **100 puzzles curados** + 10 retos DS/ML, capstones + **certificados PDF verificables**.
- ✅ **Track 2 (Data Science) cerrado** — 11 lecciones (NumPy/Pandas/Viz/EDA/Stats) + capstone `track-2-eda-cafecito` + datasets seedeados + render matplotlib en el editor.
- ✅ **Track 3 (ML Clásico) cerrado** — 11 lecciones sklearn en Pyodide (LogReg/KNN, métricas, pipelines, regresión, árboles/RF, CV/GridSearch, KMeans, PCA, SVM, Naive Bayes, ROC/AUC) + capstone `track-3-diagnostico-ml`.
- ✅ **Track 4 (Deep Learning) cerrado** — 5 lecciones **en numpy puro** (neurona/forward, pérdidas+gradiente numérico, backprop, training loop, MLP que resuelve XOR) + capstone `track-4-mlp-desde-cero`. **PyTorch real diferido** (necesitaría GPU remota/Colab; ver `project_track4_piloto`).
- 🚧 **Track 5 (AI Engineering) en curso** — AI 1-3: embeddings/búsqueda semántica, chunking/indexación (retriever RAG en numpy), y LLM real + prompt RAG vía **proxy backend** `POST /api/v1/ai/complete` (reusa el LLM provider; helper `pycode.llm_complete` en el worker). Falta RAG end-to-end, agentes, evals, capstone.
- ⏳ **Pendiente**: resto de Track 5, Track 6 (MLOps).

**Contenido en números**: 55 lecciones (Track 1: 25 · Track 2: 11 · Track 3: 11 · Track 4: 5 · Track 5: 3) · ~130 ejercicios con hidden_tests · 100 puzzles ELO curados · 10 retos · 4 capstones · 3 datasets. Migraciones 0001-0014 (Tracks 3-5 y el proxy LLM **no** añaden migraciones). 161 tests backend. Esquema de datos: `docs/DATABASE.md`.

**Producción**:
- Frontend: https://pycode-platform.vercel.app (Vercel Hobby)
- Backend: https://pycode-backend.onrender.com (Render Free, Docker)
- DB: Supabase Postgres `medutbqsurjnaaymmrin` (sa-east-1, RLS habilitada)
- Watchdog: UptimeRobot ping `/health` cada 5 min

**Próximo trabajo**: continuar Track 5 (AI 4 RAG end-to-end → agentes → evals → capstone "Nebula RAG"). Decisión pendiente aparte: Track 4b con PyTorch real (GPU remota vs Colab). Ver `docs/ARCHITECTURE.md` (diseño), `docs/DATABASE.md` (esquema) y `project_track5_piloto` / `project_track4_piloto` en memoria para el detalle vivo.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the technical design, [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for the vision, and [PYCODE_SPEC.md](PYCODE_SPEC.md) for the phased implementation spec.

## Notas operativas (post-deploy)

- **Cold start de Render free**: el contenedor duerme tras 15 min de inactividad; UptimeRobot lo evita pingueando `/health` cada 5 min. Si UptimeRobot se cae, las primeras llamadas tras un período idle pueden tardar 30-60s o devolver 502.
- **WebSocket del Tutor IA**: Vercel Hobby no proxea WebSockets de forma confiable a través de los rewrites de `vercel.json`. `TutorChat.tsx` conecta directamente a `wss://pycode-backend.onrender.com/ws/tutor` cuando `import.meta.env.PROD` es true.
- **CORS_ORIGINS** en Render incluye el dominio Vercel exacto (`https://pycode-platform.vercel.app`). Si se cambia el dominio de Vercel (ej. dominio custom), hay que actualizar `CORS_ORIGINS` en Render Settings → Environment y redesplegar.
- **Rate limit de SlowAPI** guarda contadores en memoria del proceso de Render; un redeploy los resetea, útil si te bloqueas durante pruebas.
- **Supabase free se pausa** tras ~7 días sin actividad de DB (estado `INACTIVE`) y tumba el siguiente deploy de Render (`alembic upgrade head` no conecta). Mitigación: el workflow `.github/workflows/keepalive-db.yml` (cron cada 4h) golpea `/health/db` (`SELECT 1`). **Señal diagnóstica**: si Render dice "deploy failed" pero **CI está verde**, sospechar Supabase pausada antes que el código/deps; restaurar con el MCP de Supabase (`restore_project`), sin tocar código.
- **Proxy LLM (Track 5)**: `POST /api/v1/ai/complete` llama al modelo real solo si `GROQ_API_KEY` está seteada en Render; sin key cae al `StubProvider` (placeholder determinista). Verificar esa env var antes de esperar respuestas reales del LLM en prod.

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

Entry point: [backend/app/main.py](backend/app/main.py). El `lifespan` ya **no** crea tablas — el schema lo gestiona Alembic. Antes de levantar el server hay que correr `alembic upgrade head` (el `Dockerfile` lo hace en su `CMD`; el `conftest` lo hace al cargar). El lifespan solo seedea puzzles, interview puzzles, generated puzzles/challenges, retos curados, external challenges, datasets, capstones y lessons-with-exercises (todos idempotentes "if empty").

Cualquier modelo nuevo debe importarse en `main.py` Y en `backend/alembic/env.py` para que `Base.metadata` lo conozca.

DB: defaults a `sqlite+aiosqlite:///./pycode.db` solo en dev/test; producción es `postgresql+asyncpg://...?sslmode=require`. `_get_engine_args(db_url, environment)` en [backend/app/core/database.py](backend/app/core/database.py) **rechaza SQLite si `ENVIRONMENT=production`** y rechaza URLs no soportadas (sin fallback silencioso).

Migraciones Alembic en [backend/alembic/versions/](backend/alembic/versions/), `0001`→`0014` monotónicas: `0001_initial_schema` (todas las tablas base), `0002_refresh_tokens`, `0003_cascade_user_fks`, `0004_enable_rls_per_user_tables` (RLS, Postgres-only), `0005_code_evaluations`, `0006_challenge_completions`, `0007_exercise_hidden_tests`, `0008_capstones`, `0009_certificates`, `0010_elo_ratings` (multi-ELO), `0011_challenge_completion_elo_delta`, `0012_code_quality_snapshots`, `0013_lesson_track`, `0014_datasets`. Las DDL Postgres-only (RLS) empiezan con `if op.get_bind().dialect.name != "postgresql": return` para ser no-op en SQLite (tests).

API surface versionada en `/api/v1` via [backend/app/api/v1/router.py](backend/app/api/v1/router.py): `auth` (login/register/refresh/logout), `users` (me, me/export, DELETE me), `lessons`, `exercises` (+ `/{id}/hidden-tests`, `/{id}/evaluations`), `execute` (run→410, validate con `ast.parse`), `tutor` (evaluate REST + WS Q&A), `progress` (competencies, track-status, code-quality), `elo` (attempt, ratings, history, puzzle-of-the-day), `challenges`, `capstones`, `certificates` (issue/download/verify público), `datasets` (CSV), `ai` (`/complete` — proxy LLM del Track 5: auth + rate limit 40/día + tope de tokens, reusa el LLM provider). WebSocket `/ws/code` está deprecado (envía mensaje y cierra); `/ws/tutor` sigue activo.

**Lessons & Exercises**: contenido multi-track en español, seeded idempotente por title en startup. [backend/app/services/lesson_content.py](backend/app/services/lesson_content.py) tiene los 25 `LessonTemplate` de **Track 1** (64 ejercicios) sin campo `track` (default `track-1`); [backend/app/services/lesson_seed.py](backend/app/services/lesson_seed.py) añade **Track 2** (11 lecciones, `track="track-2"`) y **Track 3** (8 lecciones, `track="track-3"`) con sus `ExerciseTemplate`. Añadir una lección a otro track = agregar un `LessonTemplate(track="track-N", category="...", ...)`; sin migración ni endpoints nuevos (la columna `lessons.track` es libre, migración 0013). **Known issue fixed**: GET `/{lesson_id}` usa `selectinload(Lesson.exercises)` para evitar lazy-load errors en contexto async.

**Hidden tests (Pyodide)**: cada `ExerciseTemplate` puede llevar `hidden_tests` (JSON) que NO se exponen en `GET /lessons/{id}` ni `GET /exercises/lesson/{id}` (test de no-leak lo verifica). El worker Pyodide corre cada test en namespace fresco. Es el patrón base de validación replicable a todos los tracks. Datasets (`iris`, `ventas-pyme`, `encuestas`) se sirven via `/api/v1/datasets/{slug}/csv` y se consumen en Pyodide con `pycode.fetch_dataset_csv(slug)`; numpy/pandas/scipy/sklearn autocargan via `loadPackagesFromImports`.

**Capstones & Certificados**: `Capstone` (definicional por track) + `CapstoneSubmission` (uno por user, evaluado con `runCapstoneTests` multi-archivo en Pyodide). Aprobar un capstone (`status="passed"`) desbloquea `POST /certificates/{track}/issue` (gate server-side, 403 si no aprobó), que emite un `Certificate` con `verification_code` público verificable en `GET /certificates/verify/{code}` (sin auth). PDF con reportlab. Capstones actuales: `track-1-cli-ventas`, `track-2-eda-cafecito` (Track 3 pendiente).

**ELO multidominio & calidad de código**: `EloRating(user, domain, scope)` da ELO separado por actividad y categoría temática (`puzzle:<category>`, `challenge:<dificultad>`), con lazy-init desde el ELO global. `code_quality_service.analyze_code` calcula un `static_score` 0-100 con AST (sin ejecutar) que, combinado con los scores logic/general del evaluador LLM, se persiste en `CodeQualitySnapshot` y se grafica en `/progress/code-quality`.

Code execution: el endpoint `POST /api/v1/execute/run` retorna **410 Gone**; toda la ejecución de código del estudiante vive en [Pyodide en Web Worker](frontend/src/sandbox/pyodideWorker.ts) en el cliente. `POST /api/v1/execute/validate` solo corre `ast.parse` para detectar errores de sintaxis sin ejecutar. El backend nunca toca código del estudiante.

**Seguridad transversal** (capa middleware): [security_headers.py](backend/app/core/security_headers.py) (HSTS/CSP/XCTO/XFO/Referrer-Policy/Permissions-Policy), [rate_limit.py](backend/app/core/rate_limit.py) (SlowAPI con `_user_or_ip` keyfunc), [logging_config.py](backend/app/core/logging_config.py) (structlog + redact_pii), [observability.py](backend/app/core/observability.py) (Sentry no-op si no hay DSN). Todos se montan en `main.py`.

LLM: [llm_provider.py](backend/app/services/llm_provider.py) abstrae Groq + OpenAI + Stub. `get_provider(settings)` despacha por `LLM_PROVIDER`. Stub se usa cuando no hay API key — devuelve `""` y deja que el caller use fallback.

ELO system: puzzles, attempts, ratings, and rank progression live in [backend/app/services/elo_service.py](backend/app/services/elo_service.py) + [backend/app/models/elo_models.py](backend/app/models/elo_models.py). Rank deltas use step tables keyed by rating range (`ELO_DELTA_TABLE`, `ELO_DELTA_TABLE_ADVANCED`). El ELO multidominio (separado por track/categoría) vive en [elo_rating_service.py](backend/app/services/elo_rating_service.py) + [code_quality_service.py](backend/app/services/code_quality_service.py) para la progresión de calidad. The tutor prompt lives in the repo-root file referenced by `TUTOR_PROMPT_FILE` (default `maestro_evaluador_de_codigo_python.txt`) and is resolved via `settings.tutor_prompt_path`.

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
- **Patrón para añadir un track/lección nuevo** (validado en Tracks 2 y 3, replica 1:1): agregar `LessonTemplate(track="track-N", category="...", ...)` con sus `ExerciseTemplate(hidden_tests=...)`; registrar la `category` en `Competencies.tsx` (`CATEGORY_LABELS` + `CATEGORY_TO_TRACK` + `TRACK_INFO`); si el track lo cierra un capstone, añadir entrada a `CAPSTONES` en `capstone_seed.py` y `TRACK_TITLES` en `core/tracks.py`. Sin migraciones ni endpoints nuevos — `/progress/track-status` y los certificados son genéricos por track.
- **Guard rail de no-leak**: cuando algo es opt-in o se oculta a la UI (`hidden_tests`, `reference_solution`, `correct_output` de un puzzle), añadir un test que verifique que los endpoints públicos NO lo exponen.
- **Gotcha dev Windows**: al levantar uvicorn local exportar `$env:PYTHONUTF8="1"` — sin eso structlog crashea al loggear contenido seedeado con Unicode en la consola cp1252. No afecta prod (Docker/Linux) ni CI.
- **No Co-Authored-By en commits** del proyecto (preferencia del usuario).
