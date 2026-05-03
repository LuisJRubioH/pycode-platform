# PyCode Platform v2 — Plataforma de Estudio para AI Engineer

**Fecha:** 2026-05-03
**Tipo:** Design Document / Spec
**Estado:** Aprobado — listo para writing-plans

---

## 1. Visión

PyCode Platform evoluciona de "plataforma para aprender Python" a **plataforma de estudio integral para AI Engineer profesional**: una sola ruta, en español, gratis y open source, que toma a alguien con conocimientos básicos de programación y lo lleva a un nivel donde puede construir, evaluar y deployar sistemas de IA modernos (LLMs, RAG, agentes, ML clásico en producción, MLOps).

La identidad pedagógica se mantiene: **"Aprender haciendo, guiado por el tutor socrático"**. El estudiante no consume videos ni lee teoría pasiva; cada concepto se aprende ejecutando código, fallando, y siendo guiado por preguntas hasta que descubre la respuesta.

### Decisiones de alcance (brainstorming 2026-05-03)

| Decisión | Elección |
|---|---|
| Alcance final del aprendizaje | **AI Engineer profesional** (no researcher; sí practitioner avanzado) |
| Formato de ejecución | **Híbrido**: Monaco lineal para Python+puzzles ELO; notebook propio para DS/ML/DL; puzzles ELO especializados pandas/numpy/PyTorch |
| Cómputo para Deep Learning | **Híbrido**: CPU (Pyodide cliente) para Tracks 1-3; Colab para Track 4 con botón "Abrir en Colab"; tier Pro futuro con Modal/RunPod |
| Estructura del currículo | **6 tracks secuenciales** con prerequisitos, cada uno con dashboard, certificado y boss puzzle |
| Fuente de contenido | **Híbrido**: contenido propio del usuario (Modulo1-8.ipynb, libros, datasets en carpeta REVISAR) como base + asistencia IA + curaduría humana |
| Idioma | **Bilingüe**: narración/UI en español, código y términos técnicos en inglés sin traducir (DataFrame, epoch, loss, embedding, fine-tuning, etc.) |
| Monetización | **Open source y gratis** todo el contenido + tier Pro futuro opcional para extras (GPU, certificado verificado, mentoría humana) |
| Despliegue | **100% free tier**: Supabase + Vercel + Render + Groq + Pyodide + Colab |
| Licencia | MIT para código, **CC-BY-SA 4.0 para contenido educativo** |

---

## 2. Arquitectura macro: lo que ya hay vs lo que falta

| Capa | Ya existe | Por construir |
|---|---|---|
| Auth + Users | JWT, registro, dashboard con XP/streaks | OAuth (Google/GitHub) opcional para tier Pro futuro |
| Editor Monaco lineal | Funciona para Python | Modo híbrido: lineal o notebook según contexto |
| Notebook propio | — | Kernel Pyodide en Web Worker + WebSocket outputs + renderizado MIME (HTML, imágenes, dataframes) |
| Sistema lecciones | 25 lecciones Python + 64 ejercicios | 5 tracks adicionales (~100 lecciones más, ~280 ejercicios más) |
| Puzzles ELO | Finxter-style para Python (parcialmente integrado) | Puzzles especializados NumPy/Pandas/PyTorch + integración completa frontend |
| Tutor IA socrático | Funciona, prompt en archivo `.txt` | Memoria de debilidades + contexto por track + provider abstraction (Groq + OpenAI) |
| Ejecución de código | Subprocess fallback (NO Docker real) | **Pyodide en cliente** (elimina deuda Docker sandbox) |
| Cómputo DL | — | Integración con Colab para notebooks pesados; tier Pro futuro con Modal/RunPod |
| Datasets | — | Registro versionado + API `/api/v1/datasets/{slug}` |
| Evaluador de notebooks | — | Sistema que ejecuta validators ocultos contra outputs del estudiante |
| Capstones | — | 6 proyectos finales evaluados por tutor IA con rúbrica configurable |
| Certificados | — | PDF firmado al completar cada track (reportlab) |

---

## 3. Despliegue e infraestructura (100% free tier)

### Stack consolidado

