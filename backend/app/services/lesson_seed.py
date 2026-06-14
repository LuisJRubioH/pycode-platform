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
            ),
            ExerciseTemplate(
                title="Mini presentación",
                description="Muestra dos lineas con informacion personal.",
                instructions="Imprime ciudad y lenguaje favorito en lineas separadas.",
                starter_code="ciudad = ''\nlenguaje = 'Python'\n# TODO\n",
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
                instructions="Recibe `texto_numero` y calcula su doble como int.",
                starter_code="texto_numero = '12'\n# TODO\n",
            ),
            ExerciseTemplate(
                title="Chequeo de tipos",
                description="Valida tipos de variables.",
                instructions="Imprime el tipo de `edad`, `altura` y `activo`.",
                starter_code="edad = 18\naltura = 1.72\nactivo = True\n# TODO\n",
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
                instructions="Con `edad`, imprime `menor`, `adulto` o `senior`.",
                starter_code="edad = 17\n# TODO\n",
            ),
            ExerciseTemplate(
                title="Acceso permitido",
                description="Combina condiciones.",
                instructions="Permite acceso si `tiene_pase` y `edad >= 18`.",
                starter_code="tiene_pase = True\nedad = 19\n# TODO\n",
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
                instructions="Calcula la suma de 1 a `n` usando for.",
                starter_code="n = 10\n# TODO\n",
            ),
            ExerciseTemplate(
                title="Contador while",
                description="Cuenta hacia atras.",
                instructions="Imprime de 5 a 1 usando while.",
                starter_code="# TODO\n",
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
                instructions="Calcula promedio de `notas` con dos decimales.",
                starter_code="notas = [4.5, 3.8, 5.0, 4.2]\n# TODO\n",
            ),
            ExerciseTemplate(
                title="Agenda minima",
                description="Uso de diccionario.",
                instructions="Agrega y consulta un contacto en `agenda`.",
                starter_code="agenda = {}\n# TODO\n",
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
                instructions="Crea lista con cuadrados de numeros pares de 1..20.",
                starter_code="# TODO\n",
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
                instructions="Crea clase Producto con nombre/precio y metodo aplicar_descuento.",
                starter_code="class Producto:\n    def __init__(self, nombre: str, precio: float):\n        self.nombre = nombre\n        self.precio = precio\n\n    # TODO\n",
                difficulty="medium",
                points=15,
            ),
            ExerciseTemplate(
                title="Cuenta bancaria",
                description="Mutacion de estado.",
                instructions="Implementa depositar y retirar con validaciones.",
                starter_code="class Cuenta:\n    def __init__(self):\n        self.saldo = 0\n\n    # TODO\n",
                difficulty="medium",
                points=15,
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
