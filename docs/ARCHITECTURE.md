# Arquitectura técnica — PyCode Platform

Documento técnico de referencia. Describe cómo está construida la plataforma, cómo fluyen los datos y qué patrones se replican al crecer. Para la visión de producto ver [PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md) y para el estado y las convenciones, el [README](../README.md).

Última revisión: **2026-11-03** (los siete tracks cerrados, Track 0 a Track 6; migraciones `0001`→`0017`). Para el esquema de datos detallado ver [DATABASE.md](DATABASE.md); para Track 0, [TRACK_0.md](TRACK_0.md).

---

## 1. Visión de 10.000 pies

PyCode es un monorepo con tres piezas:

```
┌─────────────────────────┐     HTTPS /api/v1      ┌──────────────────────────┐
│  Frontend (React/Vite)  │ ─────────────────────▶ │  Backend (FastAPI async) │
│  Vercel Hobby           │ ◀───────────────────── │  Render Free (Docker)    │
│                         │     WSS /ws/tutor       │                          │
│  ┌───────────────────┐  │                         │   SQLAlchemy 2.0 async   │
│  │ Pyodide Web Worker│  │                         └──────┬─────────────┬─────┘
│  │ (ejecuta el código│  │                                │ asyncpg+RLS │ HTTPS
│  │  del estudiante)  │  │                   ┌────────────▼──────┐ ┌────▼──────────────┐
│  └───────────────────┘  │                   │ Postgres (Supabase)│ │ Groq (LLM) ·      │
└─────────────────────────┘                   └────────────────────┘ │ email por API HTTP│
                                                                     └───────────────────┘
```

**Principio de diseño central**: el backend **nunca ejecuta código del estudiante**. Toda la ejecución vive en Pyodide dentro de un Web Worker en el navegador. El backend solo persiste contenido, progreso, ratings y evaluaciones, y corrige de forma determinista los ejercicios de Track 0, que no son código. Esto elimina toda una clase de riesgos (sandbox escapes, DoS por código malicioso) y permite correr en un free tier sin workers de ejecución.

Hay **dos formas de corregir** un ejercicio, y las dos desembocan en el mismo evento de completitud (§4.2):

| | Ejercicios de código (Tracks 1-6) | Ejercicios no ejecutables (Track 0) |
|---|---|---|
| Dónde se corrige | Navegador (Pyodide, `hidden_tests`) | Backend (`POST /exercises/{id}/check`) |
| Cómo | Tests en namespace fresco | `track0_service`, determinista, sin LLM |
| Qué se oculta | `hidden_tests` | `answer_key` |

---

## 2. Backend

FastAPI + SQLAlchemy 2.0 async + asyncpg. Entry point: [`backend/app/main.py`](../backend/app/main.py).

### 2.1 Ciclo de vida (`lifespan`)

- **No crea tablas** — el schema lo gestiona Alembic (`alembic upgrade head` corre en el `CMD` del Dockerfile y en el `conftest` de tests).
- Seedea (todo idempotente "if empty" o por clave natural): puzzles ELO, interview puzzles, banco generado, retos curados, external challenges, datasets, capstones y lecciones-con-ejercicios de los siete tracks.
- Todo modelo nuevo debe importarse en `main.py` **y** en `alembic/env.py` para que `Base.metadata` lo conozca.
- **Ojo**: como el lifespan siembra, arrancar contra una `DATABASE_URL` escribe en esa base. Nunca usar la de producción en local.

### 2.2 Capas

| Capa | Ubicación | Responsabilidad |
|---|---|---|
| API | `app/api/v1/endpoints/` | Routers FastAPI, validación Pydantic, auth |
| Servicios | `app/services/` | Lógica de negocio, seeders, LLM, ELO, calidad, email |
| Modelos | `app/models/` | Tablas SQLAlchemy |
| Schemas | `app/schemas/` | DTOs Pydantic (entrada/salida) |
| Core | `app/core/` | Config, DB engine, seguridad, rate limit, logging, tracks |
| WebSockets | `app/websockets/` | `/ws/tutor` (Q&A). `/ws/code` deprecado |

### 2.3 Base de datos y migraciones

