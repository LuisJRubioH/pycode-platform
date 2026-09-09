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
pide algo que nadie enseñó. Empezó con 13 huecos congelados en
`HUECOS_CONOCIDOS`; las tres primeras reescrituras los cerraron todos y **hoy
la lista está vacía**: el test ya no protege deuda, es un guard rail puro. Si
al escribir una lección aparece un hueco, la respuesta por defecto es enseñar
el concepto con un ejemplo, no anotarlo en la lista.

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
- [ ] **Ningún `hidden_test` pasa con el starter.** Uno que aprueba sin código
      del alumno no comprueba nada: pasa con `...` como cuerpo, con un `None`
      devuelto por defecto o con una lista que nadie tocó. Se detecta corriendo
      cada test dos veces, contra la solución y contra el starter.
- [ ] `pytest backend/tests/test_prerequisitos_conceptos.py` en verde. La lista
      de huecos está vacía: si aparece uno, se enseña el concepto con un
      ejemplo en vez de anotarlo.
- [ ] Los ejemplos se han **ejecutado**, no solo escrito, y **cada bloque corre
      por sí solo**: si el segundo necesita una variable del primero, el alumno
      que lo copia ve un `NameError`.

## Plan de reescritura de Track 1

Orden **por gravedad de hueco**, no por número de lección. Las tres primeras cerraron
los 13 huecos de `HUECOS_CONOCIDOS`, que ya está vacío; de aquí en adelante el test
de prerequisitos es un guard rail puro y el orden lo marca la calidad del contenido.

| # | Lección | Orden curric. | Qué cubre | Hueco que cerraba |
|---|---|---|---|---|
| ✅ | Bucles for y while | 4 | for, range, acumuladores, while, break, continue | `break`/`continue`, prometidos en la description y ausentes del contenido |
| ✅ | Funciones y Parámetros | 5 | `def`, parámetros, `return`, argumentos por defecto, docstring | **`def` ×3** (Área de rectángulo, Saludo configurable, División segura) |
| ✅ | Comprensiones y Manejo de Errores | 7 | comprensiones, `try`/`except`, `raise`, `with` como garantía de limpieza | **`raise` ×2** (AI 2, Cuenta bancaria) · **`with` ×1** (Prueba de calculadora) |
| ✅ | POO en Python | 8 | `class`, `self`, `__init__`, métodos, colecciones como estado, encapsulación, `__str__` | **`class`/`self`/`__init__` ×6** (Clase Producto, Cuenta bancaria) — los 6 últimos |
| ✅ | Listas, Tuplas y Diccionarios | 6 | listas, indexado y slicing, métodos, tuplas y desempaquetado, dicts con `.get` e `.items` | — (era la peor del temario con 148 caracteres, y POO se apoyaba en ella) |
| ✅ | Python desde Cero | 1 | `print`, orden de ejecución, primera variable, f-strings, comentarios, leer un error | — |
| **1** | **Variables y Tipos** | 2 | int/float/str/bool, conversión, f-strings, mutabilidad | — |
| **2** | **Condicionales y Lógica** | 3 | `if`/`elif`/`else`, comparadores, `and`/`or`/`not`, truthiness | — |
| 3 | Módulos, Paquetes y Entornos | 9 | módulos, `import`, `__name__`, venv, pip | — |
| 4 | Testing con pytest | 10 | tests, `assert`, `pytest.raises`, casos borde | — |

Con 6 ejercicios por lección, Track 1 pasa de 18 a 60: **42 ejercicios nuevos**, que
se escriben junto a su lección y no como tarea aparte. Llevamos **6 lecciones y 36
ejercicios**; quedan cuatro lecciones, todas sin hueco que cerrar.

### Deudas que deja este orden

**Releer las lecciones 5, 6, 7 y 8 después de reescribir las lecciones 1-3.** Se
escriben antes que la 1, 2 y 3, así que sus ejemplos se apoyan en variables,
tipos y condicionales que todavía estarán en su versión pobre. El contenido es
correcto —esos temas existen aunque flojos—, pero al reescribir 1-3 hay que volver a
las cuatro y comprobar que los ejemplos encajan con lo que para entonces se enseñe
de verdad. Se acepta a cambio de cerrar `def`, `raise` y `class` cuanto antes.

