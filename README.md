# PyCode Platform

Plataforma de aprendizaje de Python con tutor IA socrático, sandbox de ejecución en el navegador (Pyodide) y seguimiento de progreso por usuario.

## Estado

**Fase 0 v2 (fundamentos + seguridad base): 27/30 tasks.** Lo único que falta para cerrar Fase 0 es el smoke test contra el entorno staging real (Render + Vercel + Supabase + UptimeRobot). Detalle en [`docs/superpowers/plans/fase-0-checklist.md`](docs/superpowers/plans/fase-0-checklist.md).

## Características

- **Editor Monaco** con tema/fuente configurables, descarga de script, copia al portapapeles.
- **Pyodide en Web Worker**: el código del estudiante se ejecuta en el navegador con Comlink + timeout duro de 30s. El backend nunca lo ejecuta (`/api/v1/execute/run` retorna 410).
- **Tutor IA Socrático** con provider abstraction: Groq (default `llama-3.3-70b-versatile`) → OpenAI fallback → Stub determinístico si no hay API key.
- **25 lecciones + 64 ejercicios** progresivos en español.
- **Auth JWT** con refresh token rotation y `/auth/logout` que revoca el `jti`.
- **GDPR**: `DELETE /api/v1/users/me` purga la cuenta y datos relacionados; `GET /api/v1/users/me/export` retorna toda la data del usuario en JSON.
- **Seguridad transversal**: HSTS/CSP/XCTO/XFO/Referrer-Policy/Permissions-Policy, CORS whitelist (sin wildcard en prod), rate limiting por user_id (login 5/min, register 3/h, tutor 50/día), structlog con redaction de PII (JWT, API keys, emails), Sentry con scrubbing.
- **Postgres + Alembic + RLS** habilitada por tabla con `current_setting('app.current_user_id')`.
- **CI**: pytest + black + flake8 + lint anti-SQLi (`text(f"...")` rechazado), pip-audit + npm audit, Dependabot semanal.

## Stack

### Backend
- FastAPI 0.104 + SQLAlchemy 2.0 async + asyncpg
- Postgres 16 (Supabase en prod) + Alembic para migraciones
- python-jose para JWT, bcrypt para passwords
- SlowAPI para rate limiting
- structlog + sentry-sdk
- Groq SDK + OpenAI SDK
- pytest + pytest-asyncio + httpx

### Frontend
- React 18 + TypeScript + Vite 5
- TailwindCSS
- Monaco Editor
- Pyodide 0.26 + Comlink (Web Worker)
- Zustand para state
- `fetch` nativo con interceptor de refresh automático (no axios)

## Requisitos para desarrollo

- Python 3.11
- Node.js 20
- Postgres 16 local (opcional para tests; los tests también corren contra SQLite). Necesario para autogenerar migraciones y validar políticas RLS.

## Instalación

### Backend

```bash
cd backend
python -m venv .venv311
.venv311\Scripts\activate            # Windows; en Unix: source .venv311/bin/activate
pip install -r ../requirements.txt   # o ../requirements.lock para versiones pinned

cp ../.env.example ../.env
# editar .env con tus credenciales

alembic upgrade head                 # obligatorio antes de levantar — crea las tablas
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev   # vite en localhost:5173 con proxy /api y /ws hacia :8000
```

App disponible en `http://localhost:5173` (la API se sirve via proxy de vite).

## Comandos útiles

### Tests y lint backend

```bash
cd backend
pytest                                     # 37 tests, conftest aplica alembic upgrade automáticamente
pytest path/to/test.py::name               # un test
black . && flake8 .                        # formato + lint
python scripts/check_no_sqli.py            # lint anti-SQL injection (corre también en CI)
```

### Migraciones

```bash
cd backend
alembic upgrade head
alembic revision --autogenerate -m "descripcion"   # contra Postgres limpio
```

Renombra la migración generada a `NNNN_descripcion.py` con `revision = "NNNN"` para mantener orden monotónico. Las migraciones que tocan DDL Postgres-only (RLS, drop/create constraints) deben empezar con:

```python
bind = op.get_bind()
if bind.dialect.name != "postgresql":
    return
```

