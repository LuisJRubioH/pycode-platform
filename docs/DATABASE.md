# Esquema de base de datos — PyCode Platform

Referencia del modelo de datos. Postgres 17 (Supabase en prod), gestionado con **Alembic** (migraciones `0001`→`0017`). El schema se introspectó desde la DB de producción y se completa con los modelos de las migraciones posteriores; para el diseño técnico general ver [ARCHITECTURE.md](ARCHITECTURE.md).

- **23 tablas** de dominio + `alembic_version` (bookkeeping de migraciones).
- Todas las PK son `id integer` autoincremental.
- Las FKs hacia `users.id` llevan `ON DELETE CASCADE` (necesario para `DELETE /users/me` GDPR sin huérfanos).
- **RLS** (Row-Level Security) habilitada por tabla en las de datos por-usuario (ver §5). El backend conecta con el rol Postgres directo (que *bypasea* RLS por ser owner) y **además** filtra por `user_id` en cada query; RLS es la segunda línea de defensa frente al rol `anon` de Supabase.
- Contenido JSON: se usa `jsonb` para lo consultable y `json` para lo que solo se serializa.

Última introspección: 2026-07 (migración `0014`). Revisado contra los modelos el **2026-11-03** (migraciones `0015`-`0017`).

---

## 1. Identidad y autenticación

### `users` — cuentas
| Columna | Tipo | Notas |
|---|---|---|
| id | integer PK | |
| email | varchar NOT NULL | único |
| username | varchar NOT NULL | snapshot para certificados |
| hashed_password | varchar NOT NULL | bcrypt |
| is_active | boolean | |
| is_admin | boolean | |
| created_at, last_login | timestamp | |

### `user_profiles` — perfil + ELO global (1:1 con user)
`user_id` FK · `level`, `xp_points`, `badges`, `preferences` · **ELO global**: `elo_rating`, `elo_peak`, `rank`, `puzzles_attempted`, `puzzles_correct`, `streak_current`, `streak_best`, `last_activity`.

### `refresh_tokens` — rotación de JWT
`user_id` FK · `jti` (identificador del token) · `expires_at` · `revoked` (bool; `logout` lo marca). Habilita la rotación de refresh tokens y su revocación.

### `password_reset_tokens` — recuperación de contraseña (migración `0017`)
| Columna | Tipo | Notas |
|---|---|---|
| id | integer PK | |
| user_id | integer FK → users | `ON DELETE CASCADE` |
| token_hash | varchar(64) | **SHA-256** del token, único; el token en claro nunca se guarda |
| expires_at | timestamp NOT NULL | caducidad |
| used_at | timestamp NULL | `NULL` mientras no se canjea; un token usado no vuelve a servir |
| created_at | timestamp | |

Índice `(user_id, used_at)`. **Sin RLS** a propósito: el flujo ocurre sin sesión, así que no hay `app.current_user_id`; la defensa es el diseño del token. Ver [RECUPERACION_PASSWORD.md](RECUPERACION_PASSWORD.md).

---

## 2. Contenido educativo (definicional, mayormente público)

### `lessons` — lecciones (58 en el seed, 7 tracks)
| Columna | Tipo | Notas |
|---|---|---|
| id | integer PK | |
| title | varchar NOT NULL | clave natural del upsert idempotente |
| description, content | text | `content` = markdown de la teoría |
| difficulty, category | varchar | `category` agrupa en el mapa de competencias |
| order | integer | orden curricular (Track 0 usa órdenes **negativos** para ir antes de Track 1) |
| estimated_duration | integer | minutos |
| prerequisites | json | |
| track | varchar NOT NULL | `track-0`..`track-6` (migración `0013`) |
| is_active, created_at, updated_at | | |

### `exercises` — ejercicios de cada lección (258 en el seed: 198 de código + 60 de Track 0)
`lesson_id` FK · `title`, `description`, `instructions`, `starter_code`, `solution_code` · `test_cases` (json, legacy) · `hints` (json) · `points`, `difficulty`, `order` · **`hidden_tests` (json)** — tests Pyodide que **nunca** se exponen en la API (migración `0007`; guard rail con test de no-leak) · **`exercise_type`** (varchar(32), default `code`; Track 0: `trace_table`, `predict_output`, `mcq`, `flowchart_match`, `flowchart_fill`) · **`spec`** (json, **público**: pseudocódigo, columnas de la traza, opciones, nodos del diagrama) · **`answer_key`** (json, **privada**: la corrige el backend en `POST /exercises/{id}/check` y nunca sale de la API) — las tres de la migración `0016`.

