# PyCode Platform

Plataforma de aprendizaje que lleva de **Fundamentos → Python → Data Science → Machine Learning → Deep Learning → AI Engineering → MLOps**, con tutor IA socrático, sandbox de ejecución en el navegador (Pyodide), sistema ELO de puzzles estilo Finxter y certificados verificables.

> **Norte estratégico**: PyCode lleva al estudiante **de cero a ingeniería de ML/AI**. Se entra sin saber programar (Track 0: fundamentos, pseudocódigo, algoritmos y diagramas de flujo) y no se termina en Python básico: Track 1 es la rampa hacia Data Science, ML, Deep Learning, AI Engineering y MLOps. El diferenciador es el pipeline completo, con tutor socrático y ELO transversal.

## Estado

| Fase / Track | Estado | Contenido |
|---|---|---|
| **Fase 0** — fundamentos + seguridad | ✅ Cerrada (tag `fase-0-complete`) | Postgres+Alembic+RLS, Pyodide, JWT+GDPR, seguridad transversal, deploy gratis |
| **Fase 1** — pulido Track 1 + ELO | ✅ Cerrada | Tutor evaluador+Q&A, tests ocultos, ELO multidominio, calidad de código, certificados PDF |
| **Track 0** — Fundamentos de programación | ⏳ En diseño | Pseudocódigo, trazas de ejecución, algoritmos, estructuras elementales, diagramas de flujo. Requiere tipos de ejercicio **no ejecutables** (ver abajo) |
| **Track 1** — Python | ✅ Cerrado | 10 lecciones · capstone `CLI de ventas` |
| **Track 2** — Data Science | ✅ Cerrado | 11 lecciones (NumPy/Pandas/Viz/EDA/Stats) · capstone `EDA cafecito` |
| **Track 3** — ML Clásico | ✅ Cerrado | 11 lecciones sklearn · capstone `Diagnóstico ML` |
| **Track 4** — Deep Learning | ✅ Cerrado | 5 lecciones **numpy puro** (backprop→MLP→XOR) · capstone `Red desde cero`. PyTorch real diferido |
| **Track 5** — AI Engineering | 🚧 En curso | AI 1-3: embeddings, RAG retriever, LLM real vía proxy. Faltan RAG e2e/agentes/evals/capstone |
| **Track 6** — MLOps | ⏳ Pendiente | Producción |

**En números**: 40 lecciones · 108 ejercicios (la mayoría con `hidden_tests`) · 100 puzzles ELO curados · 10 retos DS/ML · 4 capstones · 3 datasets · migraciones 0001-0014 · 166 tests backend. Esquema de datos: **[docs/DATABASE.md](docs/DATABASE.md)**.

## Rampa de entrada

Track 0 **no es un peaje obligatorio**. Un alumno que ya programa en otro lenguaje no debe recorrer once lecciones de pseudocódigo para llegar a Pandas. Un diagnóstico corto (trazas y bucles) recomienda punto de entrada — Track 0 o Track 1 — pero no bloquea ninguno de los dos.

Track 0 rompe el supuesto central de validación del resto de la plataforma: sus ejercicios (trazas, ordenar pasos, hallar el error, completar un diagrama) **no se ejecutan en Pyodide**. Se validan de forma determinista en el cliente y emiten el **mismo** evento de completitud que un ejercicio de Python, para que XP, progreso, ELO y competencias sigan siendo un solo camino y no dos.

## Producción

- **Frontend**: https://pycode-platform.vercel.app (Vercel Hobby)
- **Backend**: https://pycode-backend.onrender.com (Render Free, Docker)
- **DB**: Supabase Postgres (sa-east-1, RLS habilitada)
- **Watchdog**: UptimeRobot ping `/health` cada 5 min (cold start de Render) + workflow `keepalive-db.yml` (cron 4h → `/health/db`, evita que Supabase free se pause por inactividad)

## Características