| Capa | Servicio | Free tier | Para qué |
|---|---|---|---|
| Frontend | **Vercel** o Cloudflare Pages | Ilimitado para hobby | React+Vite build |
| Backend FastAPI | **Render** (free web service) | 512 MB RAM, 750h/mes, soporta WebSockets | API + WS del editor/tutor |
| Base de datos | **Supabase** | 500 MB Postgres, 1 GB storage, 50k MAU, pg_vector incluido, Auth incluido | Lecciones, progreso, ELO, embeddings RAG |
| LLM (tutor IA) | **Groq** (Llama 3.3 70B) | 14,400 req/día, ultrarrápido | Reemplaza OpenAI gratis para tutor socrático |
| Sandbox código Python | **Pyodide en cliente** | Sin costo, infinito | Python+NumPy+Pandas+sklearn+matplotlib en el navegador |
| Cómputo DL pesado | **Google Colab** + Kaggle | T4 GPU gratis | Track 4 — botón "Abrir en Colab" |
| Datasets >500 MB | **Hugging Face Datasets** | Sin límite práctico | CSVs grandes (cases_deaths, creditcard_2023) en Parquet |
| Vector DB (RAG) | **Supabase pg_vector** | En el mismo Postgres | Track 5 capstone Nebula RAG |
| Storage de datasets pequeños | **Supabase Storage** | 1 GB | CSVs <100 MB usados en lecciones |
| Keep-alive backend | UptimeRobot (cron 14 min) | Gratis | Evitar que Render duerma |

### Variables de entorno consolidadas