### `capstones` — proyectos que cierran cada track (7 seedeados, uno por track)
`slug` (único), `track`, `title`, `short_description`, `description` (markdown) · `requirements` (jsonb), `starter_files` (jsonb) · **`hidden_tests` (jsonb)** — evaluados en Pyodide, no se serializan en el detalle · `estimated_hours`, `difficulty`, `order_index`, `is_active`. **Tabla pública (sin RLS)** — ver caveat §5.

### `datasets` — datasets servidos como CSV a Pyodide (Track 2)
`slug`, `name`, `description`, `source_url`, `license` · `columns_schema` (json), `sample_rows` (json), **`csv_content` (text)**, `row_count`, `is_active`. Servido por `GET /api/v1/datasets/{slug}/csv`.

### `coding_challenges` — retos (25 problemas × 3 niveles + 10 curados)
`title`, `slug`, `source`, `source_path`, `difficulty`, `topic`, `prompt`, `starter_code` · **`reference_solution` (text)** — no se sirve nunca (guard rail) · **`hidden_tests` (json)** (migración `0015`) — los pide el editor en `GET /challenges/{id}/hidden-tests` · `order_index`, `is_active`. El contenido lo sincroniza el seed desde `generated_bank.py`, `curated_retos.py` y `retos_validacion.py`.

### `puzzles` — puzzles ELO (predice-la-salida, estilo Finxter)
`title`, `slug`, `category`, `topic`, `code_snippet` · **`correct_output`, `explanation`, `hint`** — no se filtran en endpoints públicos (puzzle del día) · `elo_rating`, `elo_initial`, `times_attempted`, `times_correct`, `is_advanced`, `is_active` · `finxter_id`, `source_book`.

---

## 3. Progreso y actividad del usuario (por-usuario, con RLS)

### `user_progress` — progreso por lección
`user_id` FK, `lesson_id` FK · `status` (`in_progress`/`completed`), `progress`, `score`, `time_spent`, `attempts`, `started_at`, `completed_at`, `last_accessed`.

### `code_submissions` — envíos de ejercicios
`user_id` FK, `exercise_id` FK · `code`, `result` (`success`/…), `output`, `error_message`, `execution_time`, `passed_tests`, `total_tests`.

### `code_evaluations` — evaluaciones del tutor evaluador
`user_id` FK, `exercise_id` FK (nullable) · `problem_description`, `code`, `expected_output`, `actual_output` · **`verdict` (jsonb)** — salida estructurada del LLM · `model_used`. La produce `POST /tutor/evaluate`.

### `code_quality_snapshots` — progresión de calidad de código
`user_id` FK · `source` (`evaluation`), `reference_id` · `logic_score`, `general_score` (del LLM), **`static_score`** (análisis AST sin ejecutar), `metrics` (jsonb). Serie temporal para `/progress/code-quality`.

### `tutor_sessions` — sesiones Q&A del tutor
`user_id` FK, `lesson_id` FK (nullable) · `messages` (json, historial del WS `/ws/tutor`).

### `ai_feedback` — feedback sobre respuestas del tutor
`session_id`, `message_index`, `helpful_rating`, `feedback_text`. (Sin RLS.)

### `capstone_submissions` — envíos de capstone (uno por user/capstone)
`user_id` FK, `capstone_id` FK · `files` (jsonb, código del alumno) · `status` (`passed`/`failed`), `tests_passed`, `tests_total`, `test_results` (jsonb). `status="passed"` desbloquea el certificado del track.

### `challenge_completions` — retos resueltos
`user_id` FK, `challenge_id` FK · `completed_at` · **`elo_delta`** (migración `0011`) — permite revertir el ELO exacto al des-completar. Desde `0015` una fila solo se crea si el cliente reporta todos los tests del reto aprobados.

### `certificates` — certificados verificables (públicos)
`user_id` FK, `capstone_id` FK (nullable), `track`, `title` · **`recipient_name`** (snapshot del username al emitir) · **`verification_code`** (`PYC-XXXX-XXXX`, capacidad impredecible), `issued_at`. `UniqueConstraint(user_id, track)`. Verificable sin auth en `GET /certificates/verify/{code}`. **Tabla pública (sin RLS)** — ver caveat §5.

---

## 4. Sistema ELO

Tres capas conviven (backward-compatible):

