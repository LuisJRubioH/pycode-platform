"""
Seed theory-first Python lessons and guided exercises.
"""

# flake8: noqa: E501 -- archivo de contenido curado: enunciados y starters de ejercicios en espanol.

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning import Exercise, Lesson


@dataclass(frozen=True)
class ExerciseTemplate:
    title: str
    description: str
    instructions: str
    starter_code: str
    hints: list[str] = field(default_factory=list)
    points: int = 10
    difficulty: str = "easy"
    hidden_tests: list[dict] = field(default_factory=list)


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
    track: str = "track-1"


LESSON_TEMPLATES: list[LessonTemplate] = [
    LessonTemplate(
        title="Python desde Cero",
        description="Que es Python, como ejecutar scripts y estructura minima de un programa.",
        content=(
            "## Objetivo\n"
            "Entender que es Python y como correr tu primer script.\n\n"
            "## Teoria\n"
            "- Python es un lenguaje interpretado y multiparadigma.\n"
            "- `print()` muestra informacion en consola.\n"
            "- Un archivo `.py` se ejecuta de arriba hacia abajo.\n\n"
            "## Buenas practicas\n"
            "- Usa nombres claros.\n"
            "- Comenta solo cuando aporta contexto.\n"
            "- Prueba cambios pequeños y frecuentes.\n"
        ),
        difficulty="beginner",
        category="fundamentos",
        order=1,
        estimated_duration=20,
        exercises=[
            ExerciseTemplate(
                title="Hola Python",
                description="Imprime un saludo y tu nombre.",
                instructions="Crea una variable `nombre` y muestra `Hola, <nombre>` usando f-string.",
                starter_code="nombre = ''\n# TODO\n",
                hints=[
                    "Usa print(f'Hola, {nombre}')",
                    "Asigna primero un string a nombre",
                ],
                hidden_tests=[
                    {
                        "name": "imprime 'Hola, <nombre>' con f-string",
                        "code": (
                            "assert nombre, 'define nombre con tu nombre'\n"
                            "assert _salida.strip() == f'Hola, {nombre}', _salida"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Mini presentación",
                description="Muestra dos lineas con informacion personal.",
                instructions="Imprime `ciudad` y `lenguaje` en dos lineas separadas (una por print).",
                starter_code="ciudad = ''\nlenguaje = 'Python'\n# TODO\n",
                hidden_tests=[
                    {
                        "name": "imprime dos lineas (incluye 'Python')",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "assert len(lineas) == 2, ('esperaba 2 lineas', lineas)\n"
                            "assert 'Python' in _salida, _salida"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Variables y Tipos",
        description="Numeros, strings, booleanos y conversiones basicas.",
        content=(
            "## Tipos comunes\n"
            "- `int`, `float`, `str`, `bool`\n"
            "- `type(valor)` permite inspeccionar el tipo.\n\n"
            "## Conversion\n"
            "- `int('10')`, `str(25)`, `float(3)`\n"
            "- Convierte antes de operar para evitar errores.\n"
        ),
        difficulty="beginner",
        category="fundamentos",
        order=2,
        estimated_duration=25,
        prerequisites_titles=["Python desde Cero"],
        exercises=[
            ExerciseTemplate(
                title="Conversor simple",
                description="Convierte texto a numero.",
                instructions="Convierte `texto_numero` a int, calcula su doble e imprimelo (debe dar 24).",
                starter_code="texto_numero = '12'\n# TODO\n",
                hidden_tests=[
                    {
                        "name": "imprime el doble (24)",
                        "code": "assert '24' in _salida, ('esperaba 24 en la salida', _salida)",
                    },
                ],
            ),
            ExerciseTemplate(
                title="Chequeo de tipos",
                description="Valida tipos de variables.",
                instructions="Imprime el tipo (`type(...)`) de `edad`, `altura` y `activo`.",
                starter_code="edad = 18\naltura = 1.72\nactivo = True\n# TODO\n",
                hidden_tests=[
                    {
                        "name": "muestra int, float y bool",
                        "code": (
                            "assert 'int' in _salida and 'float' in _salida and 'bool' in _salida, _salida"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Condicionales y Logica",
        description="if/elif/else, comparaciones y operadores logicos.",
        content=(
            "## Estructura\n"
            "```python\n"
            "if condicion:\n"
            "    ...\n"
            "elif otra:\n"
            "    ...\n"
            "else:\n"
            "    ...\n"
            "```\n\n"
            "## Operadores\n"
            "- Comparacion: `==`, `!=`, `<`, `>`, `<=`, `>=`\n"
            "- Logica: `and`, `or`, `not`\n"
        ),
        difficulty="beginner",
        category="control-flujo",
        order=3,
        estimated_duration=30,
        prerequisites_titles=["Variables y Tipos"],
        exercises=[
            ExerciseTemplate(
                title="Clasificador de edad",
                description="Define etapa de vida basica.",
                instructions="Con `edad` (17), imprime `menor` (<18), `adulto` (<65) o `senior`.",
                starter_code="edad = 17\n# TODO\n",
                hidden_tests=[
                    {
                        "name": "edad 17 -> menor",
                        "code": "assert 'menor' in _salida.lower(), _salida",
                    },
                ],
            ),
            ExerciseTemplate(
                title="Acceso permitido",
                description="Combina condiciones.",
                instructions="Imprime 'Acceso permitido' si `tiene_pase` y `edad >= 18`; si no, 'Acceso denegado'.",
                starter_code="tiene_pase = True\nedad = 19\n# TODO\n",
                hidden_tests=[
                    {
                        "name": "pase + mayor de edad -> permitido",
                        "code": "assert 'permitido' in _salida.lower(), _salida",
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Bucles for y while",
        description="Iteraciones, range y control con break/continue.",
        content=(
            "## for\n"
            "- Recorre elementos o rangos.\n"
            "- `range(inicio, fin, paso)`\n\n"
            "## while\n"
            "- Repite mientras se cumpla una condicion.\n"
            "- Evita bucles infinitos actualizando estado.\n"
        ),
        difficulty="beginner",
        category="control-flujo",
        order=4,
        estimated_duration=35,
        prerequisites_titles=["Condicionales y Logica"],
        exercises=[
            ExerciseTemplate(
                title="Suma acumulada",
                description="Acumula valores 1..n.",
                instructions="Calcula la suma de 1 a `n` (10) usando for e imprime el resultado (55).",
                starter_code="n = 10\n# TODO\n",
                hidden_tests=[
                    {
                        "name": "suma 1..10 = 55",
                        "code": "assert '55' in _salida, ('esperaba 55', _salida)",
                    },
                ],
            ),
            ExerciseTemplate(
                title="Contador while",
                description="Cuenta hacia atras.",
                instructions="Imprime de 5 a 1 (un numero por linea) usando while.",
                starter_code="# TODO\n",
                hidden_tests=[
                    {
                        "name": "imprime 5,4,3,2,1 en orden",
                        "code": (
                            "nums = [x for x in _salida.split() if x.lstrip('-').isdigit()]\n"
                            "assert nums[:5] == ['5', '4', '3', '2', '1'], nums"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Funciones y Parametros",
        description="Definir funciones, retorno y argumentos por defecto.",
        content=(
            "## Funcion\n"
            "Una funcion encapsula una tarea reutilizable.\n\n"
            "## Reglas\n"
            "- Usa `return` para devolver resultados.\n"
            "- Prefiere funciones cortas con una responsabilidad.\n"
            "- Documenta inputs/salidas en comentarios o docstring.\n"
        ),
        difficulty="intermediate",
        category="funciones",
        order=5,
        estimated_duration=35,
        prerequisites_titles=["Bucles for y while"],
        exercises=[
            ExerciseTemplate(
                title="Area de rectangulo",
                description="Funcion con retorno.",
                instructions="Implementa `area_rectangulo(base, altura)`.",
                starter_code="def area_rectangulo(base: float, altura: float) -> float:\n    # TODO\n    pass\n",
                hidden_tests=[
                    {
                        "name": "rectangulo 3x4 da 12",
                        "code": "assert area_rectangulo(3, 4) == 12",
                    },
                    {
                        "name": "soporta floats (2.5 x 4 = 10.0)",
                        "code": "assert abs(area_rectangulo(2.5, 4) - 10.0) < 1e-9",
                    },
                    {
                        "name": "altura 0 da 0",
                        "code": "assert area_rectangulo(7, 0) == 0",
                    },
                ],
            ),
            ExerciseTemplate(
                title="Saludo configurable",
                description="Parametro por defecto.",
                instructions="Implementa `saludar(nombre, prefijo='Hola')`.",
                starter_code="def saludar(nombre: str, prefijo: str = 'Hola') -> str:\n    # TODO\n    pass\n",
                hidden_tests=[
                    {
                        "name": "prefijo por defecto",
                        "code": "assert saludar('Ana') == 'Hola, Ana'",
                    },
                    {
                        "name": "prefijo personalizado",
                        "code": "assert saludar('Luis', prefijo='Hey') == 'Hey, Luis'",
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Listas, Tuplas y Diccionarios",
        description="Estructuras de datos base para colecciones.",
        content=(
            "## Listas\n"
            "- Mutables, indexadas y ordenadas.\n\n"
            "## Tuplas\n"
            "- Inmutables, utiles para pares fijos.\n\n"
            "## Diccionarios\n"
            "- Clave-valor para busqueda rapida.\n"
        ),
        difficulty="intermediate",
        category="estructuras-datos",
        order=6,
        estimated_duration=40,
        prerequisites_titles=["Funciones y Parametros"],
        exercises=[
            ExerciseTemplate(
                title="Promedio de notas",
                description="Recorre listas.",
                instructions="Calcula el promedio de `notas` redondeado a 2 decimales e imprimelo (~4.38).",
                starter_code="notas = [4.5, 3.8, 5.0, 4.2]\n# TODO\n",
                hidden_tests=[
                    {
                        "name": "imprime el promedio (~4.38)",
                        "code": "assert '4.3' in _salida, ('esperaba ~4.38', _salida)",
                    },
                ],
            ),
            ExerciseTemplate(
                title="Agenda minima",
                description="Uso de diccionario.",
                instructions="Agrega a `agenda` el contacto 'ana' con numero '123' e imprime su numero.",
                starter_code="agenda = {}\n# TODO\n",
                hidden_tests=[
                    {
                        "name": "agrega 'ana':'123' y lo imprime",
                        "code": (
                            "assert agenda.get('ana') == '123', ('agenda debe tener ana:123', agenda)\n"
                            "assert '123' in _salida, _salida"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Comprensiones y Manejo de Errores",
        description="List comprehensions y try/except para codigo robusto.",
        content=(
            "## Comprensiones\n"
            "- Sintaxis compacta para transformar colecciones.\n"
            "- Ejemplo: `[x * 2 for x in numeros if x % 2 == 0]`\n\n"
            "## Errores\n"
            "- Usa `try/except` para capturar fallos esperables.\n"
            "- No captures excepciones demasiado generales sin contexto.\n"
        ),
        difficulty="intermediate",
        category="python-moderno",
        order=7,
        estimated_duration=35,
        prerequisites_titles=["Listas, Tuplas y Diccionarios"],
        exercises=[
            ExerciseTemplate(
                title="Filtrado par",
                description="Practica comprehension.",
                instructions="Guarda en `resultado` la lista con los cuadrados de los numeros pares de 1 a 20.",
                starter_code="# TODO: resultado = [...]\n",
                hidden_tests=[
                    {
                        "name": "cuadrados de pares 1..20",
                        "code": (
                            "assert resultado == [4, 16, 36, 64, 100, 144, 196, 256, 324, 400], resultado"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Division segura",
                description="Captura errores comunes.",
                instructions="Implementa `division_segura(a, b)` que retorne None si b es 0.",
                starter_code="def division_segura(a: float, b: float):\n    # TODO\n    pass\n",
                hidden_tests=[
                    {
                        "name": "10 / 2 da 5",
                        "code": "assert division_segura(10, 2) == 5",
                    },
                    {
                        "name": "5 / 0 retorna None",
                        "code": "assert division_segura(5, 0) is None",
                    },
                    {
                        "name": "negativos: -8 / 4 da -2",
                        "code": "assert division_segura(-8, 4) == -2",
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="POO en Python",
        description="Clases, objetos, metodos y encapsulacion basica.",
        content=(
            "## Clase y objeto\n"
            "- Clase define estructura/comportamiento.\n"
            "- Objeto es una instancia de clase.\n\n"
            "## Buenas practicas\n"
            "- Usa `__init__` para estado inicial.\n"
            "- Manten metodos pequenos y enfocados.\n"
        ),
        difficulty="advanced",
        category="oop",
        order=8,
        estimated_duration=45,
        prerequisites_titles=["Comprensiones y Manejo de Errores"],
        exercises=[
            ExerciseTemplate(
                title="Clase Producto",
                description="Modela entidad simple.",
                instructions="Agrega a Producto el metodo `aplicar_descuento(pct)` que reduce `self.precio` en `pct` por ciento.",
                starter_code="class Producto:\n    def __init__(self, nombre: str, precio: float):\n        self.nombre = nombre\n        self.precio = precio\n\n    # TODO: def aplicar_descuento(self, pct): ...\n",
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "descuento 20% sobre 100 -> 80",
                        "code": (
                            "p = Producto('lapiz', 100)\n"
                            "p.aplicar_descuento(20)\n"
                            "assert abs(p.precio - 80) < 1e-9, p.precio"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Cuenta bancaria",
                description="Mutacion de estado.",
                instructions="Implementa `depositar(monto)` (suma al saldo) y `retirar(monto)` (resta si hay saldo; si no, lanza ValueError).",
                starter_code="class Cuenta:\n    def __init__(self):\n        self.saldo = 0\n\n    # TODO: depositar y retirar\n",
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "depositar/retirar actualiza saldo; retiro invalido lanza ValueError",
                        "code": (
                            "c = Cuenta()\n"
                            "c.depositar(100)\n"
                            "c.retirar(30)\n"
                            "assert c.saldo == 70, c.saldo\n"
                            "try:\n"
                            "    c.retirar(1000)\n"
                            "    raise AssertionError('retiro > saldo debio lanzar ValueError')\n"
                            "except ValueError:\n"
                            "    pass"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Modulos, Paquetes y Entornos",
        description="Organiza proyectos Python y gestiona dependencias.",
        content=(
            "## Modulos\n"
            "- Un archivo `.py` es un modulo.\n"
            "- Importa con `import` o `from ... import ...`.\n\n"
            "## Entornos virtuales\n"
            "- Aislan dependencias por proyecto.\n"
            "- Usa `python -m venv .venv` y activa antes de instalar paquetes.\n"
        ),
        difficulty="advanced",
        category="tooling",
        order=9,
        estimated_duration=30,
        prerequisites_titles=["POO en Python"],
        exercises=[
            ExerciseTemplate(
                title="Refactor a modulo",
                description="Separacion por archivos.",
                instructions="Divide funciones en un modulo `utils.py` y consumelo desde `main.py`.",
                starter_code="# main.py\n# TODO\n",
                difficulty="medium",
            ),
        ],
    ),
    LessonTemplate(
        title="Testing con pytest",
        description="Pruebas unitarias para validar comportamiento.",
        content=(
            "## Idea central\n"
            "Las pruebas automatizadas permiten refactorizar con confianza.\n\n"
            "## pytest basico\n"
            "- Archivos `test_*.py`\n"
            "- Funciones `test_*`\n"
            "- Usa asserts claros y casos borde.\n"
        ),
        difficulty="advanced",
        category="testing",
        order=10,
        estimated_duration=40,
        prerequisites_titles=["Modulos, Paquetes y Entornos"],
        exercises=[
            ExerciseTemplate(
                title="Prueba de calculadora",
                description="Escribe tus primeros tests.",
                instructions="Crea tests para suma, resta y division por cero.",
                starter_code="# test_calculadora.py\n# TODO\n",
                difficulty="hard",
                points=20,
            ),
        ],
    ),
    # -----------------------------------------------------------------------
    # Track 2 - Data Science Foundations (piloto)
    # -----------------------------------------------------------------------
    LessonTemplate(
        title="NumPy esencial: arrays y broadcasting",
        description="Crear arrays, indexar, hacer slicing y aprovechar broadcasting para operar vectorizado.",
        content=(
            "## Por que NumPy importa\n"
            "Python puro es lento haciendo loops sobre numeros porque cada\n"
            "operacion pasa por el interprete. NumPy guarda los numeros en un\n"
            "buffer contiguo de memoria y opera en bloque con codigo C/Fortran:\n"
            "un loop de 1 millon de sumas pasa de segundos a milisegundos.\n"
            "Toda la pila de Data Science y ML (Pandas, scikit-learn, PyTorch)\n"
            "esta construida encima de arrays NumPy o de sus equivalentes.\n\n"
            "## Crear arrays\n"
            "```python\n"
            "import numpy as np\n\n"
            "a = np.array([1, 2, 3, 4])        # desde lista\n"
            "ceros = np.zeros(5)               # [0. 0. 0. 0. 0.]\n"
            "unos = np.ones((2, 3))            # matriz 2x3 de unos\n"
            "rango = np.arange(0, 10, 2)       # [0 2 4 6 8]\n"
            "lin = np.linspace(0, 1, 5)        # 5 numeros equiespaciados\n"
            "```\n"
            "Cada array tiene **shape** (forma), **dtype** (tipo numerico) y\n"
            "**ndim** (numero de dimensiones). Inspeccionalos con `a.shape`,\n"
            "`a.dtype`, `a.ndim`.\n\n"
            "## Indexacion y slicing\n"
            "```python\n"
            "a = np.array([10, 20, 30, 40, 50])\n"
            "a[0]       # 10\n"
            "a[-1]      # 50\n"
            "a[1:4]     # [20 30 40]  (vista, no copia)\n"
            "a[a > 20]  # [30 40 50]  (mascara booleana)\n"
            "a[[0, 2, 4]]  # [10 30 50] (fancy indexing)\n"
            "```\n"
            "Las **vistas** comparten memoria con el array original: modificar la\n"
            "vista modifica el original. `a[1:4].copy()` te da una copia\n"
            "independiente. En matrices la regla es la misma por eje:\n"
            "`m[1, 2]` es fila 1 columna 2, `m[:, 0]` es la primera columna entera.\n\n"
            "## Broadcasting\n"
            "Operaciones entre arrays de shapes distintas funcionan si las\n"
            "dimensiones son compatibles: NumPy 'estira' la mas pequeña\n"
            "siguiendo la regla **de derecha a izquierda**, las dimensiones\n"
            "deben ser iguales o una de ellas debe ser 1.\n\n"
            "```python\n"
            "matriz = np.array([[1, 2, 3], [4, 5, 6]])  # shape (2, 3)\n"
            "matriz + 10                                # suma 10 a todo\n"
            "matriz + np.array([10, 20, 30])            # suma fila a fila\n"
            "matriz - matriz.mean(axis=0)               # centra por columna\n"
            "```\n"
            "Esto reemplaza loops anidados y deja el codigo legible.\n\n"
            "## Operaciones vectorizadas vs loop Python\n"
            "Cuando alguien escribe `for i in range(n): a[i] = a[i] * 2` en\n"
            "NumPy, esta tirando a la basura todo lo que NumPy ofrece. La\n"
            "forma idiomatica es `a = a * 2`. Lo mismo con condiciones:\n"
            "en vez de un `for` con `if`, usa una mascara booleana:\n\n"
            "```python\n"
            "negativos = a < 0\n"
            "a[negativos] = 0   # ReLU sin loops\n"
            "```\n\n"
            "## Errores comunes\n"
            "- Confundir `a[i, j]` (NumPy multidim) con `a[i][j]` (Python\n"
            "  encadenado): el primero es mas rapido y aplica slicing real.\n"
            "- Modificar una **vista** pensando que es copia: si despues lees\n"
            "  el original encontraras los cambios.\n"
            "- Olvidar el `axis=` en agregados: `mean()` sin axis colapsa a un\n"
            "  escalar; con `axis=0` colapsa filas (devuelve una fila), con\n"
            "  `axis=1` colapsa columnas (devuelve una columna).\n\n"
            "## Resumen\n"
            "- NumPy = memoria contigua + operaciones en C. Velocidad real.\n"
            "- Crea con `array`, `zeros`, `ones`, `arange`, `linspace`.\n"
            "- Indexa con enteros, slices, mascaras booleanas o fancy indexing.\n"
            "- Vectoriza: si vas a escribir un `for` para mutar un array,\n"
            "  primero piensa si broadcasting o una mascara lo hacen mejor.\n"
        ),
        difficulty="intermediate",
        category="numpy",
        order=11,
        track="track-2",
        estimated_duration=45,
        prerequisites_titles=["Comprensiones y Manejo de Errores"],
        exercises=[
            ExerciseTemplate(
                title="Pares hasta 20",
                description="Crea un array con los pares del 0 al 20 inclusive.",
                instructions=(
                    "Define `pares` como un array NumPy de los enteros pares desde 0 "
                    "hasta 20 inclusive. Usa `np.arange` con el paso adecuado en una "
                    "sola linea. No uses loops."
                ),
                starter_code=(
                    "import numpy as np\n\n" "# Define `pares` aqui:\n" "pares = None\n"
                ),
                hints=[
                    "np.arange(start, stop, step) -- stop es exclusivo, asi que apunta a 21.",
                    "Los pares empiezan en 0 y van de 2 en 2.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "es un ndarray de NumPy",
                        "code": (
                            "import numpy as np\n"
                            "assert isinstance(pares, np.ndarray), "
                            "'pares debe ser np.ndarray'"
                        ),
                    },
                    {
                        "name": "contiene los pares de 0 a 20",
                        "code": (
                            "import numpy as np\n"
                            "assert np.array_equal(pares, np.arange(0, 21, 2))"
                        ),
                    },
                    {
                        "name": "tiene 11 elementos",
                        "code": "assert len(pares) == 11",
                    },
                ],
            ),
            ExerciseTemplate(
                title="Centrar una matriz por columna",
                description="Resta a cada columna su media para que cada columna quede con media cero.",
                instructions=(
                    "Implementa `centrar(matriz)` que recibe un array 2D y devuelve "
                    "una matriz del mismo shape donde a cada columna se le resto su "
                    "media. Usa broadcasting, no loops."
                ),
                starter_code=(
                    "import numpy as np\n\n"
                    "def centrar(matriz: np.ndarray) -> np.ndarray:\n"
                    "    # TODO: calcula la media por columna y restala usando broadcasting.\n"
                    "    pass\n"
                ),
                hints=[
                    "matriz.mean(axis=0) te da un vector con la media de cada columna.",
                    "Restar ese vector a la matriz aprovecha broadcasting fila por fila.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "preserva el shape original",
                        "code": (
                            "import numpy as np\n"
                            "m = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])\n"
                            "assert centrar(m).shape == (3, 2)"
                        ),
                    },
                    {
                        "name": "deja media cero por columna",
                        "code": (
                            "import numpy as np\n"
                            "m = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])\n"
                            "assert np.allclose(centrar(m).mean(axis=0), 0)"
                        ),
                    },
                    {
                        "name": "matriz constante queda en ceros",
                        "code": (
                            "import numpy as np\n"
                            "m = np.full((4, 3), 7.0)\n"
                            "assert np.allclose(centrar(m), 0)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="ReLU sin loops",
                description="Aplica una mascara booleana para poner en cero los valores negativos.",
                instructions=(
                    "Implementa `relu(arr)` que recibe un array NumPy de cualquier "
                    "shape y devuelve un array del mismo shape donde los valores "
                    "negativos quedan en 0 y los positivos se preservan. No uses "
                    "loops ni list comprehensions; usa indexacion booleana o "
                    "`np.maximum`."
                ),
                starter_code=(
                    "import numpy as np\n\n"
                    "def relu(arr: np.ndarray) -> np.ndarray:\n"
                    "    # TODO: devolver una copia con los negativos en 0.\n"
                    "    pass\n"
                ),
                hints=[
                    "Una opcion: out = arr.copy(); out[out < 0] = 0; return out",
                    "Otra opcion mas idiomatica: np.maximum(arr, 0)",
                    "No mutes el array de entrada; haz copia o crea uno nuevo.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "preserva el shape",
                        "code": (
                            "import numpy as np\n"
                            "x = np.array([[-1.0, 2.0, -3.0], [4.0, -5.0, 6.0]])\n"
                            "assert relu(x).shape == x.shape"
                        ),
                    },
                    {
                        "name": "no quedan negativos",
                        "code": (
                            "import numpy as np\n"
                            "x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])\n"
                            "assert (relu(x) >= 0).all()"
                        ),
                    },
                    {
                        "name": "valores positivos quedan iguales",
                        "code": (
                            "import numpy as np\n"
                            "x = np.array([-2.0, 5.0, -1.0, 7.0])\n"
                            "out = relu(x)\n"
                            "assert out[1] == 5.0 and out[3] == 7.0"
                        ),
                    },
                    {
                        "name": "no muta el array de entrada",
                        "code": (
                            "import numpy as np\n"
                            "x = np.array([-1.0, 2.0, -3.0])\n"
                            "original = x.copy()\n"
                            "_ = relu(x)\n"
                            "assert np.array_equal(x, original)"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Pandas esencial: Series, DataFrame e indexing",
        description="Estructuras tabulares con etiquetas: Series, DataFrame, loc/iloc, filtros booleanos y exploracion rapida con head/info/describe.",
        content=(
            "## Por que Pandas\n"
            "NumPy es perfecto para numeros homogeneos en arrays sin etiquetas.\n"
            "El mundo real llega con **columnas heterogeneas** (un string, dos\n"
            "floats, una fecha) y filas que conviene identificar por id o\n"
            "fecha. Pandas envuelve NumPy con dos estructuras etiquetadas:\n"
            "**Series** (1D) y **DataFrame** (2D). Toda la pila de Data\n"
            "Science y casi todo scikit-learn aceptan DataFrames como input.\n\n"
            "## Series — vector con etiquetas\n"
            "```python\n"
            "import pandas as pd\n\n"
            "ventas = pd.Series([120, 80, 95, 200], index=['lun','mar','mie','jue'])\n"
            "ventas['mar']        # 80\n"
            "ventas.mean()        # 123.75\n"
            "ventas > 100         # mascara booleana por dia\n"
            "```\n"
            "Por dentro, `ventas.values` es un array NumPy y `ventas.index`\n"
            "es el indice etiquetado. Las operaciones vectorizadas que viste\n"
            "en NumPy (`* 2`, `+ otra`, broadcasting) funcionan igual.\n\n"
            "## DataFrame — tabla con columnas\n"
            "```python\n"
            "data = {\n"
            "    'nombre': ['Ana','Beto','Carla','David'],\n"
            "    'curso':  ['mate','mate','lengua','lengua'],\n"
            "    'nota':   [4.5, 3.8, 5.0, 2.9],\n"
            "}\n"
            "df = pd.DataFrame(data)\n"
            "```\n"
            "`df` tiene un **indice de filas** (0..3 por defecto), columnas\n"
            "nombradas (`nombre`, `curso`, `nota`) y dtypes por columna\n"
            "(object/float64). Inspeccionalo con:\n\n"
            "```python\n"
            "df.shape       # (4, 3)\n"
            "df.dtypes      # tipo por columna\n"
            "df.head(2)     # primeras 2 filas\n"
            "df.tail()      # ultimas 5 (default)\n"
            "df.info()      # tipos + nulos + memoria\n"
            "df.describe()  # estadisticas de columnas numericas\n"
            "```\n\n"
            "## Indexacion: tres formas (no las mezcles)\n"
            "1. **Por columna** — `df['nota']` devuelve la Serie 'nota'.\n"
            "2. **Por etiqueta** — `df.loc[2, 'nota']` (fila etiqueta 2,\n"
            "   columna 'nota'). Slicing inclusivo: `df.loc[1:3]` trae\n"
            "   filas 1,2,3.\n"
            "3. **Por posicion** — `df.iloc[0, 2]` (primera fila, tercera\n"
            "   columna). Slicing exclusivo: `df.iloc[0:2]` trae 2 filas.\n\n"
            "Si tu indice ya es 0..N-1, `loc` e `iloc` parecen iguales pero\n"
            "dejan de serlo apenas pones `df.set_index('nombre')`.\n\n"
            "## Filtros booleanos\n"
            "```python\n"
            "aprobados = df[df['nota'] >= 4]\n"
            "df[(df['nota'] >= 4) & (df['curso'] == 'mate')]\n"
            "```\n"
            "**Cuidado con `and`/`or`**: en pandas se usan los operadores\n"
            "bit a bit `&` y `|` (con parentesis obligatorios), no las\n"
            "palabras `and`/`or`. Confundirlos da un `ValueError`.\n\n"
            "## Cargar desde CSV\n"
            "Lo mas comun en la vida real es leer un archivo:\n"
            "```python\n"
            "df = pd.read_csv('iris.csv')\n"
            "```\n"
            "En PyCode tenes datasets curados accesibles via:\n"
            "```python\n"
            "import pycode\n"
            "df = await pycode.load_dataset('iris')\n"
            "```\n"
            "(el `await` es porque corre en navegador y la red es asincronica)\n\n"
            "## Errores comunes\n"
            "- Mezclar `loc` e `iloc`. Si tu indice es entero pero no es 0..N-1\n"
            "  (porque hiciste `drop` o `query`), `df.loc[0]` puede no existir\n"
            "  aunque la primera fila si.\n"
            "- Usar `and`/`or` en filtros: rompe con\n"
            "  `The truth value of a Series is ambiguous`.\n"
            "- Modificar una vista con `df[df.col > X].col = ...`: pandas avisa con\n"
            "  `SettingWithCopyWarning`. Lo correcto: `df.loc[df.col > X, 'col'] = ...`.\n"
            "- Olvidar que `read_csv` infiere dtypes y a veces convierte tu id\n"
            "  numerico a float si hay un NaN. Mira `df.dtypes` primero.\n\n"
            "## Resumen\n"
            "- Series = vector con etiquetas. DataFrame = tabla con columnas.\n"
            "- Tres indexadores: por columna, `loc` (etiqueta), `iloc` (posicion).\n"
            "- Filtros con `&`/`|` y parentesis.\n"
            "- `head`/`info`/`describe` son tu primer reflejo al recibir un\n"
            "  dataset desconocido.\n"
        ),
        difficulty="intermediate",
        category="pandas",
        order=12,
        track="track-2",
        estimated_duration=50,
        prerequisites_titles=["NumPy esencial: arrays y broadcasting"],
        exercises=[
            ExerciseTemplate(
                title="Series desde diccionario",
                description="Crea una Series de pandas a partir de un dict.",
                instructions=(
                    "Define `ventas` como una `pd.Series` cuyos valores sean "
                    "[120, 80, 95, 200] con indice ['lun','mar','mie','jue']. "
                    "No uses pd.DataFrame; la respuesta es una Series."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "# Define `ventas` aqui:\n"
                    "ventas = None\n"
                ),
                hints=[
                    "pd.Series acepta una lista de valores y un parametro `index=`.",
                    "Tambien podes pasarle un dict directamente: pd.Series({'lun': 120, ...}).",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "es una pandas Series",
                        "code": (
                            "import pandas as pd\n"
                            "assert isinstance(ventas, pd.Series), 'debe ser pd.Series'"
                        ),
                    },
                    {
                        "name": "tiene los 4 valores correctos",
                        "code": ("assert list(ventas.values) == [120, 80, 95, 200]"),
                    },
                    {
                        "name": "indice por dia de la semana",
                        "code": (
                            "assert list(ventas.index) == ['lun','mar','mie','jue']"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Filtrar aprobados",
                description="Funcion que devuelve solo las filas con nota >= 4.",
                instructions=(
                    "Implementa `filtrar_aprobados(df)` que recibe un DataFrame "
                    "con una columna 'nota' y devuelve un DataFrame con solo "
                    "las filas donde nota >= 4. Usa filtro booleano, no loops."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def filtrar_aprobados(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: filtro booleano sobre la columna 'nota'.\n"
                    "    pass\n"
                ),
                hints=[
                    "df[df['nota'] >= 4] devuelve un DataFrame con esas filas.",
                    "Recorda que el indice de las filas se preserva (no se reinicia).",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "devuelve un DataFrame",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'nombre': ['A','B','C'], 'nota': [4.5, 2.9, 5.0]})\n"
                            "out = filtrar_aprobados(df)\n"
                            "assert isinstance(out, pd.DataFrame)"
                        ),
                    },
                    {
                        "name": "no incluye notas menores a 4",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'nombre': ['A','B','C'], 'nota': [4.5, 2.9, 5.0]})\n"
                            "out = filtrar_aprobados(df)\n"
                            "assert (out['nota'] >= 4).all()"
                        ),
                    },
                    {
                        "name": "incluye las notas correctas",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'nombre': ['A','B','C','D'], 'nota': [4.5, 2.9, 5.0, 3.9]})\n"
                            "out = filtrar_aprobados(df)\n"
                            "assert sorted(out['nombre'].tolist()) == ['A','C']"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Promedio por curso (groupby)",
                description="Agrupa por curso y calcula el promedio de notas.",
                instructions=(
                    "Implementa `promedio_por_curso(df)` que devuelve una Series "
                    "donde el indice es el nombre del curso y el valor es el "
                    "promedio de notas en ese curso. Usa groupby + mean, no loops."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def promedio_por_curso(df: pd.DataFrame) -> pd.Series:\n"
                    "    # TODO: df.groupby('curso')['nota'].mean()\n"
                    "    pass\n"
                ),
                hints=[
                    "df.groupby('curso') agrupa por la columna 'curso'.",
                    "['nota'].mean() selecciona la columna y aplica la agregacion.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "devuelve una Series",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'curso': ['mate','mate','lengua','lengua'],\n"
                            "    'nota': [4.5, 3.5, 5.0, 3.0],\n"
                            "})\n"
                            "out = promedio_por_curso(df)\n"
                            "assert isinstance(out, pd.Series)"
                        ),
                    },
                    {
                        "name": "promedio de mate = 4.0, lengua = 4.0",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'curso': ['mate','mate','lengua','lengua'],\n"
                            "    'nota': [4.5, 3.5, 5.0, 3.0],\n"
                            "})\n"
                            "out = promedio_por_curso(df)\n"
                            "assert abs(out['mate'] - 4.0) < 1e-9\n"
                            "assert abs(out['lengua'] - 4.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "funciona con 3 cursos",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'curso': ['a','a','b','c','c','c'],\n"
                            "    'nota': [2.0, 4.0, 5.0, 3.0, 3.0, 3.0],\n"
                            "})\n"
                            "out = promedio_por_curso(df)\n"
                            "assert sorted(out.index.tolist()) == ['a','b','c']\n"
                            "assert abs(out['a'] - 3.0) < 1e-9\n"
                            "assert abs(out['c'] - 3.0) < 1e-9"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Pandas: groupby, agregaciones y pivot",
        description="Agrupacion con multiples claves, agg multi-metrica, transform vs apply, y reshape con pivot_table.",
        content=(
            "## Por que importa\n"
            "El 80% del trabajo de un analista DS es **agrupar y agregar**.\n"
            "Pandas tiene un set de herramientas para hacerlo en una sola\n"
            "linea y de forma vectorizada. Sin esto terminas con loops sobre\n"
            "filas y matas la performance.\n\n"
            "## groupby — el patron split-apply-combine\n"
            "```python\n"
            "import pandas as pd\n\n"
            "df = pd.DataFrame({\n"
            "    'sucursal': ['centro','centro','norte','norte','sur'],\n"
            "    'producto': ['cafe','te','cafe','te','cafe'],\n"
            "    'ingreso':  [120,    80,  90,    70,   60],\n"
            "})\n"
            "df.groupby('sucursal')['ingreso'].sum()\n"
            "# sucursal\n"
            "# centro    200\n"
            "# norte     160\n"
            "# sur        60\n"
            "```\n"
            "El objeto `df.groupby(...)` no calcula nada hasta que aplicas\n"
            "una agregacion (`.sum`, `.mean`, `.count`, etc.).\n\n"
            "## Agrupar por varias columnas\n"
            "```python\n"
            "df.groupby(['sucursal','producto'])['ingreso'].sum()\n"
            "```\n"
            "Devuelve una Serie con **MultiIndex**: cada fila esta indexada\n"
            "por la tupla (sucursal, producto). Para volver a DataFrame\n"
            "plano usa `.reset_index()`.\n\n"
            "## agg — varias metricas a la vez\n"
            "```python\n"
            "df.groupby('sucursal')['ingreso'].agg(['sum','mean','count'])\n"
            "```\n"
            "Devuelve un DataFrame con una columna por metrica. Tambien acepta\n"
            "un dict para metricas por columna:\n"
            "```python\n"
            "df.groupby('sucursal').agg({\n"
            "    'ingreso': 'sum',\n"
            "    'producto': 'nunique',\n"
            "})\n"
            "```\n\n"
            "## transform — agregar al original\n"
            "`groupby().agg(...)` colapsa filas. `transform(...)` devuelve\n"
            "un Series del **mismo largo** que el DataFrame, util para\n"
            "agregar una columna calculada por grupo:\n"
            "```python\n"
            "df['ingreso_total_sucursal'] = df.groupby('sucursal')['ingreso'].transform('sum')\n"
            "```\n"
            "Ahora cada fila tiene el total de su sucursal al lado. Esto\n"
            "permite calcular porcentajes (`fila['ingreso'] / total_sucursal`)\n"
            "sin merge manual.\n\n"
            "## pivot_table — reshape facil\n"
            "Cuando tu data esta en formato 'largo' (cada fila es una observacion)\n"
            "y la queres en formato 'ancho' (filas y columnas con sus combinaciones):\n"
            "```python\n"
            "df.pivot_table(\n"
            "    index='sucursal',\n"
            "    columns='producto',\n"
            "    values='ingreso',\n"
            "    aggfunc='sum',\n"
            "    fill_value=0,\n"
            ")\n"
            "# producto    cafe   te\n"
            "# sucursal\n"
            "# centro       120   80\n"
            "# norte         90   70\n"
            "# sur           60    0\n"
            "```\n"
            "Es el equivalente a una tabla dinamica de Excel pero programable.\n\n"
            "## Errores comunes\n"
            "- Olvidar `reset_index()` despues de un groupby cuando necesitas\n"
            "  pasar el resultado a otra funcion que espera DataFrame plano.\n"
            "- Usar `groupby().apply(lambda x: ...)` para algo que ya hace\n"
            "  `agg` o `transform`. `apply` es la opcion mas lenta y mas\n"
            "  flexible — usala cuando las otras dos no alcancen.\n"
            "- En `pivot_table`, olvidar `fill_value` deja NaN en combinaciones\n"
            "  inexistentes (sur no vendio te → NaN). Casi siempre queres 0.\n"
            "- Confundir `groupby` con `pivot_table`: `groupby` colapsa filas\n"
            "  manteniendo el orden tabular; `pivot_table` reshapea filas a\n"
            "  columnas.\n\n"
            "## Resumen\n"
            "- `groupby` divide en grupos; las agregaciones colapsan filas.\n"
            "- `agg` permite multiples metricas / columnas en una llamada.\n"
            "- `transform` mantiene el largo original — util para columnas\n"
            "  derivadas por grupo.\n"
            "- `pivot_table` reshapea largo → ancho con agregaciones.\n"
        ),
        difficulty="intermediate",
        category="pandas",
        order=13,
        track="track-2",
        estimated_duration=50,
        prerequisites_titles=["Pandas esencial: Series, DataFrame e indexing"],
        exercises=[
            ExerciseTemplate(
                title="Total por sucursal y producto",
                description="Suma de ingresos agrupando por dos columnas.",
                instructions=(
                    "Implementa `total_por_sucursal_producto(df)` que recibe un "
                    "DataFrame con columnas 'sucursal', 'producto' e 'ingreso' "
                    "y devuelve una Series con MultiIndex (sucursal, producto) "
                    "y la suma de ingresos. Usa groupby con lista de columnas."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def total_por_sucursal_producto(df: pd.DataFrame) -> pd.Series:\n"
                    "    # TODO: df.groupby([col1, col2])['ingreso'].sum()\n"
                    "    pass\n"
                ),
                hints=[
                    "groupby acepta una lista de columnas: df.groupby(['sucursal','producto']).",
                    "El resultado es una Series con MultiIndex.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "es una pandas Series",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['centro','centro','norte','norte','sur'],\n"
                            "    'producto':['cafe','te','cafe','te','cafe'],\n"
                            "    'ingreso':[120,80,90,70,60],\n"
                            "})\n"
                            "out = total_por_sucursal_producto(df)\n"
                            "assert isinstance(out, pd.Series)"
                        ),
                    },
                    {
                        "name": "MultiIndex con 2 niveles",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['centro','centro','norte','norte','sur'],\n"
                            "    'producto':['cafe','te','cafe','te','cafe'],\n"
                            "    'ingreso':[120,80,90,70,60],\n"
                            "})\n"
                            "out = total_por_sucursal_producto(df)\n"
                            "assert isinstance(out.index, pd.MultiIndex)\n"
                            "assert out.index.nlevels == 2"
                        ),
                    },
                    {
                        "name": "totales correctos",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['centro','centro','norte','norte','sur'],\n"
                            "    'producto':['cafe','te','cafe','te','cafe'],\n"
                            "    'ingreso':[120,80,90,70,60],\n"
                            "})\n"
                            "out = total_por_sucursal_producto(df)\n"
                            "assert out[('centro','cafe')] == 120\n"
                            "assert out[('centro','te')] == 80\n"
                            "assert out[('sur','cafe')] == 60"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Multiples metricas por sucursal",
                description="Agregar varias estadisticas en una llamada usando agg.",
                instructions=(
                    "Implementa `metricas_sucursal(df)` que devuelve un "
                    "DataFrame indexado por 'sucursal' con tres columnas: "
                    "'total_ingreso' (suma), 'venta_promedio' (mean) y "
                    "'cantidad' (count) de la columna 'ingreso'. Una sola "
                    "llamada con agg + named aggregation."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def metricas_sucursal(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: df.groupby('sucursal').agg(total_ingreso=('ingreso','sum'), ...)\n"
                    "    pass\n"
                ),
                hints=[
                    "Named aggregation: agg(col_nueva=('col_origen','funcion')).",
                    "Devolves un DataFrame con sucursal como indice y las 3 columnas.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "es un DataFrame con las 3 columnas",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','n'],\n"
                            "    'ingreso':[100,50,80,20],\n"
                            "})\n"
                            "out = metricas_sucursal(df)\n"
                            "assert isinstance(out, pd.DataFrame)\n"
                            "assert set(out.columns) == {'total_ingreso','venta_promedio','cantidad'}"
                        ),
                    },
                    {
                        "name": "valores correctos para 2 sucursales",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','n'],\n"
                            "    'ingreso':[100,50,80,20],\n"
                            "})\n"
                            "out = metricas_sucursal(df)\n"
                            "assert out.loc['c','total_ingreso'] == 150\n"
                            "assert out.loc['n','venta_promedio'] == 50\n"
                            "assert out.loc['c','cantidad'] == 2"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Pivot ventas por sucursal y producto",
                description="Reshape de formato largo a ancho con pivot_table.",
                instructions=(
                    "Implementa `pivot_ventas(df)` que devuelve un DataFrame "
                    "con sucursal como indice, producto como columnas, y suma "
                    "de 'ingreso' como valores. Combinaciones inexistentes "
                    "deben quedar en 0, no en NaN."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def pivot_ventas(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: pd.pivot_table(df, index=..., columns=..., values=..., aggfunc='sum', fill_value=0)\n"
                    "    pass\n"
                ),
                hints=[
                    "Usa pd.pivot_table o df.pivot_table — la API es igual.",
                    "fill_value=0 reemplaza los NaN de las combinaciones que no existen.",
                    "aggfunc='sum' especifica que agregamos sumando los ingresos.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "es DataFrame con sucursal de index",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','sur'],\n"
                            "    'producto':['cafe','te','cafe','cafe'],\n"
                            "    'ingreso':[100,50,80,60],\n"
                            "})\n"
                            "out = pivot_ventas(df)\n"
                            "assert isinstance(out, pd.DataFrame)\n"
                            "assert out.index.name == 'sucursal'"
                        ),
                    },
                    {
                        "name": "combinacion inexistente queda en 0 (no NaN)",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','sur'],\n"
                            "    'producto':['cafe','te','cafe','cafe'],\n"
                            "    'ingreso':[100,50,80,60],\n"
                            "})\n"
                            "out = pivot_ventas(df)\n"
                            "# sur no vendio te → debe ser 0, no NaN\n"
                            "assert out.loc['sur','te'] == 0"
                        ),
                    },
                    {
                        "name": "sumas correctas en celdas con datos",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','c','n'],\n"
                            "    'producto':['cafe','cafe','te','cafe'],\n"
                            "    'ingreso':[100,50,80,90],\n"
                            "})\n"
                            "out = pivot_ventas(df)\n"
                            "# c-cafe = 100 + 50 = 150\n"
                            "assert out.loc['c','cafe'] == 150\n"
                            "assert out.loc['c','te'] == 80\n"
                            "assert out.loc['n','cafe'] == 90"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Pandas: merge, join y fechas",
        description="Unir tablas con merge (inner/left/right/outer), parsear fechas con to_datetime y extraer componentes con el accessor .dt.",
        content=(
            "## Por que merge\n"
            "Casi ningun dataset llega completo. La info que necesitas suele\n"
            "estar **separada en varias tablas** (ventas + productos + clientes)\n"
            "y la juntas por una clave comun. Es la operacion equivalente a un\n"
            "JOIN en SQL, pero sintaxis Python.\n\n"
            "## merge basico\n"
            "```python\n"
            "import pandas as pd\n\n"
            "ventas = pd.DataFrame({\n"
            "    'producto_id': [1, 2, 1, 3],\n"
            "    'unidades':    [5, 2, 3, 1],\n"
            "})\n"
            "productos = pd.DataFrame({\n"
            "    'producto_id': [1, 2, 3, 4],\n"
            "    'nombre':      ['cafe','te','torta','sandwich'],\n"
            "    'precio':      [3.5, 2.5, 4.5, 6.0],\n"
            "})\n\n"
            "df = ventas.merge(productos, on='producto_id')\n"
            "```\n"
            "Por defecto, `merge` hace un **inner join**: solo filas con clave\n"
            "presente en ambas tablas. Los `producto_id=4` (sandwich) y filas\n"
            "huerfanas en ventas desaparecen.\n\n"
            "## El parametro how — controla el tipo de join\n"
            "```python\n"
            "# Quiero TODAS las ventas, aunque el producto no exista en el catalogo\n"
            "ventas.merge(productos, on='producto_id', how='left')\n\n"
            "# Quiero TODOS los productos, aunque no se hayan vendido\n"
            "ventas.merge(productos, on='producto_id', how='right')\n\n"
            "# Quiero TODO (ventas huerfanas + productos sin ventas)\n"
            "ventas.merge(productos, on='producto_id', how='outer')\n"
            "```\n"
            "Las filas sin match del otro lado quedan con NaN en las columnas\n"
            "que aporta la tabla ausente.\n\n"
            "## Claves con nombres distintos\n"
            "Cuando las columnas se llaman distinto en cada tabla, usa\n"
            "`left_on` y `right_on`:\n"
            "```python\n"
            "ventas.merge(productos, left_on='producto_id', right_on='id')\n"
            "```\n\n"
            "## pd.to_datetime — parsear fechas en serio\n"
            "Pandas no infiere fechas por defecto: una columna `'2026-06-14'`\n"
            "queda como `object` (string). Convertir explicitamente:\n"
            "```python\n"
            "df['fecha'] = pd.to_datetime(df['fecha'])  # detecta el formato\n"
            "df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y')  # explicit\n"
            "```\n"
            "Despues de esto, `df['fecha'].dtype` es `datetime64[ns]` y\n"
            "podes hacer aritmetica de fechas y comparaciones.\n\n"
            "## El accessor .dt — extraer componentes\n"
            "Sobre una columna datetime, `.dt` expone propiedades:\n"
            "```python\n"
            "df['mes'] = df['fecha'].dt.month        # 1..12\n"
            "df['dia_semana'] = df['fecha'].dt.day_name()  # 'Monday', ...\n"
            "df['anio'] = df['fecha'].dt.year\n"
            "df['es_fin_de_semana'] = df['fecha'].dt.dayofweek >= 5\n"
            "```\n\n"
            "## resample — agregar por ventana temporal\n"
            "Si la fecha es indice del DataFrame, `resample(...)` agrupa por\n"
            "ventana de tiempo (similar a `groupby` pero para series temporales):\n"
            "```python\n"
            "df2 = df.set_index('fecha')\n"
            "df2['ingreso'].resample('W').sum()  # suma por semana\n"
            "df2['ingreso'].resample('M').mean() # promedio por mes\n"
            "```\n\n"
            "## Errores comunes\n"
            "- Hacer merge sin especificar `on=`: pandas adivina por columnas\n"
            "  con el mismo nombre, lo que puede mezclar columnas\n"
            "  irrelevantes (`fecha` por ejemplo) o fallar silenciosamente.\n"
            "  **Siempre se explicito con `on=` o `left_on/right_on`**.\n"
            "- Olvidar `how=` cuando queres preservar filas sin match: te\n"
            "  perdes data sin darte cuenta.\n"
            "- Hacer `.dt.year` sobre una columna que sigue siendo string:\n"
            "  da AttributeError. Llamar `pd.to_datetime` primero.\n"
            "- Mergear con duplicados en la clave: el resultado tiene\n"
            "  **producto cartesiano** de los duplicados — el numero de filas\n"
            "  explota. Revisa `df['clave'].duplicated().sum()` antes.\n\n"
            "## Resumen\n"
            "- `merge(on=, how=)` une tablas; inner es default. Usa left/right/\n"
            "  outer cuando necesitas preservar filas sin match.\n"
            "- `pd.to_datetime` antes de operar sobre fechas. Sin esto, son strings.\n"
            "- `.dt` expone month/year/day_name/dayofweek/... sobre columnas datetime.\n"
            "- `resample` agrega por ventana temporal cuando el indice es datetime.\n"
        ),
        difficulty="intermediate",
        category="pandas",
        order=14,
        track="track-2",
        estimated_duration=55,
        prerequisites_titles=["Pandas: groupby, agregaciones y pivot"],
        exercises=[
            ExerciseTemplate(
                title="Join ventas con catalogo (inner)",
                description="Unir dos DataFrames por producto_id con inner join.",
                instructions=(
                    "Implementa `unir_con_catalogo(ventas, productos)` que "
                    "merge ventas con productos por 'producto_id' con inner join. "
                    "Devuelve el DataFrame combinado."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def unir_con_catalogo(ventas: pd.DataFrame, productos: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: merge por 'producto_id', how='inner'.\n"
                    "    pass\n"
                ),
                hints=[
                    "ventas.merge(productos, on='producto_id') hace inner por defecto.",
                    "Las filas sin match en ambas tablas desaparecen.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve un DataFrame",
                        "code": (
                            "import pandas as pd\n"
                            "v = pd.DataFrame({'producto_id':[1,2,1], 'unidades':[5,2,3]})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'nombre':['cafe','te']})\n"
                            "out = unir_con_catalogo(v, p)\n"
                            "assert isinstance(out, pd.DataFrame)"
                        ),
                    },
                    {
                        "name": "incluye la columna 'nombre' del catalogo",
                        "code": (
                            "import pandas as pd\n"
                            "v = pd.DataFrame({'producto_id':[1,2,1], 'unidades':[5,2,3]})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'nombre':['cafe','te']})\n"
                            "out = unir_con_catalogo(v, p)\n"
                            "assert 'nombre' in out.columns\n"
                            "assert 'unidades' in out.columns"
                        ),
                    },
                    {
                        "name": "huerfanas en ventas no aparecen (inner)",
                        "code": (
                            "import pandas as pd\n"
                            "v = pd.DataFrame({'producto_id':[1,2,99], 'unidades':[5,2,1]})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'nombre':['cafe','te']})\n"
                            "out = unir_con_catalogo(v, p)\n"
                            "assert 99 not in out['producto_id'].tolist()\n"
                            "assert len(out) == 2"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Extraer mes de una fecha",
                description="Parsear fechas y agregar columna con el mes.",
                instructions=(
                    "Implementa `con_mes(df)` que recibe un DataFrame con "
                    "columna 'fecha' (strings tipo '2026-06-14') y devuelve el "
                    "mismo DataFrame con una nueva columna 'mes' (int 1..12). "
                    "No modifiques el DataFrame original — devuelve una copia."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def con_mes(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: copia, parsea fecha con pd.to_datetime, usa .dt.month.\n"
                    "    pass\n"
                ),
                hints=[
                    "df_copy = df.copy() para no mutar el original.",
                    "pd.to_datetime(df_copy['fecha']).dt.month da int 1..12.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "no muta el DataFrame original",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'fecha': ['2026-01-15', '2026-06-30']})\n"
                            "_ = con_mes(df)\n"
                            "assert 'mes' not in df.columns, 'no muta el original'"
                        ),
                    },
                    {
                        "name": "agrega columna mes con valores correctos",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'fecha': ['2026-01-15', '2026-06-30', '2026-12-01']})\n"
                            "out = con_mes(df)\n"
                            "assert 'mes' in out.columns\n"
                            "assert out['mes'].tolist() == [1, 6, 12]"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Ingresos por semana (resample)",
                description="Join + parseo de fechas + resample semanal de ingresos.",
                instructions=(
                    "Implementa `ingresos_semanales(ventas, productos)` que: "
                    "(1) mergea por 'producto_id', (2) calcula 'ingreso' = "
                    "unidades * precio, (3) parsea 'fecha' a datetime, (4) "
                    "devuelve una Serie con la suma de ingresos por semana, "
                    "indexada por fecha de fin de semana. Usa resample('W')."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def ingresos_semanales(ventas: pd.DataFrame, productos: pd.DataFrame) -> pd.Series:\n"
                    "    # TODO: merge, calcular ingreso, to_datetime, set_index, resample('W').sum()\n"
                    "    pass\n"
                ),
                hints=[
                    "df['ingreso'] = df['unidades'] * df['precio'] (vectorizado).",
                    "df = df.set_index('fecha') antes de resamplear.",
                    "df['ingreso'].resample('W').sum() agrupa por semana terminando en domingo.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "devuelve una pandas Series",
                        "code": (
                            "import pandas as pd\n"
                            "v = pd.DataFrame({\n"
                            "    'fecha':['2026-01-05','2026-01-06','2026-01-13'],\n"
                            "    'producto_id':[1,2,1],\n"
                            "    'unidades':[2,3,1],\n"
                            "})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'precio':[10.0, 5.0]})\n"
                            "out = ingresos_semanales(v, p)\n"
                            "assert isinstance(out, pd.Series)"
                        ),
                    },
                    {
                        "name": "indice es datetime",
                        "code": (
                            "import pandas as pd\n"
                            "v = pd.DataFrame({\n"
                            "    'fecha':['2026-01-05','2026-01-06','2026-01-13'],\n"
                            "    'producto_id':[1,2,1],\n"
                            "    'unidades':[2,3,1],\n"
                            "})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'precio':[10.0, 5.0]})\n"
                            "out = ingresos_semanales(v, p)\n"
                            "assert pd.api.types.is_datetime64_any_dtype(out.index)"
                        ),
                    },
                    {
                        "name": "ingresos sumados correctamente por semana",
                        "code": (
                            "import pandas as pd\n"
                            "# 5-ene (lun) y 6-ene (mar) caen en la misma semana W (term. domingo 11)\n"
                            "# 13-ene (mar) cae en la semana terminando domingo 18\n"
                            "v = pd.DataFrame({\n"
                            "    'fecha':['2026-01-05','2026-01-06','2026-01-13'],\n"
                            "    'producto_id':[1,2,1],\n"
                            "    'unidades':[2,3,1],\n"
                            "})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'precio':[10.0, 5.0]})\n"
                            "out = ingresos_semanales(v, p)\n"
                            "# semana 1: 2*10 + 3*5 = 35\n"
                            "# semana 2: 1*10 = 10\n"
                            "assert sorted(out.values.tolist()) == [10.0, 35.0]"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Pandas: limpieza de datos y missing values",
        description="Detectar y manejar NaN con isna/fillna/dropna, eliminar duplicados, convertir tipos con errors=coerce, y limpiar strings con el accessor .str.",
        content=(
            "## Por que limpiar\n"
            "Los datos reales tienen problemas: celdas vacias, espacios al\n"
            "principio de strings, fechas en formato mixto, numeros guardados\n"
            "como texto, duplicados. La regla general en DS: **70% del tiempo\n"
            "es limpieza, 30% es modelado**. Esta leccion es la caja de\n"
            "herramientas que vas a usar todos los dias.\n\n"
            "## Detectar missing values\n"
            "```python\n"
            "df.isna()           # DataFrame booleano del mismo shape\n"
            "df.isna().sum()     # cuantos NaN por columna\n"
            "df['col'].notna()   # mascara inversa\n"
            "df.isna().any(axis=1).sum()  # cuantas FILAS tienen al menos un NaN\n"
            "```\n"
            "Recorda: en pandas `NaN` vale `float('nan')` y `None` vale\n"
            "`np.nan` cuando entra en una columna numerica. `isna` detecta\n"
            "ambos sin distinguir.\n\n"
            "## fillna — rellenar NaN\n"
            "```python\n"
            "df['edad'].fillna(0)                  # con escalar\n"
            "df['edad'].fillna(df['edad'].mean())  # con la media\n"
            "df['edad'].fillna(method='ffill')     # propaga el ultimo valido\n"
            "df.fillna({'edad': 0, 'plan': 'basico'})  # distinto por columna\n"
            "```\n"
            "**Decisiones de imputacion**:\n"
            "- Numerico no critico: media o mediana.\n"
            "- Series temporales: `ffill` o `bfill`.\n"
            "- Categorico: una categoria nueva tipo `'desconocido'`.\n"
            "- Critico (target del modelo): mejor `dropna`.\n\n"
            "## dropna — eliminar filas/columnas con NaN\n"
            "```python\n"
            "df.dropna()                       # filas con CUALQUIER NaN\n"
            "df.dropna(subset=['edad'])        # solo si 'edad' es NaN\n"
            "df.dropna(axis=1, how='all')      # columnas que son TODAS NaN\n"
            "df.dropna(thresh=3)               # filas con al menos 3 no-NaN\n"
            "```\n\n"
            "## drop_duplicates — quitar filas repetidas\n"
            "```python\n"
            "df.drop_duplicates()                              # filas identicas\n"
            "df.drop_duplicates(subset=['email'])              # por una columna\n"
            "df.drop_duplicates(subset=['id'], keep='last')    # quedate con la ultima\n"
            "```\n"
            "Verifica antes con `df.duplicated().sum()` cuantas hay.\n\n"
            "## astype — convertir tipos\n"
            "```python\n"
            "df['edad'] = df['edad'].astype(int)          # falla si hay NaN\n"
            "df['edad'] = df['edad'].astype('Int64')      # int nullable de pandas\n"
            "df['precio'] = df['precio'].astype(float)\n"
            "df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')\n"
            "```\n"
            "`errors='coerce'` convierte lo que no parsea a NaN en vez de crashear.\n"
            "Util para datasets sucios.\n\n"
            "## El accessor .str — limpiar texto\n"
            "Sobre columnas string, `.str` expone metodos vectorizados:\n"
            "```python\n"
            "df['email'] = df['email'].str.strip().str.lower()\n"
            "df['telefono'] = df['telefono'].str.replace(r'[^0-9]', '', regex=True)\n"
            "df['pais'] = df['pais'].str.title()  # 'argentina' -> 'Argentina'\n"
            "df['valida'] = df['email'].str.contains('@', na=False)\n"
            "```\n"
            "Sin `.str` estarias usando un loop Python sobre cada fila — lento\n"
            "y feo.\n\n"
            "## Errores comunes\n"
            "- Llamar `df.fillna(0)` sobre TODO el DataFrame cuando solo una\n"
            "  columna lo necesita. Eso reemplaza NaN de strings con 0 (string\n"
            "  inconsistente) y oculta problemas en otras columnas. Usa dict.\n"
            "- `df.dropna()` sin `subset=`: borra cualquier fila con UN NaN.\n"
            "  Si tu dataset tiene una columna con muchos NaN no criticos\n"
            "  puede quedarse con cero filas.\n"
            "- `astype(int)` con NaN presente: ValueError. Usar `'Int64'`\n"
            "  (mayuscula) o llenar NaN antes.\n"
            "- Usar `.str` sobre una columna que tiene NaN: la mayoria de\n"
            "  metodos `.str` propagan NaN correctamente, pero `.str.contains`\n"
            "  devuelve NaN como tercer estado. Pasar `na=False`.\n\n"
            "## Resumen\n"
            "- `isna().sum()` te dice donde estan los NaN, columna por columna.\n"
            "- `fillna` decide la estrategia de imputacion; `dropna` borra.\n"
            "- `drop_duplicates(subset=)` quita repetidos por clave.\n"
            "- `astype` + `errors='coerce'` convierte tipos sin crashear.\n"
            "- `.str` aplica metodos de string vectorizados sobre toda la columna.\n"
        ),
        difficulty="intermediate",
        category="pandas",
        order=15,
        track="track-2",
        estimated_duration=55,
        prerequisites_titles=["Pandas: merge, join y fechas"],
        exercises=[
            ExerciseTemplate(
                title="Contar nulos por columna",
                description="Devolver una Serie con la cantidad de NaN por columna.",
                instructions=(
                    "Implementa `nulos_por_columna(df)` que recibe un DataFrame "
                    "y devuelve una Serie indexada por nombre de columna con la "
                    "cantidad de NaN en cada una. Las columnas sin NaN deben "
                    "aparecer con valor 0."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def nulos_por_columna(df: pd.DataFrame) -> pd.Series:\n"
                    "    # TODO: df.isna().sum() devuelve exactamente eso.\n"
                    "    pass\n"
                ),
                hints=[
                    "df.isna() es un DataFrame booleano.",
                    ".sum() por defecto suma por columna (axis=0).",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "es una pandas Series",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({'a':[1,np.nan,3], 'b':[4,5,6]})\n"
                            "out = nulos_por_columna(df)\n"
                            "assert isinstance(out, pd.Series)"
                        ),
                    },
                    {
                        "name": "cuenta los NaN correctamente",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({\n"
                            "    'a':[1,np.nan,3,np.nan],\n"
                            "    'b':[4,5,6,7],\n"
                            "    'c':[np.nan,np.nan,np.nan,1],\n"
                            "})\n"
                            "out = nulos_por_columna(df)\n"
                            "assert out['a'] == 2\n"
                            "assert out['b'] == 0\n"
                            "assert out['c'] == 3"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Rellenar edad con la media",
                description="fillna con la media de la columna, preservando dtype.",
                instructions=(
                    "Implementa `rellenar_edad_con_media(df)` que devuelve una "
                    "copia de df donde los NaN en la columna 'edad' fueron "
                    "reemplazados por la media de 'edad' (calculada sin contar "
                    "los NaN). No modifiques el DataFrame original."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def rellenar_edad_con_media(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: copia, calcula media, fillna en columna edad.\n"
                    "    pass\n"
                ),
                hints=[
                    "df.copy() para no mutar el original.",
                    "media = df['edad'].mean() — pandas ignora NaN automaticamente.",
                    "out['edad'] = out['edad'].fillna(media)",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "no muta el original",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({'edad':[20.0, np.nan, 40.0]})\n"
                            "_ = rellenar_edad_con_media(df)\n"
                            "assert df['edad'].isna().any(), 'no muta el original'"
                        ),
                    },
                    {
                        "name": "rellena con la media correcta",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({'edad':[20.0, np.nan, 40.0]})\n"
                            "out = rellenar_edad_con_media(df)\n"
                            "# media de [20, 40] = 30\n"
                            "assert out['edad'].isna().sum() == 0\n"
                            "assert abs(out['edad'].iloc[1] - 30.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "preserva valores no nulos sin cambios",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({'edad':[25.0, np.nan, 35.0, 45.0]})\n"
                            "out = rellenar_edad_con_media(df)\n"
                            "assert out['edad'].iloc[0] == 25.0\n"
                            "assert out['edad'].iloc[2] == 35.0\n"
                            "assert out['edad'].iloc[3] == 45.0"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Pipeline de limpieza completo",
                description="Strip + lower + drop_duplicates + fillna en una funcion.",
                instructions=(
                    "Implementa `limpiar_clientes(df)` que recibe un DataFrame "
                    "con columnas 'email' (string posiblemente con espacios y "
                    "mayusculas mixtas) y 'edad' (float con NaN). Devuelve una "
                    "copia donde: (1) 'email' fue strip + lower, (2) NaN de "
                    "'edad' rellenados con la mediana, (3) duplicados por "
                    "'email' eliminados (queda la primera ocurrencia)."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def limpiar_clientes(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: copia, .str.strip().str.lower() en email,\n"
                    "    # fillna con mediana de edad, drop_duplicates por email.\n"
                    "    pass\n"
                ),
                hints=[
                    "out['email'] = out['email'].str.strip().str.lower()",
                    "mediana = out['edad'].median()",
                    "out = out.drop_duplicates(subset=['email'])",
                    "El orden de los pasos importa: limpia email ANTES de quitar duplicados.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "no muta el DataFrame original",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({\n"
                            "    'email':['  A@x.com','b@x.com'],\n"
                            "    'edad':[30.0, np.nan],\n"
                            "})\n"
                            "_ = limpiar_clientes(df)\n"
                            "assert df['email'].iloc[0] == '  A@x.com'"
                        ),
                    },
                    {
                        "name": "emails normalizados (strip + lower)",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({\n"
                            "    'email':['  A@x.com','B@X.com '],\n"
                            "    'edad':[30.0, 40.0],\n"
                            "})\n"
                            "out = limpiar_clientes(df)\n"
                            "assert set(out['email']) == {'a@x.com','b@x.com'}"
                        ),
                    },
                    {
                        "name": "edad rellenada con mediana",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({\n"
                            "    'email':['a@x.com','b@x.com','c@x.com'],\n"
                            "    'edad':[20.0, np.nan, 40.0],\n"
                            "})\n"
                            "out = limpiar_clientes(df)\n"
                            "# mediana de [20, 40] = 30\n"
                            "assert out['edad'].isna().sum() == 0\n"
                            "assert 30.0 in out['edad'].tolist()"
                        ),
                    },
                    {
                        "name": "duplicados por email eliminados despues de normalizar",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({\n"
                            "    'email':['A@x.com','a@x.com  ','b@x.com'],\n"
                            "    'edad':[30.0, 35.0, 40.0],\n"
                            "})\n"
                            "out = limpiar_clientes(df)\n"
                            "assert len(out) == 2\n"
                            "assert set(out['email']) == {'a@x.com','b@x.com'}"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Visualizacion 1: matplotlib esencial",
        description="Histograma, scatter, lineas y bar charts con matplotlib. Decidir que tipo de plot usar segun la pregunta que quieres responder.",
        content=(
            "## Que es matplotlib\n"
            "matplotlib es la libreria base de visualizacion en Python. Casi\n"
            "todas las demas (seaborn, pandas.plot, plotly Express) la usan\n"
            "por dentro o la imitan. Dominar la API te da control total.\n\n"
            "En PyCode, cuando llames `plt.show()` el plot aparece inline\n"
            "en el panel de salida del editor — el worker captura la figura\n"
            "como PNG y la renderiza ahi mismo.\n\n"
            "## La estructura: Figure y Axes\n"
            "```python\n"
            "import matplotlib.pyplot as plt\n\n"
            "fig, ax = plt.subplots()       # crea figura + 1 eje\n"
            "ax.plot([1, 2, 3], [10, 20, 15])\n"
            "ax.set_title('Demo')\n"
            "ax.set_xlabel('x'); ax.set_ylabel('y')\n"
            "plt.show()\n"
            "```\n"
            "`Figure` es el lienzo. `Axes` es donde dibujas. Una figura puede\n"
            "tener varios axes (subplots). El API tiene dos modos:\n"
            "- **Funcional**: `plt.plot`, `plt.title`, `plt.show` (mas corto,\n"
            "  bueno para exploracion).\n"
            "- **Orientado a objetos**: `ax.plot`, `ax.set_title` (mas explicito,\n"
            "  necesario cuando hay multiples subplots).\n\n"
            "## Cuatro plots que cubren el 80% de los casos\n\n"
            "### 1. Linea — evolucion temporal\n"
            "```python\n"
            "plt.plot(fechas, ventas, marker='o')\n"
            "```\n"
            "Pregunta: '¿como cambia X a lo largo del tiempo?'.\n\n"
            "### 2. Scatter — relacion entre dos variables\n"
            "```python\n"
            "plt.scatter(altura, peso, alpha=0.6)\n"
            "```\n"
            "Pregunta: '¿hay correlacion entre X e Y?'. `alpha` evita que los\n"
            "puntos densos tapen lo que hay debajo.\n\n"
            "### 3. Histograma — distribucion de una variable\n"
            "```python\n"
            "plt.hist(notas, bins=10)\n"
            "```\n"
            "Pregunta: '¿como se distribuyen los valores de X? ¿hay outliers?'.\n"
            "Mas bins = mas detalle pero mas ruido.\n\n"
            "### 4. Barra — comparar categorias\n"
            "```python\n"
            "plt.bar(['cafe','te','torta'], [120, 80, 95])\n"
            "```\n"
            "Pregunta: '¿que categoria tiene mas X?'. Cuidado: no uses barras\n"
            "para variables continuas (eso es histograma).\n\n"
            "## Decorar el plot\n"
            "```python\n"
            "plt.title('Notas del trimestre')\n"
            "plt.xlabel('Estudiante'); plt.ylabel('Nota')\n"
            "plt.grid(True, alpha=0.3)\n"
            "plt.legend(['mate', 'lengua'])\n"
            "plt.tight_layout()  # evita que las labels se corten\n"
            "```\n\n"
            "## Multiples plots en una figura (subplots)\n"
            "```python\n"
            "fig, axes = plt.subplots(1, 2, figsize=(10, 4))\n"
            "axes[0].hist(notas_mate, bins=10); axes[0].set_title('Mate')\n"
            "axes[1].hist(notas_leng, bins=10); axes[1].set_title('Lengua')\n"
            "plt.tight_layout()\n"
            "plt.show()\n"
            "```\n\n"
            "## Plot directo desde pandas\n"
            "Series y DataFrame tienen `.plot()` que delega a matplotlib:\n"
            "```python\n"
            "df['ingreso'].plot(kind='line')\n"
            "df['ingreso'].plot(kind='hist', bins=20)\n"
            "df.plot.scatter(x='altura', y='peso')\n"
            "```\n"
            "Para algo rapido es ideal. Para control fino vuelve a `ax.plot`.\n\n"
            "## Errores comunes\n"
            "- Olvidar `plt.show()`: en PyCode el plot no aparece. En un\n"
            "  notebook Jupyter se muestra solo, pero aca explicitamente lo\n"
            "  necesitas para emitir el PNG.\n"
            "- Mezclar modo funcional con orientado a objetos en el mismo plot:\n"
            "  decidi uno y manteneo. Si usas `subplots`, casi obligatorio el\n"
            "  modo OO.\n"
            "- Hacer barras con muchas categorias (>15): se vuelve ilegible.\n"
            "  Mejor un horizontal bar (`plt.barh`) o un boxplot.\n"
            "- Usar `bins=` muy grande en histograma con pocos datos: cada bin\n"
            "  tiene 1-2 valores y el histograma se ve como ruido.\n\n"
            "## Resumen\n"
            "- 4 plots cubren el 80%: linea (tiempo), scatter (correlacion),\n"
            "  histograma (distribucion), barra (categorias).\n"
            "- API funcional para algo rapido; OO para subplots o control fino.\n"
            "- Siempre `plt.title`, `xlabel`, `ylabel`. Un plot sin etiquetas\n"
            "  es invendible.\n"
            "- `plt.show()` para emitir el PNG en PyCode.\n"
        ),
        difficulty="intermediate",
        category="visualizacion",
        order=16,
        track="track-2",
        estimated_duration=50,
        prerequisites_titles=["Pandas: limpieza de datos y missing values"],
        exercises=[
            ExerciseTemplate(
                title="Histograma de notas",
                description="Plot de distribucion con plt.hist.",
                instructions=(
                    "Implementa `plot_hist_notas(notas)` que recibe una lista o "
                    "Serie de notas, dibuja un histograma con 10 bins, agrega "
                    "titulo 'Distribucion de notas' y label de eje y 'Frecuencia'. "
                    "La funcion debe devolver el objeto Axes que uso para que "
                    "podamos verificar el plot."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_hist_notas(notas):\n"
                    "    # TODO: fig, ax = plt.subplots(); ax.hist(...); ax.set_title(...)\n"
                    "    # return ax\n"
                    "    pass\n"
                ),
                hints=[
                    "fig, ax = plt.subplots(); luego ax.hist(notas, bins=10).",
                    "ax.set_title('Distribucion de notas'); ax.set_ylabel('Frecuencia').",
                    "Devolve ax al final para que los tests puedan inspeccionar el plot.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve un objeto Axes de matplotlib",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_hist_notas([3.0, 4.0, 4.5, 5.0, 2.5, 3.5])\n"
                            "assert hasattr(ax, 'patches'), 'debe devolver un Axes'\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "tiene 10 bins",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_hist_notas([3.0, 4.0, 4.5, 5.0, 2.5, 3.5])\n"
                            "assert len(ax.patches) == 10\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "tiene titulo y label correctos",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_hist_notas([3.0, 4.0, 4.5, 5.0, 2.5, 3.5])\n"
                            "assert 'distribucion' in ax.get_title().lower()\n"
                            "assert 'frecuencia' in ax.get_ylabel().lower()\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Bar chart de ventas por sucursal",
                description="Agregar con groupby y graficar con plt.bar.",
                instructions=(
                    "Implementa `plot_ventas_por_sucursal(df)` que recibe un "
                    "DataFrame con columnas 'sucursal' e 'ingreso', calcula la "
                    "suma de ingresos por sucursal con groupby, y dibuja un bar "
                    "chart con esas sucursales en el eje X. Devuelve el Axes."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_ventas_por_sucursal(df):\n"
                    "    # TODO: groupby + ax.bar(sucursales, totales)\n"
                    "    pass\n"
                ),
                hints=[
                    "totales = df.groupby('sucursal')['ingreso'].sum()",
                    "ax.bar(totales.index, totales.values) usa el indice como categorias.",
                    "Las series de pandas tienen .plot(kind='bar', ax=ax) tambien.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "devuelve un Axes con barras",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','n','sur'],\n"
                            "    'ingreso':[100,50,80,20,60],\n"
                            "})\n"
                            "ax = plot_ventas_por_sucursal(df)\n"
                            "assert hasattr(ax, 'patches')\n"
                            "assert len(ax.patches) == 3, '3 sucursales = 3 barras'\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "alturas corresponden a las sumas",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','n','sur'],\n"
                            "    'ingreso':[100,50,80,20,60],\n"
                            "})\n"
                            "ax = plot_ventas_por_sucursal(df)\n"
                            "alturas = sorted(p.get_height() for p in ax.patches)\n"
                            "# centro=150, norte=100, sur=60\n"
                            "assert alturas == [60.0, 100.0, 150.0]\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Scatter coloreado por categoria",
                description="Scatter con un color por especie usando un loop sobre groupby.",
                instructions=(
                    "Implementa `plot_iris_scatter(df)` que recibe un DataFrame "
                    "con columnas 'sepal_length', 'petal_length' y 'species'. "
                    "Dibuja un scatter con sepal_length en X, petal_length en Y, "
                    "y un color distinto por especie usando groupby + ax.scatter "
                    "en un loop. Agrega legend con los nombres de especies. "
                    "Devuelve el Axes."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_iris_scatter(df):\n"
                    "    # TODO: fig, ax = plt.subplots()\n"
                    "    # for nombre, grupo in df.groupby('species'):\n"
                    "    #     ax.scatter(grupo['sepal_length'], grupo['petal_length'], label=nombre)\n"
                    "    # ax.legend(); return ax\n"
                    "    pass\n"
                ),
                hints=[
                    "df.groupby('species') itera devolviendo (nombre, sub_df).",
                    "ax.scatter(..., label=nombre) prepara la leyenda; ax.legend() la dibuja.",
                    "matplotlib elige los colores automaticamente al haber multiples llamadas a scatter.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "devuelve un Axes",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sepal_length':[5.1, 5.5, 6.3, 6.5, 7.0, 6.7],\n"
                            "    'petal_length':[1.4, 4.0, 6.0, 4.5, 4.7, 5.8],\n"
                            "    'species':['setosa','versicolor','virginica','versicolor','versicolor','virginica'],\n"
                            "})\n"
                            "ax = plot_iris_scatter(df)\n"
                            "assert hasattr(ax, 'collections')\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "3 grupos = 3 colecciones de puntos",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sepal_length':[5.1, 5.5, 6.3, 6.5, 7.0, 6.7],\n"
                            "    'petal_length':[1.4, 4.0, 6.0, 4.5, 4.7, 5.8],\n"
                            "    'species':['setosa','versicolor','virginica','versicolor','versicolor','virginica'],\n"
                            "})\n"
                            "ax = plot_iris_scatter(df)\n"
                            "# Cada ax.scatter(...) crea una PathCollection\n"
                            "assert len(ax.collections) == 3, '3 especies = 3 scatter calls'\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "tiene legend con las 3 especies",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sepal_length':[5.1, 5.5, 6.3, 6.5, 7.0, 6.7],\n"
                            "    'petal_length':[1.4, 4.0, 6.0, 4.5, 4.7, 5.8],\n"
                            "    'species':['setosa','versicolor','virginica','versicolor','versicolor','virginica'],\n"
                            "})\n"
                            "ax = plot_iris_scatter(df)\n"
                            "leg = ax.get_legend()\n"
                            "assert leg is not None, 'falta legend'\n"
                            "labels = {t.get_text() for t in leg.get_texts()}\n"
                            "assert labels == {'setosa','versicolor','virginica'}\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Visualizacion 2: subplots, estilos y anotaciones",
        description="Layouts con multiples axes, ejes compartidos, dual y-axis con twinx, estilos globales, y anotaciones sobre el plot.",
        content=(
            "## Cuando un plot no alcanza\n"
            "Muchos analisis requieren comparar **distribuciones lado a lado**\n"
            "o ver **dos variables con escalas distintas** en el mismo grafico.\n"
            "matplotlib resuelve los dos con la misma idea: combinar Axes.\n\n"
            "## subplots — grid de plots\n"
            "```python\n"
            "import matplotlib.pyplot as plt\n\n"
            "fig, axes = plt.subplots(2, 2, figsize=(10, 8))\n"
            "axes[0, 0].plot(x1, y1)\n"
            "axes[0, 1].scatter(x2, y2)\n"
            "axes[1, 0].hist(z1, bins=20)\n"
            "axes[1, 1].bar(cat, vals)\n"
            "plt.tight_layout()\n"
            "plt.show()\n"
            "```\n"
            "`axes` es un array 2D — accedelo con `axes[fila, columna]`. Si\n"
            "solo hay una fila o columna, es 1D.\n\n"
            "## Compartir ejes — sharex / sharey\n"
            "Cuando comparas series temporales o distribuciones con la misma\n"
            "escala, compartir ejes evita ambiguedad visual:\n"
            "```python\n"
            "fig, axes = plt.subplots(2, 1, sharex=True, figsize=(8, 6))\n"
            "axes[0].plot(fechas, ventas_a); axes[0].set_title('Sucursal A')\n"
            "axes[1].plot(fechas, ventas_b); axes[1].set_title('Sucursal B')\n"
            "```\n"
            "Hacer zoom en uno ajusta el otro. El xlabel solo aparece en el de\n"
            "abajo automaticamente.\n\n"
            "## twinx — dos escalas en Y\n"
            "Cuando dos variables con unidades muy distintas (ventas en pesos\n"
            "vs unidades vendidas) viven en el mismo plot:\n"
            "```python\n"
            "fig, ax1 = plt.subplots()\n"
            "ax1.plot(fechas, ingresos, color='tab:blue', label='ingresos')\n"
            "ax1.set_ylabel('Ingresos $', color='tab:blue')\n\n"
            "ax2 = ax1.twinx()  # eje Y derecho compartiendo X\n"
            "ax2.plot(fechas, unidades, color='tab:orange', label='unidades')\n"
            "ax2.set_ylabel('Unidades', color='tab:orange')\n"
            "```\n"
            "**Cuidado**: twinx puede engaiar visualmente porque la escala\n"
            "doble esconde correlaciones reales. Usar con criterio y siempre\n"
            "con ejes coloreados a juego.\n\n"
            "## Estilos globales — plt.style.use\n"
            "Cambia el look de todos los plots con una linea:\n"
            "```python\n"
            "plt.style.use('seaborn-v0_8-darkgrid')  # fondo gris con grid\n"
            "plt.style.use('ggplot')                  # estilo R/ggplot2\n"
            "plt.style.use('default')                 # vuelve al default\n"
            "```\n"
            "Lista los disponibles con `plt.style.available`. Para presentaciones,\n"
            "`seaborn-v0_8-whitegrid` queda profesional.\n\n"
            "## Anotaciones — ax.annotate / ax.text\n"
            "Apuntar a un valor especifico vale mas que mil ejes:\n"
            "```python\n"
            "max_val = vals.max()\n"
            "idx_max = vals.argmax()\n"
            "ax.annotate(\n"
            "    f'Pico: {max_val}',\n"
            "    xy=(idx_max, max_val),       # punto donde apunta\n"
            "    xytext=(idx_max + 1, max_val + 5),  # donde va el texto\n"
            "    arrowprops={'arrowstyle': '->'},\n"
            ")\n"
            "```\n"
            "Para textos sin flecha: `ax.text(x, y, 'mensaje', fontsize=10)`.\n\n"
            "## Anotar valores sobre cada barra\n"
            "Pattern util para bar charts ejecutivos:\n"
            "```python\n"
            "bars = ax.bar(categorias, valores)\n"
            "for bar in bars:\n"
            "    h = bar.get_height()\n"
            "    ax.text(bar.get_x() + bar.get_width()/2, h + 0.5,\n"
            "            f'{h:.0f}', ha='center', va='bottom')\n"
            "```\n\n"
            "## Errores comunes\n"
            "- `subplots(1, 2)` devuelve `axes` como ARRAY 1D, no matriz 2D.\n"
            "  Indexalo `axes[0]`, no `axes[0, 0]` — el segundo da IndexError.\n"
            "- Olvidar `plt.tight_layout()` cuando los titulos se solapan o\n"
            "  los labels se cortan en la imagen final.\n"
            "- Usar twinx para variables que SI tienen la misma escala — confunde\n"
            "  al lector. Si comparten unidad, mejor ponelas en el mismo eje.\n"
            "- Aplicar `plt.style.use` despues de crear los axes: no afecta\n"
            "  retroactivamente. Llamalo al inicio del script o celda.\n\n"
            "## Resumen\n"
            "- `subplots(filas, cols)` crea un grid de Axes. 2D si filas y cols > 1.\n"
            "- `sharex`/`sharey` sincronizan ejes cuando compares lo mismo.\n"
            "- `twinx` agrega un eje Y derecho — usar con cuidado.\n"
            "- `plt.style.use` cambia look global; `ax.annotate` para anotaciones\n"
            "  apuntadas; `ax.text` para texto libre.\n"
        ),
        difficulty="intermediate",
        category="visualizacion",
        order=17,
        track="track-2",
        estimated_duration=45,
        prerequisites_titles=["Visualizacion 1: matplotlib esencial"],
        exercises=[
            ExerciseTemplate(
                title="2x1 subplots con eje X compartido",
                description="Dos plots verticales que comparten el eje X.",
                instructions=(
                    "Implementa `plot_dos_series(x, y1, y2)` que crea una figura "
                    "con 2 axes apilados verticalmente (2 filas, 1 columna) "
                    "compartiendo el eje X. En el de arriba grafica (x, y1) y en "
                    "el de abajo (x, y2). Devuelve la tupla (fig, axes)."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_dos_series(x, y1, y2):\n"
                    "    # TODO: plt.subplots(2, 1, sharex=True)\n"
                    "    pass\n"
                ),
                hints=[
                    "fig, axes = plt.subplots(2, 1, sharex=True)",
                    "axes[0].plot(x, y1) — axes es array 1D porque hay una sola columna.",
                    "Devolve (fig, axes).",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve fig y array de 2 axes",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, axes = plot_dos_series([1,2,3], [4,5,6], [10,20,30])\n"
                            "assert fig is not None\n"
                            "assert len(axes) == 2\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "ambos axes tienen una linea cada uno",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, axes = plot_dos_series([1,2,3], [4,5,6], [10,20,30])\n"
                            "assert len(axes[0].lines) == 1\n"
                            "assert len(axes[1].lines) == 1\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "comparten el eje X (sharex)",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, axes = plot_dos_series([1,2,3], [4,5,6], [10,20,30])\n"
                            "# Cuando sharex=True, los Axes apuntan a la misma instancia de eje X.\n"
                            "assert axes[0].get_shared_x_axes().joined(axes[0], axes[1])\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Bar chart con valores anotados",
                description="Bar con texto encima de cada barra mostrando el valor.",
                instructions=(
                    "Implementa `plot_bar_con_valores(categorias, valores)` que "
                    "dibuja un bar chart y agrega texto centrado encima de cada "
                    "barra con el valor numerico (formato entero). Devuelve el "
                    "Axes."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_bar_con_valores(categorias, valores):\n"
                    "    # TODO: fig, ax = plt.subplots(); bars = ax.bar(...)\n"
                    "    # for bar in bars:\n"
                    "    #     h = bar.get_height()\n"
                    "    #     ax.text(bar.get_x() + bar.get_width()/2, h, f'{h:.0f}',\n"
                    "    #             ha='center', va='bottom')\n"
                    "    pass\n"
                ),
                hints=[
                    "ax.bar devuelve un BarContainer iterable de Rectangulos.",
                    "bar.get_x() + bar.get_width()/2 da la X central de la barra.",
                    "ha='center' centra horizontalmente el texto.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "tiene tantas barras como categorias",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_bar_con_valores(['a','b','c'], [10, 20, 15])\n"
                            "assert len(ax.patches) == 3\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "hay 3 textos (uno por barra)",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_bar_con_valores(['a','b','c'], [10, 20, 15])\n"
                            "textos = [t.get_text() for t in ax.texts]\n"
                            "assert len(textos) == 3\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "los textos muestran los valores correctos",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_bar_con_valores(['a','b','c'], [10, 20, 15])\n"
                            "textos = sorted(int(t.get_text()) for t in ax.texts)\n"
                            "assert textos == [10, 15, 20]\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Dual y-axis: ingresos vs unidades",
                description="Mismo X (tiempo), dos escalas Y (ingresos $ y unidades).",
                instructions=(
                    "Implementa `plot_dual_y(fechas, ingresos, unidades)` que "
                    "crea una figura con un Axes principal (ax1) graficando "
                    "(fechas, ingresos) y un Axes secundario via twinx (ax2) "
                    "graficando (fechas, unidades). Cada eje Y debe tener un "
                    "label distinto: 'Ingresos' y 'Unidades'. Devuelve "
                    "(fig, ax1, ax2)."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_dual_y(fechas, ingresos, unidades):\n"
                    "    # TODO: fig, ax1 = plt.subplots()\n"
                    "    # ax1.plot(fechas, ingresos); ax1.set_ylabel('Ingresos')\n"
                    "    # ax2 = ax1.twinx(); ax2.plot(...); ax2.set_ylabel('Unidades')\n"
                    "    pass\n"
                ),
                hints=[
                    "ax1.twinx() devuelve un nuevo Axes que comparte X con ax1.",
                    "Cada axes mantiene sus propias lineas y label de Y.",
                    "Devolve la tupla (fig, ax1, ax2) en ese orden.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "devuelve fig, ax1, ax2",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, ax1, ax2 = plot_dual_y([1,2,3], [100,150,200], [10,12,15])\n"
                            "assert fig is not None and ax1 is not None and ax2 is not None\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "cada axes tiene su linea",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, ax1, ax2 = plot_dual_y([1,2,3], [100,150,200], [10,12,15])\n"
                            "assert len(ax1.lines) == 1\n"
                            "assert len(ax2.lines) == 1\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "ylabels son 'Ingresos' y 'Unidades'",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, ax1, ax2 = plot_dual_y([1,2,3], [100,150,200], [10,12,15])\n"
                            "assert ax1.get_ylabel() == 'Ingresos'\n"
                            "assert ax2.get_ylabel() == 'Unidades'\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "ax2 comparte el eje X con ax1 (twinx)",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, ax1, ax2 = plot_dual_y([1,2,3], [100,150,200], [10,12,15])\n"
                            "# twinx comparte el eje X\n"
                            "assert ax1.get_shared_x_axes().joined(ax1, ax2)\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="EDA: exploracion sistematica de un dataset",
        description="Pipeline reproducible para entender un dataset nuevo: shape/info/describe, distribuciones, outliers via IQR, correlaciones bivariadas.",
        content=(
            "## Que es EDA\n"
            "**Exploratory Data Analysis** es la fase de investigacion previa\n"
            "al modelado. El objetivo es responder cinco preguntas antes de\n"
            "entrenar nada:\n"
            "1. ¿Cuantas filas y columnas hay?\n"
            "2. ¿Que tipo es cada columna y cuantos NaN?\n"
            "3. ¿Como se distribuye cada variable?\n"
            "4. ¿Hay outliers? ¿Son errores o casos reales?\n"
            "5. ¿Que variables estan relacionadas entre si?\n\n"
            "Cuanto mejor hagas EDA, menos sorpresas en produccion.\n\n"
            "## Pipeline en cinco lineas\n"
            "```python\n"
            "df.shape       # 1. tamano\n"
            "df.info()      # 2. dtypes + nulos por columna\n"
            "df.head(5)     # primeras filas para sanity check\n"
            "df.describe()  # 3. distribucion (count/mean/std/min/quartiles/max)\n"
            "df.duplicated().sum()  # ¿hay filas repetidas?\n"
            "```\n"
            "Esto te da el 70% de la radiografia. Si algo te llama la atencion\n"
            "(una columna con 80% NaN, un max absurdo), profundizas ahi.\n\n"
            "## Distribuciones — histogramas y boxplots\n"
            "Para variables numericas:\n"
            "```python\n"
            "df['edad'].hist(bins=20)        # forma de la distribucion\n"
            "df.boxplot(column='edad')       # outliers visibles como puntos\n"
            "```\n"
            "El **boxplot** es perfecto para detectar outliers: la caja es Q1-Q3,\n"
            "la linea del medio es la mediana, los 'bigotes' van hasta 1.5*IQR,\n"
            "y los puntos fuera son candidatos a outlier.\n\n"
            "Para variables categoricas:\n"
            "```python\n"
            "df['pais'].value_counts()\n"
            "df['pais'].value_counts(normalize=True)  # porcentajes\n"
            "```\n\n"
            "## Detectar outliers con IQR\n"
            "La regla **1.5 * IQR** es el clasico:\n"
            "```python\n"
            "q1 = df['precio'].quantile(0.25)\n"
            "q3 = df['precio'].quantile(0.75)\n"
            "iqr = q3 - q1\n"
            "bajos = df['precio'] < q1 - 1.5 * iqr\n"
            "altos = df['precio'] > q3 + 1.5 * iqr\n"
            "outliers = df[bajos | altos]\n"
            "```\n"
            "Recordatorio importante: **no eliminar outliers automaticamente**.\n"
            "Algunas veces son los casos mas interesantes (fraude, errores de\n"
            "captura, segmentos especiales). Investigarlos primero.\n\n"
            "## Correlaciones — variables que se mueven juntas\n"
            "```python\n"
            "df.corr(numeric_only=True)\n"
            "```\n"
            "Devuelve una matriz simetrica con coeficientes de Pearson\n"
            "(-1 a +1):\n"
            "- **+1**: cuando una sube, la otra sube en la misma proporcion.\n"
            "- **0**: no hay relacion lineal.\n"
            "- **-1**: cuando una sube, la otra baja en la misma proporcion.\n\n"
            "Cuidado: Pearson solo captura relaciones **lineales**. Una relacion\n"
            "cuadratica puede dar correlacion casi cero y aun ser fuerte.\n\n"
            "Para visualizar la matriz, un heatmap:\n"
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "fig, ax = plt.subplots()\n"
            "im = ax.imshow(df.corr(numeric_only=True), cmap='coolwarm', vmin=-1, vmax=1)\n"
            "plt.colorbar(im)\n"
            "```\n\n"
            "## Crosstab — relacion entre categoricas\n"
            "```python\n"
            "pd.crosstab(df['pais'], df['plan'])\n"
            "pd.crosstab(df['pais'], df['plan'], normalize='index')  # % por fila\n"
            "```\n\n"
            "## Errores comunes\n"
            "- Saltarse el EDA por apuro: terminas entrenando con NaN, leaks\n"
            "  o columnas inutiles. **30 minutos de EDA ahorran horas de debug**.\n"
            "- Tirar outliers sin investigarlos: muchas veces son el problema\n"
            "  que queres modelar.\n"
            "- Interpretar correlacion como causalidad. Una correlacion alta\n"
            "  entre 'ventas de helado' y 'ahogamientos' no significa que el\n"
            "  helado cause ahogamientos (hay una variable de confusion: verano).\n"
            "- Olvidar `numeric_only=True` en `df.corr()`: en pandas modernos\n"
            "  esto avisa con un FutureWarning porque las columnas string no\n"
            "  tienen correlacion definida.\n\n"
            "## Resumen\n"
            "- EDA responde 5 preguntas antes de modelar.\n"
            "- 5 lineas (shape/info/head/describe/duplicated) dan el 70% del\n"
            "  panorama.\n"
            "- Histogramas para forma de distribucion, boxplots para outliers,\n"
            "  IQR como regla numerica.\n"
            "- `.corr(numeric_only=True)` para correlaciones; crosstab para\n"
            "  categoricas.\n"
            "- Correlacion no implica causalidad.\n"
        ),
        difficulty="intermediate",
        category="eda",
        order=18,
        track="track-2",
        estimated_duration=55,
        prerequisites_titles=["Visualizacion 2: subplots, estilos y anotaciones"],
        exercises=[
            ExerciseTemplate(
                title="Resumen estadistico de columnas numericas",
                description="Filtrar las columnas numericas y devolver describe().",
                instructions=(
                    "Implementa `resumen_numerico(df)` que devuelve el DataFrame "
                    "resultado de aplicar describe() SOLO a las columnas numericas. "
                    "Si una columna es de tipo object o categorico, excluirla. "
                    "Usa select_dtypes."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def resumen_numerico(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: df.select_dtypes(include='number').describe()\n"
                    "    pass\n"
                ),
                hints=[
                    "df.select_dtypes(include='number') filtra columnas numericas.",
                    "Sobre el resultado, .describe() devuelve el resumen estadistico.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "es un DataFrame",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'a':[1.0,2.0,3.0],\n"
                            "    'b':[10,20,30],\n"
                            "    'c':['x','y','z'],\n"
                            "})\n"
                            "out = resumen_numerico(df)\n"
                            "assert isinstance(out, pd.DataFrame)"
                        ),
                    },
                    {
                        "name": "excluye columnas no numericas",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'a':[1.0,2.0,3.0],\n"
                            "    'b':[10,20,30],\n"
                            "    'c':['x','y','z'],\n"
                            "})\n"
                            "out = resumen_numerico(df)\n"
                            "assert 'c' not in out.columns\n"
                            "assert set(out.columns) == {'a','b'}"
                        ),
                    },
                    {
                        "name": "incluye las metricas tipicas de describe",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'a':[1.0,2.0,3.0]})\n"
                            "out = resumen_numerico(df)\n"
                            "for metric in ['mean','std','min','25%','50%','75%','max']:\n"
                            "    assert metric in out.index"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Detectar outliers con regla IQR",
                description="Devolver las filas con valores fuera de Q1-1.5IQR / Q3+1.5IQR.",
                instructions=(
                    "Implementa `outliers_iqr(df, columna)` que recibe un "
                    "DataFrame y el nombre de una columna numerica. Calcula "
                    "Q1, Q3 y IQR. Devuelve el subset de filas cuyo valor en "
                    "esa columna es < Q1 - 1.5*IQR o > Q3 + 1.5*IQR."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def outliers_iqr(df: pd.DataFrame, columna: str) -> pd.DataFrame:\n"
                    "    # TODO: q1, q3 = quantile(0.25), quantile(0.75); iqr = q3-q1\n"
                    "    # mascara = (df[columna] < q1 - 1.5*iqr) | (df[columna] > q3 + 1.5*iqr)\n"
                    "    pass\n"
                ),
                hints=[
                    "df[columna].quantile(0.25) da el Q1 ignorando NaN.",
                    "Combina las dos condiciones con | (or bit a bit) y parentesis.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "devuelve DataFrame",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10,12,11,13,12,500]})\n"
                            "out = outliers_iqr(df, 'precio')\n"
                            "assert isinstance(out, pd.DataFrame)"
                        ),
                    },
                    {
                        "name": "detecta outlier alto evidente",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10,12,11,13,12,500]})\n"
                            "out = outliers_iqr(df, 'precio')\n"
                            "assert 500 in out['precio'].tolist()"
                        ),
                    },
                    {
                        "name": "no marca filas en rango normal",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10,12,11,13,12,500]})\n"
                            "out = outliers_iqr(df, 'precio')\n"
                            "# Los valores 10-13 NO deben aparecer como outliers\n"
                            "assert 11 not in out['precio'].tolist()\n"
                            "assert 12 not in out['precio'].tolist()"
                        ),
                    },
                    {
                        "name": "detecta outlier bajo extremo",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[100, 102, 101, 99, 100, -50]})\n"
                            "out = outliers_iqr(df, 'precio')\n"
                            "assert -50 in out['precio'].tolist()"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Par mas correlacionado",
                description="Encontrar las dos columnas con mayor correlacion absoluta.",
                instructions=(
                    "Implementa `par_mas_correlacionado(df)` que calcula la "
                    "matriz de correlacion entre columnas numericas y devuelve "
                    "una tupla (col_a, col_b, correlacion) con las dos columnas "
                    "DISTINTAS que tienen la mayor correlacion absoluta. "
                    "(col_a, col_b) ordenadas alfabeticamente."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def par_mas_correlacionado(df: pd.DataFrame) -> tuple:\n"
                    "    # TODO: corr = df.corr(numeric_only=True)\n"
                    "    # Ignorar la diagonal (col consigo misma = 1).\n"
                    "    # Encontrar el max de |corr| en off-diagonal.\n"
                    "    pass\n"
                ),
                hints=[
                    "corr.abs() te da magnitudes sin signo.",
                    "Para evitar la diagonal: mascara `corr.values[i, i] = 0` o usar `corr.where(...)`.",
                    "Una vez encontradas col_a y col_b, devolve `(a, b, corr.loc[a, b])` con a, b ordenados.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "devuelve una tupla de 3 elementos",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "x = rng.normal(size=100)\n"
                            "df = pd.DataFrame({\n"
                            "    'a': x,\n"
                            "    'b': 2*x + rng.normal(scale=0.1, size=100),  # casi perfecta\n"
                            "    'c': rng.normal(size=100),  # ruido\n"
                            "})\n"
                            "out = par_mas_correlacionado(df)\n"
                            "assert isinstance(out, tuple) and len(out) == 3"
                        ),
                    },
                    {
                        "name": "identifica el par mas correlacionado correcto",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "x = rng.normal(size=100)\n"
                            "df = pd.DataFrame({\n"
                            "    'a': x,\n"
                            "    'b': 2*x + rng.normal(scale=0.1, size=100),\n"
                            "    'c': rng.normal(size=100),\n"
                            "})\n"
                            "out = par_mas_correlacionado(df)\n"
                            "assert set(out[:2]) == {'a','b'}"
                        ),
                    },
                    {
                        "name": "ordena el par alfabeticamente",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "x = rng.normal(size=100)\n"
                            "df = pd.DataFrame({\n"
                            "    'zeta': x,\n"
                            "    'alpha': 2*x + rng.normal(scale=0.1, size=100),\n"
                            "    'beta': rng.normal(size=100),\n"
                            "})\n"
                            "out = par_mas_correlacionado(df)\n"
                            "assert out[0] < out[1], 'columnas no estan ordenadas'\n"
                            "assert out[0] == 'alpha' and out[1] == 'zeta'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="EDA 2: feature engineering basico",
        description="Codificar categoricas con one-hot, agrupar continuas en bins, y normalizar variables para que un modelo las trate por igual.",
        content=(
            "## Por que feature engineering\n"
            "Los modelos de ML no entienden 'Argentina' ni 'plan premium': solo\n"
            "numeros. Y dentro de los numeros tampoco les es indiferente que\n"
            "una variable este en miles y otra en decimales — los algoritmos\n"
            "basados en distancia (kNN, SVM, redes) se van a quedar mirando\n"
            "solo la variable de mayor escala.\n\n"
            "Feature engineering es **transformar las columnas crudas en algo\n"
            "que el modelo pueda usar**. En esta leccion: encoding, binning y\n"
            "normalizacion.\n\n"
            "## One-hot encoding — categorias a columnas binarias\n"
            "```python\n"
            "import pandas as pd\n\n"
            "df = pd.DataFrame({'pais': ['AR','MX','AR','CO']})\n"
            "dummies = pd.get_dummies(df['pais'])\n"
            "#    AR     CO     MX\n"
            "# 0   1      0      0\n"
            "# 1   0      0      1\n"
            "# 2   1      0      0\n"
            "# 3   0      1      0\n"
            "```\n"
            "Cada categoria pasa a una columna binaria (0/1). Para integrar al\n"
            "DataFrame original, `pd.get_dummies(df, columns=['pais'])` lo hace\n"
            "directo y agrega las dummies en lugar de la columna original.\n\n"
            "**`drop_first=True`** quita la primera categoria para evitar\n"
            "multicolinealidad (importante para regresion lineal):\n"
            "```python\n"
            "pd.get_dummies(df['pais'], drop_first=True)  # 2 columnas en vez de 3\n"
            "```\n\n"
            "## Label encoding — orden manual\n"
            "Cuando hay orden natural (ordinal), no uses one-hot — perdes la\n"
            "informacion del orden. Mapea a numeros con `map`:\n"
            "```python\n"
            "orden_plan = {'basico': 0, 'pro': 1, 'enterprise': 2}\n"
            "df['plan_num'] = df['plan'].map(orden_plan)\n"
            "```\n\n"
            "## Binning — convertir continuo en categorico\n"
            "Para histogramas, segmentar usuarios o variables 'edad → grupo etario':\n\n"
            "**`pd.cut`** con limites definidos:\n"
            "```python\n"
            "rangos = [0, 18, 30, 50, 100]\n"
            "labels = ['menor', 'joven', 'adulto', 'mayor']\n"
            "df['grupo'] = pd.cut(df['edad'], bins=rangos, labels=labels)\n"
            "```\n\n"
            "**`pd.qcut`** con cuantiles (cada bin tiene la misma cantidad de\n"
            "puntos):\n"
            "```python\n"
            "df['quintil'] = pd.qcut(df['ingreso'], q=5, labels=['Q1','Q2','Q3','Q4','Q5'])\n"
            "```\n"
            "`qcut` es ideal cuando los datos estan sesgados (long tail): los\n"
            "limites se adaptan a la distribucion.\n\n"
            "## Transformaciones — comprimir/expandir escalas\n"
            "Si una variable es muy sesgada hacia la derecha (precios, ingresos),\n"
            "el log la simetriza:\n"
            "```python\n"
            "import numpy as np\n"
            "df['log_precio'] = np.log1p(df['precio'])  # log(1 + x), maneja 0\n"
            "```\n"
            "`log1p` se usa en vez de `log` porque acepta 0 (log(0) = -inf).\n\n"
            "## Normalizacion min-max — escala 0 a 1\n"
            "```python\n"
            "def min_max(s):\n"
            "    return (s - s.min()) / (s.max() - s.min())\n\n"
            "df['edad_norm'] = min_max(df['edad'])\n"
            "```\n"
            "Util cuando importa la **forma** de la distribucion mas que la\n"
            "escala (kNN, redes con sigmoid).\n\n"
            "## Estandarizacion z-score — media 0, std 1\n"
            "```python\n"
            "def zscore(s):\n"
            "    return (s - s.mean()) / s.std()\n\n"
            "df['edad_z'] = zscore(df['edad'])\n"
            "```\n"
            "Mas comun en regresion lineal / logistica y para detectar outliers\n"
            "(|z| > 3 suele considerarse outlier).\n\n"
            "## Errores comunes\n"
            "- Hacer one-hot a una columna con miles de categorias: explosion\n"
            "  de columnas. Mejor usar target encoding o agrupar las raras en\n"
            "  'otros'.\n"
            "- Normalizar TODO el dataset junto incluyendo el target: leak.\n"
            "  Normaliza features, no el target.\n"
            "- Calcular la normalizacion sobre el dataset COMPLETO y despues\n"
            "  hacer split train/test: leak temporal. Lo correcto es fitear\n"
            "  los stats en train y aplicarlos a test.\n"
            "- Usar log sobre una columna con ceros sin log1p: -inf en la\n"
            "  primera fila, modelo roto.\n\n"
            "## Resumen\n"
            "- One-hot para nominales (sin orden); label/map para ordinales.\n"
            "- `pd.cut` con limites fijos; `pd.qcut` con cuantiles.\n"
            "- Log para distribuciones sesgadas (`log1p` si hay ceros).\n"
            "- Min-max para distancias (kNN); z-score para regresion lineal.\n"
            "- Calcula los parametros de normalizacion en train, no en todo el\n"
            "  dataset.\n"
        ),
        difficulty="intermediate",
        category="eda",
        order=19,
        track="track-2",
        estimated_duration=55,
        prerequisites_titles=["EDA: exploracion sistematica de un dataset"],
        exercises=[
            ExerciseTemplate(
                title="One-hot encoding de pais",
                description="Convertir una columna categorica en columnas binarias.",
                instructions=(
                    "Implementa `one_hot_pais(df)` que devuelve un DataFrame "
                    "agregando columnas one-hot por cada valor unico de la "
                    "columna 'pais', con el prefijo 'pais_' (ej. 'pais_AR'). "
                    "Devuelve el DataFrame con las columnas originales MAS las "
                    "nuevas; NO drop_first."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def one_hot_pais(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: pd.get_dummies(df, columns=['pais'], prefix='pais')\n"
                    "    pass\n"
                ),
                hints=[
                    "pd.get_dummies(df, columns=['pais'], prefix='pais') hace todo en una linea.",
                    "Sin drop_first quedan tantas columnas dummy como categorias distintas.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve DataFrame con las dummies",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'pais':['AR','MX','CO','AR']})\n"
                            "out = one_hot_pais(df)\n"
                            "assert 'pais_AR' in out.columns\n"
                            "assert 'pais_MX' in out.columns\n"
                            "assert 'pais_CO' in out.columns"
                        ),
                    },
                    {
                        "name": "los valores son 0/1 correctos",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'pais':['AR','MX','CO','AR']})\n"
                            "out = one_hot_pais(df)\n"
                            "assert int(out['pais_AR'].iloc[0]) == 1\n"
                            "assert int(out['pais_AR'].iloc[1]) == 0\n"
                            "assert int(out['pais_MX'].iloc[1]) == 1\n"
                            "assert int(out['pais_AR'].iloc[3]) == 1"
                        ),
                    },
                    {
                        "name": "la columna original pais ya no esta",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'pais':['AR','MX','CO','AR']})\n"
                            "out = one_hot_pais(df)\n"
                            "# get_dummies con columns= drop la original.\n"
                            "assert 'pais' not in out.columns"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Binning de edad en grupos",
                description="Convertir edad numerica en categorias etarias con pd.cut.",
                instructions=(
                    "Implementa `grupos_etarios(df)` que recibe un DataFrame con "
                    "columna 'edad'. Devuelve el mismo DataFrame con una nueva "
                    "columna 'grupo' usando los bins [0, 18, 30, 50, 100] y "
                    "labels ['menor', 'joven', 'adulto', 'mayor']. No mutar "
                    "el original."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def grupos_etarios(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: copia, df['grupo'] = pd.cut(df['edad'], bins=..., labels=...)\n"
                    "    pass\n"
                ),
                hints=[
                    "pd.cut(serie, bins=[0,18,30,50,100], labels=['menor','joven','adulto','mayor'])",
                    "Devolve una copia: out = df.copy(); out['grupo'] = ...",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "no muta el original",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'edad':[10, 25, 40, 60]})\n"
                            "_ = grupos_etarios(df)\n"
                            "assert 'grupo' not in df.columns"
                        ),
                    },
                    {
                        "name": "asigna el grupo correcto a cada edad",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'edad':[10, 25, 40, 60]})\n"
                            "out = grupos_etarios(df)\n"
                            "assert str(out['grupo'].iloc[0]) == 'menor'\n"
                            "assert str(out['grupo'].iloc[1]) == 'joven'\n"
                            "assert str(out['grupo'].iloc[2]) == 'adulto'\n"
                            "assert str(out['grupo'].iloc[3]) == 'mayor'"
                        ),
                    },
                    {
                        "name": "preserva las columnas originales",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'edad':[10, 25, 40, 60], 'extra': [1,2,3,4]})\n"
                            "out = grupos_etarios(df)\n"
                            "assert 'edad' in out.columns\n"
                            "assert 'extra' in out.columns"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Normalizar con min-max y z-score",
                description="Devolver el DataFrame con dos columnas extra normalizadas.",
                instructions=(
                    "Implementa `normalizar_precio(df)` que recibe un DataFrame "
                    "con columna 'precio'. Devuelve una copia con dos columnas "
                    "extra: 'precio_norm' (min-max a [0, 1]) y 'precio_z' "
                    "(z-score). No mutar el original."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def normalizar_precio(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: copia, calcula min/max y mean/std,\n"
                    "    # crea precio_norm y precio_z.\n"
                    "    pass\n"
                ),
                hints=[
                    "min-max: (s - s.min()) / (s.max() - s.min())",
                    "z-score: (s - s.mean()) / s.std()",
                    "Calcula los stats sobre la columna del DataFrame copiado, no de pasos intermedios.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "no muta el original",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10.0, 20.0, 30.0]})\n"
                            "_ = normalizar_precio(df)\n"
                            "assert 'precio_norm' not in df.columns\n"
                            "assert 'precio_z' not in df.columns"
                        ),
                    },
                    {
                        "name": "min-max queda en rango [0, 1]",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10.0, 20.0, 30.0, 40.0]})\n"
                            "out = normalizar_precio(df)\n"
                            "assert abs(out['precio_norm'].min() - 0.0) < 1e-9\n"
                            "assert abs(out['precio_norm'].max() - 1.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "z-score tiene media cercana a 0",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10.0, 20.0, 30.0, 40.0]})\n"
                            "out = normalizar_precio(df)\n"
                            "assert abs(out['precio_z'].mean()) < 1e-9"
                        ),
                    },
                    {
                        "name": "preserva la columna original 'precio'",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10.0, 20.0, 30.0]})\n"
                            "out = normalizar_precio(df)\n"
                            "assert 'precio' in out.columns\n"
                            "assert out['precio'].tolist() == [10.0, 20.0, 30.0]"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Estadistica descriptiva: resumir un dataset",
        description="Tendencia central y dispersion, cuando usar media vs mediana, forma de la distribucion con skewness y kurtosis.",
        content=(
            "## Por que estadistica descriptiva\n"
            "Antes de cualquier modelo, necesitas **comunicar** que hay en\n"
            "tus datos. La estadistica descriptiva resume con pocos numeros\n"
            "lo que veria un humano mirando miles de filas:\n"
            "- ¿Donde esta el 'centro' de la variable?\n"
            "- ¿Que tan dispersos estan los valores?\n"
            "- ¿La distribucion es simetrica o sesgada?\n\n"
            "## Medidas de tendencia central\n\n"
            "### Media (promedio)\n"
            "```python\n"
            "df['edad'].mean()  # suma / n\n"
            "```\n"
            "Sensible a outliers: un valor extremo arrastra el promedio.\n\n"
            "### Mediana (valor central)\n"
            "```python\n"
            "df['edad'].median()  # el del medio cuando ordenas\n"
            "```\n"
            "**Resistente a outliers**. Si tu distribucion tiene cola larga\n"
            "(salarios, vistas en YouTube), usa mediana.\n\n"
            "### Moda (valor mas frecuente)\n"
            "```python\n"
            "df['plan'].mode()  # puede haber varias modas si hay empate\n"
            "```\n"
            "Util para categoricas. En numericas continuas rara vez tiene sentido.\n\n"
            "**Cuando usar cual**:\n"
            "- **Media** — distribucion simetrica sin outliers (notas, alturas).\n"
            "- **Mediana** — distribucion sesgada o con outliers (precios, ingresos).\n"
            "- **Moda** — categoricas, o discretas donde 'el caso mas comun' importa.\n\n"
            "## Medidas de dispersion\n\n"
            "### Varianza y desviacion estandar\n"
            "```python\n"
            "df['edad'].var()   # promedio de (x - mean)^2\n"
            "df['edad'].std()   # raiz cuadrada de la varianza\n"
            "```\n"
            "La std esta en las mismas unidades que la variable (edades en\n"
            "anios, std en anios). Por eso se prefiere para reportar.\n\n"
            "### Rango intercuartil (IQR)\n"
            "```python\n"
            "iqr = df['edad'].quantile(0.75) - df['edad'].quantile(0.25)\n"
            "```\n"
            "**Resistente a outliers**. Si usas mediana como centro, IQR es la\n"
            "dispersion natural a reportar (no std).\n\n"
            "## Forma de la distribucion\n\n"
            "### Skewness (asimetria)\n"
            "```python\n"
            "df['precio'].skew()\n"
            "```\n"
            "- **0**: simetrica.\n"
            "- **>0**: cola a la derecha (salarios, precios).\n"
            "- **<0**: cola a la izquierda (edad de jubilacion).\n"
            "- **|skew| > 1**: muy sesgada — considera transformacion log.\n\n"
            "### Kurtosis (peso de las colas)\n"
            "```python\n"
            "df['precio'].kurt()\n"
            "```\n"
            "- **0** (Fisher): igual a una normal.\n"
            "- **>0**: leptokurtic — colas mas pesadas que normal, mas outliers.\n"
            "- **<0**: platykurtic — distribucion mas plana.\n\n"
            "## Regla 68-95-99.7 (solo para distribuciones casi normales)\n"
            "Si tu variable es ~normal:\n"
            "- 68% de los valores caen dentro de mean ± 1 std.\n"
            "- 95% dentro de mean ± 2 std.\n"
            "- 99.7% dentro de mean ± 3 std.\n\n"
            "Esta regla es como detectas outliers via z-score: |z| > 3 implica\n"
            "<0.3% de probabilidad si fuera realmente normal.\n\n"
            "## Cuidado: estadisticas mienten con poca data\n"
            "Calcular media y std sobre 3 puntos no te dice nada. Reglas\n"
            "practicas:\n"
            "- **n < 30**: usa mediana y rango, no media y std.\n"
            "- **n < 5**: no calcules nada, mira los valores uno por uno.\n"
            "- Siempre acompaña el resumen con n (count) para que el lector\n"
            "  pondere la confianza.\n\n"
            "## Errores comunes\n"
            "- Reportar 'el promedio de salario es 80k' cuando hay un CEO de\n"
            "  10M en la muestra: la mediana puede ser 45k. Usa mediana cuando\n"
            "  hay outliers grandes.\n"
            "- Confundir n (sample size) con la cantidad de valores unicos.\n"
            "  `df['edad'].nunique()` no es lo mismo que `len(df)`.\n"
            "- Aplicar la regla 68-95-99.7 a distribuciones que no son normales.\n"
            "  Hace falta verificar primero (skew, qq-plot, Shapiro-Wilk).\n"
            "- `df.mean()` ignora NaN automaticamente. Util, pero verificar\n"
            "  `df.isna().sum()` para saber sobre cuantos valores realmente se\n"
            "  promedio.\n\n"
            "## Resumen\n"
            "- Media/mediana/moda: tendencia central. Mediana resiste outliers.\n"
            "- std/var/IQR: dispersion. IQR resiste outliers.\n"
            "- skew indica asimetria; kurt indica colas pesadas.\n"
            "- Si distribucion casi normal, regla 68-95-99.7 para z-score.\n"
            "- Siempre reportar n junto con el resumen.\n"
        ),
        difficulty="intermediate",
        category="estadistica",
        order=20,
        track="track-2",
        estimated_duration=50,
        prerequisites_titles=["EDA 2: feature engineering basico"],
        exercises=[
            ExerciseTemplate(
                title="Resumen de una columna",
                description="Devolver un dict con mean, median, std y count.",
                instructions=(
                    "Implementa `resumir(serie)` que recibe una pd.Series numerica "
                    "y devuelve un dict con keys 'mean', 'median', 'std', 'count'. "
                    "Los NaN deben ignorarse en mean/median/std (que es el default "
                    "de pandas), pero count debe ser el numero de NO-NaN."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def resumir(serie: pd.Series) -> dict:\n"
                    "    # TODO: {'mean': ..., 'median': ..., 'std': ..., 'count': ...}\n"
                    "    pass\n"
                ),
                hints=[
                    "serie.mean(), serie.median(), serie.std() ignoran NaN.",
                    "serie.count() devuelve la cantidad de no-NaN.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve dict con las 4 keys",
                        "code": (
                            "import pandas as pd\n"
                            "out = resumir(pd.Series([1.0, 2.0, 3.0, 4.0]))\n"
                            "assert isinstance(out, dict)\n"
                            "assert set(out.keys()) == {'mean','median','std','count'}"
                        ),
                    },
                    {
                        "name": "calcula media y mediana correctas",
                        "code": (
                            "import pandas as pd\n"
                            "out = resumir(pd.Series([1.0, 2.0, 3.0, 4.0, 5.0]))\n"
                            "assert abs(out['mean'] - 3.0) < 1e-9\n"
                            "assert abs(out['median'] - 3.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "count ignora NaN",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "out = resumir(pd.Series([1.0, 2.0, np.nan, 4.0]))\n"
                            "assert out['count'] == 3"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Detectar distribucion sesgada",
                description="Devolver True si |skew| > 1 (regla practica de sesgo fuerte).",
                instructions=(
                    "Implementa `esta_sesgada(serie)` que recibe una pd.Series "
                    "y devuelve True si el skew absoluto es mayor a 1 (regla "
                    "comun para sesgo 'fuerte'). En otro caso False."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def esta_sesgada(serie: pd.Series) -> bool:\n"
                    "    # TODO: abs(serie.skew()) > 1\n"
                    "    pass\n"
                ),
                hints=[
                    "serie.skew() devuelve el coeficiente de asimetria (float).",
                    "Usa abs() y compara con 1.",
                    "Devolve un bool, no un numpy bool. bool(serie.skew()) si hace falta.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "distribucion simetrica devuelve False",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "# Normal: skew ~ 0\n"
                            "s = pd.Series(rng.normal(0, 1, 1000))\n"
                            "assert esta_sesgada(s) is False"
                        ),
                    },
                    {
                        "name": "distribucion muy sesgada devuelve True",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "# Exponencial: skew muy positivo\n"
                            "s = pd.Series(rng.exponential(1.0, 1000))\n"
                            "assert esta_sesgada(s) is True"
                        ),
                    },
                    {
                        "name": "negativamente sesgada tambien devuelve True",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "# Exp invertida: skew muy negativo\n"
                            "s = pd.Series(-rng.exponential(1.0, 1000))\n"
                            "assert esta_sesgada(s) is True"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Comparar dos grupos numericamente",
                description="Resumen comparado entre dos grupos: diferencia de medias normalizada por std combinado.",
                instructions=(
                    "Implementa `comparar(grupo_a, grupo_b)` que recibe dos "
                    "pd.Series numericas y devuelve un dict con: "
                    "(1) 'mean_a' y 'mean_b' (medias), (2) 'std_pooled' "
                    "(desviacion estandar combinada = sqrt((var_a + var_b)/2)), "
                    "(3) 'cohen_d' (diferencia de medias / std_pooled). "
                    "Cohen's d es una medida estandar de tamano del efecto."
                ),
                starter_code=(
                    "import pandas as pd\n"
                    "import numpy as np\n\n"
                    "def comparar(grupo_a: pd.Series, grupo_b: pd.Series) -> dict:\n"
                    "    # TODO: calcular mean_a, mean_b, var_a, var_b,\n"
                    "    # std_pooled = sqrt((var_a + var_b) / 2),\n"
                    "    # cohen_d = (mean_a - mean_b) / std_pooled.\n"
                    "    pass\n"
                ),
                hints=[
                    "grupo_a.var() y grupo_b.var() dan las varianzas.",
                    "np.sqrt((var_a + var_b) / 2) es la formula de pooled std (version simple).",
                    "Devolve floats convencionales, no numpy scalars (usa float(...) si necesario).",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "devuelve las 4 keys esperadas",
                        "code": (
                            "import pandas as pd\n"
                            "a = pd.Series([1.0, 2.0, 3.0, 4.0])\n"
                            "b = pd.Series([2.0, 3.0, 4.0, 5.0])\n"
                            "out = comparar(a, b)\n"
                            "assert set(out.keys()) == {'mean_a','mean_b','std_pooled','cohen_d'}"
                        ),
                    },
                    {
                        "name": "medias correctas",
                        "code": (
                            "import pandas as pd\n"
                            "a = pd.Series([1.0, 2.0, 3.0, 4.0])\n"
                            "b = pd.Series([2.0, 3.0, 4.0, 5.0])\n"
                            "out = comparar(a, b)\n"
                            "assert abs(out['mean_a'] - 2.5) < 1e-9\n"
                            "assert abs(out['mean_b'] - 3.5) < 1e-9"
                        ),
                    },
                    {
                        "name": "grupos identicos dan cohen_d 0",
                        "code": (
                            "import pandas as pd\n"
                            "a = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])\n"
                            "b = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])\n"
                            "out = comparar(a, b)\n"
                            "assert abs(out['cohen_d']) < 1e-9"
                        ),
                    },
                    {
                        "name": "cohen_d tiene el signo correcto",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "a = pd.Series(rng.normal(10.0, 1.0, 200))\n"
                            "b = pd.Series(rng.normal(5.0, 1.0, 200))\n"
                            "out = comparar(a, b)\n"
                            "# a > b en media -> cohen_d > 0\n"
                            "assert out['cohen_d'] > 0"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Correlacion, probabilidad y bootstrap",
        description="Pearson vs Spearman, simular probabilidades con Monte Carlo y estimar intervalos de confianza con bootstrap.",
        content=(
            "## Tres ideas que necesitas\n"
            "1. **Correlacion sirve para describir relaciones, pero hay dos\n"
            "   tipos** segun la forma de esa relacion.\n"
            "2. **Cuando no podes derivar una probabilidad analiticamente,\n"
            "   simulala** con muestreo (Monte Carlo).\n"
            "3. **Tus estimaciones tienen incertidumbre**; reportar un\n"
            "   intervalo en vez de un numero solo es lo profesional.\n\n"
            "## Correlacion Pearson vs Spearman\n\n"
            "### Pearson — relacion lineal\n"
            "```python\n"
            "df['x'].corr(df['y'])              # default Pearson\n"
            "df['x'].corr(df['y'], method='pearson')\n"
            "```\n"
            "Mide que tan bien una **linea recta** ajusta los datos. Va de -1\n"
            "a +1. Si la relacion entre X e Y es cuadratica (Y = X^2), Pearson\n"
            "puede dar casi cero — y aun asi habria una relacion fortisima.\n\n"
            "### Spearman — relacion monotona\n"
            "```python\n"
            "df['x'].corr(df['y'], method='spearman')\n"
            "```\n"
            "Mide si, al ordenar X, Y tambien queda ordenado. **Captura\n"
            "relaciones no lineales monotonas** (Y = X^3, Y = log(X)).\n\n"
            "**Cuando usar cual**:\n"
            "- Pearson: variables continuas con relacion aparentemente lineal.\n"
            "- Spearman: ordinales, distribuciones sesgadas, o cuando sospechas\n"
            "  relacion no lineal pero monotona.\n"
            "- Si tenes outliers, Spearman es mas robusto (usa rankings).\n\n"
            "## Probabilidad — vocabulario minimo\n"
            "Para una variable aleatoria X:\n"
            "- **P(A)**: probabilidad del evento A.\n"
            "- **P(A ∩ B)**: probabilidad de que pasen A Y B.\n"
            "- **P(A | B)**: probabilidad de A **dado que** ya paso B (condicional).\n"
            "- **Bayes**: P(A | B) = P(B | A) * P(A) / P(B).\n\n"
            "## Monte Carlo — simular probabilidades\n"
            "Cuando no podes deducir una probabilidad analiticamente:\n"
            "1. Simulas N experimentos.\n"
            "2. Contas cuantas veces ocurrio el evento.\n"
            "3. P(evento) ≈ ocurrencias / N.\n\n"
            "Ejemplo: ¿que chance hay de que la suma de 2 dados sea 7?\n"
            "```python\n"
            "import numpy as np\n\n"
            "rng = np.random.default_rng(42)\n"
            "N = 100_000\n"
            "d1 = rng.integers(1, 7, size=N)\n"
            "d2 = rng.integers(1, 7, size=N)\n"
            "p = (d1 + d2 == 7).mean()  # ~0.167 (real: 6/36 = 0.1667)\n"
            "```\n"
            "Cuanto mayor N, mas estable la estimacion. La regla heuristica:\n"
            "el error escala con `1/sqrt(N)`, asi que 100x mas muestras = 10x\n"
            "menos error.\n\n"
            "## Bootstrap — intervalos de confianza para cualquier estadistica\n"
            "El bootstrap responde: '¿que tan confiable es mi estimacion?'.\n"
            "Estrategia:\n"
            "1. Resampleas tu sample con reemplazo (mismo tamano).\n"
            "2. Calculas la estadistica (media, mediana, etc.) sobre cada\n"
            "   resample.\n"
            "3. Despues de muchos resamples (1000-10000), tomas los percentiles\n"
            "   2.5 y 97.5 — eso es el IC del 95%.\n\n"
            "```python\n"
            "def ic_bootstrap_media(datos, n_resamples=2000, ci=0.95, seed=0):\n"
            "    rng = np.random.default_rng(seed)\n"
            "    medias = np.empty(n_resamples)\n"
            "    n = len(datos)\n"
            "    for i in range(n_resamples):\n"
            "        muestra = rng.choice(datos, size=n, replace=True)\n"
            "        medias[i] = muestra.mean()\n"
            "    alpha = 1 - ci\n"
            "    bajo = np.percentile(medias, 100 * alpha / 2)\n"
            "    alto = np.percentile(medias, 100 * (1 - alpha / 2))\n"
            "    return bajo, alto\n"
            "```\n"
            "Salida: '(IC 95%): [4.8, 5.3]' es mas util que 'la media es 5.1'.\n\n"
            "## Errores comunes\n"
            "- Reportar solo Pearson sin haber visto el scatter: si la relacion\n"
            "  es no lineal, Pearson puede esconder algo importante.\n"
            "- Confundir P(A | B) con P(B | A). Caso clasico: test medico con\n"
            "  positivo no significa enfermedad alta probabilidad si la\n"
            "  enfermedad es rara (paradoja de la base).\n"
            "- Hacer Monte Carlo con N muy chico (1000) y reportar 3 decimales:\n"
            "  esos decimales son ruido.\n"
            "- Bootstrap mal: resamplear SIN reemplazo (te queda el mismo sample\n"
            "  cada vez), o no fijar la seed para reproducibilidad.\n\n"
            "## Resumen\n"
            "- Pearson: relacion lineal. Spearman: relacion monotona (mas\n"
            "  robusta).\n"
            "- Monte Carlo: simulas N veces y contas para estimar P. Error\n"
            "  ~ 1/sqrt(N).\n"
            "- Bootstrap: resample con reemplazo y calcula percentiles para\n"
            "  obtener IC sin asumir distribucion.\n"
            "- Siempre acompaña una estimacion con su incertidumbre.\n"
        ),
        difficulty="advanced",
        category="estadistica",
        order=21,
        track="track-2",
        estimated_duration=60,
        prerequisites_titles=["Estadistica descriptiva: resumir un dataset"],
        exercises=[
            ExerciseTemplate(
                title="Pearson vs Spearman",
                description="Detectar cuando una relacion no es lineal pero si monotona.",
                instructions=(
                    "Implementa `comparar_correlaciones(x, y)` que recibe dos "
                    "pd.Series numericas y devuelve un dict con keys 'pearson' "
                    "y 'spearman' con cada correlacion. Ambas son floats entre "
                    "-1 y 1."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def comparar_correlaciones(x: pd.Series, y: pd.Series) -> dict:\n"
                    "    # TODO: {'pearson': x.corr(y), 'spearman': x.corr(y, method='spearman')}\n"
                    "    pass\n"
                ),
                hints=[
                    "x.corr(y) sin method= devuelve Pearson.",
                    "x.corr(y, method='spearman') usa rankings.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve dict con las dos keys",
                        "code": (
                            "import pandas as pd\n"
                            "x = pd.Series([1.0, 2.0, 3.0, 4.0])\n"
                            "y = pd.Series([2.0, 4.0, 6.0, 8.0])\n"
                            "out = comparar_correlaciones(x, y)\n"
                            "assert set(out.keys()) == {'pearson','spearman'}"
                        ),
                    },
                    {
                        "name": "relacion lineal: pearson cercano a 1",
                        "code": (
                            "import pandas as pd\n"
                            "x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])\n"
                            "y = pd.Series([2.0, 4.0, 6.0, 8.0, 10.0])\n"
                            "out = comparar_correlaciones(x, y)\n"
                            "assert abs(out['pearson'] - 1.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "relacion cubica: spearman > pearson",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "x = pd.Series(np.linspace(-5, 5, 50))\n"
                            "# y = x^3 es monotona pero no lineal\n"
                            "y = pd.Series(x.values ** 3)\n"
                            "out = comparar_correlaciones(x, y)\n"
                            "# Spearman captura monotonia perfecta\n"
                            "assert abs(out['spearman'] - 1.0) < 1e-9\n"
                            "# Pearson es alto pero no perfecto\n"
                            "assert out['pearson'] < 1.0"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Monte Carlo: suma de dos dados",
                description="Simular N tiradas y estimar P(suma == valor_objetivo).",
                instructions=(
                    "Implementa `prob_suma_dados(valor_objetivo, n=100_000, seed=0)` "
                    "que simula `n` tiradas de dos dados (cada uno 1..6 inclusive) "
                    "y devuelve la probabilidad estimada (float) de que la suma "
                    "sea igual a `valor_objetivo`. Usa np.random.default_rng(seed)."
                ),
                starter_code=(
                    "import numpy as np\n\n"
                    "def prob_suma_dados(valor_objetivo: int, n: int = 100_000, seed: int = 0) -> float:\n"
                    "    # TODO: rng = np.random.default_rng(seed)\n"
                    "    # d1 = rng.integers(1, 7, size=n)  # 7 exclusivo\n"
                    "    # d2 = rng.integers(1, 7, size=n)\n"
                    "    # return float((d1 + d2 == valor_objetivo).mean())\n"
                    "    pass\n"
                ),
                hints=[
                    "rng.integers(low, high, size=n) — high es EXCLUSIVO. Para 1..6 usar (1, 7).",
                    "(d1 + d2 == valor).mean() te da la proporcion en un solo paso.",
                    "Devolve un float Python (usa float(...) si pandas/numpy te devuelve scalar).",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "devuelve un float",
                        "code": (
                            "p = prob_suma_dados(7, n=1000, seed=0)\n"
                            "assert isinstance(p, float)"
                        ),
                    },
                    {
                        "name": "suma 7 da probabilidad cercana a 0.167",
                        "code": (
                            "# 6/36 combinaciones (1+6, 2+5, ..., 6+1) → 0.1667\n"
                            "p = prob_suma_dados(7, n=200_000, seed=0)\n"
                            "assert abs(p - 6/36) < 0.01, f'esperaba ~0.167, obtuve {p}'"
                        ),
                    },
                    {
                        "name": "suma 2 da probabilidad cercana a 0.028",
                        "code": (
                            "# 1/36 combinaciones (1+1)\n"
                            "p = prob_suma_dados(2, n=200_000, seed=0)\n"
                            "assert abs(p - 1/36) < 0.01, f'esperaba ~0.028, obtuve {p}'"
                        ),
                    },
                    {
                        "name": "suma imposible da 0 (suma 13)",
                        "code": (
                            "p = prob_suma_dados(13, n=10_000, seed=0)\n"
                            "assert p == 0.0"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="IC 95% de la media con bootstrap",
                description="Resamplear con reemplazo y devolver percentiles 2.5/97.5 de las medias.",
                instructions=(
                    "Implementa `ic_media_bootstrap(datos, n_resamples=2000, "
                    "seed=0)` que recibe un array/lista de numeros y devuelve "
                    "una tupla (lim_inferior, lim_superior) del IC del 95% de "
                    "la media estimado por bootstrap. Usar "
                    "`np.random.default_rng(seed)` y `np.percentile`."
                ),
                starter_code=(
                    "import numpy as np\n\n"
                    "def ic_media_bootstrap(datos, n_resamples: int = 2000, seed: int = 0) -> tuple:\n"
                    "    # TODO: rng = np.random.default_rng(seed)\n"
                    "    # medias = np.empty(n_resamples)\n"
                    "    # for i in range(n_resamples):\n"
                    "    #     muestra = rng.choice(datos, size=len(datos), replace=True)\n"
                    "    #     medias[i] = muestra.mean()\n"
                    "    # bajo = np.percentile(medias, 2.5); alto = np.percentile(medias, 97.5)\n"
                    "    # return (bajo, alto)\n"
                    "    pass\n"
                ),
                hints=[
                    "rng.choice(datos, size=n, replace=True) es el resampleo con reemplazo.",
                    "np.percentile(medias, 2.5) y np.percentile(medias, 97.5) dan los limites.",
                    "Devolve una tupla (float, float), no un array.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "devuelve una tupla de 2 floats",
                        "code": (
                            "out = ic_media_bootstrap([1.0,2.0,3.0,4.0,5.0], seed=0)\n"
                            "assert isinstance(out, tuple) and len(out) == 2\n"
                            "assert isinstance(float(out[0]), float)\n"
                            "assert isinstance(float(out[1]), float)"
                        ),
                    },
                    {
                        "name": "el intervalo contiene la media muestral",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "datos = rng.normal(10.0, 2.0, 200)\n"
                            "bajo, alto = ic_media_bootstrap(datos, seed=42)\n"
                            "media = float(datos.mean())\n"
                            "assert bajo <= media <= alto"
                        ),
                    },
                    {
                        "name": "ancho razonable (no demasiado grande ni cero)",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "datos = rng.normal(10.0, 2.0, 200)\n"
                            "bajo, alto = ic_media_bootstrap(datos, seed=42)\n"
                            "ancho = alto - bajo\n"
                            "# para normal(10, 2) con n=200, IC tipico ~ +/- 0.28\n"
                            "assert 0.0 < ancho < 1.5"
                        ),
                    },
                    {
                        "name": "reproducibilidad con misma seed",
                        "code": (
                            "out1 = ic_media_bootstrap([1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0], seed=7)\n"
                            "out2 = ic_media_bootstrap([1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0], seed=7)\n"
                            "assert out1 == out2"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 1 · Tu primer clasificador con scikit-learn",
        description=(
            "Aprendizaje supervisado en 3 ideas: features vs target, "
            "train/test split y el API fit/predict. Entrena un LogisticRegression "
            "y un KNN sobre iris."
        ),
        content=(
            "# ML 1: tu primer clasificador con scikit-learn\n\n"
            "Los tracks anteriores te dieron Python solido y la caja de "
            "herramientas de Data Science (NumPy, Pandas, matplotlib, "
            "estadistica). En este bloque empieza el Track 3: **Machine "
            "Learning clasico** con `scikit-learn`.\n\n"
            "## Tres ideas para empezar\n\n"
            "### 1. Aprendizaje supervisado = mapear X a y\n\n"
            "Un problema de aprendizaje supervisado tiene dos piezas:\n\n"
            "- **X** (features / caracteristicas): una matriz `n_samples x n_features` "
            "con lo que **observas** de cada ejemplo. En iris: 4 columnas numericas "
            "(largo y ancho del sepalo y del petalo).\n"
            "- **y** (target / etiqueta): un vector de longitud `n_samples` con "
            "lo que **quieres predecir**. Puede ser una categoria (clasificacion) "
            "o un numero (regresion). En iris: la especie (setosa / versicolor / "
            "virginica).\n\n"
            "Un modelo de ML es una funcion `f` tal que `y_estimado = f(X)`. El "
            "**entrenamiento** aprende los parametros de `f` a partir de datos "
            "vistos.\n\n"
            "> Regla mental: si no puedes describir X e y en una frase, no tienes "
            "un problema de ML todavia — tienes un problema de definicion de "
            "producto.\n\n"
            "### 2. Train / test split evita autoengano\n\n"
            "Si evaluas el modelo sobre los mismos datos con los que lo "
            "entrenaste, el modelo puede memorizar y darte 100% de accuracy sin "
            "haber aprendido nada generalizable. Por eso se separa el dataset:\n\n"
            "- **train**: 70-80% del dataset. El modelo lo ve y ajusta sus "
            "parametros.\n"
            "- **test**: 20-30% del dataset. Se guarda escondido; solo se usa al "
            "final para medir performance.\n\n"
            "```python\n"
            "from sklearn.model_selection import train_test_split\n\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y,\n"
            "    test_size=0.3,       # 30% para test\n"
            "    random_state=42,     # reproducible\n"
            "    stratify=y,          # mantiene proporcion de clases\n"
            ")\n"
            "```\n\n"
            "**Notas clave:**\n\n"
            "- `random_state=42` fija la semilla del RNG interno; sin esto cada "
            "corrida da un split distinto y no puedes reproducir resultados.\n"
            "- `stratify=y` es crucial en clasificacion desbalanceada: garantiza "
            "que la proporcion de cada clase en train y test sea la misma que en "
            "el dataset original. Sin esto, un split puede dejarte con 0 muestras "
            "de una clase en test.\n\n"
            "### 3. sklearn expone una API uniforme fit/predict\n\n"
            "Cualquier modelo de sklearn (`LogisticRegression`, `KNeighborsClassifier`, "
            "`DecisionTreeClassifier`, `RandomForestClassifier`, ...) implementa el "
            "mismo trio de metodos:\n\n"
            "1. `modelo.fit(X_train, y_train)` — aprende parametros.\n"
            "2. `modelo.predict(X_test)` — genera predicciones.\n"
            "3. `modelo.score(X_test, y_test)` — retorna la metrica por defecto "
            "(accuracy para clasificadores).\n\n"
            "Esta uniformidad es la que hace potente a sklearn: cambiar de modelo "
            "es literalmente cambiar una linea.\n\n"
            "## Tu primer clasificador: LogisticRegression\n\n"
            "A pesar del nombre, `LogisticRegression` es un **clasificador** — "
            "modela la probabilidad de cada clase con una funcion sigmoide sobre "
            "una combinacion lineal de features.\n\n"
            "```python\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import accuracy_score\n\n"
            "modelo = LogisticRegression(random_state=42, max_iter=500)\n"
            "modelo.fit(X_train, y_train)\n"
            "predicciones = modelo.predict(X_test)\n"
            "acc = accuracy_score(y_test, predicciones)\n"
            "print(f'accuracy = {acc:.3f}')\n"
            "```\n\n"
            "**Por que `max_iter=500`?** El default es 100; para datasets pequenos "
            "o mal escalados el optimizador puede no converger en 100 iteraciones "
            "y te sale un `ConvergenceWarning`. Subirlo es mas simple que "
            "estandarizar features en este primer contacto.\n\n"
            "## Otro modelo con la misma API: KNN\n\n"
            "`KNeighborsClassifier` no aprende parametros — memoriza el train y "
            "para cada punto de test busca los `k` vecinos mas cercanos, votando "
            "la clase mayoritaria.\n\n"
            "```python\n"
            "from sklearn.neighbors import KNeighborsClassifier\n\n"
            "knn = KNeighborsClassifier(n_neighbors=3)\n"
            "knn.fit(X_train, y_train)\n"
            "acc_knn = knn.score(X_test, y_test)\n"
            "```\n\n"
            "**Elegir `k`:**\n\n"
            "- `k=1`: sensible al ruido (memoriza un solo vecino).\n"
            "- `k` grande: promedia mucho, puede perder patrones locales.\n"
            "- Regla intuitiva: `k` impar y pequeno (3, 5, 7). En produccion se "
            "elige con cross-validation.\n\n"
            "## Metrica: accuracy\n\n"
            "`accuracy = predicciones correctas / total`. Es la metrica default "
            "de `score()` en clasificadores. Es simple e intuitiva pero **enganosa "
            "en desbalance**: si el 95% de los datos son de una clase, predecir "
            "siempre esa clase te da 95% de accuracy sin haber aprendido nada. "
            "Para esos casos existen precision, recall y f1 — los veras en la "
            "proxima leccion.\n\n"
            "## Errores comunes de la primera semana en ML\n\n"
            "1. **Entrenar y evaluar sobre el mismo split** — el clasico "
            '"tengo 100% de accuracy". Casi siempre significa que estas '
            "midiendo sobre train, o que la variable objetivo se filtro en X "
            "(data leakage).\n"
            "2. **Olvidar `random_state`** — sin semilla, cada corrida da un "
            "resultado distinto y no puedes comparar experimentos.\n"
            "3. **No estratificar** — con clases desbalanceadas o datasets "
            "pequenos, `stratify=y` puede ser la diferencia entre un split "
            "aprovechable y uno inutil.\n"
            "4. **Confundir `predict` con `predict_proba`** — el primero devuelve "
            "la clase (0/1/2 en iris), el segundo la probabilidad de cada clase "
            "(matriz n x n_clases).\n"
            "5. **Comparar accuracies sin test comun** — LogReg 0.90 y KNN 0.88 "
            "no significa nada si se corrieron sobre splits distintos. Fija "
            "`X_train, X_test, y_train, y_test` una vez y reusalos.\n\n"
            "## Resumen\n\n"
            "- ML supervisado = `f(X) -> y`, entrenada sobre datos historicos.\n"
            "- `train_test_split(random_state=42, stratify=y)` es tu punto de "
            "partida siempre. Sin split limpio no hay conclusion valida.\n"
            "- sklearn expone `fit`, `predict` y `score` en todos sus modelos. "
            "Cambiar de LogReg a KNN son 2 imports y una linea.\n"
            "- accuracy es el primer contacto con metricas de clasificacion; en "
            "la proxima leccion apareceran precision, recall y confusion matrix "
            "para escenarios reales.\n"
        ),
        difficulty="intermediate",
        category="ml-fundamentos",
        order=22,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "Estadistica descriptiva",
        ],
        exercises=[
            ExerciseTemplate(
                title="Split de iris estratificado",
                description=(
                    "Divide el dataset iris en train/test manteniendo la "
                    "proporcion de clases."
                ),
                instructions=(
                    "Implementa `preparar_iris_split(df)` que recibe el DataFrame "
                    "de iris (columnas `sepal_length, sepal_width, petal_length, "
                    "petal_width, species`) y devuelve la tupla `(X_train, X_test, "
                    "y_train, y_test)` con `test_size=0.3`, `random_state=42` y "
                    "`stratify=y`. X debe ser un DataFrame con las 4 features; y "
                    "una Series con la columna `species`."
                ),
                starter_code=(
                    "from sklearn.model_selection import train_test_split\n"
                    "\n"
                    "\n"
                    "def preparar_iris_split(df):\n"
                    "    # TODO: separa features (X) del target (y)\n"
                    "    # TODO: llama a train_test_split con test_size=0.3,\n"
                    "    #       random_state=42 y stratify=y\n"
                    "    # TODO: retorna (X_train, X_test, y_train, y_test)\n"
                    "    ...\n"
                ),
                hints=[
                    "X = df[['sepal_length','sepal_width','petal_length','petal_width']]; y = df['species'].",
                    "train_test_split retorna 4 objetos: X_train, X_test, y_train, y_test en ese orden.",
                    "stratify=y garantiza 3 muestras de cada clase en test (dataset 30 filas, 30% => 9).",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "tamanos correctos 21 train / 9 test",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n'\n"
                            "for i, sp in enumerate(['setosa']*10 + ['versicolor']*10 + ['virginica']*10):\n"
                            "    csv += f'{5.0+0.1*i},{3.0+0.05*i},{1.5+0.2*i},{0.3+0.1*i},{sp}\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X_train, X_test, y_train, y_test = preparar_iris_split(df)\n"
                            "assert len(X_train) == 21, len(X_train)\n"
                            "assert len(X_test) == 9, len(X_test)\n"
                            "assert len(y_train) == 21\n"
                            "assert len(y_test) == 9"
                        ),
                    },
                    {
                        "name": "X mantiene las 4 columnas de features",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n'\n"
                            "for i, sp in enumerate(['setosa']*10 + ['versicolor']*10 + ['virginica']*10):\n"
                            "    csv += f'{5.0+0.1*i},{3.0+0.05*i},{1.5+0.2*i},{0.3+0.1*i},{sp}\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X_train, X_test, _, _ = preparar_iris_split(df)\n"
                            "esperado = ['sepal_length','sepal_width','petal_length','petal_width']\n"
                            "assert list(X_train.columns) == esperado, list(X_train.columns)\n"
                            "assert list(X_test.columns) == esperado"
                        ),
                    },
                    {
                        "name": "stratify preserva 3 por clase en test",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n'\n"
                            "for i, sp in enumerate(['setosa']*10 + ['versicolor']*10 + ['virginica']*10):\n"
                            "    csv += f'{5.0+0.1*i},{3.0+0.05*i},{1.5+0.2*i},{0.3+0.1*i},{sp}\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "_, _, _, y_test = preparar_iris_split(df)\n"
                            "conteo = y_test.value_counts().to_dict()\n"
                            "assert conteo == {'setosa': 3, 'versicolor': 3, 'virginica': 3}, conteo"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Primer LogisticRegression sobre iris",
                description=(
                    "Entrena un modelo LogisticRegression y devuelve accuracy en test."
                ),
                instructions=(
                    "Implementa `entrenar_logreg(X_train, y_train, X_test, y_test)` "
                    "que crea un `LogisticRegression(random_state=42, max_iter=500)`, "
                    "lo entrena con `fit`, predice sobre `X_test` y devuelve la "
                    "accuracy como `float` (usa `accuracy_score` o `.score`)."
                ),
                starter_code=(
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.metrics import accuracy_score\n"
                    "\n"
                    "\n"
                    "def entrenar_logreg(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: crea LogisticRegression(random_state=42, max_iter=500)\n"
                    "    # TODO: fit sobre X_train, y_train\n"
                    "    # TODO: retorna float(accuracy_score(y_test, modelo.predict(X_test)))\n"
                    "    ...\n"
                ),
                hints=[
                    "El API es tres pasos: instanciar, fit, predict.",
                    "random_state=42 es lo que garantiza que tu resultado sea reproducible.",
                    "En iris con solo 30 filas y clases muy separables, LogReg puede llegar a 1.0.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "retorna un float en [0, 1]",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = entrenar_logreg(X_train, y_train, X_test, y_test)\n"
                            "assert isinstance(acc, float), type(acc)\n"
                            "assert 0.0 <= acc <= 1.0, acc"
                        ),
                    },
                    {
                        "name": "accuracy = 1.0 sobre iris con seed 42",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = entrenar_logreg(X_train, y_train, X_test, y_test)\n"
                            "assert acc == 1.0, acc"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Comparar KNN con distintos k",
                description=(
                    "Escribe una funcion que entrene KNN para varios valores de k "
                    "y devuelva el mapa k -> accuracy."
                ),
                instructions=(
                    "Implementa `comparar_knn(X_train, y_train, X_test, y_test, ks)` "
                    "que recibe una lista `ks` de enteros (p.ej. [3, 5, 7]) y "
                    "devuelve un `dict` `{k: accuracy_float}` entrenando un "
                    "`KNeighborsClassifier(n_neighbors=k)` distinto para cada k. "
                    "Usa la accuracy sobre `X_test`."
                ),
                starter_code=(
                    "from sklearn.neighbors import KNeighborsClassifier\n"
                    "from sklearn.metrics import accuracy_score\n"
                    "\n"
                    "\n"
                    "def comparar_knn(X_train, y_train, X_test, y_test, ks):\n"
                    "    # TODO: recorre ks, entrena un KNeighborsClassifier(n_neighbors=k),\n"
                    "    #       calcula accuracy en X_test y guarda en un dict\n"
                    "    ...\n"
                ),
                hints=[
                    "Cada k necesita su propio modelo entrenado — no reuses el mismo objeto entre iteraciones.",
                    "float(accuracy_score(y_test, modelo.predict(X_test))) o modelo.score(X_test, y_test).",
                    "En iris con 30 filas, k=3 y k=5 dan accuracies parecidos porque las clases estan muy separadas.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "devuelve dict con las k pedidas",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "res = comparar_knn(X_train, y_train, X_test, y_test, [3, 5])\n"
                            "assert isinstance(res, dict), type(res)\n"
                            "assert set(res.keys()) == {3, 5}, res.keys()\n"
                            "for v in res.values():\n"
                            "    assert isinstance(v, float), type(v)\n"
                            "    assert 0.0 <= v <= 1.0, v"
                        ),
                    },
                    {
                        "name": "accuracies iguales a 0.8889 para k=3 y k=5",
                        "code": (
                            "import io\n"
                            "import math\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "res = comparar_knn(X_train, y_train, X_test, y_test, [3, 5])\n"
                            "assert math.isclose(res[3], 8/9, abs_tol=1e-4), res[3]\n"
                            "assert math.isclose(res[5], 8/9, abs_tol=1e-4), res[5]"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 2 · Metricas mas alla de accuracy",
        description=(
            "Confusion matrix, precision, recall y f1. Cuando accuracy "
            "engana y como leer un clasificador bajo desbalance real."
        ),
        content=(
            "# ML 2: metricas mas alla de accuracy\n\n"
            "En la leccion anterior mediste tu primer clasificador con "
            "`accuracy_score`. En iris con 3 clases perfectamente "
            "balanceadas y muy separables, accuracy es informativa. En "
            "problemas reales (fraude, deteccion medica, spam, churn) "
            "accuracy casi siempre miente. Aqui aprendes las metricas que "
            "usan los equipos de ML en produccion.\n\n"
            "## Tres ideas para entender clasificacion real\n\n"
            "### 1. Accuracy engana con desbalance\n\n"
            "Ejemplo canonico: un dataset de fraude bancario donde el 99% "
            "de las transacciones son legitimas. Un modelo que **siempre "
            "predice legitimo** tiene 99% de accuracy y detecta 0 fraudes. "
            "En terminos de valor de negocio, ese modelo es peor que un "
            "generador aleatorio.\n\n"
            "Con clases desbalanceadas la clase mayoritaria domina la "
            'cuenta. Accuracy no distingue entre "acerto todos los '
            'faciles" y "acerto lo dificil".\n\n'
            "### 2. La confusion matrix te da la verdad completa\n\n"
            "Para clasificacion binaria (positivo/negativo), toda la "
            "informacion sobre las predicciones cabe en una matriz 2x2:\n\n"
            "```\n"
            "                predijo=0    predijo=1\n"
            "actual=0           TN           FP\n"
            "actual=1           FN           TP\n"
            "```\n\n"
            "- **TP (True Positive)**: real=1, predijo=1. Aciertos "
            "positivos.\n"
            "- **TN (True Negative)**: real=0, predijo=0. Aciertos "
            "negativos.\n"
            "- **FP (False Positive)**: real=0, predijo=1. Falsa alarma. "
            "Ej: usuario marcado como fraudulento cuando no lo era.\n"
            "- **FN (False Negative)**: real=1, predijo=0. Pase por alto. "
            "Ej: fraude no detectado, tumor no diagnosticado.\n\n"
            "sklearn lo devuelve con:\n\n"
            "```python\n"
            "from sklearn.metrics import confusion_matrix\n"
            "cm = confusion_matrix(y_true, y_pred)\n"
            "# cm[0, 0] = TN,  cm[0, 1] = FP\n"
            "# cm[1, 0] = FN,  cm[1, 1] = TP\n"
            "```\n\n"
            "> **Ordena importa:** el default de sklearn es "
            "`labels=sorted(unique)`, asi que para 0/1 el orden es "
            '"actual 0" arriba, "actual 1" abajo — coincide con la '
            'convencion academica. Para etiquetas string ("spam"/"ham") '
            "el orden alfabetico puede sorprenderte; siempre pasa `labels=` "
            "explicito.\n\n"
            "### 3. Precision, recall y f1: tres angulos del mismo problema\n\n"
            "A partir de la confusion matrix salen las tres metricas "
            "canonicas de clasificacion binaria:\n\n"
            "**Precision** = `TP / (TP + FP)`. De todo lo que predije como "
            "positivo, cuanto lo era. Optimizala cuando el costo de un "
            "**falso positivo** es alto — ej: acusar de fraude a un "
            "cliente inocente le genera friccion; queremos estar seguros "
            "antes de senalar.\n\n"
            "**Recall** (o sensibilidad) = `TP / (TP + FN)`. De todos los "
            "positivos reales, cuantos atrape. Optimizala cuando el costo "
            "de un **falso negativo** es alto — ej: no detectar un tumor "
            "cuando lo hay puede matar al paciente; preferimos falsas "
            "alarmas.\n\n"
            "**F1-score** = media armonica de precision y recall = "
            "`2 * P * R / (P + R)`. Un solo numero que penaliza dejar "
            "cualquiera de las dos en cero. Es el default cuando no tienes "
            "una razon fuerte para priorizar precision sobre recall.\n\n"
            "sklearn los expone en un solo call:\n\n"
            "```python\n"
            "from sklearn.metrics import (\n"
            "    precision_score, recall_score, f1_score,\n"
            "    classification_report,\n"
            ")\n"
            "print('precision:', precision_score(y_true, y_pred))\n"
            "print('recall:',    recall_score(y_true, y_pred))\n"
            "print('f1:',        f1_score(y_true, y_pred))\n"
            "\n"
            "# Todo junto (por clase + weighted):\n"
            "print(classification_report(y_true, y_pred))\n"
            "```\n\n"
            "## El tradeoff precision-recall\n\n"
            "Casi todos los clasificadores devuelven una **probabilidad** "
            "(via `predict_proba`) y aplican un **umbral** por defecto de "
            "0.5 para pasar a 0/1. Ese umbral es un dial:\n\n"
            "- **Umbral alto** (ej: 0.9): solo llamas positivo cuando el "
            "modelo esta muy seguro. Precision sube, recall baja.\n"
            "- **Umbral bajo** (ej: 0.2): llamas positivo con poca "
            "evidencia. Recall sube, precision baja.\n\n"
            "En produccion casi nunca usas el 0.5 default; eliges el "
            "umbral segun el costo relativo de FP vs FN en tu caso de uso.\n\n"
            "## Ejemplo con desbalance real: por que f1 es tu red\n\n"
            "Imagina un dataset de churn con 90 clientes que no se van y "
            '10 que si. Un modelo que predice "nadie se va":\n\n'
            "- accuracy = 90/100 = **0.90**  <- se ve genial\n"
            "- precision = indefinida (division por 0)\n"
            "- recall = 0/10 = **0.0**  <- no atrapo un solo churn\n"
            "- f1 = **0.0**  <- la metrica te grita que el modelo es "
            "inutil\n\n"
            "Un modelo decente que detecta 5 de 10 churns sin falsas "
            "alarmas:\n\n"
            "- accuracy = 95/100 = 0.95\n"
            "- precision = 5/5 = 1.00\n"
            "- recall = 5/10 = 0.50\n"
            "- f1 = 0.667\n\n"
            "El salto real (0 a 0.667 en f1) refleja el valor de negocio "
            "que accuracy no captura (subio de 0.90 a 0.95, apenas 5 "
            "puntos).\n\n"
            "## Errores comunes\n\n"
            "1. **Reportar solo accuracy en clasificacion binaria** — la "
            "audiencia tecnica pedira precision y recall en el siguiente "
            "mensaje.\n"
            "2. **Optimizar la metrica equivocada** — si tu problema es "
            '"encontrar todos los fraudes" (recall) pero reportas y '
            "optimizas accuracy, terminaras con un modelo elegante que no "
            "sirve.\n"
            "3. **Confundir precision (metrica) con precision (numero de "
            "decimales)** — precision de un clasificador es un ratio 0-1, "
            "no tiene nada que ver con float precision.\n"
            "4. **Comparar f1 entre modelos entrenados con distinto split** "
            "— fija `random_state` y reusa el mismo `X_test`, `y_test`.\n"
            "5. **`zero_division` warnings** — cuando no hay positivos "
            "predichos, sklearn levanta `UndefinedMetricWarning`. Pasa "
            "`zero_division=0` explicito para tratarlo como 0 en pipelines "
            "reales.\n\n"
            "## Resumen\n\n"
            "- Accuracy es la metrica de entrada; para clasificacion real "
            "reporta al menos precision, recall y f1.\n"
            "- La confusion matrix es la fuente de verdad: TP, TN, FP, FN "
            "definen todas las demas.\n"
            "- Precision minimiza falsas alarmas; recall minimiza casos "
            "perdidos; f1 los balancea.\n"
            "- Bajo desbalance, accuracy alta puede coexistir con f1 = 0. "
            "Siempre revisa la confusion matrix antes de celebrar.\n"
        ),
        difficulty="intermediate",
        category="ml-evaluacion",
        order=23,
        track="track-3",
        estimated_duration=50,
        prerequisites_titles=[
            "ML 1 · Tu primer clasificador con scikit-learn",
        ],
        exercises=[
            ExerciseTemplate(
                title="Extraer TN/FP/FN/TP de la confusion matrix",
                description=(
                    "Escribe una funcion que devuelva los 4 componentes de "
                    "la confusion matrix binaria como dict."
                ),
                instructions=(
                    "Implementa `desglose_confusion(y_true, y_pred)` que "
                    "usa `sklearn.metrics.confusion_matrix` sobre etiquetas "
                    "binarias 0/1 y devuelve un `dict` con las claves "
                    "`tn`, `fp`, `fn`, `tp` (todos ints). Recuerda: "
                    "`cm[0,0]=tn`, `cm[0,1]=fp`, `cm[1,0]=fn`, `cm[1,1]=tp`."
                ),
                starter_code=(
                    "from sklearn.metrics import confusion_matrix\n"
                    "\n"
                    "\n"
                    "def desglose_confusion(y_true, y_pred):\n"
                    "    # TODO: cm = confusion_matrix(y_true, y_pred, labels=[0, 1])\n"
                    "    # TODO: retorna dict {'tn': int(cm[0,0]), ...}\n"
                    "    ...\n"
                ),
                hints=[
                    "Pasa labels=[0, 1] explicito para que el orden sea determinista.",
                    "int(cm[i, j]) para asegurar que cada valor sea Python int, no numpy int64.",
                    "El dict debe tener exactamente las 4 claves tn, fp, fn, tp.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "caso balanceado 4-4-1-1",
                        "code": (
                            "res = desglose_confusion(\n"
                            "    [1, 0, 1, 1, 0, 1, 0, 0, 1, 0],\n"
                            "    [1, 0, 1, 0, 0, 1, 1, 0, 1, 0],\n"
                            ")\n"
                            "assert isinstance(res, dict), type(res)\n"
                            "assert set(res.keys()) == {'tn','fp','fn','tp'}, res.keys()\n"
                            "assert res == {'tn': 4, 'fp': 1, 'fn': 1, 'tp': 4}, res"
                        ),
                    },
                    {
                        "name": "todos correctos (FP=FN=0)",
                        "code": (
                            "res = desglose_confusion([0, 0, 1, 1], [0, 0, 1, 1])\n"
                            "assert res == {'tn': 2, 'fp': 0, 'fn': 0, 'tp': 2}, res"
                        ),
                    },
                    {
                        "name": "modelo dummy predice todo 0 con desbalance",
                        "code": (
                            "y_true = [0]*90 + [1]*10\n"
                            "y_pred = [0]*100\n"
                            "res = desglose_confusion(y_true, y_pred)\n"
                            "assert res == {'tn': 90, 'fp': 0, 'fn': 10, 'tp': 0}, res"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Precision, recall y f1 de un clasificador",
                description=("Devuelve un dict con las tres metricas usando sklearn."),
                instructions=(
                    "Implementa `metricas_binarias(y_true, y_pred)` que "
                    "retorna un `dict` con las claves `precision`, "
                    "`recall`, `f1` (floats en [0, 1]). Usa "
                    "`precision_score`, `recall_score` y `f1_score` de "
                    "`sklearn.metrics` con `zero_division=0` para "
                    "manejar el caso sin positivos predichos."
                ),
                starter_code=(
                    "from sklearn.metrics import precision_score, recall_score, f1_score\n"
                    "\n"
                    "\n"
                    "def metricas_binarias(y_true, y_pred):\n"
                    "    # TODO: retorna dict con 'precision', 'recall', 'f1'\n"
                    "    # TODO: usa zero_division=0 en cada score\n"
                    "    ...\n"
                ),
                hints=[
                    "float(precision_score(...)) evita numpy.float64 en el dict.",
                    "zero_division=0 devuelve 0.0 cuando no hay positivos predichos, en vez de lanzar warning.",
                    "El caso balanceado del ejercicio anterior (TP=4, FP=1, FN=1) da 0.8 en las tres metricas.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "caso balanceado da 0.8 en las 3",
                        "code": (
                            "import math\n"
                            "res = metricas_binarias(\n"
                            "    [1, 0, 1, 1, 0, 1, 0, 0, 1, 0],\n"
                            "    [1, 0, 1, 0, 0, 1, 1, 0, 1, 0],\n"
                            ")\n"
                            "assert set(res.keys()) == {'precision','recall','f1'}, res.keys()\n"
                            "for v in res.values():\n"
                            "    assert isinstance(v, float), type(v)\n"
                            "assert math.isclose(res['precision'], 0.8, abs_tol=1e-4), res\n"
                            "assert math.isclose(res['recall'], 0.8, abs_tol=1e-4), res\n"
                            "assert math.isclose(res['f1'], 0.8, abs_tol=1e-4), res"
                        ),
                    },
                    {
                        "name": "modelo dummy todo 0: precision=recall=f1=0",
                        "code": (
                            "res = metricas_binarias([0]*90 + [1]*10, [0]*100)\n"
                            "assert res['precision'] == 0.0, res\n"
                            "assert res['recall'] == 0.0, res\n"
                            "assert res['f1'] == 0.0, res"
                        ),
                    },
                    {
                        "name": "prediccion perfecta da 1.0 en las 3",
                        "code": (
                            "res = metricas_binarias([0, 1, 0, 1, 1], [0, 1, 0, 1, 1])\n"
                            "assert res['precision'] == 1.0, res\n"
                            "assert res['recall'] == 1.0, res\n"
                            "assert res['f1'] == 1.0, res"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Accuracy vs f1 bajo desbalance",
                description=(
                    "Demuestra por que accuracy sola no basta: compara "
                    "las metricas de un modelo dummy y uno decente sobre "
                    "un dataset 90/10."
                ),
                instructions=(
                    "Implementa `comparar_dummy_vs_decente(y_true, "
                    "pred_dummy, pred_decente)` que recibe tres listas de "
                    "0/1 y retorna un `dict` con dos entradas: `'dummy'` y "
                    "`'decente'`. Cada entrada es a su vez un dict con "
                    "`accuracy` y `f1` (floats con `zero_division=0`). "
                    "La idea es que el caller vea de un vistazo que la "
                    "diferencia real esta en f1, no en accuracy."
                ),
                starter_code=(
                    "from sklearn.metrics import accuracy_score, f1_score\n"
                    "\n"
                    "\n"
                    "def comparar_dummy_vs_decente(y_true, pred_dummy, pred_decente):\n"
                    "    # TODO: para cada prediccion calcula accuracy y f1\n"
                    "    # TODO: retorna {'dummy': {'accuracy': ..., 'f1': ...},\n"
                    "    #                'decente': {'accuracy': ..., 'f1': ...}}\n"
                    "    ...\n"
                ),
                hints=[
                    "Reutiliza accuracy_score(y_true, pred) y f1_score(y_true, pred, zero_division=0).",
                    "El dummy sobre 90/10 con todo 0 da accuracy=0.9 y f1=0.0.",
                    "El modelo decente con 5 TP, 0 FP, 5 FN sobre 90/10 da accuracy=0.95 y f1=0.6667.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "dummy y decente correctamente calculados",
                        "code": (
                            "import math\n"
                            "y_true = [0]*90 + [1]*10\n"
                            "pred_dummy = [0]*100\n"
                            "pred_decente = [0]*90 + [1]*5 + [0]*5\n"
                            "res = comparar_dummy_vs_decente(y_true, pred_dummy, pred_decente)\n"
                            "assert set(res.keys()) == {'dummy','decente'}, res.keys()\n"
                            "assert math.isclose(res['dummy']['accuracy'], 0.9, abs_tol=1e-4), res\n"
                            "assert math.isclose(res['dummy']['f1'], 0.0, abs_tol=1e-4), res\n"
                            "assert math.isclose(res['decente']['accuracy'], 0.95, abs_tol=1e-4), res\n"
                            "assert math.isclose(res['decente']['f1'], 2/3, abs_tol=1e-3), res"
                        ),
                    },
                    {
                        "name": "moraleja: f1 discrimina, accuracy no",
                        "code": (
                            "y_true = [0]*90 + [1]*10\n"
                            "res = comparar_dummy_vs_decente(y_true, [0]*100, [0]*90 + [1]*5 + [0]*5)\n"
                            "# accuracy sube apenas 0.05 (0.90 -> 0.95)\n"
                            "assert res['decente']['accuracy'] - res['dummy']['accuracy'] < 0.10\n"
                            "# f1 salta drasticamente (0.0 -> 0.667)\n"
                            "assert res['decente']['f1'] - res['dummy']['f1'] > 0.60"
                        ),
                    },
                    {
                        "name": "cada sub-entrada tiene exactamente accuracy y f1",
                        "code": (
                            "res = comparar_dummy_vs_decente([0,1,1], [0,0,0], [0,1,1])\n"
                            "for label in ('dummy', 'decente'):\n"
                            "    sub = res[label]\n"
                            "    assert set(sub.keys()) == {'accuracy', 'f1'}, sub.keys()\n"
                            "    for v in sub.values():\n"
                            "        assert isinstance(v, float), type(v)"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 3 · Features escaladas y Pipelines",
        description=(
            "StandardScaler, OneHotEncoder y Pipeline. Como preparar "
            "features numericas y categoricas sin data leakage."
        ),
        content=(
            "# ML 3: features escaladas y pipelines\n\n"
            "Ya tienes el flujo `split -> fit -> predict -> metricas`. En "
            "un dataset real, entre `split` y `fit` hay un paso crucial "
            "que decide si tu modelo funciona: **preprocesar las features** "
            "(escalar numericas, codificar categoricas). Hacerlo mal es la "
            "causa mas comun de resultados enganosamente buenos en "
            "notebooks que se desmoronan en produccion.\n\n"
            "## Tres ideas para preprocesar bien\n\n"
            "### 1. La mayoria de modelos asumen features 'razonables'\n\n"
            '"Razonables" significa: en escalas comparables y sin '
            "categorias como strings crudas. Si dejas los defaults del "
            "dataset:\n\n"
            "- **LogisticRegression** con features de escalas muy "
            "distintas (ej: edad 0-100 y ingreso 0-100000) puede no "
            "converger en `max_iter` iteraciones o quedar dominada por "
            "la feature de mayor magnitud.\n"
            "- **KNN** calcula distancias euclideas — una feature 1000x "
            "mas grande que otra la vuelve invisible.\n"
            "- **SVM con kernel RBF** es extremadamente sensible a la "
            "escala; sin escalar es casi inutil.\n"
            "- **Arboles de decision y Random Forest** son la excepcion: "
            "no les afecta la escala (particionan por umbral en cada "
            "feature individual). Pero siguen necesitando categoricas "
            "codificadas numericamente.\n\n"
            "**Regla de dedo:** casi siempre `StandardScaler` (media 0, "
            "desviacion 1) para numericas y `OneHotEncoder` para "
            "categoricas. Ahi arrancas.\n\n"
            "### 2. Pipeline evita el data leakage clasico\n\n"
            "El error mas comun del primer mes en ML es escalar antes de "
            "hacer split:\n\n"
            "```python\n"
            "# ANTI-PATTERN: data leakage\n"
            "scaler = StandardScaler()\n"
            "X_all = scaler.fit_transform(X)      # usa mean/std de TODO\n"
            "X_train, X_test = train_test_split(X_all, ...)\n"
            "```\n\n"
            "Por que es un problema: `mean` y `std` de `X_all` incluyen "
            "las filas de test. El modelo, al entrenarse, esta viendo "
            "indirectamente la distribucion de test — informacion que "
            "**en produccion no vas a tener**.\n\n"
            "La solucion correcta es aprender los parametros del "
            "preprocesador **solo con train** y aplicarlos igual sobre "
            "test:\n\n"
            "```python\n"
            "X_train, X_test = train_test_split(X, ...)\n"
            "scaler = StandardScaler()\n"
            "X_train_s = scaler.fit_transform(X_train)  # calcula + aplica\n"
            "X_test_s  = scaler.transform(X_test)       # SOLO aplica\n"
            "```\n\n"
            "Escribirlo asi cada vez es tedioso y facil de romper. "
            "`Pipeline` de sklearn lo automatiza:\n\n"
            "```python\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n\n"
            "pipe = Pipeline([\n"
            "    ('sc', StandardScaler()),\n"
            "    ('lr', LogisticRegression(random_state=42, max_iter=500)),\n"
            "])\n"
            "pipe.fit(X_train, y_train)         # escala + entrena\n"
            "acc = pipe.score(X_test, y_test)   # escala test con params de train + evalua\n"
            "```\n\n"
            "El pipeline garantiza que `StandardScaler.fit` solo ve "
            "`X_train`. Es lo que usan los equipos serios.\n\n"
            "### 3. ColumnTransformer maneja columnas heterogeneas\n\n"
            "Los datasets reales tienen una mezcla: `edad` (numerica), "
            "`plan` (categorica), `pais` (categorica), `ingreso` "
            "(numerica). No puedes aplicar `StandardScaler` a un string. "
            "`ColumnTransformer` es el switch:\n\n"
            "```python\n"
            "from sklearn.compose import ColumnTransformer\n"
            "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n\n"
            "preproc = ColumnTransformer([\n"
            "    ('num', StandardScaler(),                 ['edad', 'ingreso']),\n"
            "    ('cat', OneHotEncoder(sparse_output=False), ['plan']),\n"
            "])\n"
            "```\n\n"
            "El resultado es una matriz numerica lista para el modelo. "
            "Cada categoria se vuelve una columna 0/1: `plan` con valores "
            "`{basico, pro, enterprise}` da 3 columnas.\n\n"
            "**Flags utiles de OneHotEncoder:**\n"
            "- `sparse_output=False`: devuelve `np.ndarray` denso en vez "
            "de matriz sparse (mas facil de inspeccionar con pandas).\n"
            "- `handle_unknown='ignore'`: si en produccion aparece una "
            "categoria nueva, no crashea (la ignora en vez de lanzar).\n"
            "- `drop='first'`: elimina la primera categoria para evitar "
            "colinealidad (necesario en regresion lineal, opcional en "
            "arboles/redes).\n\n"
            "Se combina con Pipeline igual de facil:\n\n"
            "```python\n"
            "pipe = Pipeline([\n"
            "    ('prep', preproc),\n"
            "    ('lr', LogisticRegression(max_iter=500)),\n"
            "])\n"
            "pipe.fit(X_train, y_train)\n"
            "```\n\n"
            "## Debug: entender los nombres de features generadas\n\n"
            "Despues del preprocesador es dificil saber que columna es "
            "que. Usa `get_feature_names_out()` para verlo:\n\n"
            "```python\n"
            "preproc.fit(X_train)\n"
            "print(preproc.get_feature_names_out())\n"
            "# ['num__edad', 'num__ingreso', 'cat__plan_basico',\n"
            "#  'cat__plan_enterprise', 'cat__plan_pro']\n"
            "```\n\n"
            "El prefijo `num__` / `cat__` viene del nombre del "
            "transformador; despues del `__` va el nombre original y, "
            "para OHE, la categoria.\n\n"
            "## Errores comunes\n\n"
            "1. **`fit_transform` sobre el dataset completo** — data "
            "leakage. Escala/PCA/imputer siempre despues del split o "
            "dentro de un Pipeline.\n"
            "2. **`.fit` sobre test** — nunca. Test solo recibe "
            "`.transform` con los parametros aprendidos de train.\n"
            "3. **Escalar arboles/random forest** — no hace dano pero es "
            "trabajo inutil.\n"
            "4. **One-hot encodear una feature con miles de categorias** "
            "— genera miles de columnas. Para alta cardinalidad usa "
            "target encoding o embeddings; OHE es para 3-30 categorias.\n"
            "5. **Olvidar `handle_unknown='ignore'`** — en produccion un "
            "usuario con plan `enterprise-plus` que no vio train hara "
            "crashear la API entera.\n\n"
            "## Resumen\n\n"
            "- Escala numericas con `StandardScaler`; codifica "
            "categoricas con `OneHotEncoder(sparse_output=False, "
            "handle_unknown='ignore')`.\n"
            "- Envuelve todo en un `Pipeline` para que el preprocesador "
            "aprenda solo de train — sin leakage por defecto.\n"
            "- `ColumnTransformer` combina scalers y encoders segun el "
            "tipo de columna.\n"
            "- `.get_feature_names_out()` para inspeccionar la salida.\n"
            "- Arboles no necesitan escalado, pero si necesitan que las "
            "categoricas ya sean numericas.\n"
        ),
        difficulty="intermediate",
        category="ml-features",
        order=24,
        track="track-3",
        estimated_duration=50,
        prerequisites_titles=[
            "ML 2 · Metricas mas alla de accuracy",
        ],
        exercises=[
            ExerciseTemplate(
                title="Escalar train/test con StandardScaler",
                description=(
                    "Aprende los parametros del scaler SOLO con train y "
                    "aplicalos igual sobre test."
                ),
                instructions=(
                    "Implementa `escalar_train_test(X_train, X_test)` "
                    "que crea un `StandardScaler`, hace `fit_transform` "
                    "sobre `X_train`, hace `transform` sobre `X_test` "
                    "(NO fit) y devuelve la tupla `(X_train_s, X_test_s)` "
                    "como `np.ndarray`."
                ),
                starter_code=(
                    "from sklearn.preprocessing import StandardScaler\n"
                    "\n"
                    "\n"
                    "def escalar_train_test(X_train, X_test):\n"
                    "    # TODO: sc = StandardScaler()\n"
                    "    # TODO: X_train_s = sc.fit_transform(X_train)\n"
                    "    # TODO: X_test_s  = sc.transform(X_test)  # NO fit\n"
                    "    # TODO: retorna (X_train_s, X_test_s)\n"
                    "    ...\n"
                ),
                hints=[
                    "fit_transform SOLO sobre X_train — es la esencia de no leakage.",
                    "transform (sin fit) sobre X_test aplica media/std aprendidas.",
                    "El resultado es np.ndarray; los tests no asumen DataFrame.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "X_train_s tiene media 0 y std 1 por columna",
                        "code": (
                            "import numpy as np\n"
                            "X_train = np.array([[1.0, 100.0], [2.0, 200.0], [3.0, 300.0], [4.0, 400.0]])\n"
                            "X_test = np.array([[2.5, 250.0]])\n"
                            "X_train_s, X_test_s = escalar_train_test(X_train, X_test)\n"
                            "assert np.allclose(X_train_s.mean(axis=0), [0.0, 0.0], atol=1e-9), X_train_s.mean(axis=0)\n"
                            "assert np.allclose(X_train_s.std(axis=0), [1.0, 1.0], atol=1e-9), X_train_s.std(axis=0)"
                        ),
                    },
                    {
                        "name": "X_test se transforma con params de train (2.5,250 -> 0,0)",
                        "code": (
                            "import numpy as np\n"
                            "X_train = np.array([[1.0, 100.0], [2.0, 200.0], [3.0, 300.0], [4.0, 400.0]])\n"
                            "X_test = np.array([[2.5, 250.0]])\n"
                            "_, X_test_s = escalar_train_test(X_train, X_test)\n"
                            "assert np.allclose(X_test_s, [[0.0, 0.0]], atol=1e-9), X_test_s"
                        ),
                    },
                    {
                        "name": "no filtra info de test al scaler (leakage guard)",
                        "code": (
                            "import numpy as np\n"
                            "X_train = np.array([[1.0], [2.0], [3.0], [4.0]])\n"
                            "X_test  = np.array([[1000.0]])  # outlier extremo\n"
                            "X_train_s, _ = escalar_train_test(X_train, X_test)\n"
                            "# si el scaler se hubiera fitteado con test, el std seria enorme\n"
                            "# y X_train_s tendria valores minusculos. Aqui debe seguir teniendo std=1.\n"
                            "assert np.allclose(X_train_s.std(axis=0), [1.0], atol=1e-9), X_train_s.std(axis=0)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Pipeline con StandardScaler + LogisticRegression",
                description=(
                    "Envuelve el preprocesador y el modelo en un Pipeline "
                    "para evitar leakage por default."
                ),
                instructions=(
                    "Implementa `pipeline_logreg(X_train, y_train, "
                    "X_test, y_test)` que crea un `Pipeline` con dos "
                    "pasos: `('sc', StandardScaler())` y "
                    "`('lr', LogisticRegression(random_state=42, "
                    "max_iter=500))`. Entrena con `fit`, retorna la "
                    "accuracy sobre `X_test` como `float`."
                ),
                starter_code=(
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "\n"
                    "\n"
                    "def pipeline_logreg(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: pipe = Pipeline([('sc', StandardScaler()),\n"
                    "    #                        ('lr', LogisticRegression(random_state=42, max_iter=500))])\n"
                    "    # TODO: pipe.fit(X_train, y_train)\n"
                    "    # TODO: return float(pipe.score(X_test, y_test))\n"
                    "    ...\n"
                ),
                hints=[
                    "Pipeline([(nombre, estimador), ...]) — orden importa: primero preproc, ultimo modelo.",
                    "pipe.fit escala con train y entrena; pipe.score escala test con params de train y evalua.",
                    "Sobre iris con random_state=42 y stratify=y, el pipeline llega a 1.0.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "pipeline retorna float 1.0 sobre iris seed 42",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = pipeline_logreg(X_train, y_train, X_test, y_test)\n"
                            "assert isinstance(acc, float), type(acc)\n"
                            "assert acc == 1.0, acc"
                        ),
                    },
                    {
                        "name": "el pipeline corre y retorna accuracy valida",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = pipeline_logreg(X_train, y_train, X_test, y_test)\n"
                            "assert 0.0 <= acc <= 1.0"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="ColumnTransformer con numericas + categoricas",
                description=(
                    "Preprocesa un DataFrame heterogeneo mezclando "
                    "StandardScaler para numericas y OneHotEncoder para "
                    "categoricas en un solo objeto."
                ),
                instructions=(
                    "Implementa `preprocess_mixto(df, num_cols, cat_cols)` "
                    "que crea un `ColumnTransformer` con dos "
                    "transformadores: `('num', StandardScaler(), "
                    "num_cols)` y `('cat', OneHotEncoder(sparse_output="
                    "False, handle_unknown='ignore'), cat_cols)`. Hace "
                    "`fit_transform` sobre `df` y devuelve la matriz "
                    "resultante como `np.ndarray`."
                ),
                starter_code=(
                    "from sklearn.compose import ColumnTransformer\n"
                    "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
                    "\n"
                    "\n"
                    "def preprocess_mixto(df, num_cols, cat_cols):\n"
                    "    # TODO: ct = ColumnTransformer([\n"
                    "    #     ('num', StandardScaler(), num_cols),\n"
                    "    #     ('cat', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), cat_cols),\n"
                    "    # ])\n"
                    "    # TODO: retorna ct.fit_transform(df)\n"
                    "    ...\n"
                ),
                hints=[
                    "El orden en la lista define el orden de columnas de salida: primero numericas.",
                    "sparse_output=False evita tener que llamar .toarray() para inspeccionar el resultado.",
                    "handle_unknown='ignore' es la variante que no crashea con categorias nuevas.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "shape correcto (5, 5) = 2 num + 3 cat",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'edad': [25, 40, 30, 55, 22],\n"
                            "    'ingreso': [30000, 60000, 45000, 90000, 25000],\n"
                            "    'plan': ['basico', 'pro', 'basico', 'enterprise', 'basico'],\n"
                            "})\n"
                            "out = preprocess_mixto(df, ['edad', 'ingreso'], ['plan'])\n"
                            "assert out.shape == (5, 5), out.shape"
                        ),
                    },
                    {
                        "name": "columnas numericas escaladas a media 0 std 1",
                        "code": (
                            "import numpy as np\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'edad': [25, 40, 30, 55, 22],\n"
                            "    'ingreso': [30000, 60000, 45000, 90000, 25000],\n"
                            "    'plan': ['basico', 'pro', 'basico', 'enterprise', 'basico'],\n"
                            "})\n"
                            "out = preprocess_mixto(df, ['edad', 'ingreso'], ['plan'])\n"
                            "assert abs(out[:, 0].mean()) < 1e-9, out[:, 0].mean()\n"
                            "assert abs(out[:, 0].std() - 1.0) < 1e-9, out[:, 0].std()\n"
                            "assert abs(out[:, 1].mean()) < 1e-9\n"
                            "assert abs(out[:, 1].std() - 1.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "one-hot: cada fila tiene exactamente un 1 en las cols categoricas",
                        "code": (
                            "import numpy as np\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'edad': [25, 40, 30, 55, 22],\n"
                            "    'ingreso': [30000, 60000, 45000, 90000, 25000],\n"
                            "    'plan': ['basico', 'pro', 'basico', 'enterprise', 'basico'],\n"
                            "})\n"
                            "out = preprocess_mixto(df, ['edad', 'ingreso'], ['plan'])\n"
                            "one_hot = out[:, 2:5]\n"
                            "assert np.array_equal(one_hot.sum(axis=1), [1, 1, 1, 1, 1]), one_hot.sum(axis=1)\n"
                            "# alfabetico: 3 basico + 1 enterprise + 1 pro\n"
                            "assert one_hot.sum(axis=0).tolist() == [3.0, 1.0, 1.0], one_hot.sum(axis=0)"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 4 · Regresion: LinearRegression, MSE, RMSE y R2",
        description=(
            "Predecir un numero (no una clase): regresion lineal, "
            "metricas MSE/RMSE/R2 y Ridge para casos con "
            "multicolinealidad."
        ),
        content=(
            "# ML 4: regresion con LinearRegression\n\n"
            "Hasta aqui todo fue **clasificacion**: predecir una categoria "
            "(iris = setosa/versicolor/virginica, churn = 0/1). Este "
            "bloque cambia el juego: predecir un **numero continuo** — "
            "el precio de una casa, la demanda del proximo mes, el "
            "tiempo hasta el primer pago. Es **regresion**.\n\n"
            "## Tres ideas para regresion\n\n"
            "### 1. Clasificacion vs regresion: no es lo mismo\n\n"
            "El shape del problema cambia todo:\n\n"
            "| Aspecto             | Clasificacion         | Regresion             |\n"
            "|---------------------|-----------------------|-----------------------|\n"
            "| Target              | Categoria (0/1, A/B)  | Numero real           |\n"
            "| Modelo base         | LogisticRegression    | LinearRegression      |\n"
            "| Metrica intuitiva   | accuracy, f1          | MSE, RMSE, R2         |\n"
            "| `.score()` default  | accuracy              | R2                    |\n"
            '| Error tipico        | "clase mal predicha" | "me equivoque por X"  |\n\n'
            "El API de sklearn es identico: `fit`, `predict`, `score`. "
            "Solo cambian los estimadores y las metricas.\n\n"
            "### 2. LinearRegression aprende una combinacion lineal\n\n"
            "El modelo mas simple de regresion asume que:\n\n"
            "```\n"
            "y = w_1 * x_1 + w_2 * x_2 + ... + w_n * x_n + b\n"
            "```\n\n"
            "El entrenamiento encuentra los pesos `w_i` y el intercepto "
            "`b` que **minimizan el error cuadratico** sobre train.\n\n"
            "```python\n"
            "from sklearn.linear_model import LinearRegression\n\n"
            "modelo = LinearRegression()\n"
            "modelo.fit(X_train, y_train)\n\n"
            "# inspeccion\n"
            "print('coefs:', modelo.coef_)         # array de w_i\n"
            "print('intercept:', modelo.intercept_) # b\n\n"
            "y_pred = modelo.predict(X_test)       # array de floats\n"
            "```\n\n"
            "**Interpretacion:** si `coef_[0] == 3.0`, significa que "
            "cuando la feature 0 sube 1 unidad, `y` sube 3.0 unidades "
            "(manteniendo el resto constante). Este es el gran atractivo "
            "de LinReg: es **directamente interpretable**.\n\n"
            "### 3. Tres metricas para regresion\n\n"
            "**MSE (Mean Squared Error)** = media de `(y_true - y_pred)^2`. "
            "Penaliza mucho errores grandes (el cuadrado los "
            "amplifica). El problema: sus unidades son las del target "
            "**al cuadrado** — si predices precios en euros, MSE esta "
            "en euros^2, dificil de interpretar.\n\n"
            "**RMSE (Root Mean Squared Error)** = `sqrt(MSE)`. Vuelve a "
            "las unidades del target: RMSE=1500 sobre precios de casas "
            'significa "me equivoco tipicamente en 1500 euros". Es la '
            "metrica que reportas a un stakeholder.\n\n"
            "**R2 (coeficiente de determinacion)** = fraccion de la "
            "varianza de `y` que el modelo captura. Va de -inf a 1.0:\n"
            "- **R2 = 1.0**: predicciones perfectas.\n"
            "- **R2 = 0.0**: el modelo no mejora sobre predecir la "
            "media de `y`.\n"
            "- **R2 < 0**: el modelo es **peor** que predecir la media. "
            "Casi siempre significa que tienes un bug o un problema muy "
            "no-lineal para LinReg.\n\n"
            "```python\n"
            "from sklearn.metrics import mean_squared_error, r2_score\n"
            "import numpy as np\n\n"
            "mse  = mean_squared_error(y_test, y_pred)\n"
            "rmse = np.sqrt(mse)\n"
            "r2   = r2_score(y_test, y_pred)\n"
            "```\n\n"
            "> Alternativa reciente: `root_mean_squared_error` te da "
            "RMSE directo. El viejo flag `mean_squared_error(..., "
            "squared=False)` esta deprecado en sklearn 1.6+; usa "
            "`sqrt(mse)` o la nueva funcion.\n\n"
            "## Ridge: regresion con regularizacion\n\n"
            "Cuando dos features son casi identicas (**multicolinealidad**), "
            "LinearRegression puede asignar pesos absurdos (uno "
            "positivo enorme y el otro negativo enorme que se "
            "cancelan). Es matematicamente correcto pero pesimo para "
            "generalizar.\n\n"
            "**Ridge** agrega una penalizacion al tamano de los coefs "
            "(`alpha * ||w||^2` al costo). Los pesos quedan mas "
            "chicos y balanceados:\n\n"
            "```python\n"
            "from sklearn.linear_model import Ridge\n\n"
            "modelo = Ridge(alpha=1.0)  # alpha=0 == LinReg; alpha grande == mas penalizacion\n"
            "modelo.fit(X_train, y_train)\n"
            "```\n\n"
            "**Regla de dedo:** si tienes features correlacionadas o "
            "notas coefs raros, cambia `LinearRegression()` por "
            "`Ridge(alpha=1.0)` como default. La perdida en R2 sobre "
            "train es minima y ganas robustez.\n\n"
            "**Lasso** (`Lasso(alpha=0.1)`) es similar pero manda "
            "algunos coefs a exactamente **cero** — util para feature "
            "selection automatica. Ridge y Lasso son las dos formas "
            "canonicas de regularizacion lineal (L2 y L1 "
            "respectivamente).\n\n"
            "## El pipeline completo de regresion\n\n"
            "Combinando lo de leccion anterior:\n\n"
            "```python\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import Ridge\n\n"
            "pipe = Pipeline([\n"
            "    ('sc', StandardScaler()),   # escalar es importante para Ridge/Lasso\n"
            "    ('reg', Ridge(alpha=1.0)),\n"
            "])\n"
            "pipe.fit(X_train, y_train)\n"
            "rmse = np.sqrt(mean_squared_error(y_test, pipe.predict(X_test)))\n"
            "```\n\n"
            "**Ridge y Lasso SI necesitan escalado**: la penalizacion es "
            "sobre `||w||`, y una feature en escala grande naturalmente "
            "tiene coef pequeno — la regularizacion la castigaria menos "
            "sin escalar. StandardScaler nivela el terreno.\n\n"
            "## Errores comunes\n\n"
            "1. **Reportar R2 sin contexto** — un R2 de 0.6 puede ser "
            "excelente en un dominio ruidoso (finanzas) y terrible en "
            "otro (fisica de laboratorio). Siempre comparalo contra un "
            "baseline trivial (predecir la media).\n"
            '2. **RMSE sin unidades** — "mi modelo tiene RMSE=1500" '
            'no significa nada; "me equivoco tipicamente en 1500 euros '
            'sobre precios que van de 50k a 500k" es una frase util.\n'
            "3. **LinReg sobre datos no-lineales** — si el patron real "
            "es `y = x^2`, LinReg tendra R2 mediocre por diseno. Prueba "
            "PolynomialFeatures o un modelo no-lineal (arbol, RF).\n"
            "4. **Regularizar sin escalar** — Ridge y Lasso asumen "
            "features en escala similar. Sin StandardScaler la "
            "regularizacion pesa mas a features de escala pequena.\n"
            "5. **Ignorar residuos** — R2 alto no significa que los "
            "errores esten uniformemente distribuidos. Grafica "
            "`y_pred vs residuos` para detectar patrones no capturados.\n\n"
            "## Resumen\n\n"
            "- Regresion predice un numero: `LinearRegression` es el "
            "modelo base, mismo API (`fit`, `predict`, `score`) que "
            "clasificacion.\n"
            "- Metricas: MSE (unidades^2), RMSE (unidades del target, "
            "el que reportas), R2 (fraccion de varianza explicada, "
            "compare-friendly).\n"
            "- Con multicolinealidad o riesgo de overfitting, usa "
            "`Ridge(alpha=1.0)` como default. Escala las features "
            "antes.\n"
            "- Interpretabilidad: `coef_` te dice cuanto sube `y` por "
            "unidad de cada feature; `intercept_` es el valor esperado "
            "cuando todas las features son 0.\n"
        ),
        difficulty="intermediate",
        category="ml-regresion",
        order=25,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "ML 3 · Features escaladas y Pipelines",
        ],
        exercises=[
            ExerciseTemplate(
                title="Evaluar LinearRegression con MSE y R2",
                description=(
                    "Entrena un modelo lineal y devuelve las metricas "
                    "clasicas de regresion como dict."
                ),
                instructions=(
                    "Implementa `evaluar_regresion(X_train, y_train, "
                    "X_test, y_test)` que entrena un `LinearRegression`, "
                    "predice sobre test y retorna un `dict` con las "
                    "claves `mse`, `rmse`, `r2` (todos floats). "
                    "Usa `mean_squared_error` para MSE, "
                    "`math.sqrt(mse)` o `numpy.sqrt(mse)` para RMSE y "
                    "`r2_score` para R2."
                ),
                starter_code=(
                    "import math\n"
                    "from sklearn.linear_model import LinearRegression\n"
                    "from sklearn.metrics import mean_squared_error, r2_score\n"
                    "\n"
                    "\n"
                    "def evaluar_regresion(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: entrena LinearRegression().fit(X_train, y_train)\n"
                    "    # TODO: y_pred = modelo.predict(X_test)\n"
                    "    # TODO: retorna dict con 'mse', 'rmse' (=sqrt(mse)), 'r2'\n"
                    "    ...\n"
                ),
                hints=[
                    "float(mean_squared_error(y_test, y_pred)) evita numpy.float64.",
                    "rmse = math.sqrt(mse). No hay que llamar mean_squared_error dos veces.",
                    "Sobre y = 2x + 1 exacto, MSE deberia ser 0 y R2 igual a 1.0.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "y = 2x + 1 exacto: mse=0, rmse=0, r2=1",
                        "code": (
                            "import math\n"
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0],[2.0],[3.0],[4.0],[5.0]])\n"
                            "y_tr = np.array([3.0, 5.0, 7.0, 9.0, 11.0])\n"
                            "X_te = np.array([[6.0],[7.0]])\n"
                            "y_te = np.array([13.0, 15.0])\n"
                            "res = evaluar_regresion(X_tr, y_tr, X_te, y_te)\n"
                            "assert set(res.keys()) == {'mse','rmse','r2'}, res.keys()\n"
                            "assert math.isclose(res['mse'], 0.0, abs_tol=1e-9), res\n"
                            "assert math.isclose(res['rmse'], 0.0, abs_tol=1e-9), res\n"
                            "assert math.isclose(res['r2'], 1.0, abs_tol=1e-9), res"
                        ),
                    },
                    {
                        "name": "todas las metricas son floats",
                        "code": (
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0],[2.0],[3.0]])\n"
                            "y_tr = np.array([2.0, 4.0, 7.0])\n"
                            "X_te = np.array([[4.0],[5.0]])\n"
                            "y_te = np.array([8.0, 10.0])\n"
                            "res = evaluar_regresion(X_tr, y_tr, X_te, y_te)\n"
                            "for v in res.values():\n"
                            "    assert isinstance(v, float), type(v)"
                        ),
                    },
                    {
                        "name": "rmse = sqrt(mse) siempre",
                        "code": (
                            "import math\n"
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0],[2.0],[3.0]])\n"
                            "y_tr = np.array([2.0, 4.0, 7.0])  # no lineal\n"
                            "X_te = np.array([[4.0],[5.0]])\n"
                            "y_te = np.array([8.0, 10.0])\n"
                            "res = evaluar_regresion(X_tr, y_tr, X_te, y_te)\n"
                            "assert math.isclose(res['rmse'], math.sqrt(res['mse']), abs_tol=1e-9), res"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Predecir valores nuevos",
                description=(
                    "Entrena un LinearRegression y usalo para predecir "
                    "puntos que no vio."
                ),
                instructions=(
                    "Implementa `predecir_lineal(X_train, y_train, "
                    "X_nuevo)` que entrena un `LinearRegression` sobre "
                    "train y devuelve `model.predict(X_nuevo)` como "
                    "`np.ndarray`. Los tests pasan datos exactos y "
                    "verifican predicciones conocidas."
                ),
                starter_code=(
                    "from sklearn.linear_model import LinearRegression\n"
                    "\n"
                    "\n"
                    "def predecir_lineal(X_train, y_train, X_nuevo):\n"
                    "    # TODO: modelo = LinearRegression().fit(X_train, y_train)\n"
                    "    # TODO: return modelo.predict(X_nuevo)\n"
                    "    ...\n"
                ),
                hints=[
                    "predict acepta una matriz 2D — para un solo punto pasa [[x1, x2, ...]].",
                    "Sobre y = 2x + 1, pred(10) = 21 y pred(20) = 41.",
                    "El return de predict es np.ndarray; no lo conviertas a lista.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "y = 2x+1 exacto: pred(10)=21, pred(20)=41",
                        "code": (
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0],[2.0],[3.0],[4.0],[5.0]])\n"
                            "y_tr = np.array([3.0, 5.0, 7.0, 9.0, 11.0])\n"
                            "X_new = np.array([[10.0],[20.0]])\n"
                            "pred = predecir_lineal(X_tr, y_tr, X_new)\n"
                            "assert isinstance(pred, np.ndarray), type(pred)\n"
                            "assert np.allclose(pred, [21.0, 41.0], atol=1e-9), pred"
                        ),
                    },
                    {
                        "name": "regresion multivariable: y = 3*x1 + 2*x2 + 1",
                        "code": (
                            "import numpy as np\n"
                            "X_tr = np.array([\n"
                            "    [0.0, 0.0], [1.0, 0.0], [0.0, 1.0],\n"
                            "    [1.0, 1.0], [2.0, 3.0], [4.0, 2.0],\n"
                            "])\n"
                            "y_tr = np.array([1.0, 4.0, 3.0, 6.0, 13.0, 17.0])  # 3*x1 + 2*x2 + 1\n"
                            "X_new = np.array([[5.0, 5.0], [10.0, 0.0]])\n"
                            "pred = predecir_lineal(X_tr, y_tr, X_new)\n"
                            "assert np.allclose(pred, [26.0, 31.0], atol=1e-9), pred"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Ridge vs LinearRegression con multicolinealidad",
                description=(
                    "Demuestra el valor de la regularizacion: Ridge "
                    "reparte los coefs entre features colineales "
                    "manteniendo R2 competitivo."
                ),
                instructions=(
                    "Implementa `comparar_lin_vs_ridge(X_train, "
                    "y_train, X_test, y_test, alpha)` que entrena un "
                    "`LinearRegression` y un `Ridge(alpha=alpha, "
                    "random_state=42)` sobre el mismo train, y devuelve "
                    "un `dict` con las claves `lin_r2`, `ridge_r2`, "
                    "`lin_coefs_norm`, `ridge_coefs_norm`. Usa "
                    "`numpy.linalg.norm(model.coef_)` para la norma L2 "
                    "de los coefs."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "from sklearn.linear_model import LinearRegression, Ridge\n"
                    "from sklearn.metrics import r2_score\n"
                    "\n"
                    "\n"
                    "def comparar_lin_vs_ridge(X_train, y_train, X_test, y_test, alpha):\n"
                    "    # TODO: entrena LinReg y Ridge(alpha=alpha, random_state=42)\n"
                    "    # TODO: retorna dict con 'lin_r2', 'ridge_r2',\n"
                    "    #       'lin_coefs_norm', 'ridge_coefs_norm'\n"
                    "    ...\n"
                ),
                hints=[
                    "np.linalg.norm(model.coef_) es la norma L2 (sqrt(sum(w_i^2))).",
                    "float(np.linalg.norm(...)) para asegurar Python float en el dict.",
                    "Con features casi identicas, ||coefs_ridge|| < ||coefs_lin|| casi siempre.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "estructura del dict y tipos",
                        "code": (
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0, 1.0],[2.0, 2.0],[3.0, 3.0],[4.0, 4.0]])\n"
                            "y_tr = np.array([2.0, 4.0, 6.0, 8.0])\n"
                            "X_te = np.array([[5.0, 5.0],[6.0, 6.0]])\n"
                            "y_te = np.array([10.0, 12.0])\n"
                            "res = comparar_lin_vs_ridge(X_tr, y_tr, X_te, y_te, alpha=1.0)\n"
                            "assert set(res.keys()) == {'lin_r2','ridge_r2','lin_coefs_norm','ridge_coefs_norm'}, res.keys()\n"
                            "for v in res.values():\n"
                            "    assert isinstance(v, float), type(v)"
                        ),
                    },
                    {
                        "name": "Ridge reduce ||coefs|| bajo multicolinealidad",
                        "code": (
                            "import numpy as np\n"
                            "# features casi identicas (x1 ~ x2)\n"
                            "X_tr = np.array([\n"
                            "    [1.0, 1.01],[2.0, 2.02],[3.0, 3.01],\n"
                            "    [4.0, 4.02],[5.0, 5.03],[6.0, 6.01],[7.0, 7.02],\n"
                            "])\n"
                            "y_tr = np.array([3.0, 5.0, 7.0, 9.0, 11.0, 13.0, 15.0])\n"
                            "X_te = np.array([[8.0, 8.03],[9.0, 9.01],[10.0, 10.02]])\n"
                            "y_te = np.array([17.0, 19.0, 21.0])\n"
                            "res = comparar_lin_vs_ridge(X_tr, y_tr, X_te, y_te, alpha=1.0)\n"
                            "assert res['ridge_coefs_norm'] < res['lin_coefs_norm'], res\n"
                            "# ambos deben tener r2 razonables\n"
                            "assert res['lin_r2'] > 0.9, res\n"
                            "assert res['ridge_r2'] > 0.9, res"
                        ),
                    },
                    {
                        "name": "alpha minusculo hace que Ridge tienda a LinReg",
                        "code": (
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0, 1.01],[2.0, 2.02],[3.0, 3.01],[4.0, 4.02]])\n"
                            "y_tr = np.array([3.0, 5.0, 7.0, 9.0])\n"
                            "X_te = np.array([[5.0, 5.02]])\n"
                            "y_te = np.array([11.0])\n"
                            "res = comparar_lin_vs_ridge(X_tr, y_tr, X_te, y_te, alpha=1e-6)\n"
                            "# con alpha minusculo, las normas casi coinciden\n"
                            "assert abs(res['lin_coefs_norm'] - res['ridge_coefs_norm']) < 0.1, res"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 5 · Arboles y Random Forest",
        description=(
            "Primer modelo no-lineal: DecisionTree y RandomForest. "
            "Interpretabilidad via feature_importances_ y por que "
            "RF suele ser el mejor baseline en tabular."
        ),
        content=(
            "# ML 5: arboles de decision y Random Forest\n\n"
            "Todos los modelos que has visto (LogReg, LinReg, Ridge) son "
            "**lineales**: buscan una combinacion lineal de features + "
            "un umbral. Con relaciones no-lineales o interacciones "
            "entre features, no dan la talla. Este bloque presenta los "
            "**arboles de decision** y su ensamble estrella: **Random "
            "Forest** — el default no-lineal que casi siempre te da un "
            "baseline competitivo en datos tabulares.\n\n"
            "## Tres ideas para entender arboles\n\n"
            "### 1. Un arbol es una serie de if-then sobre features\n\n"
            "Un DecisionTree divide el espacio en rectangulos. En cada "
            "nodo elige una feature y un umbral que **maximiza la "
            "pureza** de los grupos resultantes (usa Gini o entropia "
            "para clasificacion, MSE para regresion).\n\n"
            "```\n"
            "raiz:  petal_width <= 0.8 ?\n"
            "  si  -> setosa                        # nodo hoja puro\n"
            "  no  -> petal_length <= 4.75 ?\n"
            "        si -> versicolor                # nodo hoja\n"
            "        no -> virginica                 # nodo hoja\n"
            "```\n\n"
            "Ventajas frente a modelos lineales:\n\n"
            "- **No-linealidad**: aprende umbrales, no combinaciones "
            "lineales.\n"
            "- **Sin escalado**: cada split usa una feature aislada; "
            "escalar no cambia nada.\n"
            "- **Sin one-hot obligatorio** para ordinales: puede "
            "particionar por umbral en enteros (0/1/2/3).\n"
            "- **Interpretabilidad**: puedes imprimir el arbol y ver "
            "cada regla.\n\n"
            "Desventaja: **overfittean facil**. Sin restriccion, un "
            "arbol memoriza el train con hojas de una sola muestra. Por "
            "eso siempre se usa con `max_depth` o `min_samples_leaf`.\n\n"
            "```python\n"
            "from sklearn.tree import DecisionTreeClassifier\n\n"
            "arbol = DecisionTreeClassifier(max_depth=3, random_state=42)\n"
            "arbol.fit(X_train, y_train)\n"
            "acc = arbol.score(X_test, y_test)\n"
            "```\n\n"
            "**Parametros que casi siempre tocas:**\n"
            "- `max_depth`: limite duro de profundidad. 3-10 es lo "
            "tipico.\n"
            "- `min_samples_leaf`: minimo de muestras por hoja. "
            "Valores 5-20 evitan hojas ruidosas.\n"
            "- `random_state`: reproducibilidad — sklearn desempata "
            "features iguales al azar.\n\n"
            "### 2. Random Forest promedia muchos arboles\n\n"
            "Un arbol solo es de alta varianza (cambias 3 filas y sale "
            "otro arbol distinto). La idea de **Random Forest** es "
            "entrenar N arboles independientes con dos tipos de "
            "aleatoriedad y promediar sus predicciones:\n\n"
            "1. **Bootstrap sampling**: cada arbol ve un subset "
            "aleatorio de las filas (con reemplazo).\n"
            "2. **Feature subsampling**: en cada split, solo puede "
            "elegir entre `sqrt(n_features)` features (para "
            "clasificacion; `n_features/3` para regresion).\n\n"
            "El promedio reduce varianza sin subir el sesgo. Resultado: "
            "**mismo bias que un arbol solo, mucho menos varianza**.\n\n"
            "```python\n"
            "from sklearn.ensemble import RandomForestClassifier\n\n"
            "rf = RandomForestClassifier(n_estimators=100, random_state=42)\n"
            "rf.fit(X_train, y_train)\n"
            "acc = rf.score(X_test, y_test)\n"
            "```\n\n"
            "**Parametros clave:**\n"
            "- `n_estimators`: cuantos arboles. 100 es el default; "
            "500 rara vez es peor pero tarda mas. Nunca es "
            '"demasiados".\n'
            "- `max_depth`, `min_samples_leaf`: se aplican por arbol.\n"
            "- `n_jobs=-1`: paraleliza el entrenamiento en todos los "
            "cores.\n\n"
            "### 3. feature_importances_: que features usa el modelo\n\n"
            "Tanto DecisionTree como RandomForest exponen "
            "`feature_importances_`: un array de floats en [0, 1] que "
            "suman 1, indicando cuanto contribuye cada feature a las "
            "decisiones del modelo (medido por la reduccion de "
            "impureza que trae al agregarla).\n\n"
            "```python\n"
            "importances = dict(zip(feature_names, rf.feature_importances_))\n"
            "# {'sepal_length': 0.12, 'sepal_width': 0.04,\n"
            "#  'petal_length': 0.40, 'petal_width': 0.44}\n"
            "```\n\n"
            "Interpretacion sobre iris: `petal_width` y `petal_length` "
            "son las que discriminan las especies; `sepal_width` casi "
            "no aporta. Esto **matchea** lo que sabemos del dataset — "
            "un buen indicador de que el modelo aprendio patrones "
            "reales.\n\n"
            "**Uso en la practica:**\n"
            "- Debugging: si una feature que crees importante aparece "
            "con importancia 0, algo esta raro (bug en pipeline, "
            "leakage, feature constante).\n"
            "- Feature selection: entrenas un RF con todas, tiras las "
            "importances=0, reentrenas con menos features (mismo "
            "score, mas rapido).\n"
            "- Storytelling: reportar al stakeholder que features "
            "guian las predicciones (interpretabilidad de alto nivel).\n\n"
            "**Cuidado:** `feature_importances_` esta **sesgada hacia "
            "features de alta cardinalidad** (numericas continuas o "
            "categoricas con muchos niveles) y hacia features "
            "correlacionadas (comparten importancia). Para "
            "interpretabilidad seria, usa `permutation_importance` o "
            "SHAP.\n\n"
            "## Cuando usar cada uno\n\n"
            "| Escenario                              | Modelo         |\n"
            "|----------------------------------------|----------------|\n"
            "| Necesitas explicar cada decision       | DecisionTree   |\n"
            "| Datos tabulares, primer baseline       | RandomForest   |\n"
            "| Muchas features numericas correladas   | RF > LinReg    |\n"
            "| Interacciones no-lineales entre features | RF, no LinReg  |\n"
            "| Fronteras suaves (imagenes, senales)   | Redes neuronales|\n"
            "| Dataset gigante (>10M filas)           | GradientBoosting/LightGBM |\n\n"
            "## Errores comunes\n\n"
            "1. **Arbol sin `max_depth`** — memoriza el train, R2 en "
            "test bajo. Empieza siempre con `max_depth=3-10`.\n"
            "2. **Escalar antes de un arbol** — no rompe nada pero es "
            "trabajo inutil. RF es invariante a la escala.\n"
            "3. **`n_estimators=10`** — ahorra segundos y sacrifica "
            "estabilidad. 100 es el minimo razonable en produccion.\n"
            "4. **Interpretar `feature_importances_` como causalidad** "
            '— importancia no es causa; solo dice "el modelo se '
            'apoyo en esta feature".\n'
            "5. **Olvidar `random_state`** — dos RF con distinta "
            "semilla pueden dar accuracies ligeramente distintas por "
            "el bootstrap. Fijala para experimentos comparables.\n\n"
            "## Resumen\n\n"
            "- `DecisionTree` particiona el espacio con if-then; es "
            "no-lineal, interpretable, no necesita escalado. "
            "Regularizalo con `max_depth`.\n"
            "- `RandomForest` = promedio de muchos arboles con "
            "bootstrap + feature subsampling. Reduce varianza. Baseline "
            "por defecto en tabular.\n"
            "- `feature_importances_` te dice que features usa el "
            "modelo (utilidad grande para debug + storytelling; ojo con "
            "sesgos hacia alta cardinalidad).\n"
            "- Cuando quieras un modelo lineal-interpretable, usa "
            "LogReg/LinReg + coefs; cuando quieras potencia sin tunear, "
            "usa RandomForest con `n_estimators=100`.\n"
        ),
        difficulty="intermediate",
        category="ml-arboles",
        order=26,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "ML 4 · Regresion: LinearRegression, MSE, RMSE y R2",
        ],
        exercises=[
            ExerciseTemplate(
                title="DecisionTree con max_depth sobre iris",
                description=(
                    "Entrena un arbol de decision con profundidad "
                    "limitada y devuelve accuracy."
                ),
                instructions=(
                    "Implementa `entrenar_arbol(X_train, y_train, "
                    "X_test, y_test, max_depth)` que crea un "
                    "`DecisionTreeClassifier(max_depth=max_depth, "
                    "random_state=42)`, lo entrena con `fit` y devuelve "
                    "la accuracy sobre `X_test` como `float`."
                ),
                starter_code=(
                    "from sklearn.tree import DecisionTreeClassifier\n"
                    "\n"
                    "\n"
                    "def entrenar_arbol(X_train, y_train, X_test, y_test, max_depth):\n"
                    "    # TODO: dt = DecisionTreeClassifier(max_depth=max_depth, random_state=42)\n"
                    "    # TODO: dt.fit(X_train, y_train)\n"
                    "    # TODO: return float(dt.score(X_test, y_test))\n"
                    "    ...\n"
                ),
                hints=[
                    "random_state=42 es imprescindible para reproducibilidad en split-ties.",
                    "score() en clasificadores devuelve accuracy por default.",
                    "Sobre iris con seed 42 + stratify, max_depth=3 llega a 1.0.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "acc = 1.0 en iris con max_depth=3",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = entrenar_arbol(X_tr, y_tr, X_te, y_te, max_depth=3)\n"
                            "assert isinstance(acc, float), type(acc)\n"
                            "assert acc == 1.0, acc"
                        ),
                    },
                    {
                        "name": "max_depth=1 da accuracy menor (arbol subajustado)",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc_1 = entrenar_arbol(X_tr, y_tr, X_te, y_te, max_depth=1)\n"
                            "# depth=1 solo separa una clase => acc <= 0.75\n"
                            "assert acc_1 <= 0.75, acc_1"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="RandomForest con n_estimators",
                description=(
                    "Entrena un Random Forest y compara accuracy con " "un arbol solo."
                ),
                instructions=(
                    "Implementa `entrenar_rf(X_train, y_train, X_test, "
                    "y_test, n_estimators)` que crea un "
                    "`RandomForestClassifier(n_estimators=n_estimators, "
                    "random_state=42)`, lo entrena y devuelve la "
                    "accuracy sobre `X_test` como `float`."
                ),
                starter_code=(
                    "from sklearn.ensemble import RandomForestClassifier\n"
                    "\n"
                    "\n"
                    "def entrenar_rf(X_train, y_train, X_test, y_test, n_estimators):\n"
                    "    # TODO: rf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)\n"
                    "    # TODO: rf.fit(X_train, y_train)\n"
                    "    # TODO: return float(rf.score(X_test, y_test))\n"
                    "    ...\n"
                ),
                hints=[
                    "n_estimators es el numero de arboles del bosque.",
                    "random_state=42 fija el bootstrap y feature subsampling para reproducibilidad.",
                    "Sobre iris seed 42, RF con 100 arboles llega a 1.0.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "RF con 100 arboles = 1.0 sobre iris seed 42",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = entrenar_rf(X_tr, y_tr, X_te, y_te, n_estimators=100)\n"
                            "assert isinstance(acc, float), type(acc)\n"
                            "assert acc == 1.0, acc"
                        ),
                    },
                    {
                        "name": "RF con n_estimators=1 (basicamente un arbol) da acc menor con datos ruidosos",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "# datos con ruido para que RF-100 supere a RF-1\n"
                            "rng = np.random.default_rng(42)\n"
                            "X = rng.uniform(0, 10, size=(200, 4))\n"
                            "y = (X[:, 0] + X[:, 1] > 10).astype(int)\n"
                            "# meter ruido en 20 filas\n"
                            "flip = rng.choice(200, size=20, replace=False)\n"
                            "y[flip] = 1 - y[flip]\n"
                            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc_1 = entrenar_rf(X_tr, y_tr, X_te, y_te, n_estimators=1)\n"
                            "acc_100 = entrenar_rf(X_tr, y_tr, X_te, y_te, n_estimators=100)\n"
                            "# El promedio de 100 arboles reduce varianza -> acc_100 >= acc_1\n"
                            "assert acc_100 >= acc_1, (acc_1, acc_100)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="feature_importances_ ordenadas",
                description=(
                    "Extrae las importancias de features de un "
                    "RandomForest y ordenalas descendentemente."
                ),
                instructions=(
                    "Implementa `importancias_ordenadas(X_train, "
                    "y_train, feature_names)` que entrena un "
                    "`RandomForestClassifier(n_estimators=100, "
                    "random_state=42)` sobre train, extrae "
                    "`feature_importances_` y devuelve una `list` de "
                    "tuplas `(nombre, importancia_float)` ordenada "
                    "**descendentemente** por importancia."
                ),
                starter_code=(
                    "from sklearn.ensemble import RandomForestClassifier\n"
                    "\n"
                    "\n"
                    "def importancias_ordenadas(X_train, y_train, feature_names):\n"
                    "    # TODO: entrena RF con n_estimators=100 y random_state=42\n"
                    "    # TODO: pares = list(zip(feature_names, rf.feature_importances_))\n"
                    "    # TODO: retorna sorted(pares, key=..., reverse=True)\n"
                    "    ...\n"
                ),
                hints=[
                    "sorted(pares, key=lambda t: t[1], reverse=True) ordena por importancia desc.",
                    "float(imp) en la tupla para evitar numpy.float64.",
                    "feature_importances_ suman ~1.0 en RF (con tolerancia de flotante).",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "importancias suman ~1.0 y estan ordenadas desc",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "res = importancias_ordenadas(X_tr, y_tr, list(X.columns))\n"
                            "assert isinstance(res, list), type(res)\n"
                            "assert len(res) == 4, len(res)\n"
                            "# ordenadas desc\n"
                            "vals = [imp for _, imp in res]\n"
                            "assert vals == sorted(vals, reverse=True), vals\n"
                            "# suman aprox 1.0\n"
                            "assert abs(sum(vals) - 1.0) < 1e-6, sum(vals)"
                        ),
                    },
                    {
                        "name": "top feature es petal_width o petal_length en iris seed 42",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "res = importancias_ordenadas(X_tr, y_tr, list(X.columns))\n"
                            "top_name, top_imp = res[0]\n"
                            "assert top_name in {'petal_width', 'petal_length'}, top_name\n"
                            "# sepal_width debe ser el ultimo con importancia muy chica\n"
                            "last_name, last_imp = res[-1]\n"
                            "assert last_imp < 0.1, res"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 6 · Cross-validation y GridSearchCV",
        description=(
            "Evaluar modelos de forma honesta con K-Fold y encontrar "
            "hiperparametros con GridSearchCV. Fin de la ilusion de "
            "una sola accuracy."
        ),
        content=(
            "# ML 6: cross-validation y GridSearchCV\n\n"
            "Un solo `train_test_split` te da **una** accuracy. Suena "
            "razonable, pero esa accuracy depende de que muestras "
            "cayeron en el test — cambia el `random_state` y sale otra. "
            "Peor: si eliges hiperparametros mirando ese test, te "
            "**enganas a ti mismo** (data leakage sutil). Este bloque "
            "resuelve ambos problemas con **cross-validation** y "
            "**GridSearchCV**.\n\n"
            "## Tres ideas para entender CV\n\n"
            "### 1. K-Fold: promediar sobre varios splits\n\n"
            "En vez de un split unico, divide el dataset en **K partes** "
            "(folds). Entrena K veces: cada fold es el test una vez, y "
            "los otros K-1 folds son el train. Al final tienes K "
            "accuracies — su **media** es una estimacion mucho mas "
            "estable que un solo split.\n\n"
            "```\n"
            "K=5:\n"
            "  fold 1: [test][train][train][train][train]\n"
            "  fold 2: [train][test][train][train][train]\n"
            "  fold 3: [train][train][test][train][train]\n"
            "  fold 4: [train][train][train][test][train]\n"
            "  fold 5: [train][train][train][train][test]\n"
            "  scores = [0.96, 1.00, 0.93, 0.96, 1.00]\n"
            "  mean = 0.97, std = 0.025\n"
            "```\n\n"
            "```python\n"
            "from sklearn.model_selection import cross_val_score\n"
            "from sklearn.linear_model import LogisticRegression\n\n"
            "lr = LogisticRegression(max_iter=1000, random_state=42)\n"
            "scores = cross_val_score(lr, X, y, cv=5)\n"
            "print(scores.mean(), scores.std())\n"
            "```\n\n"
            "**Que te da CV que un split no te da:**\n\n"
            "- **Estimacion estable**: promedio de K medidas independientes.\n"
            "- **Desviacion**: `scores.std()` te dice cuanto varia el "
            "modelo entre folds. Std alta = modelo inestable.\n"
            "- **Usa todo el dataset**: cada fila aparece en train Y en "
            "test (en folds distintos). Sin desperdicio.\n\n"
            "**Reglas practicas para K:**\n\n"
            "- `cv=5` o `cv=10` son los estandares. 5 mas rapido; 10 "
            "mas robusto.\n"
            "- Con datasets pequenos, sube K (K=10, incluso "
            "leave-one-out K=N).\n"
            "- Con datasets grandes, baja K (K=3 o incluso 2) — cada "
            "fold ya es grande.\n\n"
            "### 2. StratifiedKFold: preserva la proporcion de clases\n\n"
            "Por default, `cross_val_score` con un clasificador usa "
            "`StratifiedKFold`: cada fold mantiene la misma proporcion "
            "de clases que el dataset completo. Esto es **imprescindible** "
            "en clasificacion desbalanceada — sin stratify, un fold "
            "podria quedar con 0% de la clase minoritaria y las metricas "
            "explotan.\n\n"
            "```python\n"
            "from sklearn.model_selection import StratifiedKFold\n\n"
            "skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n"
            "scores = cross_val_score(lr, X, y, cv=skf)\n"
            "```\n\n"
            "Para regresion no hay clases que estratificar; se usa "
            "`KFold` normal.\n\n"
            "### 3. GridSearchCV: probar combinaciones de hiperparametros\n\n"
            "Elegir `max_depth=3` a ojo es adivinar. `GridSearchCV` "
            "prueba **todas las combinaciones** de un `param_grid` con "
            "CV interno y te devuelve la mejor:\n\n"
            "```python\n"
            "from sklearn.model_selection import GridSearchCV\n"
            "from sklearn.tree import DecisionTreeClassifier\n\n"
            "param_grid = {'max_depth': [1, 2, 3, 5, 10]}\n"
            "gs = GridSearchCV(\n"
            "    DecisionTreeClassifier(random_state=42),\n"
            "    param_grid,\n"
            "    cv=5,\n"
            ")\n"
            "gs.fit(X, y)\n"
            "print(gs.best_params_)   # {'max_depth': 3}\n"
            "print(gs.best_score_)    # 0.9733 (media CV del mejor)\n"
            "print(gs.best_estimator_)  # DecisionTreeClassifier(max_depth=3, ...)\n"
            "```\n\n"
            "**Que hace GridSearchCV por dentro:**\n\n"
            "1. Genera todas las combinaciones del `param_grid` "
            "(producto cartesiano).\n"
            "2. Para cada combinacion, corre `cross_val_score(cv=5)`.\n"
            "3. Selecciona la combinacion con la media mas alta.\n"
            "4. **Reentrena** el mejor modelo con **todo** el dataset "
            "de entrada (por eso `best_estimator_` esta listo para "
            "predecir).\n\n"
            "**Multiples hiperparametros = producto cartesiano:**\n\n"
            "```python\n"
            "param_grid = {\n"
            "    'max_depth': [3, 5, 10],\n"
            "    'min_samples_leaf': [1, 5, 10],\n"
            "}\n"
            "# GridSearchCV probara 3 * 3 = 9 combinaciones\n"
            "```\n\n"
            "Cuando el grid se pone grande (>50 combinaciones) usa "
            "`RandomizedSearchCV` — muestrea N combinaciones al azar en "
            "vez de exhaustivo. Casi tan bueno, mucho mas rapido.\n\n"
            "## Nested CV: el estandar de oro\n\n"
            "Si usas GridSearchCV para elegir hiperparametros **y** "
            "reportas `best_score_` como tu accuracy final, estas "
            "**contaminando** — elegiste el hiperparametro mirando el "
            "mismo CV que ahora reportas. El estandar riguroso es "
            "**nested CV**: un CV externo para estimar performance y "
            "un CV interno (dentro de GridSearchCV) para tunear.\n\n"
            "```python\n"
            "from sklearn.model_selection import cross_val_score, GridSearchCV\n\n"
            "gs = GridSearchCV(DecisionTreeClassifier(random_state=42),\n"
            "                  {'max_depth': [3, 5, 10]}, cv=5)\n"
            "final = cross_val_score(gs, X, y, cv=5)  # nested\n"
            "print(final.mean())  # accuracy honesta\n"
            "```\n\n"
            "En la practica esto es 25x mas costoso. Muchos proyectos "
            "se conforman con un `train / val / test` clasico: tunean "
            "con GridSearchCV sobre train+val, y reportan sobre el test "
            "intocado.\n\n"
            "## Errores comunes\n\n"
            "1. **Reportar `best_score_` como accuracy de produccion** "
            "— es optimista; usa un test set separado o nested CV.\n"
            "2. **CV sin stratify en desbalanceado** — folds sin la "
            "clase minoritaria = metricas rotas. `cross_val_score` "
            "con clasificador ya lo hace por default; con "
            "regresion/pipeline custom, verificalo.\n"
            "3. **Escalar antes de CV** — data leakage: el scaler ve "
            "medias del test. Solucion: envolver el modelo en un "
            "`Pipeline` y pasar el pipeline a `cross_val_score`.\n"
            "4. **Grid gigante sin sentido** — probar 500 combinaciones "
            "cuando 20 dan la misma respuesta. Empieza pequeno, "
            "expande solo si el mejor esta en el borde del grid.\n"
            "5. **K muy alto con datasets grandes** — leave-one-out en "
            "1M filas = 1M entrenamientos. Con datasets grandes, K=3 "
            "sobra.\n\n"
            "## Resumen\n\n"
            "- `cross_val_score(modelo, X, y, cv=5)` devuelve un array "
            "de K accuracies. Reporta `mean` y `std`.\n"
            "- Para clasificadores, `cv=5` ya estratifica; para "
            "regresion o pipelines custom, pasa un `KFold`/`StratifiedKFold`.\n"
            "- `GridSearchCV(estimator, param_grid, cv=5)` prueba "
            "todas las combinaciones y expone `best_params_`, "
            "`best_score_`, `best_estimator_`.\n"
            "- El mejor `best_score_` **no es** la accuracy que veras "
            "en produccion — usa un test set aparte o nested CV para "
            "reportar honestamente.\n"
        ),
        difficulty="intermediate",
        category="ml-tuning",
        order=27,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "ML 5 · Arboles y Random Forest",
        ],
        exercises=[
            ExerciseTemplate(
                title="cross_val_score sobre LogisticRegression",
                description=(
                    "Corre 5-fold cross-validation sobre un modelo "
                    "LogReg y devuelve el array de scores."
                ),
                instructions=(
                    "Implementa `cv_score_logreg(X, y, cv=5)` que crea "
                    "`LogisticRegression(max_iter=1000, random_state=42)`, "
                    "corre `cross_val_score` con `cv=cv` y devuelve el "
                    "array de scores (`np.ndarray`) tal cual."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "\n"
                    "\n"
                    "def cv_score_logreg(X, y, cv=5):\n"
                    "    # TODO: lr = LogisticRegression(max_iter=1000, random_state=42)\n"
                    "    # TODO: return cross_val_score(lr, X, y, cv=cv)\n"
                    "    ...\n"
                ),
                hints=[
                    "cross_val_score devuelve np.ndarray de shape (cv,).",
                    "Con cv=5 sobre iris (150 filas) tienes 30 filas por fold.",
                    "No hagas .mean() aqui — devuelve el array completo.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "cv=5 sobre iris devuelve array de 5 scores con mean > 0.95",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "scores = cv_score_logreg(X, y, cv=5)\n"
                            "assert isinstance(scores, np.ndarray), type(scores)\n"
                            "assert scores.shape == (5,), scores.shape\n"
                            "assert (scores >= 0).all() and (scores <= 1).all(), scores\n"
                            "assert scores.mean() > 0.95, scores.mean()"
                        ),
                    },
                    {
                        "name": "cv=3 devuelve array de 3 scores",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "scores = cv_score_logreg(X, y, cv=3)\n"
                            "assert scores.shape == (3,), scores.shape\n"
                            "assert scores.mean() > 0.9, scores.mean()"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Elegir el mejor k para KNN via CV",
                description=(
                    "Compara varios valores de k con cross-validation "
                    "y devuelve el que da mejor media."
                ),
                instructions=(
                    "Implementa `mejor_k_knn(X, y, ks)` que, para cada "
                    "`k` en la lista `ks`, entrena "
                    "`KNeighborsClassifier(n_neighbors=k)`, calcula la "
                    "media de `cross_val_score(cv=5)` y devuelve el `k` "
                    "con la media mas alta como `int`. En caso de empate, "
                    "prefiere el `k` mas chico (el primero en aparecer "
                    "con el maximo)."
                ),
                starter_code=(
                    "from sklearn.neighbors import KNeighborsClassifier\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "\n"
                    "\n"
                    "def mejor_k_knn(X, y, ks):\n"
                    "    # TODO: para cada k en ks, calcular mean = cross_val_score(...).mean()\n"
                    "    # TODO: retornar el k con la media mas alta (empate -> primero)\n"
                    "    ...\n"
                ),
                hints=[
                    "max con key=lambda k: score_de(k) devuelve el primer maximo.",
                    "cross_val_score(...).mean() te da la accuracy promedio.",
                    "Sobre iris con ks=[1,3,5,7,9], gana k=7 con score 0.98.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "iris con ks=[1,3,5,7,9] -> k=7 gana",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "k = mejor_k_knn(X, y, [1, 3, 5, 7, 9])\n"
                            "assert isinstance(k, int), type(k)\n"
                            "assert k == 7, k"
                        ),
                    },
                    {
                        "name": "k devuelto pertenece a ks y no rompe con lista de 1 elemento",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "k = mejor_k_knn(X, y, [5])\n"
                            "assert k == 5, k\n"
                            "k2 = mejor_k_knn(X, y, [3, 11])\n"
                            "assert k2 in {3, 11}, k2"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="GridSearchCV sobre DecisionTree",
                description=(
                    "Encuentra el mejor max_depth para un DecisionTree "
                    "con GridSearchCV."
                ),
                instructions=(
                    "Implementa `grid_search_dt(X, y, depths)` que corre "
                    "`GridSearchCV` con "
                    "`DecisionTreeClassifier(random_state=42)`, "
                    "`param_grid={'max_depth': depths}` y `cv=5`. "
                    "Devuelve una tupla `(best_depth: int, best_score: float)` "
                    "con `best_params_['max_depth']` y "
                    "`best_score_`."
                ),
                starter_code=(
                    "from sklearn.tree import DecisionTreeClassifier\n"
                    "from sklearn.model_selection import GridSearchCV\n"
                    "\n"
                    "\n"
                    "def grid_search_dt(X, y, depths):\n"
                    "    # TODO: gs = GridSearchCV(DT(random_state=42), {'max_depth': depths}, cv=5)\n"
                    "    # TODO: gs.fit(X, y)\n"
                    "    # TODO: return (int(gs.best_params_['max_depth']), float(gs.best_score_))\n"
                    "    ...\n"
                ),
                hints=[
                    "gs.best_params_ es un dict; gs.best_score_ es la media CV del mejor.",
                    "Envuelve en int() y float() para evitar numpy types.",
                    "Sobre iris con depths=[1,2,3,5] gana max_depth=3 con ~0.9733.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "iris depths=[1,2,3,5] -> best_depth=3, best_score ~0.9733",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "best_depth, best_score = grid_search_dt(X, y, [1, 2, 3, 5])\n"
                            "assert isinstance(best_depth, int), type(best_depth)\n"
                            "assert isinstance(best_score, float), type(best_score)\n"
                            "assert best_depth == 3, best_depth\n"
                            "assert abs(best_score - 0.9733) < 0.01, best_score"
                        ),
                    },
                    {
                        "name": "depths=[1] fuerza best_depth=1 y best_score coincide con cross_val_score",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.tree import DecisionTreeClassifier\n"
                            "from sklearn.model_selection import cross_val_score\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "best_depth, best_score = grid_search_dt(X, y, [1])\n"
                            "assert best_depth == 1, best_depth\n"
                            "esperado = cross_val_score(\n"
                            "    DecisionTreeClassifier(max_depth=1, random_state=42), X, y, cv=5\n"
                            ").mean()\n"
                            "assert abs(best_score - esperado) < 1e-6, (best_score, esperado)"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 7 · Clustering con KMeans y metodo del codo",
        description=(
            "Primer modelo no supervisado: KMeans para agrupar sin "
            "labels. Metodo del codo y silhouette para elegir k."
        ),
        content=(
            "# ML 7: clustering con KMeans\n\n"
            "Hasta ahora todo fue **supervisado**: dabas `X` y `y`, el "
            "modelo aprendia el mapeo. En **clustering** solo tienes "
            "`X` — el modelo debe encontrar grupos naturales sin que "
            "nadie le diga cuales son las clases. Aplicaciones clasicas: "
            "segmentacion de clientes, deteccion de anomalias, "
            "compresion de datos, exploracion de datasets nuevos.\n\n"
            "## Tres ideas para entender KMeans\n\n"
            "### 1. KMeans busca K centroides que minimizan la inercia\n\n"
            "**Inercia** = suma de distancias al cuadrado de cada punto "
            "a su centroide asignado. KMeans reparte los puntos en K "
            "grupos y ajusta los centros iterativamente para que la "
            "inercia sea la menor posible.\n\n"
            "```\n"
            "algoritmo:\n"
            "  1. Elige K centros iniciales (KMeans++ los pone bien).\n"
            "  2. Repite hasta convergencia:\n"
            "     a. Asigna cada punto al centro mas cercano.\n"
            "     b. Recalcula cada centro como la media de sus puntos.\n"
            "```\n\n"
            "```python\n"
            "from sklearn.cluster import KMeans\n\n"
            "km = KMeans(n_clusters=3, random_state=42, n_init=10)\n"
            "km.fit(X)                # aprende centroides\n"
            "labels = km.labels_      # cluster de cada fila (0..K-1)\n"
            "centers = km.cluster_centers_  # shape (K, n_features)\n"
            "print(km.inertia_)       # suma de dist^2 al centro asignado\n"
            "```\n\n"
            "**Cuidados clave:**\n\n"
            "- **`random_state`** — KMeans depende de la inicializacion. "
            "Fijarlo hace el resultado reproducible.\n"
            "- **`n_init=10`** — corre KMeans 10 veces con diferentes "
            "inicializaciones y se queda con la mejor. Sin esto, un "
            "arranque malo te da clusters horribles.\n"
            "- **Escalado obligatorio** — KMeans usa distancia "
            "euclideana; una feature en dolares (0-1000000) dominara a "
            "una en anios (20-80). Aplica `StandardScaler` antes.\n\n"
            "### 2. Metodo del codo: como elegir K\n\n"
            "A diferencia del supervisado, no hay accuracy que "
            "maximizar. La inercia siempre baja al subir K (con K=N "
            "cada punto es su propio cluster e inercia=0). Necesitas un "
            "criterio externo. El **metodo del codo** grafica inercia "
            "vs K y busca el punto donde deja de bajar rapido.\n\n"
            "```python\n"
            "inertias = []\n"
            "for k in range(1, 8):\n"
            "    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)\n"
            "    inertias.append(km.inertia_)\n"
            "# grafico inertias vs k, buscar el 'codo'\n"
            "```\n\n"
            "```\n"
            "iris:\n"
            "  k=1: inertia=681.37\n"
            "  k=2: inertia=152.35  <- brutal caida\n"
            "  k=3: inertia= 78.85\n"
            "  k=4: inertia= 57.23  <- caidas cada vez mas chicas\n"
            "  k=5: inertia= 46.46\n"
            "```\n\n"
            "El codo esta entre k=2 y k=3: despues de k=3 los "
            "beneficios marginales caen. Es una decision **visual** — "
            "no hay formula matematica que devuelva 'el K correcto'. "
            "Complementalo con conocimiento del dominio.\n\n"
            "### 3. Silhouette: metrica cuantitativa para K\n\n"
            "El **silhouette score** mide, para cada punto, que tan "
            "cerca esta de su cluster vs que tan lejos del cluster mas "
            "cercano ajeno. Rango [-1, +1]:\n\n"
            "- **+1**: punto muy dentro de su cluster.\n"
            "- **0**: en la frontera entre dos clusters.\n"
            "- **-1**: probablemente asignado al cluster equivocado.\n\n"
            "```python\n"
            "from sklearn.metrics import silhouette_score\n\n"
            "score = silhouette_score(X, km.labels_)\n"
            "```\n\n"
            "El K con mejor silhouette suele ser un buen punto de "
            "partida objetivo:\n\n"
            "```\n"
            "iris escalado:\n"
            "  k=2: silhouette=0.582  <- gana!\n"
            "  k=3: silhouette=0.460\n"
            "  k=4: silhouette=0.387\n"
            "```\n\n"
            "**Sorpresa pedagogica:** iris tiene 3 especies "
            "conocidas, pero silhouette dice k=2 es mejor. La razon: "
            "setosa es muy distinta, pero versicolor y virginica se "
            "**solapan** en el espacio de features. Clustering "
            "encuentra la estructura geometrica, no las etiquetas — "
            "si no coinciden, el problema puede ser que las features "
            "no discriminan las clases reales.\n\n"
            "## Cuando NO usar KMeans\n\n"
            "KMeans asume que los clusters son **esferas de tamano "
            "similar** en el espacio de features. Falla feo cuando:\n\n"
            "- Los clusters tienen **densidades muy distintas** — usa "
            "`DBSCAN`.\n"
            "- Los clusters tienen **formas raras** (medialunas, "
            "espirales) — usa clustering jerarquico o DBSCAN.\n"
            "- **No sabes cuantos clusters** hay y no quieres asumir "
            "un K — DBSCAN los descubre solo (usa densidad, no "
            "cantidad fija).\n"
            "- Tienes **outliers extremos** — mueven los centroides y "
            "estropean el resultado. Limpialos antes o usa "
            "clustering robusto.\n\n"
            "## Errores comunes\n\n"
            "1. **No escalar** — feature con rango 0-1M domina a otras "
            "con rango 0-1. Siempre `StandardScaler` antes de KMeans.\n"
            "2. **`n_init=1`** — un arranque malo da clusters malos. "
            "El default nuevo de sklearn ya es `n_init='auto'`, pero "
            "en versiones viejas es 1. Ponlo explicito en 10.\n"
            "3. **Elegir K por inercia sola** — inercia siempre baja "
            "con K. Usa codo + silhouette + dominio.\n"
            "4. **Interpretar labels como etiquetas reales** — el "
            "cluster 0 no es 'setosa'; es solo un ID interno. Si "
            "quieres etiquetar los clusters, hazlo despues mirando "
            "sus centroides o promedios.\n"
            "5. **KMeans en categoricas one-hot** — la distancia "
            "euclideana en one-hot no tiene sentido pleno; usa "
            "KModes o algoritmos especificos para categoricas.\n\n"
            "## Resumen\n\n"
            "- `KMeans(n_clusters=K, random_state=42, n_init=10)` "
            "agrupa `X` en K clusters minimizando la inercia.\n"
            "- **Escala** siempre las features antes con "
            "`StandardScaler`.\n"
            "- Para elegir K: **codo** (visual, inercia vs K) + "
            "**silhouette** (cuantitativo, [-1, +1]) + dominio.\n"
            "- KMeans es tu default no-supervisado; para densidades "
            "raras o clusters no esfericos, mira DBSCAN o clustering "
            "jerarquico.\n"
        ),
        difficulty="intermediate",
        category="ml-clustering",
        order=28,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "ML 6 · Cross-validation y GridSearchCV",
        ],
        exercises=[
            ExerciseTemplate(
                title="Entrenar KMeans y devolver inertia",
                description=(
                    "Entrena un modelo KMeans y devuelve la inertia "
                    "final y las labels."
                ),
                instructions=(
                    "Implementa `entrenar_kmeans(X, k)` que crea "
                    "`KMeans(n_clusters=k, random_state=42, n_init=10)`, "
                    "lo entrena con `fit(X)` y devuelve una tupla "
                    "`(inertia: float, labels: np.ndarray)` con "
                    "`km.inertia_` (envuelto en `float`) y `km.labels_`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "from sklearn.cluster import KMeans\n"
                    "\n"
                    "\n"
                    "def entrenar_kmeans(X, k):\n"
                    "    # TODO: km = KMeans(n_clusters=k, random_state=42, n_init=10)\n"
                    "    # TODO: km.fit(X)\n"
                    "    # TODO: return (float(km.inertia_), km.labels_)\n"
                    "    ...\n"
                ),
                hints=[
                    "n_init=10 evita quedarte con una inicializacion mala.",
                    "km.labels_ tiene shape (n_samples,) con valores en 0..k-1.",
                    "float(km.inertia_) evita numpy.float64 en la salida.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "iris k=3 -> inertia ~78.85, labels con 3 valores unicos",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "inertia, labels = entrenar_kmeans(X, 3)\n"
                            "assert isinstance(inertia, float), type(inertia)\n"
                            "assert isinstance(labels, np.ndarray), type(labels)\n"
                            "assert labels.shape == (150,), labels.shape\n"
                            "assert set(labels.tolist()) == {0, 1, 2}, set(labels.tolist())\n"
                            "assert abs(inertia - 78.85) < 0.5, inertia"
                        ),
                    },
                    {
                        "name": "k=1 da inertia = suma total de dist^2 al centro global",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "inertia, labels = entrenar_kmeans(X, 1)\n"
                            "# con k=1 todas las labels son 0 y la inertia es la varianza total\n"
                            "assert set(labels.tolist()) == {0}, set(labels.tolist())\n"
                            "centro = X.mean(axis=0)\n"
                            "esperado = float(((X - centro) ** 2).sum())\n"
                            "assert abs(inertia - esperado) < 1e-3, (inertia, esperado)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Metodo del codo: inertias para varios K",
                description=(
                    "Corre KMeans para distintos valores de K y "
                    "devuelve la lista de inertias."
                ),
                instructions=(
                    "Implementa `metodo_del_codo(X, ks)` que, para cada "
                    "`k` en `ks`, entrena "
                    "`KMeans(n_clusters=k, random_state=42, n_init=10)` "
                    "y devuelve una `list[float]` con las inercias en el "
                    "mismo orden que `ks`."
                ),
                starter_code=(
                    "from sklearn.cluster import KMeans\n"
                    "\n"
                    "\n"
                    "def metodo_del_codo(X, ks):\n"
                    "    # TODO: para cada k en ks, entrenar KMeans y appendear km.inertia_\n"
                    "    # TODO: retornar la lista de inercias\n"
                    "    ...\n"
                ),
                hints=[
                    "La inertia baja monotonicamente al subir k.",
                    "float(km.inertia_) para evitar numpy.float64 en la lista.",
                    "El 'codo' se busca visualmente en un plot inertia vs k.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "iris ks=[1,2,3,4,5] -> inertias decrecientes",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "inertias = metodo_del_codo(X, [1, 2, 3, 4, 5])\n"
                            "assert isinstance(inertias, list), type(inertias)\n"
                            "assert len(inertias) == 5, len(inertias)\n"
                            "# monotonicamente decreciente\n"
                            "for i in range(len(inertias) - 1):\n"
                            "    assert inertias[i] >= inertias[i + 1], inertias\n"
                            "# k=1 muy alta, k=3 baja\n"
                            "assert inertias[0] > 600, inertias[0]\n"
                            "assert 70 < inertias[2] < 90, inertias[2]"
                        ),
                    },
                    {
                        "name": "respeta el orden de ks (aunque este desordenado)",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "inertias = metodo_del_codo(X, [3, 1, 2])\n"
                            "assert len(inertias) == 3, len(inertias)\n"
                            "# ks=[3,1,2] -> inertias en ese orden\n"
                            "assert inertias[1] > inertias[2] > inertias[0], inertias"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Mejor K por silhouette score",
                description=("Elige el mejor K comparando silhouette scores."),
                instructions=(
                    "Implementa `mejor_k_silhouette(X, ks)` que, para "
                    "cada `k` en `ks` (asumir `k >= 2`), entrena "
                    "`KMeans(n_clusters=k, random_state=42, n_init=10)`, "
                    "calcula `silhouette_score(X, labels)` y devuelve "
                    "el `k` con el score mas alto como `int`. En empate, "
                    "prefiere el `k` mas chico."
                ),
                starter_code=(
                    "from sklearn.cluster import KMeans\n"
                    "from sklearn.metrics import silhouette_score\n"
                    "\n"
                    "\n"
                    "def mejor_k_silhouette(X, ks):\n"
                    "    # TODO: para cada k en ks, fit_predict con KMeans y calcular silhouette\n"
                    "    # TODO: retornar k con mayor silhouette (empate -> primero)\n"
                    "    ...\n"
                ),
                hints=[
                    "silhouette_score requiere >=2 clusters distintos.",
                    "KMeans.fit_predict(X) devuelve labels en un paso.",
                    "En blobs sinteticos con 4 centros bien separados, gana k=4.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "make_blobs 4 centros -> mejor k=4",
                        "code": (
                            "from sklearn.datasets import make_blobs\n"
                            "X, _ = make_blobs(\n"
                            "    n_samples=200, centers=4, cluster_std=0.5, random_state=42\n"
                            ")\n"
                            "k = mejor_k_silhouette(X, [2, 3, 4, 5])\n"
                            "assert isinstance(k, int), type(k)\n"
                            "assert k == 4, k"
                        ),
                    },
                    {
                        "name": "iris escalado -> silhouette prefiere k=2 (versicolor+virginica se solapan)",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "k = mejor_k_silhouette(Xs, [2, 3, 4])\n"
                            "assert k == 2, k"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 8 · PCA para reducir dimensionalidad",
        description=(
            "Principal Component Analysis: comprimir features "
            "preservando varianza. Visualizacion 2D y aceleracion de "
            "modelos."
        ),
        content=(
            "# ML 8: reduccion de dimensionalidad con PCA\n\n"
            "Cuando tienes 64 features (o 10.000), pasan tres cosas "
            "molestas: es dificil visualizar los datos, los modelos "
            "tardan mas en entrenar, y muchas features estan "
            "**correlacionadas** entre si (informacion redundante). "
            "**PCA (Principal Component Analysis)** ataca las tres: "
            "encuentra un espacio nuevo de menor dimension que "
            "**preserva la mayor varianza posible** de los datos "
            "originales.\n\n"
            "## Tres ideas para entender PCA\n\n"
            "### 1. PCA encuentra los ejes con mayor varianza\n\n"
            "Imagina una nube de puntos alargada en el plano (X, Y). "
            "PCA rota los ejes para que **el primer eje nuevo (PC1) "
            "vaya a lo largo de la nube** (direccion de maxima "
            "varianza), y el segundo (PC2) sea perpendicular a PC1 y "
            "capture la varianza restante. Cada componente principal es "
            "una **combinacion lineal** de las features originales.\n\n"
            "```\n"
            "features originales -> ejes rotados por PCA\n"
            "  X (sepal_length)         PC1 (0.52*sl + 0.27*sw + 0.58*pl + 0.56*pw)\n"
            "  Y (sepal_width)     ->   PC2 (-0.38*sl + 0.92*sw - 0.02*pl - 0.07*pw)\n"
            "  Z (petal_length)         PC3 (...)\n"
            "  W (petal_width)          PC4 (...)\n"
            "```\n\n"
            "Las componentes estan **ordenadas por varianza explicada** "
            "de mayor a menor. Si te quedas con las primeras K, "
            "conservas la mayor parte de la informacion en menos "
            "dimensiones.\n\n"
            "```python\n"
            "from sklearn.decomposition import PCA\n\n"
            "pca = PCA(n_components=2, random_state=42)\n"
            "X2 = pca.fit_transform(X)   # shape (n_samples, 2)\n"
            "print(pca.explained_variance_ratio_)\n"
            "# [0.7296, 0.2285]  -> las 2 primeras PC explican 95.8% de la varianza\n"
            "```\n\n"
            "### 2. Cuantas componentes usar\n\n"
            "Dos estrategias tipicas:\n\n"
            "**A. Fijar un umbral de varianza explicada** (ej. 95%):\n"
            "```python\n"
            "pca = PCA(n_components=0.95, random_state=42).fit(X)\n"
            "print(pca.n_components_)  # cuantas necesito para llegar a 95%\n"
            "```\n\n"
            "**B. Scree plot**: grafica varianza explicada acumulada vs "
            "K y buscas el codo (igual que en KMeans):\n\n"
            "```\n"
            "iris:\n"
            "  1 PC:  72.96%\n"
            "  2 PC:  95.81%  <- ya cerca del 100%\n"
            "  3 PC:  99.48%\n"
            "  4 PC: 100.00%\n"
            "```\n\n"
            "Con 4 features originales, la ganancia de dimensionalidad "
            "es minima. PCA brilla cuando tienes **muchas** features:\n\n"
            "```\n"
            "digits (64 features):\n"
            "  para conservar 90% de varianza -> 31 componentes\n"
            "  reduces ~50% las columnas sin perder informacion util\n"
            "```\n\n"
            "### 3. Escalado obligatorio (otra vez)\n\n"
            "PCA usa **varianza**, y la varianza depende de la escala. "
            "Una feature en dolares (0-1M) tendra varianza millones de "
            "veces mayor que una en 0-1: dominara PC1 aunque sea "
            "irrelevante. Aplica siempre `StandardScaler` antes de PCA "
            "(salvo que todas tus features ya esten en la misma "
            "escala fisica).\n\n"
            "```python\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n\n"
            "pipe = Pipeline([\n"
            "    ('sc', StandardScaler()),\n"
            "    ('pca', PCA(n_components=2, random_state=42)),\n"
            "    ('lr', LogisticRegression(max_iter=1000)),\n"
            "])\n"
            "```\n\n"
            "## Cuando usar PCA\n\n"
            "**Casos donde PCA es la herramienta correcta:**\n\n"
            "- **Visualizacion**: reducir a 2 o 3 componentes para "
            "plotear datos de alta dimension.\n"
            "- **Compresion**: cientos/miles de features ->\n"
            "  decenas conservando 95% de la varianza.\n"
            "- **Denoising**: al descartar componentes de baja varianza "
            "eliminas ruido idiosincratico.\n"
            "- **Multicolinealidad**: features muy correlacionadas "
            "confunden a la regresion lineal; PCA las combina en "
            "componentes ortogonales.\n\n"
            "**Casos donde PCA es mala idea:**\n\n"
            "- **Necesitas interpretabilidad por feature** — los PCs "
            "son combinaciones lineales, no features originales. "
            'Explicar "el modelo depende de 0.5*X1 - 0.3*X2 + '
            '0.8*X3" no vende.\n'
            "- **Features categoricas o binarias** — PCA es lineal y "
            "asume continuidad; en categoricas usa MCA o embeddings.\n"
            "- **Relaciones no lineales** en los datos — PCA solo "
            "captura estructura lineal. Para manifolds curvos usa "
            "t-SNE o UMAP (solo para visualizacion) o autoencoders.\n"
            "- **Dataset gigante** — PCA calcula la matriz de "
            "covarianza (O(n * d^2)); con d>10.000 se pone lento. Usa "
            "`TruncatedSVD` o `IncrementalPCA`.\n\n"
            "## Precio a pagar: casi siempre pierdes algo de accuracy\n\n"
            "Reducir dimensionalidad tiene un costo. Sobre iris "
            "escalado con LogReg:\n\n"
            "```\n"
            "  features originales (4):  CV accuracy = 0.96\n"
            "  PCA a 2 componentes:      CV accuracy = 0.91\n"
            "```\n\n"
            "Perder 0.05 puede o no valer la pena — depende del "
            "problema. Si eres mucho mas rapido, visualizas datos, "
            "y el modelo sigue siendo aceptable, PCA gana. Si cada "
            "punto de accuracy vale plata, PCA no es tu amigo.\n\n"
            "## Errores comunes\n\n"
            "1. **No escalar antes** — features con rangos muy "
            "distintos dominan PCs. `StandardScaler` primero.\n"
            "2. **Aplicar PCA a train + test juntos** — data leakage. "
            "`fit` solo en train; `transform` en test.\n"
            "3. **Usar todos los PCs pensando que 'ayuda'** — PCA con "
            "n_components = n_features solo rota; no reduce ni "
            "acelera nada.\n"
            "4. **Interpretar PC1 como una feature real** — es una "
            "combinacion; puedes mirar `pca.components_` para ver los "
            "coeficientes, pero rara vez tiene un nombre claro.\n"
            "5. **Aplicar PCA a arboles/RF** — no ayuda: los arboles "
            "no sufren de multicolinealidad ni les molesta la escala. "
            "PCA solo agrega complejidad y tira interpretabilidad.\n\n"
            "## Resumen\n\n"
            "- `PCA(n_components=K)` proyecta X a un espacio de K "
            "dimensiones que **preserva la mayor varianza posible**.\n"
            "- Elige K por umbral (`n_components=0.95`) o scree plot.\n"
            "- `pca.explained_variance_ratio_` te dice que fraccion de "
            "varianza captura cada componente.\n"
            "- **Escala siempre** antes con `StandardScaler`, y "
            "envuelve todo en un `Pipeline` para evitar leakage.\n"
            "- Usa PCA para visualizar, comprimir, denoisar; NO para "
            "categoricas, arboles, o cuando necesites interpretabilidad "
            "por feature.\n"
        ),
        difficulty="intermediate",
        category="ml-dim-reduction",
        order=29,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "ML 7 · Clustering con KMeans y metodo del codo",
        ],
        exercises=[
            ExerciseTemplate(
                title="PCA a n componentes",
                description=(
                    "Aplica PCA para reducir features y devuelve la "
                    "transformacion + varianza explicada."
                ),
                instructions=(
                    "Implementa `pca_reducir(X_scaled, n)` que crea "
                    "`PCA(n_components=n, random_state=42)`, lo entrena "
                    "con `fit_transform(X_scaled)` y devuelve una tupla "
                    "`(X_reducido: np.ndarray, ratios: np.ndarray)` con "
                    "el X transformado (shape `(n_samples, n)`) y el "
                    "atributo `explained_variance_ratio_`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "from sklearn.decomposition import PCA\n"
                    "\n"
                    "\n"
                    "def pca_reducir(X_scaled, n):\n"
                    "    # TODO: pca = PCA(n_components=n, random_state=42)\n"
                    "    # TODO: X_red = pca.fit_transform(X_scaled)\n"
                    "    # TODO: return (X_red, pca.explained_variance_ratio_)\n"
                    "    ...\n"
                ),
                hints=[
                    "fit_transform hace fit + transform en un paso.",
                    "explained_variance_ratio_ suma <=1 (=1 solo si n = n_features).",
                    "Escala X antes con StandardScaler para que PCA sea significativo.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "iris escalado n=2 -> shape (150,2) y ~95.8% varianza",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "X2, ratios = pca_reducir(Xs, 2)\n"
                            "assert isinstance(X2, np.ndarray), type(X2)\n"
                            "assert X2.shape == (150, 2), X2.shape\n"
                            "assert ratios.shape == (2,), ratios.shape\n"
                            "# PC1 ~0.73, PC2 ~0.23\n"
                            "assert abs(ratios[0] - 0.7296) < 0.01, ratios\n"
                            "assert abs(ratios.sum() - 0.9581) < 0.01, ratios.sum()"
                        ),
                    },
                    {
                        "name": "n=4 = n_features -> ratios suman 1.0",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "X4, ratios = pca_reducir(Xs, 4)\n"
                            "assert X4.shape == (150, 4), X4.shape\n"
                            "assert abs(ratios.sum() - 1.0) < 1e-6, ratios.sum()"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Componentes necesarias para X% de varianza",
                description=(
                    "Cuenta cuantas componentes necesitas para llegar "
                    "a un umbral de varianza explicada."
                ),
                instructions=(
                    "Implementa `n_componentes_para(X_scaled, "
                    "var_explicada)` que entrena "
                    "`PCA(n_components=var_explicada, random_state=42)` "
                    "sobre `X_scaled` y devuelve `pca.n_components_` "
                    "como `int` (numero minimo de componentes que "
                    "alcanzan al menos ese umbral). `var_explicada` "
                    "debe estar entre 0 y 1 (fraccion, no porcentaje)."
                ),
                starter_code=(
                    "from sklearn.decomposition import PCA\n"
                    "\n"
                    "\n"
                    "def n_componentes_para(X_scaled, var_explicada):\n"
                    "    # TODO: pca = PCA(n_components=var_explicada, random_state=42)\n"
                    "    # TODO: pca.fit(X_scaled)\n"
                    "    # TODO: return int(pca.n_components_)\n"
                    "    ...\n"
                ),
                hints=[
                    "PCA acepta n_components como float en (0,1) = umbral de varianza.",
                    "pca.n_components_ es el numero final elegido (int).",
                    "digits (64 features) escalado con umbral 0.9 -> 31 componentes.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "iris escalado 0.95 -> 2 componentes",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "n = n_componentes_para(Xs, 0.95)\n"
                            "assert isinstance(n, int), type(n)\n"
                            "assert n == 2, n"
                        ),
                    },
                    {
                        "name": "digits escalado 0.9 -> 31 componentes",
                        "code": (
                            "from sklearn.datasets import load_digits\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "X, _ = load_digits(return_X_y=True)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "n = n_componentes_para(Xs, 0.9)\n"
                            "assert n == 31, n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Pipeline PCA + LogReg: costo en accuracy",
                description=(
                    "Compara accuracy de LogReg con features originales "
                    "vs con PCA aplicado antes."
                ),
                instructions=(
                    "Implementa `pca_conserva_accuracy(X, y, "
                    "n_components)` que arma DOS pipelines y devuelve "
                    "un dict `{'full': acc_full, 'pca': acc_pca}` con "
                    "las accuracies medias de `cross_val_score(cv=5)`:\n"
                    "- `full`: `StandardScaler` + "
                    "`LogisticRegression(max_iter=1000, random_state=42)`.\n"
                    "- `pca`: `StandardScaler` + "
                    "`PCA(n_components=n_components, random_state=42)` "
                    "+ `LogisticRegression(max_iter=1000, "
                    "random_state=42)`.\n"
                    "Ambas accuracies como `float` (no numpy)."
                ),
                starter_code=(
                    "from sklearn.decomposition import PCA\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "\n"
                    "\n"
                    "def pca_conserva_accuracy(X, y, n_components):\n"
                    "    # TODO: pipe_full = Pipeline([('sc', ...), ('lr', ...)])\n"
                    "    # TODO: pipe_pca = Pipeline([('sc', ...), ('pca', ...), ('lr', ...)])\n"
                    "    # TODO: acc_full = cross_val_score(pipe_full, X, y, cv=5).mean()\n"
                    "    # TODO: acc_pca = cross_val_score(pipe_pca, X, y, cv=5).mean()\n"
                    "    # TODO: return {'full': float(acc_full), 'pca': float(acc_pca)}\n"
                    "    ...\n"
                ),
                hints=[
                    "Pipeline garantiza que el scaler se ajusta solo en train por fold.",
                    "En iris con n_components=2, acc_full ~0.96 y acc_pca ~0.91.",
                    "float(acc) en la salida para que el dict no tenga numpy.float64.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "iris n=2 -> ambos > 0.9, full >= pca, dict shape correcta",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "res = pca_conserva_accuracy(X, y, 2)\n"
                            "assert isinstance(res, dict), type(res)\n"
                            "assert set(res.keys()) == {'full', 'pca'}, res.keys()\n"
                            "assert isinstance(res['full'], float), type(res['full'])\n"
                            "assert isinstance(res['pca'], float), type(res['pca'])\n"
                            "assert res['full'] > 0.9, res\n"
                            "assert res['pca'] > 0.9, res\n"
                            "assert res['full'] >= res['pca'], res"
                        ),
                    },
                    {
                        "name": "iris n=4 -> pca deberia igualar full (mismas dimensiones = sin perdida)",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "res = pca_conserva_accuracy(X, y, 4)\n"
                            "assert abs(res['full'] - res['pca']) < 0.02, res"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 9 · Support Vector Machines (SVM)",
        description=(
            "Margen maximo, kernel trick (linear vs rbf), y por que "
            "el escalado y los support vectors importan."
        ),
        content=(
            "# ML 9: Support Vector Machines\n\n"
            "Una **SVM** busca la frontera que separa las clases dejando "
            "el **margen mas ancho posible** entre ellas. No cualquier "
            "recta que separe: la que queda mas lejos de los puntos de "
            "ambos lados. Esos puntos criticos que tocan el margen son "
            "los **support vectors**, y son los unicos que definen la "
            "frontera (si mueves un punto lejano, la frontera no cambia).\n\n"
            "## Tres ideas clave\n\n"
            "### 1. Margen maximo\n\n"
            "Entre todas las fronteras que separan las clases, la SVM "
            "elige la de mayor margen. Un margen ancho generaliza mejor: "
            "deja mas 'colchon' antes de equivocarse con datos nuevos.\n\n"
            "```python\n"
            "from sklearn.svm import SVC\n"
            "clf = SVC(kernel='linear', C=1.0, random_state=42)\n"
            "clf.fit(X_train, y_train)\n"
            "print(clf.support_vectors_.shape)  # cuantos SV definen la frontera\n"
            "```\n\n"
            "### 2. El kernel trick: separar lo no separable\n\n"
            "Muchos datos **no** se separan con una recta. El kernel "
            "**rbf** proyecta los datos a un espacio de mas dimensiones "
            "donde si son linealmente separables, sin calcularlo "
            "explicitamente. Sobre datos con forma de lunas o circulos, "
            "`kernel='rbf'` supera claramente a `kernel='linear'`:\n\n"
            "```\n"
            "make_moons (no lineal):\n"
            "  kernel linear:  CV accuracy ~0.85\n"
            "  kernel rbf:     CV accuracy ~0.96\n"
            "```\n\n"
            "### 3. C y gamma\n\n"
            "- **C** controla el trade-off margen vs errores. C grande = "
            "menos tolerante a errores (margen estrecho, riesgo de "
            "overfit); C pequeno = margen ancho, mas tolerante.\n"
            "- **gamma** (solo rbf) controla el alcance de cada punto. "
            "Gamma grande = fronteras muy locales (overfit); `gamma="
            "'scale'` es el default sensato.\n\n"
            "## Escalado obligatorio\n\n"
            "La SVM mide **distancias**, asi que es sensible a la escala "
            "igual que KNN. **Siempre** `StandardScaler` antes (dentro de "
            "un `Pipeline`), o una feature de rango grande dominara.\n\n"
            "```python\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "pipe = Pipeline([('sc', StandardScaler()),\n"
            "                 ('svc', SVC(kernel='rbf', gamma='scale'))])\n"
            "```\n\n"
            "## Cuando usar SVM\n\n"
            "- **Datasets pequenos/medianos** con frontera compleja: rbf "
            "brilla.\n"
            "- **Muchas features, pocas muestras** (texto, genomica): SVM "
            "lineal es fuerte.\n"
            "- **Evitala** en datasets enormes (millones de filas): "
            "escala mal con n (usa modelos lineales o arboles).\n"
            "- **No da probabilidades** de forma natural (necesita "
            "`probability=True`, que la hace mas lenta).\n\n"
            "## Resumen\n\n"
            "- SVM maximiza el margen; solo los **support vectors** "
            "cuentan.\n"
            "- `kernel='rbf'` separa datos no lineales; `linear` para "
            "alta dimension.\n"
            "- **Escala siempre** antes con `StandardScaler`.\n"
            "- Ajusta `C` (y `gamma` en rbf); usa `gamma='scale'` de "
            "base.\n"
        ),
        difficulty="intermediate",
        category="ml-svm",
        order=30,
        track="track-3",
        estimated_duration=50,
        prerequisites_titles=[
            "ML 8 · PCA para reducir dimensionalidad",
        ],
        exercises=[
            ExerciseTemplate(
                title="Entrenar una SVM con kernel configurable",
                description=(
                    "Entrena una SVC con kernel y C dados y devuelve la "
                    "accuracy en test."
                ),
                instructions=(
                    "Implementa `entrenar_svm(X_train, y_train, X_test, "
                    "y_test, kernel='rbf', C=1.0)` que crea "
                    "`SVC(kernel=kernel, C=C, gamma='scale', "
                    "random_state=42)`, la entrena con train y devuelve "
                    "la accuracy sobre test como `float`. Asume que X ya "
                    "viene escalado."
                ),
                starter_code=(
                    "from sklearn.svm import SVC\n"
                    "\n"
                    "\n"
                    "def entrenar_svm(X_train, y_train, X_test, y_test, kernel='rbf', C=1.0):\n"
                    "    # TODO: clf = SVC(kernel=kernel, C=C, gamma='scale', random_state=42)\n"
                    "    # TODO: clf.fit(X_train, y_train)\n"
                    "    # TODO: return float(clf.score(X_test, y_test))\n"
                    "    ...\n"
                ),
                hints=[
                    "clf.score(X, y) ya devuelve la accuracy.",
                    "gamma='scale' es el default sensato para rbf.",
                    "En datos no lineales, rbf supera a linear.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "moons escalado: rbf >0.9 y rbf >= linear",
                        "code": (
                            "from sklearn.datasets import make_moons\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = make_moons(n_samples=200, noise=0.2, random_state=42)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(Xs, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "rbf = entrenar_svm(Xtr, ytr, Xte, yte, kernel='rbf')\n"
                            "lin = entrenar_svm(Xtr, ytr, Xte, yte, kernel='linear')\n"
                            "assert isinstance(rbf, float), type(rbf)\n"
                            "assert rbf > 0.9, rbf\n"
                            "assert lin > 0.8, lin\n"
                            "assert rbf >= lin, (rbf, lin)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Comparar kernels linear vs rbf",
                description=(
                    "Compara la accuracy CV de un kernel lineal contra "
                    "uno rbf sobre datos no lineales."
                ),
                instructions=(
                    "Implementa `comparar_kernels(X, y)` que, para cada "
                    "kernel en `['linear', 'rbf']`, arma un "
                    "`Pipeline([StandardScaler, SVC(kernel=..., "
                    "gamma='scale', random_state=42)])`, calcula "
                    "`cross_val_score(pipe, X, y, cv=5).mean()` y devuelve "
                    "un dict `{'linear': media, 'rbf': media}` con floats."
                ),
                starter_code=(
                    "from sklearn.svm import SVC\n"
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "\n"
                    "\n"
                    "def comparar_kernels(X, y):\n"
                    "    # TODO: para cada kernel arma pipeline con StandardScaler + SVC\n"
                    "    # TODO: media = cross_val_score(pipe, X, y, cv=5).mean()\n"
                    "    # TODO: return {'linear': ..., 'rbf': ...}\n"
                    "    ...\n"
                ),
                hints=[
                    "Un dict comprehension sobre los dos kernels es suficiente.",
                    "cross_val_score devuelve un array; usa .mean().",
                    "En make_moons el rbf gana con holgura.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "moons: rbf supera a linear, ambos floats",
                        "code": (
                            "from sklearn.datasets import make_moons\n"
                            "X, y = make_moons(n_samples=200, noise=0.2, random_state=42)\n"
                            "res = comparar_kernels(X, y)\n"
                            "assert set(res.keys()) == {'linear', 'rbf'}, res.keys()\n"
                            "assert isinstance(res['rbf'], float), type(res['rbf'])\n"
                            "assert res['rbf'] > res['linear'], res\n"
                            "assert res['rbf'] > 0.9, res['rbf']"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Contar support vectors",
                description=(
                    "Cuenta cuantos puntos de entrenamiento terminan "
                    "siendo support vectors."
                ),
                instructions=(
                    "Implementa `n_support_vectors(X_train, y_train, "
                    "kernel='linear')` que entrena "
                    "`SVC(kernel=kernel, gamma='scale', random_state=42)` "
                    "y devuelve el numero total de support vectors "
                    "(`clf.support_vectors_.shape[0]`) como `int`."
                ),
                starter_code=(
                    "from sklearn.svm import SVC\n"
                    "\n"
                    "\n"
                    "def n_support_vectors(X_train, y_train, kernel='linear'):\n"
                    "    # TODO: clf = SVC(kernel=kernel, gamma='scale', random_state=42)\n"
                    "    # TODO: clf.fit(X_train, y_train)\n"
                    "    # TODO: return int(clf.support_vectors_.shape[0])\n"
                    "    ...\n"
                ),
                hints=[
                    "support_vectors_ es un array (n_sv, n_features).",
                    "Los SV son un subconjunto del train, nunca mas que len(y_train).",
                    "La frontera depende SOLO de esos puntos.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "moons: 0 < n_sv < n_train",
                        "code": (
                            "from sklearn.datasets import make_moons\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = make_moons(n_samples=200, noise=0.2, random_state=42)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(Xs, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "n = n_support_vectors(Xtr, ytr, kernel='linear')\n"
                            "assert isinstance(n, int), type(n)\n"
                            "assert 0 < n < len(ytr), (n, len(ytr))"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 10 · Naive Bayes",
        description=(
            "Clasificador probabilistico basado en el teorema de Bayes "
            "y la suposicion 'naive' de independencia. Rapido y buen "
            "baseline."
        ),
        content=(
            "# ML 10: Naive Bayes\n\n"
            "**Naive Bayes** es un clasificador probabilistico que aplica "
            "el **teorema de Bayes** asumiendo que las features son "
            "**independientes entre si** dada la clase. Esa suposicion "
            "casi nunca es literalmente cierta (por eso 'naive', "
            "ingenua), pero funciona sorprendentemente bien y es "
            "**rapidisimo** de entrenar.\n\n"
            "## La idea\n\n"
            "Para cada clase, calcula la probabilidad de que la muestra "
            "pertenezca a ella y elige la mayor:\n\n"
            "```\n"
            "P(clase | features) proporcional a P(clase) * prod P(feature_i | clase)\n"
            "```\n\n"
            "El termino `prod P(feature_i | clase)` es donde entra la "
            "suposicion naive: multiplica las probabilidades de cada "
            "feature como si fueran independientes.\n\n"
            "## Variantes\n\n"
            "- **GaussianNB**: features continuas; asume que cada feature "
            "sigue una normal por clase. Es la que usaras con datos como "
            "iris.\n"
            "- **MultinomialNB**: conteos (bolsa de palabras en texto).\n"
            "- **BernoulliNB**: features binarias (presencia/ausencia).\n\n"
            "```python\n"
            "from sklearn.naive_bayes import GaussianNB\n"
            "clf = GaussianNB()\n"
            "clf.fit(X_train, y_train)\n"
            "print(clf.predict_proba(X_test)[:3])  # probabilidades por clase\n"
            "```\n\n"
            "## Da probabilidades calibradas-ish\n\n"
            "A diferencia de la SVM, Naive Bayes entrega `predict_proba` "
            "de forma natural: cada fila suma 1 (una distribucion sobre "
            "las clases). Util cuando necesitas confianza, no solo la "
            "etiqueta.\n\n"
            "## Baseline fuerte y barato\n\n"
            "Sobre iris, GaussianNB (~0.95 CV) queda a un pelo de "
            "LogisticRegression (~0.97), sin tuning y entrenando en "
            "milisegundos:\n\n"
            "```\n"
            "iris (CV 5-fold):\n"
            "  GaussianNB:          ~0.953\n"
            "  LogisticRegression:  ~0.973\n"
            "```\n\n"
            "Por eso Naive Bayes es un **baseline** que deberias probar "
            "antes de sacar la artilleria: si tu modelo complejo no lo "
            "supera, algo esta mal.\n\n"
            "## Cuando usar Naive Bayes\n\n"
            "- **Clasificacion de texto / spam** — MultinomialNB es un "
            "clasico que sigue vigente.\n"
            "- **Baseline rapido** en cualquier problema de "
            "clasificacion.\n"
            "- **Muchisimas features** — como asume independencia, no "
            "sufre tanto la maldicion de la dimensionalidad.\n"
            "- **Evitalo** cuando las features estan muy correlacionadas "
            "(la suposicion naive se rompe) y necesitas exprimir "
            "accuracy.\n\n"
            "## Resumen\n\n"
            "- Aplica Bayes asumiendo independencia entre features.\n"
            "- `GaussianNB` para continuas, `MultinomialNB` para conteos.\n"
            "- Entrega `predict_proba` (filas suman 1).\n"
            "- Rapido, sin hiperparametros, gran baseline.\n"
        ),
        difficulty="intermediate",
        category="ml-naive-bayes",
        order=31,
        track="track-3",
        estimated_duration=45,
        prerequisites_titles=[
            "ML 9 · Support Vector Machines (SVM)",
        ],
        exercises=[
            ExerciseTemplate(
                title="Entrenar GaussianNB",
                description=(
                    "Entrena un GaussianNB y devuelve la accuracy en " "test."
                ),
                instructions=(
                    "Implementa `entrenar_gnb(X_train, y_train, X_test, "
                    "y_test)` que crea `GaussianNB()`, la entrena con "
                    "train y devuelve la accuracy sobre test como "
                    "`float`."
                ),
                starter_code=(
                    "from sklearn.naive_bayes import GaussianNB\n"
                    "\n"
                    "\n"
                    "def entrenar_gnb(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: clf = GaussianNB(); clf.fit(X_train, y_train)\n"
                    "    # TODO: return float(clf.score(X_test, y_test))\n"
                    "    ...\n"
                ),
                hints=[
                    "GaussianNB no lleva hiperparametros.",
                    "clf.score(X, y) devuelve la accuracy.",
                    "GaussianNB ni siquiera necesita escalado.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "iris split 0.3 -> accuracy > 0.85",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = entrenar_gnb(Xtr, ytr, Xte, yte)\n"
                            "assert isinstance(acc, float), type(acc)\n"
                            "assert acc > 0.85, acc"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Probabilidades por clase",
                description=(
                    "Devuelve la matriz de probabilidades predichas y "
                    "verifica que cada fila es una distribucion."
                ),
                instructions=(
                    "Implementa `proba_gnb(X_train, y_train, X_test)` que "
                    "entrena `GaussianNB` con train y devuelve "
                    "`clf.predict_proba(X_test)` (un `np.ndarray` de shape "
                    "`(n_test, n_clases)` donde cada fila suma 1)."
                ),
                starter_code=(
                    "from sklearn.naive_bayes import GaussianNB\n"
                    "\n"
                    "\n"
                    "def proba_gnb(X_train, y_train, X_test):\n"
                    "    # TODO: clf = GaussianNB(); clf.fit(X_train, y_train)\n"
                    "    # TODO: return clf.predict_proba(X_test)\n"
                    "    ...\n"
                ),
                hints=[
                    "predict_proba devuelve una fila por muestra.",
                    "Cada fila es una distribucion: suma 1.",
                    "iris tiene 3 clases -> 3 columnas.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "iris: shape (n,3), filas suman 1, valores en [0,1]",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "P = np.asarray(proba_gnb(Xtr, ytr, Xte))\n"
                            "assert P.shape == (45, 3), P.shape\n"
                            "assert np.allclose(P.sum(axis=1), 1.0), P.sum(axis=1)[:5]\n"
                            "assert (P >= 0).all() and (P <= 1).all()"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Naive Bayes vs Logistic Regression",
                description=(
                    "Compara CV de GaussianNB contra LogisticRegression "
                    "como baseline."
                ),
                instructions=(
                    "Implementa `nb_vs_logreg(X, y)` que calcula "
                    "`cross_val_score(clf, X, y, cv=5).mean()` para "
                    "`GaussianNB()` y para "
                    "`LogisticRegression(max_iter=1000)`, y devuelve un "
                    "dict `{'nb': media_nb, 'logreg': media_logreg}` con "
                    "floats."
                ),
                starter_code=(
                    "from sklearn.naive_bayes import GaussianNB\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "\n"
                    "\n"
                    "def nb_vs_logreg(X, y):\n"
                    "    # TODO: nb = cross_val_score(GaussianNB(), X, y, cv=5).mean()\n"
                    "    # TODO: lr = cross_val_score(LogisticRegression(max_iter=1000), X, y, cv=5).mean()\n"
                    "    # TODO: return {'nb': float(nb), 'logreg': float(lr)}\n"
                    "    ...\n"
                ),
                hints=[
                    "Naive Bayes suele quedar competitivo, no muy por debajo.",
                    "Ambos deberian superar 0.9 en iris.",
                    "NB entrena mucho mas rapido que LogReg.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "iris: ambos > 0.9, keys correctas",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "res = nb_vs_logreg(X, y)\n"
                            "assert set(res.keys()) == {'nb', 'logreg'}, res.keys()\n"
                            "assert isinstance(res['nb'], float), type(res['nb'])\n"
                            "assert res['nb'] > 0.9, res\n"
                            "assert res['logreg'] > 0.9, res"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 11 · Curva ROC, AUC y umbral de decision",
        description=(
            "Evaluar clasificadores binarios de forma agnostica al "
            "umbral: TPR vs FPR, AUC y como mover el umbral cambia "
            "precision/recall."
        ),
        content=(
            "# ML 11: Curva ROC, AUC y umbral\n\n"
            "Un clasificador binario no solo dice 0 o 1: internamente "
            "calcula una **probabilidad** (o score) y la compara contra "
            "un **umbral** (por defecto 0.5). Cambiar ese umbral cambia "
            "el balance entre atrapar positivos y evitar falsas alarmas. "
            "La **curva ROC** y el **AUC** miden que tan bueno es el "
            "modelo **independientemente del umbral que elijas**.\n\n"
            "## La curva ROC\n\n"
            "Barre todos los umbrales posibles y grafica:\n\n"
            "- **TPR** (recall, eje Y): de los positivos reales, cuantos "
            "atrapo.\n"
            "- **FPR** (eje X): de los negativos reales, cuantos marco "
            "por error.\n\n"
            "```python\n"
            "from sklearn.metrics import roc_curve\n"
            "proba = pipe.predict_proba(X_test)[:, 1]\n"
            "fpr, tpr, thresholds = roc_curve(y_test, proba)\n"
            "```\n\n"
            "Un modelo perfecto pasa por la esquina superior izquierda "
            "(TPR=1, FPR=0). La diagonal es el azar.\n\n"
            "## AUC: un numero para resumir la curva\n\n"
            "El **AUC** (area bajo la ROC) resume la curva en un valor "
            "entre 0.5 (azar) y 1.0 (perfecto). Interpretacion elegante: "
            "es la probabilidad de que el modelo asigne mayor score a un "
            "positivo aleatorio que a un negativo aleatorio.\n\n"
            "```python\n"
            "from sklearn.metrics import roc_auc_score\n"
            "auc = roc_auc_score(y_test, proba)   # ~0.995 en breast_cancer\n"
            "```\n\n"
            "**Clave**: AUC usa las **probabilidades**, no las etiquetas "
            "0/1. No depende del umbral, por eso compara modelos de forma "
            "mas justa que la accuracy.\n\n"
            "## Mover el umbral: precision vs recall\n\n"
            "El umbral 0.5 no es sagrado. **Bajarlo** marca mas cosas "
            "como positivas: sube el **recall** (atrapas mas positivos) "
            "pero baja la **precision** (mas falsas alarmas). Subirlo "
            "hace lo contrario.\n\n"
            "```\n"
            "breast_cancer (clase benigno):\n"
            "  umbral 0.5:  precision 0.99, recall 0.99\n"
            "  umbral 0.3:  precision 0.97, recall 1.00   <- no se escapa ninguno\n"
            "```\n\n"
            "En medicina o fraude, muchas veces prefieres **recall alto** "
            "(no perder un caso) aunque cueste precision. Eliges el "
            "umbral segun el costo de cada tipo de error, no por "
            "defecto.\n\n"
            "## Cuando mirar ROC/AUC\n\n"
            "- **Clasificacion binaria** donde el umbral es ajustable.\n"
            "- **Clases desbalanceadas**: AUC es mas informativo que "
            "accuracy (recuerda ML 2).\n"
            "- **Comparar modelos** sin fijar un umbral arbitrario.\n"
            "- **Ojo**: con desbalance extremo, la curva "
            "**precision-recall** (PR) puede ser mas honesta que la ROC.\n\n"
            "## Resumen\n\n"
            "- `roc_curve` da (fpr, tpr, thresholds); graficala para ver "
            "el trade-off.\n"
            "- `roc_auc_score` resume la calidad en [0.5, 1.0], usando "
            "**probabilidades**.\n"
            "- El **umbral** es una decision de negocio: bajalo para mas "
            "recall, subelo para mas precision.\n"
        ),
        difficulty="intermediate",
        category="ml-roc",
        order=32,
        track="track-3",
        estimated_duration=50,
        prerequisites_titles=[
            "ML 10 · Naive Bayes",
        ],
        exercises=[
            ExerciseTemplate(
                title="Calcular el AUC de un modelo",
                description=(
                    "Entrena un pipeline y devuelve el ROC AUC usando "
                    "probabilidades."
                ),
                instructions=(
                    "Implementa `auc_modelo(X_train, y_train, X_test, "
                    "y_test)` que arma un "
                    "`Pipeline([StandardScaler, "
                    "LogisticRegression(max_iter=5000, "
                    "random_state=42)])`, lo entrena, saca "
                    "`predict_proba(X_test)[:, 1]` y devuelve "
                    "`roc_auc_score(y_test, proba)` como `float`."
                ),
                starter_code=(
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.metrics import roc_auc_score\n"
                    "\n"
                    "\n"
                    "def auc_modelo(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: arma y entrena el pipeline\n"
                    "    # TODO: proba = pipe.predict_proba(X_test)[:, 1]\n"
                    "    # TODO: return float(roc_auc_score(y_test, proba))\n"
                    "    ...\n"
                ),
                hints=[
                    "AUC usa las probabilidades de la clase positiva (columna 1).",
                    "roc_auc_score(y_true, y_score) NO recibe etiquetas 0/1.",
                    "En breast_cancer el AUC pasa de 0.99.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "breast_cancer: AUC > 0.98",
                        "code": (
                            "from sklearn.datasets import load_breast_cancer\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = load_breast_cancer(return_X_y=True)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
                            "auc = auc_modelo(Xtr, ytr, Xte, yte)\n"
                            "assert isinstance(auc, float), type(auc)\n"
                            "assert 0.98 < auc <= 1.0, auc"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Puntos de la curva ROC",
                description=(
                    "Devuelve fpr, tpr y thresholds y verifica sus " "propiedades."
                ),
                instructions=(
                    "Implementa `curva_roc(X_train, y_train, X_test, "
                    "y_test)` que entrena el mismo pipeline (StandardScaler "
                    "+ LogisticRegression max_iter=5000, random_state=42), "
                    "saca las probabilidades de la clase 1 y devuelve la "
                    "tupla `(fpr, tpr, thresholds)` de "
                    "`roc_curve(y_test, proba)`."
                ),
                starter_code=(
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.metrics import roc_curve\n"
                    "\n"
                    "\n"
                    "def curva_roc(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: entrena el pipeline y saca proba de clase 1\n"
                    "    # TODO: return roc_curve(y_test, proba)\n"
                    "    ...\n"
                ),
                hints=[
                    "roc_curve devuelve tres arrays alineados.",
                    "fpr y tpr son monotonos no decrecientes.",
                    "La curva arranca en fpr=0 y termina en tpr=1.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "breast_cancer: fpr/tpr monotonos, arranca 0 termina 1",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_breast_cancer\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = load_breast_cancer(return_X_y=True)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
                            "fpr, tpr, thr = curva_roc(Xtr, ytr, Xte, yte)\n"
                            "fpr = np.asarray(fpr); tpr = np.asarray(tpr)\n"
                            "assert len(fpr) == len(tpr), (len(fpr), len(tpr))\n"
                            "assert fpr[0] == 0.0, fpr[0]\n"
                            "assert tpr[-1] == 1.0, tpr[-1]\n"
                            "assert np.all(np.diff(fpr) >= 0), 'fpr no monotona'\n"
                            "assert np.all(np.diff(tpr) >= 0), 'tpr no monotona'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Metricas segun el umbral",
                description=(
                    "Calcula precision y recall a un umbral dado y "
                    "comprueba el trade-off."
                ),
                instructions=(
                    "Implementa `metricas_umbral(X_train, y_train, "
                    "X_test, y_test, umbral)` que entrena el pipeline "
                    "(StandardScaler + LogisticRegression max_iter=5000, "
                    "random_state=42), predice positivo cuando "
                    "`predict_proba` de la clase 1 es `>= umbral`, y "
                    "devuelve un dict `{'precision': ..., 'recall': ...}` "
                    "con floats (usa `zero_division=0`)."
                ),
                starter_code=(
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.metrics import precision_score, recall_score\n"
                    "\n"
                    "\n"
                    "def metricas_umbral(X_train, y_train, X_test, y_test, umbral):\n"
                    "    # TODO: entrena pipeline, proba = predict_proba(X_test)[:, 1]\n"
                    "    # TODO: pred = (proba >= umbral).astype(int)\n"
                    "    # TODO: return {'precision': ..., 'recall': ...}\n"
                    "    ...\n"
                ),
                hints=[
                    "Bajar el umbral atrapa mas positivos: sube el recall.",
                    "zero_division=0 evita warnings si no marcas ningun positivo.",
                    "Compara 0.5 vs 0.3 para ver el trade-off.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "breast_cancer: bajar umbral 0.5->0.3 no baja el recall",
                        "code": (
                            "from sklearn.datasets import load_breast_cancer\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = load_breast_cancer(return_X_y=True)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
                            "m5 = metricas_umbral(Xtr, ytr, Xte, yte, 0.5)\n"
                            "m3 = metricas_umbral(Xtr, ytr, Xte, yte, 0.3)\n"
                            "assert set(m5.keys()) == {'precision', 'recall'}, m5.keys()\n"
                            "assert isinstance(m5['recall'], float), type(m5['recall'])\n"
                            "assert m3['recall'] >= m5['recall'], (m5, m3)\n"
                            "assert m5['precision'] >= m3['precision'] - 1e-9, (m5, m3)"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="DL 1 · La neurona: forward pass y activaciones",
        description=(
            "Arranca Deep Learning desde cero con numpy: que es una "
            "neurona, el forward pass (X @ W + b) y por que las "
            "funciones de activacion dan no-linealidad."
        ),
        content=(
            "# DL 1: la neurona y el forward pass\n\n"
            "Bienvenido al **Track 4 (Deep Learning)**. Antes de tocar "
            "PyTorch vas a entender que hace una red neuronal por "
            "dentro, y lo vas a construir con **numpy puro** (el mismo "
            "que ya usaste en Data Science). Una red no es magia: es "
            "multiplicacion de matrices + una funcion no lineal, "
            "repetido en capas.\n\n"
            "## La neurona\n\n"
            "Una **neurona** toma un vector de entradas `x`, lo combina "
            "linealmente con unos **pesos** `w` y un **sesgo** `b`, y "
            "pasa el resultado por una **funcion de activacion** `f`:\n\n"
            "```\n"
            "z = w . x + b        (combinacion lineal, un escalar)\n"
            "a = f(z)             (activacion)\n"
            "```\n\n"
            "Con varias neuronas en paralelo (una **capa**), los pesos "
            "pasan a ser una matriz `W` y el calculo se vectoriza para "
            "un **batch** de muestras `X` de una sola vez:\n\n"
            "```python\n"
            "import numpy as np\n"
            "Z = X @ W + b        # X: (n_muestras, n_features)\n"
            "                     # W: (n_features, n_units)\n"
            "                     # b: (n_units,)  -> broadcasting\n"
            "                     # Z: (n_muestras, n_units)\n"
            "A = f(Z)\n"
            "```\n\n"
            "El operador `@` es el producto matricial. Ese `X @ W + b` "
            "es **el forward pass de una capa densa**, la operacion mas "
            "repetida en todo el deep learning.\n\n"
            "## Funciones de activacion\n\n"
            "Sin activacion, apilar capas seria inutil: la composicion "
            "de funciones lineales es otra funcion lineal. La "
            "**no-linealidad** es lo que permite a la red aprender "
            "relaciones complejas.\n\n"
            "### Sigmoid\n\n"
            "Aplasta cualquier numero al rango `(0, 1)`. Util para "
            "probabilidades en la capa de salida.\n\n"
            "```\n"
            "sigmoid(z) = 1 / (1 + e^-z)\n"
            "  sigmoid(0)   = 0.5\n"
            "  sigmoid(+inf) -> 1\n"
            "  sigmoid(-inf) -> 0\n"
            "```\n\n"
            "```python\n"
            "def sigmoid(z):\n"
            "    return 1.0 / (1.0 + np.exp(-z))\n"
            "```\n\n"
            "### ReLU\n\n"
            "`relu(z) = max(0, z)`. Cero para negativos, identidad para "
            "positivos. Es la activacion por defecto en las capas "
            "ocultas modernas: barata y no satura para valores "
            "positivos.\n\n"
            "```python\n"
            "def relu(z):\n"
            "    return np.maximum(0.0, z)\n"
            "```\n\n"
            "### tanh\n\n"
            "Parecida a sigmoid pero centrada en 0, rango `(-1, 1)`. "
            "`np.tanh(z)` ya viene en numpy.\n\n"
            "## Por que numpy y no PyTorch (todavia)\n\n"
            "PyTorch automatiza el calculo de gradientes (lo veras "
            "pronto), pero **el forward pass es exactamente esto**: "
            "`X @ W + b` y una activacion. Construirlo a mano en numpy "
            "te da la intuicion que despues PyTorch te esconde. Cuando "
            "pasemos al framework, no sera una caja negra.\n\n"
            "## Errores comunes\n\n"
            "1. **Dimensiones de W al reves** — si `X` es `(n, features)`, "
            "entonces `W` debe ser `(features, units)`. Si las inviertes, "
            "`@` lanza un error de shapes.\n"
            "2. **Olvidar el sesgo** — `b` se suma por broadcasting sobre "
            "cada muestra del batch; su shape es `(units,)`.\n"
            "3. **Aplicar la activacion antes de sumar b** — el orden es "
            "`f(X @ W + b)`, no `f(X @ W) + b`.\n"
            "4. **Creer que sin activacion la red es mas potente** — sin "
            "no-linealidad, 10 capas equivalen a 1.\n\n"
            "## Resumen\n\n"
            "- Una neurona: `a = f(w . x + b)`.\n"
            "- Una capa densa vectorizada: `A = f(X @ W + b)`.\n"
            "- `sigmoid` -> (0,1), `relu` -> max(0, z), `tanh` -> "
            "(-1,1).\n"
            "- La activacion aporta la no-linealidad; sin ella apilar "
            "capas no sirve.\n"
        ),
        difficulty="intermediate",
        category="dl-fundamentos",
        order=33,
        track="track-4",
        estimated_duration=50,
        prerequisites_titles=[
            "ML 11 · Curva ROC, AUC y umbral de decision",
        ],
        exercises=[
            ExerciseTemplate(
                title="Funcion sigmoid",
                description=(
                    "Implementa la activacion sigmoid, vectorizada con " "numpy."
                ),
                instructions=(
                    "Implementa `sigmoid(z)` que devuelve "
                    "`1 / (1 + e^-z)` usando numpy, funcionando tanto "
                    "para escalares como para arrays (vectorizada). "
                    "Convierte la entrada con `np.asarray(z, dtype=float)` "
                    "y usa `np.exp`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def sigmoid(z):\n"
                    "    # TODO: z = np.asarray(z, dtype=float)\n"
                    "    # TODO: return 1.0 / (1.0 + np.exp(-z))\n"
                    "    ...\n"
                ),
                hints=[
                    "np.exp aplica e^x elemento a elemento.",
                    "sigmoid(0) debe dar exactamente 0.5.",
                    "El resultado siempre queda entre 0 y 1.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "sigmoid(0)=0.5, rango (0,1), monotona, vectorizada",
                        "code": (
                            "import numpy as np\n"
                            "assert abs(float(sigmoid(0.0)) - 0.5) < 1e-9\n"
                            "z = np.array([-20.0, -1.0, 0.0, 1.0, 20.0])\n"
                            "s = np.asarray(sigmoid(z))\n"
                            "assert s.shape == (5,), s.shape\n"
                            "assert np.all((s > 0) & (s < 1)), s\n"
                            "assert np.all(np.diff(s) > 0), 'no monotona'\n"
                            "assert s[0] < 1e-6 and s[-1] > 0.999999, s"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Funcion ReLU",
                description=(
                    "Implementa la activacion ReLU con numpy, " "vectorizada."
                ),
                instructions=(
                    "Implementa `relu(z)` que devuelve `max(0, z)` "
                    "elemento a elemento usando `np.maximum`. Debe "
                    "preservar la shape de la entrada (escalares, "
                    "vectores o matrices)."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def relu(z):\n"
                    "    # TODO: z = np.asarray(z, dtype=float)\n"
                    "    # TODO: return np.maximum(0.0, z)\n"
                    "    ...\n"
                ),
                hints=[
                    "np.maximum compara elemento a elemento (no confundir con np.max).",
                    "Los negativos van a 0; los positivos quedan igual.",
                    "La shape de salida es la misma que la de entrada.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "relu: negativos->0, positivos igual, preserva shape",
                        "code": (
                            "import numpy as np\n"
                            "z = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])\n"
                            "r = np.asarray(relu(z))\n"
                            "assert r.shape == (5,), r.shape\n"
                            "assert np.allclose(r, [0, 0, 0, 1, 2]), r\n"
                            "Z = np.array([[-1.0, 3.0], [2.0, -5.0]])\n"
                            "assert np.asarray(relu(Z)).shape == (2, 2)\n"
                            "assert np.all(np.asarray(relu(Z)) >= 0)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Forward pass de una capa densa",
                description=(
                    "Combina producto matricial, sesgo y activacion en "
                    "el forward de una capa."
                ),
                instructions=(
                    "Implementa `forward_capa(X, W, b, activacion)` que "
                    "calcula `activacion(X @ W + b)`, donde `X` es "
                    "`(n_muestras, n_features)`, `W` es "
                    "`(n_features, n_units)`, `b` es `(n_units,)` y "
                    "`activacion` es una funcion (p.ej. `relu` o "
                    "`sigmoid`). Devuelve un array `(n_muestras, "
                    "n_units)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def forward_capa(X, W, b, activacion):\n"
                    "    # TODO: z = np.asarray(X, float) @ np.asarray(W, float) + np.asarray(b, float)\n"
                    "    # TODO: return activacion(z)\n"
                    "    ...\n"
                ),
                hints=[
                    "El orden importa: primero X @ W + b, luego la activacion.",
                    "b se suma por broadcasting sobre cada fila del batch.",
                    "Si las shapes no cuadran, revisa que W sea (features, units).",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "forward_capa: shape (n,units) + valores con relu/sigmoid/lineal",
                        "code": (
                            "import numpy as np\n"
                            "# El test define sus propias activaciones (namespace aislado)\n"
                            "_relu = lambda x: np.maximum(0.0, x)\n"
                            "_sig = lambda x: 1.0 / (1.0 + np.exp(-x))\n"
                            "X = np.array([[1.0, 2.0]])\n"
                            "W = np.array([[0.5], [-0.5]])\n"
                            "b = np.array([0.0])\n"
                            "out_lin = np.asarray(forward_capa(X, W, b, lambda x: x))\n"
                            "assert out_lin.shape == (1, 1), out_lin.shape\n"
                            "assert abs(float(out_lin[0, 0]) - (-0.5)) < 1e-9, out_lin\n"
                            "out_relu = np.asarray(forward_capa(X, W, b, _relu))\n"
                            "assert abs(float(out_relu[0, 0]) - 0.0) < 1e-9, out_relu\n"
                            "out_sig = np.asarray(forward_capa(X, W, b, _sig))\n"
                            "assert abs(float(out_sig[0, 0]) - 0.37754067) < 1e-6, out_sig\n"
                            "Xb = np.ones((3, 2))\n"
                            "Wb = np.ones((2, 4))\n"
                            "bb = np.zeros(4)\n"
                            "assert np.asarray(forward_capa(Xb, Wb, bb, _relu)).shape == (3, 4)"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="DL 2 · Funciones de perdida y gradiente numerico",
        description=(
            "Como mide una red que tan mal lo hace (MSE, cross-entropy) "
            "y como se aproxima un gradiente por diferencias finitas."
        ),
        content=(
            "# DL 2: funciones de perdida y gradiente numerico\n\n"
            "En DL 1 hiciste el forward pass: la red produce una "
            "prediccion. Ahora falta lo mas importante para "
            "**aprender**: medir que tan equivocada esta esa prediccion "
            "y en que direccion mover los pesos para mejorarla. Eso son "
            "la **funcion de perdida** y el **gradiente**.\n\n"
            "## La funcion de perdida\n\n"
            "Una **perdida** (loss) es un numero que resume el error: "
            "grande cuando la red se equivoca, cero cuando acierta "
            "perfecto. Entrenar = **minimizar** la perdida. Cual usar "
            "depende del problema.\n\n"
            "### MSE (error cuadratico medio) — regresion\n\n"
            "Para predecir numeros continuos:\n\n"
            "```\n"
            "MSE = promedio( (y_pred - y_true)^2 )\n"
            "```\n\n"
            "Eleva al cuadrado para (a) penalizar mas los errores "
            "grandes y (b) que el signo no importe. MSE = 0 solo si la "
            "prediccion es exacta.\n\n"
            "```python\n"
            "import numpy as np\n"
            "def mse(y_true, y_pred):\n"
            "    y_true = np.asarray(y_true, float)\n"
            "    y_pred = np.asarray(y_pred, float)\n"
            "    return float(np.mean((y_pred - y_true) ** 2))\n"
            "```\n\n"
            "### Binary cross-entropy (BCE) — clasificacion binaria\n\n"
            "Cuando la red predice una **probabilidad** `p` (0 a 1, la "
            "salida de un sigmoid) y la verdad es 0 o 1:\n\n"
            "```\n"
            "BCE = -promedio( y*log(p) + (1-y)*log(1-p) )\n"
            "```\n\n"
            "Castiga con fuerza la confianza equivocada: si `y=1` y "
            "predices `p=0.01`, `-log(0.01)=4.6` (perdida enorme); si "
            "predices `p=0.99`, `-log(0.99)=0.01` (casi cero).\n\n"
            "**Gotcha del clip:** `log(0)` es `-inf`. Si la red predice "
            "exactamente 0 o 1, la perdida explota. Se evita recortando "
            "`p` a `[eps, 1-eps]` con `np.clip` antes del `log`:\n\n"
            "```python\n"
            "def bce(y_true, y_pred):\n"
            "    y_true = np.asarray(y_true, float)\n"
            "    p = np.clip(np.asarray(y_pred, float), 1e-12, 1 - 1e-12)\n"
            "    return float(-np.mean(y_true*np.log(p) + (1-y_true)*np.log(1-p)))\n"
            "```\n\n"
            "## El gradiente: en que direccion mejorar\n\n"
            "El **gradiente** de la perdida respecto a un peso te dice "
            "cuanto cambia la perdida si mueves ese peso un poquito. Es "
            "la **pendiente**. Para minimizar, das un paso en direccion "
            "**opuesta** al gradiente (descenso de gradiente, DL 4).\n\n"
            "Analiticamente el gradiente se calcula con backprop (DL 3), "
            "pero primero conviene la version conceptual: el **gradiente "
            "numerico** por diferencias finitas centradas.\n\n"
            "```\n"
            "df/dx ~= ( f(x+h) - f(x-h) ) / (2h)     con h pequeno\n"
            "```\n\n"
            "```python\n"
            "def gradiente_numerico(f, x, h=1e-5):\n"
            "    x = np.asarray(x, float)\n"
            "    return (f(x + h) - f(x - h)) / (2 * h)\n"
            "```\n\n"
            "Para `f(x)=x^2` en `x=3`, deberia dar ~6 (la derivada "
            "`2x`). Es **lento** (no sirve para entrenar redes reales, "
            "requiere 2 forward por parametro), pero es la mejor forma "
            "de **verificar** que tu backprop analitico esta bien: se "
            "llama *gradient checking*.\n\n"
            "## La diferencia central es mas precisa\n\n"
            "Podrias usar `(f(x+h) - f(x)) / h` (diferencia hacia "
            "adelante), pero la **centrada** `(f(x+h)-f(x-h))/(2h)` "
            "cancela mas error y da una aproximacion mucho mejor para el "
            "mismo `h`.\n\n"
            "## Errores comunes\n\n"
            "1. **MSE sin promediar** — sumar en vez de promediar hace "
            "la perdida dependiente del tamano del batch.\n"
            "2. **BCE sin clip** — un `p` de 0 o 1 mete un `-inf` y todo "
            "el entrenamiento se vuelve `nan`.\n"
            "3. **h demasiado chico en el gradiente numerico** — con "
            "`h=1e-12` el error de redondeo de floats domina; `1e-5` es "
            "un buen punto medio.\n"
            "4. **Confundir perdida con accuracy** — la perdida es "
            "continua y derivable (por eso entrena); la accuracy es un "
            "conteo, no sirve para el gradiente.\n\n"
            "## Resumen\n\n"
            "- La **perdida** mide el error; entrenar = minimizarla.\n"
            "- `MSE` para regresion, `BCE` para clasificacion binaria "
            "(con `clip` para evitar `log(0)`).\n"
            "- El **gradiente** es la pendiente de la perdida; se avanza "
            "en su direccion opuesta.\n"
            "- El **gradiente numerico** `(f(x+h)-f(x-h))/(2h)` aproxima "
            "la derivada; util para *verificar* backprop, no para "
            "entrenar.\n"
        ),
        difficulty="intermediate",
        category="dl-fundamentos",
        order=34,
        track="track-4",
        estimated_duration=50,
        prerequisites_titles=[
            "DL 1 · La neurona: forward pass y activaciones",
        ],
        exercises=[
            ExerciseTemplate(
                title="Error cuadratico medio (MSE)",
                description=(
                    "Implementa la perdida MSE para regresion, " "vectorizada."
                ),
                instructions=(
                    "Implementa `mse(y_true, y_pred)` que devuelve el "
                    "promedio de `(y_pred - y_true) ** 2` como `float`. "
                    "Convierte ambas entradas con `np.asarray(..., "
                    "float)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def mse(y_true, y_pred):\n"
                    "    # TODO: y_true = np.asarray(y_true, float); y_pred = np.asarray(y_pred, float)\n"
                    "    # TODO: return float(np.mean((y_pred - y_true) ** 2))\n"
                    "    ...\n"
                ),
                hints=[
                    "np.mean promedia todos los elementos.",
                    "Elevar al cuadrado elimina el signo del error.",
                    "MSE de una prediccion perfecta es 0.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "mse: casos conocidos, simetria, float",
                        "code": (
                            "import numpy as np\n"
                            "assert mse([1, 2, 3], [1, 2, 3]) == 0\n"
                            "assert abs(mse([0, 0], [1, 1]) - 1.0) < 1e-12\n"
                            "assert abs(mse([3.0], [0.0]) - 9.0) < 1e-12\n"
                            "assert isinstance(mse([1.0], [2.0]), float)\n"
                            "a = [1.0, 2.0, 3.0]\n"
                            "b = [2.0, 0.0, 5.0]\n"
                            "assert abs(mse(a, b) - mse(b, a)) < 1e-12"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Binary cross-entropy (BCE)",
                description=(
                    "Implementa la perdida de clasificacion binaria con "
                    "clip para evitar log(0)."
                ),
                instructions=(
                    "Implementa `bce(y_true, y_pred)` = "
                    "`-promedio(y*log(p) + (1-y)*log(1-p))`. Recorta "
                    "`y_pred` a `[1e-12, 1 - 1e-12]` con `np.clip` antes "
                    "de los logaritmos para no obtener `-inf`. Devuelve "
                    "un `float`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def bce(y_true, y_pred):\n"
                    "    # TODO: y_true = np.asarray(y_true, float)\n"
                    "    # TODO: p = np.clip(np.asarray(y_pred, float), 1e-12, 1 - 1e-12)\n"
                    "    # TODO: return float(-np.mean(y_true*np.log(p) + (1-y_true)*np.log(1-p)))\n"
                    "    ...\n"
                ),
                hints=[
                    "El clip es lo que evita log(0) = -inf.",
                    "Predecir p cercano a la verdad da perdida cercana a 0.",
                    "Predecir con confianza lo contrario da perdida alta.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "bce: valores conocidos, clip finito, peor > mejor",
                        "code": (
                            "import numpy as np\n"
                            "assert abs(bce([1], [0.9]) - 0.105360516) < 1e-5, bce([1], [0.9])\n"
                            "assert abs(bce([0], [0.1]) - 0.105360516) < 1e-5\n"
                            "assert bce([1, 0], [0.999, 0.001]) < 0.01\n"
                            "assert bce([1], [0.01]) > bce([1], [0.99])\n"
                            "assert np.isfinite(bce([1], [1.0]))\n"
                            "assert np.isfinite(bce([0], [0.0]))"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Gradiente numerico",
                description=(
                    "Aproxima la derivada de una funcion por diferencias "
                    "finitas centradas."
                ),
                instructions=(
                    "Implementa `gradiente_numerico(f, x, h=1e-5)` que "
                    "devuelve `(f(x + h) - f(x - h)) / (2 * h)`. Funciona "
                    "para `x` escalar o array (vectorizado con numpy). "
                    "`f` es una funcion que recibe un numero/array y "
                    "devuelve lo mismo."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def gradiente_numerico(f, x, h=1e-5):\n"
                    "    # TODO: x = np.asarray(x, float)\n"
                    "    # TODO: return (f(x + h) - f(x - h)) / (2 * h)\n"
                    "    ...\n"
                ),
                hints=[
                    "La diferencia centrada es mas precisa que la de adelante.",
                    "Para f(x)=x^2, la derivada en x es 2x.",
                    "Como usa numpy, funciona elemento a elemento sobre un array.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "gradiente: x^2->2x, x^3->3x^2, vectorizado",
                        "code": (
                            "import numpy as np\n"
                            "g = gradiente_numerico(lambda x: x**2, 3.0)\n"
                            "assert abs(float(g) - 6.0) < 1e-3, g\n"
                            "gv = np.asarray(gradiente_numerico(lambda x: x**2, np.array([1.0, 2.0, 3.0])))\n"
                            "assert np.allclose(gv, [2, 4, 6], atol=1e-3), gv\n"
                            "g3 = gradiente_numerico(lambda x: x**3, 2.0)\n"
                            "assert abs(float(g3) - 12.0) < 1e-2, g3"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="DL 3 · Backpropagation: la regla de la cadena",
        description=(
            "Como fluye el gradiente hacia atras por la red: derivada "
            "local de la activacion, backward de la capa lineal, y "
            "gradient checking contra el gradiente numerico."
        ),
        content=(
            "# DL 3: backpropagation\n\n"
            "Ya sabes hacer el forward (DL 1) y medir el error (DL 2). "
            "**Backpropagation** es el algoritmo que calcula el "
            "gradiente de la perdida respecto a **cada** peso de forma "
            "eficiente, para poder ajustarlos. No es mas que la **regla "
            "de la cadena** del calculo, aplicada capa por capa de la "
            "salida hacia la entrada.\n\n"
            "## La regla de la cadena\n\n"
            "Si `L` depende de `a`, y `a` depende de `z`, y `z` depende "
            "de `W`, entonces:\n\n"
            "```\n"
            "dL/dW = dL/da * da/dz * dz/dW\n"
            "```\n\n"
            "Backprop calcula esto de derecha a izquierda: parte del "
            "**gradiente que llega de arriba** (`dL/da`, el *upstream "
            "gradient*), lo multiplica por la **derivada local** de cada "
            "operacion, y propaga el resultado hacia atras. Cada nodo "
            "solo necesita saber su derivada local.\n\n"
            "## Backward de una activacion\n\n"
            "Para el sigmoid hay un truco precioso: si `a = sigmoid(z)`, "
            "su derivada local se escribe en terminos de la **propia "
            "salida**:\n\n"
            "```\n"
            "da/dz = a * (1 - a)\n"
            "```\n\n"
            "Asi que el gradiente que sale hacia atras es el que entra "
            "multiplicado elemento a elemento por la derivada local:\n\n"
            "```python\n"
            "def grad_sigmoid(a, grad_out):   # a = salida del sigmoid\n"
            "    return grad_out * a * (1 - a)\n"
            "```\n\n"
            "(Para ReLU la derivada local es `1` donde `z > 0` y `0` "
            "donde `z <= 0`.)\n\n"
            "## Backward de una capa lineal\n\n"
            "El forward era `z = X @ W + b`. Dado el gradiente que llega "
            "`grad_z = dL/dz`, la regla de la cadena da las tres "
            "derivadas locales (esto se deduce, pero conviene "
            "memorizarlo):\n\n"
            "```\n"
            "dW = X.T @ grad_z        # como cambiar los pesos\n"
            "db = grad_z.sum(axis=0)  # el sesgo suma sobre el batch\n"
            "dX = grad_z @ W.T        # gradiente que sigue hacia atras\n"
            "```\n\n"
            "```python\n"
            "def backward_lineal(X, W, grad_z):\n"
            "    dW = X.T @ grad_z\n"
            "    db = grad_z.sum(axis=0)\n"
            "    dX = grad_z @ W.T\n"
            "    return dW, db, dX\n"
            "```\n\n"
            "Fijate en las **transpuestas**: hacen que las shapes "
            "cuadren. `dW` tiene la shape de `W`, `dX` la de `X`. Si "
            "algo no cuadra, casi siempre es una transpuesta mal "
            "puesta.\n\n"
            "## Gradient checking: no te fies, verifica\n\n"
            "El backprop analitico es facil de equivocar (un signo, una "
            "transpuesta). La forma estandar de verificarlo es "
            "compararlo contra el **gradiente numerico** de DL 2: "
            "perturbas cada peso un `h` y mides como cambia la perdida. "
            "Si el analitico y el numerico coinciden (hasta ~1e-4), tu "
            "backprop esta bien.\n\n"
            "```\n"
            "para cada peso W[i,j]:\n"
            "  num[i,j] = ( L(W con W[i,j]+h) - L(W con W[i,j]-h) ) / (2h)\n"
            "comparar num  vs  gradiente analitico   -> deben coincidir\n"
            "```\n\n"
            "Esta es la mejor red de seguridad al implementar backprop a "
            "mano. PyTorch lo hace por ti con autograd (lo veras "
            "despues), pero ahora entiendes que hay debajo.\n\n"
            "## Errores comunes\n\n"
            "1. **Transpuesta olvidada** — `dW = X @ grad_z` en vez de "
            "`X.T @ grad_z`: las shapes no cuadran o el gradiente es "
            "erroneo.\n"
            "2. **Usar z en vez de a en grad_sigmoid** — la formula "
            "`a*(1-a)` usa la **salida** del sigmoid, no la entrada.\n"
            "3. **No sumar el sesgo sobre el batch** — `db` es "
            "`grad_z.sum(axis=0)`; el bias se comparte entre muestras.\n"
            "4. **Saltarse el gradient checking** — implementar backprop "
            "sin verificarlo numericamente es pedir un bug silencioso.\n\n"
            "## Resumen\n\n"
            "- Backprop = regla de la cadena aplicada de la salida hacia "
            "la entrada.\n"
            "- Cada operacion aporta su **derivada local**; se multiplica "
            "por el gradiente *upstream*.\n"
            "- Capa lineal: `dW = X.T @ grad_z`, `db = grad_z.sum(0)`, "
            "`dX = grad_z @ W.T`.\n"
            "- Sigmoid: `da/dz = a*(1-a)`.\n"
            "- **Verifica** siempre con gradient checking contra el "
            "gradiente numerico.\n"
        ),
        difficulty="advanced",
        category="dl-fundamentos",
        order=35,
        track="track-4",
        estimated_duration=60,
        prerequisites_titles=[
            "DL 2 · Funciones de perdida y gradiente numerico",
        ],
        exercises=[
            ExerciseTemplate(
                title="Backward del sigmoid",
                description=(
                    "Propaga el gradiente a traves de un sigmoid usando "
                    "su derivada local a*(1-a)."
                ),
                instructions=(
                    "Implementa `grad_sigmoid(a, grad_out)` donde `a` es "
                    "la **salida** del sigmoid y `grad_out` es el "
                    "gradiente que llega de arriba (`dL/da`). Devuelve "
                    "`grad_out * a * (1 - a)` (elemento a elemento)."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def grad_sigmoid(a, grad_out):\n"
                    "    # a = salida del sigmoid; grad_out = dL/da\n"
                    "    # TODO: a = np.asarray(a, float); grad_out = np.asarray(grad_out, float)\n"
                    "    # TODO: return grad_out * a * (1 - a)\n"
                    "    ...\n"
                ),
                hints=[
                    "La derivada local del sigmoid es a*(1-a), con a la SALIDA.",
                    "En a=0.5 la derivada local vale 0.25 (el maximo).",
                    "Multiplica elemento a elemento por grad_out.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "grad_sigmoid: a(1-a) y coincide con derivada numerica",
                        "code": (
                            "import numpy as np\n"
                            "assert abs(float(grad_sigmoid(0.5, 1.0)) - 0.25) < 1e-12\n"
                            "assert abs(float(grad_sigmoid(0.8, 2.0)) - 0.32) < 1e-12\n"
                            "out = np.asarray(grad_sigmoid(np.array([0.5, 0.8]), np.array([1.0, 1.0])))\n"
                            "assert out.shape == (2,), out.shape\n"
                            "sig = lambda z: 1.0 / (1.0 + np.exp(-z))\n"
                            "z0 = 0.7\n"
                            "a = sig(z0)\n"
                            "h = 1e-5\n"
                            "analitico = float(grad_sigmoid(a, 1.0))\n"
                            "numerico = (sig(z0 + h) - sig(z0 - h)) / (2 * h)\n"
                            "assert abs(analitico - numerico) < 1e-4, (analitico, numerico)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Backward de la capa lineal",
                description=(
                    "Calcula los gradientes dW, db y dX de una capa " "z = X @ W + b."
                ),
                instructions=(
                    "Implementa `backward_lineal(X, W, grad_z)` que, "
                    "dado el gradiente `grad_z = dL/dz`, devuelve la "
                    "tupla `(dW, db, dX)` con `dW = X.T @ grad_z`, "
                    "`db = grad_z.sum(axis=0)` y `dX = grad_z @ W.T`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def backward_lineal(X, W, grad_z):\n"
                    "    # TODO: dW = X.T @ grad_z\n"
                    "    # TODO: db = grad_z.sum(axis=0)\n"
                    "    # TODO: dX = grad_z @ W.T\n"
                    "    # TODO: return dW, db, dX\n"
                    "    ...\n"
                ),
                hints=[
                    "dW tiene la misma shape que W; dX la misma que X.",
                    "Las transpuestas son las que hacen cuadrar las shapes.",
                    "db suma el gradiente sobre las muestras del batch (axis=0).",
                ],
                difficulty="advanced",
                points=25,
                hidden_tests=[
                    {
                        "name": "backward_lineal: shapes y valores (dW, db, dX)",
                        "code": (
                            "import numpy as np\n"
                            "X = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])\n"
                            "W = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])\n"
                            "grad_z = np.array([[1.0, 0.0], [0.0, 1.0]])\n"
                            "dW, db, dX = backward_lineal(X, W, grad_z)\n"
                            "dW = np.asarray(dW)\n"
                            "db = np.asarray(db)\n"
                            "dX = np.asarray(dX)\n"
                            "assert dW.shape == (3, 2), dW.shape\n"
                            "assert db.shape == (2,), db.shape\n"
                            "assert dX.shape == (2, 3), dX.shape\n"
                            "assert np.allclose(dW, X.T @ grad_z)\n"
                            "assert np.allclose(db, [1.0, 1.0])\n"
                            "assert np.allclose(dX, grad_z @ W.T)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Gradient checking de una capa lineal + MSE",
                description=(
                    "Calcula el gradiente analitico de la perdida MSE "
                    "respecto a W y verifica que coincide con el "
                    "numerico."
                ),
                instructions=(
                    "Para una capa `z = X @ W + b` con perdida "
                    "`L = mean((z - y_true) ** 2)`, implementa "
                    "`grad_W(X, W, b, y_true)` que devuelve `dL/dW`. "
                    "Pista: `dL/dz = 2 * (z - y_true) / z.size` y "
                    "`dL/dW = X.T @ dL/dz`. El test compara tu resultado "
                    "contra el gradiente numerico (gradient checking)."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def grad_W(X, W, b, y_true):\n"
                    "    # TODO: z = X @ W + b\n"
                    "    # TODO: dz = 2.0 * (z - y_true) / z.size\n"
                    "    # TODO: return X.T @ dz\n"
                    "    ...\n"
                ),
                hints=[
                    "El factor 2 y el /z.size vienen de derivar la media de cuadrados.",
                    "dL/dW = X.T @ dL/dz, igual que en backward_lineal.",
                    "Si coincide con el numerico hasta 1e-4, tu gradiente esta bien.",
                ],
                difficulty="advanced",
                points=25,
                hidden_tests=[
                    {
                        "name": "grad_W coincide con el gradiente numerico",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "X = rng.normal(size=(5, 3))\n"
                            "W = rng.normal(size=(3, 1))\n"
                            "b = np.array([0.5])\n"
                            "y = rng.normal(size=(5, 1))\n"
                            "g = np.asarray(grad_W(X, W, b, y))\n"
                            "assert g.shape == W.shape, g.shape\n"
                            "def loss(Wm):\n"
                            "    z = X @ Wm + b\n"
                            "    return float(np.mean((z - y) ** 2))\n"
                            "h = 1e-5\n"
                            "num = np.zeros_like(W)\n"
                            "for i in range(W.shape[0]):\n"
                            "    for j in range(W.shape[1]):\n"
                            "        Wp = W.copy(); Wp[i, j] += h\n"
                            "        Wm = W.copy(); Wm[i, j] -= h\n"
                            "        num[i, j] = (loss(Wp) - loss(Wm)) / (2 * h)\n"
                            "assert np.allclose(g, num, atol=1e-4), (g.ravel(), num.ravel())"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="DL 4 · Training loop: entrenar con descenso de gradiente",
        description=(
            "Junta forward, perdida, backward y actualizacion de pesos "
            "en un bucle que entrena de verdad: regresion y clasificacion "
            "logistica desde cero, viendo bajar la perdida."
        ),
        content=(
            "# DL 4: el bucle de entrenamiento\n\n"
            "Ya tienes todas las piezas: forward (DL 1), perdida (DL 2) "
            "y gradientes (DL 3). **Entrenar** es repetirlas en un bucle "
            "y, en cada vuelta, empujar los pesos un pasito en la "
            "direccion que reduce la perdida. Eso es el **descenso de "
            "gradiente**.\n\n"
            "## El paso de descenso\n\n"
            "El gradiente apunta hacia donde la perdida **crece**. Para "
            "minimizar, te mueves en direccion **contraria**, escalado "
            "por el **learning rate** `lr`:\n\n"
            "```\n"
            "W <- W - lr * dW\n"
            "```\n\n"
            "```python\n"
            "def paso_sgd(param, grad, lr):\n"
            "    return param - lr * grad\n"
            "```\n\n"
            "- `lr` muy chico -> entrena lentisimo.\n"
            "- `lr` muy grande -> la perdida oscila o **diverge** (se "
            "va a infinito).\n"
            "- El punto justo hace bajar la perdida de forma estable.\n\n"
            "## El bucle completo\n\n"
            "Un entrenamiento no es mas que esto, repetido N **epocas**:\n\n"
            "```\n"
            "inicializa W, b\n"
            "repite epocas veces:\n"
            "    z = forward(X, W, b)          # 1. forward\n"
            "    perdida = loss(z, y)          # 2. medir error\n"
            "    dW, db = backward(...)        # 3. gradientes\n"
            "    W = W - lr * dW               # 4. actualizar\n"
            "    b = b - lr * db\n"
            "```\n\n"
            "Para **regresion lineal** (`z = X @ W + b`, perdida MSE) el "
            "gradiente ya lo dedujiste en DL 3:\n\n"
            "```python\n"
            "z = X @ W + b\n"
            "dz = 2 * (z - y) / z.size\n"
            "W = W - lr * (X.T @ dz)\n"
            "b = b - lr * dz.sum(axis=0)\n"
            "```\n\n"
            "Si guardas la perdida de cada epoca, veras una curva que "
            "**baja** hasta estabilizarse. Esa curva es tu mejor amiga "
            "para diagnosticar el entrenamiento.\n\n"
            "## El mismo bucle sirve para clasificar\n\n"
            "Cambia la activacion y la perdida y ya tienes **regresion "
            "logistica**: `p = sigmoid(X @ W + b)`, perdida BCE. Y aqui "
            "pasa algo precioso: al combinar sigmoid + BCE, el gradiente "
            "se simplifica al **mismo** que en regresion lineal:\n\n"
            "```\n"
            "dz = (p - y) / N        # p = sigmoid(z), N = numero de muestras\n"
            "```\n\n"
            "Es decir: **el bucle es identico**, solo cambian la "
            "activacion del forward y la formula de la perdida que "
            "registras. Esa uniformidad es lo que hace que las redes "
            "escalen a arquitecturas enormes.\n\n"
            "## Errores comunes\n\n"
            "1. **Learning rate mal elegido** — si la perdida sube o se "
            "vuelve `nan`, bajalo (prueba /10). Si baja lentisimo, "
            "subelo.\n"
            "2. **No normalizar las features** — con features de escalas "
            "muy distintas, un `lr` unico no sirve para todas; el "
            "descenso zigzaguea (recuerda `StandardScaler` de Track 3).\n"
            "3. **Actualizar W usando el z ya actualizado** — calcula "
            "todos los gradientes con los pesos actuales, *despues* "
            "actualiza.\n"
            "4. **Olvidar sumar el bias sobre el batch** — `db` es "
            "`dz.sum(axis=0)`, no `dz`.\n\n"
            "## Resumen\n\n"
            "- Descenso de gradiente: `W <- W - lr * dW`, repetido por "
            "epocas.\n"
            "- El bucle es forward -> perdida -> backward -> "
            "actualizar.\n"
            "- La **curva de perdida** debe bajar; si sube, el `lr` es "
            "muy grande.\n"
            "- El mismo bucle entrena regresion (MSE) y clasificacion "
            "(sigmoid + BCE); en ambos `dz` termina siendo `(pred - y)` "
            "normalizado.\n"
        ),
        difficulty="advanced",
        category="dl-fundamentos",
        order=36,
        track="track-4",
        estimated_duration=60,
        prerequisites_titles=[
            "DL 3 · Backpropagation: la regla de la cadena",
        ],
        exercises=[
            ExerciseTemplate(
                title="Paso de descenso de gradiente",
                description=(
                    "Implementa la actualizacion de un parametro en "
                    "direccion opuesta al gradiente."
                ),
                instructions=(
                    "Implementa `paso_sgd(param, grad, lr)` que devuelve "
                    "`param - lr * grad` (funciona para escalares o "
                    "arrays). Convierte con `np.asarray(..., float)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def paso_sgd(param, grad, lr):\n"
                    "    # TODO: return np.asarray(param, float) - lr * np.asarray(grad, float)\n"
                    "    ...\n"
                ),
                hints=[
                    "Se resta porque el gradiente apunta hacia donde la perdida crece.",
                    "lr escala el tamano del paso.",
                    "Funciona elemento a elemento sobre arrays.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "paso_sgd resta lr*grad",
                        "code": (
                            "import numpy as np\n"
                            "out = np.asarray(paso_sgd(np.array([1.0, 2.0]), np.array([0.5, -1.0]), 0.1))\n"
                            "assert np.allclose(out, [0.95, 2.1]), out\n"
                            "assert abs(float(paso_sgd(5.0, 2.0, 0.5)) - 4.0) < 1e-12"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Entrenar regresion lineal",
                description=(
                    "Escribe el bucle de entrenamiento completo para "
                    "regresion lineal con MSE."
                ),
                instructions=(
                    "Implementa `entrenar_regresion(X, y, lr=0.1, "
                    "epocas=500)` que inicializa `W = zeros((n_features, "
                    "1))` y `b = zeros(1)`, y en cada epoca: calcula "
                    "`z = X @ W + b`, guarda la perdida MSE en una lista, "
                    "computa `dz = 2*(z - y)/z.size`, y actualiza "
                    "`W -= lr*(X.T @ dz)` y `b -= lr*dz.sum(axis=0)`. "
                    "`y` puede venir como `(n,)` o `(n,1)` (usa "
                    "`.reshape(-1, 1)`). Devuelve `(W, b, historial)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def entrenar_regresion(X, y, lr=0.1, epocas=500):\n"
                    "    X = np.asarray(X, float)\n"
                    "    y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    W = np.zeros((X.shape[1], 1))\n"
                    "    b = np.zeros((1,))\n"
                    "    historial = []\n"
                    "    # TODO: bucle de epocas: forward, guardar MSE, dz, actualizar W y b\n"
                    "    return W, b, historial\n"
                ),
                hints=[
                    "Guarda la perdida ANTES de actualizar los pesos de esa epoca.",
                    "dz = 2*(z - y)/z.size; dW = X.T @ dz; db = dz.sum(axis=0).",
                    "En un problema convexo la perdida baja de forma monotona.",
                ],
                difficulty="advanced",
                points=25,
                hidden_tests=[
                    {
                        "name": "entrenar_regresion: perdida baja y converge a W_true",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "X = rng.normal(size=(20, 3))\n"
                            "W_true = np.array([[1.0], [-2.0], [0.5]])\n"
                            "y = X @ W_true + 0.3\n"
                            "W, b, hist = entrenar_regresion(X, y, lr=0.1, epocas=800)\n"
                            "assert len(hist) == 800, len(hist)\n"
                            "assert hist[-1] < hist[0], (hist[0], hist[-1])\n"
                            "assert all(hist[i + 1] <= hist[i] + 1e-9 for i in range(len(hist) - 1)), 'no monotono'\n"
                            "assert hist[-1] < 1e-4, hist[-1]\n"
                            "assert np.allclose(np.asarray(W), W_true, atol=0.05), np.asarray(W).ravel()"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Entrenar regresion logistica",
                description=(
                    "El mismo bucle, pero con sigmoid + BCE para " "clasificar."
                ),
                instructions=(
                    "Implementa `entrenar_logistica(X, y, lr=0.5, "
                    "epocas=500)`: en cada epoca calcula "
                    "`p = sigmoid(X @ W + b)`, guarda la perdida BCE (con "
                    "clip a `[1e-12, 1-1e-12]`), y actualiza con "
                    "`dz = (p - y) / N` (N = numero de muestras), "
                    "`W -= lr*(X.T @ dz)`, `b -= lr*dz.sum(axis=0)`. "
                    "Inicializa `W`, `b` en cero. Devuelve "
                    "`(W, b, historial)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def entrenar_logistica(X, y, lr=0.5, epocas=500):\n"
                    "    X = np.asarray(X, float)\n"
                    "    y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    W = np.zeros((X.shape[1], 1))\n"
                    "    b = np.zeros((1,))\n"
                    "    historial = []\n"
                    "    # TODO: bucle: p = sigmoid(X@W+b), guardar BCE, dz=(p-y)/N, actualizar\n"
                    "    return W, b, historial\n"
                ),
                hints=[
                    "sigmoid(z) = 1/(1+exp(-z)).",
                    "El gradiente sigmoid+BCE se simplifica a dz = (p - y)/N.",
                    "Con datos separables, la accuracy final debe superar 0.9.",
                ],
                difficulty="advanced",
                points=25,
                hidden_tests=[
                    {
                        "name": "entrenar_logistica: perdida baja y clasifica > 0.9",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(1)\n"
                            "X = rng.normal(size=(60, 2))\n"
                            "W_true = np.array([[2.0], [-1.0]])\n"
                            "y = ((X @ W_true + 0.5) > 0).astype(float).reshape(-1, 1)\n"
                            "W, b, hist = entrenar_logistica(X, y, lr=0.5, epocas=800)\n"
                            "assert hist[-1] < hist[0], (hist[0], hist[-1])\n"
                            "p = 1.0 / (1.0 + np.exp(-(X @ np.asarray(W) + np.asarray(b))))\n"
                            "acc = float(np.mean((p > 0.5).astype(float) == y))\n"
                            "assert acc > 0.9, acc"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="DL 5 · Tu primer MLP: dos capas resuelven XOR",
        description=(
            "El clima de los fundamentos: una red de 2 capas con "
            "forward y backward encadenados, entrenada para resolver "
            "XOR, el problema no lineal que una sola neurona no puede."
        ),
        content=(
            "# DL 5: el perceptron multicapa (MLP)\n\n"
            "Una sola capa lineal (con o sin sigmoid) solo puede trazar "
            "una **frontera recta**. Hay problemas donde eso no alcanza. "
            "El clasico es **XOR**:\n\n"
            "```\n"
            "  (0,0) -> 0     (0,1) -> 1\n"
            "  (1,0) -> 1     (1,1) -> 0\n"
            "```\n\n"
            "No existe ninguna recta que separe los 1 de los 0. Este "
            "problema **hundio a los perceptrones** en los anos 70... "
            "hasta que se apilaron capas con no-linealidad. Un **MLP "
            "(perceptron multicapa)** de 2 capas lo resuelve sin "
            "problema.\n\n"
            "## Arquitectura de 2 capas\n\n"
            "```\n"
            "X --[W1,b1]--> z1 --relu--> h --[W2,b2]--> z2 --sigmoid--> p\n"
            "   capa oculta                capa de salida\n"
            "```\n\n"
            "```python\n"
            "z1 = X @ W1 + b1     # capa oculta\n"
            "h  = relu(z1)        # no-linealidad (¡clave!)\n"
            "z2 = h @ W2 + b2     # capa de salida\n"
            "p  = sigmoid(z2)     # probabilidad\n"
            "```\n\n"
            "La capa oculta transforma el espacio para que el problema "
            "**si** sea linealmente separable en la salida. Sin el "
            "`relu` de por medio, las dos capas colapsarian en una sola "
            "(recuerda DL 1): la no-linealidad es lo que da el poder.\n\n"
            "## Backward encadenado\n\n"
            "El gradiente fluye hacia atras por **las dos** capas, "
            "aplicando la regla de la cadena de DL 3 dos veces. Con "
            "salida sigmoid + BCE, `dz2 = (p - y)/N`, y de ahi:\n\n"
            "```python\n"
            "dz2 = (p - y) / N\n"
            "dW2 = h.T @ dz2\n"
            "db2 = dz2.sum(axis=0)\n"
            "dh  = dz2 @ W2.T          # gradiente que baja a la capa oculta\n"
            "dz1 = dh * (z1 > 0)       # derivada local del relu\n"
            "dW1 = X.T @ dz1\n"
            "db1 = dz1.sum(axis=0)\n"
            "```\n\n"
            "Nota como el gradiente de la capa 2 (`dh`) se convierte en "
            "el gradiente *upstream* de la capa 1. Eso es "
            "backpropagation encadenado: la salida de un backward "
            "alimenta al siguiente. Con 50 capas seria el mismo patron, "
            "50 veces.\n\n"
            "## Entrenar\n\n"
            "El bucle es identico al de DL 4 (forward -> perdida -> "
            "backward -> actualizar), solo que ahora actualizas "
            "**cuatro** grupos de parametros: `W1, b1, W2, b2`. Con "
            "suficientes neuronas ocultas (p.ej. 8) y epocas, la red "
            "aprende XOR y clasifica los 4 puntos perfecto.\n\n"
            "## Errores comunes\n\n"
            "1. **Olvidar la derivada del relu** — `dz1 = dh * (z1 > 0)`. "
            "Sin ese `(z1 > 0)`, el gradiente de la capa oculta esta "
            "mal.\n"
            "2. **Encadenar mal** — el `dh = dz2 @ W2.T` es lo que "
            "conecta las dos capas; es facil equivocar la transpuesta.\n"
            "3. **Red demasiado pequena** — con 1-2 neuronas ocultas "
            "quiza no aprenda XOR; dale unas 8.\n"
            "4. **Inicializar los pesos en cero** — si `W1` es todo "
            "ceros, todas las neuronas ocultas hacen lo mismo y nunca se "
            "diferencian (*symmetry breaking*). Se inicializan al azar.\n\n"
            "## Resumen\n\n"
            "- Un **MLP** apila capas con no-linealidad entre medias; "
            "resuelve problemas no lineales como XOR.\n"
            "- Forward: `relu(X@W1+b1)` -> `sigmoid(h@W2+b2)`.\n"
            "- Backward: encadena la regla de la cadena; el gradiente de "
            "una capa es el *upstream* de la anterior.\n"
            "- Con esto ya construiste una red neuronal **completa** "
            "desde cero. Lo que sigue (PyTorch) automatiza justo este "
            "backward que ya entiendes.\n"
        ),
        difficulty="advanced",
        category="dl-fundamentos",
        order=37,
        track="track-4",
        estimated_duration=70,
        prerequisites_titles=[
            "DL 4 · Training loop: entrenar con descenso de gradiente",
        ],
        exercises=[
            ExerciseTemplate(
                title="Forward de un MLP de 2 capas",
                description=(
                    "Encadena capa oculta (relu) y capa de salida " "(sigmoid)."
                ),
                instructions=(
                    "Implementa `forward_mlp(X, W1, b1, W2, b2)` que "
                    "calcula `z1 = X @ W1 + b1`, `h = relu(z1)`, "
                    "`z2 = h @ W2 + b2` y devuelve `p = sigmoid(z2)` "
                    "(las probabilidades de salida)."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def forward_mlp(X, W1, b1, W2, b2):\n"
                    "    # TODO: z1 = X @ W1 + b1; h = np.maximum(0.0, z1)\n"
                    "    # TODO: z2 = h @ W2 + b2\n"
                    "    # TODO: return 1.0 / (1.0 + np.exp(-z2))\n"
                    "    ...\n"
                ),
                hints=[
                    "El relu de la capa oculta es np.maximum(0.0, z1).",
                    "La salida pasa por sigmoid, no por relu.",
                    "Shapes: X (n,d_in), W1 (d_in,d_oculta), W2 (d_oculta,1).",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "forward_mlp: shape y valor conocido sigmoid(2)",
                        "code": (
                            "import numpy as np\n"
                            "X = np.array([[1.0, 1.0]])\n"
                            "W1 = np.array([[1.0, 0.0], [0.0, 1.0]])\n"
                            "b1 = np.array([0.0, 0.0])\n"
                            "W2 = np.array([[1.0], [1.0]])\n"
                            "b2 = np.array([0.0])\n"
                            "p = np.asarray(forward_mlp(X, W1, b1, W2, b2))\n"
                            "assert p.shape == (1, 1), p.shape\n"
                            "assert 0 < float(p[0, 0]) < 1\n"
                            "assert abs(float(p[0, 0]) - 0.880797) < 1e-4, p\n"
                            "Xb = np.zeros((5, 2))\n"
                            "assert np.asarray(forward_mlp(Xb, W1, b1, W2, b2)).shape == (5, 1)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Backward encadenado del MLP",
                description=(
                    "Propaga el gradiente por las dos capas y verifica "
                    "con gradient checking."
                ),
                instructions=(
                    "Implementa `backward_mlp(X, W1, b1, W2, b2, y)` que "
                    "hace el forward, y con perdida BCE calcula los "
                    "gradientes de las dos capas: "
                    "`dz2 = (p - y)/N`, `dW2 = h.T @ dz2`, "
                    "`db2 = dz2.sum(0)`, `dh = dz2 @ W2.T`, "
                    "`dz1 = dh * (z1 > 0)`, `dW1 = X.T @ dz1`, "
                    "`db1 = dz1.sum(0)`. Devuelve `(dW1, db1, dW2, db2)`. "
                    "`N` es el numero de muestras."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def backward_mlp(X, W1, b1, W2, b2, y):\n"
                    "    X = np.asarray(X, float)\n"
                    "    y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    N = X.shape[0]\n"
                    "    # forward guardando z1, h, p\n"
                    "    # TODO: z1 = X @ W1 + b1; h = np.maximum(0.0, z1)\n"
                    "    # TODO: p = 1/(1+exp(-(h @ W2 + b2)))\n"
                    "    # backward encadenado\n"
                    "    # TODO: dz2 = (p - y)/N; dW2 = h.T @ dz2; db2 = dz2.sum(0)\n"
                    "    # TODO: dh = dz2 @ W2.T; dz1 = dh * (z1 > 0)\n"
                    "    # TODO: dW1 = X.T @ dz1; db1 = dz1.sum(0)\n"
                    "    # TODO: return dW1, db1, dW2, db2\n"
                    "    ...\n"
                ),
                hints=[
                    "dh = dz2 @ W2.T conecta la salida con la capa oculta.",
                    "La derivada del relu es (z1 > 0): 1 donde z1 positivo, 0 si no.",
                    "El gradiente numerico de DL 2 sirve para verificar esto.",
                ],
                difficulty="advanced",
                points=30,
                hidden_tests=[
                    {
                        "name": "backward_mlp: coincide con gradiente numerico (dW1)",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "X = rng.normal(size=(6, 3))\n"
                            "y = (rng.normal(size=(6, 1)) > 0).astype(float)\n"
                            "W1 = rng.normal(size=(3, 4)) * 0.5\n"
                            "b1 = rng.normal(size=(4,)) * 0.5\n"
                            "W2 = rng.normal(size=(4, 1)) * 0.5\n"
                            "b2 = np.array([0.1])\n"
                            "dW1, db1, dW2, db2 = backward_mlp(X, W1, b1, W2, b2, y)\n"
                            "dW1 = np.asarray(dW1)\n"
                            "dW2 = np.asarray(dW2)\n"
                            "assert dW1.shape == W1.shape and dW2.shape == W2.shape\n"
                            "def loss(W1_, b1_, W2_, b2_):\n"
                            "    z1 = X @ W1_ + b1_\n"
                            "    h = np.maximum(0.0, z1)\n"
                            "    p = 1.0 / (1.0 + np.exp(-(h @ W2_ + b2_)))\n"
                            "    pc = np.clip(p, 1e-12, 1 - 1e-12)\n"
                            "    return float(-np.mean(y*np.log(pc) + (1-y)*np.log(1-pc)))\n"
                            "h = 1e-5\n"
                            "num = np.zeros_like(W1)\n"
                            "for i in range(W1.shape[0]):\n"
                            "    for j in range(W1.shape[1]):\n"
                            "        Wp = W1.copy(); Wp[i, j] += h\n"
                            "        Wm = W1.copy(); Wm[i, j] -= h\n"
                            "        num[i, j] = (loss(Wp, b1, W2, b2) - loss(Wm, b1, W2, b2)) / (2 * h)\n"
                            "assert np.allclose(dW1, num, atol=1e-4), (dW1.ravel()[:3], num.ravel()[:3])"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Entrenar el MLP para resolver XOR",
                description=(
                    "Bucle de entrenamiento de 2 capas que aprende XOR " "al 100%."
                ),
                instructions=(
                    "Implementa `entrenar_mlp(X, y, W1, b1, W2, b2, "
                    "lr=0.5, epocas=2000)` que en cada epoca hace el "
                    "forward (relu + sigmoid), guarda la perdida BCE, "
                    "computa los gradientes encadenados (como en "
                    "`backward_mlp`) y actualiza los **cuatro** grupos de "
                    "pesos con descenso de gradiente. Recibe los pesos "
                    "iniciales por argumento (no los inicialices tu). "
                    "Devuelve `(W1, b1, W2, b2, historial)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def entrenar_mlp(X, y, W1, b1, W2, b2, lr=0.5, epocas=2000):\n"
                    "    X = np.asarray(X, float)\n"
                    "    y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    W1 = np.array(W1, float); b1 = np.array(b1, float)\n"
                    "    W2 = np.array(W2, float); b2 = np.array(b2, float)\n"
                    "    N = X.shape[0]\n"
                    "    historial = []\n"
                    "    # TODO: bucle de epocas: forward, guardar BCE, backward encadenado, actualizar\n"
                    "    return W1, b1, W2, b2, historial\n"
                ),
                hints=[
                    "Es el bucle de DL 4 pero actualizando 4 grupos de pesos.",
                    "El backward es el de backward_mlp (dz2 -> dh -> dz1).",
                    "Con 8 neuronas ocultas y varios miles de epocas, XOR llega al 100%.",
                ],
                difficulty="advanced",
                points=30,
                hidden_tests=[
                    {
                        "name": "entrenar_mlp resuelve XOR al 100%",
                        "code": (
                            "import numpy as np\n"
                            "X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])\n"
                            "y = np.array([[0.0], [1.0], [1.0], [0.0]])\n"
                            "rng = np.random.default_rng(3)\n"
                            "W1 = rng.normal(size=(2, 8)); b1 = np.zeros(8)\n"
                            "W2 = rng.normal(size=(8, 1)); b2 = np.zeros(1)\n"
                            "W1, b1, W2, b2, hist = entrenar_mlp(X, y, W1, b1, W2, b2, lr=0.5, epocas=4000)\n"
                            "assert hist[-1] < hist[0], (hist[0], hist[-1])\n"
                            "z1 = X @ np.asarray(W1) + np.asarray(b1)\n"
                            "h = np.maximum(0.0, z1)\n"
                            "p = 1.0 / (1.0 + np.exp(-(h @ np.asarray(W2) + np.asarray(b2))))\n"
                            "acc = float(np.mean((p > 0.5).astype(float) == y))\n"
                            "assert acc == 1.0, (acc, p.ravel())"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="AI 1 · Embeddings y busqueda semantica desde cero",
        description=(
            "El primer ladrillo de AI Engineering: representar texto como "
            "vectores, medir similitud con coseno y recuperar los mas "
            "parecidos. La 'R' (retrieval) de RAG, en numpy puro."
        ),
        content=(
            "# AI 1: embeddings y busqueda semantica\n\n"
            "Bienvenido al **Track 5 (AI Engineering)**. Aqui dejamos de "
            "entrenar modelos y empezamos a **construir sistemas** sobre "
            "modelos que ya existen (LLMs, embeddings). El primer bloque "
            "es el motor de **RAG** (Retrieval-Augmented Generation): "
            "antes de que un LLM responda, hay que **recuperar** el "
            "contexto relevante. Eso es **busqueda semantica**, y su "
            "mecanica se construye con numpy.\n\n"
            "## De texto a vectores: embeddings\n\n"
            "Un **embedding** es un vector de numeros que representa el "
            "*significado* de un texto. Textos parecidos -> vectores "
            "cercanos. En la practica los produce un modelo de embeddings "
            "(OpenAI, sentence-transformers, etc.); aqui nos centramos en "
            "lo que haces **con** esos vectores, que es lo que define un "
            "sistema RAG.\n\n"
            "```\n"
            '"gato"   -> [0.9, 0.1, ...]\n'
            '"felino" -> [0.88, 0.12, ...]   (cerca de gato)\n'
            '"avion"  -> [0.1, 0.95, ...]    (lejos de gato)\n'
            "```\n\n"
            "## Similitud coseno\n\n"
            "Para medir 'que tan parecidos' son dos vectores se usa la "
            "**similitud coseno**: el coseno del angulo entre ellos. "
            "Ignora la magnitud y se fija solo en la **direccion**, que "
            "es lo que codifica el significado.\n\n"
            "```\n"
            "cos(a, b) = (a . b) / (||a|| * ||b||)\n"
            "  1   -> misma direccion (maxima similitud)\n"
            "  0   -> perpendiculares (sin relacion)\n"
            " -1   -> opuestos\n"
            "```\n\n"
            "```python\n"
            "import numpy as np\n"
            "def cosine_sim(a, b):\n"
            "    a = np.asarray(a, float); b = np.asarray(b, float)\n"
            "    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))\n"
            "```\n\n"
            "Fijate que **la escala no importa**: `[1,2,3]` y `[2,4,6]` "
            "apuntan a lo mismo, similitud 1. Por eso el coseno es el "
            "estandar para comparar embeddings (mejor que la distancia "
            "euclidea, sensible a la magnitud).\n\n"
            "## Recuperar los top-k\n\n"
            "Con una **query** y una coleccion de documentos "
            "vectorizados, calculas la similitud de la query con cada "
            "doc y te quedas con los `k` mas altos. Ese es el corazon de "
            "un buscador semantico (y de un retriever de RAG):\n\n"
            "```python\n"
            "def top_k(query, docs, k):\n"
            "    query = np.asarray(query, float); docs = np.asarray(docs, float)\n"
            "    sims = docs @ query / (np.linalg.norm(docs, axis=1) * np.linalg.norm(query))\n"
            "    return list(np.argsort(sims)[::-1][:k])\n"
            "```\n\n"
            "`np.argsort` ordena ascendente; con `[::-1]` lo inviertes a "
            "descendente y tomas los primeros `k`. Devolver los "
            "**indices** te deja mapear de vuelta a los textos "
            "originales.\n\n"
            "## Esto ya es un mini vector store\n\n"
            "Una matriz de embeddings (una fila por documento) + esta "
            "busqueda top-k es, conceptualmente, lo que hacen Pinecone, "
            "FAISS o pgvector — solo que ellos lo hacen sobre millones de "
            "vectores con indices aproximados (ANN) para ir rapido. La "
            "**mecanica** es la que acabas de escribir.\n\n"
            "## Como encaja en RAG\n\n"
            "```\n"
            "1. Indexar:  documentos -> embeddings -> matriz\n"
            "2. Query:    pregunta   -> embedding\n"
            "3. Retrieve: top_k(query, matriz) -> fragmentos relevantes\n"
            "4. Generate: LLM(pregunta + fragmentos) -> respuesta fundamentada\n"
            "```\n\n"
            "Esta leccion cubre los pasos 1-3 (la parte determinista y "
            "testeable). El paso 4 (llamar al LLM) llega en las "
            "siguientes lecciones del track.\n\n"
            "## Errores comunes\n\n"
            "1. **Usar distancia euclidea en vez de coseno** — sensible a "
            "la longitud del vector; el coseno compara direccion, que es "
            "lo que importa en embeddings.\n"
            "2. **No normalizar** — si implementas el producto punto sin "
            "dividir por las normas, un vector 'largo' gana siempre "
            "aunque no sea el mas parecido.\n"
            "3. **Ordenar ascendente y olvidar invertir** — `argsort` da "
            "menor-a-mayor; los mas similares estan al final.\n"
            "4. **Confundir el indice con el texto** — `top_k` devuelve "
            "posiciones; hay que mapearlas a los documentos.\n\n"
            "## Resumen\n\n"
            "- Un **embedding** convierte texto en un vector de "
            "significado.\n"
            "- La **similitud coseno** `(a.b)/(||a|| ||b||)` mide "
            "cercania por direccion, ignorando la escala.\n"
            "- **Busqueda semantica** = similitud de la query con cada "
            "doc + tomar los top-k.\n"
            "- Esto es el **retriever** de RAG; la generacion con LLM "
            "viene despues.\n"
        ),
        difficulty="intermediate",
        category="ai-fundamentos",
        order=38,
        track="track-5",
        estimated_duration=50,
        prerequisites_titles=[],
        exercises=[
            ExerciseTemplate(
                title="Similitud coseno",
                description=(
                    "Mide que tan parecidos son dos vectores por su " "direccion."
                ),
                instructions=(
                    "Implementa `cosine_sim(a, b)` = "
                    "`(a . b) / (||a|| * ||b||)` usando numpy "
                    "(`a @ b` para el producto punto y `np.linalg.norm` "
                    "para la magnitud). Devuelve un `float`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def cosine_sim(a, b):\n"
                    "    # TODO: a = np.asarray(a, float); b = np.asarray(b, float)\n"
                    "    # TODO: return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))\n"
                    "    ...\n"
                ),
                hints=[
                    "np.linalg.norm(v) da la magnitud (longitud) del vector.",
                    "Vectores paralelos dan 1; perpendiculares, 0.",
                    "La escala no importa: [1,2] y [2,4] dan similitud 1.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "cosine_sim: paralelos=1, ortogonales=0, opuestos=-1",
                        "code": (
                            "import numpy as np\n"
                            "assert abs(cosine_sim([1, 0], [1, 0]) - 1.0) < 1e-12\n"
                            "assert abs(cosine_sim([1, 0], [0, 1]) - 0.0) < 1e-12\n"
                            "assert abs(cosine_sim([1, 0], [-1, 0]) - (-1.0)) < 1e-12\n"
                            "assert abs(cosine_sim([1, 2, 3], [2, 4, 6]) - 1.0) < 1e-9\n"
                            "assert abs(cosine_sim([1, 1], [1, 0]) - 0.70710678) < 1e-6\n"
                            "assert isinstance(cosine_sim([1, 0], [1, 1]), float)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Recuperar los top-k",
                description=(
                    "Devuelve los indices de los documentos mas similares "
                    "a una query."
                ),
                instructions=(
                    "Implementa `top_k(query, docs, k)` donde `query` es "
                    "un vector `(d,)` y `docs` una matriz `(n_docs, d)`. "
                    "Calcula la similitud coseno de la query con cada "
                    "fila de `docs` y devuelve la lista de los `k` indices "
                    "mas similares, ordenados de mayor a menor. Pista: "
                    "`np.argsort(sims)[::-1][:k]`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def top_k(query, docs, k):\n"
                    "    query = np.asarray(query, float)\n"
                    "    docs = np.asarray(docs, float)\n"
                    "    # TODO: sims = docs @ query / (np.linalg.norm(docs, axis=1) * np.linalg.norm(query))\n"
                    "    # TODO: return list(np.argsort(sims)[::-1][:k])\n"
                    "    ...\n"
                ),
                hints=[
                    "np.linalg.norm(docs, axis=1) da la norma de cada fila.",
                    "argsort ordena ascendente; [::-1] lo invierte a descendente.",
                    "El resultado son indices (posiciones), no los vectores.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "top_k: indices mas similares, orden desc, invariante a escala",
                        "code": (
                            "import numpy as np\n"
                            "q = [1.0, 0.0]\n"
                            "docs = [[1.0, 0.0], [0.0, 1.0], [0.9, 0.1], [-1.0, 0.0]]\n"
                            "assert list(top_k(q, docs, 2)) == [0, 2], top_k(q, docs, 2)\n"
                            "assert list(top_k(q, docs, 1)) == [0]\n"
                            "docs2 = [[10.0, 0.0], [0.0, 5.0], [0.9, 0.1]]\n"
                            "assert list(top_k(q, docs2, 1)) == [0]"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Busqueda semantica end-to-end",
                description=(
                    "Recupera los textos mas relevantes para una query "
                    "(el retriever de RAG)."
                ),
                instructions=(
                    "Implementa `busqueda_semantica(query, docs, textos, "
                    "k)` que recibe el vector `query`, la matriz `docs` "
                    "de embeddings, la lista `textos` (un string por "
                    "documento, alineado con `docs`), y devuelve la lista "
                    "de los `k` textos mas similares a la query, de mayor "
                    "a menor similitud."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def busqueda_semantica(query, docs, textos, k):\n"
                    "    query = np.asarray(query, float)\n"
                    "    docs = np.asarray(docs, float)\n"
                    "    # TODO: sims = docs @ query / (np.linalg.norm(docs, axis=1) * np.linalg.norm(query))\n"
                    "    # TODO: idx = np.argsort(sims)[::-1][:k]\n"
                    "    # TODO: return [textos[i] for i in idx]\n"
                    "    ...\n"
                ),
                hints=[
                    "Reutiliza la logica de top_k y mapea los indices a textos.",
                    "textos[i] recupera el documento en la posicion i.",
                    "Este es exactamente el retriever de un pipeline RAG.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "busqueda_semantica: devuelve los textos top-k",
                        "code": (
                            "import numpy as np\n"
                            "q = [1.0, 0.0]\n"
                            "docs = [[1.0, 0.0], [0.0, 1.0], [0.9, 0.1], [-1.0, 0.0]]\n"
                            "textos = ['gato', 'avion', 'felino', 'antonimo']\n"
                            "assert busqueda_semantica(q, docs, textos, 2) == ['gato', 'felino']\n"
                            "assert busqueda_semantica(q, docs, textos, 1) == ['gato']"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="AI 2 · Chunking e indexacion de documentos",
        description=(
            "Como preparar un corpus para RAG: partir documentos en "
            "fragmentos (chunks), construir el indice de embeddings y "
            "recuperar el contexto relevante de una pregunta."
        ),
        content=(
            "# AI 2: chunking e indexacion\n\n"
            "En AI 1 recuperaste vectores ya dados. Pero antes de "
            "buscar, hay que **preparar el corpus**: partir los "
            "documentos largos en fragmentos manejables y construir un "
            "**indice** de embeddings. Este es el paso de *indexado* de "
            "RAG, y decisiones aparentemente pequenas aqui determinan si "
            "el sistema recupera bien o mal.\n\n"
            "## Por que partir en chunks\n\n"
            "No puedes (ni quieres) embeder un documento de 50 paginas "
            "como un solo vector: perderias todo el detalle, y no cabe "
            "en la ventana de contexto del LLM. En su lugar lo partes en "
            "**chunks** (fragmentos de unas pocas frases/parrafos), "
            "embedes cada uno, y recuperas solo los chunks relevantes a "
            "la pregunta.\n\n"
            "```\n"
            "documento largo --chunking--> [chunk1, chunk2, ... chunkN]\n"
            "cada chunk --embed--> un vector --> matriz indice (N, dim)\n"
            "```\n\n"
            "## Chunking con solapamiento\n\n"
            "Partir en seco puede cortar una idea justo a la mitad. Por "
            "eso los chunks suelen **solaparse**: cada uno comparte unas "
            "palabras con el anterior, para no perder contexto en los "
            "bordes.\n\n"
            "```python\n"
            "def chunk_texto(texto, tam, solapamiento=0):\n"
            "    palabras = texto.split()\n"
            "    step = tam - solapamiento          # cuanto avanzas cada vez\n"
            "    chunks = []\n"
            "    for i in range(0, len(palabras), step):\n"
            "        chunks.append(' '.join(palabras[i:i + tam]))\n"
            "        if i + tam >= len(palabras):\n"
            "            break                       # ya cubriste el final\n"
            "    return chunks\n"
            "```\n\n"
            "Con `tam=3, solapamiento=1` sobre `a b c d e f g`:\n\n"
            "```\n"
            '  "a b c"  ->  "c d e"  ->  "e f g"\n'
            "   step = 2 (avanzas 2, mantienes 1 de solape)\n"
            "```\n\n"
            "El `tam` y el `solapamiento` son **hiperparametros de "
            "RAG**: chunks muy grandes diluyen la senal; muy chicos "
            "pierden contexto. Solape tipico: 10-20% del tamano.\n\n"
            "## Construir el indice\n\n"
            "El **indice** es simplemente la matriz con el embedding de "
            "cada chunk. En produccion `embed_fn` es una llamada a un "
            "modelo de embeddings; aqui lo recibes como funcion para que "
            "todo sea testeable:\n\n"
            "```python\n"
            "def construir_indice(chunks, embed_fn):\n"
            "    return np.array([embed_fn(c) for c in chunks], float)\n"
            "```\n\n"
            "## Recuperar el contexto\n\n"
            "Juntando todo: embedes la pregunta, la comparas contra el "
            "indice (coseno de AI 1) y devuelves los `k` chunks mas "
            "relevantes. Eso es el **contexto** que despues le pasaras al "
            "LLM.\n\n"
            "```python\n"
            "def recuperar_contexto(pregunta, chunks, embed_fn, k):\n"
            "    indice = np.array([embed_fn(c) for c in chunks], float)\n"
            "    q = np.asarray(embed_fn(pregunta), float)\n"
            "    sims = indice @ q / (np.linalg.norm(indice, axis=1) * np.linalg.norm(q) + 1e-12)\n"
            "    idx = np.argsort(sims)[::-1][:k]\n"
            "    return [chunks[i] for i in idx]\n"
            "```\n\n"
            "El `+ 1e-12` evita dividir por cero si algun chunk quedara "
            "con embedding nulo. Ya tienes el **retriever completo**: "
            "chunk -> index -> retrieve. Solo falta la generacion.\n\n"
            "## Como encaja en RAG\n\n"
            "```\n"
            "1. Indexar:  documento --chunk--> chunks --embed--> indice   <- AI 2\n"
            "2. Retrieve: pregunta --embed--> top-k chunks del indice     <- AI 1 + AI 2\n"
            "3. Generate: LLM(pregunta + chunks recuperados) -> respuesta <- AI 3+\n"
            "```\n\n"
            "## Errores comunes\n\n"
            "1. **Chunks demasiado grandes** — recuperas texto irrelevante "
            "junto al relevante y confundes al LLM.\n"
            "2. **Sin solapamiento** — cortas ideas a la mitad y el chunk "
            "pierde sentido.\n"
            "3. **Solapamiento >= tam** — el `step` seria <= 0 y el bucle "
            "no avanza; valida que `solapamiento < tam`.\n"
            "4. **Reconstruir el indice en cada query** — en produccion "
            "el indice se calcula una vez y se guarda; solo la pregunta "
            "se embede en tiempo real.\n\n"
            "## Resumen\n\n"
            "- **Chunking** parte documentos en fragmentos; el "
            "solapamiento evita cortar ideas.\n"
            "- El **indice** es la matriz de embeddings de los chunks.\n"
            "- **Recuperar contexto** = embeder la pregunta + top-k del "
            "indice.\n"
            "- Con AI 1 + AI 2 tienes el retriever completo de RAG; la "
            "generacion con LLM llega en AI 3.\n"
        ),
        difficulty="intermediate",
        category="ai-fundamentos",
        order=39,
        track="track-5",
        estimated_duration=50,
        prerequisites_titles=[
            "AI 1 · Embeddings y busqueda semantica desde cero",
        ],
        exercises=[
            ExerciseTemplate(
                title="Partir texto en chunks",
                description=(
                    "Divide un texto en fragmentos de N palabras con "
                    "solapamiento opcional."
                ),
                instructions=(
                    "Implementa `chunk_texto(texto, tam, solapamiento=0)` "
                    "que parte `texto` (por palabras, con `.split()`) en "
                    "chunks de `tam` palabras, avanzando "
                    "`step = tam - solapamiento` palabras cada vez. Cada "
                    "chunk se devuelve como string (`' '.join(...)`). "
                    "Para en cuanto un chunk llega al final. Lanza "
                    "`ValueError` si `solapamiento >= tam` (step <= 0)."
                ),
                starter_code=(
                    "def chunk_texto(texto, tam, solapamiento=0):\n"
                    "    palabras = texto.split()\n"
                    "    step = tam - solapamiento\n"
                    "    # TODO: if step <= 0: raise ValueError(...)\n"
                    "    # TODO: recorre range(0, len(palabras), step),\n"
                    "    #   agrega ' '.join(palabras[i:i+tam]) y corta al llegar al final\n"
                    "    ...\n"
                ),
                hints=[
                    "step = tam - solapamiento es cuanto avanzas cada iteracion.",
                    "Corta el bucle cuando i + tam >= len(palabras).",
                    "Un solapamiento >= tam dejaria step <= 0: lanza ValueError.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "chunk_texto: tamano, solapamiento y validacion",
                        "code": (
                            "assert chunk_texto('a b c d e f', 2) == ['a b', 'c d', 'e f']\n"
                            "assert chunk_texto('a b c d e f g', 3, 1) == ['a b c', 'c d e', 'e f g']\n"
                            "assert chunk_texto('hola', 3) == ['hola']\n"
                            "assert chunk_texto('a b c d e', 2) == ['a b', 'c d', 'e']\n"
                            "try:\n"
                            "    chunk_texto('a b c', 2, 2)\n"
                            "    raise AssertionError('debio lanzar ValueError')\n"
                            "except ValueError:\n"
                            "    pass"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Construir el indice de embeddings",
                description=("Embede cada chunk para formar la matriz del indice."),
                instructions=(
                    "Implementa `construir_indice(chunks, embed_fn)` que "
                    "aplica `embed_fn` a cada chunk y devuelve un "
                    "`np.ndarray` de shape `(n_chunks, dim)` "
                    "(`np.array([embed_fn(c) for c in chunks], float)`)."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def construir_indice(chunks, embed_fn):\n"
                    "    # TODO: return np.array([embed_fn(c) for c in chunks], float)\n"
                    "    ...\n"
                ),
                hints=[
                    "Una fila por chunk, una columna por dimension del embedding.",
                    "embed_fn se aplica a cada chunk.",
                    "En produccion embed_fn seria una llamada al modelo de embeddings.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "construir_indice: matriz (n_chunks, dim)",
                        "code": (
                            "import numpy as np\n"
                            "embed = lambda t: [t.count('gato'), t.count('avion')]\n"
                            "chunks = ['el gato duerme', 'un avion vuela', 'gato gato']\n"
                            "M = np.asarray(construir_indice(chunks, embed))\n"
                            "assert M.shape == (3, 2), M.shape\n"
                            "assert np.allclose(M[0], [1, 0])\n"
                            "assert np.allclose(M[2], [2, 0])"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Recuperar el contexto de una pregunta",
                description=(
                    "El retriever completo: indexa, embede la pregunta y "
                    "devuelve los chunks relevantes."
                ),
                instructions=(
                    "Implementa `recuperar_contexto(pregunta, chunks, "
                    "embed_fn, k)` que construye el indice de los chunks, "
                    "embede la `pregunta`, calcula la similitud coseno "
                    "(usa `+ 1e-12` en el denominador para evitar "
                    "division por cero) y devuelve la lista de los `k` "
                    "chunks (strings) mas relevantes, de mayor a menor."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def recuperar_contexto(pregunta, chunks, embed_fn, k):\n"
                    "    indice = np.array([embed_fn(c) for c in chunks], float)\n"
                    "    q = np.asarray(embed_fn(pregunta), float)\n"
                    "    # TODO: sims = indice @ q / (np.linalg.norm(indice, axis=1) * np.linalg.norm(q) + 1e-12)\n"
                    "    # TODO: idx = np.argsort(sims)[::-1][:k]\n"
                    "    # TODO: return [chunks[i] for i in idx]\n"
                    "    ...\n"
                ),
                hints=[
                    "Es AI 1 (top-k) pero embediendo la pregunta y devolviendo chunks.",
                    "El +1e-12 evita NaN si algun chunk tiene embedding nulo.",
                    "Devuelve los textos de los chunks, no sus indices.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "recuperar_contexto: trae los chunks relevantes",
                        "code": (
                            "embed = lambda t: [t.count('gato'), t.count('avion'), t.count('python')]\n"
                            "chunks = ['el gato maulla', 'el avion despega', 'python es un lenguaje', 'gato y python']\n"
                            "res = recuperar_contexto('cuentame del gato', chunks, embed, 2)\n"
                            "assert 'el gato maulla' in res, res\n"
                            "assert 'el avion despega' not in res, res\n"
                            "assert len(res) == 2"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="AI 3 · Llamar a un LLM y armar un prompt RAG",
        description=(
            "La generacion de RAG: llamar a un LLM real desde el editor, "
            "construir un prompt con contexto recuperado, presupuestar la "
            "ventana y parsear salida estructurada (JSON)."
        ),
        content=(
            "# AI 3: llamar a un LLM y armar el prompt de RAG\n\n"
            "En AI 1 y AI 2 construiste el **retriever**. Ahora llega la "
            "**G** de RAG: **generar** la respuesta con un LLM, "
            "pasandole el contexto recuperado. Aqui aprendes a llamar al "
            "modelo y, sobre todo, a **construir bien el prompt** — que "
            "es donde se gana o se pierde la calidad de un sistema de "
            "AI Engineering.\n\n"
            "## Llamar al LLM desde el editor\n\n"
            "PyCode expone un helper que llama a un LLM real **a traves "
            "del backend** (sin exponer API keys). Es asincrono:\n\n"
            "```python\n"
            "import pycode\n"
            "respuesta = await pycode.llm_complete(\n"
            "    'Explica que es un embedding en una frase.',\n"
            "    system='Eres un profesor conciso.',\n"
            "    max_tokens=100,\n"
            ")\n"
            "print(respuesta)\n"
            "```\n\n"
            "El backend aplica **rate limit** y un **tope de tokens** "
            "para controlar el costo. En este entorno, si no hay modelo "
            "configurado, recibiras una respuesta placeholder — la "
            "**logica** que rodea la llamada es lo que importa y lo que "
            "vas a practicar.\n\n"
            "> Nota: la respuesta de un LLM es **no determinista** "
            "(cambia entre llamadas). Por eso los ejercicios evaluados "
            "no comprueban el texto del modelo, sino el codigo que "
            "**prepara** la llamada y **procesa** su salida — que es "
            "justo el trabajo de un AI Engineer.\n\n"
            "## Construir el prompt de RAG\n\n"
            "El truco de RAG esta en el prompt: le das al modelo el "
            "contexto recuperado y le pides que responda **solo** con "
            "eso (para reducir alucinaciones).\n\n"
            "```python\n"
            "def construir_prompt_rag(pregunta, contextos):\n"
            "    bloque = '\\n'.join('- ' + c for c in contextos)\n"
            "    return (\n"
            "        'Usa unicamente el siguiente contexto para responder. '\n"
            "        'Si la respuesta no esta en el contexto, di que no lo sabes.\\n\\n'\n"
            "        'Contexto:\\n' + bloque + '\\n\\nPregunta: ' + pregunta\n"
            "    )\n"
            "```\n\n"
            "El pipeline RAG completo queda:\n\n"
            "```python\n"
            "contextos = recuperar_contexto(pregunta, chunks, embed, k=3)  # AI 2\n"
            "prompt = construir_prompt_rag(pregunta, contextos)            # AI 3\n"
            "respuesta = await pycode.llm_complete(prompt)                 # generacion\n"
            "```\n\n"
            "## Presupuestar la ventana de contexto\n\n"
            "Un LLM tiene una **ventana de contexto** finita (y cada "
            "token cuesta). No puedes meter 500 chunks. Hay que "
            "**presupuestar**: incluir chunks (en orden de relevancia) "
            "hasta agotar un limite.\n\n"
            "```python\n"
            "def truncar_contexto(contextos, max_chars):\n"
            "    incluidos, total = [], 0\n"
            "    for c in contextos:\n"
            "        if total + len(c) > max_chars:\n"
            "            break\n"
            "        incluidos.append(c)\n"
            "        total += len(c)\n"
            "    return incluidos\n"
            "```\n\n"
            "(En produccion se cuenta en **tokens**, no caracteres, con "
            "un tokenizador; la idea es la misma.)\n\n"
            "## Parsear salida estructurada\n\n"
            "Muchas veces le pides al LLM que responda en **JSON** (para "
            "usar la salida en codigo). Pero los modelos a menudo la "
            "envuelven en cercas markdown ```` ```json ... ``` ```` o "
            "agregan texto. Hay que limpiarla antes de `json.loads`:\n\n"
            "```python\n"
            "import json\n"
            "def parsear_json_llm(texto):\n"
            "    t = texto.strip()\n"
            "    if '```' in t:\n"
            "        t = t.split('```')[1]\n"
            "        if t.startswith('json'):\n"
            "            t = t[4:]\n"
            "        t = t.strip()\n"
            "    try:\n"
            "        return json.loads(t)\n"
            "    except json.JSONDecodeError:\n"
            "        ini, fin = t.find('{'), t.rfind('}')\n"
            "        return json.loads(t[ini:fin + 1])\n"
            "```\n\n"
            "## Errores comunes\n\n"
            "1. **No acotar el contexto** — metes texto de mas, gastas "
            "tokens y confundes al modelo.\n"
            "2. **Confiar en que el JSON viene limpio** — casi nunca; "
            "limpia cercas y texto antes de parsear.\n"
            "3. **No instruir contra la alucinacion** — sin el 'usa solo "
            "el contexto', el modelo inventa.\n"
            "4. **Testear el texto exacto del LLM** — es no "
            "determinista; testea la logica que lo rodea.\n\n"
            "## Resumen\n\n"
            "- `pycode.llm_complete(prompt)` llama a un LLM real via el "
            "backend (await, rate-limited).\n"
            "- RAG = recuperar contexto (AI 1-2) + **construir el "
            "prompt** con ese contexto + generar.\n"
            "- **Presupuesta** el contexto para no exceder la ventana.\n"
            "- **Limpia y parsea** la salida estructurada (JSON con "
            "cercas).\n"
            "- Un AI Engineer disena el codigo **alrededor** del LLM; el "
            "modelo es una pieza mas.\n"
        ),
        difficulty="intermediate",
        category="ai-fundamentos",
        order=40,
        track="track-5",
        estimated_duration=55,
        prerequisites_titles=[
            "AI 2 · Chunking e indexacion de documentos",
        ],
        exercises=[
            ExerciseTemplate(
                title="Construir el prompt de RAG",
                description=(
                    "Ensambla el contexto recuperado y la pregunta en un "
                    "prompt anti-alucinacion."
                ),
                instructions=(
                    "Implementa `construir_prompt_rag(pregunta, "
                    "contextos)` que devuelve un prompt que: (1) instruye "
                    "a usar SOLO el contexto y decir 'no lo sabes' si no "
                    "esta; (2) lista cada contexto como vineta "
                    "(`'- ' + c`); (3) termina con `'Pregunta: ' + "
                    "pregunta`."
                ),
                starter_code=(
                    "def construir_prompt_rag(pregunta, contextos):\n"
                    "    # TODO: bloque = '\\n'.join('- ' + c for c in contextos)\n"
                    "    # TODO: return instruccion + 'Contexto:\\n' + bloque + '\\n\\nPregunta: ' + pregunta\n"
                    "    ...\n"
                ),
                hints=[
                    "La instruccion 'usa solo el contexto' reduce alucinaciones.",
                    "Cada contexto va como vineta: '- ' + c.",
                    "El prompt debe contener la pregunta al final.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "prompt contiene instruccion, contextos y pregunta",
                        "code": (
                            "p = construir_prompt_rag('cual es la capital?', "
                            "['Paris es la capital de Francia', 'Francia esta en Europa'])\n"
                            "assert 'cual es la capital?' in p\n"
                            "assert 'Paris es la capital de Francia' in p\n"
                            "assert 'Francia esta en Europa' in p\n"
                            "assert 'no lo sabes' in p\n"
                            "assert '- Paris es la capital de Francia' in p"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Presupuestar el contexto",
                description=(
                    "Incluye chunks hasta agotar un presupuesto de " "caracteres."
                ),
                instructions=(
                    "Implementa `truncar_contexto(contextos, max_chars)` "
                    "que recorre los chunks en orden y los va incluyendo "
                    "mientras la suma de sus longitudes no supere "
                    "`max_chars`. En cuanto el siguiente chunk no quepa, "
                    "para. Devuelve la lista de chunks incluidos."
                ),
                starter_code=(
                    "def truncar_contexto(contextos, max_chars):\n"
                    "    incluidos = []\n"
                    "    total = 0\n"
                    "    # TODO: for c in contextos: si total+len(c) > max_chars: break;\n"
                    "    #   si no, incluir c y sumar len(c)\n"
                    "    return incluidos\n"
                ),
                hints=[
                    "Acumula la longitud total y corta cuando el siguiente no cabe.",
                    "Si el primer chunk ya excede el presupuesto, devuelves [].",
                    "En produccion se mide en tokens; aqui, en caracteres.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "incluye chunks hasta agotar el presupuesto",
                        "code": (
                            "assert truncar_contexto(['abc', 'defgh', 'ij'], 8) == ['abc', 'defgh']\n"
                            "assert truncar_contexto(['abc'], 2) == []\n"
                            "assert truncar_contexto([], 100) == []\n"
                            "assert truncar_contexto(['ab', 'cd', 'ef'], 100) == ['ab', 'cd', 'ef']"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Parsear la salida JSON del LLM",
                description=(
                    "Limpia cercas markdown y texto para extraer el JSON "
                    "de una respuesta."
                ),
                instructions=(
                    "Implementa `parsear_json_llm(texto)` que devuelve el "
                    "dict parseado. Debe manejar: JSON plano, JSON dentro "
                    "de cercas ```` ```json ... ``` ```` o ```` ``` ... "
                    "``` ````, y JSON con texto alrededor (extrae desde "
                    "el primer `{` hasta el ultimo `}`). Usa `json.loads`."
                ),
                starter_code=(
                    "import json\n"
                    "\n"
                    "\n"
                    "def parsear_json_llm(texto):\n"
                    "    t = texto.strip()\n"
                    "    # TODO: si hay '```', quedate con lo de dentro y quita el prefijo 'json'\n"
                    "    # TODO: intenta json.loads(t); si falla, extrae de '{' a '}' y parsea\n"
                    "    ...\n"
                ),
                hints=[
                    "t.split('```')[1] te da el bloque entre la primera pareja de cercas.",
                    "Si el bloque empieza con 'json', quitalo (t[4:]).",
                    "Como fallback, t[t.find('{'):t.rfind('}')+1] aisla el objeto.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "parsea JSON plano, con cercas y con texto alrededor",
                        "code": (
                            "assert parsear_json_llm('{\"nombre\": \"ana\", \"edad\": 30}') == {'nombre': 'ana', 'edad': 30}\n"
                            "assert parsear_json_llm('```json\\n{\"ok\": true}\\n```') == {'ok': True}\n"
                            "assert parsear_json_llm('Claro:\\n```\\n{\"n\": [1, 2, 3]}\\n```') == {'n': [1, 2, 3]}\n"
                            "assert parsear_json_llm('bla bla {\"a\": 1} fin') == {'a': 1}"
                        ),
                    },
                ],
            ),
        ],
    ),
]


async def seed_lessons_with_exercises(db: AsyncSession) -> int:
    """Create/update core lessons and their exercises."""
    lessons_by_title: dict[str, Lesson] = {}
    inserted = 0

    for template in LESSON_TEMPLATES:
        existing_result = await db.execute(
            select(Lesson).where(Lesson.title == template.title)
        )
        lesson = existing_result.scalar_one_or_none()

        if not lesson:
            lesson = Lesson(
                title=template.title,
                description=template.description,
                content=template.content,
                difficulty=template.difficulty,
                category=template.category,
                track=template.track,
                order=template.order,
                estimated_duration=template.estimated_duration,
                prerequisites=[],
                is_active=True,
            )
            db.add(lesson)
            await db.flush()
            inserted += 1
        else:
            lesson.description = template.description
            lesson.content = template.content
            lesson.difficulty = template.difficulty
            lesson.category = template.category
            lesson.track = template.track
            lesson.order = template.order
            lesson.estimated_duration = template.estimated_duration
            lesson.is_active = True

        lessons_by_title[template.title] = lesson

        await db.execute(delete(Exercise).where(Exercise.lesson_id == lesson.id))
        for index, ex in enumerate(template.exercises, start=1):
            db.add(
                Exercise(
                    lesson_id=lesson.id,
                    title=ex.title,
                    description=ex.description,
                    instructions=ex.instructions,
                    starter_code=ex.starter_code,
                    solution_code=None,
                    test_cases=[],
                    hidden_tests=list(ex.hidden_tests),
                    hints=ex.hints,
                    points=ex.points,
                    difficulty=ex.difficulty,
                    order=index,
                )
            )

    await db.flush()
    for template in LESSON_TEMPLATES:
        lesson = lessons_by_title[template.title]
        prerequisites = []
        for prereq_title in template.prerequisites_titles:
            prereq_lesson = lessons_by_title.get(prereq_title)
            if prereq_lesson:
                prerequisites.append(prereq_lesson.id)
        lesson.prerequisites = prerequisites

    await db.commit()
    return inserted
