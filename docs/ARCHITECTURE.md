# Arquitectura técnica — PyCode Platform

Documento técnico de referencia. Describe cómo está construida la plataforma, cómo fluyen los datos y qué patrones se replican al crecer. Para la guía operativa día a día ver [CLAUDE.md](../CLAUDE.md); para la visión de producto ver [PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md).

Última revisión: 2026-07 (Tracks 1-4 cerrados, Track 5 en curso). Para el esquema de datos detallado ver [DATABASE.md](DATABASE.md).

---

## 1. Visión de 10.000 pies

PyCode es un monorepo con tres piezas:

```
┌─────────────────────────┐     HTTPS /api/v1      ┌──────────────────────────┐
│  Frontend (React/Vite)  │ ─────────────────────▶ │  Backend (FastAPI async) │
│  Vercel Hobby           │ ◀───────────────────── │  Render Free (Docker)    │
│                         │     WSS /ws/tutor       │                          │
│  ┌───────────────────┐  │                         │   SQLAlchemy 2.0 async   │
│  │ Pyodide Web Worker│  │                         └────────────┬─────────────┘
│  │ (ejecuta el código│  │                                      │ asyncpg + RLS
│  │  del estudiante)  │  │                         ┌────────────▼─────────────┐
│  └───────────────────┘  │                         │  Postgres (Supabase)     │
└─────────────────────────┘                         └──────────────────────────┘
```

**Principio de diseño central**: el backend **nunca ejecuta código del estudiante**. Toda la ejecución vive en Pyodide dentro de un Web Worker en el navegador. El backend solo persiste contenido, progreso, ratings y evaluaciones. Esto elimina toda una clase de riesgos (sandbox escapes, DoS por código malicioso) y permite correr en un free tier sin workers de ejecución.

---

## 2. Backend

FastAPI + SQLAlchemy 2.0 async + asyncpg. Entry point: [`backend/app/main.py`](../backend/app/main.py).

### 2.1 Ciclo de vida (`lifespan`)

- **No crea tablas** — el schema lo gestiona Alembic (`alembic upgrade head` corre en el `CMD` del Dockerfile y en el `conftest` de tests).
- Seedea (todo idempotente "if empty"): puzzles ELO, interview puzzles, generated bank, retos curados, external challenges, datasets, capstones y lecciones-con-ejercicios de los tres tracks.
- Todo modelo nuevo debe importarse en `main.py` **y** en `alembic/env.py` para que `Base.metadata` lo conozca.

### 2.2 Capas

| Capa | Ubicación | Responsabilidad |
|---|---|---|
| API | `app/api/v1/endpoints/` | Routers FastAPI, validación Pydantic, auth |
| Servicios | `app/services/` | Lógica de negocio, seeders, LLM, ELO, calidad |
| Modelos | `app/models/` | Tablas SQLAlchemy |
| Schemas | `app/schemas/` | DTOs Pydantic (entrada/salida) |
| Core | `app/core/` | Config, DB engine, seguridad, rate limit, logging, tracks |
| WebSockets | `app/websockets/` | `/ws/tutor` (Q&A). `/ws/code` deprecado |

### 2.3 Base de datos y migraciones

- Dev/test default: `sqlite+aiosqlite`. Prod: `postgresql+asyncpg://...?sslmode=require`.
- `_get_engine_args(db_url, environment)` en [`core/database.py`](../backend/app/core/database.py) **rechaza SQLite si `ENVIRONMENT=production`** — sin fallback silencioso.
- Migraciones Alembic `0001`→`0014` (monotónicas):

| # | Migración | Contenido |
|---|---|---|
| 0001 | initial_schema | Tablas base (users, lessons, exercises, progress, puzzles, ...) |
| 0002 | refresh_tokens | Tabla de refresh tokens |
| 0003 | cascade_user_fks | `ON DELETE CASCADE` en FKs a users (Postgres) |
| 0004 | enable_rls_per_user_tables | Políticas RLS (Postgres-only) |
| 0005 | code_evaluations | Evaluaciones del tutor evaluador |
| 0006 | challenge_completions | Auto-marcado de retos |
| 0007 | exercise_hidden_tests | Columna `hidden_tests` JSON |
| 0008 | capstones | `capstones` + `capstone_submissions` (RLS) |
| 0009 | certificates | Certificados (tabla pública, sin RLS) |
| 0010 | elo_ratings | ELO multidominio `EloRating(user, domain, scope)` |
| 0011 | challenge_completion_elo_delta | Columna `elo_delta` para revertir |
| 0012 | code_quality_snapshots | Snapshots de calidad de código (RLS) |
| 0013 | lesson_track | Columna `lessons.track` (habilita multi-track) |
| 0014 | datasets | Datasets seedeables servidos como CSV |

