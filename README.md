# PyCode Platform

Plataforma de aprendizaje que lleva de **Fundamentos → Python → Data Science → Machine Learning → Deep Learning → AI Engineering → MLOps**, con tutor IA socrático, sandbox de ejecución en el navegador (Pyodide), sistema ELO de puzzles estilo Finxter y certificados verificables.

> **Norte estratégico**: PyCode lleva al estudiante **de cero a ingeniería de ML/AI**. Se entra sin saber programar (Track 0: fundamentos, pseudocódigo, algoritmos y diagramas de flujo) y no se termina en Python básico: Track 1 es la rampa hacia Data Science, ML, Deep Learning, AI Engineering y MLOps. El diferenciador es el pipeline completo, con tutor socrático y ELO transversal.

## Estado

| Fase / Track | Estado | Contenido |
|---|---|---|
| **Fase 0** — fundamentos + seguridad | ✅ Cerrada (tag `fase-0-complete`) | Postgres+Alembic+RLS, Pyodide, JWT+GDPR, seguridad transversal, deploy gratis |
| **Fase 1** — pulido Track 1 + ELO | ✅ Cerrada | Tutor evaluador+Q&A, tests ocultos, ELO multidominio, calidad de código, certificados PDF |
| **Track 0** — Fundamentos de programación | ✅ Cerrado | 10 lecciones de pseudocódigo, trazas, condicionales, bucles, diagramas de flujo, descomposición, arreglos, algoritmos clásicos y coste · capstone `Del pseudocódigo al Python`. Ejercicios **no ejecutables** (ver abajo) |
| **Track 1** — Python | ✅ Cerrado | 10 lecciones · capstone `CLI de ventas` |
| **Track 2** — Data Science | ✅ Cerrado | 11 lecciones (NumPy/Pandas/Viz/EDA/Stats) · capstone `EDA cafecito` |
| **Track 3** — ML Clásico | ✅ Cerrado | 11 lecciones sklearn · capstone `Diagnóstico ML` |
| **Track 4** — Deep Learning | ✅ Cerrado | 5 lecciones **numpy puro** (backprop→MLP→XOR) · capstone `Red desde cero`. PyTorch real diferido |
| **Track 5** — AI Engineering | ✅ Cerrado | 6 lecciones (embeddings, RAG, LLM real vía proxy, agentes, evals) · capstone `Nebula RAG` |
| **Track 6** — MLOps | ✅ Cerrado | 5 lecciones (reproducibilidad, tracking/registro, servir un modelo, drift, CI/CD) · capstone `Pipeline de producción` |

**En números**: ~60 lecciones · ~260 ejercicios (los de código con `hidden_tests`; los de Track 0 con su clave en el servidor) · 265 puzzles ELO (100 curados) · 85 retos, todos con tests · 7 capstones · 3 datasets · migraciones 0001-0017 · ~290 tests backend, ~75 de frontend y un guard rail E2E de responsive (ancho y alto). Esquema de datos: **[docs/DATABASE.md](docs/DATABASE.md)**. *(Cifras redondeadas a propósito; el conteo exacto vive en los tests, ej. `test_bank_has_100_puzzles`.)*

## Rampa de entrada

Track 0 **no es un peaje obligatorio**. Un alumno que ya programa en otro lenguaje no debe recorrer once lecciones de pseudocódigo para llegar a Pandas. Un diagnóstico corto (trazas y bucles) recomienda punto de entrada — Track 0 o Track 1 — pero no bloquea ninguno de los dos.

Track 0 rompe el supuesto central de validación del resto de la plataforma: sus ejercicios (tablas de traza, predecir la salida, opción múltiple, emparejar diagramas y completarlos) **no se ejecutan en Pyodide**. Los corrige el **backend** en `POST /api/v1/exercises/{id}/check`, de forma determinista: sin Pyodide y sin LLM. La solución (`answer_key`) no viaja al cliente —mismo guard rail de no-leak que `hidden_tests`, con su test— y el feedback dice **dónde** falla, nunca cuál era el valor.

Aprobar uno emite el **mismo** evento de completitud que un ejercicio de Python (una `CodeSubmission` con `result="success"`), así que XP, progreso, ELO y competencias siguen siendo un solo camino y no dos.

