"""
Temario completo de Python para PyCode Platform.

Contiene LESSON_TEMPLATES con lecciones agrupadas en una ruta
principiante -> intermedio -> avanzado. Cada leccion incluye teoria extensa
con ejemplos, errores comunes y ejercicios dirigidos.

El contenido se usa desde ``lesson_seed.py`` para poblar las tablas.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExerciseTemplate:
    title: str
    description: str
    instructions: str
    starter_code: str
    hints: list[str] = field(default_factory=list)
    points: int = 10
    difficulty: str = "easy"


@dataclass(frozen=True)
class LessonTemplate:
    title: str
    description: str
    content: str
    difficulty: str
    category: str
    order: int
    estimated_duration: int
    prerequisites_titles: list[str] = field(default_factory=list)
    exercises: list[ExerciseTemplate] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Ruta PRINCIPIANTE
# ---------------------------------------------------------------------------

L_INTRO = LessonTemplate(
    title="Python desde Cero",
    description="Que es Python, como instalarlo, ejecutar scripts y tu primer programa.",
    content="""## Objetivo
Entender que es Python, como se ejecuta y escribir tu primer programa.

## Que es Python
Python es un lenguaje de programacion **interpretado**, de **alto nivel** y de
**tipado dinamico**. Se usa en ciencia de datos, web, automatizacion, IA y
scripting general. Fue creado por Guido van Rossum en 1991 y su filosofia
enfatiza la legibilidad: "codigo limpio es mejor que codigo inteligente".

### Caracteristicas clave
- **Interpretado**: no compilas a binario, el interprete lee el `.py` linea a linea.
- **Multiparadigma**: soporta programacion imperativa, funcional y orientada a objetos.
- **Bateria incluida**: la libreria estandar (`os`, `datetime`, `json`, ...) trae todo lo necesario para empezar sin dependencias.
- **Tipado dinamico y fuerte**: una variable no tiene tipo fijo, pero sumar `"3" + 4` da error (no convierte implicitamente).

## Tu primer programa
```python
print("Hola, Python!")
```

`print()` es una **funcion** que recibe argumentos y los muestra en consola.
El texto entre comillas se llama **string**. Puedes usar comillas simples
`'...'` o dobles `"..."` indistintamente.

### Ejecutar el script
Guarda el archivo como `hola.py` y ejecuta desde terminal:
```
python hola.py
```

## Sintaxis y estilo
Python usa **indentacion** (4 espacios por convencion) en vez de llaves
`{ }` para delimitar bloques:

```python
if 3 > 2:
    print("tres es mayor")
    print("dentro del if")
print("fuera del if")
```

Si la indentacion es inconsistente, el programa falla con `IndentationError`.

### Comentarios
```python
# Esto es un comentario de linea
x = 5  # tambien se puede al final

'''
Comentario de varias lineas (tecnicamente es un string sin asignar).
'''
```

## Errores comunes al empezar
- **Olvidar los parentesis de `print`**: `print "hola"` es sintaxis de Python 2, no funciona en Python 3.
- **Mezclar tabuladores y espacios**: provoca `TabError`. Configura tu editor a 4 espacios.
- **No guardar el archivo**: ejecutar `python hola.py` antes de guardar muestra la version anterior.

## Resumen
- Python se ejecuta con `python archivo.py`.
- Los bloques se delimitan por indentacion consistente.
- `print()` muestra en consola; `#` inicia un comentario.
""",
    difficulty="beginner",
    category="fundamentos",
    order=1,
    estimated_duration=20,
    exercises=[
        ExerciseTemplate(
            title="Hola Python",
            description="Imprime un saludo personalizado.",
            instructions="Asigna tu nombre a la variable `nombre` y muestra 'Hola, <nombre>' usando un f-string.",
            starter_code="nombre = ''\n# TODO: usa print y un f-string\n",
            hints=["Usa print(f'Hola, {nombre}')", "Los f-strings llevan f antes de las comillas"],
        ),
        ExerciseTemplate(
            title="Mini presentacion",
            description="Varias lineas de salida.",
            instructions="Imprime tu ciudad y tu lenguaje favorito en dos lineas separadas.",
            starter_code="ciudad = ''\nlenguaje = 'Python'\n# TODO\n",
        ),
    ],
)

L_VARIABLES = LessonTemplate(
    title="Variables y Tipos",
    description="Numeros, strings, booleanos, None y conversion entre tipos.",
    content="""## Objetivo
Dominar los tipos primitivos de Python y la conversion entre ellos.

## Variables
Una variable es un nombre que referencia un valor:

```python
edad = 25
nombre = "Ana"
altura = 1.72
activo = True
```

No declaras el tipo: Python lo infiere del valor. Puedes reasignar con un
tipo distinto (pero no es buena practica).

## Tipos primitivos

### int (enteros)
```python
a = 42
b = -7
c = 1_000_000  # el _ es separador visual, no cambia el valor
```

### float (decimales)
```python
pi = 3.14159
g = 9.8
notacion = 1.5e3   # 1500.0
```

### str (texto)
```python
s1 = "con dobles"
s2 = 'con simples'
s3 = '''multi
linea'''
```

### bool (booleanos)
```python
es_mayor = True
tiene_pase = False
```
Internamente, `True == 1` y `False == 0`.

### None
Representa ausencia de valor:
```python
resultado = None
```
No es lo mismo que `0`, `False` o `""`.

## Inspeccionar tipos
```python
type(3)        # <class 'int'>
type(3.0)      # <class 'float'>
type("3")      # <class 'str'>
isinstance(3, int)  # True
```

## Conversion (casting)
```python
int("42")      # 42
int(3.9)       # 3 (trunca, no redondea)
float("3.14")  # 3.14
str(25)        # "25"
bool(0)        # False
bool("x")      # True (cualquier string no vacio es True)
```

### Reglas de "falsedad"
Son `False` al convertir a bool: `0`, `0.0`, `""`, `None`, `[]`, `{}`, `set()`.
Todo lo demas es `True`.

## Operadores aritmeticos
| Operador | Nombre | Ejemplo | Resultado |
|---|---|---|---|
| `+` | suma | `3 + 2` | 5 |
| `-` | resta | `3 - 2` | 1 |
| `*` | producto | `3 * 2` | 6 |
| `/` | division real | `7 / 2` | 3.5 |
| `//` | division entera | `7 // 2` | 3 |
| `%` | modulo | `7 % 2` | 1 |
| `**` | potencia | `2 ** 10` | 1024 |

## Errores comunes
- **`int("3.14")`** falla: usa `int(float("3.14"))`.
- **Sumar str + int** lanza `TypeError`: convierte antes con `str()` o usa f-strings.
- **Comparar float con `==`**: los floats tienen imprecision. Usa `math.isclose(a, b)`.

## Resumen
- Los tipos basicos son `int`, `float`, `str`, `bool`, `None`.
- `type()` e `isinstance()` inspeccionan tipos.
- Convierte explicitamente con `int()`, `str()`, `float()`, `bool()`.
""",
    difficulty="beginner",
    category="fundamentos",
    order=2,
    estimated_duration=25,
    prerequisites_titles=["Python desde Cero"],
    exercises=[
        ExerciseTemplate(
            title="Doble conversion",
            description="Convierte texto a numero y calcula.",
            instructions="Recibe `texto_numero` (str). Convierte a int, calcula el doble y guardalo en `resultado`.",
            starter_code="texto_numero = '12'\n# TODO: calcula el doble\n",
        ),
        ExerciseTemplate(
            title="Chequeo de tipos",
            description="Usa type() sobre variables.",
            instructions="Imprime el tipo de `edad`, `altura` y `activo`.",
            starter_code="edad = 18\naltura = 1.72\nactivo = True\n# TODO\n",
        ),
        ExerciseTemplate(
            title="Verdadero o falso",
            description="Practica falsedad.",
            instructions="Imprime True/False para bool(0), bool(''), bool('0'), bool([]), bool([0]).",
            starter_code="# TODO: prueba cada caso\n",
            hints=["'0' es un string no vacio", "[0] es una lista con un elemento"],
        ),
    ],
)

L_OPERADORES = LessonTemplate(
    title="Operadores y Expresiones",
    description="Operadores aritmeticos, de comparacion, logicos y de asignacion.",
    content="""## Objetivo
Combinar valores con operadores para formar expresiones correctas y legibles.

## Aritmeticos
Ya los vimos: `+`, `-`, `*`, `/`, `//`, `%`, `**`.
**Precedencia** (de mayor a menor): `**` > `*` `/` `//` `%` > `+` `-`.
Usa parentesis para forzar orden: `(3 + 4) * 2`.

## Comparacion
Devuelven `bool`:
```python
3 == 3      # True
3 != 4      # True
3 < 4       # True
3 <= 3      # True
"a" < "b"   # True (orden lexicografico)
```

Python permite comparaciones **encadenadas**:
```python
18 <= edad < 65   # equivale a  18 <= edad and edad < 65
```

## Logicos
```python
True and False   # False
True or False    # True
not True         # False
```

### Evaluacion corta (short-circuit)
`and` y `or` evaluan de izquierda a derecha y **paran** en cuanto saben el resultado.
Esto es util para defaults:
```python
nombre = entrada or "anonimo"  # si entrada es "" o None, usa "anonimo"
```

## Asignacion compuesta
```python
x = 5
x += 3     # x = x + 3   -> 8
x -= 1     # 7
x *= 2     # 14
x //= 3    # 4
x **= 2    # 16
x %= 5     # 1
```

## Identidad vs igualdad
```python
a = [1, 2]
b = [1, 2]
a == b    # True  (mismos valores)
a is b    # False (objetos distintos en memoria)
a is None # usa 'is' para comparar con None
```

**Regla**: usa `==` para valor, `is` para identidad (sobre todo con `None`).

## Operador ternario
```python
estado = "adulto" if edad >= 18 else "menor"
```

## Errores comunes
- **Confundir `=` con `==`**: `=` asigna, `==` compara.
- **`if x = 5:`** es error de sintaxis; debe ser `if x == 5:`.
- **Usar `==` con `None`**: funciona pero la guia oficial recomienda `is None`.

## Resumen
- Domina la precedencia; usa parentesis cuando tengas dudas.
- `and`/`or` hacen short-circuit.
- `is` compara identidad (mismo objeto), `==` compara valor.
""",
    difficulty="beginner",
    category="fundamentos",
    order=3,
    estimated_duration=25,
    prerequisites_titles=["Variables y Tipos"],
    exercises=[
        ExerciseTemplate(
            title="Orden y precedencia",
            description="Predice el resultado.",
            instructions="Calcula `2 + 3 * 4 ** 2` usando parentesis explicitos y muestra ambos resultados (con y sin parentesis).",
            starter_code="# TODO: imprime resultados\n",
        ),
        ExerciseTemplate(
            title="Rango encadenado",
            description="Usa comparacion encadenada.",
            instructions="Define `edad` y determina si esta en el rango [18, 65) usando una sola expresion.",
            starter_code="edad = 30\n# TODO: en_rango = ...\n",
        ),
    ],
)

L_STRINGS = LessonTemplate(
    title="Strings: operaciones y f-strings",
    description="Slicing, metodos, inmutabilidad y formato moderno con f-strings.",
    content="""## Objetivo
Manipular texto con los metodos y formatos mas usados.

## Strings son inmutables
Una vez creado, no puedes cambiar un caracter. Las "modificaciones" crean
un string nuevo:
```python
s = "hola"
s[0] = "H"  # TypeError
s = "H" + s[1:]   # ahora s es "Hola"
```

## Indexacion y slicing
```python
s = "Python"
s[0]      # 'P'
s[-1]     # 'n'  (ultimo)
s[0:3]    # 'Pyt'
s[:3]     # 'Pyt'
s[3:]     # 'hon'
s[::-1]   # 'nohtyP'  (invertido)
s[::2]    # 'Pto'     (paso 2)
```
Regla: `s[a:b:paso]`. `b` es **excluyente**.

## Metodos esenciales
```python
"hola".upper()          # 'HOLA'
"HOLA".lower()          # 'hola'
"  hola  ".strip()      # 'hola'
"hola".replace("o","0") # 'h0la'
"a,b,c".split(",")      # ['a','b','c']
",".join(['a','b','c']) # 'a,b,c'
"hola".startswith("ho") # True
"python".endswith("on") # True
"python".find("th")     # 2  (indice donde empieza, -1 si no)
"abc".count("b")        # 1
"abc".index("b")        # 1  (lanza ValueError si no)
len("python")           # 6
```

## f-strings (Python 3.6+)
La forma moderna y preferida de formatear:
```python
nombre = "Ana"
edad = 30
f"Hola, {nombre}, tienes {edad} anos"
f"Suma: {2 + 3}"            # 'Suma: 5'
f"Con 2 decimales: {3.14159:.2f}"  # 'Con 2 decimales: 3.14'
f"{'x':>10}"                 # derecha, ancho 10
f"{'x':<10}"                 # izquierda
f"{'x':^10}"                 # centrado
f"{42:04d}"                  # '0042' (rellena con ceros)
```

## Escapes y strings crudos
```python
"linea1\\nlinea2"     # \\n = salto de linea
"col1\\tcol2"         # \\t = tab
"comilla: \\""        # comilla escapada
r"C:\\ruta\\archivo" # raw string: no interpreta backslashes
```