- **Regla DDL Postgres-only** (RLS, constraints sin nombre estable): empezar el `upgrade()` con
  ```python
  if op.get_bind().dialect.name != "postgresql":
      return
  ```
  para que sea no-op en SQLite (los tests usan SQLite).
- **Columna nueva sobre tabla existente**: usar `batch_alter_table` para que la migración sea no-op-safe en SQLite.

### 2.4 Row-Level Security (RLS)

Las tablas por-usuario tienen políticas RLS que filtran por `current_setting('app.current_user_id')`. El backend setea ese valor por request/sesión de DB. Los endpoints **además** filtran por `user_id` en la query (RLS es la segunda línea de defensa, no la única). Tests cross-user verifican que un usuario no puede leer datos de otro.

Tablas **públicas sin RLS** por diseño: `certificates` (credencial compartible vía código de verificación), `capstones`/`lessons` (contenido definicional).

### 2.5 API surface (`/api/v1`)

| Router | Endpoints clave |
|---|---|
| `auth` | login, register, refresh (rotation), logout (revoca jti) |
| `users` | me, me/export (GDPR), DELETE me (GDPR) |
| `lessons` | list, `/{id}` (con `selectinload(exercises)`) |
| `exercises` | por lección, `/{id}/hidden-tests` (auth, no leak), `/{id}/evaluations` |
| `execute` | run → **410 Gone**, validate → `ast.parse` (sin ejecutar) |
| `tutor` | `POST /evaluate` (REST atómico) + WS `/ws/tutor` (Q&A) |
| `progress` | competencies, track-status, code-quality |
| `elo` | attempt, ratings, history, puzzle-of-the-day (público) |
| `challenges` | list, detail (sin `reference_solution`), complete/uncomplete |
| `capstones` | list, `/{slug}` detail (sin hidden_tests), submissions |
| `certificates` | issue (gate 403), download (PDF), verify/{code} (público) |
| `datasets` | `/{slug}/csv` |
| `ai` | `/complete` — proxy LLM (Track 5): auth + rate limit + tope de tokens |

### 2.6 Servicios notables

- **`llm_provider.py`** — abstrae Groq + OpenAI + Stub. `get_provider(settings)` despacha por `LLM_PROVIDER`. Stub devuelve `""` y deja al caller usar fallback (sin API key el sistema sigue funcionando de forma degradada).
- **`elo_service.py`** — ELO clásico: attempts, rank progression con `ELO_DELTA_TABLE` / `ELO_DELTA_TABLE_ADVANCED` por rango.
- **`elo_rating_service.py`** — ELO multidominio: `get_or_init_rating(user, domain, scope)` con lazy-init desde el ELO global (continuidad), `apply_result_to_rating`.
- **`code_quality_service.py`** — `analyze_code` calcula un `static_score` 0-100 con AST **sin ejecutar** (complejidad ciclomática, longitud de funciones, anidamiento, docstrings, líneas largas).
- **`certificate_pdf.py`** — render con reportlab (A4 apaisado, marco, código de verificación, fecha ES sin locale).
- **Seeders** (`lesson_seed`, `capstone_seed`, `dataset_seed`, `curated_retos`, `puzzle_seed`, `generated_bank`) — idempotentes por clave natural (title/slug).

---

## 3. Frontend

React 18 + TypeScript + Vite 5 + Tailwind + Zustand.

- **Proxy dev**: Vite proxea `/api` y `/ws` a `localhost:8000` — el código llama rutas relativas, nunca `http://localhost:8000`.
- **Estado global**: un único store Zustand [`authStore.ts`](../frontend/src/stores/authStore.ts) con `accessToken` + `refreshToken` + `user`.
- **API layer**: [`services/api.ts`](../frontend/src/services/api.ts) (fetch nativo). Interceptor: ante un 401 intenta `POST /auth/refresh` y reintenta el request original; si falla, limpia tokens y redirige a `/login`. Opción `skipAuth` para endpoints públicos (puzzle del día, verify certificado).
- **Producción**: `TutorChat.tsx` conecta directo a `wss://pycode-backend.onrender.com/ws/tutor` cuando `import.meta.env.PROD` (Vercel Hobby no proxea WS de forma confiable).

### 3.1 Sandbox Pyodide