```env
DATABASE_URL=postgresql+asyncpg://...supabase.../postgres
SUPABASE_URL=https://<proyecto>.supabase.co
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_KEY=...           # solo backend
GROQ_API_KEY=gsk_...
LLM_PROVIDER=groq                  # configurable: groq|openai|anthropic
LLM_MODEL=llama-3.3-70b-versatile
HF_TOKEN=hf_...                    # para descargar datasets HF
SECRET_KEY=...
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Tradeoffs aceptados

- **Render duerme tras 15 min idle** → cron UptimeRobot pinguea `/health` cada 14 min. Migrar a Fly.io/Railway si crece.
- **Supabase 500 MB BD** → tablas con TTL/limpieza (`code_submissions`, `tutor_messages` >30 días eliminadas para usuarios free); datasets fuera de BD.
- **Pyodide no soporta PyTorch** → Track 4 va a Colab. División natural Tracks 1-3 (Pyodide) vs Track 4 (Colab) vs Tracks 5-6 (mix con APIs LLM).
- **Groq rate limit 14,400 req/día** se reparte entre usuarios → caching de respuestas comunes + fallback a HF Inference/Cohere si necesario.
- **Migración SQLite → Postgres ahora indispensable** → Alembic ya no es opcional, debe ir en Fase 0.

---

## 4. Estructura del currículo: los 6 tracks

Cada track: **lecciones (Markdown + Monaco/notebook) + ejercicios cortos + puzzles ELO + 1 capstone + certificado PDF**.

### Track 1 — Python Mastery *(YA EXISTE, requiere pulido)*

- **Estado:** 25 lecciones, 64 ejercicios. Pendientes: puzzles ELO específicos del track + capstone + certificado.
- **Bloques:** fundamentos → estructuras de datos → POO → I/O y archivos → módulos → decoradores → tipado → async → stdlib → testing → patrones de diseño.
- **Puzzles ELO:** 80-100 (los 22 actuales + ampliación estilo Coffee Break Python).
- **Capstone:** CLI completa con argparse + tests + empaquetado pip + tipado estricto. Inspiración: `FileIndexer_Pro`.
- **Libros referenciados:** carpetas `python/`, `Master Python from Basics to Advanced`, `PythonBooks`, `Python Programming for Mathematics`, `PILDORAS_DE_PROGRAMACION`.
- **Trabajo nuevo:** ~1-2 semanas.

### Track 2 — Data Science Foundations

- **Bloques (~20 lecciones):** NumPy esencial → Pandas core → Limpieza de datos (los 7 notebooks de `Proyecto_limpiaza_datos`) → Visualización (matplotlib/seaborn/plotly) → Estadística aplicada (Spiegelhalter como referencia) → EDA estructurado.
- **Ejercicios:** ~50, cada uno carga un dataset real.
- **Puzzles ELO especializados:** ~80 estilo Coffee Break Pandas / Coffee Break NumPy.
- **Capstone:** análisis EDA completo con dashboard final. Ideas: análisis CO2 por país, Olympic medalists, retail sales.
- **Datasets aprovechados:** penguins, retail_sales_dataset, olympic_medalists, cars, books, vehicles_us, music_project, megaline_*, customers, orders, Dataset-Colombia.
- **Base directa:** Modulo1-8.ipynb de Automatiza-con-Max → adaptados al sistema notebook.
- **Libros referenciados:** carpeta `Statistics`, *El arte de la estadística* (Spiegelhalter).
- **Trabajo nuevo:** ~3-4 semanas.

### Track 3 — Machine Learning Clásico

- **Bloques (~18 lecciones):** Pipeline ML → Regresión lineal/logística → Árboles, RF, Gradient Boosting (XGBoost/LightGBM) → Clustering → Reducción dimensionalidad → Feature engineering → Métricas → Validación robusta → Modelos interpretables (SHAP).
- **Ejercicios:** ~50.
- **Puzzles ELO:** ~60 sobre sklearn API y elección de modelo.
- **Capstone:** clasificador de churn/credit scoring con feature engineering, validación rigurosa, reporte profesional. Datasets: Telco_customer_churn, creditcard_2023, credit_scoring_eng, cancer.csv, diabetes.csv.
- **Base directa:** `bird-radar-rfc.ipynb` (random forest classifier) + `Modelo.ipynb` de Automatiza-con-Max.
- **Libros referenciados:** *AI and Machine Learning for Coders* (O'Reilly 2020), *Data Science y Machine Learning con Fundamento Matemático* (en español), carpeta `LIBROS/lIBROS RECOMEDADOS/ML`.
- **Trabajo nuevo:** ~4-5 semanas. Pyodide soporta sklearn casi completo.

### Track 4 — Deep Learning con PyTorch

- **Bloques (~18 lecciones):** Tensores PyTorch → MLP desde cero (forward/backward manual) → Training loop → CNNs → RNNs/LSTMs/GRUs → Embeddings y atención → Transformers from scratch (mini-GPT) → CV con torchvision → NLP con HuggingFace transformers → Evaluación DL.
- **Ejercicios:** ~45 (todos con botón "Abrir en Colab").
- **Puzzles ELO:** ~50 (predicción de shapes, debugging training loops, lectura de stack traces).
- **Capstone:** clasificador de imágenes con transfer learning, deployado como API.
- **Datasets:** MNIST, CIFAR-10, FashionMNIST (vía torchvision), cancer.csv para MLP binario.
- **Libros referenciados:** *AI and ML for Coders in PyTorch* (O'Reilly 2025), *Dive into Deep Learning* (CC-BY-SA).
- **Trabajo nuevo:** ~5-6 semanas.

### Track 5 — AI Engineering & LLMs

- **Bloques (~16 lecciones):** APIs LLMs (OpenAI/Anthropic/Groq/HF) → Prompt engineering → Structured output (JSON mode, function calling, Pydantic+LLM) → RAG fundamentos (embeddings, vector DBs, chunking) → RAG avanzado (re-ranking, hybrid search, evaluación) → Agentes con tool use (ReAct) → MCP → Fine-tuning LoRA/QLoRA → Evaluación LLMs (LLM-as-judge, MMLU, HumanEval) → Costos/caching/latencia.
- **Ejercicios:** ~40 (mix Pyodide + APIs reales con Groq gratis).
- **Puzzles ELO:** ~40 (debugging prompts, predicción outputs, eligiendo arquitectura).
- **Capstone directo:** **Proyecto Nebula Docs RAG** (ya documentado en PDF del usuario). Sistema RAG completo con Supabase pg_vector + Groq + frontend React.
- **Lección bonus:** "Construir un tutor socrático con Qwen-math fine-tuned" basada en `pipeline_qwen_math_socratico.docx` y `proceso_entrenamiento_socratic.pdf` — meta-aprendizaje (la plataforma enseña cómo construir su propio cerebro).
- **Trabajo nuevo:** ~5-6 semanas.

### Track 6 — MLOps & Producción

- **Bloques (~15 lecciones):** Docker para ML → FastAPI serving → MLflow → CI/CD para ML (GitHub Actions) → Monitoring y drift detection → Vector DBs en producción → Caching de inferencia (Redis, semantic cache) → Observabilidad LLM (Langfuse/Helicone) → A/B testing → Costos y escalabilidad.
- **Ejercicios:** ~30.
- **Puzzles ELO:** ~25 (configs Docker, debugging YAML CI, lectura métricas drift).
- **Capstone:** deployar el clasificador del Track 4 con API + monitoring + CI/CD a producción real (Hugging Face Spaces o Render).
- **Trabajo nuevo:** ~4-5 semanas.

### Totales

| Track | Lecciones | Ejercicios | Puzzles ELO | Capstone |
|---|---:|---:|---:|---|
| 1 — Python | 25 ✅ | 64 ✅ | ~80-100 (faltan) | CLI tool |
| 2 — DS Foundations | ~20 | ~50 | ~80 | EDA + Dashboard |
| 3 — ML Clásico | ~18 | ~50 | ~60 | Churn/Credit classifier |
| 4 — Deep Learning | ~18 | ~45 | ~50 | Image classifier |
| 5 — AI Engineering | ~16 | ~40 | ~40 | **Nebula RAG** |
| 6 — MLOps | ~15 | ~30 | ~25 | Production pipeline |
| **Total** | **~112** | **~280** | **~340** | **6 capstones** |

---

## 5. Sistemas técnicos nuevos a construir

### 5.1 Notebook propio integrado

Construido sobre Pyodide (no JupyterLite embebido) para mantener control sobre evaluación, persistencia, ELO e integración con tutor.

**Componentes frontend:**
```
frontend/src/components/Notebook/
├── NotebookView.tsx           # contenedor de celdas
├── Cell.tsx                   # célula individual (Monaco + output)
├── CellOutput.tsx             # renderizador MIME
├── KernelStatus.tsx           # indicador "ejecutando", "listo", "error"
└── NotebookToolbar.tsx        # add/run/restart kernel, save
```

**Backend:**
```
backend/app/api/v1/endpoints/notebooks.py  # CRUD de notebooks del usuario
backend/app/models/notebook.py             # Notebooks {user_id, lesson_id, cells_json, kernel_state}
```

**Decisiones clave:**
- **Pyodide en Web Worker** (no main thread): no congela UI con bucles infinitos; variables persisten entre celdas; "restart kernel" = matar Worker y crear nuevo.
- **Carga inicial Pyodide:** ~7 MB descarga, 2-3 segundos primera vez, cacheable indefinido en service worker.
- **Renderizado MIME:** `text/plain` → `<pre>`; `image/png` (matplotlib) → `<img>` base64; `text/html` (df.to_html()) → render seguro DOMPurify; `application/json` → JSON viewer; `text/markdown` → react-markdown.
- **DataFrame rico:** patch al hook de Pyodide para detectar `display(df)` y mostrar tabla con scroll, tipos de columna, nulls highlighted.
- **Persistencia:** Supabase tabla `notebooks` por `(user_id, lesson_id)`, celdas como JSON, auto-save con debounce 5s, botón "reiniciar al estado original".

**Estimación:** 3-4 semanas. MVP de 1-2 semanas (solo celdas código + texto + matplotlib) y luego iterar.

### 5.2 Evaluador de notebooks

Sistema de **tests ocultos contra el namespace del kernel** (no `print() == expected`).

**Modelo:**
```python
class NotebookExercise(Base):
    id = Column(Integer, primary_key=True)
    lesson_id = Column(ForeignKey("lessons.id"))
    title = Column(String)
    instructions = Column(Text)
    starter_notebook_json = Column(JSON)        # plantilla inicial
    hidden_validators = Column(JSON)            # ver formato
    points = Column(Integer)
