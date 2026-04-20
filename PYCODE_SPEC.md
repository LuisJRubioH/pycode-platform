# PyCode Platform — Especificaciones de Implementación

> Documento para Claude Code. Cada sección es una unidad de trabajo independiente.
> Implementar en el orden indicado. No saltarse fases.

---

## Contexto del proyecto

**PyCode Platform** es una plataforma educativa de Python con:
- Editor Monaco con ejecución real en Docker
- Tutor socrático IA (guía por preguntas, no da respuestas directas)
- Sistema ELO de progreso inspirado en Finxter / Coffee Break Python
- Stack: FastAPI + SQLAlchemy async + PostgreSQL + React + TypeScript + TailwindCSS

**Archivos de referencia ya escritos** (integrar, no reescribir):
- `backend/app/services/elo_service.py` — lógica ELO completa
- `backend/app/models/elo_models.py` — modelos `UserProfile`, `Puzzle`, `PuzzleAttempt`, `EloHistory`
- `backend/app/schemas/elo_schemas.py` — schemas Pydantic
- `backend/app/api/elo_router.py` — endpoints ELO
- `backend/app/services/puzzle_seed.py` — 22 puzzles iniciales
- `frontend/src/components/ELODashboard.tsx` — dashboard de progreso
- `frontend/src/components/EloResultModal.tsx` — modal post-intento
- `frontend/src/store/eloStore.ts` — Zustand store ELO

---

## FASE 1 — Infraestructura crítica (hacer primero, sin excepción)

### 1.1 Configurar Alembic para migraciones

**Objetivo:** Gestión de esquema de base de datos con migraciones versionadas.

```
pip install alembic
alembic init alembic
```

**Tareas:**
- Configurar `alembic.ini` con `sqlalchemy.url` apuntando a la variable de entorno `DATABASE_URL`
- En `alembic/env.py`, importar `Base` de `app.models` y asignar `target_metadata = Base.metadata`
- Crear migración inicial: `alembic revision --autogenerate -m "initial_schema"`
- Aplicar: `alembic upgrade head`
- Añadir al `docker-compose.yml` un servicio `migrator` que corra `alembic upgrade head` antes del startup

**Archivos a crear/modificar:**
- `alembic.ini`
- `alembic/env.py`
- `alembic/versions/001_initial_schema.py`
- `docker-compose.yml` (servicio migrator)

---

### 1.2 Hardening del sandbox Docker de ejecución de código

**Objetivo:** Ejecución de código Python del usuario de forma segura y aislada.

**Implementar en `backend/app/services/code_runner.py`:**

```python
# Límites obligatorios por container:
DOCKER_CONFIG = {
    "mem_limit": "128m",           # RAM máxima
    "memswap_limit": "128m",       # Sin swap
    "cpu_period": 100000,
    "cpu_quota": 50000,            # 50% de 1 CPU
    "network_disabled": True,      # Sin acceso a red
    "read_only": True,             # Filesystem read-only
    "pids_limit": 64,              # Máximo 64 procesos
    "security_opt": ["no-new-privileges"],
}

EXECUTION_TIMEOUT_SECONDS = 10

# Lista blanca de módulos permitidos (rechazar imports fuera de esta lista)
ALLOWED_MODULES = {
    "math", "random", "datetime", "collections", "itertools",
    "functools", "string", "re", "json", "os.path",
    "numpy", "pandas",  # solo para puzzles avanzados
}
```

**Flujo de ejecución:**
1. Recibir código del usuario
2. Validar que no importa módulos fuera de `ALLOWED_MODULES`
3. Lanzar container Docker con los límites definidos
4. Capturar stdout/stderr con timeout de 10 segundos
5. Destruir el container inmediatamente tras la ejecución
6. Retornar output o error estructurado

**Endpoint a modificar:** `POST /api/code/run`

**Respuesta:**
```json
{
  "output": "string",
  "error": "string | null",
  "execution_time_ms": 150,
  "timed_out": false
}
```

---

### 1.3 Integrar el router ELO al main de FastAPI

**Archivo:** `backend/app/main.py`

Añadir:
```python
from app.api.elo_router import router as elo_router
app.include_router(elo_router, prefix="/api")
```

Registrar los modelos ELO en Alembic (ya incluidos en `elo_models.py`).

---

### 1.4 Rate limiting del tutor IA

**Objetivo:** Evitar costos descontrolados de la API de IA.

**Implementar en `backend/app/services/tutor_limiter.py`:**

```python
# Límites por plan
PLAN_LIMITS = {
    "free": 20,      # mensajes/día
    "pro": -1,       # ilimitado (-1)
    "teams": -1,
}
```

