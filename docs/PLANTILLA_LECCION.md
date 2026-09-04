# Plantilla de lección

Estructura estándar para escribir (o reescribir) una lección de PyCode. Está
sacada de **una lección concreta que ya funciona**, no de un promedio de las 30.

Su primer destino es la reescritura de Track 1, cuyo diagnóstico está en
[AUDITORIA_CONTENIDO.md](AUDITORIA_CONTENIDO.md).

## El modelo: "Pandas: limpieza de datos y missing values"

De las 30 lecciones de Tracks 2-5, es la que puntúa más alto midiendo
estructura (`##`), cantidad de ejemplos ejecutables, proporción de líneas de
código anotadas, presencia de *Errores comunes* y *Resumen*, y curva de
dificultad de los ejercicios.

| | La modelo | Mejor rival | Mediana de las 30 |
|---|---|---|---|
| Secciones `##` | **8** | 7 | 6 |
| Bloques de código | **6** | 7 | 6 |
| Líneas de código de ejemplo | **23** | 8 | 22 |
| **Líneas con comentario explicativo** | **78%** | 62% | ~20% |
| *Errores comunes* + *Resumen* | ✅ | ✅ | 27/30 y 30/30 |
| Curva easy → medium → hard | ✅ | ✅ | 19/30 |

Lo que la separa del resto no es la longitud —hay lecciones de ML con 6.000
caracteres, casi el doble— sino que **casi cada línea de ejemplo lleva un
comentario que dice qué devuelve o qué decisión implica**. Eso es lo que
convierte un bloque de código en una explicación:

```python
df.isna()           # DataFrame booleano del mismo shape
df.isna().sum()     # cuantos NaN por columna
df['col'].notna()   # mascara inversa
```

La mediana de las lecciones anda por el 20% de líneas anotadas. Esa diferencia
es la plantilla.

## Anatomía

### 1 · `## Por que <tema>` — la apuesta

Abre siempre con **por qué le importa al alumno**, con algo concreto en juego.
La modelo dice: *"La regla general en DS: 70% del tiempo es limpieza, 30% es
modelado. Esta lección es la caja de herramientas que vas a usar todos los
días."*

No es decoración: es lo que sostiene la atención de alguien que no sabe todavía
para qué sirve lo que va a leer. 3-6 líneas.

### 2 · Una sección `##` por operación, cada una con su ejemplo

De 4 a 7 secciones, cada una con **nombre de la operación concreta**
(`## fillna — rellenar NaN`), no un rótulo genérico. Cada sección lleva:

1. Un bloque ```` ```python ```` con 3-6 líneas.
2. **Comentario al final de cada línea** con lo que devuelve o el matiz.
3. Debajo, la prosa que aporta el criterio de decisión, no la repetición del
   código.

La prosa responde a *cuándo usar cuál*, que es lo que no cabe en un comentario:

> **Decisiones de imputación**: numérico no crítico → media o mediana; series
> temporales → `ffill`; categórico → una categoría nueva; crítico → mejor
> `dropna`.

### 3 · `## Errores comunes`

De 3 a 5 viñetas. Cada una con las tres partes: **qué se hace mal, por qué
duele, y cuál es la forma correcta.** No vale "cuidado con los NaN".

> `astype(int)` con NaN presente: ValueError. Usar `'Int64'` (mayúscula) o
> llenar NaN antes.

Es la sección que más se salta al escribir con prisa: falta en 3 de las 30
(ML 9, 10 y 11) y en las 10 de Track 1.

### 4 · `## Resumen`

Una viñeta por sección, cada una con el nombre del método y qué resuelve.
Sirve como chuleta de repaso, no como conclusión.

## Los ejercicios

La modelo tiene 3 (easy/medium/hard). **Para Track 1 el objetivo son 6 por
lección**, así que la curva se estira manteniendo su forma:

| # | Dificultad | Puntos | Pistas | Tests | Qué pide |
|---|---|---|---|---|---|
| 1-2 | easy | 10 | 2 | ≥2 | Un solo concepto, aplicación directa |
| 3-4 | medium | 15 | 3 | ≥3 | Un concepto con una decisión o un caso borde |
| 5 | hard | 20 | 4 | ≥3 | Dos conceptos de la lección combinados |
| 6 | hard | 25 | 4 | ≥4 | El "pipeline": tres o más conceptos encadenados |

Reglas que la modelo cumple y conviene copiar:

