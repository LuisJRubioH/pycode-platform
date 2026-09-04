# Auditoría de calidad del contenido de las lecciones

Inventario objetivo de las 40 lecciones activas. **Snapshot: 2026-09-03.**
Diagnóstico: **no se modificó ninguna lección**.

## Método y sus límites

Todas las métricas salen de la **base de datos de producción** (Supabase
`medutbqsurjnaaymmrin`), no de `lesson_seed.py`: interesa lo que el estudiante
ve, no lo que el seed pretende sembrar. Consultas de solo lectura.

Qué mide cada columna:

- **chars** — `length(lessons.content)`.
- **h2** — cabeceras `## ` (el nivel que estructura la lección).
- **cód.** — bloques de código: pares de ` ``` `.
- **Err. / Res.** — presencia de las secciones *Errores comunes* y *Resumen*.
  Son las dos únicas convenciones reales del contenido: entre las 40 lecciones
  hay **154 cabeceras `##` distintas**, y solo *Resumen* (30/40) y *Errores
  comunes* (26/40) se repiten lo bastante como para medir con ellas.
- **ej.** — ejercicios de la lección. **c/tests** — de esos, cuántos tienen
  `hidden_tests`, es decir, cuántos el alumno **puede** completar.

Lo que estas métricas **no** miden: si la explicación es buena. Un texto de
6.000 caracteres puede estar mal escrito. Sirven para localizar lo que es
demostrablemente insuficiente, no para certificar lo demás como bueno.

## Inventario, de peor a mejor