## Errores comunes
- **Intentar mutar caracteres**: `s[0] = "X"` falla; crea un string nuevo.
- **Confundir `find` con `index`**: `find` devuelve -1 si no encuentra, `index` lanza excepcion.
- **Concatenar en bucle**: `s += otro` crea strings nuevos (costoso). Para muchas uniones usa `"".join(lista)`.

## Resumen
- Slicing `s[a:b:paso]` es inclusivo-exclusivo.
- Los strings son inmutables.
- Prefiere f-strings para formatear.
""",
    difficulty="beginner",
    category="fundamentos",
    order=4,
    estimated_duration=30,
    prerequisites_titles=["Operadores y Expresiones"],
    exercises=[
        ExerciseTemplate(
            title="Invertir y contar",
            description="Slicing y metodos.",
            instructions="Dada `frase`, imprime su version invertida y cuantas veces aparece la letra 'a' (mayusculas o minusculas).",
            starter_code="frase = 'La lluvia en Sevilla'\n# TODO\n",
            hints=["Normaliza con lower()", "Usa slicing [::-1]"],
        ),
        ExerciseTemplate(
            title="Ficha con f-string",
            description="Formato con alineacion.",
            instructions="Imprime una ficha con nombre alineado a la izquierda (ancho 15) y precio con 2 decimales.",
            starter_code="nombre = 'Cafe'\nprecio = 3.5\n# TODO\n",
        ),
    ],
)

L_IO = LessonTemplate(
    title="Entrada y salida",
    description="input(), print() con parametros y lectura basica de datos del usuario.",
    content="""## Objetivo
Leer datos del usuario y mostrar resultados con formato.

## print() avanzado
```python
print("a", "b", "c")                # a b c   (sep=' ' por defecto)
print("a", "b", sep="-")            # a-b
print("progreso...", end="")        # no salto de linea
print("terminado", end="\\n")
print("x", "y", sep=",", end=";\\n") # x,y;
```

### Imprimir a archivo
```python
with open("log.txt", "w") as f:
    print("algo", file=f)
```

## input()
Lee una linea como **string** (siempre).
```python
nombre = input("Tu nombre: ")
edad_str = input("Tu edad: ")
edad = int(edad_str)  # convierte explicitamente
```

### Patron tipico
```python
try:
    n = int(input("Numero: "))
except ValueError:
    print("Eso no era un numero valido")
```

## Multiples valores en una linea
```python
# El usuario escribe: "10 20 30"
partes = input("Numeros: ").split()
nums = [int(x) for x in partes]
```

## Errores comunes
- **Olvidar convertir**: `input()` siempre devuelve `str`; si esperas un numero, haz `int()` o `float()`.
- **`eval(input(...))`** es peligroso: ejecuta codigo arbitrario del usuario. Nunca lo uses con entrada no confiable.
- **No manejar errores de conversion**: usa `try/except ValueError` para entradas defensivas.

## Resumen
- `input()` devuelve siempre string.
- `print()` acepta `sep`, `end`, `file` y varios argumentos.
- Valida y convierte la entrada antes de usarla.
""",
    difficulty="beginner",
    category="fundamentos",
    order=5,
    estimated_duration=20,
    prerequisites_titles=["Strings: operaciones y f-strings"],
    exercises=[
        ExerciseTemplate(
            title="Suma dos numeros",
            description="Lee y suma.",
            instructions="Pide dos numeros al usuario (usa input) y muestra su suma.",
            starter_code="# TODO\n",
            hints=["Recuerda convertir con int() o float()"],
        ),
        ExerciseTemplate(
            title="Promedio de varios numeros",
            description="Lee N numeros y saca el promedio.",
            instructions=(
                "Pide primero un entero N. Despues lee N numeros (uno por linea) y muestra el promedio "
                "con dos decimales. Ejemplo: si N=3 y los numeros son 10, 20, 30, imprime 'Promedio: 20.00'."
            ),
            starter_code="n = int(input('Cuantos numeros? '))\n# TODO: leer n numeros y promediar\n",
            hints=[
                "Usa un bucle for range(n) para acumular la suma",
                "Formatea con f'{promedio:.2f}' para dos decimales",
            ],
            difficulty="medium",
            points=15,
        ),
        ExerciseTemplate(
            title="Numeros separados por espacios",
            description="Lee una linea con varios numeros.",
            instructions=(
                "Pide una linea tipo '4 7 2 9 1'. Divide con split(), convierte a int y muestra "
                "el minimo, el maximo y la suma en el formato: 'min=1 max=9 suma=23'. "
                "Si el usuario escribe algo que no es un numero, imprime 'Entrada invalida' y no revientes."
            ),
            starter_code="linea = input('Numeros separados por espacios: ')\n# TODO: split, convertir y mostrar\n",
            hints=[
                "try/except ValueError atrapa conversiones fallidas",
                "min(lista), max(lista) y sum(lista) te resuelven el calculo",
            ],
            difficulty="hard",
            points=20,
        ),
    ],
)

L_CONDICIONALES = LessonTemplate(
    title="Condicionales y logica",
    description="if, elif, else, operador ternario y patrones comunes de decision.",
    content="""## Objetivo
Tomar decisiones en tu codigo con condicionales claros y legibles.

## Estructura basica
```python
if condicion:
    ...
elif otra_condicion:
    ...
else:
    ...
```
Cada rama es un **bloque indentado**. `elif` y `else` son opcionales.

## Ejemplos
```python
edad = 17

if edad >= 65:
    print("senior")
elif edad >= 18:
    print("adulto")
elif edad >= 13:
    print("adolescente")
else:
    print("nino")
```

## Operador ternario (valor condicional)
```python
estado = "adulto" if edad >= 18 else "menor"
```
Util para asignaciones cortas, no abuses con logica compleja.

## match (Python 3.10+)
```python
status = 404
match status:
    case 200:
        print("OK")
    case 404 | 500:
        print("error servidor")
    case _:
        print("desconocido")
```

## Patrones utiles
### Default con `or`
```python
nombre = nombre_usuario or "anonimo"
```

### Verificacion de pertenencia
```python
if letra in "aeiou":
    print("vocal")
if nivel in {"free", "pro", "teams"}:
    print("plan valido")
```

### Guardia temprana (early return)
Reduce anidamiento profundo:
```python
def procesar(x):
    if x is None:
        return "sin dato"
    if x < 0:
        return "negativo"
    # logica principal aqui
    return x * 2
```

## Errores comunes
- **Olvidar los dos puntos**: `if x > 0` sin `:` es `SyntaxError`.
- **Usar `=` en lugar de `==`**: es `SyntaxError` en `if`.
- **Comparar con `== None`**: funciona pero se prefiere `is None`.
- **Anidar 5 niveles de if**: refactoriza con guardias tempranas o diccionarios.

## Resumen
- `if / elif / else` para decisiones.
- El ternario es para asignaciones cortas.
- Usa guardias tempranas y `in` para codigo limpio.
""",
    difficulty="beginner",
    category="control-flujo",
    order=6,
    estimated_duration=25,
    prerequisites_titles=["Entrada y salida"],
    exercises=[
        ExerciseTemplate(
            title="Clasificador de edad",
            description="if / elif / else.",
            instructions="Dada `edad`, imprime 'menor', 'adulto' o 'senior' segun 0-17, 18-64, 65+.",
            starter_code="edad = 17\n# TODO\n",
        ),
        ExerciseTemplate(
            title="Control de acceso",
            description="Combina condiciones logicas.",
            instructions="Permite acceso solo si `tiene_pase` es True y `edad >= 18`. Imprime 'OK' o 'Denegado'.",
            starter_code="tiene_pase = True\nedad = 19\n# TODO\n",
        ),
        ExerciseTemplate(
            title="Mini semaforo",
            description="Usa match o if/elif.",
            instructions="Dada `color`, imprime 'pare', 'precaucion' o 'avance' para rojo, amarillo, verde.",
            starter_code="color = 'verde'\n# TODO\n",
        ),
    ],
)

L_BUCLES = LessonTemplate(
    title="Bucles for y while",
    description="Iteracion con for, while, range, enumerate, zip y control con break/continue.",
    content="""## Objetivo
Repetir tareas con bucles expresivos y correctos.

## for
Recorre cualquier **iterable** (lista, tupla, string, dict, range, ...):
```python
for letra in "abc":
    print(letra)

for x in [10, 20, 30]:
    print(x)
```

## range
Genera numeros perezosamente:
```python
range(5)          # 0, 1, 2, 3, 4
range(2, 8)       # 2..7
range(0, 10, 2)   # 0, 2, 4, 6, 8
range(5, 0, -1)   # 5, 4, 3, 2, 1
```

## enumerate
Obten indice y valor al mismo tiempo:
```python
for i, nombre in enumerate(["Ana", "Luis", "Eva"], start=1):
    print(i, nombre)
# 1 Ana
# 2 Luis
# 3 Eva
```

## zip
Itera varias secuencias a la vez:
```python
for nombre, edad in zip(["Ana","Luis"], [25, 30]):
    print(nombre, edad)
```

## while
Repite mientras la condicion sea verdadera:
```python
n = 5
while n > 0:
    print(n)
    n -= 1
```
**Actualiza siempre** el estado para evitar bucles infinitos.

## break y continue
```python
for x in range(10):
    if x == 5:
        break         # sale del bucle
    if x % 2 == 0:
        continue      # salta al siguiente
    print(x)
# imprime 1, 3
```

## else en bucles
Se ejecuta si el bucle **termina sin break**:
```python
for n in [2, 4, 6]:
    if n % 2 != 0:
        print("impar!")
        break
else:
    print("todos pares")
```

## Patrones
### Acumular
```python
total = 0
for x in [3, 1, 4]:
    total += x
```

### Buscar
```python
encontrado = False
for user in usuarios:
    if user.email == target:
        encontrado = True
        break
```

## Errores comunes
- **Bucle infinito**: olvidar `n -= 1` en `while`.
- **Modificar la lista mientras iteras**: crea copia con `lista[:]`.
- **Usar `range(len(lista))`** cuando `enumerate` o iterar directo es mas limpio.

## Resumen
- `for` recorre iterables; `while` repite mientras se cumpla una condicion.
- `enumerate`, `zip` y `range` cubren la mayoria de casos.
- `break`/`continue` controlan el flujo; el `else` de un bucle es util.
""",
    difficulty="beginner",
    category="control-flujo",
    order=7,
    estimated_duration=30,
    prerequisites_titles=["Condicionales y logica"],
    exercises=[
        ExerciseTemplate(
            title="Suma 1..n",
            description="for + range.",
            instructions="Calcula la suma de 1 a n (inclusive) usando un for.",
            starter_code="n = 10\n# TODO: calcula total\n",
        ),
        ExerciseTemplate(
            title="Tablas con zip",
            description="Combina dos listas.",
            instructions="Dadas `nombres` y `edades`, imprime 'Ana tiene 25 anos' para cada par.",
            starter_code="nombres = ['Ana', 'Luis']\nedades = [25, 30]\n# TODO\n",
        ),
        ExerciseTemplate(
            title="Contador regresivo",
            description="while con break.",
            instructions="Imprime de 10 a 1 usando while; si llegas a 5, rompe el bucle con break.",
            starter_code="# TODO\n",
        ),
    ],
)

L_LISTAS = LessonTemplate(
    title="Listas",
    description="Creacion, indexacion, metodos, slicing y list comprehensions.",
    content="""## Objetivo
Usar listas con fluidez: crear, modificar, recorrer y transformar.

## Creacion
```python
vacia = []
nums = [1, 2, 3, 4]
mixed = [1, "dos", 3.0, True]
ceros = [0] * 5        # [0, 0, 0, 0, 0]
from_range = list(range(5))  # [0, 1, 2, 3, 4]
```

## Acceso e indexacion
```python
nums[0]     # 1
nums[-1]    # 4
nums[1:3]   # [2, 3]
nums[::-1]  # invertida
```

## Mutacion
Las listas son **mutables**:
```python
nums[0] = 100          # cambia un elemento
nums.append(5)         # agrega al final
nums.insert(0, -1)     # inserta en posicion
nums.extend([6, 7])    # agrega varios
nums.remove(2)         # elimina la primera aparicion
del nums[0]            # elimina por indice
ultimo = nums.pop()    # elimina y retorna ultimo
nums.sort()            # ordena in-place
nums.reverse()         # invierte in-place
```

### Ordenar sin mutar
```python
ordenada = sorted(nums)
ordenada = sorted(nums, reverse=True, key=lambda x: abs(x))
```

## Busqueda y conteo
```python
nums.count(3)     # cuantas veces aparece el 3
nums.index(3)     # indice de la primera aparicion (ValueError si no esta)
3 in nums         # True/False
```

## Copiar correctamente
```python
a = [1, 2, 3]
b = a             # MISMA lista (alias)
c = a[:]          # copia
d = list(a)       # copia
import copy
e = copy.deepcopy(a)  # copia profunda (para listas anidadas)
```

## Comprehensions
Forma compacta de construir listas:
```python
cuadrados = [x * x for x in range(6)]
pares = [x for x in range(20) if x % 2 == 0]
matriz = [[i*j for j in range(3)] for i in range(3)]
```

## Desempaquetar
```python
a, b, c = [1, 2, 3]
primero, *resto = [1, 2, 3, 4]  # primero=1, resto=[2,3,4]
*inicio, ultimo = [1, 2, 3, 4]  # inicio=[1,2,3], ultimo=4
```

## Errores comunes
- **`[0] * 3` vs `[[]] * 3`**: el segundo comparte la misma lista interna.
  Usa `[[] for _ in range(3)]`.