El capstone del track es el puente: implementar en Python los algoritmos ya trazados a mano. Como Track 0 nunca enseña sintaxis, su enunciado lleva dentro la tabla de traducción pseudocódigo → Python.

## Qué falta

El contenido y la plataforma están construidos y desplegados; lo que falta es **recorrerlos**. A día de hoy nadie ha llegado a un capstone en producción, así que los ~260 ejercicios están verificados con solución de referencia y pruebas E2E, que no es lo mismo que haberlos atravesado aprendiendo. La deuda técnica abierta (cobertura de tests del frontend, código muerto, un componente de 900 líneas) está listada y priorizada en [docs/BARRIDO_PROBLEMAS.md](docs/BARRIDO_PROBLEMAS.md).

Lo del 2026-09-15 lo ilustra: usando la plataforma un rato aparecieron tres fallos que ninguna suite veía. El **tutor llevaba un mes muerto** — Groq retiró el modelo configurado y el fallback del evaluador se parece tanto a una respuesta real que nada lo delató—; la nota del veredicto salía con un guión porque el modelo escribe `**95/100**` y el parser esperaba `95/100`; y el editor **se desbordaba al encoger la ventana**, no al abrirla estrecha. De ahí salieron `/health/llm` y el guard rail de responsive: la lección no es que faltaran tests, es que fallaban cosas que solo se ven usándolo.

### Cuentas y acceso

El 2026-10-04 un estudiante no consiguió registrarse: el formulario le decía
`String should match pattern '^[a-zA-Z0-9_-]+$'` sin aclarar que ese patrón era
el del **nombre de usuario**, así que estuvo cambiando la contraseña intento
tras intento. Y al terminar descubrió que tampoco había forma de recuperar el
acceso si se le olvidaba.

Arreglado en los dos frentes: el registro ahora pinta cada error **dentro de su
campo** y enseña las reglas antes de enviar, y existe recuperación por email
(`/forgot-password`) con token de un solo uso. Detalle, decisiones de seguridad
y puesta en marcha de Brevo en **[docs/RECUPERACION_PASSWORD.md](docs/RECUPERACION_PASSWORD.md)**.

Es otro caso del mismo patrón: un fallo que ninguna suite veía y que apareció
en cuanto alguien de fuera intentó usar la plataforma.

### El editor en pantallas reales (2026-11-03)

Al retomar el proyecto en otra máquina salió que, en producción, el editor
medía **5 px** en celular y tablet, y bajaba a 5 px en el portátil al ejecutar
los tests: el guard rail de responsive medía el ancho, no el alto. Se rediseñó
probándolo en portátil, celular y monitores de 24" y 27": el enunciado pasa a
una columna a la izquierda en pantallas anchas, los resultados de los tests van
dentro de la Salida y hay un segundo botón **Ejecutar** en la cabecera de la
Salida. Los errores ya no llegan encabezados por una docena de frames internos
de Pyodide. El guard rail mide ahora también el alto del editor y de la Salida.

El mismo día se puso al día la seguridad de dependencias: `python-jose` se
sustituyó por **PyJWT**, `pip-audit` queda limpio (también sobre
`requirements.lock`, que es lo que instala el Dockerfile) y `npm audit` sin
critical ni high. Plan de lo que queda en
[docs/SEGURIDAD_DEPENDENCIAS.md](docs/SEGURIDAD_DEPENDENCIAS.md).

## Producción

- **Frontend**: https://pycode-platform.vercel.app (Vercel Hobby)
- **Backend**: https://pycode-backend.onrender.com (Render Free, Docker)
- **DB**: Supabase Postgres (sa-east-1, RLS habilitada)
- **Watchdog**: UptimeRobot ping `/health` cada 5 min (cold start de Render) + workflow `keepalive-db.yml` (cron 4h → `/health/db`, evita que Supabase free se pause por inactividad)

## Características