Vive en [`frontend/src/sandbox/`](../frontend/src/sandbox/):

- `pyodideWorker.ts` corre como **Web Worker** (cargado via `new URL(..., import.meta.url)` con `worker.format='es'`).
- `PyodideSandbox.ts` lo envuelve con **Comlink** (llamadas async transparentes al worker).
- El runtime Pyodide se carga lazy desde `cdn.jsdelivr.net` (whitelisted en CSP).
- **Autocarga de paquetes**: `loadPackagesFromImports(allCode)` detecta imports y descarga numpy/pandas/scipy/sklearn del CDN de Pyodide bajo demanda (primera carga ~10-30s).
- **`runTests`**: cada hidden_test corre en namespace fresco (`py.toPy({})`), con timeout por test y error truncado. La UI **nunca** renderiza el código del test, solo `name` + verdict ✓/✗.
- **`runCapstoneTests`**: escribe múltiples archivos al FS virtual y agrega el dir al `sys.path` para evaluar proyectos multi-archivo.
- **matplotlib**: se renderiza como MIME `image/png` en el editor.

---

## 4. Modelo de dominio educativo

```
Track (track-1..6)
 └── Lesson (category, order, track)
      └── Exercise (hidden_tests JSON)          ← evaluado en Pyodide
 └── Capstone (por track)
      └── CapstoneSubmission (uno por user)      ← multi-archivo en Pyodide
      └── desbloquea → Certificate (verify público)

Puzzle (ELO) ── PuzzleAttempt ── EloRating(domain, scope)
CodingChallenge ── ChallengeCompletion (elo_delta)
CodeEvaluation (tutor evaluador) ── CodeQualitySnapshot (logic+general+static)
Dataset (CSV servido a Pyodide)
```

### 4.1 El patrón multi-track (lo que se replica)

Añadir contenido a cualquier track **no requiere migraciones ni endpoints nuevos**. Validado end-to-end en Tracks 2 y 3:

1. **Lección**: agregar `LessonTemplate(track="track-N", category="...", exercises=[ExerciseTemplate(hidden_tests=...)])`. Seeder idempotente por title.
2. **Competencias**: registrar la `category` en `Competencies.tsx` (`CATEGORY_LABELS` + `CATEGORY_TO_TRACK` + `TRACK_INFO`).
3. **Dataset** (opcional): entrada en `dataset_seed.py`; se consume con `pycode.fetch_dataset_csv(slug)`.
4. **Capstone** (cierra el track): entrada en `CAPSTONES` (`slug`, `track`, `starter_files`, `hidden_tests`).
5. **Certificado**: automático — `POST /certificates/{track}/issue` es genérico; añadir el título a `TRACK_TITLES` en `core/tracks.py`.
6. **Track-status**: automático — `/progress/track-status` itera `TRACK_TITLES`, filtra por `Lesson.track`, elige el capstone canónico y skipea tracks vacíos.

**Verificación de datos**: los valores esperados de cada `hidden_test` (numpy/pandas/sklearn) se fijan ejecutando el snippet con las librerías reales localmente antes de commitear, con un test guard-rail anti-drift de versión.

---

## 5. Sistema ELO

Dos capas coexisten (backward-compatible):

- **ELO global/clásico** (`elo_service.py`): rating overall + rank progression por rangos.
- **ELO multidominio** (`elo_rating_service.py`): `EloRating(user, domain, scope)` da rating separado por:
  - `puzzle:<category>` (Python, NumPy, Pandas, Interview, ...)
  - `challenge:<dificultad>` (easy 850 / medium 1200 / hard 1550 nominal)
  
  Lazy-init desde el ELO global para no romper la continuidad. `GET /elo/ratings` devuelve tracks hoja + agregados por dominio + overall. UI: `EloTracks.tsx` en el Dashboard.

El ELO de retos por auto-marcado es *gameable* por diseño (decisión de producto aceptada); `uncomplete` revierte el delta exacto vía la columna `challenge_completions.elo_delta`.

---

## 6. Tutor IA — dos roles

| | Evaluador | Q&A |
|---|---|---|
| Transporte | REST `POST /tutor/evaluate` | WS `/ws/tutor` |
| Naturaleza | Atómico, sin historial | Multi-turno |
| Contexto | Código del ejercicio (opt-in, botón "Evaluar") | Pregunta libre, sin auto-load del editor |
| Salida | `CodeEvaluation` + `CodeQualitySnapshot` | Respuesta socrática |

