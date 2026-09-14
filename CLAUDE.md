# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

PyCode Platform — learning platform for Python with Monaco editor, sandboxed code execution, a Socratic AI tutor, and a Finxter-inspired ELO puzzle progression system. 

**Norte estratégico**: PyCode lleva al estudiante **de cero a ingeniería de ML/AI**. Se entra sin saber programar (Track 0: fundamentos/pseudocódigo/algoritmos) y **no** se termina en Python básico: Track 1 es la rampa hacia el pipeline **Fundamentos → Python → Data Science → ML → Deep Learning → AI Engineering → MLOps**. No excluye a principiantes; el diferenciador es el pipeline completo con tutor socrático y ELO transversal. Toda feature nueva debe apoyar esa rampa (ver memoria `project_norte_ml_ai`).

**Estado actual (2026-07)**:
- 🚧 **Track 0 (Fundamentos) — piloto en marcha (2026-09-14)** — el tramo de entrada para quien no ha programado nunca, con **ejercicios que no se ejecutan** (pseudocódigo y trazas no corren en Pyodide). Infra hecha: migración **0016** (`exercises.exercise_type` + `spec` público + `answer_key` privada), corrección **en el backend** `POST /exercises/{id}/check` con `track0_service` (determinista, sin Pyodide ni LLM; el doc pedía validar en el cliente y es incompatible con no filtrar la solución), y `ExerciseRunner` en el front que despacha por tipo. Tipos vivos: `trace_table` (el central), `predict_output` y `mcq`. Aprobar crea una `CodeSubmission` normal, así que XP/progreso/competencias **no se ramifican**. Categoría `algoritmos` (no `fundamentos`: ya la usa Track 1) y órdenes **negativos** (-10..-8) para ir antes de Track 1. **9 lecciones** (algoritmo, variables, **traza**, condicionales, bucles, descomposición, arreglos, algoritmos clásicos y coste) con 54 ejercicios, **más el capstone `track-0-del-pseudocodigo-al-python`**: 8 requisitos en Python con `hidden_tests` en Pyodide y certificado de Track 0. Como Track 0 nunca enseña sintaxis, el enunciado del capstone lleva dentro la **tabla de traducción pseudocódigo → Python**. Falta solo la lección 6. Los arreglos se indexan **desde 0**, no desde 1 como PSeInt: el capstone pide implementar en Python lo ya trazado y cambiar de base en ese salto convierte el puente en un tropiezo. Convención de pseudocódigo: estilo PSeInt en español, **confirmada por el usuario** (cambiarla obliga a reescribir los enunciados). Detalle en [docs/TRACK_0.md](docs/TRACK_0.md).
- ✅ **Fase 0 cerrada (30/30)** — tag `fase-0-complete` (2026-05-08). Infra: Postgres+Alembic+RLS, Pyodide Web Worker, LLM provider abstraction, seguridad transversal, JWT+GDPR, deploy gratis.
- ✅ **Fase 1 cerrada** — pulido Track 1 + ELO completo. Tutor separado en evaluador (REST) + Q&A (WS), tests ocultos Pyodide, **ELO multidominio** + snapshots de calidad de código, banco de **100 puzzles curados** + 10 retos DS/ML, capstones + **certificados PDF verificables**.
- ✅ **Track 2 (Data Science) cerrado** — 11 lecciones (NumPy/Pandas/Viz/EDA/Stats) + capstone `track-2-eda-cafecito` + datasets seedeados + render matplotlib en el editor.
- ✅ **Track 3 (ML Clásico) cerrado** — 11 lecciones sklearn en Pyodide (LogReg/KNN, métricas, pipelines, regresión, árboles/RF, CV/GridSearch, KMeans, PCA, SVM, Naive Bayes, ROC/AUC) + capstone `track-3-diagnostico-ml`.
- ✅ **Track 4 (Deep Learning) cerrado** — 5 lecciones **en numpy puro** (neurona/forward, pérdidas+gradiente numérico, backprop, training loop, MLP que resuelve XOR) + capstone `track-4-mlp-desde-cero`. **PyTorch real diferido** (necesitaría GPU remota/Colab; ver `project_track4_piloto`).
- ✅ **Track 5 (AI Engineering) cerrado** — AI 1-3: embeddings/búsqueda semántica, chunking/indexación (retriever RAG en numpy), y LLM real + prompt RAG vía **proxy backend** `POST /api/v1/ai/complete` (reusa el LLM provider; helper `pycode.llm_complete` en el worker). **AI 4 · RAG de punta a punta** (2026-09-13, primera de Track 5 con el estándar de la plantilla: 6 ejercicios, 88% de líneas anotadas): tokenizar sin tildes, bolsa de palabras, índice único, umbral de relevancia (sin contexto no se llama al LLM), fuentes numeradas con citas validadas y `async def responder` con el LLM inyectable (falso en tests, `pycode.llm_complete` en el editor). **AI 5 · Agentes que usan herramientas** (mismo estándar): fichas de herramientas, acción en JSON, validación de nombre y argumentos, errores como observaciones, detección de bucles y ciclo ReAct `async` con tope de pasos. **AI 6 · Evaluar sistemas con LLM**: conjunto de casos con datos clave y fuentes esperadas, métricas deterministas (cobertura, precision/recall de fuentes), LLM como juez con veredicto validado (ilegible = sin veredicto, no un 1), `async def evaluar` y comparación de versiones caso a caso. **Capstone `track-5-nebula-rag`** (2026-09-13): el asistente completo en 5 módulos (`recuperacion`, `asistente`, `herramientas`, `nebula` = router agente/RAG, `evaluacion`) + `datos.py` + `demo.py` opcional con `pycode.llm_complete`; 10 requisitos y 10 hidden_tests `async` con **LLM falso inyectado** (guiones + registro de prompts), nunca el real. Verificado: 10/10 con la solución de referencia en Pyodide real, 0/10 con el starter, y cada test falla si solo su módulo queda sin hacer.
- ✅ **Track 6 (MLOps) cerrado** — mismo enfoque "desde cero en el navegador" que Tracks 4-5 (Python/numpy en Pyodide, sin Docker/MLflow reales; las herramientas reales, si entran, como paso opcional no evaluado). Categoría `mlops`. **MLOps 1 · Reproducibilidad** (2026-09-13, estándar de la plantilla: 6 ejercicios, 90% de líneas anotadas): semillas con generador propio, división train/test reproducible, huellas SHA-256 de datos y configuración en formato canónico (`json.dumps(sort_keys=True)`), manifiesto con entorno y métricas, comparación de manifiestos y `ejecutar_experimento` con id = huella de la receta (sin métricas). **MLOps 2 · Seguimiento de experimentos y registro de modelos** (MLflow desde cero): runs con parámetros/métricas/historial y estado, JSON Lines, mejor run (solo terminados con la métrica; empate = el primero), modelo con `pickle` + checksum SHA-256 comprobado **antes** de `pickle.loads`, registro de versiones con etapas (una sola en producción, rollback promoviendo una anterior) y `experimentar` que tolera entrenamientos fallidos y deja el mejor en staging. **MLOps 3 · Servir un modelo: contrato de entrada y validación** (2026-09-14, estándar de la plantilla: 6 ejercicios, 82% de líneas anotadas): el contrato como esquema de datos (tipo, `min`/`max`, `opciones`, `por_defecto` = opcional), coacción que convierte lo inequívoco y rechaza lo demás (`bool` comprobado **antes** que `int`), validación que acumula **todos** los errores y trata los campos desconocidos como error, vector de características recorriendo el `orden` del entrenamiento (categoría fuera del mapa = error, nunca un 0 por defecto: *training/serving skew*), sobre de respuesta con la misma forma siempre (`codigo`/`peticion_id`/`version`/`cuerpo`, 200/422/500/503) y `servir` que nunca revienta —`try`/`except` alrededor del modelo, 500 genérico fuera y detalle en el log de peticiones que alimentará MLOps 4—. **MLOps 4 · Monitoreo y drift** (2026-09-14, estándar de la plantilla: 6 ejercicios, 91% de líneas anotadas): vigilar el modelo con el log de MLOps 3 **sin esperar a las etiquetas** (el acierto real tarda 60 días), métricas del servicio primero (422 acusa a quien llama, 500 a nosotros, 200 no dice nada del acierto), histograma con **bordes fijos guardados con el modelo** y clip en los extremos (los conteos suman siempre), **PSI** `sum((a-e)·ln(a/e))` sobre proporciones con suelo `1e-6` y los umbrales 0.1 / 0.25, drift categórico (unión ordenada, `.get(c, 0)`, categorías **nuevas** como el aviso más urgente), drift de la predicción como resumen de todas las columnas, y `monitorear` que devuelve alertas con severidad, mínimo de muestra antes de opinar y `sorted` estable para que lo crítico salga primero. **MLOps 5 · CI/CD de modelos: de candidato a producción** (2026-09-14, estándar de la plantilla: 6 ejercicios, 94% de líneas anotadas): la decisión de desplegar escrita como código — puerta de calidad con los requisitos como datos (una métrica **no medida** cuenta como fallo, y todos los motivos juntos), champion/challenger contra **lo que ya sirve** con margen y `mayor_es_mejor` para las métricas que se leen al revés, rollout 1%→10%→50% repartido con `sha256(id) % 100` (estable por usuario y monótono al ampliar, que `random` no da), criterio de rollback por tasas de error con tolerancia y mínimo de peticiones, promover = cambiar etapa y archivar (el registro de MLOps 2), y `desplegar` con la misma forma siempre (`estado`/`motivos`/`historial`) y **cuatro finales**: rechazado, rollback, pausado (`sin datos` no es `seguir`) y promovido. **Capstone `track-6-pipeline-produccion`** (2026-09-14): el pipeline entero en 5 módulos (`reproducibilidad`, `registro`, `servicio`, `monitoreo`, `despliegue`) + `datos.py` + `demo.py` opcional que encadena las cinco piezas; 10 requisitos y 10 hidden_tests, cada uno con **sus propios datos**, nunca los de `datos.py`. Verificado en Pyodide real con `runCapstoneTests`: 10/10 con la solución de referencia, 0/10 con el starter y exactamente 8/10 con cada módulo a solas en versión starter. Con él **Track 6 queda cerrado** y el pipeline Fundamentos → Python → DS → ML → DL → AI Engineering → MLOps está completo de punta a punta.