- **Editor Monaco** con tres modos (libre, lección y reto, con Anterior/Siguiente sin salir del editor), tema/fuente configurables, descarga de script, copia al portapapeles, **pantalla completa** (Esc para salir) y enunciado plegable. En pantallas anchas el enunciado es una columna a la izquierda; los resultados de los tests se ven en la Salida, que tiene su propio botón Ejecutar.
- **Pyodide en Web Worker**: el código del estudiante se ejecuta en el navegador con Comlink + timeout duro (corta un bucle infinito sin castigar la carga de numpy) y tracebacks sin los frames internos de Pyodide. El backend nunca lo ejecuta (`/api/v1/execute/run` retorna 410; `/validate` solo hace `ast.parse`). numpy/pandas/scipy/sklearn/matplotlib autocargan bajo demanda.
- **Tutor IA Socrático** con dos roles separados: **evaluador de código** (REST atómico) y **Q&A** (WebSocket multi-turno). Provider abstraction: Groq (default) → OpenAI fallback → Stub determinístico si no hay API key. La retroalimentación se presenta con forma: las dos notas como fichas de color por tramo (85/70/50) y cada bloque del veredicto en su tarjeta — verde lo que ya está bien, ámbar lo que falta, índigo las preguntas socráticas.
- **Diagnóstico del LLM** (`GET /health/llm?ping=1`, público y sin secretos): dice si hay API key, si el modelo responde y **si responde vacío**. Existe porque el modo degradado del tutor es invisible — su texto de reserva se parece a una respuesta real, así que `/health` y `/health/db` pueden estar en verde con el tutor muerto.
- **Proxy LLM para AI Engineering** (Track 5): `POST /api/v1/ai/complete` deja que el código del alumno (en Pyodide) llame a un LLM real vía backend — auth + rate limit + tope de tokens, sin exponer API keys. Helper `pycode.llm_complete()` en el editor.
- **Ejercicios que no se ejecutan** (Track 0): tablas de traza, predecir la salida, opción múltiple y dos tipos de diagrama de flujo. Los corrige el backend, no el navegador. Los diagramas se dibujan en **SVG a partir de datos** (nodos en el `spec` del ejercicio), sin Mermaid ni imágenes: en el de completar huecos, el diagrama se redibuja con lo que el alumno elige.
- **Tests ocultos por ejercicio**: `hidden_tests` que corren en Pyodide en namespace fresco, sin exponerse a la UI. Es el patrón base de validación replicado en todos los tracks de código.
- **Sistema ELO multidominio**: rating separado por actividad y categoría temática (`puzzle:<category>`, `challenge:<dificultad>`), con lazy-init desde el ELO global. Banco de 100 puzzles curados + puzzle del día público.
- **Progresión de calidad de código**: `static_score` con AST (sin ejecutar) + scores logic/general del evaluador LLM, persistidos y graficados en el tiempo.
- **Capstones y certificados**: proyectos multi-archivo evaluados en Pyodide; aprobarlos desbloquea un certificado PDF con código de verificación **público**.
- **Auth JWT** (PyJWT) con refresh token rotation, `/auth/logout` que revoca el `jti`, errores de registro por campo y **recuperación de contraseña por email** (token de un solo uso; Brevo, SendGrid o Mailjet por API HTTP). **GDPR**: `DELETE /users/me` + `GET /users/me/export`.
- **Seguridad transversal**: HSTS/CSP/XCTO/XFO/Referrer-Policy/Permissions-Policy, CORS whitelist, rate limiting por user_id, structlog con redaction de PII, Sentry con scrubbing.
- **Postgres + Alembic + RLS** por tabla con `current_setting('app.current_user_id')`.
- **CI**: pytest + black + flake8 + lint anti-SQLi, pip-audit + npm audit, Dependabot semanal.

## Stack

**Backend**: FastAPI + SQLAlchemy 2.0 async + asyncpg · Postgres (Supabase en prod) + Alembic · PyJWT + bcrypt · SlowAPI (rate limit) · structlog + sentry-sdk · Groq SDK + OpenAI SDK · reportlab (PDF) · pytest + pytest-asyncio + httpx + Playwright (E2E).

**Frontend**: React 18 + TypeScript + Vite 6 · TailwindCSS · Monaco Editor · Pyodide + Comlink (Web Worker) · Zustand · Recharts · `fetch` nativo con interceptor de refresh (no axios) · vitest 4 + Playwright.

## Requisitos