El system prompt del evaluador vive en el archivo raíz `maestro_evaluador_de_codigo_python.txt` (`TUTOR_PROMPT_FILE`, resuelto vía `settings.tutor_prompt_path`).

---

## 7. Seguridad transversal

Middleware montado en `main.py`:

- **`security_headers.py`** — HSTS, CSP (whitelist `cdn.jsdelivr.net` para Pyodide), X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy.
- **`rate_limit.py`** — SlowAPI con keyfunc `_user_or_ip` (por user_id autenticado, si no por IP). Contadores en memoria del proceso (un redeploy los resetea).
- **`logging_config.py`** — structlog con `redact_pii` (JWT, API keys, emails).
- **`observability.py`** — Sentry con scrubbing; no-op si no hay DSN.
- **`check_no_sqli.py`** — lint que rechaza `text(f"...")` (corre en CI).
- **Auth**: JWT con refresh token rotation; `logout` revoca el `jti`. GDPR: export + delete.

---

## 8. Notas operativas (prod)

- **Cold start Render free**: el contenedor duerme tras 15 min idle; UptimeRobot pingea `/health` cada 5 min. Sin él, las primeras llamadas tras idle tardan 30-60s o dan 502.
- **CORS_ORIGINS** en Render incluye el dominio Vercel exacto. Si cambia el dominio, actualizar y redesplegar.
- **Supabase free se pausa** tras ~7 días sin actividad de DB y tumba el deploy con "tenant/user not found"; se restaura con el MCP de Supabase (sin tocar código). **Mitigación implementada**: el workflow `.github/workflows/keepalive-db.yml` (cron cada 4h) golpea `GET /health/db` (que hace `SELECT 1`), generando actividad real de DB. Nota diagnóstica: si Render reporta "deploy failed" pero **CI está verde**, sospechar Supabase pausada antes que el código/deps.
- **Proxy LLM y GROQ_API_KEY**: `POST /api/v1/ai/complete` (Track 5) llama al LLM real solo si `GROQ_API_KEY` está seteada en Render; sin key cae al `StubProvider` (respuesta placeholder determinista). El helper `pycode.llm_complete` del worker Pyodide incluye el token de sesión (empujado desde el hilo principal, ya que el worker no lee localStorage).
- **Dev Windows**: exportar `$env:PYTHONUTF8="1"` antes de `uvicorn` — sin eso structlog crashea al loggear contenido Unicode en consola cp1252. No afecta prod ni CI (Linux UTF-8).

---

## 9. Testing y CI

- **Backend**: 161 tests (pytest-asyncio mode=auto). El `conftest` aplica `alembic upgrade head` sobre SQLite y resetea SlowAPI. Guard rails de no-leak para todo lo oculto a la UI. El contenido de lecciones/capstones se verifica aparte con solución de referencia (numpy/sklearn local) porque sus `hidden_tests` corren en Pyodide, no en pytest.
- **Frontend**: vitest (unit) + Playwright (E2E, Chromium headless) para flujos de capstone/certificado.
- **CI** (`.github/workflows/ci.yml`): backend-tests, backend-lint (black + flake8 + mypy + check_no_sqli), frontend-build, audit (pip-audit + npm audit). Dependabot semanal.

---

## 10. Roadmap técnico

**Cerrado**: Fase 0, Fase 1, Track 1 (Python), Track 2 (Data Science), Track 3 (ML Clásico), Track 4 (Deep Learning). **En curso**: Track 5 (AI Engineering) — AI 1-3 (embeddings, chunking/indexación, LLM real + prompt RAG). **Pendiente**: resto de Track 5 (RAG end-to-end, agentes, evals), Track 6 (MLOps).

Dos decisiones arquitectónicas resueltas en Tracks 4-5:
- **Track 4 (Deep Learning)**: se enseñó **desde cero en numpy** (neurona → backprop → MLP), que corre en Pyodide sin infra nueva. **PyTorch real** (nn.Module/GPU/CNNs) se **difirió** a un futuro Track 4b — requeriría ejecución fuera de Pyodide (GPU remota vs Colab), la decisión de infra/costo que sigue pendiente.
- **Track 5 (AI Engineering)**: el retrieval de RAG se construye **en numpy** (determinista, testeable); la generación con LLM usa un **proxy backend** (`/api/v1/ai/complete`) que reutiliza el LLM provider existente — barato, sin GPU, sin exponer API keys. Las lecciones de generación testean la **lógica alrededor** del LLM (prompts, parseo), no su salida no-determinista.

El framework multi-track (§4.1) absorbió Tracks 3-5 sin migraciones ni cambios estructurales.
