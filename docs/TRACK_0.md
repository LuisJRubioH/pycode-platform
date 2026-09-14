# Track 0 — Fundamentos de programación

Tramo de entrada de PyCode, previo a Track 1 (Python). El alumno aprende a **razonar
algoritmos antes de escribir código**: pseudocódigo, trazas de ejecución, estructuras de
datos elementales y diagramas de flujo.

> Estado: **piloto en marcha** (2026-09-14). Infraestructura hecha y lecciones 1-5
> construidas; quedan las lecciones 6-10 y el capstone. Este documento sigue siendo la
> fuente de verdad del track; el README enlaza aquí.

## Por qué existe

Un estudiante que no sabe seguir un bucle a mano no aprende Python: memoriza sintaxis. Track 0
separa las dos habilidades — primero el algoritmo, después el lenguaje — y las une en el
capstone, donde el alumno implementa en Python algoritmos que ya trazó a mano.

## Ubicación en la ruta

Track 0 → Track 1 (Python) → Track 2 (Data Science) → ... → Track 6 (MLOps).

**No es obligatorio.** Un alumno que ya programa en otro lenguaje no debe recorrer once
lecciones de pseudocódigo para llegar a Pandas. Un diagnóstico corto (5-6 ejercicios de traza
y bucles) recomienda punto de entrada; no bloquea ninguno de los dos caminos.

## Restricción de diseño: ejercicios no ejecutables

Todo el resto de la plataforma valida con `hidden_tests` ejecutados en Pyodide. **Track 0 no
puede hacer eso**: el pseudocódigo y los diagramas de flujo no se ejecutan.

Reglas que gobiernan la solución:

1. Los ejercicios de Track 0 se validan de forma **determinista**, sin Pyodide y sin LLM.
   **Corrige el backend**, en `POST /api/v1/exercises/{id}/check`. La primera versión de
   este documento decía "en el cliente", y es incompatible con la regla 3: para corregir
   en el navegador hay que mandarle la respuesta, y mandarla hasheada no salva nada cuando
   el valor de una celda es `3` (se saca por fuerza bruta en el propio navegador). El
   cliente manda lo que escribió el alumno y el backend contesta.
2. Al aprobar, emiten **el mismo evento de completitud** que un ejercicio de Python. XP,
   progreso de lección, ELO y competencias no se ramifican por tipo de ejercicio.
3. La solución correcta **no viaja al cliente**. Vive en `exercises.answer_key`, que no
   aparece en ningún endpoint; el guard rail está en
   `backend/tests/test_track0.py::test_answer_key_nunca_viaja_al_cliente`, que además
   comprueba que `spec` (el enunciado estructurado) **sí** llega, porque sin él no hay nada
   que pintar. El feedback dice **dónde** falla, nunca cuál era el valor.
4. Reintentos permitidos; XP idempotente (aprobar dos veces no suma dos veces).
5. Añadir un tipo nuevo no debe obligar a tocar la página de lección: un componente
   contenedor despacha por `exercise_type`.

## Tipos de ejercicio

| Tipo | Qué hace el alumno | Validación |
|---|---|---|
| `trace_table` | Completa la tabla de traza: valor de cada variable en cada iteración | Celda a celda; feedback de la primera celda incorrecta, sin revelar el resto |
| `order_steps` | Ordena los pasos desordenados de un algoritmo (drag & drop) | Secuencia exacta; admite varias secuencias válidas si el enunciado lo permite |
| `predict_output` | Responde qué imprime un pseudocódigo | Comparación normalizada (espacios y saltos de línea) |
| `find_bug` | Señala la línea errónea y elige el motivo | Número de línea + opción |
| `flowchart_match` | Empareja fragmentos de pseudocódigo con diagramas | Emparejamiento exacto |
| `flowchart_fill` | Completa los nodos vacíos de un diagrama desde un banco de opciones | Por nodo, no por texto libre |
| `mcq` | Opción múltiple conceptual | Opción exacta; los distractores corresponden a errores reales |

`trace_table` es el tipo central del track. Si solo se implementa uno, es ese.

**Hechos (2026-09-14)**: `trace_table`, `predict_output` y `mcq`, que son los que usan las
lecciones 1-5. Cada uno es un componente en `frontend/src/components/track0/` y un
`_validar_<tipo>` en `backend/app/services/track0_service.py`; añadir uno nuevo es
escribir ese par y registrarlo en `TIPOS` y en `VALIDADORES`, sin tocar el endpoint ni
la página de lección (regla 5, ya verificada).

## Diagramas de flujo