- Python 3.11 · Node.js 20 (el de CI; también probado con Node 24) · Postgres 16 local (opcional; los tests corren contra SQLite, pero Postgres es necesario para autogenerar migraciones y validar RLS).

## Instalación

### Backend

```bash
cd backend
python -m venv .venv311
.venv311\Scripts\activate            # Windows; en Unix: source .venv311/bin/activate
pip install -r ../requirements.txt   # o ../requirements.lock para versiones pinned

cp ../.env.example .env              # backend/.env: se lee desde la carpeta donde arrancas

alembic upgrade head                 # obligatorio antes de levantar — crea las tablas
# Windows: exportar UTF-8 para que structlog no crashee al seedear contenido Unicode
$env:PYTHONUTF8="1"                  # (PowerShell)
uvicorn app.main:app --reload --port 8000
```

`Settings` lee `env_file=".env"` **relativo al directorio de arranque**, así que
el `.env` va en `backend/`, que es desde donde se lanzan `alembic` y `uvicorn`.
Para desarrollo local basta con `DATABASE_URL=sqlite+aiosqlite:///./pycode.db`,
una `SECRET_KEY` propia y `EMAIL_PROVIDER=console`. **No uses la `DATABASE_URL`
de producción en local**: al arrancar, el `lifespan` siembra contenido en la base
a la que apunte. Sin `GROQ_API_KEY` el tutor responde con su texto de reserva
(`GET /health/llm` lo dice).

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
python scripts/check_hidden_tests_triviales.py  # ningún hidden_test aprueba con el starter
alembic revision --autogenerate -m "descripcion"   # contra Postgres limpio

# Frontend
cd frontend
npm run build       # tsc + vite build (errores de TS fallan el build)
npm run lint        # eslint --max-warnings 0
npm run test        # vitest (no corre en CI: lánzalo antes de subir)
npm run test:e2e    # Playwright (Chromium headless) — necesita backend + usuario E2E
npx playwright test --project=responsive   # guard rail de responsive; no necesita backend
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
│   │                          code_evaluation, capstone, certificate, code_quality, dataset,
│   │                          password_reset
│   ├── services/            # ai_tutor, tutor_guide_service, llm_provider, track0_service,
│   │                          lesson_seed (el contenido real; lesson_content.py es código muerto),
│   │                          progress_service, elo_service, elo_rating_service,
│   │                          code_quality_service, capstone_seed, certificate_pdf,
│   │                          email_provider, password_reset_service, curated_retos, ...
│   └── websockets/          # tutor_chat (/ws/tutor); /ws/code deprecado
├── alembic/versions/        # 0001 → 0017
├── scripts/check_no_sqli.py
├── tests/                   # suite de tests del backend
└── Dockerfile               # alembic upgrade head + uvicorn

frontend/
├── src/
│   ├── pages/               # Dashboard, Lessons, LessonDetail, CodeEditor, Puzzles,
│   │                          InterviewProblems, Challenges, Competencies, CapstoneDetail,
│   │                          CertificateVerify, TutorChat, Home, Login, Register,
│   │                          ForgotPassword, ResetPassword
│   ├── components/          # EvaluacionSocratica (veredicto del tutor), EloResultModal,
│   │                       EloTracks, CodeQualityPanel, PuzzleOfTheDay, ...
│   │   └── track0/          # ExerciseRunner + un componente por tipo no ejecutable,
│   │                          incluido el render SVG de diagramas de flujo
│   ├── sandbox/             # pyodideWorker, PyodideSandbox (Comlink), watchdog, traceback
│   ├── services/api.ts      # fetch + interceptor de refresh
│   └── stores/authStore.ts
├── e2e/                     # Playwright specs
└── vite.config.ts

docs/
├── ARCHITECTURE.md          # diseño técnico (empezar aquí)
├── DATABASE.md              # esquema de base de datos descrito
├── DEPLOY.md                # Render + Vercel + Supabase + UptimeRobot
├── TRACK_0.md               # ejercicios no ejecutables y convención de pseudocódigo
├── PLANTILLA_LECCION.md     # estándar de redacción de lecciones
├── RECUPERACION_PASSWORD.md # registro y recuperación de contraseña
├── SEGURIDAD_DEPENDENCIAS.md
├── BARRIDO_PROBLEMAS.md · AUDITORIA_CONTENIDO.md
├── historico/               # diseño inicial descartado
└── superpowers/specs/       # specs por fase