- Dev/test default: `sqlite+aiosqlite`. Prod: `postgresql+asyncpg://...?sslmode=require`.
- `_get_engine_args(db_url, environment)` en [`core/database.py`](../backend/app/core/database.py) **rechaza SQLite si `ENVIRONMENT=production`** — sin fallback silencioso.
- Migraciones Alembic `0001`→`0017` (monotónicas):

| # | Migración | Contenido |
|---|---|---|
| 0001 | initial_schema | Tablas base (users, lessons, exercises, progress, puzzles, ...) |
| 0002 | refresh_tokens | Tabla de refresh tokens |
| 0003 | cascade_user_fks | `ON DELETE CASCADE` en FKs a users (Postgres) |
| 0004 | enable_rls_per_user_tables | Políticas RLS (Postgres-only) |
| 0005 | code_evaluations | Evaluaciones del tutor evaluador |
| 0006 | challenge_completions | Completado de retos (auto-marcado hasta `0015`) |
| 0007 | exercise_hidden_tests | Columna `hidden_tests` JSON |
| 0008 | capstones | `capstones` + `capstone_submissions` (RLS) |
| 0009 | certificates | Certificados (tabla pública, sin RLS) |
| 0010 | elo_ratings | ELO multidominio `EloRating(user, domain, scope)` |
| 0011 | challenge_completion_elo_delta | Columna `elo_delta` para revertir |
| 0012 | code_quality_snapshots | Snapshots de calidad de código (RLS) |
| 0013 | lesson_track | Columna `lessons.track` (habilita multi-track) |
| 0014 | datasets | Datasets seedeables servidos como CSV |
| 0015 | challenge_hidden_tests | Columna `coding_challenges.hidden_tests`: completar un reto exige pasar sus tests |
| 0016 | exercise_types | `exercises.exercise_type` (default `code`) + `spec` (público) + `answer_key` (privada) para Track 0 |
| 0017 | password_reset_tokens | Tokens de recuperación de contraseña (hash SHA-256, un solo uso, **sin RLS** a propósito) |

- **Regla DDL Postgres-only** (RLS, constraints sin nombre estable): empezar el `upgrade()` con
  ```python
  if op.get_bind().dialect.name != "postgresql":
      return
  ```
  para que sea no-op en SQLite (los tests usan SQLite).
- **Columna nueva sobre tabla existente**: usar `batch_alter_table` para que la migración sea no-op-safe en SQLite.
- Tracks 3-6 y el proxy LLM **no añadieron migraciones**: el contenido nuevo son filas seedeadas.

### 2.4 Row-Level Security (RLS)

Las tablas por-usuario tienen políticas RLS que filtran por `current_setting('app.current_user_id')`, que `get_current_user` setea a partir del JWT. Los endpoints **además** filtran por `user_id` en la query (RLS es la segunda línea de defensa, no la única). Tests cross-user verifican que un usuario no puede leer datos de otro.

Tablas **sin RLS** por diseño: `certificates` (credencial compartible vía código de verificación), `capstones` (contenido definicional) y `password_reset_tokens`: el flujo de recuperación ocurre **sin sesión**, así que no hay `app.current_user_id` que setear; su defensa es el diseño del token (ver [RECUPERACION_PASSWORD.md](RECUPERACION_PASSWORD.md)).

### 2.5 API surface (`/api/v1`)

| Router | Endpoints clave |
|---|---|
| `auth` | register, login, refresh (rotation), logout (revoca jti), `password-reset/request` + `password-reset/confirm`, me |
| `users` | me, profile, me/export (GDPR), DELETE me (GDPR) |
| `lessons` | list (con `order` y `track`), `/{id}` (con `selectinload(exercises)`) |
| `exercises` | por lección, `/{id}/submit`, `/{id}/check` (Track 0), `/{id}/hidden-tests` (auth, no leak), `/{id}/evaluations`, `/{id}/hints` |
| `execute` | run → **410 Gone**, validate → `ast.parse` (sin ejecutar) |
| `tutor` | `POST /evaluate` (REST atómico) + WS `/ws/tutor` (Q&A) |
| `progress` | competencies, track-status, code-quality |
| `elo` | attempt, ratings, history, puzzle-of-the-day (público) |
| `challenges` | list, detail (sin `reference_solution`), `/{id}/hidden-tests`, complete (exige tests aprobados) / uncomplete |
| `capstones` | list, `/{slug}` detail (sin hidden_tests), submissions |
| `certificates` | issue (gate 403), download (PDF), verify/{code} (público) |
| `datasets` | `/{slug}/csv` |
| `ai` | `/complete` — proxy LLM (Track 5): auth + rate limit 40/día + tope de tokens |