- **Modificar mientras iteras**: comportamiento impredecible. Itera sobre copia.
- **Pasar `list` como default de funcion**: `def f(x=[])` comparte la lista entre llamadas.

## Resumen
- Listas son mutables, ordenadas e indexables.
- `append`, `extend`, `pop`, `sort` son los metodos mas usados.
- Las comprehensions son tu mejor amigo para transformar.
""",
    difficulty="beginner",
    category="estructuras-datos",
    order=8,
    estimated_duration=35,
    prerequisites_titles=["Bucles for y while"],
    exercises=[
        ExerciseTemplate(
            title="Filtrar pares",
            description="Comprehension con condicion.",
            instructions="Dada `nums`, crea `pares` con solo los numeros pares usando list comprehension.",
            starter_code="nums = [1, 2, 3, 4, 5, 6]\n# TODO\n",
        ),
        ExerciseTemplate(
            title="Top 3",
            description="Ordenar y recortar.",
            instructions="Dada `notas`, obten las 3 mas altas en una nueva lista sin mutar la original.",
            starter_code="notas = [4.5, 3.8, 5.0, 4.2, 2.5, 4.9]\n# TODO: top = ...\n",
        ),
    ],
)

L_TUPLAS_SETS = LessonTemplate(
    title="Tuplas y Conjuntos",
    description="Inmutabilidad, desempaquetado y operaciones de conjuntos.",
    content="""## Objetivo
Saber cuando usar tuplas (inmutables) y conjuntos (sin duplicados, rapidos).

## Tuplas
```python
punto = (3, 4)
una_sola = (5,)       # coma obligatoria para tupla de 1
sin_parens = 1, 2, 3  # tambien es tupla
x, y = punto          # desempaquetado
```

**Son inmutables**: `punto[0] = 9` falla. Por eso son:
- Mas baratas en memoria.
- Usables como clave de diccionario.
- Mas seguras para datos que no deben cambiar.

### Metodos
```python
t = (1, 2, 2, 3)
t.count(2)   # 2
t.index(3)   # 3
```

### Cuando usar tupla vs lista
- Tupla: coleccion **heterogenea fija** (coordenadas, registro, retorno multiple).
- Lista: coleccion **homogenea variable** (lista de usuarios, resultados).

## Namedtuple (extra)
```python
from collections import namedtuple
Punto = namedtuple("Punto", ["x", "y"])
p = Punto(3, 4)
p.x, p.y   # acceso por nombre
```

## Sets (conjuntos)
Coleccion **no ordenada** de elementos **unicos**:
```python
s = {1, 2, 3}
vacio = set()         # OJO: {} es dict vacio
s.add(4)
s.discard(2)          # no falla si no esta
s.remove(3)           # KeyError si no esta
s | {5, 6}            # union
s & {2, 3}            # interseccion
s - {1}               # diferencia
s ^ {2, 4}            # diferencia simetrica
3 in s                # busqueda O(1)
```

### Frozen set
```python
fs = frozenset([1, 2, 3])  # inmutable, hashable
```

### Caso de uso tipico
**Eliminar duplicados**:
```python
duplicados = [1, 2, 2, 3, 3, 3]
unicos = list(set(duplicados))  # orden no garantizado
```

**Busqueda rapida**:
```python
permitidos = {"free", "pro", "teams"}
if plan in permitidos:  # O(1) promedio
    ...
```

## Errores comunes
- **`{}` es dict, no set**: para set vacio usa `set()`.
- **Meter objetos mutables en set/dict**: listas no son hashables.
  Convierte a tupla primero.
- **Creer que set mantiene orden**: desde 3.7 dict preserva orden, pero set NO.

## Resumen
- Tupla: inmutable, heterogenea, hashable.
- Set: unico, sin orden, busqueda O(1).
- Usa set para deduplicar y busquedas rapidas.
""",
    difficulty="beginner",
    category="estructuras-datos",
    order=9,
    estimated_duration=25,
    prerequisites_titles=["Listas"],
    exercises=[
        ExerciseTemplate(
            title="Deduplicar preservando orden",
            description="Uso hibrido de set.",
            instructions="Dada `items`, devuelve una lista sin duplicados preservando el primer orden de aparicion.",
            starter_code="items = [3, 1, 2, 1, 3, 4, 2]\n# TODO: usa un set auxiliar\n",
            hints=["Recorre items y agrega solo si no esta en el set visto"],
        ),
        ExerciseTemplate(
            title="Interseccion de tags",
            description="Operaciones de set.",
            instructions="Dados dos sets `a` y `b`, calcula los tags comunes y los exclusivos de cada uno.",
            starter_code="a = {'python','web','api'}\nb = {'python','data','api'}\n# TODO\n",
        ),
    ],
)

L_DICTS = LessonTemplate(
    title="Diccionarios",
    description="Clave-valor, iteracion, get con default y dict comprehensions.",
    content="""## Objetivo
Modelar datos por clave-valor, la estructura mas usada de Python.

## Creacion
```python
vacio = {}
usuario = {"id": 1, "nombre": "Ana", "email": "ana@x.com"}
por_pares = dict([("a", 1), ("b", 2)])
por_kwargs = dict(a=1, b=2)
```

## Acceso
```python
usuario["nombre"]       # 'Ana'
usuario["ciudad"]       # KeyError
usuario.get("ciudad")   # None (seguro)
usuario.get("ciudad", "desconocida")  # default
```

## Mutacion
```python
usuario["activo"] = True        # agrega o actualiza
del usuario["email"]            # elimina
usuario.pop("email", None)      # elimina seguro
usuario.update({"plan": "pro", "edad": 30})
```

## Iteracion
```python
for clave in usuario:             # claves
    print(clave)
for valor in usuario.values():    # valores
    print(valor)
for k, v in usuario.items():      # pares
    print(k, v)
```

### Preserva orden de insercion
Desde Python 3.7 los dicts **mantienen el orden de insercion**.

## Dict comprehensions
```python
cuadrados = {x: x*x for x in range(5)}
invertido = {v: k for k, v in usuario.items()}
filtrado = {k: v for k, v in usuario.items() if v}
```

## Patrones utiles

### Contar frecuencias
```python
texto = "mississippi"
conteo = {}
for c in texto:
    conteo[c] = conteo.get(c, 0) + 1
# {'m':1, 'i':4, 's':4, 'p':2}
```

O con Counter (`collections`):
```python
from collections import Counter
conteo = Counter(texto)
```

### Agrupar por clave
```python
from collections import defaultdict
por_categoria = defaultdict(list)
for producto in productos:
    por_categoria[producto["cat"]].append(producto)
```

### Fusionar dicts (3.9+)
```python
base = {"a": 1, "b": 2}
extra = {"b": 20, "c": 3}
combinado = base | extra     # {'a':1,'b':20,'c':3}
base |= extra                # muta base
```

## Errores comunes
- **Acceder a clave inexistente con `[ ]`**: lanza `KeyError`. Usa `.get()` o `in`.
- **Usar listas como clave**: no son hashables; usa tuplas.
- **Creer que `.keys()` es set**: es una **view**. Para operar como set: `set(d.keys())` o `d.keys() & otras_claves`.

## Resumen
- Accede seguro con `.get(clave, default)`.
- Itera con `.items()` cuando necesitas ambos.
- `defaultdict` y `Counter` resuelven problemas comunes sin boilerplate.
""",
    difficulty="beginner",
    category="estructuras-datos",
    order=10,
    estimated_duration=30,
    prerequisites_titles=["Tuplas y Conjuntos"],
    exercises=[
        ExerciseTemplate(
            title="Frecuencia de palabras",
            description="Count manual con dict.",
            instructions="Cuenta cuantas veces aparece cada palabra en `frase` separada por espacios. Guarda el resultado en `freq`.",
            starter_code="frase = 'uno dos uno tres dos uno'\n# TODO: freq = ...\n",
        ),
        ExerciseTemplate(
            title="Invertir mapping",
            description="Dict comprehension.",
            instructions="Dado `mapa` clave->valor con valores unicos, crea `inverso` valor->clave.",
            starter_code="mapa = {'a': 1, 'b': 2, 'c': 3}\n# TODO\n",
        ),
    ],
)


# ---------------------------------------------------------------------------
# Ruta INTERMEDIO
# ---------------------------------------------------------------------------

L_FUNCIONES = LessonTemplate(
    title="Funciones",
    description="def, return, parametros, defaults, *args y **kwargs.",
    content="""## Objetivo
Escribir funciones reutilizables, claras y correctamente parametrizadas.

## Anatomia
```python
def nombre(parametros) -> tipo_retorno:
    '''Docstring opcional.'''
    # cuerpo
    return valor
```

### Ejemplo
```python
def area_circulo(radio: float) -> float:
    '''Calcula el area de un circulo.'''
    import math
    return math.pi * radio ** 2
```

## Parametros

### Posicionales y por nombre
```python
def saludar(nombre, saludo):
    print(saludo, nombre)

saludar("Ana", "Hola")             # posicional
saludar(nombre="Ana", saludo="Hi") # por nombre
saludar("Ana", saludo="Hi")        # mixto: posicionales primero
```

### Valores por defecto
```python
def saludar(nombre, saludo="Hola"):
    print(saludo, nombre)

saludar("Ana")           # Hola Ana
saludar("Ana", "Hi")     # Hi Ana
```
**Cuidado**: el default se evalua **una sola vez** al definir la funcion.
Nunca uses mutables como default:
```python
def malo(x, lista=[]):   # lista es compartida entre llamadas!
    lista.append(x)
    return lista

def bueno(x, lista=None):
    if lista is None:
        lista = []
    lista.append(x)
    return lista
```

### *args y **kwargs
```python
def total(*args):
    return sum(args)

total(1, 2, 3)    # 6

def config(**kwargs):
    for k, v in kwargs.items():
        print(k, "=", v)

config(host="local", port=8000)
```

### Orden de parametros
```python
def f(pos1, pos2, /, normal, *, solo_por_nombre):
    ...
```
- Todo antes de `/` es **solo posicional**.
- Todo despues de `*` es **solo por nombre**.

## return
```python
def dividir(a, b):
    if b == 0:
        return None         # o lanza excepcion
    return a / b
```
Una funcion sin `return` explicito devuelve `None`.

### Multiples valores
```python
def min_max(xs):
    return min(xs), max(xs)     # devuelve tupla

lo, hi = min_max([3, 1, 5, 2])
```

## Ambito (scope)
```python
x = 10  # global

def f():
    x = 5           # local, no afecta al global
    print(x)        # 5

f()
print(x)            # 10
```

Para modificar el global:
```python
def set_x():
    global x
    x = 99
```
Pero es mejor **no usar `global`** y pasar/retornar valores.

## Type hints
Son opcionales pero muy utiles:
```python
def total(items: list[int]) -> int:
    return sum(items)
```
No se chequean en runtime; usa `mypy` para verificar.

## Errores comunes
- **Default mutable** (ya mencionado).
- **Olvidar `return`**: la funcion devuelve `None`.
- **Nombres que pisan built-ins**: `list = [1,2]` rompe el tipo `list`.

## Resumen
- `def` crea funciones; `return` devuelve (una tupla si son varios valores).
- Usa defaults inmutables y `*args`/`**kwargs` para flexibilidad.
- Escribe docstrings y type hints cuando el codigo sea publico.
""",
    difficulty="intermediate",
    category="funciones",
    order=11,
    estimated_duration=40,
    prerequisites_titles=["Diccionarios"],
    exercises=[
        ExerciseTemplate(
            title="Area de rectangulo",
            description="Funcion con retorno.",
            instructions="Implementa `area_rectangulo(base, altura) -> float`.",
            starter_code="def area_rectangulo(base: float, altura: float) -> float:\n    # TODO\n    pass\n",
        ),
        ExerciseTemplate(
            title="Saludo configurable",
            description="Parametro con default.",
            instructions="Implementa `saludar(nombre, prefijo='Hola') -> str` que devuelva el saludo.",
            starter_code="def saludar(nombre: str, prefijo: str = 'Hola') -> str:\n    # TODO\n    pass\n",
        ),
        ExerciseTemplate(
            title="Suma variable",
            description="Usa *args.",
            instructions="Implementa `suma(*nums)` que acepte cualquier cantidad de numeros y los sume.",
            starter_code="def suma(*nums):\n    # TODO\n    pass\n",
            difficulty="medium",
            points=15,
        ),
    ],
)

L_LAMBDAS = LessonTemplate(
    title="Lambdas y programacion funcional",
    description="Funciones anonimas, map, filter, sorted con key y reduce.",
    content="""## Objetivo
Tratar funciones como valores de primera clase y usar herramientas funcionales.

## Lambda (funcion anonima)
```python
square = lambda x: x ** 2
square(5)   # 25

sumar = lambda a, b: a + b
sumar(3, 4) # 7
```
Solo admiten **una expresion**. Si necesitas mas, usa `def`.

## Funciones como valores
```python
def aplicar(fn, x):
    return fn(x)

aplicar(lambda n: n * 10, 3)   # 30
aplicar(str.upper, "hola")     # 'HOLA'
```

## map
Transforma cada elemento:
```python
nums = [1, 2, 3]
list(map(lambda x: x * 2, nums))   # [2, 4, 6]

# Con varias secuencias
list(map(lambda a, b: a + b, [1,2,3], [10,20,30]))  # [11, 22, 33]
```

**Alternativa idiomatica**: list comprehension.
```python
[x * 2 for x in nums]
```

