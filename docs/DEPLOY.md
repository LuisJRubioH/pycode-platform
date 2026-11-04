# Despliegue PyCode Platform v2

Revisado: 2026-11-03. Un push a `main` dispara la CI y los despliegues automáticos de Render y Vercel.

| Pieza | Servicio | URL |
|---|---|---|
| Frontend | Vercel Hobby | https://pycode-platform.vercel.app |
| Backend | Render Free (Docker) | https://pycode-backend.onrender.com |
| Base de datos | Supabase Postgres (free, sa-east-1, RLS) | — |
| Watchdog | UptimeRobot + workflow `keepalive-db.yml` | — |

## Backend (Render)

1. Crear cuenta en [render.com](https://render.com).
2. **New → Blueprint → conectar repo GitHub**.
3. Render detecta `render.yaml` y crea el servicio. El `CMD` del Dockerfile corre `alembic upgrade head` antes de uvicorn e instala `requirements.lock`.
4. **Settings → Environment**: pegar valores reales (los marcados `sync: false`):
   - `DATABASE_URL` (de Supabase, `postgresql+asyncpg://...?sslmode=require`)
   - `SECRET_KEY` (32 bytes o más: `openssl rand -hex 32`; con menos, PyJWT avisa)
   - `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`
   - `GROQ_API_KEY` (sin ella, tutor y proxy LLM caen al Stub y responden con texto de reserva)
   - `EMAIL_PROVIDER` (`brevo` | `sendgrid` | `mailjet` | `console`) + la clave del proveedor elegido (`BREVO_API_KEY`, `SENDGRID_API_KEY` o `MAILJET_API_KEY` + `MAILJET_API_SECRET`) y `EMAIL_FROM`. Render free **bloquea SMTP**: el correo sale por API HTTP. Ver [RECUPERACION_PASSWORD.md](RECUPERACION_PASSWORD.md).
   - `SENTRY_DSN` (opcional)
5. Revisar las que llevan valor en `render.yaml`, porque **la copia del dashboard gana** sobre el archivo:
   - `LLM_MODEL` = `openai/gpt-oss-120b` (Groq retiró `llama-3.3-70b-versatile` el 2026-08-16).
   - `CORS_ORIGINS` debe incluir el dominio exacto de Vercel, `https://pycode-platform.vercel.app`. El valor de `render.yaml` (`pycode.app`, `pycode.vercel.app`) está desfasado; el bueno es el del dashboard.
   - `FRONTEND_URL` = `https://pycode-platform.vercel.app` (con él se construyen el enlace de recuperación de contraseña y la URL de verificación de los certificados).
6. **Manual Deploy** la primera vez.

## Frontend (Vercel)

1. [vercel.com](https://vercel.com) → New Project → import repo.
2. Root directory: la **raíz del repo**. El `vercel.json` de la raíz fija el build (`cd frontend && npm ci && npm run build`), la salida (`frontend/dist`) y las cabeceras de seguridad; no hace falta configurarlos en el dashboard.
3. Environment Variables: ninguna. Los rewrites del `vercel.json` redirigen `/api` al backend Render y el resto a `index.html`. Dos salvedades:
   - El WebSocket del tutor **no** pasa por el rewrite: en producción `TutorChat.tsx` conecta directo a `wss://pycode-backend.onrender.com/ws/tutor`.
   - El rewrite no proxea rutas con **slash final** (devuelve `index.html` con 200): el front nunca debe llamarlas.

## Supabase

1. [supabase.com](https://supabase.com) → New Project (free tier).
2. **Project Settings → Database → Connection string**.
   Forma: `postgresql+asyncpg://postgres:PASSWORD@db.PROJECT.supabase.co:5432/postgres?sslmode=require`.
3. **Project Settings → API → anon key + service_role key**.
4. Las migraciones las aplica el backend en su `CMD`; no hace falta correrlas a mano.
5. El free tier se **pausa** tras ~7 días sin actividad de DB y tumba el siguiente deploy de Render. Si Render dice "deploy failed" con la CI verde, sospechar esto primero y restaurar el proyecto, sin tocar código.

## Monitoreo

- **UptimeRobot**: monitor HTTP(s) a `https://pycode-backend.onrender.com/health` cada **5 minutos** (Render free duerme tras 15 de inactividad).
- **`.github/workflows/keepalive-db.yml`**: cron cada 4 h contra `/health/db` (`SELECT 1`), para que Supabase no se pause. `/health` no genera actividad de DB.
- **`/health/llm?ping=1`**: comprobar tras cualquier cambio de modelo o de key. `healthy` = el modelo contestó; `degraded` = sin key; `unhealthy` = falla o responde vacío. El tutor degradado **no se nota** desde `/health`.

## Comprobación tras desplegar

1. `/health`, `/health/db` y `/health/llm?ping=1` responden bien.
2. Render muestra el commit en **Live** y Vercel en **Ready**.
3. Login en producción y abrir una lección; ejecutar un ejercicio en el editor (Pyodide) y pasar sus tests.