- **Editor Monaco** con tema/fuente configurables, descarga de script, copia al portapapeles.
- **Pyodide en Web Worker**: el código del estudiante se ejecuta en el navegador con Comlink + timeout duro. El backend nunca lo ejecuta (`/api/v1/execute/run` retorna 410; `/validate` solo hace `ast.parse`). numpy/pandas/scipy/sklearn/matplotlib autocargan bajo demanda.
- **Tutor IA Socrático** con dos roles separados: **evaluador de código** (REST atómico) y **Q&A** (WebSocket multi-turno). Provider abstraction: Groq (default) → OpenAI fallback → Stub determinístico si no hay API key.
- **Proxy LLM para AI Engineering** (Track 5): `POST /api/v1/ai/complete` deja que el código del alumno (en Pyodide) llame a un LLM real vía backend — auth + rate limit + tope de tokens, sin exponer API keys. Helper `pycode.llm_complete()` en el editor.
- **Tests ocultos por ejercicio**: `hidden_tests` que corren en Pyodide en namespace fresco, sin exponerse a la UI. Es el patrón base de validación replicado en todos los tracks de código.
- **Sistema ELO multidominio**: rating separado por actividad y categoría temática (`puzzle:<category>`, `challenge:<dificultad>`), con lazy-init desde el ELO global. Banco de 100 puzzles curados + puzzle del día público.
- **Progresión de calidad de código**: `static_score` con AST (sin ejecutar) + scores logic/general del evaluador LLM, persistidos y graficados en el tiempo.
- **Capstones y certificados**: proyectos multi-archivo evaluados en Pyodide; aprobarlos desbloquea un certificado PDF con código de verificación **público**.
- **Auth JWT** con refresh token rotation y `/auth/logout` que revoca el `jti`. **GDPR**: `DELETE /users/me` + `GET /users/me/export`.
- **Seguridad transversal**: HSTS/CSP/XCTO/XFO/Referrer-Policy/Permissions-Policy, CORS whitelist, rate limiting por user_id, structlog con redaction de PII, Sentry con scrubbing.
- **Postgres + Alembic + RLS** por tabla con `current_setting('app.current_user_id')`.
- **CI**: pytest + black + flake8 + lint anti-SQLi, pip-audit + npm audit, Dependabot semanal.

## Stack

**Backend**: FastAPI + SQLAlchemy 2.0 async + asyncpg · Postgres (Supabase en prod) + Alembic · python-jose (JWT) + bcrypt · SlowAPI (rate limit) · structlog + sentry-sdk · Groq SDK + OpenAI SDK · reportlab (PDF) · pytest + pytest-asyncio + httpx + Playwright (E2E).

**Frontend**: React 18 + TypeScript + Vite 5 · TailwindCSS · Monaco Editor · Pyodide + Comlink (Web Worker) · Zustand · Recharts · `fetch` nativo con interceptor de refresh (no axios).

## Requisitos

- Python 3.11 · Node.js 20 · Postgres 16 local (opcional; los tests corren contra SQLite, pero Postgres es necesario para autogenerar migraciones y validar RLS).

## Instalación

### Backend

```bash
cd backend
python -m venv .venv311
.venv311\Scripts\activate            # Windows; en Unix: source .venv311/bin/activate
pip install -r ../requirements.txt   # o ../requirements.lock para versiones pinned

cp ../.env.example ../.env            # editar con tus credenciales

alembic upgrade head                 # obligatorio antes de levantar — crea las tablas
# Windows: exportar UTF-8 para que structlog no crashee al seedear contenido Unicode
$env:PYTHONUTF8="1"                  # (PowerShell)
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev   # vite en localhost:5173 con proxy /api y /ws hacia :8000
```

App en `http://localhost:5173`. Full stack alternativo: `docker-compose up`.

## Comandos útiles

```bash
# Backend
cd backend
pytest                                     # conftest aplica alembic upgrade + resetea SlowAPI
pytest path/to/test.py::name               # un test
black . && flake8 . && mypy .
python scripts/check_no_sqli.py            # lint anti-SQL injection (también en CI)
alembic revision --autogenerate -m "descripcion"   # contra Postgres limpio

# Frontend
cd frontend
npm run build       # tsc + vite build (errores de TS fallan el build)
npm run lint        # eslint --max-warnings 0
npm run test        # vitest
npm run test:e2e    # Playwright (Chromium headless)
```

Las migraciones se renombran a `NNNN_descripcion.py` con orden monotónico. Las que tocan DDL Postgres-only (RLS) empiezan con:

```python
if op.get_bind().dialect.name != "postgresql":
    return
```