## filter
Mantiene elementos donde la funcion devuelve truthy:
```python
list(filter(lambda x: x > 2, [1, 2, 3, 4]))   # [3, 4]
```
Equivalente:
```python
[x for x in [1,2,3,4] if x > 2]
```

## sorted con key
```python
personas = [{"nombre": "Ana", "edad": 30}, {"nombre": "Luis", "edad": 25}]
sorted(personas, key=lambda p: p["edad"])
# ordenados por edad

sorted(["banana", "apple", "cherry"], key=len)
# por longitud

sorted(nums, key=abs)  # por valor absoluto

# Multi-criterio: tupla
sorted(personas, key=lambda p: (p["edad"], p["nombre"]))
```

## reduce
Combina elementos con un acumulador:
```python
from functools import reduce
reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)   # 10 (como sum)
reduce(lambda acc, x: acc * x, [1, 2, 3, 4], 1)   # 24 (factorial)
```
Usa `reduce` solo cuando `sum`/`min`/`max`/comprehensions no alcancen.

## functools utiles
```python
from functools import partial, reduce, lru_cache

# partial: fija argumentos
doblar = partial(map, lambda x: x * 2)
list(doblar([1,2,3]))  # [2, 4, 6]

# lru_cache: memoiza
@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
```

## Cuando NO usar lambda
- Si la logica no cabe en una expresion, usa `def`.
- Para nombres descriptivos (debugging/tracebacks), `def` gana.
- En sorted `key=str.lower` es mas claro que `lambda s: s.lower()`.

## Errores comunes
- **Asignar lambda a variable con nombre descriptivo**: mejor `def`.
- **Capturar variable de bucle en lambda**: hay que fijar con `default` param:
  ```python
  fns = [lambda x, i=i: x + i for i in range(3)]
  ```

## Resumen
- Lambdas son funciones de una expresion.
- `map`/`filter` existen, pero las comprehensions son mas idiomatic.
- `sorted(key=...)` cubre la mayoria de ordenamientos.
""",
    difficulty="intermediate",
    category="funciones",
    order=12,
    estimated_duration=30,
    prerequisites_titles=["Funciones"],
    exercises=[
        ExerciseTemplate(
            title="Ordenar por campo",
            description="sorted con key.",
            instructions="Dada `productos` (lista de dicts con 'nombre' y 'precio'), retorna lista ordenada por precio ascendente.",
            starter_code="productos = [{'nombre':'a','precio':10},{'nombre':'b','precio':3}]\n# TODO\n",
        ),
        ExerciseTemplate(
            title="Map + filter en cascada",
            description="Comprehension o funcional.",
            instructions="Dada `nums`, obten los cuadrados de los numeros pares.",
            starter_code="nums = [1,2,3,4,5,6]\n# TODO\n",
        ),
    ],
)

L_COMPREHENSIONS = LessonTemplate(
    title="Comprehensions (list, dict, set, gen)",
    description="Sintaxis compacta para transformar y filtrar iterables.",
    content="""## Objetivo
Dominar las cuatro formas de comprehension y cuando usar cada una.

## List comprehension
```python
[expr for x in iterable if cond]
```
```python
cuadrados = [x*x for x in range(6)]
pares = [x for x in range(20) if x % 2 == 0]
palabras_mayusculas = [w.upper() for w in ["a","b","c"]]

# Anidadas: aplanar matriz
matriz = [[1,2],[3,4],[5,6]]
plano = [x for fila in matriz for x in fila]   # [1,2,3,4,5,6]

# Condicional ternario dentro
etiquetas = ["par" if x % 2 == 0 else "impar" for x in range(5)]
```

## Dict comprehension
```python
{k: v for k, v in pares}
```
```python
cuadrados = {x: x*x for x in range(5)}
invertido = {v: k for k, v in d.items()}
filtrado = {k: v for k, v in d.items() if v > 0}
```

## Set comprehension
```python
{expr for x in iterable}
```
```python
vocales = {c for c in "murcielago" if c in "aeiou"}  # {'u','i','e','a','o'}
```

## Generator expression
Como list comprehension pero **perezoso** (no construye la lista en memoria):
```python
suma = sum(x*x for x in range(10**6))   # eficiente
cualquiera = any(x > 100 for x in datos) # para temprano
```
Nota los **parentesis** en vez de corchetes.

### Cuando usar generator
- Datos grandes donde no quieres construir la lista completa.
- Cuando solo iteras una vez.
- Con funciones que aceptan iterables (`sum`, `any`, `all`, `max`, `min`).

## Cuando NO usar comprehension
- Logica con 3+ clausulas anidadas: se vuelve ilegible. Usa for clasico.
- Efectos secundarios (print, escribir a DB): expresa intent con `for`.
- Acumuladores complejos: un bucle explicito es mas claro.

## Errores comunes
- **Olvidar el parentesis en generator**: `sum[x for x in r]` es TypeError.
- **Sobre-anidar**: `[x for a in m for b in a for x in b]` es dificil de mantener.
- **Usar comprehension para side effects**: `[print(x) for x in xs]` construye una lista de None sin sentido.

## Resumen
- `[...]` list, `{...}` dict/set, `(...)` generator.
- Prefiere comprehension sobre `map`/`filter` para codigo mas legible.
- Cambia a `for` clasico si crece la complejidad.
""",
    difficulty="intermediate",
    category="python-moderno",
    order=13,
    estimated_duration=25,
    prerequisites_titles=["Lambdas y programacion funcional"],
    exercises=[
        ExerciseTemplate(
            title="Cuadrados de pares",
            description="List comprehension con filtro.",
            instructions="Con numeros 1..20, construye una lista con los cuadrados de los pares.",
            starter_code="# TODO\n",
        ),
        ExerciseTemplate(
            title="Dict comprehension",
            description="De lista a dict.",
            instructions="Dada `palabras`, crea un dict `largos` palabra -> longitud.",
            starter_code="palabras = ['hola','mundo','python']\n# TODO\n",
        ),
    ],
)

L_EXCEPCIONES = LessonTemplate(
    title="Manejo de excepciones",
    description="try/except/else/finally, raise y excepciones personalizadas.",
    content="""## Objetivo
Escribir codigo robusto que controle errores esperables sin esconder bugs.

## Anatomia
```python
try:
    bloque_riesgoso()
except TipoError as e:
    # reacciona
    ...
except (OtroError, OtroMas) as e:
    ...
else:
    # solo si NO hubo excepcion
    ...
finally:
    # SIEMPRE se ejecuta (limpieza)
    ...
```

## Ejemplos
```python
try:
    n = int(input("Numero: "))
except ValueError:
    print("No era un numero valido")

try:
    f = open("datos.txt")
    data = f.read()
except FileNotFoundError:
    data = ""
finally:
    f.close() if 'f' in dir() else None
# Mejor: usar `with` (context manager)
```

## Jerarquia de excepciones
Todas heredan de `BaseException` -> `Exception`:
- `ArithmeticError` -> `ZeroDivisionError`
- `LookupError` -> `KeyError`, `IndexError`
- `ValueError`, `TypeError`, `AttributeError`
- `OSError` -> `FileNotFoundError`, `PermissionError`
- `RuntimeError` -> `RecursionError`

Captura **especifica**; evita `except Exception` (o peor, `except:`) porque
oculta bugs.

## raise
Lanza excepciones explicitamente:
```python
def retirar(saldo, monto):
    if monto > saldo:
        raise ValueError(f"Monto {monto} supera saldo {saldo}")
    return saldo - monto
```

### Re-lanzar
```python
try:
    ...
except ValueError:
    log.warning("fallo")
    raise   # vuelve a propagarla
```

### Encadenar
```python
try:
    parse(data)
except ParseError as e:
    raise RuntimeError("no pude procesar") from e
```

## Excepciones personalizadas
```python
class SaldoInsuficiente(Exception):
    '''Se lanza cuando una operacion supera el saldo.'''

def retirar(saldo, monto):
    if monto > saldo:
        raise SaldoInsuficiente(f"falta {monto - saldo}")
```

## Patron EAFP vs LBYL
- **LBYL** (Look Before You Leap): chequear antes.
  ```python
  if "clave" in d:
      valor = d["clave"]
  ```
- **EAFP** (Easier to Ask Forgiveness than Permission): intenta y captura.
  ```python
  try:
      valor = d["clave"]
  except KeyError:
      valor = None
  ```
Python prefiere EAFP cuando el caso "normal" casi siempre tiene exito.

## Errores comunes
- **`except:` pelado o `except Exception:`** captura demasiado (incluido SystemExit si usas BaseException). Se tan especifico como puedas.
- **Swallow de excepciones**: capturar y no hacer nada oculta bugs. Registra y re-lanza si no sabes como manejarlo.
- **`finally` con `return`**: el `return` de finally pisa el de try/except.

## Resumen
- Captura tipos concretos.
- Usa `finally` o `with` para limpieza garantizada.
- Excepciones propias dan semantica a errores de dominio.
""",
    difficulty="intermediate",
    category="python-moderno",
    order=14,
    estimated_duration=30,
    prerequisites_titles=["Comprehensions (list, dict, set, gen)"],
    exercises=[
        ExerciseTemplate(
            title="Division segura",
            description="Captura ZeroDivisionError.",
            instructions="Implementa `division_segura(a, b)` que devuelva None si b == 0 y a/b en otro caso.",
            starter_code="def division_segura(a: float, b: float):\n    # TODO\n    pass\n",
        ),
        ExerciseTemplate(
            title="Excepcion propia",
            description="raise custom exception.",
            instructions="Define `SaldoInsuficiente(Exception)` y una funcion `retirar(saldo, monto)` que la lance si monto > saldo.",
            starter_code="# TODO\n",
            difficulty="medium",
            points=15,
        ),
    ],
)

L_ARCHIVOS = LessonTemplate(
    title="Archivos y context managers",
    description="open, with, modos r/w/a y uso de context managers.",
    content="""## Objetivo
Leer y escribir archivos de forma segura usando context managers.

## open()
```python
f = open("datos.txt", "r", encoding="utf-8")
texto = f.read()
f.close()
```
**Problema**: si algo falla antes de `close()`, el archivo queda abierto.

## `with` (context manager)
Garantiza cierre incluso con excepciones:
```python
with open("datos.txt", encoding="utf-8") as f:
    texto = f.read()
# al salir del with, se hace f.close() automaticamente
```

### Varios archivos
```python
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read())
```

## Modos
| Modo | Significado |
|---|---|
| `r` | lectura (default) |
| `w` | escritura, **borra contenido** previo |
| `a` | append (agregar al final) |
| `x` | crear; falla si existe |
| `b` | binario (ej. `rb`, `wb`) |
| `+` | lectura y escritura (`r+`, `w+`) |

## Lectura linea a linea
```python
with open("log.txt") as f:
    for linea in f:
        procesar(linea.rstrip())  # quita \\n
```
**No uses** `f.readlines()` si el archivo es enorme: carga todo en memoria.

## Escritura
```python
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("linea 1\\n")
    f.writelines(["l2\\n", "l3\\n"])
```

## JSON y CSV
```python
import json
with open("data.json") as f:
    data = json.load(f)

with open("out.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

import csv
with open("items.csv", newline="") as f:
    for fila in csv.DictReader(f):
        print(fila)
```

## pathlib
Forma moderna de manejar rutas:
```python
from pathlib import Path

p = Path("datos") / "archivo.txt"
p.exists()
p.read_text(encoding="utf-8")
p.write_text("nuevo contenido", encoding="utf-8")
for f in Path("logs").glob("*.log"):
    print(f.name)
```

## Crear tu propio context manager
```python
from contextlib import contextmanager

@contextmanager
def cronometro(nombre):
    import time
    t0 = time.perf_counter()
    yield
    print(f"{nombre}: {time.perf_counter() - t0:.3f}s")

with cronometro("procesar"):
    procesar_todo()
```

## Errores comunes
- **Olvidar encoding** en Windows: usa siempre `encoding="utf-8"`.
- **Abrir sin `with`**: fugas de recursos si algo falla.
- **`readlines()`** con archivos gigantes: usa el iterador del archivo.

## Resumen
- Usa siempre `with open(...)` para garantizar cierre.
- Itera linea a linea en archivos grandes.
- `pathlib` es mas comodo que `os.path` para rutas.
""",
    difficulty="intermediate",
    category="io-sistema",
    order=15,
    estimated_duration=30,
    prerequisites_titles=["Manejo de excepciones"],
    exercises=[
        ExerciseTemplate(
            title="Copia de archivo",
            description="Lectura + escritura.",
            instructions="Lee `entrada.txt` y escribe su contenido en mayusculas a `salida.txt`. Usa with.",
            starter_code="# TODO: simula con io.StringIO si no quieres crear archivos reales\n",
            hints=["Puedes probar con io.StringIO si no tienes permisos de archivo"],
        ),
        ExerciseTemplate(
            title="Contar lineas no vacias",
            description="Iterar sobre un archivo.",
            instructions=(
                "Implementa `contar_lineas(texto: str) -> int` que reciba el contenido ya leido de un archivo "
                "y devuelva cuantas lineas NO estan vacias (ignorando espacios en blanco). "
                "Prueba con 'hola\\n\\n  \\nmundo\\n' -> 2."
            ),
            starter_code="def contar_lineas(texto: str) -> int:\n    # TODO\n    pass\n",
            hints=[
                "str.splitlines() te da una lista sin los saltos de linea",
                "Usa strip() para detectar lineas 'vacias' con solo espacios",
            ],
            difficulty="medium",
            points=15,
        ),
        ExerciseTemplate(
            title="Filtrar JSON de usuarios",
            description="Lee JSON, filtra y serializa.",
            instructions=(
                "Implementa `activos(entrada_json: str) -> str`. Recibe un JSON con forma "
                "`[{\"id\": 1, \"nombre\": \"Ana\", \"activo\": true}, ...]` y devuelve un JSON "
                "(string) solo con los usuarios cuyo campo `activo` es True, manteniendo la misma forma. "
                "Usa `json.loads` y `json.dumps(..., ensure_ascii=False)`."
            ),
            starter_code="import json\n\ndef activos(entrada_json: str) -> str:\n    # TODO\n    pass\n",
            hints=[
                "Filtra con una list comprehension",
                "Pasa ensure_ascii=False para no escapar acentos",
            ],
            difficulty="hard",
            points=20,
        ),
    ],
)

L_MODULOS = LessonTemplate(
    title="Modulos, paquetes y entornos virtuales",
    description="import, from, __init__.py, pip y venv.",
    content="""## Objetivo