**Lógica:**
- Usar Redis para trackear `tutor_messages:{user_id}:{date}` con TTL de 24h
- Si el usuario supera el límite, retornar HTTP 429 con mensaje claro
- Incluir en la respuesta del endpoint headers: `X-Tutor-Remaining: N`

**Endpoint a modificar:** `POST /api/tutor/chat`

---

## FASE 2 — Sistema ELO (integrar archivos existentes)

### 2.1 Ejecutar seed de puzzles

**Archivo:** `backend/app/services/puzzle_seed.py` (ya existe)

Crear script `backend/scripts/seed_puzzles.py`:

```python
# Leer ALL_PUZZLES de puzzle_seed.py
# Para cada puzzle, hacer INSERT OR IGNORE en la tabla puzzles
# Log: "Insertados X puzzles nuevos, Y ya existían"
```

Añadir al `docker-compose.yml` como comando post-migración.

---

### 2.2 Endpoint de intento de puzzle

El endpoint `POST /api/elo/attempt` ya está en `elo_router.py`.

**Verificar que:**
- Llama a `process_attempt()` de `elo_service.py`
- Guarda registro en `PuzzleAttempt` y `EloHistory`
- Actualiza `UserProfile.streak_current` (reset a 0 si incorrecto)
- Retorna `PuzzleAttemptOut` completo

---

### 2.3 Integrar ELODashboard en el frontend

**Archivo:** `frontend/src/pages/Dashboard.tsx`

Importar y renderizar `ELODashboard` en la sección de progreso:

```tsx
import ELODashboard from "@/components/ELODashboard";

// En el JSX del Dashboard:
<section>
  <h2>Tu progreso</h2>
  <ELODashboard />
</section>
```

Instalar dependencia si no existe:
```
npm install recharts
```

---

### 2.4 Integrar EloResultModal en el editor

**Archivo:** `frontend/src/pages/Editor.tsx` (o donde esté el editor Monaco)

```tsx
import EloResultModal from "@/components/EloResultModal";
import { useEloStore } from "@/store/eloStore";

// Después de que el usuario submita respuesta:
const { submitAttempt, lastResult, clearLastResult } = useEloStore();

// Al confirmar respuesta en el editor:
const result = await submitAttempt(puzzleId, userAnswer, elapsedSeconds);

// Renderizar modal si hay resultado:
{lastResult && (
  <EloResultModal
    result={lastResult}
    onClose={clearLastResult}
    onNextPuzzle={handleNextPuzzle}
  />
)}
```

---

## FASE 3 — Mejoras del editor

### 3.1 Tests ocultos por ejercicio

**Objetivo:** El usuario no puede ver los tests; su código debe generalizarlos.

**Modelo:** Añadir columna a `Puzzle` en una nueva migración:

```python
hidden_tests = Column(JSON, nullable=True)
# Formato:
# [
#   {"input": "func(2, 3)", "expected": "5"},
#   {"input": "func(0, 0)", "expected": "0"},
# ]
```

**Servicio `backend/app/services/test_runner.py`:**

```python
async def run_hidden_tests(code: str, tests: list[dict]) -> dict:
    """
    Para cada test:
    1. Ejecutar el código del usuario + la llamada del test
    2. Comparar output con expected
    3. Retornar resumen: passed, failed, total
    """
    results = []
    for test in tests:
        full_code = f"{code}\nprint({test['input']})"
        output = await run_in_sandbox(full_code)
        results.append({
            "passed": output.strip() == test["expected"],
            "input": test["input"],   # no revelar el expected al usuario
        })
    return {
        "passed": sum(r["passed"] for r in results),
        "total": len(results),
        "all_passed": all(r["passed"] for r in results),
        "details": results,
    }
```

**Endpoint:** `POST /api/puzzles/{puzzle_id}/test`

**Frontend:** Mostrar barra de progreso de tests: `✓ 3/5 tests pasando`

---

### 3.2 Historial de intentos por ejercicio

**Endpoint:** `GET /api/puzzles/{puzzle_id}/attempts`

Retorna los últimos 10 intentos del usuario en ese puzzle específico:

```json
[
  {
    "attempt_number": 3,
    "correct": false,
    "user_answer": "5",
    "elo_delta": -46,
    "created_at": "2026-04-11T10:30:00Z"
  }
]
```

**Frontend:** Panel colapsable debajo del editor "Tus intentos anteriores" con el código de cada intento y si pasó o no.

---

### 3.3 Debugger visual paso a paso

**Objetivo:** Mostrar el estado de variables línea a línea.

**Implementar en `backend/app/services/debugger.py`** usando el módulo `bdb` de Python:

