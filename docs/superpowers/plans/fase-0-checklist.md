# Fase 0 — Checklist de salida

Estado al 2026-05-08. **Fase 0 cerrada (30/30).** Smoke test pasó
contra producción real (Render + Vercel + Supabase + UptimeRobot).
Tag `fase-0-complete` aplicado.

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
- [x] RLS habilitada en `users`, `user_profiles`, `user_progress`,
  `code_submissions`, `tutor_sessions`, `refresh_tokens`,
  `puzzle_attempts` con políticas
  `USING (user_id = current_setting('app.current_user_id', true)::int)`;
  `lessons`/`exercises`/`puzzles` con `_public_read`. Migración 0004
  no-op en SQLite. Validada contra Postgres 16 local (10/10 tablas
  con `rowsecurity=true`).
  — Task 18
- [x] Test suite cross-user (5 tests) que valida en SQLite la defensa
  app-layer y en Postgres la doble defensa con RLS:
  `test_user_lookup_by_id_not_exposed`, `test_export_only_returns_own_data`,
  `test_progress_isolated_per_user`,
  `test_delete_me_does_not_affect_other_user`,
  `test_a_cannot_use_b_token_after_logout`.
  — Task 19

- [x] Smoke test contra producción — Task 29:
  - `https://pycode-backend.onrender.com/health` → 200 + 6 headers
    seguros (HSTS, CSP, XCTO, XFO, Referrer-Policy, Permissions-Policy)
  - Auth flow: `POST /auth/register` → 201, `POST /auth/login` → JWT,
    `GET /lessons/` con Bearer → 200 (25 lecciones seedeadas)
  - GDPR: `DELETE /me` purga al usuario y dependientes en cascada
  - Frontend Vercel: registro/login/dashboard/editor con Pyodide
    funcionando contra el backend de Render via rewrite
  - Tutor IA conectado por WS directo a Render (Vercel Hobby no
    proxea WS); Groq responde en estilo socrático
  - UptimeRobot pingueando `/health` cada 5min para evitar cold start
- [x] Cleanup final + tag `fase-0-complete` — Task 30

## Producción

| Servicio | URL | Notas |
|---|---|---|
| Frontend | https://pycode-platform.vercel.app | Vercel Hobby, Vite build |
| Backend | https://pycode-backend.onrender.com | Render Free, Docker |
| DB | Supabase Postgres `medutbqsurjnaaymmrin` | sa-east-1, RLS habilitada |
| Watchdog | UptimeRobot monitor `pycode-backend health` | HTTP 5min |