para que sean no-op en SQLite y los tests sigan pasando.

### Build frontend

```bash
cd frontend
npm run build     # tsc + vite build
npm run lint      # eslint --max-warnings 0
```

## Estructura del repo

```
backend/
├── app/
│   ├── api/v1/endpoints/        # auth, users, lessons, exercises, execute, tutor, progress, elo, challenges
│   ├── core/                    # config, database, security, security_headers, rate_limit,
│   │                              logging_config, observability
│   ├── models/                  # user, learning, elo_models, refresh_token, challenge
│   ├── schemas/                 # auth, learning
│   ├── services/                # ai_tutor, llm_provider, lesson_seed, puzzle_seed, ...
│   └── websockets/              # tutor_chat (code_execution está deprecado)
├── alembic/versions/            # 0001_initial / 0002_refresh_tokens / 0003_cascade_user_fks /
│                                  0004_enable_rls_per_user_tables
├── scripts/check_no_sqli.py     # lint anti-SQLi
├── tests/                       # 37 tests
├── Dockerfile                   # python:3.11-slim, alembic upgrade head + uvicorn
└── alembic.ini

frontend/
├── src/
│   ├── pages/CodeEditor.tsx
│   ├── sandbox/                 # types, pyodideWorker, PyodideSandbox, index
│   ├── services/                # api (fetch interceptor), codeRunner, tutorContext
│   └── stores/authStore.ts      # accessToken + refreshToken + user
└── vite.config.ts               # alias @/, worker.format='es', proxy /api y /ws

docs/
├── DEPLOY.md                    # pasos Render + Vercel + Supabase + UptimeRobot
└── superpowers/
    ├── plans/2026-05-03-fase-0-fundamentos-seguridad.md
    ├── plans/fase-0-checklist.md
    └── specs/2026-05-03-pycode-platform-v2-design.md

render.yaml                      # blueprint Render
vercel.json                      # rewrites + headers
.github/dependabot.yml
.github/workflows/ci.yml         # backend-tests, backend-lint, frontend-build, audit
requirements.txt
requirements.lock                # pinned con pip-tools
```

## Despliegue (Fase 0)

Pasos manuales en [`docs/DEPLOY.md`](docs/DEPLOY.md):

1. **Supabase** → New Project → copiar `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`.
2. **Render** → New Blueprint → conecta el repo (lee `render.yaml`) → pega los secrets en Environment.
3. **Vercel** → Import Project → root `frontend` (lee `vercel.json` con rewrites a Render).
4. **UptimeRobot** → monitor `/health` cada 14 min para mantener Render free awake.

## Cerrar Fase 0

Solo queda Task 29 (smoke test contra staging) + Task 30 (cleanup final + tag `fase-0-complete`). Cuando los servicios estén levantados:

```bash
# 1. validar endpoints públicos del backend desplegado
curl -s https://pycode-backend.onrender.com/health
curl -s -I https://pycode-backend.onrender.com/health | grep -iE "strict-transport|content-security"

# 2. registrar usuario, login, /me, /lessons/, /exercises/lesson/1
# 3. abrir https://pycode.vercel.app y verificar:
#    - login
#    - cargar lecciones
#    - editor con Pyodide ejecuta print("hola") localmente
#    - tutor IA responde
# 4. confirmar que UptimeRobot está pingueando
```

Una vez todo verde:

```bash
git tag fase-0-complete
git push --tags
```

## Convenciones

- Idioma de UI / docs / commits / comentarios: **español**.
- Commits **sin línea Co-Authored-By**.
- Schema changes pasan por Alembic (no `create_all`); FKs hacia `users.id` con `ondelete="CASCADE"`; DDL Postgres-only con guard `if dialect.name != "postgresql": return`.
- Async SQLAlchemy: usar `selectinload`/`joinedload` para relaciones accedidas en endpoints.

## Próxima fase

Fase 1: pulido del Track 1 + sistema ELO completo. Spec en [`docs/superpowers/specs/2026-05-03-pycode-platform-v2-design.md`](docs/superpowers/specs/2026-05-03-pycode-platform-v2-design.md).

## Licencia

MIT — ver [LICENSE](LICENSE).
