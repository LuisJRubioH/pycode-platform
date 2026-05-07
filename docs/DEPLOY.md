# Despliegue PyCode Platform v2

## Backend (Render)

1. Crear cuenta en [render.com](https://render.com).
2. **New → Blueprint → conectar repo GitHub**.
3. Render detecta `render.yaml` y crea el servicio.
4. **Settings → Environment**: pegar valores reales (los marcados `sync: false`):
   - `DATABASE_URL` (de Supabase, Connection string tipo `postgresql+asyncpg://...`)
   - `SECRET_KEY` (generar con `openssl rand -hex 32`)
   - `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`
   - `GROQ_API_KEY`
   - `SENTRY_DSN` (opcional al inicio)
5. **Manual Deploy**.

## Frontend (Vercel)

1. [vercel.com](https://vercel.com) → New Project → import repo.
2. Root directory: `frontend`.
3. Build command: `npm run build`.
4. Output directory: `dist`.
5. Environment Variables: ninguna (los rewrites del `vercel.json` redirigen `/api` y `/ws` al backend Render).

## Supabase

1. [supabase.com](https://supabase.com) → New Project (free tier).
2. **Project Settings → Database → Connection string** (tipo `postgres+asyncpg`).
   Forma: `postgresql+asyncpg://postgres:PASSWORD@db.PROJECT.supabase.co:5432/postgres?sslmode=require`.
3. **Project Settings → API → anon key + service_role key**.
4. **SQL Editor**: ejecutar las migraciones manualmente o dejar que el backend Render lo haga en su CMD (`alembic upgrade head` antes de uvicorn).

## UptimeRobot

1. [uptimerobot.com](https://uptimerobot.com) → Add Monitor.
2. Type: HTTP(s).
3. URL: `https://pycode-backend.onrender.com/health`.
4. Interval: 14 minutos (Render free tier duerme tras 15 minutos de inactividad).