**Contenido en números**: 57 lecciones (Track 0: 9 · Track 1: 10 · Track 2: 11 · Track 3: 11 · Track 4: 5 · Track 5: 6 · Track 6: 5) · 252 ejercicios (198 de código + 54 de Track 0, que no se ejecutan) (todos con hidden_tests; Track 1 reescrito entero: 60) · 100 puzzles ELO curados · 85 retos (25 problemas × 3 niveles, 5 de ellos de datos/ML, + 10 curados; todos con hidden_tests y solución de referencia) · 7 capstones · 3 datasets. Migraciones 0001-0016 (Tracks 3-6 y el proxy LLM **no** añaden migraciones; la 0015 es `coding_challenges.hidden_tests` y la 0016 los tipos de ejercicio de Track 0). 229 tests backend. Esquema de datos: `docs/DATABASE.md`. **Nota**: el contenido real vive en `lesson_seed.py`; `lesson_content.py` es código **muerto/duplicado** (no se importa) — no editarlo pensando que seedea.

**Producción**:
- Frontend: https://pycode-platform.vercel.app (Vercel Hobby)
- Backend: https://pycode-backend.onrender.com (Render Free, Docker)
- DB: Supabase Postgres `medutbqsurjnaaymmrin` (sa-east-1, RLS habilitada)
- Watchdog: UptimeRobot ping `/health` cada 5 min