Se renderizan con **Mermaid** (`flowchart`), no como imágenes: texto versionable, editable,
accesible y con tema claro/oscuro. En toda lección con condicionales o bucles se muestra el
diagrama junto al pseudocódigo equivalente — la equivalencia entre ambos *es* el concepto que
se enseña.

Fuera de alcance: editor gráfico de diagramas.

## Temario

| # | Lección | Núcleo | Estado |
|---|---|---|---|
| 1 | Qué es un algoritmo | Entrada/proceso/salida, precisión, finitud, ambigüedad | ✅ |
| 2 | Variables, tipos y expresiones | Asignación, evaluación de expresiones, tipos en pseudocódigo | ✅ |
| 3 | Traza de ejecución | Seguir un algoritmo a mano — **habilidad central del track** | ✅ |
| 4 | Condicionales | Decisiones simples, anidadas, condiciones compuestas | ✅ |
| 5 | Bucles | Mientras / Para, contadores, acumuladores, condición de parada | ✅ |
| 6 | Diagramas de flujo | Símbolos y equivalencia con el pseudocódigo | |
| 7 | Descomposición | Subprogramas, parámetros, valor de retorno | |
| 8 | Arreglos y recorridos | Indexación, recorrido completo, búsqueda lineal | |
| 9 | Algoritmos clásicos | Máximo, conteo, intercambio, ordenamiento por selección y burbuja | |
| 10 | Cuánto cuesta un algoritmo | Contar operaciones, comparación intuitiva de eficiencia | |
| 11 | Capstone: del pseudocódigo al Python | Implementar en Python tres algoritmos ya trazados a mano | |

Mínimo **6 ejercicios por lección**, mezclando tipos. La lección 11 usa `hidden_tests`
normales: es el puente hacia Track 1.

## Convención de pseudocódigo

Una sola convención en todo el track, en español, documentada en una página de referencia
enlazada desde cada lección.

```
Algoritmo <nombre>
    Leer <variable>
    <variable> <- <expresión>
    Escribir <expresión>

    Si <condición> Entonces
        ...
    SiNo
        ...
    FinSi

    Mientras <condición> Hacer
        ...
    FinMientras

    Para <variable> <- <inicio> Hasta <fin> Hacer
        ...
    FinPara
FinAlgoritmo
```

Subprogramas:

```
Funcion <nombre>(<parámetros>)
    ...
    Retornar <expresión>
FinFuncion
```

> **Confirmada por el autor (2026-09-14)**: esta es la convención del track, estilo PSeInt en
> español. Las lecciones 1-3 ya están escritas con ella, así que cambiarla ahora obliga a
> reescribir sus 18 enunciados (y los 40+ que faltan).

## Tutor socrático en Track 0

El prompt del tutor debe adaptarse: sobre pseudocódigo se pregunta por la **traza**
("¿cuánto vale `i` en la tercera vuelta?", "¿qué condición hizo que saliera del bucle?"),
nunca por sintaxis de Python.

## ELO y competencias

Categoría propia **`algoritmos`** (no `fundamentos`: esa ya la usan cuatro lecciones de
Track 1 y las dos competencias se habrían fundido en una). El error se coló de verdad al
escribir las lecciones 4 y 5, así que ahora hay un guard rail que lo impide:
`test_ninguna_categoria_se_comparte_entre_tracks`. Registrada en `Competencies.tsx`
(`CATEGORY_LABELS`, `CATEGORY_TO_TRACK`, `TRACK_INFO` y `TRACK_ORDER`) y en
`backend/app/core/tracks.py`. Verificado: un alumno de Track 0 aparece en
`/progress/competencies` y en `/progress/track-status` como cualquier otro.

El ELO por categoría (`puzzle:algoritmos` y derivadas), con lazy-init que no contamine el
rating global, queda para cuando haya puzzles de Track 0.

## Dependencia

**Saldada.** El bug de persistencia del progreso se cerró y se verificó en producción
(Bloque 1 del plan de correcciones), así que el piloto de Track 0 se construyó encima de un
progreso que ya funcionaba. De hecho no hubo que tocarlo: aprobar un ejercicio de Track 0
crea una `CodeSubmission` con `result="success"` igual que uno de Python, así que XP,
progreso, competencias y track-status no se enteran de que el ejercicio no era código.

## Ubicación en el orden curricular

`Lesson.order` es global y monótono (Track 1 va del 1 al 10, Track 2 del 11 al 21...), así que
Track 0 usa **órdenes negativos**: -10 a -6 para las lecciones 1-5, y hasta el 0 para las
que faltan. Alternativa descartada: renumerar las 48 lecciones existentes, que toca contenido
ya verificado en producción a cambio de nada.