```

**Formato de `hidden_validators`** (lista de checks ejecutados después del notebook):
```json
[
  {"type": "variable_exists", "name": "df_clean", "error": "Falta crear df_clean"},
  {"type": "variable_type", "name": "df_clean", "expected_type": "pandas.DataFrame"},
  {"type": "dataframe_shape", "name": "df_clean", "rows": 891, "cols": 8},
  {"type": "dataframe_no_nulls", "name": "df_clean", "columns": ["age", "fare"]},
  {"type": "function_returns", "function": "calcular_promedio",
   "input": [1, 2, 3, 4], "expected": 2.5, "tolerance": 0.001},
  {"type": "model_accuracy_min", "name": "model",
   "X_test_var": "X_test", "y_test_var": "y_test", "min_accuracy": 0.85},
  {"type": "plot_exists", "min_artists": 1, "title_contains": ["Distribución"]}
]
```

**Implementación:** los validators se ejecutan en el mismo Worker Pyodide del estudiante en cliente. Backend solo recibe resultados serializados. **Backend nunca ejecuta código del estudiante** — gratis y seguro. Estudiante ve mensajes útiles (`"df_clean tiene shape (900, 8), esperaba (891, 8)"`) sin ver los validators.

**Estimación:** 1-2 semanas.

### 5.3 Sistema de datasets

**Endpoints:**
```
GET  /api/v1/datasets                 # lista catálogo
GET  /api/v1/datasets/{slug}          # metadata
GET  /api/v1/datasets/{slug}/download # CSV/Parquet stream
```

**Modelo:**
```python
class Dataset(Base):
    slug = Column(String, primary_key=True)        # "titanic", "telco-churn"
    title = Column(String)
    description = Column(Text)
    license = Column(String)
    source = Column(String)                         # URL original
    columns = Column(JSON)                          # [{"name": ..., "type": ..., "nullable": ...}]
    size_bytes = Column(Integer)
    storage = Column(String)                        # "supabase" | "huggingface" | "url"
    storage_path = Column(String)
    tracks = Column(JSON)                           # ["track-2", "track-3"]
    sample_row = Column(JSON)