- **El enunciado fija el nombre exacto y el tipo de retorno.** *"Implementa
  `nulos_por_columna(df)` que devuelve una Serie indexada por nombre de columna
  con la cantidad de NaN"*. Sin ambigüedad no hay discusión con el test.
- **Las pistas escalan hacia la respuesta.** La primera orienta
  (*"`df.isna()` es un DataFrame booleano"*), la última casi da la línea
  (*"`out['edad'] = out['edad'].fillna(media)`"*). El alumno decide cuánta
  ayuda toma.
- **El último ejercicio encadena.** "Pipeline de limpieza completo" usa `.str`,
  `fillna` y `drop_duplicates` juntos, y una de sus pistas es *"el orden de los
  pasos importa"*. Es donde se ve si entendió o solo copió.
- **Los `hidden_tests` verifican comportamiento, no forma.** Nada de comprobar
  que el código contenga cierta cadena.

## Regla dura: nada se pide antes de haberse enseñado

**Todo concepto que un ejercicio exige tiene que aparecer antes en un bloque de
código ejecutable**, en esa lección o en una anterior del temario. La prosa no
cuenta: *"Usa `__init__` para estado inicial"* en una viñeta no enseña a
escribir un método.

Esto **no es una recomendación, es un test**:
`backend/tests/test_prerequisitos_conceptos.py` recorre el temario en orden,
acumula lo que se ha mostrado dentro de bloques ``` y falla si un ejercicio
pide algo que nadie enseñó. Hoy tiene congelados 13 huecos conocidos (todos de
Track 1 salvo uno); según se reescriban las lecciones, se van borrando de
`HUECOS_CONOCIDOS`.

Su límite: detecta *tokens de Python*, no paráfrasis. "Cuenta bancaria" pide
"lanza ValueError" sin escribir `raise`, y eso se le escapa. Es un suelo, no un
techo: al escribir hay que mirar también los enunciados en español.

## Restricciones del runner al diseñar ejercicios

El código del alumno corre en Pyodide dentro de un Web Worker, no en un Python
normal. Tres cosas cambian, verificadas ejecutándolas (detalle en
[AUDITORIA_CONTENIDO.md](AUDITORIA_CONTENIDO.md)):

1. **`__name__` vale `'builtins'`, no `'__main__'`.** El bloque
   `if __name__ == "__main__":` **nunca se ejecuta**. No se puede ejercitar ni
   verificar el *main guard*: se explica como teoría, con una nota diciéndole
   al alumno por qué aquí no lo puede probar. No se parchea el runner por un
   patrón.
2. **`sys.modules` sobrevive entre ejecuciones.** Si un ejercicio hace que el
   alumno escriba e importe un módulo, el starter code **debe** llevar
   `sys.modules.pop('<modulo>', None)`; sin eso, corrige su archivo y sigue
   viendo el error viejo.
3. **Un solo archivo por ejercicio.** El runner concatena todo en un namespace;
   lo multiarchivo solo existe en `runCapstoneTests`. Un ejercicio de "módulos"
   se resuelve escribiendo el `.py` en el FS de Pyodide (`Path(...).write_text`
   + `sys.path`), que sí funciona.

A favor: **pytest 8.1.1 está disponible**, y un `hidden_test` puede **romper a
propósito el código del alumno** para comprobar que sus tests lo detectan — así
"escribe un test" no se aprueba con `assert True`.

## Antes de dar una lección por terminada

- [ ] Abre con `## Por que <tema>` y algo concreto en juego.
- [ ] 4-7 secciones `##`, cada una con su bloque de código.
- [ ] **≥ 60% de las líneas de ejemplo llevan comentario** con el resultado o
      el matiz (la modelo: 78%; la mediana actual: ~20%).
- [ ] `## Errores comunes` con 3-5 viñetas de qué/por qué/cómo.
- [ ] `## Resumen` con una viñeta por sección.
- [ ] 6 ejercicios con la curva de arriba y el último encadenando conceptos.
- [ ] Cada ejercicio con `hidden_tests` — hay un test que lo exige.
- [ ] `pytest backend/tests/test_prerequisitos_conceptos.py` en verde, con los
      huecos cerrados borrados de `HUECOS_CONOCIDOS`.
- [ ] Los ejemplos se han **ejecutado**, no solo escrito.

## Plan de reescritura de Track 1

