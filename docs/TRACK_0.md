# Track 0 — Fundamentos de programación

Tramo de entrada de PyCode, previo a Track 1 (Python). El alumno aprende a **razonar
algoritmos antes de escribir código**: pseudocódigo, trazas de ejecución, estructuras de
datos elementales y diagramas de flujo.

> Estado: **en diseño**. Este documento es la fuente de verdad del track; el README enlaza aquí.

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

1. Los ejercicios de Track 0 se validan de forma **determinista en el cliente**, sin Pyodide
   y sin LLM.
2. Al aprobar, emiten **el mismo evento de completitud** que un ejercicio de Python. XP,
   progreso de lección, ELO y competencias no se ramifican por tipo de ejercicio.
3. La solución correcta **no viaja al cliente**. Aplica el mismo guard rail de no-leak que
   `hidden_tests` y `reference_solution`, con su test.
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

## Diagramas de flujo

Se renderizan con **Mermaid** (`flowchart`), no como imágenes: texto versionable, editable,
accesible y con tema claro/oscuro. En toda lección con condicionales o bucles se muestra el
diagrama junto al pseudocódigo equivalente — la equivalencia entre ambos *es* el concepto que
se enseña.

Fuera de alcance: editor gráfico de diagramas.

## Temario

| # | Lección | Núcleo |
|---|---|---|
| 1 | Qué es un algoritmo | Entrada/proceso/salida, precisión, finitud, ambigüedad |
| 2 | Variables, tipos y expresiones | Asignación, evaluación de expresiones, tipos en pseudocódigo |
| 3 | Traza de ejecución | Seguir un algoritmo a mano — **habilidad central del track** |
| 4 | Condicionales | Decisiones simples, anidadas, condiciones compuestas |
| 5 | Bucles | Mientras / Para, contadores, acumuladores, condición de parada |
| 6 | Diagramas de flujo | Símbolos y equivalencia con el pseudocódigo |
| 7 | Descomposición | Subprogramas, parámetros, valor de retorno |
| 8 | Arreglos y recorridos | Indexación, recorrido completo, búsqueda lineal |
| 9 | Algoritmos clásicos | Máximo, conteo, intercambio, ordenamiento por selección y burbuja |
| 10 | Cuánto cuesta un algoritmo | Contar operaciones, comparación intuitiva de eficiencia |
| 11 | Capstone: del pseudocódigo al Python | Implementar en Python tres algoritmos ya trazados a mano |

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

> **Pendiente de decisión del autor**: confirmar o reemplazar esta convención por la que se
> use en clase antes de generar contenido. Cambiarla después obliga a reescribir los 60+
> enunciados del track.

## Tutor socrático en Track 0

El prompt del tutor debe adaptarse: sobre pseudocódigo se pregunta por la **traza**
("¿cuánto vale `i` en la tercera vuelta?", "¿qué condición hizo que saliera del bucle?"),
nunca por sintaxis de Python.

## ELO y competencias

Categoría propia (`puzzle:fundamentos` y derivadas), con lazy-init que no contamine el rating
global de un alumno que llega desde Track 1. La categoría se registra en `Competencies.tsx`;
verificar que el gráfico de competencias no se rompe con un alumno de Track 0 vacío.

## Dependencia

**No implementar Track 0 antes de cerrar el bug de persistencia del progreso** (ejercicios
aprobados que no se marcan completados, barras que no llegan al 100%). Los tipos de ejercicio
nuevos heredarían el mismo fallo y habría que depurar dos sistemas a la vez.