```

**Hosting según tamaño:**
- <10 MB → Supabase Storage (1 GB free)
- 10-100 MB → HuggingFace Datasets (gratis)
- >100 MB → HuggingFace Datasets en formato Parquet

**Helper en notebook** (cargado al iniciar kernel):
```python
import pycode
df = pycode.load_dataset("telco-churn")     # cachea en IndexedDB
df = pycode.load_dataset("retail-sales", year=2025)
pycode.list_datasets(track=2)
```

**Inventario inicial (de carpeta `REVISAR/`):**

| Slug | Origen | Track | Tamaño |
|---|---|---|---|
| `titanic` | clásico | 2,3 | <1 MB |
| `penguins` | DATA_SETS_PARA PROYECTOS | 2 | <1 MB |
| `retail-sales-2025` | retail_sales_dataset.csv | 2 | 51 KB |
| `olympic-medalists` | 3_data_sets | 2 | 2.3 MB |
| `cars` | 3_data_sets | 2,3 | 7.5 MB |
| `vehicles-us` | Automatiza | 3 | — |
| `telco-churn` | Telco_customer_churn.xlsx | 3 | <1 MB |
| `creditcard-2023` | 3_data_sets (zip) | 3 | 150 MB → HF |
| `cases-deaths-covid` | 3_data_sets | 2 | 150 MB → HF |
| `cancer` | 3_data_sets | 3,4 | 137 KB |
| `diabetes` | 3_data_sets | 3 | 24 KB |
| `books` | 3_data_sets | 2,5 (RAG) | 1 MB |
| `netflix-titles` | DATA_SETS_PARA PROYECTOS | 2 | — |
| `laliga-2526` | LaLiga_2526_actualizado.xlsx | 2 (opcional) | — |
| `colombia-data` | Dataset-Colombia/ | 2 (regional) | — |
| `appearances-football` | 3_data_sets (zip) | 2,3 | 9 MB |

**Estimación:** 1 semana (incluye script de bootstrap que indexa `REVISAR/DATASETS` y genera el catálogo).

### 5.4 Integración con Google Colab (Track 4)

- Cada lección de Track 4 tiene `colab_template_url` apuntando a `.ipynb` en repo público GitHub `pycode-platform/track4-notebooks`.
- Botón **"Abrir en Google Colab con GPU"** → `https://colab.research.google.com/github/pycode-platform/track4-notebooks/blob/main/{leccion}.ipynb`.
- Estudiante trabaja en Colab, descarga `.ipynb` resuelto, lo sube a la plataforma.
- Validador acepta `.ipynb` upload: parsea celdas, ejecuta `hidden_validators` contra outputs serializados.

**Estimación:** 3-4 días.

### 5.5 Tutor socrático evolucionado

**Cambios sobre el actual:**

1. **Provider abstraction:** `backend/app/services/llm_provider.py` con clase abstracta `LLMProvider` y dos implementaciones (`GroqProvider`, `OpenAIProvider`). Configurable vía `LLM_PROVIDER`.
2. **Memoria de debilidades** (PYCODE_SPEC Fase 4.1, pendiente). Tabla `user_weaknesses` con topic + fail_count + last_failed. Tutor recibe top-3 debilidades en system prompt.
3. **Contexto por track:** prompts en `backend/prompts/track1.md`, `track2.md`, etc. — concatenados al prompt base. Track 4 pregunta sobre shapes de tensores, no indexing de listas.
4. **Rate limit por usuario** (PYCODE_SPEC Fase 1.4, pendiente). Free: 50 mensajes/día. Pro futuro: ilimitado. Tracking en Redis o tabla `tutor_quota` con TTL diario.
5. **Pipeline futuro de fine-tuning:** `pipeline_qwen_math_socratico.docx` se convierte en lección DEL Track 5 + rama de investigación interna (modelo fine-tuneado reemplaza Llama 3.3 cuando esté listo).

**Estimación:** 1-2 semanas.

### 5.6 Capstone evaluator

- Estudiante sube ZIP o link a repo público GitHub.
- Backend extrae estructura (`README.md`, archivos clave).
- Tutor IA evalúa contra **rúbrica configurable** (JSON con criterios y pesos):

```json
{
  "criterios": [
    {"nombre": "Limpieza de datos correcta", "peso": 20, "tipo": "check_funcional"},
    {"nombre": "Visualizaciones claras", "peso": 15, "tipo": "rubrica_llm"},
    {"nombre": "Modelo accuracy > 80%", "peso": 25, "tipo": "ejecucion_test"},
    {"nombre": "Reporte ejecutivo claro", "peso": 20, "tipo": "rubrica_llm"},
    {"nombre": "Código limpio y comentado", "peso": 20, "tipo": "rubrica_llm"}
  ]
}
```