- **`user_profiles`** (§1) — ELO global/overall clásico.
- **`elo_ratings`** — ELO **multidominio** (migración `0010`): `user_id` FK, `domain`, `scope` (p.ej. `puzzle:<category>`, `challenge:<dificultad>`), `elo_rating`, `elo_peak`, `rank`, `attempts`, `correct`, `streak_current`, `streak_best`, `last_activity`. Lazy-init desde el ELO global.
- **`puzzle_attempts`** — cada intento de puzzle: `user_id` FK, `puzzle_id` FK, `correct`, `user_answer`, `user_elo_before/after`, `puzzle_elo_before/after`, `elo_delta_user`, `elo_delta_puzzle`, `expected_probability`, `time_spent_seconds`.
- **`elo_history`** — histórico de cambios de ELO: `user_profile_id`, `puzzle_id`, `attempt_id`, `elo_value`, `delta`, `correct`, `rank_label`, `puzzle_title`, `category`, `domain`. (Sin RLS.)

---

## 5. Row-Level Security (RLS) y caveat de seguridad

**Modelo**: las tablas por-usuario tienen RLS habilitada (migración `0004`) con políticas que filtran por `current_setting('app.current_user_id')`. El backend setea ese valor por sesión de DB, pero como conecta con el rol Postgres **owner**, RLS se bypasea para la app; la app filtra por `user_id` en cada query. **RLS protege específicamente frente al rol `anon`** de Supabase (PostgREST).

**RLS habilitada** (15): `users`, `user_profiles`, `refresh_tokens`, `lessons`, `exercises`, `user_progress`, `code_submissions`, `code_evaluations`, `code_quality_snapshots`, `tutor_sessions`, `puzzles`, `puzzle_attempts`, `elo_ratings`, `challenge_completions`, `capstone_submissions`.

**RLS deshabilitada** (8): `capstones`, `certificates`, `datasets`, `coding_challenges`, `ai_feedback`, `elo_history`, `password_reset_tokens` (sin sesión, ver §1), `alembic_version`.

> ⚠️ **Caveat de seguridad (advisory de Supabase)**: las tablas sin RLS quedan expuestas al rol `anon`/`authenticated` si el API PostgREST de Supabase está accesible con la anon key. Tres son públicas por diseño y de bajo riesgo (`datasets`, contenido; `alembic_version`, bookkeeping). Pero **`capstones.hidden_tests`** (tests ocultos) y **`certificates`** (nombres + códigos de verificación) contienen datos que la API de PyCode oculta a propósito — si PostgREST está abierto, se podrían leer directamente por la anon key, saltándose ese guard rail. **Acción sugerida** (no aplicada automáticamente): verificar si PostgREST está expuesto en el proyecto Supabase y, si aplica, habilitar RLS con políticas de solo-lectura adecuadas (p.ej. `certificates` accesible solo por `verification_code`), o restringir el acceso del rol anon. No habilitar RLS sin políticas: bloquearía todo acceso.

---

## 6. Migraciones (Alembic)

| # | Migración | Contenido |
|---|---|---|
| 0001 | initial_schema | Tablas base (users, lessons, exercises, progress, puzzles, ...) |
| 0002 | refresh_tokens | Rotación de JWT |
| 0003 | cascade_user_fks | `ON DELETE CASCADE` en FKs a users (Postgres) |
| 0004 | enable_rls_per_user_tables | Políticas RLS (Postgres-only) |
| 0005 | code_evaluations | Evaluaciones del tutor evaluador |
| 0006 | challenge_completions | Completado de retos (auto-marcado hasta `0015`) |
| 0007 | exercise_hidden_tests | Columna `exercises.hidden_tests` |
| 0008 | capstones | `capstones` + `capstone_submissions` |
| 0009 | certificates | Certificados verificables |
| 0010 | elo_ratings | ELO multidominio + `elo_history.domain` |
| 0011 | challenge_completion_elo_delta | Columna `elo_delta` para revertir |
| 0012 | code_quality_snapshots | Snapshots de calidad de código |
| 0013 | lesson_track | Columna `lessons.track` (multi-track) |
| 0014 | datasets | Datasets seedeables servidos como CSV |
| 0015 | challenge_hidden_tests | Columna `coding_challenges.hidden_tests`: completar un reto exige pasar sus tests |
| 0016 | exercise_types | `exercises.exercise_type` + `spec` + `answer_key` (ejercicios no ejecutables de Track 0) |
| 0017 | password_reset_tokens | Tokens de recuperación de contraseña (sin RLS) |

Los Tracks 3 a 6 (incluido el proxy LLM) **no añadieron migraciones**: el contenido nuevo son filas seedeadas y el proxy LLM no persiste datos. Track 0 solo necesitó la `0016`.

**Regla DDL Postgres-only** (RLS y similares): el `upgrade()` empieza con `if op.get_bind().dialect.name != "postgresql": return`, para ser no-op en SQLite (los tests usan SQLite).