Organizar codigo en archivos reutilizables y gestionar dependencias.

## Modulos
Un archivo `.py` es un modulo. Se importa por su nombre (sin `.py`):

```python
# utils.py
def saludar(n): return f"Hola {n}"

# main.py
import utils
print(utils.saludar("Ana"))

from utils import saludar
print(saludar("Ana"))

from utils import saludar as sal
print(sal("Ana"))
```

## Paquetes
Una carpeta con `__init__.py` es un paquete:

```
proyecto/
    main.py
    mipaquete/
        __init__.py
        motor.py
        utils.py
```

```python
from mipaquete.motor import arrancar
from mipaquete import utils
```

## `__name__ == "__main__"`
Codigo que solo corre cuando ejecutas el archivo directamente (no al importarlo):
```python
def core():
    ...

if __name__ == "__main__":
    core()
```

## Imports absolutos vs relativos
- **Absoluto** (preferido): `from mipaquete.utils import x`.
- **Relativo**: `from .utils import x` (solo dentro de paquetes).

## pip y requirements
```
pip install requests
pip install "fastapi==0.104.1"
pip install -r requirements.txt
pip freeze > requirements.txt
```

## Entornos virtuales
Aislan dependencias por proyecto:
```
python -m venv .venv

# activar (Windows)
.venv\\Scripts\\activate
# activar (Linux/Mac)
source .venv/bin/activate

pip install ...
deactivate
```

Alternativas modernas: **poetry**, **uv**, **pipenv**.

## sys.path y PYTHONPATH
Cuando Python busca un modulo, revisa:
1. Directorio del script actual.
2. `PYTHONPATH` (variable de entorno).
3. Directorios instalados (site-packages).

Puedes inspeccionar con `import sys; print(sys.path)`.

## Estructura tipica de proyecto
```
miproyecto/
    pyproject.toml       # configuracion
    requirements.txt
    README.md
    src/
        miproyecto/
            __init__.py
            core.py
            cli.py
    tests/
        test_core.py
```

## Errores comunes
- **`ImportError`**: el modulo no esta en el path. Revisa `sys.path`.
- **`circular import`**: A importa B, B importa A. Refactoriza a un tercer modulo.
- **Instalar fuera del venv**: contaminas el Python global.

## Resumen
- Un archivo = modulo; carpeta con `__init__.py` = paquete.
- Usa `if __name__ == "__main__":` para scripts ejecutables.
- Crea venv por proyecto y congela dependencias.
""",
    difficulty="intermediate",
    category="tooling",
    order=16,
    estimated_duration=30,
    prerequisites_titles=["Archivos y context managers"],
    exercises=[
        ExerciseTemplate(
            title="Refactor a modulo",
            description="Separa funciones.",
            instructions="Mueve `sumar`, `restar` y `multiplicar` a `operaciones.py`. En `main.py`, importalos y usa con 2 y 3.",
            starter_code="# main.py\n# TODO\n",
            difficulty="medium",
        ),
        ExerciseTemplate(
            title="Guardian __main__",
            description="Evita ejecutar al importar.",
            instructions=(
                "Un modulo `reporte.py` define `generar_reporte()` y ademas lo llama en el tope del archivo. "
                "Refactoriza para que la funcion solo se ejecute cuando el archivo se corra directamente, "
                "NO cuando se importe desde otro modulo. Usa el patron idiomatico de `__name__`."
            ),
            starter_code=(
                "# reporte.py\n"
                "def generar_reporte():\n"
                "    print('Generando reporte...')\n\n"
                "generar_reporte()  # TODO: proteger con __name__ == '__main__'\n"
            ),
            hints=[
                "`if __name__ == '__main__': ...`",
                "Al importar, __name__ toma el nombre del modulo; al ejecutar, vale '__main__'",
            ],
            difficulty="medium",
            points=15,
        ),
        ExerciseTemplate(
            title="Diseno de paquete",
            description="Estructura de carpetas.",
            instructions=(
                "Tienes `geometria.py` con funciones `area_circulo`, `area_cuadrado`, `perimetro_circulo` "
                "y `perimetro_cuadrado`. Disena una estructura de paquete `geometria/` que separe por responsabilidad "
                "(`areas.py`, `perimetros.py`) y exponga todo desde `__init__.py`. "
                "Escribe el contenido de los tres archivos como strings en una lista `estructura`, cada entrada "
                "con formato `('ruta/al/archivo.py', '<contenido>')`. Al final `print(len(estructura))` debe dar 3."
            ),
            starter_code=(
                "estructura = [\n"
                "    # ('geometria/__init__.py', '...'),\n"
                "    # ('geometria/areas.py', '...'),\n"
                "    # ('geometria/perimetros.py', '...'),\n"
                "]\n"
                "# TODO\n"
            ),
            hints=[
                "`__init__.py` puede reexportar: `from .areas import area_circulo, area_cuadrado`",
                "Asi el usuario escribe `from geometria import area_circulo` sin saber la estructura interna",
            ],
            difficulty="hard",
            points=25,
        ),
    ],
)


# ---------------------------------------------------------------------------
# Ruta AVANZADO
# ---------------------------------------------------------------------------

L_POO = LessonTemplate(
    title="POO: clases, objetos y encapsulacion",
    description="Clases, self, __init__, atributos, metodos y visibilidad.",
    content="""## Objetivo
Modelar entidades con clases, atributos y comportamiento.

## Anatomia de una clase
```python
class Producto:
    '''Representa un articulo en inventario.'''

    iva = 0.19          # atributo de clase (compartido)

    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre      # atributo de instancia
        self.precio = precio

    def precio_con_iva(self) -> float:
        return self.precio * (1 + self.iva)

    def aplicar_descuento(self, porcentaje: float) -> None:
        self.precio *= (1 - porcentaje / 100)

p = Producto("Cafe", 3.50)
p.precio_con_iva()        # 4.165
p.aplicar_descuento(10)   # muta p.precio
```

## self
Es la referencia a la **instancia actual**. Python la pasa automaticamente
como primer argumento.

## Atributos de clase vs de instancia
```python
class Contador:
    total = 0    # clase

    def __init__(self):
        self.valor = 0  # instancia

    def inc(self):
        self.valor += 1
        Contador.total += 1

a = Contador()
b = Contador()
a.inc(); a.inc(); b.inc()
a.valor, b.valor, Contador.total   # 2, 1, 3
```

## Visibilidad
Python no tiene modificadores estrictos:
- `nombre` publico.
- `_nombre` convencion "interno" (no tocar de fuera).
- `__nombre` name mangling (se renombra a `_Clase__nombre`).

```python
class Cuenta:
    def __init__(self):
        self._saldo = 0      # "privado" por convencion
        self.__pin = "1234"  # name-mangled
```

## Propiedades
Expone un atributo con logica getter/setter:
```python
class Temperatura:
    def __init__(self, c: float):
        self._c = c

    @property
    def celsius(self) -> float:
        return self._c

    @celsius.setter
    def celsius(self, valor: float) -> None:
        if valor < -273.15:
            raise ValueError("temperatura imposible")
        self._c = valor

    @property
    def fahrenheit(self) -> float:
        return self._c * 9/5 + 32

t = Temperatura(25)
t.celsius       # 25 (sin parentesis)
t.fahrenheit    # 77.0
t.celsius = -300  # ValueError
```

## Metodos de clase y estaticos
```python
class Fecha:
    def __init__(self, anio: int):
        self.anio = anio

    @classmethod
    def desde_string(cls, s: str) -> "Fecha":
        return cls(int(s.split("-")[0]))

    @staticmethod
    def es_bisiesto(anio: int) -> bool:
        return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)
```

## dataclasses (alternativa moderna)
Reducen boilerplate:
```python
from dataclasses import dataclass

@dataclass
class Producto:
    nombre: str
    precio: float
    iva: float = 0.19

    def precio_con_iva(self) -> float:
        return self.precio * (1 + self.iva)
```

## Errores comunes
- **Olvidar `self`** en metodos: `def f(): ...` sin `self` falla al llamar.
- **Atributo de clase mutable** (`lista = []`) compartido entre instancias.
  Ponlo en `__init__`.
- **`self.__x` y luego acceder como `obj.__x`**: name mangling lo renombra.

## Resumen
- `__init__` inicializa instancias; `self` es la instancia.
- Convenciones: `_` interno, `__` name mangling.
- `@property`, `@classmethod`, `@staticmethod` cubren patrones comunes.
- `dataclass` quita boilerplate.
""",
    difficulty="advanced",
    category="oop",
    order=17,
    estimated_duration=40,
    prerequisites_titles=["Modulos, paquetes y entornos virtuales"],
    exercises=[
        ExerciseTemplate(
            title="Clase Producto",
            description="Modela entidad simple.",
            instructions="Crea clase `Producto` con nombre y precio, metodo `aplicar_descuento(pct)` y propiedad `precio_con_iva`.",
            starter_code="class Producto:\n    def __init__(self, nombre: str, precio: float):\n        self.nombre = nombre\n        self.precio = precio\n\n    # TODO\n",
            difficulty="medium",
            points=15,
        ),
        ExerciseTemplate(
            title="Cuenta bancaria",
            description="Validacion y estado.",
            instructions="Implementa `Cuenta` con `depositar(monto)` y `retirar(monto)`, lanzando ValueError si el monto es negativo o excede saldo.",
            starter_code="class Cuenta:\n    def __init__(self):\n        self.saldo = 0\n\n    # TODO\n",
            difficulty="medium",
            points=15,
        ),
    ],
)

L_HERENCIA = LessonTemplate(
    title="Herencia, polimorfismo y dunder methods",
    description="super(), MRO, dunder methods (__str__, __eq__, __len__...).",
    content="""## Objetivo
Extender clases y definir comportamiento idiomatic con metodos especiales.

## Herencia simple
```python
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre

    def hablar(self) -> str:
        return "..."

class Perro(Animal):
    def hablar(self) -> str:
        return "Guau"

class Gato(Animal):
    def hablar(self) -> str:
        return "Miau"

for a in [Perro("Rex"), Gato("Mia")]:
    print(a.nombre, a.hablar())
```

## super()
Llama al metodo de la clase padre:
```python
class Cuenta:
    def __init__(self, saldo):
        self.saldo = saldo

class CuentaPremium(Cuenta):
    def __init__(self, saldo, cashback):
        super().__init__(saldo)
        self.cashback = cashback
```

## Herencia multiple y MRO
Python resuelve la herencia multiple con **MRO** (Method Resolution Order) C3:
```python
class A: ...
class B(A): ...
class C(A): ...
class D(B, C): ...

print(D.__mro__)
# (D, B, C, A, object)
```

`super()` sigue el MRO, lo que permite **cooperative multiple inheritance**.

## isinstance y issubclass
```python
isinstance(perro, Animal)   # True
issubclass(Perro, Animal)   # True
```

## Dunder methods (metodos magicos)
Dan a tus objetos comportamiento idiomatic:

### Representacion
```python
class Punto:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self) -> str:
        return f"Punto(x={self.x}, y={self.y})"   # para devs (debug)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"            # para usuarios
```

### Igualdad y hashing
```python
def __eq__(self, otro):
    if not isinstance(otro, Punto):
        return NotImplemented
    return self.x == otro.x and self.y == otro.y

def __hash__(self):
    return hash((self.x, self.y))   # requerido si lo usas en sets/dict
```

### Comparacion
```python
def __lt__(self, otro):
    return (self.x, self.y) < (otro.x, otro.y)
```
Con `functools.total_ordering` defines solo `__eq__` y `__lt__`.

### Contenedor
```python
class Bolsa:
    def __init__(self):
        self.items = []

    def __len__(self):      # len(bolsa)
        return len(self.items)

    def __contains__(self, x):  # x in bolsa
        return x in self.items

    def __getitem__(self, i):   # bolsa[i], iteracion
        return self.items[i]
```

### Aritmetica
```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, otro):
        return Vector(self.x + otro.x, self.y + otro.y)

    def __mul__(self, escalar):
        return Vector(self.x * escalar, self.y * escalar)
```

## Composicion vs herencia
Prefiere composicion: un `Coche` **tiene un** `Motor`, no **es un** `Motor`.
Usa herencia solo cuando realmente sea un **es-un** con comportamiento compartido.