- Resultado: feedback detallado + nota + decisión "aprobado/iterar".
- Si aprueba: certificado PDF generado (PYCODE_SPEC Fase 5.3, pendiente, reportlab).

**Estimación:** 2 semanas.

### Resumen subsistemas nuevos

| Subsistema | Estimación | Crítico para |
|---|---|---|
| Notebook propio (Pyodide+Worker) | 3-4 sem | Tracks 2-5 |
| Evaluador de notebooks | 1-2 sem | Tracks 2-5 |
| Sistema de datasets | 1 sem | Tracks 2-5 |
| Integración Colab | 3-4 días | Track 4 |
| Tutor evolucionado | 1-2 sem | Todos |
| Capstone evaluator + certificados | 2 sem | Cierre tracks |
| **Total** | **~10-12 sem** | — |

---

## 6. Roadmap por fases

### FASE 0 — Fundamentos críticos (2-3 sem) **BLOQUEANTE**

| Tarea | Origen | Esfuerzo |
|---|---|---|
| Migrar a Supabase Postgres (asyncpg) | Nuevo | 3-4 días |
| Configurar Alembic + migración inicial | PYCODE_SPEC 1.1 | 2 días |
| Eliminar `bootstrap_elo_schema` shim | Limpieza | 1 día |
| Provider abstraction LLM (Groq + OpenAI) | Nuevo | 2-3 días |
| Rate limiting tutor | PYCODE_SPEC 1.4 | 1-2 días |
| Logging estructurado + Sentry | PYCODE_SPEC 6.1 | 1 día |
| Setup despliegue (Vercel + Render + UptimeRobot + Supabase) | Nuevo | 1-2 días |
| Reemplazar subprocess executor por Pyodide | Reemplaza PYCODE_SPEC 1.2 | 4-5 días |

**Salida:** plataforma actual sigue funcionando, ahora en producción gratis con Postgres + Pyodide + Groq. **Deuda Docker sandbox eliminada.**

### FASE 1 — Pulido Track 1 + sistema ELO completo (2-3 sem)

| Tarea | Origen | Esfuerzo |
|---|---|---|
| Integrar router ELO al main FastAPI | PYCODE_SPEC 1.3 | 1 día |
| ELODashboard en Dashboard frontend | PYCODE_SPEC 2.3 | 2 días |
| EloResultModal en Editor | PYCODE_SPEC 2.4 | 1-2 días |
| Tests ocultos para ejercicios Python (Pyodide-based) | PYCODE_SPEC 3.1 | 3-4 días |
| Historial de intentos por ejercicio | PYCODE_SPEC 3.2 | 2 días |
| Capstone Track 1 (CLI tool con argparse + tests) | Nuevo | 4-5 días |
| Generador certificado PDF (reportlab) | PYCODE_SPEC 5.3 | 2-3 días |
| Mapa de competencias del Track 1 | PYCODE_SPEC 5.1 | 2 días |
| Puzzle del día público | PYCODE_SPEC 5.2 | 2 días |
| Ampliar puzzles ELO de 22 a 80-100 | Nuevo | 1 sem |

**Salida:** Track 1 completo. Modelo "lecciones + ejercicios + puzzles + capstone + certificado" validado.

### FASE 2 — Sistema notebook + datasets + Track 2 (4-6 sem)

| Tarea | Esfuerzo |
|---|---|
| Notebook propio MVP (Pyodide Worker, código, texto, matplotlib) | 2 sem |
| Renderizado MIME completo (DataFrame ricos, HTML, plotly) | 4-5 días |
| Persistencia notebooks (Supabase tabla `notebooks`) | 2-3 días |
| Sistema datasets (catálogo + API + helper `pycode.load_dataset`) | 1 sem |
| Bootstrap script datasets desde `REVISAR/` | 2 días |
| Evaluador de notebooks (validators ocultos) | 1-2 sem |
| Track 2 contenido (20 lecciones + 50 ejercicios + 80 puzzles + capstone) | 3-4 sem |

**Salida:** Track 1 → Track 2 sin fricción. Plataforma cubre ~70% de un bootcamp DS básico. **Punto de inflexión — primera versión comercializable.**

### FASE 3 — Track 3 (ML Clásico) + tutor evolucionado (4-5 sem)

| Tarea | Esfuerzo |
|---|---|
| Tutor track-aware (prompts por track) | 3-4 días |
| Memoria de debilidades del usuario | 3-4 días |
| Track 3 contenido (18 lecciones + 50 ejercicios + 60 puzzles + capstone) | 3-4 sem |
| Validators específicos para modelos sklearn | 3-4 días |