Orden **por gravedad de hueco**, no por número de lección. Las tres primeras cierran
los 13 huecos que quedan en `HUECOS_CONOCIDOS`; a partir de ahí el test de
prerequisitos pasa a ser un guard rail puro.

| # | Lección | Orden curric. | Qué cubre | Hueco que cierra |
|---|---|---|---|---|
| ✅ | Bucles for y while | 4 | for, range, acumuladores, while, break, continue | `break`/`continue`, prometidos en la description y ausentes del contenido |
| **1** | **Funciones y Parámetros** | 5 | `def`, parámetros, `return`, argumentos por defecto, docstring | **`def` ×3** (Área de rectángulo, Saludo configurable, División segura) |
| **2** | **Comprensiones y Manejo de Errores** | 7 | comprensiones, `try`/`except`, `raise`, `with` como garantía de limpieza | **`raise` ×2** (AI 2, Cuenta bancaria) · **`with` ×1** (Prueba de calculadora) |
| **3** | **POO en Python** | 8 | `class`, `self`, `__init__`, métodos, encapsulación | **`class`/`self`/`__init__`/`def` ×8** (Clase Producto, Cuenta bancaria) |
| 4 | Python desde Cero | 1 | `print`, ejecutar código, sintaxis, indentación, errores de novato | — |
| 5 | Variables y Tipos | 2 | int/float/str/bool, conversión, f-strings, mutabilidad | — |
| 6 | Condicionales y Lógica | 3 | `if`/`elif`/`else`, comparadores, `and`/`or`/`not`, truthiness | — |
| 7 | Listas, Tuplas y Diccionarios | 6 | listas, tuplas, dicts, indexado, slicing, métodos | — (hoy 148 caracteres: la peor del temario) |
| 8 | Módulos, Paquetes y Entornos | 9 | módulos, `import`, `__name__`, venv, pip | — |
| 9 | Testing con pytest | 10 | tests, `assert`, `pytest.raises`, casos borde | — |

Con 6 ejercicios por lección, Track 1 pasa de 18 a 60: **42 ejercicios nuevos**, que
se escriben junto a su lección y no como tarea aparte.

### Dos deudas que deja este orden

**Releer "Funciones y Parámetros" después de reescribir las lecciones 1-3.** Se
escribe la 5 antes que la 1, 2 y 3, así que sus ejemplos se apoyan en variables,
tipos y condicionales que todavía estarán en su versión pobre. El contenido es
correcto —esos temas existen aunque flojos—, pero al reescribir 1-3 hay que volver a
la 5 y comprobar que los ejemplos encajan con lo que para entonces se enseñe de
verdad. Se acepta a cambio de cerrar `def` cuanto antes.

**Las f-strings se enseñan en "Funciones y Parámetros" (lección 5), fuera de su
sitio.** Se usaban en varios ejemplos sin haberse enseñado nunca, así que la 5 las
introduce sobre la marcha para no dejar el agujero. Por temario pertenecen a
"Variables y Tipos" (lección 2). Al reescribir la 2 hay que decidir si se mueven allí
y la 5 pasa a darlas por sabidas, o si se quedan donde están y la 2 solo las repasa.
El test de prerequisitos **no** cubre esto: las f-strings no están en `CONCEPTOS`.

**No rehacer los ejercicios ya validados de las lecciones 8, 9 y 10.** "Refactor a
modulo" (lección 9) y "Prueba de calculadora" (lección 10) se rediseñaron y se
validaron en Pyodide real; los de POO (lección 8) siguen siendo los originales pero
funcionan. Al reescribir el **contenido** de esas tres lecciones hay que respetar los
ejercicios existentes y limitarse a añadir los que falten hasta seis.

### Limitación de plataforma pendiente

Un bucle infinito bloquea el sandbox de forma permanente: el timeout del runner no
puede interrumpir código Python síncrono. Está documentado con el diagnóstico y las
mediciones en el **issue #32**, y se aborda **después** de Track 1. Mientras tanto la
lección 4 lo avisa en el contenido.

## Cómo llega a producción

Editar `backend/app/services/lesson_seed.py` y desplegar. El seeder hace
**upsert por título** y actualiza en sitio preservando los ids, así que el
progreso de los alumnos no se pierde. Sin migración.

Cuidado con **renombrar**: un título nuevo se trata como lección/ejercicio
distinto, y el viejo se borra con sus submissions en cascada. Antes de cambiar
un título, comprobar si tiene progreso registrado.

`lesson_content.py` es código muerto: no lo importa nadie. No editarlo.