.github/workflows/
├── ci.yml                   # backend-tests, backend-lint, frontend-build, audit
└── keepalive-db.yml         # cron 4h → /health/db (evita pausa de Supabase)
```

## Documentación

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — diseño técnico: capas, flujo de datos, modelos, el patrón multi-track, sandbox, ELO, seguridad.
- **[docs/DATABASE.md](docs/DATABASE.md)** — esquema de base de datos: 23 tablas por dominio, columnas, relaciones, RLS y migraciones.
- **[docs/TRACK_0.md](docs/TRACK_0.md)** — Track 0: temario, tipos de ejercicio no ejecutables, convención de pseudocódigo y por qué los diagramas no usan Mermaid.
- **[docs/BARRIDO_PROBLEMAS.md](docs/BARRIDO_PROBLEMAS.md)** — problemas detectados con evidencia y prioridad, y cuáles siguen abiertos.
- **[docs/RECUPERACION_PASSWORD.md](docs/RECUPERACION_PASSWORD.md)** — registro con errores por campo y recuperación de contraseña por email: diseño del token, qué no se filtra y cómo configurar Brevo.
- **[docs/DEPLOY.md](docs/DEPLOY.md)** — despliegue Render + Vercel + Supabase, variables de entorno que ganan en el dashboard y comprobación tras desplegar.
- **[docs/PLANTILLA_LECCION.md](docs/PLANTILLA_LECCION.md)** — estándar de una lección (estructura, ejercicios, anotación de líneas).
- **[docs/AUDITORIA_CONTENIDO.md](docs/AUDITORIA_CONTENIDO.md)** — la auditoría que mostró que Track 1 no tenía contenido y llevó a reescribirlo.
- **[docs/SEGURIDAD_DEPENDENCIAS.md](docs/SEGURIDAD_DEPENDENCIAS.md)** — triaje de vulnerabilidades de dependencias (P1-P4 por alcance real, no por CVSS), lo aplicado y el plan de lo que queda.
- `docs/historico/` — `PYCODE_SPEC.md` y `PLAN_COMPLETO.md`: diseño inicial **descartado** (ejecución en Docker server-side, Kubernetes, microservicios). Se conservan como registro; no son fuente de verdad.

## Convenciones

- Idioma de UI / docs / commits / comentarios: **español**.
- Commits **sin línea Co-Authored-By**.
- **El backend nunca ejecuta código del alumno.** La ejecución vive en Pyodide, en el navegador. No reintroducir sandbox Docker ni endpoints de ejecución server-side.
- Schema changes pasan por Alembic (no `create_all`); FKs hacia `users.id` con `ondelete="CASCADE"`; DDL Postgres-only con guard de dialecto.
- Async SQLAlchemy: usar `selectinload`/`joinedload` para relaciones accedidas en endpoints.
- Añadir lección/track de **código** = agregar `LessonTemplate(track=..., category=...)` + registrar la categoría en `Competencies.tsx`. Sin migración ni endpoints nuevos. Track 0 es la excepción, ya construida: sus tipos no ejecutables viven en `exercise_type` + `spec` + `answer_key` (migración 0016) y añadir uno nuevo es un validador en `track0_service` y un componente en `components/track0/` (ver `docs/TRACK_0.md`).
- Guard rail de no-leak: lo oculto a la UI (`hidden_tests`, `reference_solution`, y la solución de cualquier ejercicio no ejecutable) debe tener un test que verifique que no se expone.
- Guard rail de responsive: `e2e/responsive.spec.ts` comprueba que ninguna página sea más ancha que la ventana, en 6 anchos (360–1920) **y encogiendo** una ventana que estaba a 1920 — la mitad de los fallos solo aparecen ahí —, y que el editor (≥ 280 px) y la Salida (≥ 200 px) tengan alto en 6 ventanas. Toda columna flex que contenga Monaco, una tabla o un `pre` necesita **`min-w-0`**; y en una columna apilada, `flex-1` anula el alto propio (usar `lg:flex-1`).

## Licencia

MIT — ver [LICENSE](LICENSE).
