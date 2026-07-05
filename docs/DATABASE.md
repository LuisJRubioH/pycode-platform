# Esquema de base de datos — PyCode Platform

Referencia del modelo de datos. Postgres 17 (Supabase en prod), gestionado con **Alembic** (migraciones `0001`→`0014`). El schema lo introspecta este documento desde la DB de producción; para el diseño técnico general ver [ARCHITECTURE.md](ARCHITECTURE.md).

- **22 tablas** de dominio + `alembic_version` (bookkeeping de migraciones).
- Todas las PK son `id integer` autoincremental.
- Las FKs hacia `users.id` llevan `ON DELETE CASCADE` (necesario para `DELETE /users/me` GDPR sin huérfanos).
- **RLS** (Row-Level Security) habilitada por tabla en las de datos por-usuario (ver §5). El backend conecta con el rol Postgres directo (que *bypasea* RLS por ser owner) y **además** filtra por `user_id` en cada query; RLS es la segunda línea de defensa frente al rol `anon` de Supabase.
- Contenido JSON: se usa `jsonb` para lo consultable y `json` para lo que solo se serializa.

Última introspección: 2026-07 (migración `0014`).

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

---

## 2. Contenido educativo (definicional, mayormente público)

### `lessons` — lecciones (55 en el seed, multi-track)
| Columna | Tipo | Notas |
|---|---|---|
| id | integer PK | |
| title | varchar NOT NULL | clave natural del upsert idempotente |
| description, content | text | `content` = markdown de la teoría |
| difficulty, category | varchar | `category` agrupa en el mapa de competencias |
| order | integer | orden de display |
| estimated_duration | integer | minutos |
| prerequisites | json | |
| track | varchar NOT NULL | `track-1`..`track-5` (migración `0013`) |
| is_active, created_at, updated_at | | |

### `exercises` — ejercicios de cada lección (~130 en el seed)
`lesson_id` FK · `title`, `description`, `instructions`, `starter_code`, `solution_code` · `test_cases` (json, legacy) · `hints` (json) · `points`, `difficulty`, `order` · **`hidden_tests` (json)** — tests Pyodide que **nunca** se exponen en la API (migración `0007`; guard rail con test de no-leak).

### `capstones` — proyectos que cierran cada track (4 seedeados)
`slug` (único), `track`, `title`, `short_description`, `description` (markdown) · `requirements` (jsonb), `starter_files` (jsonb) · **`hidden_tests` (jsonb)** — evaluados en Pyodide, no se serializan en el detalle · `estimated_hours`, `difficulty`, `order_index`, `is_active`. **Tabla pública (sin RLS)** — ver caveat §5.

### `datasets` — datasets servidos como CSV a Pyodide (Track 2)
`slug`, `name`, `description`, `source_url`, `license` · `columns_schema` (json), `sample_rows` (json), **`csv_content` (text)**, `row_count`, `is_active`. Servido por `GET /api/v1/datasets/{slug}/csv`.

### `coding_challenges` — retos autoevaluados
`title`, `slug`, `source`, `source_path`, `difficulty`, `topic`, `prompt`, `starter_code` · **`reference_solution` (text)** — no se sirve en el detalle (guard rail) · `order_index`, `is_active`.

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

### `challenge_completions` — auto-marcado de retos
`user_id` FK, `challenge_id` FK · `completed_at` · **`elo_delta`** (migración `0011`) — permite revertir el ELO exacto al des-completar.

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

**RLS deshabilitada** (7): `capstones`, `certificates`, `datasets`, `coding_challenges`, `ai_feedback`, `elo_history`, `alembic_version`.

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
| 0006 | challenge_completions | Auto-marcado de retos |
| 0007 | exercise_hidden_tests | Columna `exercises.hidden_tests` |
| 0008 | capstones | `capstones` + `capstone_submissions` |
| 0009 | certificates | Certificados verificables |
| 0010 | elo_ratings | ELO multidominio + `elo_history.domain` |
| 0011 | challenge_completion_elo_delta | Columna `elo_delta` para revertir |
| 0012 | code_quality_snapshots | Snapshots de calidad de código |
| 0013 | lesson_track | Columna `lessons.track` (multi-track) |
| 0014 | datasets | Datasets seedeables servidos como CSV |

Los Tracks 3, 4 y 5 (incluido el proxy LLM) **no añadieron migraciones**: el contenido nuevo son filas seedeadas y el proxy LLM no persiste datos.

**Regla DDL Postgres-only** (RLS y similares): el `upgrade()` empieza con `if op.get_bind().dialect.name != "postgresql": return`, para ser no-op en SQLite (los tests usan SQLite).