Fuera de `/api/v1`, en `main.py`: `GET /health` (vivo), `GET /health/db` (`SELECT 1`, lo usa el keepalive) y **`GET /health/llm`** (`?ping=1` hace una llamada real al modelo). Este último es público y sin secretos: `degraded` = sin key, `unhealthy` = el modelo falla o **responde vacío** (y dice por qué), `healthy` = contestó.

### 2.6 Servicios notables

- **`llm_provider.py`** — abstrae Groq + OpenAI + Stub. `get_provider(settings)` despacha por `LLM_PROVIDER`. Stub devuelve `""` y deja al caller usar fallback (sin API key el sistema sigue funcionando de forma degradada). Modelo actual: `openai/gpt-oss-120b`; `GroqProvider` manda `reasoning_effort: "low"` vía `extra_body` porque los tokens de razonamiento salen del mismo `max_tokens` que la respuesta.
- **`ai_tutor.py`** / **`tutor_guide_service.py`** / **`evaluation_service.py`** — tutor Q&A y evaluador. Distinguen el track: con `track-0` preguntan por la traza, no por código.
- **`track0_service.py`** — correctores deterministas por `exercise_type` (`trace_table`, `predict_output`, `mcq`, `flowchart_match`, `flowchart_fill`). El feedback dice **dónde** falla, nunca el valor correcto.
- **`progress_service.py`** — fuente única de "ejercicio hecho" (`completed_exercise_ids`: ≥ 1 `CodeSubmission` con `result="success"`) y de la conversión `XP_POR_PUNTO = 10`. Ningún endpoint reimplementa esa query.
- **`password_reset_service.py`** + **`email_provider.py`** — tokens de un solo uso y envío por **API HTTP** (Render free bloquea SMTP). `EMAIL_PROVIDER` = `brevo` | `sendgrid` | `mailjet` | `console`; sin credenciales cae a `console`, que escribe el enlace en el log.
- **`elo_service.py`** — ELO clásico: attempts, rank progression con `ELO_DELTA_TABLE` / `ELO_DELTA_TABLE_ADVANCED` por rango.
- **`elo_rating_service.py`** — ELO multidominio: `get_or_init_rating(user, domain, scope)` con lazy-init desde el ELO global (continuidad), `apply_result_to_rating`.
- **`code_quality_service.py`** — `analyze_code` calcula un `static_score` 0-100 con AST **sin ejecutar** (complejidad ciclomática, longitud de funciones, anidamiento, docstrings, líneas largas).
- **`certificate_pdf.py`** — render con reportlab (A4 apaisado, marco, código de verificación, fecha ES sin locale).
- **Seeders** (`lesson_seed`, `capstone_seed`, `dataset_seed`, `curated_retos`, `retos_validacion`, `puzzle_seed`, `generated_bank`) — idempotentes por clave natural (title/slug). **El contenido de las lecciones vive en `lesson_seed.py`**; `lesson_content.py` es código muerto que no se importa.

### 2.7 Autenticación

- **PyJWT** (HS256; sustituyó a python-jose el 2026-11-03). La excepción es `jwt.InvalidTokenError`. La `SECRET_KEY` debe medir 32 bytes o más.
- Access token corto + refresh token con **rotación**; `logout` revoca el `jti`. Contraseñas con bcrypt.
- El registro devuelve los errores de validación **por campo** y el front los pinta en su input (el patrón de `username` parecía un error de la contraseña).

---

## 3. Frontend

React 18 + TypeScript + Vite 6 + Tailwind + Zustand. Tests con vitest 4 y Playwright.