## Plan de correcciones en curso (`INSTRUCCIONES_CLAUDE_CODE.md`)

Fuente: `INSTRUCCIONES_CLAUDE_CODE.md` en la raíz (bloques 0-7, se pegan de uno
en uno). **Estado a 2026-09-09**:

| Bloque | Estado |
|---|---|
| 0 — Diagnóstico | ✅ cerrado |
| 1 — Progreso que no se persiste | ✅ cerrado y **verificado en producción por el usuario** |
| 2 — Navegación del editor | ✅ implementado (`6e82b1f`, `b694db2`) — se hizo **sin autorización previa** |
| 3 — Warning de pyarrow | ✅ cerrado (`9e47395`) — se hizo fuera de turno, pero el usuario decidió mantenerlo |
| 4 — Densidad de contenido | ✅ cerrado dentro de la reescritura de Track 1 (fila de abajo). La [auditoría](docs/AUDITORIA_CONTENIDO.md) demostró que el problema no era la densidad de ejercicios sino que **las 10 lecciones de Track 1 no tenían contenido** (208 chars de media, 1 bloque de código entre las 10); hoy están entre 4.954 y 8.698 chars |
| 5 — Presentación de la lección | ✅ typography + resaltado + copiar + ancho de línea; **índice con anclas** (lateral fijo / plegable en móvil, marca la sección activa) y **bloques semánticos** Objetivo · Errores comunes · Resumen (2026-09-13). Las etiquetas "Teoría"/"Buenas prácticas" que pedía el bloque no existen en el contenido: los bloques salen de los títulos `##` que sí son constantes. No hay tema oscuro en la app |
| **Contenido de Track 1** | ✅ **10 de 10 reescritas** con la plantilla ([PLANTILLA_LECCION.md](docs/PLANTILLA_LECCION.md)): Track 1 entero, de 18 a **60 ejercicios**. `HUECOS_CONOCIDOS` quedó vacío y el test de prerequisitos es ya un guard rail puro; saldadas también las deudas de f-strings, `split`, tuplas/`.get` y la relectura de las lecciones 5-8. El Bloque 4 quedó fusionado aquí: los ejercicios se escribieron con su lección, no aparte |
| 6 — Documentación desalineada | ✅ cerrado (`docs/historico/`) |
| 7 — Barrido de problemas | ✅ listado en [docs/BARRIDO_PROBLEMAS.md](docs/BARRIDO_PROBLEMAS.md): 14 problemas con evidencia y prioridad. **Los tres P1 resueltos el 2026-09-13**: hidden_tests triviales (con guard rail en CI), enunciados en Markdown, y react-router (6.30.6 + reclasificado: lo que queda solo se parchea en v7 y no tiene alcance). También el P2 #9 (issue #32, bucle infinito) y la mitad del #5 (enunciado editable) |