## Errores comunes
- **Olvidar `super().__init__()`** en subclase: atributos del padre no se inicializan.
- **`__eq__` sin `__hash__`**: el objeto deja de ser hashable.
- **Herencia multiple para mezclar**: considera composicion o mixins pequenos.

## Resumen
- `super()` respeta el MRO.
- Los dunder methods integran tus clases con `len()`, `==`, `in`, `+`, etc.
- Prefiere composicion cuando no hay un "es-un" claro.
""",
    difficulty="advanced",
    category="oop",
    order=18,
    estimated_duration=45,
    prerequisites_titles=["POO: clases, objetos y encapsulacion"],
    exercises=[
        ExerciseTemplate(
            title="Vector con suma",
            description="Dunder methods aritmeticos.",
            instructions="Implementa `Vector(x, y)` con `__add__` y `__repr__` para que `Vector(1,2) + Vector(3,4)` sea `Vector(4, 6)`.",
            starter_code="class Vector:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\n    # TODO: __add__ y __repr__\n",
            difficulty="medium",
            points=15,
        ),
        ExerciseTemplate(
            title="Jerarquia Animal polimorfica",
            description="Herencia + sobreescritura.",
            instructions=(
                "Define `Animal` con `__init__(nombre)` y un metodo `hablar()` que devuelva '...'. "
                "Crea `Perro`, `Gato` y `Vaca` que hereden de Animal y sobreescriban `hablar()` "
                "para devolver 'Guau', 'Miau' y 'Muuu' respectivamente. "
                "Implementa tambien `presentar(animales)` que recibe una lista y devuelve una lista de strings "
                "tipo 'Rex dice Guau'. Deberia funcionar con `presentar([Perro('Rex'), Gato('Mia')])`."
            ),
            starter_code=(
                "class Animal:\n"
                "    def __init__(self, nombre):\n"
                "        self.nombre = nombre\n\n"
                "    def hablar(self) -> str:\n"
                "        return '...'\n\n"
                "# TODO: Perro, Gato, Vaca y presentar\n"
            ),
            hints=[
                "No necesitas repetir `__init__` en las subclases si no agregas atributos",
                "`presentar` itera y usa f-strings",
            ],
            difficulty="medium",
            points=15,
        ),
        ExerciseTemplate(
            title="Cuenta premium con super()",
            description="Super, igualdad y orden.",
            instructions=(
                "Define `Cuenta(titular, saldo)` con metodos `depositar(cantidad)` y `retirar(cantidad)` "
                "(sin permitir saldo negativo; si no alcanza, lanza `ValueError`). "
                "Define `CuentaPremium(titular, saldo, cashback_pct)` que herede de Cuenta y "
                "sobreescriba `depositar` para sumar `saldo += cantidad * cashback_pct / 100` despues del deposito base (usa super). "
                "Agrega `__repr__` y define `__eq__` en Cuenta (dos cuentas son iguales si tienen mismo titular y saldo) "
                "y `__lt__` por saldo, para poder ordenar listas con `sorted`."
            ),
            starter_code=(
                "class Cuenta:\n"
                "    def __init__(self, titular, saldo):\n"
                "        self.titular = titular\n"
                "        self.saldo = saldo\n\n"
                "    # TODO: depositar, retirar, __repr__, __eq__, __lt__\n\n"
                "class CuentaPremium(Cuenta):\n"
                "    # TODO\n"
                "    pass\n"
            ),
            hints=[
                "En retirar, valida antes de modificar saldo",
                "Para orden total tambien puedes usar @functools.total_ordering",
                "`super().depositar(cantidad)` antes de aplicar el cashback",
            ],
            difficulty="hard",
            points=25,
        ),
    ],
)

L_ITERADORES = LessonTemplate(
    title="Iteradores y generadores",
    description="Protocolo de iteracion, yield y expresiones generadoras.",
    content="""## Objetivo
Crear iterables perezosos y entender como Python recorre colecciones.

## Protocolo de iteracion
Un **iterable** sabe devolver un **iterador** con `iter(obj)`. Un iterador
responde a `next(it)` devolviendo el siguiente valor o lanzando
`StopIteration`.

```python
nums = [1, 2, 3]
it = iter(nums)
next(it)    # 1
next(it)    # 2
next(it)    # 3
next(it)    # StopIteration
```

El bucle `for x in iterable:` hace exactamente eso por ti.

## Crear un iterador manual
```python
class ContadorHastaN:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        self.i += 1
        return self.i

for x in ContadorHastaN(3):
    print(x)   # 1, 2, 3
```

## Generadores con `yield`
Manera compacta y pythonica:
```python
def contador(n):
    i = 0
    while i < n:
        yield i
        i += 1

for x in contador(3):
    print(x)   # 0, 1, 2
```

### Ventajas
- **Perezosos**: producen valores bajo demanda.
- **Eficientes en memoria**: no construyen la lista entera.
- **Cortocircuitables** con `break`.

### Ejemplo: linea a linea de un archivo
```python
def lineas_largas(path, minlen=80):
    with open(path, encoding="utf-8") as f:
        for linea in f:
            if len(linea) >= minlen:
                yield linea.rstrip()

for l in lineas_largas("log.txt"):
    print(l)
```

## Expresion generadora
Sintaxis inline:
```python
total = sum(x*x for x in range(10**6))
cualquiera = any(e.startswith("ERR") for e in eventos)
```

## Stdlib util: itertools
```python
from itertools import islice, chain, count, cycle, takewhile, groupby

# Tomar solo N elementos
primeros_10 = list(islice(generator, 10))

# Concatenar iterables
for x in chain([1,2], [3,4], [5]):
    print(x)

# Contador infinito
for i in islice(count(100, 5), 3):   # 100, 105, 110
    print(i)

# Agrupar consecutivos
datos = sorted(productos, key=lambda p: p["cat"])
for cat, grupo in groupby(datos, key=lambda p: p["cat"]):
    print(cat, list(grupo))
```

## Errores comunes
- **Agotamiento**: un generador **se consume una vez**. Para iterar de nuevo, regenera.
- **`return` en generador**: termina la iteracion (StopIteration con el valor).
- **`list(gen)`** en datos enormes: anula el beneficio de lazy.

## Resumen
- `yield` crea generadores perezosos.
- Los generadores son iteradores de un solo uso.
- `itertools` te da herramientas potentes sin crear listas intermedias.
""",
    difficulty="advanced",
    category="python-moderno",
    order=19,
    estimated_duration=35,
    prerequisites_titles=["Herencia, polimorfismo y dunder methods"],
    exercises=[
        ExerciseTemplate(
            title="Generador de pares",
            description="yield con condicion.",
            instructions="Implementa `pares_hasta(n)` que use yield para devolver los pares 0..n-1.",
            starter_code="def pares_hasta(n):\n    # TODO: usa yield\n    pass\n",
        ),
        ExerciseTemplate(
            title="Chunks de iterable",
            description="Agrupar de k en k.",
            instructions="Implementa `chunks(it, k)` que devuelva listas de tamano k consumiendo el iterable (la ultima puede ser menor).",
            starter_code="def chunks(it, k):\n    # TODO\n    pass\n",
            difficulty="medium",
            points=15,
        ),
    ],
)

L_DECORADORES = LessonTemplate(
    title="Decoradores",
    description="Funciones de orden superior, @decorator, preservar metadata, decoradores con parametros.",
    content="""## Objetivo
Escribir decoradores para agregar comportamiento transversal sin modificar la funcion original.

## Idea central
Un decorador **envuelve** una funcion para anadir logica antes/despues:
```python
def loggear(fn):
    def envoltura(*args, **kwargs):
        print(f"llamando {fn.__name__}")
        resultado = fn(*args, **kwargs)
        print(f"termino {fn.__name__}")
        return resultado
    return envoltura

@loggear
def saludar(nombre):
    return f"Hola {nombre}"

saludar("Ana")
# llamando saludar
# termino saludar
```

`@loggear` es azucar para `saludar = loggear(saludar)`.

## Preservar metadata con functools.wraps
Sin `wraps`, el nombre/docstring de la funcion decorada se pierde:
```python
from functools import wraps

def loggear(fn):
    @wraps(fn)
    def envoltura(*args, **kwargs):
        return fn(*args, **kwargs)
    return envoltura
```

## Decoradores con parametros
Una capa mas:
```python
from functools import wraps

def reintentar(intentos=3):
    def decorador(fn):
        @wraps(fn)
        def envoltura(*args, **kwargs):
            for n in range(intentos):
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    if n == intentos - 1:
                        raise
        return envoltura
    return decorador

@reintentar(intentos=5)
def fetch(url):
    ...
```

## Decoradores utiles del stdlib
```python
from functools import lru_cache, cache

@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

@cache
def distancia(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5
```

## Decoradores de clases
```python
def registrar(cls):
    cls.registrada = True
    return cls

@registrar
class Handler:
    ...

Handler.registrada   # True
```

## Apilar decoradores
```python
@timing
@reintentar(3)
@loggear
def operacion():
    ...
```
Se aplican **de abajo hacia arriba**:
`operacion = timing(reintentar(3)(loggear(operacion)))`.

## Errores comunes
- **Olvidar `@wraps`**: pierdes nombre y docstring.
- **Modificar argumentos** sin pensar en side-effects.
- **Decorador sin paren para "con parametros"**: `@reintentar` sin `()` pasa la funcion como `intentos`.

## Resumen
- Un decorador es una funcion que recibe una funcion y devuelve otra.
- `@functools.wraps` preserva metadata.
- `lru_cache` resuelve memoizacion en una linea.
""",
    difficulty="advanced",
    category="python-moderno",
    order=20,
    estimated_duration=35,
    prerequisites_titles=["Iteradores y generadores"],
    exercises=[
        ExerciseTemplate(
            title="Decorador timing",
            description="Mide tiempo.",
            instructions="Implementa `@timing` que imprima cuantos ms tardo una funcion. Preserva metadata con wraps.",
            starter_code="from functools import wraps\n\ndef timing(fn):\n    # TODO\n    pass\n",
            difficulty="medium",
            points=15,
        ),
        ExerciseTemplate(
            title="Decorador con parametros: reintentar",
            description="Decorador parametrizable.",
            instructions=(
                "Implementa `reintentar(intentos=3, excepcion=Exception)` que devuelva un decorador. "
                "La funcion decorada debe reintentar hasta `intentos` veces si se lanza una excepcion del tipo dado. "
                "Si falla la ultima vez, re-lanza la excepcion. Usa `functools.wraps`. "
                "Ejemplo de uso: `@reintentar(intentos=5, excepcion=ValueError)` sobre `fetch()`."
            ),
            starter_code=(
                "from functools import wraps\n\n"
                "def reintentar(intentos=3, excepcion=Exception):\n"
                "    # TODO: devolver un decorador\n"
                "    pass\n"
            ),
            hints=[
                "Son tres funciones anidadas: reintentar -> decorador -> envoltura",
                "En el ultimo intento usa `raise` sin argumentos para re-levantar",
            ],
            difficulty="medium",
            points=20,
        ),
        ExerciseTemplate(
            title="Memoize casero",
            description="Decorador de cache manual.",
            instructions=(
                "Implementa `memoize(fn)` sin usar `functools.lru_cache`. Debe cachear los resultados en un dict "
                "usando los argumentos posicionales como clave (tupla). "
                "Agrega un atributo `fib.cache` sobre la envoltura que exponga el dict interno para poder inspeccionarlo. "
                "Demuestra que `fib(30)` con memoize corre en tiempo despreciable comparado con la version recursiva pura."
            ),
            starter_code=(
                "from functools import wraps\n\n"
                "def memoize(fn):\n"
                "    # TODO\n"
                "    pass\n\n"
                "@memoize\n"
                "def fib(n):\n"
                "    return n if n < 2 else fib(n-1) + fib(n-2)\n"
            ),
            hints=[
                "Usa `wrapper.cache = {}` dentro del decorador para exponerlo",
                "Si la funcion recibe kwargs, la clave tambien debe tenerlos (`frozenset(kwargs.items())`)",
            ],
            difficulty="hard",
            points=25,
        ),
    ],
)

L_TIPADO = LessonTemplate(
    title="Type hints y tipado estatico",
    description="Anotaciones, typing, Protocol, TypedDict y chequeo con mypy.",
    content="""## Objetivo
Documentar y validar contratos con type hints modernos.

## Anotaciones basicas
```python
def saludar(nombre: str) -> str:
    return f"Hola {nombre}"

edad: int = 30
nombres: list[str] = ["Ana", "Luis"]
config: dict[str, int] = {"a": 1}
opcional: str | None = None    # Python 3.10+
```

Antes de 3.10:
```python
from typing import Optional, Union, List
def f(x: Optional[int]) -> Union[str, int]: ...
```

## Typing basico
```python
from typing import Callable, Iterable, Iterator, Sequence, Mapping

def aplicar(fn: Callable[[int], int], xs: Iterable[int]) -> list[int]:
    return [fn(x) for x in xs]
```

## Tipos genericos propios
```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Pila(Generic[T]):
    def __init__(self):
        self._items: list[T] = []
    def push(self, x: T) -> None:
        self._items.append(x)
    def pop(self) -> T:
        return self._items.pop()

p: Pila[int] = Pila()
p.push(3)
```

## TypedDict
Para dicts con forma conocida:
```python
from typing import TypedDict

class Usuario(TypedDict):
    id: int
    email: str
    activo: bool

u: Usuario = {"id": 1, "email": "a@x.com", "activo": True}
```