### FASE 4 — Track 4 (Deep Learning) + Colab integration (5-6 sem)

| Tarea | Esfuerzo |
|---|---|
| Integración Colab (botón abrir + upload .ipynb) | 3-4 días |
| Validador de .ipynb subidos | 3-4 días |
| Track 4 contenido (18 lecciones + 45 ejercicios + 50 puzzles + capstone) | 5-6 sem |
| Repo público `pycode-platform/track4-notebooks` con plantillas | 2-3 días |

### FASE 5 — Track 5 (AI Engineering) + Nebula RAG capstone (5-6 sem)

| Tarea | Esfuerzo |
|---|---|
| Habilitar pg_vector en Supabase | 1 día |
| Helpers embeddings + retrieval | 3-4 días |
| Track 5 contenido (16 lecciones + 40 ejercicios + 40 puzzles) | 4-5 sem |
| Capstone Nebula RAG | 1 sem |
| Lección Qwen-math fine-tuned | 4-5 días |

**Salida:** **diferencial competitivo**. Pocos cursos en español enseñan RAG + agentes + fine-tuning con esta calidad.

### FASE 6 — Track 6 (MLOps) + cierre del producto (4-5 sem)

| Tarea | Esfuerzo |
|---|---|
| Track 6 contenido (15 lecciones + 30 ejercicios + 25 puzzles + capstone) | 4-5 sem |
| Infraestructura para deploy de capstones (botón "deploy a HF Spaces") | 3-4 días |
| Capstone evaluator multi-track integrado con tutor IA | 1-2 sem |
| Página `/learning-path` con progreso global por tracks | 2-3 días |

### FASE 7 (post-lanzamiento) — Tier Pro + comunidad

- Tier Pro opcional ($9-15/mes): GPU directa via Modal/RunPod, certificados verificados firmados, mentoría humana, contenido premium.
- OAuth Google/GitHub via Supabase Auth.
- Sistema de comunidad: foros por lección, soluciones compartidas, leaderboards.
- Mobile app o PWA optimizada.
- Fine-tuning real del tutor (pipeline Qwen-math) → reemplazar Llama 3.3 con modelo propio.
- A/B testing del contenido.
- Internacionalización a inglés.

### Cronograma macro

| Fase | Duración | Acumulado |
|---|---|---|
| 0 | 2-3 sem | 3 sem |
| 1 | 2-3 sem | 6 sem |
| 2 | 4-6 sem | 12 sem |
| 3 | 4-5 sem | 17 sem |
| 4 | 5-6 sem | 23 sem |
| 5 | 5-6 sem | 29 sem |
| 6 | 4-5 sem | 34 sem |

**~7-8 meses tiempo parcial (15-20 hrs/sem)** o **~5 meses tiempo completo**. Cada fase termina con versión publicable. Si paras en Fase 2, ya tienes plataforma valiosa.

### Estrategia de calidad sostenible

- Arrancar cada track con 60% del contenido (lecciones core), publicar, recibir feedback, completar incrementalmente.
- Sistema ELO permite agregar puzzles después del lanzamiento sin romper nada.
- Plantilla estricta `LessonTemplate`: introducción → ejemplo motivador → teoría → ejemplo guiado → ejercicios → puzzles ELO. Mantiene voz consistente.

---

## 7. Modelo Pro futuro (post-Fase 6)

**Filosofía:** contenido y código siempre gratis y open source. Pro solo agrega comodidades, no bloquea aprendizaje.

| Free | Pro (~$9-15/mes propuesto) |
|---|---|
| Todos los tracks completos | Todos los tracks completos |
| Tutor Groq (50 msg/día) | Tutor ilimitado + GPT-4/Claude opcional |
| Capstones con feedback automatizado | Capstones con review humana opcional |
| Certificado PDF descargable | Certificado verificado firmado + perfil público |
| Notebooks Pyodide (CPU) | GPU directa en plataforma (~30 min/día) |
| Track 4 con Colab manual | Colab Pro o GPU integrada |
| Datasets del catálogo | Subir datasets propios + workspace privado |
| — | Mock interviews con tutor especializado |
| — | Acceso anticipado a tracks nuevos |

**Cuándo activar:** solo con señales claras (>500 MAU, >10 solicitudes "pagaría por X"). Antes es prematuro.

**Stack:** Stripe Checkout + tabla `subscriptions` Supabase + decorador `@pro_required` + Modal/RunPod via API.

**Estimación si se activa:** 2-3 semanas.

---

## 8. Métricas de éxito