**Verificación en producción del Bloque 1** (hecha por el usuario, no por un
agente): los 3 ejercicios de "Pandas esencial" resueltos en
pycode-platform.vercel.app → 3/3 tests, lección al 100%, badge HECHO, sobrevive
al F5, contador de lecciones en 1, XP idempotente (650 XP = 65 pts, sin duplicar
al reejecutar).

### Decisiones tomadas

- **Opción A para `completed`**: el flag de "ejercicio hecho" es **derivado**, no
  una columna nueva — sin migración. Se eligió precisamente para no duplicar
  fuentes de verdad, así que la regla vive **solo** en
  `progress_service.completed_exercise_ids` (>= 1 `CodeSubmission` con
  `result == "success"`, distinct por `exercise_id`) y la llaman los cinco
  consumidores: `recompute_lesson_progress`, `GET /lessons/{id}`,
  `GET /exercises/lesson/{id}`, `/progress/competencies` y
  `/progress/track-status`. **No reimplementar esa query en ningún endpoint nuevo.**
- **Orden curricular**: es `Lesson.order`, expuesto en `LessonListResponse`. El
  cliente ordena por ese campo; no asumir que el orden de la respuesta lo sea.
- **README**: la línea "En números" va redondeada, no al dato exacto.
- **`backend/.venv311`**: destrackeado con un commit normal (`0eddd57`), **sin
  reescribir historia**. Sigue en el historial antiguo y así se queda.
- **XP**: 1 punto de ejercicio = **10 XP**. `score` persiste puntos; el XP del
  dashboard es esa conversión, no un contador aparte. La constante es
  `progress_service.XP_POR_PUNTO`. La escala se mantiene: no re-escalar.
- **Dependabot**: semanal (pip/npm/actions) + `pip-audit`/`npm audit` en CI. El
  criterio de triaje P1-P4 y la clasificación de las alertas abiertas están en
  [docs/SEGURIDAD_DEPENDENCIAS.md](docs/SEGURIDAD_DEPENDENCIAS.md). La prioridad
  sale de alcance real (¿llega a producción? ¿la alcanza entrada no confiable?),
  no de la severidad CVSS.

### Backfill del progreso legacy — APLICADO

Las filas `UserProgress` con el sentinel `progress=5` (valor falso del bug viejo)
se recalcularon en producción el **2026-09-03**: 4 filas (users 6/7/8/9),
5% → 0/50/50/0%, ninguna cambió de `status` ni de `score`. Verificado después:
0 sentinels, 0 filas incoherentes. El script
`backend/scripts/backfill_legacy_progress.py` queda para futuros arrastres (sin
`--apply` es de solo lectura).