## Protocol (duck typing estatico)
```python
from typing import Protocol

class Cerrable(Protocol):
    def close(self) -> None: ...

def limpiar(resource: Cerrable) -> None:
    resource.close()
```
Cualquier objeto con `close()` pasa, sin heredar de `Cerrable`.

## Literal, Final, NewType
```python
from typing import Literal, Final, NewType

Estado = Literal["pendiente", "ok", "error"]

PI: Final = 3.14159

UserId = NewType("UserId", int)   # tipo distinto de int para mypy
```

## dataclass con types
```python
from dataclasses import dataclass

@dataclass
class Producto:
    nombre: str
    precio: float
    tags: list[str]
```

## mypy
Chequea los tipos estaticamente:
```
pip install mypy
mypy mi_modulo.py
```
Los tipos **no se verifican en runtime** (salvo con herramientas como `pydantic`).

## Errores comunes
- **`list[str]` en Python < 3.9**: usa `List[str]` de `typing`.
- **Tipar demasiado pronto**: en scripts cortos no aporta; en bibliotecas, si.
- **`Any` en todo**: elimina el beneficio del tipado.

## Resumen
- Los hints documentan y, con mypy, validan contratos.
- `Protocol` captura duck typing; `TypedDict` valida forma de dicts.
- `dataclass` + hints = modelos de datos legibles.
""",
    difficulty="advanced",
    category="python-moderno",
    order=21,
    estimated_duration=30,
    prerequisites_titles=["Decoradores"],
    exercises=[
        ExerciseTemplate(
            title="Anotar una funcion",
            description="Agrega type hints.",
            instructions="Anota completamente `def agregar(lista, valor):` para que acepte lista de int y valor int, y devuelva lista de int.",
            starter_code="def agregar(lista, valor):\n    lista.append(valor)\n    return lista\n",
        ),
        ExerciseTemplate(
            title="TypedDict y validacion",
            description="Forma conocida de dict.",
            instructions=(
                "Define un `TypedDict` llamado `Producto` con campos `id: int`, `nombre: str`, `precio: float` y `tags: list[str]`. "
                "Implementa `total_por_tag(productos: list[Producto], tag: str) -> float` que devuelva la suma de precios "
                "de los productos que contienen `tag` en su lista de tags. Anota todo correctamente."
            ),
            starter_code=(
                "from typing import TypedDict\n\n"
                "class Producto(TypedDict):\n"
                "    # TODO: declarar campos\n"
                "    pass\n\n"
                "def total_por_tag(productos, tag):\n"
                "    # TODO: anotar parametros, retorno e implementar\n"
                "    pass\n"
            ),
            hints=[
                "Con `list[Producto]` en 3.9+ ya no necesitas `List`",
                "Usa `sum(...)` con un generador",
            ],
            difficulty="medium",
            points=15,
        ),
        ExerciseTemplate(
            title="Protocol + genericos",
            description="Duck typing estatico y TypeVar.",
            instructions=(
                "Define `Protocol` `Comparable` con un metodo `__lt__(self, otro) -> bool`. "
                "Implementa `minimo(xs: list[T]) -> T` con `T = TypeVar('T', bound=Comparable)` "
                "que devuelva el elemento menor de la lista. Si la lista esta vacia, lanza `ValueError`. "
                "El codigo debe pasar `mypy --strict`."
            ),
            starter_code=(
                "from typing import Protocol, TypeVar\n\n"
                "class Comparable(Protocol):\n"
                "    def __lt__(self, otro) -> bool: ...\n\n"
                "T = TypeVar('T', bound=Comparable)\n\n"
                "def minimo(xs):\n"
                "    # TODO: anotar y implementar\n"
                "    pass\n"
            ),
            hints=[
                "Recorre y mantén un candidato; compara con `<`",
                "Para la lista vacia: `if not xs: raise ValueError(...)`",
            ],
            difficulty="hard",
            points=25,
        ),
    ],
)

L_ASYNC = LessonTemplate(
    title="Programacion asincrona (asyncio)",
    description="async/await, corrutinas, tasks y cuando usar async vs threads.",
    content="""## Objetivo
Entender el modelo asincrono de Python y escribir codigo IO-bound concurrente.

## Sincrono vs asincrono
El IO (red, disco) es **lento**; mientras esperas podrias hacer otra cosa.
`asyncio` permite ejecutar miles de operaciones IO en un solo thread con
**cooperative multitasking**.

## async/await
```python
import asyncio

async def descargar(url):
    await asyncio.sleep(1)    # simula IO
    return f"datos de {url}"

async def main():
    datos = await descargar("https://ejemplo.com")
    print(datos)

asyncio.run(main())
```

- `async def` define una **corrutina**.
- `await` suspende la corrutina hasta que lo esperado termine.
- Solo puedes usar `await` dentro de funciones `async`.

## Concurrencia real con gather
```python
async def main():
    urls = ["a.com", "b.com", "c.com"]
    resultados = await asyncio.gather(*(descargar(u) for u in urls))
    print(resultados)
```
Las tres descargas corren **concurrentemente**, no secuencialmente.

## Tasks
```python
async def main():
    t1 = asyncio.create_task(descargar("a"))
    t2 = asyncio.create_task(descargar("b"))
    # puedes hacer otra cosa aqui mientras esperan
    a, b = await t1, await t2
```

## Timeouts
```python
try:
    r = await asyncio.wait_for(descargar(u), timeout=2.0)
except asyncio.TimeoutError:
    ...
```

## async HTTP con httpx
```python
import httpx, asyncio

async def fetch(cliente, url):
    resp = await cliente.get(url)
    return resp.status_code

async def main():
    async with httpx.AsyncClient() as c:
        resultados = await asyncio.gather(*(fetch(c, u) for u in urls))
```

## Cuando usar async
- IO-bound: red, disco, db, colas -> si.
- CPU-bound (calculo pesado): no. Usa `multiprocessing` o `concurrent.futures`.

## Errores comunes
- **Llamar `funcion_async()` sin `await`**: no ejecuta, crea una corrutina.
- **Mezclar `time.sleep` en codigo async**: bloquea el loop. Usa `asyncio.sleep`.
- **No cerrar sesiones**: usa `async with`.
- **Hacer `requests.get` dentro de async**: bloquea; usa librerias async (`httpx`, `aiohttp`).

## Resumen
- `async/await` es cooperativo y IO-first.
- `asyncio.gather` paraleliza corrutinas.
- No mezcles codigo bloqueante con codigo async.
""",
    difficulty="advanced",
    category="concurrencia",
    order=22,
    estimated_duration=35,
    prerequisites_titles=["Type hints y tipado estatico"],
    exercises=[
        ExerciseTemplate(
            title="Sumar con asyncio.gather",
            description="Concurrencia basica.",
            instructions="Crea `tarea(n)` async que duerma 0.1s y devuelva n*n. Con asyncio.gather, calcula la suma de `tarea(i)` para i en 1..5.",
            starter_code="import asyncio\n\nasync def tarea(n: int) -> int:\n    # TODO\n    pass\n\nasync def main():\n    # TODO: gather y suma\n    pass\n\nasyncio.run(main())\n",
            difficulty="medium",
            points=20,
        ),
        ExerciseTemplate(
            title="Timeout con wait_for",
            description="Cortar corrutinas lentas.",
            instructions=(
                "Implementa `async def cargar(id: int, retraso: float) -> str` que duerma `retraso` segundos "
                "y devuelva `f'item-{id}'`. Luego `async def cargar_con_timeout(id, retraso, limite)` que use "
                "`asyncio.wait_for` para cancelar si supera `limite` segundos, devolviendo `'timeout'` en ese caso. "
                "Prueba con `cargar_con_timeout(1, 0.05, 0.5)` (exito) y `cargar_con_timeout(2, 1.0, 0.2)` (timeout)."
            ),
            starter_code=(
                "import asyncio\n\n"
                "async def cargar(id: int, retraso: float) -> str:\n"
                "    # TODO\n"
                "    pass\n\n"
                "async def cargar_con_timeout(id: int, retraso: float, limite: float) -> str:\n"
                "    # TODO\n"
                "    pass\n"
            ),
            hints=[
                "`try/except asyncio.TimeoutError` captura el timeout",
                "`asyncio.wait_for(coro, timeout=limite)`",
            ],
            difficulty="medium",
            points=20,
        ),
        ExerciseTemplate(
            title="Productor y consumidor con Queue",
            description="Coordinacion de corrutinas.",
            instructions=(
                "Implementa un sistema productor/consumidor usando `asyncio.Queue`. "
                "`productor(cola)` pone 5 items 'tarea-i' (i de 1 a 5) con `await cola.put(...)` separados por `asyncio.sleep(0.01)`. "
                "Al terminar mete un centinela `None`. `consumidor(cola, resultados)` extrae en bucle con `await cola.get()`, "
                "y al ver `None` termina. Debe agregar cada item recibido (sin centinela) a la lista `resultados`. "
                "En `main()` corre ambos con `asyncio.gather` y al final la lista debe tener las 5 tareas en orden."
            ),
            starter_code=(
                "import asyncio\n\n"
                "async def productor(cola):\n"
                "    # TODO\n"
                "    pass\n\n"
                "async def consumidor(cola, resultados):\n"
                "    # TODO\n"
                "    pass\n\n"
                "async def main():\n"
                "    cola = asyncio.Queue()\n"
                "    resultados = []\n"
                "    # TODO: gather\n"
                "    return resultados\n"
            ),
            hints=[
                "`while True: item = await cola.get(); if item is None: break`",
                "La cola respeta orden FIFO, por eso los resultados salen ordenados",
            ],
            difficulty="hard",
            points=30,
        ),
    ],
)

L_STDLIB = LessonTemplate(
    title="Libreria estandar esencial",
    description="datetime, collections, itertools, functools, pathlib, os y json.",
    content="""## Objetivo
Conocer los modulos de la stdlib que resuelven el 80% de tareas diarias.

## datetime
```python
from datetime import datetime, date, timedelta, timezone

ahora = datetime.now(timezone.utc)       # con tz
hoy = date.today()
en_una_semana = hoy + timedelta(days=7)

# Parse/format
datetime.strptime("2026-04-19", "%Y-%m-%d")
hoy.strftime("%d/%m/%Y")            # '19/04/2026'
hoy.isoformat()                     # '2026-04-19'
```

## collections
```python
from collections import Counter, defaultdict, deque, namedtuple, OrderedDict

Counter("mississippi").most_common(2)   # [('i', 4), ('s', 4)]

grupos = defaultdict(list)
for p in productos:
    grupos[p["cat"]].append(p)

# Cola doble, O(1) en ambos extremos
q = deque()
q.append(1); q.appendleft(0); q.pop(); q.popleft()

Punto = namedtuple("Punto", "x y")
p = Punto(1, 2); p.x, p.y
```

## itertools
```python
from itertools import (
    chain, islice, takewhile, dropwhile,
    permutations, combinations, product, groupby, count, cycle, repeat,
)

list(permutations([1,2,3], 2))  # pares ordenados
list(combinations([1,2,3], 2))  # pares no ordenados
list(product([1,2],[3,4]))      # producto cartesiano
list(islice(count(10, 5), 3))   # [10, 15, 20]
```

## functools
```python
from functools import reduce, partial, lru_cache, cache, cached_property

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n-1)+fib(n-2)

doblar = partial(map, lambda x: x*2)
```

## pathlib
```python
from pathlib import Path
p = Path.home() / "proyecto" / "data.txt"
p.exists(); p.is_file(); p.suffix; p.stem
p.write_text("hola")
for f in Path(".").glob("**/*.py"):
    print(f)
```

## os y sys
```python
import os, sys
os.environ["API_KEY"]         # variables de entorno
os.getcwd()
sys.argv                      # argumentos CLI
sys.exit(1)
```
Para CLIs robustas usa `argparse` o `typer`.

## json
```python
import json
data = json.loads('{"a": 1}')           # str -> dict
txt = json.dumps(data, indent=2, ensure_ascii=False)
with open("f.json") as f: data = json.load(f)
with open("f.json","w") as f: json.dump(data, f)
```

## logging (mejor que print en apps)
```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)
log.info("iniciado")
log.warning("cuidado")
log.error("fallo %s", detalle)
```

## re (regex)
```python
import re
re.match(r"\\d+", "123abc")            # solo al inicio
re.search(r"\\d+", "abc123xyz")        # en cualquier parte
re.findall(r"\\d+", "a1 b22 c333")     # ['1','22','333']
re.sub(r"\\s+", "-", "hola mundo")     # 'hola-mundo'
```

