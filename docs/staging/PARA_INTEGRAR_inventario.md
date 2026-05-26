# Inventario PARA_INTEGRAR — material externo pendiente de integrar

**Carpeta fuente:** `PARA_INTEGRAR/` (no versionada en git, vive solo en el clon local del autor).

**Norte:** la plataforma esta orientada a Python → Data Science → AI Engineering. Cualquier material que no aporte a esa ruta se descarta. Los labs externos (Coursera, MoureDev) se **recrean** con redaccion propia, tests ocultos Pyodide y ELO calibrado; nunca se copian textualmente por licencia y por calidad pedagogica.

## Mapeo material → Track

| Archivo / carpeta | Contenido | Track destino | Plan |
|---|---|---|---|
| `Ejercicios_entrevistas.md` | ~10 ejercicios Python basicos (max, palindromo, vocal, sum/multip, anagrama, generar_n_caracteres) | Track 1 | Recrear como `CuratedPuzzle` en `generated_bank.py` (Pieza B futura). |
| `GUIA_PARA_MEJORAR_LOGICA.md` | Ruta MoureDev: 26+ temas (sintaxis, recursividad, pilas/colas, OOP, excepciones, ficheros, JSON, tests, async, regex, fechas). Cada tema tiene "DIFICULTAD EXTRA" con mini-proyecto. | Track 1 (lecciones + capstones) | Los "DIFICULTAD EXTRA" alimentan capstones tematicos. El #11 (gestion de ventas .txt) es la base del Capstone Track 1 de Pieza D. |
| `MISCELANEA_DE_RETOS.md` | ~50+ retos clasicos (FizzBuzz, Fibonacci, primo, Armstrong, balanceo de expresiones, morse, tres en raya, contar palabras, calculadora .txt) | Track 1 | Distribuir: algoritmicos cortos → puzzles ELO; los extensos → sistema `Challenge`. |
| `aplicaciones_pensadas_para_anadir_a_portafolio.md` | 12 apps mobile/web genericas (Conecta 4, Twitter clone, Pomodoro, Pizza, Firebase Chat, RSS, Memoria de cartas) | **Descartar (mayoria)** | No alinea con DS/IA. Rescatar solo: Star Wars API (#2) como ejercicio ETL de Track 2; Pomodoro (#4) como CSV time-tracking. El resto fuera de scope. |
| `COURSERA/Python for Data Science, AI & Development/` | Notebooks IBM (Types, Expressions, String, Loops, Functions, OOP, Numpy 1D/2D, Pandas Loading/Selecting, Text Analysis, Stock Analysis con yfinance, Web Scraping). + 4 PDFs de retos (Triangulo, IMC, Cambio, Hora vuelo). | Track 1 (refuerzo) + **Track 2** (base) | Recrear como lecciones de Track 2 cuando arranque Fase 2. No integrar notebooks tal cual (licencia IBM). |
| `COURSERA/Supervised Machine Learning Regression and Classification/` | Labs Andrew Ng W1-W3: Model Representation, Cost Function, Gradient Descent, Numpy Vectorization, Multiple Variable, Feature Scaling, Polynomial Reg, Sklearn GD/Normal, Logistic Regression. | **Track 3** | Base de Fase 3 (ML Clasico). Recrear con dataset propio, sin reutilizar `lab_utils*.py` ni `deeplearning.mplstyle`. |
| `Mathematics for Machine Learning-...zip` | Algebra lineal + calculo multivariable (Imperial College via Coursera). | Track 2 / Track 3 | Refuerzo matematico embebido. Recrear ejercicios con `sympy` + `numpy` en Pyodide. |
| `Al_lin_Lab_Files.zip` | Labs de algebra lineal. | Track 2 / Track 3 | Idem. |
| `multivariable_Files.zip` | Calculo multivariable. | Track 3 / Track 4 | Refuerzo matematico para backprop (Track 4). |
| `Platzi Python-...zip` | Curso Python basico. | Track 1 (refuerzo) | Inspeccionar y rescatar ejercicios que llenen huecos del Track 1 actual. |
| `COURSERA/.../*.png` y `Nueva carpeta/*.jpg` | Screenshots y fotos. | N/A | Solo referencia visual del autor; no integrar. |

## Politica de licencia

- **No copiar enunciados textuales** de Coursera, MoureDev ni Platzi al repo. Esos materiales son inspiracion: el enunciado en la plataforma se redacta de cero en castellano propio.
- **No incluir** los notebooks `.ipynb` originales en el repo. Si hace falta scaffolding, se crea desde cero.
- **No reutilizar** `lab_utils_*.py`, `public_tests.py`, `test_utils.py` ni `deeplearning.mplstyle` de Andrew Ng. Los helpers se reescriben.
- Datasets de los labs: si son publicos (UCI, Kaggle abierto), referenciar el dataset original con URL. Si son propios de Coursera, generar dataset sintetico equivalente.

## Roadmap de integracion

| Pieza | Material que consume | Cuando | Estado |
|---|---|---|---|
| A — Inventario (este doc) | Todo PARA_INTEGRAR | Ahora | En curso |
| D — Capstone Track 1 (gestion de ventas CLI) | MoureDev #11 "DIFICULTAD EXTRA" | Fase 1 (siguiente) | Pendiente |
| B — Banco curado 80 → 100 puzzles | MISCELANEA + Ejercicios_entrevistas | Fase 1 (opcional, post-D) | Pendiente |
| C — 10 retos algoritmicos nuevos | MISCELANEA | Fase 1 (opcional, post-D) | Pendiente |
| E — Ejercicios extra en lecciones existentes | GUIA_PARA_MEJORAR_LOGICA "DIFICULTAD EXTRA" | Fase 1 (opcional) | Pendiente |
| F — Lecciones Track 2 (Pandas/NumPy) | Coursera IBM PDS + Mathematics for ML | Fase 2 | Catalogado, no iniciado |
| G — Lecciones Track 3 (ML Clasico) | Andrew Ng W1-W3 + multivariable | Fase 3 | Catalogado, no iniciado |

## Decision sobre `aplicaciones_pensadas_para_anadir_a_portafolio.md`

12 ideas de apps mobile/web. Solo 2 sobreviven al filtro DS/IA:

| Idea original | Recreacion en plataforma |
|---|---|
| #2 Enciclopedia Star Wars (API SWAPI) | **Track 2** — capstone ETL: descargar SWAPI, normalizar a DataFrame, persistir CSV, analizar (planeta con mas personajes, etc.). |
| #4 Pomodoro con historial | **Track 1** — ejercicio CLI con argparse + persistencia JSON + reporte agregado por dia (Counter, groupby manual). |

El resto (Conecta 4, Twitter clone, Memoria de cartas, Pizza, Firebase Chat, RSS, Stripe, Quiz, Conversor unidades, DevStore) se descartan: son frontend puro o backend genericos que no aportan al curriculum DS/IA.

## Notas operativas

- La carpeta `PARA_INTEGRAR/` esta en `.gitignore` de facto (no committeada). El material vive solo en el clon local del autor.
- Cuando se integre material en una Pieza, marcarlo aqui en la tabla de roadmap como **Integrado** con commit hash.
- Si surge material nuevo, anadirlo al inventario antes de integrarlo (este doc es el indice canonico).