- **Proxy dev**: Vite proxea `/api` y `/ws` a `localhost:8000` — el código llama rutas relativas, nunca `http://localhost:8000`.
- **Estado global**: un único store Zustand [`authStore.ts`](../frontend/src/stores/authStore.ts) con `accessToken` + `refreshToken` + `user`.
- **API layer**: [`services/api.ts`](../frontend/src/services/api.ts) (fetch nativo). Interceptor: ante un 401 intenta `POST /auth/refresh` y reintenta el request original; si falla, limpia tokens y redirige a `/login`. Opción `skipAuth` para endpoints públicos (puzzle del día, verify certificado, recuperación de contraseña). Nunca llamar rutas con slash final: el rewrite de Vercel no las proxea.
- **Producción**: `TutorChat.tsx` conecta directo a `wss://pycode-backend.onrender.com/ws/tutor` cuando `import.meta.env.PROD` (Vercel Hobby no proxea WS de forma confiable).
- **Rutas**: `/`, `/login`, `/register`, `/forgot-password`, `/reset-password`, `/dashboard`, `/editor`, `/lessons`, `/lessons/:lessonId`, `/competencias`, `/capstones/:slug`, `/verify/:code`, `/challenges`, `/puzzles`, `/interview`, `/tutor`. Las páginas se cargan con `lazy`.

### 3.1 Editor

[`pages/CodeEditor.tsx`](../frontend/src/pages/CodeEditor.tsx), con tres modos según la URL:

| Modo | URL | Navegación |
|---|---|---|
| Libre | `/editor` | — |
| Lección | `/editor?lesson=<id>&exercise=<id>` | Anterior/Siguiente entre los ejercicios de la lección ("Ejercicio N de M") |
| Reto | `/editor?challenge=<id>&dificultad=<filtro>` | Anterior/Siguiente en la lista filtrada de Retos ("Reto N de M") |

El `dificultad` no es decorativo: reconstruye la misma lista con la que se entró.

**Layout** (rediseño del 2026-11-03, porque el editor llegó a medir 5 px):

- Por debajo de `lg` se apila (código arriba, Salida abajo, cada uno con alto en `dvh`) y la página scrollea. Desde `lg` el editor se ata al alto de la ventana.
- El **enunciado** es una banda superior con tope del 38% (scroll interno) hasta `xl`; desde `xl` es una columna a la izquierda con todo el alto. Es plegable y se recuerda en `localStorage`.
- Los **resultados de los tests van dentro del panel de Salida**; la "salida esperada" arranca plegada en lección y reto.
- **Dos botones de ejecutar**: el de la barra («Ejecutar») y otro en la cabecera de la Salida («Ejecutar el codigo y ver la salida»), junto a «Limpiar salida», que en el celular queda justo debajo del código.
- **Pantalla completa** (sale del contenedor de `Layout`; `Esc` para salir).
- El veredicto del tutor se pinta con `EvaluacionSocratica` + `evaluacionSecciones`: fichas de nota por tramo (85/70/50) y una tarjeta por bloque, reconocidos por slug y no por formato.

Gotchas de layout que ya rompieron producción (detalle en `CLAUDE.md`): toda columna flex con Monaco, tabla o `pre` necesita `min-w-0`; y `flex-1` en una columna apilada anula el alto propio (usar `lg:flex-1`).

### 3.2 Sandbox Pyodide

Vive en [`frontend/src/sandbox/`](../frontend/src/sandbox/):