```python
import bdb
import sys
from io import StringIO

def trace_execution(code: str) -> list[dict]:
    """
    Ejecuta el código línea a línea y captura el estado
    de las variables locales en cada paso.
    Retorna lista de snapshots ordenados por línea.
    """
    steps = []

    class Tracer(bdb.Bdb):
        def user_line(self, frame):
            steps.append({
                "line": frame.f_lineno,
                "locals": {
                    k: repr(v)
                    for k, v in frame.f_locals.items()
                    if not k.startswith("__")
                },
            })

    tracer = Tracer()
    # Ejecutar en sandbox con timeout
    tracer.run(code)
    return steps
```

**Endpoint:** `POST /api/code/debug`

**Respuesta:**
```json
{
  "steps": [
    {"line": 1, "locals": {}},
    {"line": 2, "locals": {"x": "5"}},
    {"line": 3, "locals": {"x": "5", "y": "10"}}
  ]
}
```

**Frontend `frontend/src/components/Debugger.tsx`:**
- Botón "Ejecutar paso a paso" junto al botón "Run"
- Panel lateral que muestra tabla de variables actualizada en cada paso
- Highlight de la línea activa en Monaco via `editor.deltaDecorations()`
- Controles: ← anterior | → siguiente | ⏭ ir al final

---

## FASE 4 — Tutor socrático mejorado

### 4.1 Memoria de errores recurrentes por usuario

**Objetivo:** El tutor recuerda qué conceptos le cuestan al usuario.

**Modelo `backend/app/models/elo_models.py`** — añadir tabla:

```python
class UserWeakness(Base):
    __tablename__ = "user_weaknesses"

    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer, ForeignKey("users.id"))
    topic       = Column(String(100))   # "loops", "indexing", "recursion"
    fail_count  = Column(Integer, default=0)
    last_failed = Column(DateTime)
    updated_at  = Column(DateTime, onupdate=datetime.utcnow)
```

**Lógica:**
- Cada vez que un usuario falla un puzzle, incrementar `fail_count` para el `topic` del puzzle
- En `POST /api/tutor/chat`, incluir en el system prompt del tutor las top-3 debilidades del usuario:

```python
weaknesses_context = """
El usuario tiene dificultades recurrentes con: indexing (8 fallos), loops (5 fallos).
Cuando el código del usuario involucre estos conceptos, prioriza preguntas sobre ellos.
"""
```

---

### 4.2 Detección de errores semánticos en el tutor

**Archivo:** `backend/app/services/tutor_service.py`

El system prompt del tutor debe incluir estas instrucciones obligatorias:

```
Eres un tutor socrático de Python. NUNCA des la respuesta directamente.
En cambio:
1. Identifica QUÉ intentaba hacer el usuario (intención semántica)
2. Haz UNA sola pregunta que le acerque a descubrir el error por sí mismo
3. Si el usuario pregunta "¿cómo se hace X?", responde con "¿Qué pasa si intentas Y?"
4. Usa el código del usuario como contexto, no lo corrijas directamente
5. Si el usuario lleva 3 intentos fallidos en el mismo concepto, puedes dar una pista más directa
```

**Contexto adicional a incluir en cada llamada:**
- Código actual del usuario en el editor
- Output que recibió vs output esperado
- Número de intentos en este puzzle
- Top-3 debilidades del usuario (de `UserWeakness`)

---

## FASE 5 — Gamificación y progreso

### 5.1 Mapa de competencias por concepto

**Endpoint:** `GET /api/elo/competency-map`

Calcula el nivel de dominio (0–100) por topic a partir de los `PuzzleAttempt`:

```python
def calculate_competency(attempts: list[PuzzleAttempt], topic: str) -> int:
    topic_attempts = [a for a in attempts if a.puzzle.topic == topic]
    if not topic_attempts:
        return 0
    correct = sum(1 for a in topic_attempts if a.correct)
    # Peso por ELO del puzzle: fallar un puzzle fácil penaliza más
    weighted_score = sum(
        (a.puzzle.elo_rating / 1000) * (1 if a.correct else -0.5)
        for a in topic_attempts
    )
    return max(0, min(100, int((weighted_score / len(topic_attempts)) * 50 + 50)))
```

**Respuesta:**
```json
{
  "competencies": [
    {"topic": "variables",   "level": 85, "attempts": 12},
    {"topic": "loops",       "level": 60, "attempts": 8},
    {"topic": "functions",   "level": 45, "attempts": 5},
    {"topic": "recursion",   "level": 20, "attempts": 3}
  ]
}
```

**Frontend `frontend/src/components/CompetencyMap.tsx`:**
- Grid de tarjetas por topic, cada una con barra de progreso de color según nivel
- Verde (≥80) / Amarillo (50–79) / Rojo (<50)
- Al hacer click en una tarjeta, mostrar puzzles de ese topic ordenados por ELO

