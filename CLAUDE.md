# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

PyCode Platform — learning platform for Python with Monaco editor, sandboxed code execution, a Socratic AI tutor, and a Finxter-inspired ELO puzzle progression system. 

**Current Status (Fase 1.0)**: ✅ Core features complete
- 25 lecciones con temario completo Python (principiante → avanzado)
- 64 ejercicios progresivos (easy/medium/hard) con starters y hints
- Autenticación JWT + editor de código en vivo
- Tutor IA Socrático + seguimiento de progreso por usuario

See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for the vision and [PYCODE_SPEC.md](PYCODE_SPEC.md) for the phased implementation spec (which is the source of truth for pending work).

## Common commands

Backend (`backend/`, runs via `.venv311`):
```bash
# Activate venv (Windows): backend/.venv311/Scripts/activate
cd backend && uvicorn app.main:app --reload --port 8000
pip install -r ../requirements.txt
pytest                        # repo uses pytest-asyncio
pytest path/to/test.py::name  # single test
black . && flake8 . && mypy .
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

Entry point: [backend/app/main.py](backend/app/main.py). The `lifespan` handler is doing heavy lifting — on each startup it:
1. Runs `Base.metadata.create_all` (no Alembic yet — Fase 1.1 of the spec calls for it).
2. Calls `bootstrap_elo_schema` ([schema_bootstrap.py](backend/app/services/schema_bootstrap.py)) which ALTERs `user_profiles`/`user_progress` to add missing ELO columns — this is a stopgap for schema drift against existing SQLite files.
3. Seeds puzzles, interview puzzles, generated puzzles/challenges, external challenges, and lessons-with-exercises — all idempotent "if empty" seeders. Any new model must be imported in `main.py` before `create_all` or its table won't be created.

DB: defaults to `sqlite+aiosqlite:///./pycode.db` (dev); production targets `postgresql+asyncpg`. Engine selection lives in [backend/app/core/database.py](backend/app/core/database.py) and branches on the URL prefix — keep that branching intact when changing DB config.

API surface is versioned at `/api/v1` via [backend/app/api/v1/router.py](backend/app/api/v1/router.py), mounting: `auth`, `users`, `lessons`, `exercises`, `execute`, `tutor`, `progress`, `elo`, `challenges`. WebSockets are mounted outside the versioned prefix at `/ws/code` and `/ws/tutor`.

**Lessons & Exercises**: [backend/app/services/lesson_content.py](backend/app/services/lesson_content.py) contains 25 `LessonTemplate` with Spanish content + 64 `ExerciseTemplate` (3 per lesson on average, progressive difficulty). Seeded via [backend/app/services/lesson_seed.py](backend/app/services/lesson_seed.py) on startup (idempotent upsert by title). **Known issue fixed**: GET `/{lesson_id}` now uses `selectinload(Lesson.exercises)` to avoid lazy-load errors in async context.

Code execution: [backend/app/services/docker_executor.py](backend/app/services/docker_executor.py) is the **subprocess fallback** used in dev on Windows — despite the class name `DockerCodeExecutor`, it shells out to local `python`. The real Docker sandbox with memory/CPU/network limits is Fase 1.2 of the spec and has not been implemented. Do not treat current execution as safe for untrusted code.

ELO system: puzzles, attempts, ratings, and rank progression live in [backend/app/services/elo_service.py](backend/app/services/elo_service.py) + [backend/app/models/elo_models.py](backend/app/models/elo_models.py). Rank deltas use step tables keyed by rating range (`ELO_DELTA_TABLE`, `ELO_DELTA_TABLE_ADVANCED`). The tutor prompt lives in the repo-root file referenced by `TUTOR_PROMPT_FILE` (default `maestro_evaluador_de_codigo_python.txt`) and is resolved via `settings.tutor_prompt_path`.

### Frontend (React + TS + Vite + Tailwind + Zustand)

Vite dev server proxies `/api` and `/ws` to `localhost:8000` ([vite.config.ts](frontend/vite.config.ts)) — frontend code should call relative paths, not absolute `http://localhost:8000`. `@/*` alias points to `src/`.

Global state: a single Zustand store [frontend/src/stores/authStore.ts](frontend/src/stores/authStore.ts) for auth; no ELO store yet in `src/` (the one in `Elo_pycode/eloStore.ts` is staged, not imported). API calls go through [frontend/src/services/api.ts](frontend/src/services/api.ts) (axios).

## Conventions

- Language of user-facing strings, commit messages, docs, and most code comments is **Spanish**. Keep that tone when editing UI copy or writing new docs.
- Seeders are idempotent and run on every startup — when adding one, follow the "if empty" pattern already in `puzzle_seed.py` / `lesson_seed.py` and register it inside the `lifespan` block.
- No Alembic yet: schema changes rely on `create_all` + the `bootstrap_elo_schema` shim. If you add columns to existing tables, extend that shim or implement Alembic (Fase 1.1) rather than assuming tables get recreated.
- The `Elo_pycode/` folder is a **staging area**, not dead code — files there are meant to be integrated into `backend/app/...` and `frontend/src/...` per Fase 2 of the spec. Check both locations before assuming something is missing.
- Async SQLAlchemy: Always use eager loading (`selectinload`, `joinedload`) for relationships accessed in endpoints — lazy loading fails in async context (MissingGreenlet error).