| # | id | Lección | Track | Categoría | chars | h2 | cód. | Err. | Res. | ej. | c/tests |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 6 | Listas, Tuplas y Diccionarios | 1 | estructuras-datos | **148** | 2 | 0 | — | — | 2 | 2 |
| 2 | 4 | Bucles for y while | 1 | control-flujo | **165** | 1 | 0 | — | — | 2 | 2 |
| 3 | 3 | Condicionales y Lógica | 1 | control-flujo | **175** | 1 | 1 | — | — | 2 | 2 |
| 4 | 10 | Testing con pytest | 1 | testing | **177** | 1 | 0 | — | — | 1 | **0** |
| 5 | 8 | POO en Python | 1 | oop | **194** | 1 | 0 | — | — | 2 | 2 |
| 6 | 2 | Variables y Tipos | 1 | fundamentos | **196** | 1 | 0 | — | — | 2 | 2 |
| 7 | 9 | Módulos, Paquetes y Entornos | 1 | tooling | **217** | 1 | 0 | — | — | 1 | **0** |
| 8 | 5 | Funciones y Parámetros | 1 | funciones | **217** | 1 | 0 | — | — | 2 | 2 |
| 9 | 7 | Comprensiones y Manejo de Errores | 1 | python-moderno | **243** | 1 | 0 | — | — | 2 | 2 |
| 10 | 1 | Python desde Cero | 1 | fundamentos | **352** | 2 | 0 | — | — | 2 | 2 |
| — | — | *— salto de 6,6× sin ninguna lección en medio —* | | | | | | | | | |
| 11 | 31 | ML 10 · Naive Bayes | 3 | ml-naive-bayes | 2323 | 6 | 3 | **—** | ✅ | 3 | 3 |
| 12 | 32 | ML 11 · Curva ROC, AUC y umbral | 3 | ml-roc | 2506 | 5 | 3 | **—** | ✅ | 3 | 3 |
| 13 | 30 | ML 9 · Support Vector Machines | 3 | ml-svm | 2598 | 4 | 3 | **—** | ✅ | 3 | 3 |
| 14 | 36 | DL 4 · Training loop | 4 | dl-fundamentos | 2820 | 5 | 5 | ✅ | ✅ | 3 | 3 |
| 15 | 37 | DL 5 · Tu primer MLP | 4 | dl-fundamentos | 2859 | 5 | 4 | ✅ | ✅ | 3 | 3 |
| 16 | 33 | DL 1 · La neurona | 4 | dl-fundamentos | 3027 | 5 | 5 | ✅ | ✅ | 3 | 3 |
| 17 | 11 | NumPy esencial | 2 | numpy | 3034 | 6 | 4 | ✅ | ✅ | 3 | 3 |
| 18 | 13 | Pandas: groupby y pivot | 2 | pandas | 3059 | 7 | 6 | ✅ | ✅ | 3 | 3 |
| 19 | 12 | Pandas esencial | 2 | pandas | 3311 | 7 | 6 | ✅ | ✅ | 3 | 3 |
| 20 | 16 | Visualización 1: matplotlib | 2 | visualizacion | 3356 | 7 | 8 | ✅ | ✅ | 3 | 3 |
| 21 | 35 | DL 3 · Backpropagation | 4 | dl-fundamentos | 3422 | 6 | 6 | ✅ | ✅ | 3 | 3 |
| 22 | 14 | Pandas: merge, join y fechas | 2 | pandas | 3520 | 8 | 6 | ✅ | ✅ | 3 | 3 |
| 23 | 17 | Visualización 2: subplots | 2 | visualizacion | 3529 | 8 | 6 | ✅ | ✅ | 3 | 3 |
| 24 | 18 | EDA: exploración sistemática | 2 | eda | 3553 | 7 | 7 | ✅ | ✅ | 3 | 3 |
| 25 | 20 | Estadística descriptiva | 2 | estadistica | 3583 | 7 | 7 | ✅ | ✅ | 3 | 3 |
| 26 | 15 | Pandas: limpieza y missing values | 2 | pandas | 3603 | 8 | 6 | ✅ | ✅ | 3 | 3 |
| 27 | 19 | EDA 2: feature engineering | 2 | eda | 3646 | 8 | 8 | ✅ | ✅ | 3 | 3 |
| 28 | 34 | DL 2 · Funciones de pérdida | 4 | dl-fundamentos | 3714 | 5 | 6 | ✅ | ✅ | 3 | 3 |
| 29 | 39 | AI 2 · Chunking e indexación | 5 | ai-fundamentos | 3763 | 7 | 6 | ✅ | ✅ | 3 | 3 |
| 30 | 21 | Correlación, probabilidad, bootstrap | 2 | estadistica | 3793 | 6 | 4 | ✅ | ✅ | 3 | 3 |
| 31 | 38 | AI 1 · Embeddings y búsqueda semántica | 5 | ai-fundamentos | 3879 | 7 | 5 | ✅ | ✅ | 3 | 3 |
| 32 | 40 | AI 3 · Llamar a un LLM y prompt RAG | 5 | ai-fundamentos | 3957 | 6 | 8 | ✅ | ✅ | 3 | 3 |
| 33 | 28 | ML 7 · KMeans y método del codo | 3 | ml-clustering | 5171 | 4 | 6 | ✅ | ✅ | 3 | 3 |
| 34 | 29 | ML 8 · PCA | 3 | ml-dim-reduction | 5541 | 5 | 7 | ✅ | ✅ | 3 | 3 |
| 35 | 24 | ML 3 · Features escaladas y Pipelines | 3 | ml-features | 5619 | 4 | 6 | ✅ | ✅ | 3 | 3 |
| 36 | 23 | ML 2 · Métricas más allá de accuracy | 3 | ml-evaluacion | 5643 | 5 | 3 | ✅ | ✅ | 3 | 3 |
| 37 | 22 | ML 1 · Tu primer clasificador | 3 | ml-fundamentos | 5764 | 6 | 3 | ✅ | ✅ | 3 | 3 |
| 38 | 27 | ML 6 · Cross-validation y GridSearchCV | 3 | ml-tuning | 5892 | 4 | 6 | ✅ | ✅ | 3 | 3 |
| 39 | 26 | ML 5 · Árboles y Random Forest | 3 | ml-arboles | 6099 | 4 | 4 | ✅ | ✅ | 3 | 3 |
| 40 | 25 | ML 4 · Regresión: LinearRegression | 3 | ml-regresion | 6159 | 5 | 5 | ✅ | ✅ | 3 | 3 |

## El umbral de "lección pobre" no hay que elegirlo: lo marca la distribución

Ordenadas por longitud, las lecciones no forman un gradiente. Forman **dos
poblaciones separadas por una banda vacía**:

```
148 165 175 177 194 196 217 217 243 352 │·········· 1.970 chars sin nada ··········│ 2323 2506 2598 2820 ...
        ← 10 lecciones →                                                              ← 30 lecciones →
```