**Próximo trabajo**: el plan de correcciones está cerrado (Bloques 0-7, P1 del barrido e issue #32). Track 5 quedó cerrado con el capstone "Nebula RAG". **Track 6 cerrado** (MLOps 1-5 + capstone "pipeline de producción"). **Track 0 en piloto**: infra + 9 lecciones + capstone, todo verificado. El track ya se recorre de principio a fin y emite certificado. Queda **una sola pieza**: la **lección 6** (Diagramas de flujo), que **necesita Mermaid** —aún no es dependencia del front— y los tipos `flowchart_match`/`flowchart_fill`; su orden (-5) está reservado. Quedan sin usar `order_steps` y `find_bug`: las nueve lecciones salieron con `trace_table`, `predict_output` y `mcq`. La lección N va en el orden **N - 11** (de -10 a -1), con su hueco reservado aunque se escriban desordenadas. Pendiente de decisión: si el estándar de la plantilla se aplica a las lecciones existentes de Tracks 2-5 (AI 1-3 incluidas). Decisión pendiente aparte: Track 4b con PyTorch real (GPU remota vs Colab). Ver `docs/ARCHITECTURE.md` (diseño), `docs/DATABASE.md` (esquema) y `project_track5_piloto` / `project_track4_piloto` en memoria para el detalle vivo.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the technical design, [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for the vision, and [docs/historico/](docs/historico/) for the discarded initial design (Docker server-side, Kubernetes, microservices — **not** a source of truth).

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
cd backend && python scripts/check_hidden_tests_triviales.py  # ningún hidden_test (lecciones, retos, capstones) aprueba con el starter (en CI vía pytest)
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

Migraciones Alembic en [backend/alembic/versions/](backend/alembic/versions/), `0001`→`0015` monotónicas: `0001_initial_schema` (todas las tablas base), `0002_refresh_tokens`, `0003_cascade_user_fks`, `0004_enable_rls_per_user_tables` (RLS, Postgres-only), `0005_code_evaluations`, `0006_challenge_completions`, `0007_exercise_hidden_tests`, `0008_capstones`, `0009_certificates`, `0010_elo_ratings` (multi-ELO), `0011_challenge_completion_elo_delta`, `0012_code_quality_snapshots`, `0013_lesson_track`, `0014_datasets`, `0015_challenge_hidden_tests`. Las DDL Postgres-only (RLS) empiezan con `if op.get_bind().dialect.name != "postgresql": return` para ser no-op en SQLite (tests).

API surface versionada en `/api/v1` via [backend/app/api/v1/router.py](backend/app/api/v1/router.py): `auth` (login/register/refresh/logout), `users` (me, me/export, DELETE me), `lessons`, `exercises` (+ `/{id}/hidden-tests`, `/{id}/evaluations`), `execute` (run→410, validate con `ast.parse`), `tutor` (evaluate REST + WS Q&A), `progress` (competencies, track-status, code-quality), `elo` (attempt, ratings, history, puzzle-of-the-day), `challenges` (+ `/{id}/hidden-tests`; `/{id}/complete` exige los tests aprobados), `capstones`, `certificates` (issue/download/verify público), `datasets` (CSV), `ai` (`/complete` — proxy LLM del Track 5: auth + rate limit 40/día + tope de tokens, reusa el LLM provider). WebSocket `/ws/code` está deprecado (envía mensaje y cierra); `/ws/tutor` sigue activo.

**Lessons & Exercises**: contenido multi-track en español, seeded idempotente por title en startup. [backend/app/services/lesson_content.py](backend/app/services/lesson_content.py) tiene los 25 `LessonTemplate` de **Track 1** (64 ejercicios) sin campo `track` (default `track-1`); [backend/app/services/lesson_seed.py](backend/app/services/lesson_seed.py) añade **Track 2** (11 lecciones, `track="track-2"`) y **Track 3** (8 lecciones, `track="track-3"`) con sus `ExerciseTemplate`. Añadir una lección a otro track = agregar un `LessonTemplate(track="track-N", category="...", ...)`; sin migración ni endpoints nuevos (la columna `lessons.track` es libre, migración 0013). **Known issue fixed**: GET `/{lesson_id}` usa `selectinload(Lesson.exercises)` para evitar lazy-load errors en contexto async.

**Hidden tests (Pyodide)**: cada `ExerciseTemplate` puede llevar `hidden_tests` (JSON) que NO se exponen en `GET /lessons/{id}` ni `GET /exercises/lesson/{id}` (test de no-leak lo verifica). El worker Pyodide corre cada test en namespace fresco. Es el patrón base de validación replicable a todos los tracks. Datasets (`iris`, `ventas-pyme`, `encuestas`) se sirven via `/api/v1/datasets/{slug}/csv` y se consumen en Pyodide con `pycode.fetch_dataset_csv(slug)`; numpy/pandas/scipy/sklearn autocargan via `loadPackagesFromImports`.

**Capstones & Certificados**: `Capstone` (definicional por track) + `CapstoneSubmission` (uno por user, evaluado con `runCapstoneTests` multi-archivo en Pyodide). Aprobar un capstone (`status="passed"`) desbloquea `POST /certificates/{track}/issue` (gate server-side, 403 si no aprobó), que emite un `Certificate` con `verification_code` público verificable en `GET /certificates/verify/{code}` (sin auth). PDF con reportlab. Capstones actuales: `track-1-cli-ventas`, `track-2-eda-cafecito`, `track-3-diagnostico-ml`, `track-4-mlp-desde-cero`, `track-5-nebula-rag`. Aprobar exige **todos** los tests (`tests_passed == tests_total`). Un capstone que use LLM se corrige con un `llm_fn` falso inyectado en los tests; el real solo en un paso opcional.

**ELO multidominio & calidad de código**: `EloRating(user, domain, scope)` da ELO separado por actividad y categoría temática (`puzzle:<category>`, `challenge:<dificultad>`), con lazy-init desde el ELO global. `code_quality_service.analyze_code` calcula un `static_score` 0-100 con AST (sin ejecutar) que, combinado con los scores logic/general del evaluador LLM, se persiste en `CodeQualitySnapshot` y se grafica en `/progress/code-quality`.

Code execution: el endpoint `POST /api/v1/execute/run` retorna **410 Gone**; toda la ejecución de código del estudiante vive en [Pyodide en Web Worker](frontend/src/sandbox/pyodideWorker.ts) en el cliente. `POST /api/v1/execute/validate` solo corre `ast.parse` para detectar errores de sintaxis sin ejecutar. El backend nunca toca código del estudiante.

**Seguridad transversal** (capa middleware): [security_headers.py](backend/app/core/security_headers.py) (HSTS/CSP/XCTO/XFO/Referrer-Policy/Permissions-Policy), [rate_limit.py](backend/app/core/rate_limit.py) (SlowAPI con `_user_or_ip` keyfunc), [logging_config.py](backend/app/core/logging_config.py) (structlog + redact_pii), [observability.py](backend/app/core/observability.py) (Sentry no-op si no hay DSN). Todos se montan en `main.py`.

LLM: [llm_provider.py](backend/app/services/llm_provider.py) abstrae Groq + OpenAI + Stub. `get_provider(settings)` despacha por `LLM_PROVIDER`. Stub se usa cuando no hay API key — devuelve `""` y deja que el caller use fallback.

ELO system: puzzles, attempts, ratings, and rank progression live in [backend/app/services/elo_service.py](backend/app/services/elo_service.py) + [backend/app/models/elo_models.py](backend/app/models/elo_models.py). Rank deltas use step tables keyed by rating range (`ELO_DELTA_TABLE`, `ELO_DELTA_TABLE_ADVANCED`). El ELO multidominio (separado por track/categoría) vive en [elo_rating_service.py](backend/app/services/elo_rating_service.py) + [code_quality_service.py](backend/app/services/code_quality_service.py) para la progresión de calidad. The tutor prompt lives in the repo-root file referenced by `TUTOR_PROMPT_FILE` (default `maestro_evaluador_de_codigo_python.txt`) and is resolved via `settings.tutor_prompt_path`.

### Frontend (React + TS + Vite + Tailwind + Zustand)

Vite dev server proxies `/api` and `/ws` to `localhost:8000` ([vite.config.ts](frontend/vite.config.ts)) — frontend code should call relative paths, not absolute `http://localhost:8000`. `@/*` alias points to `src/`.

Global state: un único Zustand store [frontend/src/stores/authStore.ts](frontend/src/stores/authStore.ts) que maneja `accessToken` + `refreshToken` + `user`. API calls van por [frontend/src/services/api.ts](frontend/src/services/api.ts) (fetch nativo, no axios) — incluye interceptor que ante un 401 intenta `POST /auth/refresh` con el refresh token y reintenta el request original; si falla, limpia tokens y redirect a `/login`.

El **editor tiene dos modos**: libre (`/editor`) y lección (`/editor?lesson=<id>&exercise=<id>`). En modo lección carga `GET /lessons/{id}`, muestra la cabecera "Ejercicio N de M" y navega Anterior/Siguiente entre los ejercicios de esa lección sin salir del editor; la URL identifica el ejercicio activo (compartible/recargable).

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
