# Barrido de problemas (Bloque 7)

Inventario de lo que está mal o a medias en el repo, a **2026-09-09**, con
Track 1 recién cerrado.

**Esto es una lista, no un plan de trabajo.** El Bloque 7 pide *listar, no
implementar*: aquí no se ha tocado nada. Cada punto lleva su evidencia para que
se pueda comprobar sin creerme, y una estimación de esfuerzo para decidir qué
entra y qué no.

## Método

Todo lo medible sale de comandos que se pueden repetir:

- Métricas de contenido: sobre `LESSON_TEMPLATES` de `lesson_seed.py` (lo que se
  seedea), no sobre la base de datos.
- Tests que aprueban solos: cada `hidden_test` ejecutado contra el **starter**
  del ejercicio, en un directorio temporal. Si pasa, no comprueba nada.
- Dependencias: `npm audit --omit=dev` y el contador de Dependabot que devuelve
  GitHub al hacer push.
- Frontend: `npm run build` y `npm run lint` (los dos en verde) y el tamaño de
  `frontend/dist/assets/`.

## Resumen

| # | Problema | Prioridad | Esfuerzo |
|---|---|---|---|
| 1 | 14 `hidden_tests` aprueban con el starter intacto, 7 de ellos en Track 1 | **P1** | 1-2 h |
| 2 | Los enunciados de ejercicio no se renderizan como Markdown | **P1** | 2 h |
| 3 | `react-router` con open redirect llega a producción | **P1** | 15 min |
| 4 | Tracks 2-5 se quedaron muy por debajo del estándar de Track 1 | P2 | grande |
| 5 | El enunciado del editor es un `textarea` editable que alimenta al evaluador | P2 | 1 h |
| 6 | Bundle único de 1,09 MB sin code splitting | P2 | 2-3 h |
| 7 | El frontend tiene 3 archivos de test para 20 páginas | P2 | grande |
| 8 | 33 alertas de Dependabot sin triar desde el 3 de septiembre | P2 | 1 h |
| 9 | Un bucle infinito bloquea el sandbox (issue #32) | P2 | ver issue |
| 10 | `lesson_content.py`: 3.543 líneas de código muerto ya desincronizado | P3 | 10 min |
| 11 | `Elo_pycode/`: staging con tres archivos que difieren del árbol | P3 | 30 min |
| 12 | `AUDITORIA_CONTENIDO.md` describe un Track 1 que ya no existe | P3 | 10 min |
| 13 | `CodeEditor.tsx` con 884 líneas | P3 | grande |
| 14 | `/ws/code` sigue montado, deprecado | P3 | 10 min |

---

## P1 — llega al alumno hoy

### 1. Catorce `hidden_tests` aprueban sin escribir una línea

Un test que pasa con el starter intacto no comprueba nada: da por bueno un
ejercicio vacío.

```
track   | tests | pasan con el starter
track-1 |   200 |  7
track-2 |   103 |  7
track-3 |    65 |  0
track-4 |    15 |  0
track-5 |     9 |  0
```

Los siete de Track 1 están en las **tres primeras lecciones que se reescribieron**
(Bucles, Funciones, Comprensiones), antes de que la regla "ningún test pasa con el
starter" entrara en la plantilla. Las siete restantes son de Track 2. El patrón es
casi siempre el mismo: *"no muta el original"*, que un starter que no hace nada
cumple de sobra.

- Track 1: `Tabla del 7`, `Descartar lecturas invalidas`, `Parar en el primer
  negativo`, `Normalizar una lista de nombres`, `Division segura`, `Validar edad`,
  `Guardar un informe`.
- Track 2: `ReLU sin loops`, `Extraer mes de una fecha`, `Rellenar edad con la
  media`, `Pipeline de limpieza completo`, `Binning de edad en grupos`, `Normalizar
  con min-max y z-score`, `IC 95% de la media con bootstrap`.

El arreglo es el mismo que se aplicó en las otras siete lecciones: añadir al test
la comprobación positiva que le falta (que el resultado exista y valga lo que debe),
no quitar la negativa. **Es una cota inferior**: un test que aquí falla porque le
falta un import se cuenta como no trivial.

Vale la pena que esto deje de depender de acordarse: el mismo barrido cabe en un
test de `backend/tests/` que recorra `LESSON_TEMPLATES` y falle si algún
`hidden_test` pasa contra su starter.

### 2. Los enunciados no se renderizan como Markdown

`instructions` se pinta como texto plano en las dos vistas:

- [`LessonDetail.tsx:191`](../frontend/src/pages/LessonDetail.tsx) — un `<p>` con
  `whitespace-pre-wrap`.
- [`CodeEditor.tsx:649`](../frontend/src/pages/CodeEditor.tsx) — un `<textarea>` de
  cuatro filas.

Los backticks y los `**` salen literales en los enunciados de las 40 lecciones. El
contenido de la lección sí es Markdown con resaltado (eso se arregló en el Bloque
5); son los enunciados los que se quedaron atrás.

Al escribir Track 1 se compensó a mano (las salidas esperadas van indentadas en vez
de en bloques de código), pero es una servidumbre que no debería existir.

### 3. `react-router` con open redirect en producción

`npm audit --omit=dev` sobre las dependencias que llegan al navegador:

| Paquete | Aviso | Alcance real |
|---|---|---|
| `react-router` / `react-router-dom` | Open redirect por backslash en `<Link>` y `useNavigate` (bypass de CVE-2025-68470) | **Llega a producción**: es el router de la SPA |
| `postcss`, `postcss-selector-parser` | Path traversal por `sourceMappingURL`, DoS por recursión | Build-time (Tailwind), no se ejecuta en el navegador |
| `nanoid` | Bucle infinito con tamaño negativo o cero | Build-time |

El primero es el único con alcance de verdad y se arregla con un bump de versión.
Los otros tres son del criterio P3-P4 de
[SEGURIDAD_DEPENDENCIAS.md](SEGURIDAD_DEPENDENCIAS.md): severidad alta, alcance
nulo.

---

## P2 — deuda que crece

### 4. Tracks 2-5 se quedaron por debajo del estándar

Track 1 era el peor del temario y ahora es, de largo, el mejor. Las mismas métricas
con las que se midió su reescritura, aplicadas a los otros cuatro:

| Track | Lecciones | Chars medios | Líneas anotadas | Ejercicios | Sin *Errores comunes* |
|---|---|---|---|---|---|
| **1** | 10 | **6.164** | **84%** | **60** (6 por lección) | 0 |
| 2 | 11 | 3.453 | 40% | 33 (3 por lección) | 0 |
| 3 | 11 | 4.847 | 22% | 33 | 3 |
| 4 | 5 | 3.168 | 22% | 15 | 0 |
| 5 | 3 | 3.866 | 7% | 9 | 0 |

El alumno que termine Track 1 y entre en Track 2 va a notar el escalón: la mitad de
contenido por lección, la mitad de ejercicios y una quinta parte de los comentarios
que explican qué devuelve cada línea.

No propongo repetir el trabajo entero: 30 lecciones a este nivel de detalle es
mucho más que lo que costó Track 1. Pero conviene decidir explícitamente si el
estándar de la plantilla aplica a todo el temario o solo al arranque, porque hoy la
respuesta de facto es "solo al arranque" sin que nadie lo haya decidido.

### 5. El enunciado del editor es editable

En `/editor?lesson=...` el enunciado vive en un `<textarea>` que el alumno puede
modificar o borrar. No es un descuido: **ese mismo campo es lo que se manda al
evaluador** (`problem_description`), y poder ajustarlo tiene sentido en el modo
libre. En modo lección no: si lo borra, pierde el enunciado hasta recargar, y si lo
cambia, evalúa contra otra cosa.

### 6. Un solo bundle de 1,09 MB

```
frontend/dist/assets/index-*.js    1.089.780 bytes
frontend/dist/assets/index-*.css      48.216
frontend/dist/assets/pyodideWorker-*.js  25.512
```

Vite avisa (`Some chunks are larger than 500 kB`). Todo va en un chunk: el editor
Monaco, el markdown con resaltado, los gráficos y las 20 páginas, se abra la que se
abra. El runtime de Pyodide no está aquí (se carga desde el CDN, lazy), así que el
1 MB es código propio y librerías. Un `React.lazy` por ruta y un `manualChunks` para
Monaco arreglan la mayor parte.

### 7. Cobertura de tests del frontend

3 archivos de test (`MarkdownCodeBlock`, `CodeEditor`, `Lessons`) para 20 páginas y
el sandbox, contra 35 módulos de test en el backend. Lo que se ha roto en
producción este mes —el progreso que no persistía, la navegación del editor— era
todo de frontend.

### 8. Dependabot sin triar

GitHub reporta **33 alertas** (1 crítica, 19 altas, 11 moderadas, 2 bajas) al hacer
push. [SEGURIDAD_DEPENDENCIAS.md](SEGURIDAD_DEPENDENCIAS.md) clasificó 35 el 3 de
septiembre; no consta si la crítica de hoy es una de aquellas o es nueva. El triaje
es del usuario (el criterio P1-P4 es suyo), pero conviene rehacerlo con la lista
actual.

### 9. Issue #32: el bucle infinito bloquea el sandbox

Ya diagnosticado y medido en el issue: el timeout del runner no puede interrumpir
código Python síncrono, así que un `while True:` deja el worker inservible hasta
recargar la página. La lección 4 lo avisa por escrito, que era el parche mientras
duraba Track 1. Track 1 está cerrado: toca decidir.

---

## P3 — limpieza

### 10. `lesson_content.py`, 3.543 líneas de código muerto

Nadie lo importa (`grep -rn "lesson_content" backend --include=*.py` no devuelve un
solo import). Duplica el contenido de Track 1 en una versión que ya **no** es la
que se seedea, así que además de pesar, engaña: quien lo abra creyendo que edita
lecciones estará editando un archivo que no llega a ninguna parte. Ya está avisado
en CLAUDE.md, que es exactamente la señal de que sobra.

### 11. `Elo_pycode/` diverge del árbol

`elo_service.py`, `elo_models.py` y `puzzle_seed.py` difieren de sus homólogos en
`backend/app/`. La convención dice que es un *staging area* pendiente de integrar,
pero lleva ahí desde la Fase 2 y hoy la duda es al revés: ¿cuál de las dos versiones
es la buena? Integrar o borrar, pero no dejarlo empatado.

### 12. `AUDITORIA_CONTENIDO.md` quedó desfasado

Es un snapshot fechado del 2026-09-03 cuyo diagnóstico central —"las 10 lecciones de
Track 1 no tienen contenido"— ya no describe la realidad. La fecha está puesta en la
cabecera, así que no miente, pero un lector rápido se lleva la idea contraria.
Basta una nota arriba diciendo que el diagnóstico se resolvió y dónde.

### 13. `CodeEditor.tsx`, 884 líneas

Es la página más grande con diferencia (la siguiente tiene 501). Lleva el editor,
el runner, la navegación de ejercicios, el evaluador, los tests, los gráficos y el
tutor. No está roto, pero cada arreglo ahí es más caro que en cualquier otro sitio.

### 14. `/ws/code` sigue montado

`main.py:99` sigue registrando la ruta deprecada, que solo manda un mensaje y
cierra. Nadie del frontend la usa. O se retira, o se documenta hasta cuándo se
mantiene.

---

## Lo que se miró y está bien

Para que la lista no parezca peor de lo que es:

- `npm run build` y `npm run lint` en verde, sin warnings de ESLint.
- 177 tests de backend en verde, **ninguno saltado ni marcado `xfail`**.
- Cero `TODO`/`FIXME`/`HACK` en `backend/app` y `frontend/src` (los `# TODO` que
  aparecen son parte de los `starter_code` de los ejercicios, que es donde deben
  estar).
- Cero `console.log` en el frontend.
- Los 150 ejercicios tienen `hidden_tests` y **los 150 tienen pistas**.
- Track 4 y Track 5 no tienen ningún test que apruebe con el starter.