- La peor del grupo alto (2.323) es **6,6× más larga** que la mejor del grupo
  bajo (352).
- **No existe ninguna lección entre 353 y 2.322 caracteres.** Cualquier corte
  dentro de esa banda produce exactamente la misma clasificación, así que el
  umbral no es una opinión.

**Definición propuesta — lección pobre: `content < 1.000 caracteres` y `≤ 1
bloque de código`.** Corta por el centro de la banda vacía. Clasifica 10
lecciones, y las mismas 10 cumplen además los otros tres síntomas (sin *Errores
comunes*, sin *Resumen*, ≤ 2 ejercicios), lo que confirma que el corte separa
poblaciones reales y no solo textos cortos.

Un segundo escalón, mucho más leve: **ML 9, 10 y 11** (ids 30-32) son las tres
más cortas del grupo alto y las **tres únicas de los tracks 2-5 sin sección
*Errores comunes***. Son las últimas que se escribieron del Track 3: un bajón de
final de tanda, no un problema de categoría.

### La métrica que más separa no es la longitud, son los ejemplos

| | Track 1 (10 lecciones) | Tracks 2-5 (30 lecciones) |
|---|---|---|
| Caracteres, media | **208** | 3.958 |
| **Bloques de código, total** | **1** | **162** |
| Con *Errores comunes* | 0 / 10 | 27 / 30 |
| Con *Resumen* | 0 / 10 | 30 / 30 |
| Ejercicios, media | 1,8 | 3,0 |

Las 10 lecciones de Track 1 son el **25% del temario** y aportan el **1,7% del
contenido** y **1 de los 163 bloques de código** (ese único bloque está en
"Condicionales y Lógica"). Tu diagnóstico de "6 viñetas y ningún ejemplo" no es
el caso peor: es el caso **típico** del track.

Así se ve una lección entera de Track 1, íntegra, sin recortar:

```markdown
## for
- Recorre elementos o rangos.
- `range(inicio, fin, paso)`

## while
- Repite mientras se cumpla una condicion.
- Evita bucles infinitos actualizando estado.
```

## 1 · ¿Se concentra en algún track? Sí, y es absoluto

**Tu sospecha se confirma sin matices.** Las 10 lecciones pobres son las 10
lecciones de Track 1 — ids 1 a 10, es decir, las primeras que se escribieron.
Ninguna lección de Tracks 2, 3, 4 o 5 se acerca al umbral.

No es un problema de tema ni de dificultad: es un problema de **cuándo se
escribió**. A partir de la lección 11 (NumPy, el piloto de Track 2) aparece un
formato estable —teoría, ejemplos ejecutables, *Errores comunes*, *Resumen*, 3
ejercicios con `hidden_tests`— y se mantiene en las 30 siguientes. Track 1 es
anterior a ese formato y nunca se reescribió para alcanzarlo.

### Consecuencia funcional: Track 1 no se puede completar

Las lecciones **9 (Módulos, Paquetes y Entornos)** y **10 (Testing con pytest)**
tienen **1 ejercicio cada una y 0 con `hidden_tests`**. Sin tests ocultos el
cliente nunca puede reportar `success`, así que esos ejercicios **no se pueden
aprobar por ningún medio** y esas dos lecciones se quedan permanentemente en 0%.

Como la regla de completitud es "todos los ejercicios de la lección" y el track
agrega por lecciones, **ningún estudiante puede llegar al 100% de Track 1**. Ya
estaba anotado como deuda en el docstring de `progress_service`; aquí queda
cuantificado.

## 2 · Ejercicios que dependen de lo que su lección no explica

Metodología: para cada ejercicio se compara lo que el alumno **ve y debe
escribir** (`description` + `instructions` + `starter_code`) contra el `content`
de su lección. Se excluyen los `hidden_tests`: los escribe el autor y están
llenos de `assert`/`isinstance`, lo que falseaba la señal — una primera pasada
que los incluía daba 150 falsos positivos.

Segundo filtro, el que de verdad importa: un concepto ausente de *esta* lección
**no es un hueco** si alguna lección **anterior** lo enseña. Solo cuenta lo que
no se explica en ninguna parte antes.

### Huecos reales (el concepto no aparece en ninguna lección previa)

