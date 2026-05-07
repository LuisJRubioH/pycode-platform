# Fase 0 — Checklist de salida

Estado al 2026-05-06. **25 de 30 tasks completadas.** RLS (18-19) y deploy
real (29) quedan pendientes hasta la siguiente sesión con Postgres
disponible y proyectos creados en Render/Vercel/Supabase.

## Hecho

- [x] Postgres + Alembic en producción (sin SQLite, sin `create_all`)
  — Tasks 3, 4, 5
- [x] Lint anti-SQLi en CI (`backend/scripts/check_no_sqli.py`)
  — Task 6
- [x] Pydantic strict en endpoints públicos
  — Task 7
- [x] Headers de seguridad
  (HSTS / CSP / X-Content-Type-Options / X-Frame-Options /
  Referrer-Policy / Permissions-Policy)
  — Task 8
- [x] CORS whitelist (sin wildcard en prod, raise si aparece `*`
  con `ENVIRONMENT=production`)
  — Task 9
- [x] Rate limiting universal con SlowAPI (login 5/min, register 3/h,
  tutor 50/día, default 100/min)
  — Task 10
- [x] Logging estructurado con redaction PII (JWT, gsk_, sk-, hf_,
  emails)
  — Task 11
- [x] Sentry SDK integrado con `before_send` scrubbing — no-op si
  `SENTRY_DSN` vacío
  — Task 12
- [x] `/health` slim sin info sensible (sin version, sin DB, sin URL
  de docs)
  — Task 13
- [x] `/api/v1/execute/run` retorna 410 GONE; backend deja de ejecutar
  código del estudiante
  — Task 14
- [x] Provider abstraction LLM (Groq + OpenAI + Stub fallback)
  — Task 15
- [x] JWT con refresh token rotation + endpoint `/auth/logout` que
  revoca el `jti`
  — Task 16
- [x] GDPR: `DELETE /api/v1/users/me` (purga vía CASCADE) y
  `GET /api/v1/users/me/export` (JSON con datos del usuario)
  — Task 17
- [x] Dependabot semanal (pip / npm / actions) + job `audit` en CI
  con `pip-audit` + `npm audit`
  — Task 20
- [x] `requirements.lock` commiteado; `.venv*/` ignorado
  — Task 21
- [x] Pyodide en Web Worker reemplaza subprocess executor
  — Tasks 22, 23, 24
- [x] Frontend: refresh automático del access_token via interceptor
  fetch
  — Task 25
- [x] Dockerfile backend con `alembic upgrade head` en startup
  — Task 26
- [x] Render blueprint (`render.yaml`) + documentación
  (`docs/DEPLOY.md`)
  — Task 27
- [x] Vercel config (`vercel.json`) con rewrites a Render y headers
  replicados
  — Task 28

## Pendiente

- [ ] **RLS habilitada por tabla con datos de usuario** — Task 18.
  Bloqueador: requiere Postgres real (RLS no existe en SQLite).
  Migración `0004_enable_rls_per_user_tables.py` toca `user_profiles`,
  `user_progress`, `code_submissions`, `tutor_sessions`,
  `refresh_tokens` con políticas
  `USING (user_id = current_setting('app.current_user_id', true)::int)`.
- [ ] **Test suite cross-user RLS** — Task 19.
  Bloqueador: depende de Task 18 + ejecución contra Postgres.
- [ ] **Smoke test full-stack contra entorno staging** — Task 29.
  Bloqueador: depende de proyectos creados en Render + Vercel +
  Supabase + UptimeRobot (operativo, no código).

## Cómo retomar

1. Levantar Postgres local (o crear branch en Supabase).
2. Aplicar Tasks 18 → 19 contra ese Postgres siguiendo el plan
   (sec. 18 y 19 de
   `docs/superpowers/plans/2026-05-03-fase-0-fundamentos-seguridad.md`).
3. Crear cuentas Render + Vercel + Supabase + UptimeRobot,
   aprovisionar usando `render.yaml`, `vercel.json` y los pasos de
   `docs/DEPLOY.md`.
4. Ejecutar Task 29 contra el entorno staging.
5. Cuando todo esté verde, marcar este checklist completo y crear el
   tag `fase-0-complete`.