**Engagement (semanal):**
- DAU/MAU ratio (objetivo: >20%)
- Sesiones promedio/semana por usuario activo (objetivo: ≥3)
- Tiempo promedio por sesión (objetivo: ≥25 min)

**Aprendizaje:**
- Tasa de finalización por track (objetivo: ≥40% — vs ~10% típico MOOCs)
- Distribución de ELO de usuarios (Gaussiana sana, no bimodal)
- Re-intentos por puzzle (objetivo: 1-3 promedio)
- Tiempo promedio para completar cada lección (detectar bloqueantes)

**Tutor socrático:**
- Mensajes/usuario/sesión (objetivo: 3-8)
- Helpfulness rating (thumbs up/down)
- Tasa de resolución del puzzle después de hablar con tutor (objetivo: >70%)

**Producto:**
- Capstones entregados/mes
- Certificados emitidos/mes
- Crecimiento orgánico (referrals, GitHub stars)
- Costos de infraestructura (objetivo: $0)

**Eventos a loguear (estructurados):**
```
lesson.started, lesson.completed
exercise.attempted, exercise.passed, exercise.failed
puzzle.attempted, puzzle.solved, puzzle.skipped
tutor.message_sent, tutor.helpful_feedback
notebook.cell_executed, notebook.error
capstone.submitted, capstone.evaluated
track.completed, certificate.issued
```

Stack: structlog → Supabase tabla `events` o PostHog free tier.

---

## 9. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Pyodide no soporta una librería clave (scipy avanzada, etc.) | Media | Medio | Documentar al inicio del track qué librerías funcionan; fallback Colab para casos puntuales |
| Groq baja tier free o restringe | Baja-Media | Alto | Provider abstraction permite cambiar a HF Inference / Cohere / Together en horas |
| Supabase 500 MB se llena rápido | Alta | Medio | TTL automático mensajes/submissions >30 días para users free; soft-delete; archivar a Storage |
| Render duerme y arruina experiencia | Alta | Bajo | UptimeRobot ping + mensaje "cargando" en frontend |
| Costo Colab gratis se acaba para estudiante intensivo | Media | Bajo | Documentar Kaggle Notebooks (30h GPU/sem) como alternativa |
| Contenido obsoleto (versión nueva PyTorch) | Alta a 12m | Medio | Tests automatizados que ejecutan notebooks de cada lección semanalmente en CI |
| Tutor IA da respuestas técnicamente incorrectas | Media | Alto | Eval set de 50-100 conversaciones canónicas + LLM-as-judge automatizado |
| Plagio masivo en capstones | Alta | Medio | Capstones públicos en GitHub del estudiante; tutor IA detecta inconsistencia código vs nivel previo |
| **Burnout del autor en 7-8 meses solo** | **Alta** | **Crítico** | Cada fase termina en producto deployable; si para en Fase 3 ya hay valor; buscar contributors open source después de Fase 2 |
| Licencias libros usadas indebidamente | Media | Alto | Citar siempre fuente; reescribir conceptos no copiar; `_external_sources/` separado |
| Dependencia Modulo1-8.ipynb sin permiso | Media | Alto | Confirmar permiso del autor original (Max) o reescribir desde temario propio inspirado |

---

## 10. Resumen ejecutivo

**Qué se construye:** PyCode Platform v2 — ruta integral 6 tracks (Python → DS → ML → DL → AI Eng → MLOps) en español, gratis, open source, con tutor socrático y sistema ELO de progresión, deployada 100% en infra free (Supabase + Vercel + Render + Groq + Pyodide + Colab).

**Qué se reusa:**
- Codebase FastAPI + React actual (auth, dashboard, editor, ELO parcial)
- 25 lecciones + 64 ejercicios de Python (Track 1 casi listo)
- 8 módulos notebooks Automatiza-con-Max (base Tracks 2-3)
- ~16 datasets de carpeta REVISAR (catálogo inicial)
- Libros de carpeta REVISAR como referencia bibliográfica
- Proyecto Nebula RAG documentado (capstone Track 5)
- Pipeline Qwen-math socrático (lección + futura mejora del tutor)

**Qué se construye nuevo:**
- Notebook Pyodide-en-Worker integrado
- Sistema de datasets con catálogo + helper Python
- Evaluador automático de notebooks
- Integración Colab para Track 4
- Provider abstraction LLM (Groq default)
- Tutor track-aware con memoria de debilidades
- Capstone evaluator + certificados PDF
- 5 tracks completos de contenido

**Cuándo termina:** 7-8 meses tiempo parcial. **Cuándo es útil:** desde Fase 1 (semana 6).

**Próximo paso:** invocar `writing-plans` para producir plan de implementación detallado de Fase 0 (la primera bloqueante).