| Lección | Concepto | Qué se le pide al alumno |
|---|---|---|
| **8 · POO en Python** | `class`, `self` | "Clase Producto" y "Cuenta bancaria" le piden **escribir una clase entera**. La palabra `class` y el parámetro `self` **no aparecen en ninguna lección de la plataforma**. El contenido dice *"Clase define estructura/comportamiento"* en prosa y menciona `__init__` en una viñeta, sin una sola línea de código. |
| **12 · Pandas esencial** | `groupby` | El ejercicio "Promedio por curso (groupby)" exige `groupby`, que se enseña en la lección **13**, la siguiente. Dependencia hacia adelante. |
| **39 · AI 2 · Chunking** | `raise` | "Partir texto en chunks" pide *"Lanza `ValueError`"*. `raise` no se enseña en ninguna lección: la que le correspondería, "Comprensiones y Manejo de Errores" (id 7), tiene 243 caracteres y ningún ejemplo. |
| **4 · Bucles for y while** | `break`, `continue` | Caso distinto y peor en un sentido: **la propia `description` de la lección los promete** y el `content` no los menciona. La lección anuncia algo que no entrega. |

### Falso positivo, verificado y descartado

**DL 4 · Training loop — "decorador"**: mi heurística marcó `@`, pero al leer el
ejercicio es el operador de **multiplicación matricial** de NumPy
(`p = sigmoid(X @ W + b)`, `W -= lr*(X.T @ dz)`), no un decorador. Descartado.
Lo dejo escrito porque cualquiera que repita la consulta se va a encontrar el
mismo positivo.

### Referencias cruzadas que "resuelven", con una advertencia

Otros 16 casos (`diccionario`, `sorted`, `astype`, `Pipeline`, `groupby` en
Visualización 1) sí tienen una lección anterior que cubre el concepto, así que
**no** son huecos. Pero conviene mirar a qué resuelven: la mayoría de los
`diccionario` resuelven a la lección 6, **"Listas, Tuplas y Diccionarios", de
148 caracteres**, cuyo tratamiento íntegro de los diccionarios es:

```markdown
## Diccionarios
- Clave-valor para busqueda rapida.
```

Formalmente el concepto "está explicado antes". En la práctica el alumno llega a
ML 2 con eso. **Mientras Track 1 siga como está, las referencias cruzadas hacia
él no valen como cobertura.**

## 3 · Ejercicios por lección

**Las 40 lecciones tienen menos de 6 ejercicios. Ninguna excepción.** El máximo
de la plataforma es 3.

| Ejercicios | Lecciones | Cuáles |
|---|---|---|
| 1 | 2 | ids 9, 10 (y ninguno de los dos se puede aprobar: sin `hidden_tests`) |
| 2 | 8 | el resto de Track 1 |
| 3 | 30 | todas las de Tracks 2-5 |

Total: **108 ejercicios** en 40 lecciones — 2,7 de media. Para el objetivo de 6
por lección harían falta **132 ejercicios nuevos**, de los cuales **42 solo para
Track 1** (que además necesita primero el contenido que los sostenga).

El 3 fijo de los Tracks 2-5 no es casualidad: es la plantilla del piloto de
Track 2, replicada 30 veces. Subir el listón a 6 no es "rellenar", es cambiar la
plantilla.

## Qué sale de aquí

Ordenado por daño al estudiante, no por esfuerzo:

1. **Track 1 completo (10 lecciones)**: reescritura, no ampliación. Es el 25%
   del temario, el primer contacto de alguien que entra sin saber programar, y
   la base de la que dependen los tracks siguientes vía referencias cruzadas.
2. **Los 2 ejercicios sin `hidden_tests`** (ids 9, 10): mientras sigan así,
   Track 1 es imposible de completar. Es el arreglo más barato de la lista.
3. **Los 4 huecos de concepto**, empezando por POO: un ejercicio que pide
   escribir una clase sin que la plataforma haya mostrado nunca `class`.
4. **Densidad de ejercicios**: 132 nuevos para llegar a 6 por lección. El
   volumen mayor, pero el de menor urgencia — y sin resolver los puntos 1 y 3
   antes, serían más ejercicios apoyados en el mismo vacío.
5. **ML 9, 10 y 11**: añadir *Errores comunes*. Retoque menor.

Ninguna lección fue modificada en esta auditoría.