Un caso concreto ya localizado: la 6 usa `texto.split()` para partir en palabras y
lo explica de pasada en el enunciado del ejercicio. Los métodos de string son de
"Variables y Tipos" (lección 2); al reescribirla, `split` va allí y la 6 lo da por
sabido.

**"POO en Python" (lección 8) enseña tuplas y `dict.get()` sobre la marcha.** Su
sección de colecciones como estado guarda pares `(nombre, precio)` en una lista y
usa `self.unidades.get(nombre, 0)`, y los dos ejercicios finales los piden. Por
temario eso es de "Listas, Tuplas y Diccionarios" (lección 6), que hoy tiene 148
caracteres y no enseña ninguna de las dos cosas — por eso la 6 pasa a ser la
siguiente de la lista. Al reescribirla hay que decidir si la 8 sigue explicándolas
o pasa a darlas por sabidas y solo las usa. El test de prerequisitos **no** cubre
esto: ni las tuplas ni `.get` están en `CONCEPTOS`.

**Las f-strings ya tienen sitio: la lección 1.** Estuvieron sueltas mucho tiempo
-la 5 las introducía sobre la marcha y el ejercicio "Hola Python" las pedía desde el
primer día sin que nadie las hubiera enseñado-. Al reescribir "Python desde Cero" se
metieron ahí, que es donde el alumno las necesita por primera vez. La 2 y la 5 las dan
por sabidas; la 2, como mucho, las repasa con el resto del formato de texto.

**No rehacer los ejercicios ya validados de las lecciones 9 y 10.** "Refactor a
modulo" (lección 9) y "Prueba de calculadora" (lección 10) se rediseñaron y se
validaron en Pyodide real. Al reescribir el **contenido** de esas dos lecciones hay
que respetar los ejercicios existentes y limitarse a añadir los que falten hasta
seis. Es lo que se hizo en POO: "Clase Producto" y "Cuenta bancaria" conservan su
título y su contrato (y por tanto su id y el progreso de quien los aprobó), solo se
les añadieron enunciado, pistas y tests, y los otros cuatro son nuevos.

### Limitación de plataforma pendiente

Un bucle infinito bloquea el sandbox de forma permanente: el timeout del runner no
puede interrumpir código Python síncrono. Está documentado con el diagnóstico y las
mediciones en el **issue #32**, y se aborda **después** de Track 1. Mientras tanto la
lección 4 lo avisa en el contenido.

## Los enunciados se muestran en texto plano

`instructions` **no se renderiza como Markdown** en ninguna de las dos vistas: la
lección lo pinta con `whitespace-pre-wrap`
([LessonDetail.tsx](../frontend/src/pages/LessonDetail.tsx)) y el editor lo mete en
un `textarea` de cuatro filas
([CodeEditor.tsx](../frontend/src/pages/CodeEditor.tsx)), donde además es editable
porque el mismo campo alimenta al evaluador.

Consecuencia al escribir: los backticks y los `**` salen literales, y un bloque
con triples backticks se ve como tres backticks. Para mostrar una salida esperada,
indéntala cuatro espacios en vez de usar un bloque de código. El contenido de la
**lección** sí es Markdown con resaltado de sintaxis: ahí no hay limitación.

## Cómo llega a producción

Editar `backend/app/services/lesson_seed.py` y desplegar. El seeder hace
**upsert por título** y actualiza en sitio preservando los ids, así que el
progreso de los alumnos no se pierde. Sin migración.

Cuidado con **renombrar**: un título nuevo se trata como lección/ejercicio
distinto, y el viejo se borra con sus submissions en cascada. Antes de cambiar
un título, comprobar si tiene progreso registrado.

`lesson_content.py` es código muerto: no lo importa nadie. No editarlo.