## Resumen
- `datetime`, `pathlib`, `json` cubren fechas, rutas y serializacion.
- `collections` tiene estructuras optimizadas listas.
- `itertools`/`functools` evitan reinventar ruedas.
- Usa `logging` y no `print` en aplicaciones reales.
""",
    difficulty="advanced",
    category="stdlib",
    order=23,
    estimated_duration=35,
    prerequisites_titles=["Programacion asincrona (asyncio)"],
    exercises=[
        ExerciseTemplate(
            title="Top palabras",
            description="Usa Counter.",
            instructions="Dada `texto`, devuelve las 3 palabras mas frecuentes (lista de tuplas (palabra, conteo)).",
            starter_code="from collections import Counter\n\ndef top3(texto: str):\n    # TODO\n    pass\n",
        ),
        ExerciseTemplate(
            title="Agrupar con defaultdict",
            description="Agrupacion sin else.",
            instructions=(
                "Implementa `agrupar_por_categoria(productos)`. Recibe una lista de dicts con claves "
                "`{'nombre': str, 'categoria': str, 'precio': float}` y devuelve un `dict[str, list[str]]` "
                "con los nombres agrupados por categoria. Usa `defaultdict(list)` para evitar chequear si la clave existe. "
                "Ejemplo: para `[{'nombre':'Pan','categoria':'panaderia','precio':1.0}, {'nombre':'Leche','categoria':'lacteos','precio':1.5}]` "
                "debe devolver `{'panaderia': ['Pan'], 'lacteos': ['Leche']}`."
            ),
            starter_code=(
                "from collections import defaultdict\n\n"
                "def agrupar_por_categoria(productos):\n"
                "    # TODO\n"
                "    pass\n"
            ),
            hints=[
                "Puedes devolver `dict(agrupados)` para que no parezca un defaultdict",
                "`agrupados[p['categoria']].append(p['nombre'])`",
            ],
            difficulty="medium",
            points=15,
        ),
        ExerciseTemplate(
            title="Pipeline con itertools",
            description="Combinar herramientas.",
            instructions=(
                "Dada una lista de enteros, implementa `ventanas_suma(xs, k)` que devuelva una lista con la suma "
                "de cada ventana deslizante de tamaño `k`. Usa `itertools.islice` y `itertools.tee` en lugar de indices manuales. "
                "Ejemplo: `ventanas_suma([1,2,3,4,5], 3) == [6, 9, 12]`."
            ),
            starter_code=(
                "from itertools import islice, tee\n\n"
                "def ventanas_suma(xs, k):\n"
                "    # TODO\n"
                "    pass\n"
            ),
            hints=[
                "Con `tee(it, k)` puedes crear k iteradores cooperativos",
                "Adelanta cada uno con `islice` a una posicion distinta y luego usa `zip` + `sum`",
            ],
            difficulty="hard",
            points=25,
        ),
    ],
)

L_TESTING = LessonTemplate(
    title="Testing con pytest",
    description="Tests unitarios, fixtures, parametrizacion y mocks.",
    content="""## Objetivo
Escribir pruebas que te den confianza para refactorizar.

## pytest basico
Archivos `test_*.py`, funciones `test_*`:
```python
# test_mates.py
def test_suma():
    assert 2 + 2 == 4

def test_divide_por_cero():
    import pytest
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

Ejecutar:
```
pytest
pytest -v              # verbose
pytest test_mates.py::test_suma
pytest -k "suma"
```

## Asserts claros
`pytest` muestra bien los fallos de `assert` nativo. Evita mensajes crudos:
```python
assert precio_con_iva(100) == 119
```
No necesitas `self.assertEqual`.

## Organizar tests
```
proyecto/
    src/
        mates.py
    tests/
        test_mates.py
        conftest.py    # fixtures compartidas
```

## Fixtures
Codigo de setup reutilizable:
```python
import pytest

@pytest.fixture
def usuario():
    return {"id": 1, "email": "a@x.com", "activo": True}

def test_user_ok(usuario):
    assert usuario["activo"]
```

### Fixtures con teardown
```python
@pytest.fixture
def conexion():
    con = abrir_conexion()
    yield con
    con.close()
```

## Parametrizacion
Un test, muchos casos:
```python
import pytest

@pytest.mark.parametrize("a, b, esperado", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_suma(a, b, esperado):
    assert suma(a, b) == esperado
```

## Mocks
```python
from unittest.mock import patch, MagicMock

def test_fetch(monkeypatch):
    resp = MagicMock(); resp.status_code = 200; resp.json.return_value = {"ok": True}
    with patch("mi_modulo.requests.get", return_value=resp):
        assert mi_modulo.fetch("u").status_code == 200
```

O con el plugin `pytest-mock`:
```python
def test_fetch(mocker):
    mock_get = mocker.patch("mi_modulo.requests.get")
    mock_get.return_value.status_code = 200
```

## Cobertura
```
pip install pytest-cov
pytest --cov=src --cov-report=term-missing
```

## Tests async
```python
import pytest

@pytest.mark.asyncio
async def test_fetch_async():
    resultado = await fetch_async("u")
    assert resultado["ok"]
```

## Buenas practicas
- Un test = una aseveracion logica. No 20 asserts en uno.
- Tests rapidos (ms), aislados, deterministas.
- Separa **unitarios** (rapidos, sin IO) de **integracion** (con DB/red).
- Si un test es dificil de escribir, probablemente el codigo necesita refactor.

## Errores comunes
- **Tests dependientes**: uno necesita que otro haya corrido. Aislalos.
- **Mockear demasiado**: pierdes realismo. Si todo esta mockeado, no validas nada.
- **No testear caminos de error**: el exito es obvio; los errores, no.

## Resumen
- `pytest` con asserts nativos es lo idiomatic.
- Fixtures para setup, parametrize para casos multiples.
- Mocks para aislar dependencias externas.
""",
    difficulty="advanced",
    category="testing",
    order=24,
    estimated_duration=40,
    prerequisites_titles=["Libreria estandar esencial"],
    exercises=[
        ExerciseTemplate(
            title="Tests de calculadora",
            description="Primeros tests.",
            instructions="Escribe tres tests para `suma(a, b)`: caso positivo, caso negativo y caso con cero. Incluye uno parametrizado.",
            starter_code="def suma(a, b):\n    return a + b\n\n# TODO: funciones test_*\n",
            difficulty="hard",
            points=20,
        ),
        ExerciseTemplate(
            title="Fixture con setup y teardown",
            description="Aislamiento de estado.",
            instructions=(
                "Dada una clase `Carrito` con `agregar(item, precio)`, `total()` y `vaciar()`, escribe una fixture "
                "`carrito_con_items` que cree un Carrito, le agregue dos items, lo entregue con `yield` y al final llame `vaciar()`. "
                "Escribe dos tests que usen esa fixture: uno que verifique `total()` y otro que haga `agregar` y vuelva a chequear."
            ),
            starter_code=(
                "import pytest\n\n"
                "class Carrito:\n"
                "    def __init__(self):\n"
                "        self.items = []\n"
                "    def agregar(self, item, precio):\n"
                "        self.items.append((item, precio))\n"
                "    def total(self):\n"
                "        return sum(p for _, p in self.items)\n"
                "    def vaciar(self):\n"
                "        self.items.clear()\n\n"
                "# TODO: fixture carrito_con_items + dos tests\n"
            ),
            hints=[
                "`@pytest.fixture` + `yield` permite hacer teardown despues del yield",
                "Cada test recibe una instancia fresca: la fixture se ejecuta por test",
            ],
            difficulty="medium",
            points=20,
        ),
        ExerciseTemplate(
            title="Mock de API externa",
            description="Aislar dependencias de red.",
            instructions=(
                "Tienes `obtener_usuario(client, user_id)` que llama `client.get(f'/users/{user_id}')` y devuelve `resp.json()`. "
                "Escribe un test que use `unittest.mock.MagicMock` para simular el client, configure la respuesta y verifique: "
                "(1) que la funcion devuelva el dict esperado; (2) que el path llamado sea el correcto "
                "(usa `client.get.assert_called_once_with('/users/42')`)."
            ),
            starter_code=(
                "from unittest.mock import MagicMock\n\n"
                "def obtener_usuario(client, user_id):\n"
                "    resp = client.get(f'/users/{user_id}')\n"
                "    return resp.json()\n\n"
                "# TODO: def test_obtener_usuario():\n"
            ),
            hints=[
                "`client = MagicMock(); client.get.return_value.json.return_value = {...}`",
                "`assert_called_once_with` falla si se llamo con otros argumentos o mas de una vez",
            ],
            difficulty="hard",
            points=25,
        ),
    ],
)

L_PATRONES = LessonTemplate(
    title="Patrones Pythonicos y performance",
    description="Idioms, contextos de uso, profiling y optimizacion responsable.",
    content="""## Objetivo
Escribir codigo idiomatic y medir antes de optimizar.

## Idioms Pythonicos

### Desempaquetar con seguridad
```python
primero, *resto = [1, 2, 3, 4]
```

### swap sin variable temporal
```python
a, b = b, a
```

### Default en dict
```python
d.setdefault("clave", []).append(x)
```

### Any / all
```python
all(p > 0 for p in precios)
any(p == 0 for p in precios)
```

### Enumerate con start
```python
for i, x in enumerate(lista, start=1):
    ...
```

### Uso de `zip(*matriz)` para transponer
```python
matriz = [[1,2,3],[4,5,6]]
transpuesta = list(zip(*matriz))   # [(1,4),(2,5),(3,6)]
```

### Diccionario con `dict.fromkeys`
```python
dict.fromkeys(["a","b","c"], 0)    # {'a':0,'b':0,'c':0}
```

## No optimices sin medir

### timeit
```python
import timeit
timeit.timeit("'-'.join(str(n) for n in range(100))", number=10000)
```

### cProfile
```
python -m cProfile -s cumulative mi_script.py
```

### line_profiler (extra)
```
pip install line_profiler
kernprof -lv mi_script.py
```

## Reglas de pulgar
1. **Mide** antes de optimizar.
2. Reduce la **complejidad algoritmica** (O(n^2) -> O(n)) antes que microoptimizar.
3. Evita bucles Python cuando numpy/pandas pueden vectorizar.
4. No construyas listas intermedias innecesarias (usa generadores).
5. `set`/`dict` para busqueda O(1) en vez de `in list`.

## Estructuras y costo

| Operacion | list | tuple | set | dict |
|---|---|---|---|---|
| acceso por indice | O(1) | O(1) | - | - |
| busqueda `in` | O(n) | O(n) | O(1) | O(1) |
| append/insertar | O(1)/O(n) | inmut. | O(1) | O(1) |
| ordenar | O(n log n) | - | - | - |

## Manejo de memoria
- Objetos muertos se reciclan por **reference counting** + GC.
- Las listas reservan espacio extra (amortizado).
- Los **slots** reducen memoria de clases con muchos atributos:
  ```python
  class Punto:
      __slots__ = ("x", "y")
      def __init__(self, x, y):
          self.x, self.y = x, y
  ```

## Cuando reescribir en C/Rust
Solo despues de:
1. Perfilar y localizar cuellos de botella reales.
2. Agotar optimizaciones algoritmicas.
3. Probar numpy/numba/cython.

## Resumen
- Aprende los idioms y tu codigo se vuelve corto y claro.
- Perfila antes de optimizar.
- La mayoria de ganancias vienen del algoritmo, no del lenguaje.
""",
    difficulty="advanced",
    category="performance",
    order=25,
    estimated_duration=30,
    prerequisites_titles=["Testing con pytest"],
    exercises=[
        ExerciseTemplate(
            title="Refactor a idiomatic",
            description="Aplica idioms.",
            instructions="Reescribe el siguiente codigo usando enumerate y zip:\n```\nfor i in range(len(nombres)):\n    print(i, nombres[i], edades[i])\n```",
            starter_code="nombres = ['Ana','Luis']\nedades = [25, 30]\n# TODO\n",
        ),
        ExerciseTemplate(
            title="Transponer matriz",
            description="zip(*matriz).",
            instructions=(
                "Implementa `transponer(matriz)` que reciba una lista de listas (matriz rectangular) y devuelva "
                "su transpuesta como lista de listas (no de tuplas). En una sola expresion si puedes. "
                "Ejemplo: `transponer([[1,2,3],[4,5,6]]) == [[1,4],[2,5],[3,6]]`."
            ),
            starter_code="def transponer(matriz):\n    # TODO\n    pass\n",
            hints=[
                "`zip(*matriz)` transpone, pero devuelve tuplas: convierte cada fila con `list(...)`",
                "Puedes resolverlo con una list comprehension de una linea",
            ],
            difficulty="medium",
            points=15,
        ),
        ExerciseTemplate(
            title="De O(n^2) a O(n) con set",
            description="Optimizacion algoritmica.",
            instructions=(
                "La funcion `comunes_lento(a, b)` usa `if x in b` sobre una lista, costando O(n*m). "
                "Reescribe `comunes_rapido(a, b)` para que tenga complejidad O(n+m) usando `set`. "
                "Mantén el orden de aparicion en `a` y no duplica elementos. "
                "Ejemplo: `comunes_rapido([1,2,3,2,4], [2,4,5]) == [2,4]`."
            ),
            starter_code=(
                "def comunes_lento(a, b):\n"
                "    return [x for x in a if x in b]\n\n"
                "def comunes_rapido(a, b):\n"
                "    # TODO\n"
                "    pass\n"
            ),
            hints=[
                "`set(b)` te da lookup O(1) para `in`",
                "Un segundo `set` de vistos evita duplicados manteniendo orden",
            ],
            difficulty="hard",
            points=25,
        ),
    ],
)


LESSON_TEMPLATES: list[LessonTemplate] = [
    L_INTRO,
    L_VARIABLES,
    L_OPERADORES,
    L_STRINGS,
    L_IO,
    L_CONDICIONALES,
    L_BUCLES,
    L_LISTAS,
    L_TUPLAS_SETS,
    L_DICTS,
    L_FUNCIONES,
    L_LAMBDAS,
    L_COMPREHENSIONS,
    L_EXCEPCIONES,
    L_ARCHIVOS,
    L_MODULOS,
    L_POO,
    L_HERENCIA,
    L_ITERADORES,
    L_DECORADORES,
    L_TIPADO,
    L_ASYNC,
    L_STDLIB,
    L_TESTING,
    L_PATRONES,
]