para ser no-op en SQLite (los tests usan SQLite).

## Estructura del repo

```
backend/
├── app/
│   ├── api/v1/endpoints/    # auth, users, lessons, exercises, execute, tutor, progress,
│   │                          elo, challenges, capstones, certificates, datasets, ai
│   ├── core/                # config, database, security_headers, rate_limit,
│   │                          logging_config, observability, tracks
│   ├── models/              # user, learning, elo_models, refresh_token, challenge,
│   │                          code_evaluation, capstone, certificate, code_quality, dataset
│   ├── services/            # ai_tutor, llm_provider, lesson_content, lesson_seed,
│   │                          elo_service, elo_rating_service, code_quality_service,
│   │                          capstone_seed, certificate_pdf, dataset_seed, curated_retos, ...
│   └── websockets/          # tutor_chat (/ws/tutor); /ws/code deprecado
├── alembic/versions/        # 0001 → 0014
├── scripts/check_no_sqli.py
├── tests/                   # 166 tests
└── Dockerfile               # alembic upgrade head + uvicorn

frontend/
├── src/
│   ├── pages/               # Dashboard, Lessons, LessonDetail, CodeEditor, Puzzles,
│   │                          InterviewProblems, Challenges, Competencies, CapstoneDetail,
│   │                          CertificateVerify, TutorChat, Home, Login, Register
│   ├── components/          # EloResultModal, EloTracks, CodeQualityPanel, PuzzleOfTheDay, ...
│   ├── sandbox/             # pyodideWorker, PyodideSandbox (Comlink)
│   ├── services/api.ts      # fetch + interceptor de refresh
│   └── stores/authStore.ts
├── e2e/                     # Playwright specs
└── vite.config.ts

docs/
├── ARCHITECTURE.md          # diseño técnico (empezar aquí)
├── DATABASE.md              # esquema de base de datos descrito
├── DEPLOY.md                # Render + Vercel + Supabase + UptimeRobot
└── superpowers/specs/       # specs por fase

.github/workflows/
├── ci.yml                   # backend-tests, backend-lint, frontend-build, audit
└── keepalive-db.yml         # cron 4h → /health/db (evita pausa de Supabase)
```

## Documentación

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — diseño técnico: capas, flujo de datos, modelos, el patrón multi-track, sandbox, ELO, seguridad.
- **[docs/DATABASE.md](docs/DATABASE.md)** — esquema de base de datos: 22 tablas por dominio, columnas, relaciones, RLS y migraciones.
- **[docs/TRACK_0.md](docs/TRACK_0.md)** — Track 0: temario, tipos de ejercicio no ejecutables y convención de pseudocódigo.
- **[CLAUDE.md](CLAUDE.md)** — guía operativa para agentes/contribuidores.
- **[docs/DEPLOY.md](docs/DEPLOY.md)** — despliegue Render + Vercel + Supabase.
- `docs/historico/` — `PYCODE_SPEC.md` y `PLAN_COMPLETO.md`: diseño inicial **descartado** (ejecución en Docker server-side, Kubernetes, microservicios). Se conservan como registro; no son fuente de verdad.

## Convenciones

- Idioma de UI / docs / commits / comentarios: **español**.
- Commits **sin línea Co-Authored-By**.
- **El backend nunca ejecuta código del alumno.** La ejecución vive en Pyodide, en el navegador. No reintroducir sandbox Docker ni endpoints de ejecución server-side.
- Schema changes pasan por Alembic (no `create_all`); FKs hacia `users.id` con `ondelete="CASCADE"`; DDL Postgres-only con guard de dialecto.
- Async SQLAlchemy: usar `selectinload`/`joinedload` para relaciones accedidas en endpoints.
- Añadir lección/track de **código** = agregar `LessonTemplate(track=..., category=...)` + registrar la categoría en `Competencies.tsx`. Sin migración ni endpoints nuevos. Track 0 es la excepción: introduce tipos de ejercicio no ejecutables y sí toca modelo (ver `docs/TRACK_0.md`).
- Guard rail de no-leak: lo oculto a la UI (`hidden_tests`, `reference_solution`, y la solución de cualquier ejercicio no ejecutable) debe tener un test que verifique que no se expone.

## Licencia

MIT — ver [LICENSE](LICENSE).