---

### 5.2 Puzzle del día público

**Endpoint:** `GET /api/puzzles/daily` (sin autenticación)

```python
import hashlib
from datetime import date

def get_daily_puzzle_id() -> int:
    """
    Selecciona un puzzle determinístico por fecha.
    Mismo puzzle para todos los usuarios el mismo día.
    """
    today = date.today().isoformat()   # "2026-04-11"
    hash_val = int(hashlib.md5(today.encode()).hexdigest(), 16)
    # Mapear al rango de IDs de puzzles activos
    return (hash_val % total_active_puzzles) + 1
```

**Respuesta pública** (sin solución ni ELO del puzzle):
```json
{
  "id": 7,
  "title": "Lambda Function",
  "code_snippet": "square = lambda x: x ** 2\nprint(square(4))",
  "category": "python",
  "difficulty_label": "Medium",
  "solvers_today": 142,
  "date": "2026-04-11"
}
```

**Endpoint:** `POST /api/puzzles/daily/submit` (requiere auth)
- Procesar igual que un intento normal
- Incrementar contador `solvers_today` en Redis

**Frontend:** Página `/daily` con el puzzle, contador de solvers y CTA de registro.

---

### 5.3 Certificado de módulo completado

**Trigger:** Cuando un usuario completa todos los puzzles de una categoría con al menos 1 correcto en cada uno.

**Servicio `backend/app/services/certificate_service.py`:**

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_certificate(
    user_name: str,
    module_name: str,      # "Python Fundamentals", "NumPy Basics", etc.
    completion_date: str,
    final_elo: int,
    rank: str,
) -> bytes:
    """
    Genera PDF con:
    - Nombre del usuario
    - Módulo completado
    - ELO alcanzado y rango
    - Fecha de completitud
    """
```

**Endpoint:** `GET /api/certificates/{module}` — retorna PDF para descarga.

**Instalar:** `pip install reportlab`

---

## FASE 6 — Observabilidad

### 6.1 Logging estructurado

**Instalar:** `pip install structlog sentry-sdk`

**Archivo:** `backend/app/core/logging.py`

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)

log = structlog.get_logger()
```

**Eventos a loguear obligatoriamente:**
- `puzzle.attempt` — `{user_id, puzzle_id, correct, elo_delta, time_spent}`
- `tutor.message` — `{user_id, message_count_today, puzzle_id}`
- `code.execution` — `{user_id, timed_out, execution_ms, error_type}`
- `elo.rank_change` — `{user_id, rank_before, rank_after, elo}`

**Integrar Sentry** para errores no capturados:
```python
import sentry_sdk
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=0.1)
```

---

## Variables de entorno requeridas

Añadir al `.env.example`:

```env
# Base de datos
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/pycode
REDIS_URL=redis://localhost:6379

# IA
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Observabilidad
SENTRY_DSN=https://...

# Seguridad
SECRET_KEY=cambiar-en-produccion
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Docker sandbox
DOCKER_IMAGE_PYTHON=python:3.11-alpine
```

---

## Orden de implementación recomendado

```
FASE 1 (bloqueante para todo lo demás)
  └─ 1.1 Alembic
  └─ 1.2 Sandbox hardening
  └─ 1.3 Integrar router ELO
  └─ 1.4 Rate limiting tutor

FASE 2 (integrar archivos ya escritos)
  └─ 2.1 Seed de puzzles
  └─ 2.2 Verificar endpoint attempt
  └─ 2.3 ELODashboard en frontend
  └─ 2.4 EloResultModal en editor

FASE 3 (editor mejorado)
  └─ 3.1 Tests ocultos
  └─ 3.2 Historial de intentos
  └─ 3.3 Debugger paso a paso

FASE 4 (tutor mejorado)
  └─ 4.1 Memoria de debilidades
  └─ 4.2 System prompt socrático

FASE 5 (gamificación)
  └─ 5.1 Mapa de competencias
  └─ 5.2 Puzzle del día
  └─ 5.3 Certificados

FASE 6 (observabilidad)
  └─ 6.1 Logging + Sentry
```

---

## Dependencias Python a añadir a `requirements.txt`

```
alembic==1.13.1
structlog==24.1.0
sentry-sdk[fastapi]==1.45.0
reportlab==4.1.0
redis==5.0.1
```

## Dependencias npm a añadir a `package.json`

```
recharts ^2.12.0
```

---

*Generado en base al análisis de Coffee Break Python, Coffee Break NumPy y Coffee Break Pandas (Christian Mayer / Finxter) y el código del sistema ELO implementado para PyCode Platform.*