- `pyodideWorker.ts` corre como **Web Worker** (cargado via `new URL(..., import.meta.url)` con `worker.format='es'`).
- `PyodideSandbox.ts` lo envuelve con **Comlink** (llamadas async transparentes al worker); `watchdog.ts` impone el límite duro desde el hilo principal con `worker.terminate()` (un `while True:` bloquea el event loop del worker). El reloj cuenta "tiempo sin latidos", no tiempo total: cargar numpy o una tanda de tests lentos no se castiga (issue #32).
- El runtime Pyodide se carga lazy desde `cdn.jsdelivr.net` (whitelisted en CSP).
- **Autocarga de paquetes**: `loadPackagesFromImports(allCode)` detecta imports y descarga numpy/pandas/scipy/sklearn/matplotlib del CDN de Pyodide bajo demanda (primera carga ~10-30s).
- **`runTests`**: cada hidden_test corre en namespace fresco (`py.toPy({})`), con timeout por test y error truncado. La UI **nunca** renderiza el código del test, solo `name` + verdict ✓/✗.
- **`runCapstoneTests`**: escribe múltiples archivos al FS virtual y agrega el dir al `sys.path` para evaluar proyectos multi-archivo.
- **`traceback.ts`** (`limpiarTraceback`): quita **solo** los frames de `/_pyodide/` de cada error y conserva los del alumno (`<exec>`, archivos de capstone), la stdlib y las librerías. Se aplica al ejecutar y en los dos runners de tests; sin él, un `SyntaxError` llegaba con ~12 líneas ajenas y los tests fallidos se cortaban en «...».
- **Helpers del módulo `pycode`**: `fetch_dataset_csv(slug)` (datasets de Track 2-3) y `llm_complete(...)` (proxy LLM de Track 5; el token de sesión lo empuja el hilo principal, porque el worker no lee `localStorage`).
- **matplotlib**: se renderiza como MIME `image/png` en el editor.

### 3.3 Track 0 en el cliente

`components/track0/ExerciseRunner` despacha por `exercise_type` a un componente por tipo. Los diagramas de flujo se dibujan en **SVG a partir de datos** (nodos en el `spec`), sin Mermaid; en `flowchart_fill` el diagrama se redibuja con lo que elige el alumno. Detalle y el porqué en [TRACK_0.md](TRACK_0.md).

---

## 4. Modelo de dominio educativo

```
Track (track-0..6)
 └── Lesson (category, order, track)
      └── Exercise (exercise_type)
           ├── "code"   → hidden_tests JSON          ← evaluado en Pyodide
           └── Track 0  → spec (público) + answer_key ← corregido en el backend
 └── Capstone (por track)
      └── CapstoneSubmission (uno por user)      ← multi-archivo en Pyodide
      └── desbloquea → Certificate (verify público)

Puzzle (ELO) ── PuzzleAttempt ── EloRating(domain, scope)
CodingChallenge (hidden_tests) ── ChallengeCompletion (elo_delta)
CodeEvaluation (tutor evaluador) ── CodeQualitySnapshot (logic+general+static)
Dataset (CSV servido a Pyodide)
```

Contenido actual: 58 lecciones (Track 0: 10 · Track 1: 10 · Track 2: 11 · Track 3: 11 · Track 4: 5 · Track 5: 6 · Track 6: 5), ~258 ejercicios (198 de código + 60 de Track 0), 7 capstones, 85 retos, 100 puzzles curados, 3 datasets.

### 4.1 El patrón multi-track (lo que se replica)

Añadir contenido de **código** a cualquier track **no requiere migraciones ni endpoints nuevos**. Validado end-to-end en Tracks 2 a 6:

1. **Lección**: agregar `LessonTemplate(track="track-N", category="...", exercises=[ExerciseTemplate(hidden_tests=...)])` en `lesson_seed.py`. Seeder idempotente por title. Estándar de redacción: [PLANTILLA_LECCION.md](PLANTILLA_LECCION.md).
2. **Competencias**: registrar la `category` en `Competencies.tsx` (`CATEGORY_LABELS` + `CATEGORY_TO_TRACK` + `TRACK_INFO`).
3. **Dataset** (opcional): entrada en `dataset_seed.py`; se consume con `pycode.fetch_dataset_csv(slug)`.
4. **Capstone** (cierra el track): entrada en `CAPSTONES` (`slug`, `track`, `starter_files`, `hidden_tests`). Aprobar exige `tests_passed == tests_total`. Si usa un LLM, los tests inyectan un `llm_fn` falso.
5. **Certificado**: automático — `POST /certificates/{track}/issue` es genérico; añadir el título a `TRACK_TITLES` en `core/tracks.py`.
6. **Track-status**: automático — `/progress/track-status` itera `TRACK_TITLES`, filtra por `Lesson.track`, elige el capstone canónico y skipea tracks vacíos.

Un **tipo nuevo de ejercicio no ejecutable** (Track 0) es un validador en `track0_service` y un componente en `components/track0/`, sin migración.

**Verificación de contenido**: los valores esperados de cada `hidden_test` se fijan ejecutando el snippet con las librerías reales antes de commitear. Los capstones se verifican en Pyodide real con el método solución / starter / mutación (10/10 con la referencia, 0/10 con el starter, y cada test falla si solo su módulo queda sin hacer). `check_hidden_tests_triviales.py` (en CI vía pytest) impide que un `hidden_test` apruebe con el starter.

### 4.2 Un solo camino de completitud

Aprobar un ejercicio —de código o de Track 0— crea una `CodeSubmission` con `result="success"`. De ahí derivan, sin columnas propias: el flag "hecho" (`progress_service.completed_exercise_ids`), el progreso de la lección, el XP (1 punto = 10 XP), las competencias y el `track-status`. Así XP y progreso no se ramifican por tipo de ejercicio.

---

## 5. Sistema ELO

Dos capas coexisten (backward-compatible):

- **ELO global/clásico** (`elo_service.py`): rating overall + rank progression por rangos.
- **ELO multidominio** (`elo_rating_service.py`): `EloRating(user, domain, scope)` da rating separado por:
  - `puzzle:<category>` (Python, NumPy, Pandas, Interview, ...)
  - `challenge:<dificultad>` (easy 850 / medium 1200 / hard 1550 nominal)

  Lazy-init desde el ELO global para no romper la continuidad. `GET /elo/ratings` devuelve tracks hoja + agregados por dominio + overall. UI: `EloTracks.tsx` en el Dashboard.

El ELO de retos **no es auto-marcado** (desde la migración `0015`): `POST /challenges/{id}/complete` exige el resultado de los tests ocultos del reto, todos aprobados. Como con los ejercicios, el backend confía en lo que reporta Pyodide (nunca ejecuta código del alumno), así que sigue siendo falsificable llamando a la API a mano, pero ya no con un botón. `uncomplete` revierte el delta exacto vía `challenge_completions.elo_delta`.

---

## 6. Tutor IA — dos roles

| | Evaluador | Q&A |
|---|---|---|
| Transporte | REST `POST /tutor/evaluate` | WS `/ws/tutor` |
| Naturaleza | Atómico, sin historial | Multi-turno |
| Contexto | Código del ejercicio (opt-in, botón "Evaluar") | Pregunta libre, sin contexto de lección |
| Salida | `CodeEvaluation` + `CodeQualitySnapshot` | Respuesta socrática |

El system prompt del evaluador vive en el archivo raíz `maestro_evaluador_de_codigo_python.txt` (`TUTOR_PROMPT_FILE`, resuelto vía `settings.tutor_prompt_path`). Las notas se extraen con regex que tolera el Markdown del modelo (`- Lógica: **95/100**`; ver `tests/test_evaluation_scores.py`).

**Degradación silenciosa**: ante una excepción o una respuesta vacía, el tutor devuelve un texto de reserva que se parece a una respuesta real. Por eso existe `/health/llm?ping=1`; úsalo antes de depurar el prompt (incidente del 2026-09-15: el modelo configurado llevaba un mes retirado).

---

## 7. Seguridad transversal

Middleware montado en `main.py`:

- **`security_headers.py`** — HSTS, CSP (whitelist `cdn.jsdelivr.net` para Pyodide), X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy.
- **`rate_limit.py`** — SlowAPI con keyfunc `_user_or_ip` (por user_id autenticado, si no por IP). Contadores en memoria del proceso (un redeploy los resetea).
- **`logging_config.py`** — structlog con `redact_pii` (JWT, API keys, emails).
- **`observability.py`** — Sentry con scrubbing; no-op si no hay DSN.
- **`check_no_sqli.py`** — lint que rechaza `text(f"...")` (corre en CI).
- **No-leak**: `hidden_tests`, `reference_solution`, `correct_output` y `answer_key` tienen cada uno un test que verifica que ningún endpoint público los expone.
- **Recuperación de contraseña**: token de 32 bytes guardado como SHA-256, de un solo uso y con caducidad; la petición responde igual exista o no el email.
- **Dependencias**: Dependabot semanal + `pip-audit` (sobre `requirements.txt` **y** `requirements.lock`, que es lo que instala el Dockerfile) + `npm audit` en CI. Triaje por alcance real, no por CVSS: [SEGURIDAD_DEPENDENCIAS.md](SEGURIDAD_DEPENDENCIAS.md).

---

## 8. Notas operativas (prod)

- **Cold start Render free**: el contenedor duerme tras 15 min idle; UptimeRobot pingea `/health` cada 5 min. Sin él, las primeras llamadas tras idle tardan 30-60s o dan 502.
- **CORS_ORIGINS** en Render incluye el dominio Vercel exacto. Si cambia el dominio, actualizar y redesplegar.
- **Supabase free se pausa** tras ~7 días sin actividad de DB y tumba el deploy con "tenant/user not found"; se restaura con el MCP de Supabase (sin tocar código). **Mitigación**: el workflow `.github/workflows/keepalive-db.yml` (cron cada 4h) golpea `GET /health/db`. Si Render reporta "deploy failed" pero **CI está verde**, sospechar Supabase pausada antes que el código.
- **LLM**: `LLM_MODEL` en Render tiene su propia copia de la env var, y esa gana sobre `render.yaml`. Al cambiar de modelo hay que tocar las dos.
- **Proxy LLM y GROQ_API_KEY**: `POST /api/v1/ai/complete` (Track 5) llama al LLM real solo si `GROQ_API_KEY` está seteada; sin key cae al `StubProvider`.
- **Email**: Render free bloquea SMTP; el correo sale por API HTTP. Sin credenciales, `console` escribe el enlace en el log de Render.
- **Dev Windows**: exportar `$env:PYTHONUTF8="1"` antes de `uvicorn` — sin eso structlog crashea al loggear contenido Unicode en consola cp1252. No afecta prod ni CI.

---

## 9. Testing y CI

- **Backend**: ~290 tests (pytest-asyncio mode=auto). El `conftest` aplica `alembic upgrade head` sobre SQLite y resetea SlowAPI. Guard rails de no-leak para todo lo oculto a la UI y de hidden_tests triviales. El contenido de lecciones/capstones se verifica aparte con solución de referencia porque sus `hidden_tests` corren en Pyodide, no en pytest.
- **Frontend**: vitest (~75 tests unitarios: editor, registro, recuperación, tracebacks, watchdog, resaltado, veredicto...) + Playwright (Chromium headless). El proyecto `responsive` (`e2e/responsive.spec.ts`) no necesita backend: stubea `/api` y mide **ancho y alto** (ninguna página más ancha que la ventana; editor ≥ 280 px y Salida ≥ 200 px) en 6 ventanas, incluida 1366×650, y encogiendo una ventana de 1920.
- **CI** (`.github/workflows/ci.yml`): `backend-tests`, `backend-lint` (black + flake8 + mypy + check_no_sqli), `frontend-build` (lint + build; **vitest no corre en CI**, hay que lanzarlo en local), `audit` (pip-audit sobre txt y lock + npm audit). Dependabot semanal. Un push a `main` dispara además los despliegues de Render y Vercel.

---

## 10. Roadmap técnico

**Cerrado**: Fase 0, Fase 1 y los siete tracks: Track 0 (Fundamentos), 1 (Python), 2 (Data Science), 3 (ML Clásico), 4 (Deep Learning en numpy), 5 (AI Engineering) y 6 (MLOps). El pipeline Fundamentos → MLOps está completo de punta a punta.

Decisiones arquitectónicas resueltas en Tracks 0 y 4-6:
- **Track 0**: los ejercicios que no son código se corrigen en el **backend**, no en el cliente, porque validar en el cliente obligaría a enviarle la solución.
- **Track 4 (Deep Learning)**: se enseñó **desde cero en numpy**, que corre en Pyodide sin infra nueva. **PyTorch real** se **difirió** a un futuro Track 4b — requeriría ejecución fuera de Pyodide (GPU remota vs Colab), decisión de infra/costo pendiente.
- **Track 5 (AI Engineering)**: el retrieval de RAG se construye **en numpy**; la generación usa un **proxy backend** (`/api/v1/ai/complete`). Los tests evalúan la lógica alrededor del LLM con un LLM falso inyectado, nunca su salida no determinista.
- **Track 6 (MLOps)**: mismo enfoque "desde cero en el navegador" (sin Docker ni MLflow reales); las herramientas reales, si entran, como paso opcional no evaluado.

**Abierto** (sin asignar): diagnóstico de entrada de Track 0, que el Q&A del WebSocket conozca la lección/track, los tipos `order_steps` y `find_bug`, aplicar la plantilla de lección a Tracks 2-5, Track 4b, migrar a ESLint 9. Lo prioritario no es técnico: **recorrer los tracks como alumno**, que es lo que ha encontrado los fallos reales.
