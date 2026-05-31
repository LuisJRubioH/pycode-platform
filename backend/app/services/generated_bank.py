"""
Generate a large curated bank of coding challenges and output puzzles.

The problems are original/adapted prompts inspired by common open practice sources.
"""

# flake8: noqa: E501 -- archivo de contenido curado: prompts largos en espanol por reto.

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import CodingChallenge
from app.models.elo_models import Puzzle

CURATED_SOURCE = "pycode-curated-open"


@dataclass(frozen=True)
class ChallengeTemplate:
    slug_base: str
    title: str
    topic: str
    easy_prompt: str
    medium_prompt: str
    hard_prompt: str
    starter_code: str


CHALLENGE_TEMPLATES: list[ChallengeTemplate] = [
    ChallengeTemplate(
        slug_base="strings-anagrama",
        title="Anagramas Normalizados",
        topic="strings",
        easy_prompt="Escribe una funcion `son_anagramas(a, b)` que retorne True si dos strings son anagramas ignorando mayusculas.",
        medium_prompt="Extiende `son_anagramas(a, b)` para ignorar espacios y tildes comunes. Debe funcionar en tiempo lineal respecto al largo del texto.",
        hard_prompt="Implementa `son_anagramas(a, b)` soportando caracteres unicode y signos. Explica complejidad temporal y espacial.",
        starter_code="def son_anagramas(a: str, b: str) -> bool:\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="strings-palindromo",
        title="Palindromo Robusto",
        topic="strings",
        easy_prompt="Crea `es_palindromo(texto)` que ignore mayusculas y retorne si el texto se lee igual al reves.",
        medium_prompt="Mejora `es_palindromo(texto)` para ignorar signos y espacios usando dos punteros.",
        hard_prompt="Implementa `es_palindromo(texto)` con normalizacion unicode, sin crear una copia invertida completa.",
        starter_code="def es_palindromo(texto: str) -> bool:\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="arrays-two-sum",
        title="Two Sum",
        topic="arrays",
        easy_prompt="Implementa `two_sum(nums, target)` que retorne los indices de dos valores que suman target.",
        medium_prompt="Implementa `two_sum(nums, target)` en O(n) usando hash map. Si no existe pareja, retorna None.",
        hard_prompt="Implementa `two_sum_todos(nums, target)` retornando todas las parejas de indices unicas sin repetir.",
        starter_code="def two_sum(nums: list[int], target: int):\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="arrays-rotacion",
        title="Rotacion de Arreglo",
        topic="arrays",
        easy_prompt="Crea `rotar(nums, k)` que rote una lista a la derecha k posiciones.",
        medium_prompt="Implementa `rotar(nums, k)` in-place y en O(1) memoria extra.",
        hard_prompt="Implementa `rotar_segmento(nums, k, inicio, fin)` para rotar solo un subarreglo validando bordes.",
        starter_code="def rotar(nums: list[int], k: int) -> list[int]:\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="dicts-frecuencia",
        title="Frecuencia de Tokens",
        topic="dicts",
        easy_prompt="Crea `contar_tokens(texto)` que retorne un diccionario token->frecuencia separado por espacios.",
        medium_prompt="Normaliza minusculas y elimina puntuacion basica antes de contar tokens.",
        hard_prompt="Retorna top-k tokens por frecuencia y, en empate, orden alfabetico.",
        starter_code="def contar_tokens(texto: str) -> dict[str, int]:\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="sets-diferencia",
        title="Diferencias de Inventario",
        topic="sets",
        easy_prompt="Implementa `faltantes(requeridos, presentes)` para retornar elementos requeridos que faltan.",
        medium_prompt="Implementa `delta_inventario(a, b)` retornando agregados y removidos entre dos snapshots.",
        hard_prompt="Implementa comparacion entre inventarios con ids repetidos y retorna diferencias con conteos.",
        starter_code="def faltantes(requeridos: set[str], presentes: set[str]) -> set[str]:\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="sorting-custom",
        title="Ordenamiento Personalizado",
        topic="sorting",
        easy_prompt="Ordena una lista de tuplas `(nombre, edad)` por edad ascendente.",
        medium_prompt="Ordena empleados por salario descendente y nombre ascendente en empate.",
        hard_prompt="Implementa `ordenar_por_campos(registros, campos)` para criterios dinamicos con prioridad.",
        starter_code="def ordenar_registros(registros):\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="search-binary",
        title="Busqueda Binaria",
        topic="search",
        easy_prompt="Implementa `binary_search(nums, target)` en lista ordenada y retorna indice o -1.",
        medium_prompt="Retorna la primera ocurrencia de target cuando hay duplicados.",
        hard_prompt="Retorna rango [inicio, fin] de ocurrencias de target en O(log n).",
        starter_code="def binary_search(nums: list[int], target: int) -> int:\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="recursion-factorial",
        title="Factorial y Memoizacion",
        topic="recursion",
        easy_prompt="Implementa `factorial(n)` de forma recursiva con casos base correctos.",
        medium_prompt="Implementa version iterativa y recursiva, y compara para n grandes.",
        hard_prompt="Implementa memoizacion para factorial y calcula multiples consultas eficientemente.",
        starter_code="def factorial(n: int) -> int:\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="recursion-fibonacci",
        title="Fibonacci Eficiente",
        topic="recursion",
        easy_prompt="Implementa `fib(n)` iterativo para n>=0.",
        medium_prompt="Implementa `fib(n)` con memoizacion y valida entradas negativas.",
        hard_prompt="Implementa `fib_rapido(n)` con fast doubling para O(log n).",
        starter_code="def fib(n: int) -> int:\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="window-max-sum",
        title="Ventana Deslizante",
        topic="sliding-window",
        easy_prompt="Dado `nums` y `k`, retorna la suma maxima de una sublista contigua de largo k.",
        medium_prompt="Retorna tambien los indices [inicio, fin] de la mejor ventana.",
        hard_prompt="Extiende para ventanas variables segun un umbral y minimiza longitud.",
        starter_code="def max_suma_ventana(nums: list[int], k: int) -> int:\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="stack-parentesis",
        title="Parentesis Balanceados",
        topic="stacks",
        easy_prompt="Implementa `balanceado(texto)` para parentesis `()`.",
        medium_prompt="Soporta `()[]{} ` y retorna False si algun cierre no coincide.",
        hard_prompt="Retorna posicion exacta del primer error de balanceo.",
        starter_code="def balanceado(texto: str):\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="queue-scheduler",
        title="Simulador de Cola",
        topic="queues",
        easy_prompt="Simula una cola FIFO con operaciones enqueue/dequeue basicas.",
        medium_prompt="Agrega prioridad numerica y procesa primero menor valor.",
        hard_prompt="Simula round-robin con quantum y calcula tiempos de espera.",
        starter_code="def simular_cola(operaciones):\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="regex-validacion",
        title="Validacion con Regex",
        topic="regex",
        easy_prompt="Valida correos simples con una expresion regular basica.",
        medium_prompt="Extrae todos los hashtags validos de un texto.",
        hard_prompt="Valida patrones compuestos (id, fecha, codigo) con grupos nombrados.",
        starter_code="import re\n\ndef validar(valor: str) -> bool:\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="files-logs",
        title="Procesador de Logs",
        topic="files",
        easy_prompt="Lee un archivo y cuenta lineas por nivel INFO/WARN/ERROR.",
        medium_prompt="Calcula top endpoints por numero de errores en un log.",
        hard_prompt="Implementa parser tolerante a lineas corruptas y genera resumen JSON.",
        starter_code="def procesar_log(path: str):\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="datetime-reportes",
        title="Reportes por Fecha",
        topic="datetime",
        easy_prompt="Agrupa eventos por dia y cuenta ocurrencias.",
        medium_prompt="Calcula rachas consecutivas de actividad diaria.",
        hard_prompt="Soporta zonas horarias y cortes semanales ISO.",
        starter_code="from datetime import datetime\n\ndef agrupar_eventos(fechas: list[str]):\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="oop-bank-account",
        title="Cuenta Bancaria OOP",
        topic="oop",
        easy_prompt="Crea clase `Cuenta` con depositar y retirar.",
        medium_prompt="Agrega validaciones, historial y excepciones propias.",
        hard_prompt="Implementa transferencias atomicas entre cuentas y auditoria.",
        starter_code="class Cuenta:\n    def __init__(self, saldo: float = 0):\n        self.saldo = saldo\n",
    ),
    ChallengeTemplate(
        slug_base="testing-pytest",
        title="Refactor con Pruebas",
        topic="testing",
        easy_prompt="Escribe pruebas para una funcion que calcula descuento.",
        medium_prompt="Agrega casos borde y parametrizacion con pytest.",
        hard_prompt="Refactoriza una funcion larga guiado por tests y cobertura minima 90%.",
        starter_code="def calcular_descuento(total: float, porcentaje: float) -> float:\n    return total - (total * porcentaje / 100)\n",
    ),
    ChallengeTemplate(
        slug_base="pandas-aggregations",
        title="Agregaciones con Pandas",
        topic="pandas",
        easy_prompt="Con DataFrame de ventas, calcula total por producto.",
        medium_prompt="Calcula ticket promedio por ciudad y ordena descendente.",
        hard_prompt="Construye un reporte mensual con pivot, variacion y ranking.",
        starter_code="import pandas as pd\n\ndef reporte(df: pd.DataFrame):\n    # TODO\n    pass\n",
    ),
    ChallengeTemplate(
        slug_base="numpy-vectorization",
        title="Vectorizacion con NumPy",
        topic="numpy",
        easy_prompt="Calcula media y desviacion estandar de un array.",
        medium_prompt="Normaliza matriz por columna sin bucles explicitos.",
        hard_prompt="Implementa distancia coseno por filas usando operaciones vectorizadas.",
        starter_code="import numpy as np\n\ndef transformar(a: np.ndarray):\n    # TODO\n    pass\n",
    ),
]


def _difficulty_elo(difficulty: str, offset: int) -> int:
    base = {"easy": 850, "medium": 1200, "hard": 1550}[difficulty]
    return base + offset


async def seed_generated_challenges(db: AsyncSession) -> int:
    """Insert many curated generated challenges if missing."""
    max_order = await db.execute(select(func.max(CodingChallenge.order_index)))
    order_index = (max_order.scalar_one_or_none() or 0) + 1
    inserted = 0

    variants = [("easy", "facil"), ("medium", "medio"), ("hard", "dificil")]
    for template in CHALLENGE_TEMPLATES:
        for difficulty, difficulty_slug in variants:
            for variant_idx in range(1, 4):
                slug = f"{CURATED_SOURCE}-{template.slug_base}-{difficulty_slug}-{variant_idx}"
                existing = await db.execute(
                    select(CodingChallenge.id).where(CodingChallenge.slug == slug)
                )
                if existing.scalar_one_or_none() is not None:
                    continue

                if difficulty == "easy":
                    prompt = template.easy_prompt
                elif difficulty == "medium":
                    prompt = template.medium_prompt
                else:
                    prompt = template.hard_prompt

                prompt = (
                    f"{prompt}\n\n"
                    f"Variante {variant_idx}: usa ejemplos propios y documenta decisiones clave.\n"
                    "No publiques la solucion final en el enunciado."
                )
                title = f"{template.title} (v{variant_idx})"

                challenge = CodingChallenge(
                    title=title,
                    slug=slug,
                    source=CURATED_SOURCE,
                    source_path=f"generated/{template.topic}/{difficulty}/{slug}.md",
                    difficulty=difficulty,
                    topic=template.topic,
                    prompt=prompt,
                    starter_code=template.starter_code,
                    reference_solution=None,
                    order_index=order_index,
                )
                db.add(challenge)
                order_index += 1
                inserted += 1

    if inserted:
        await db.commit()

    return inserted


@dataclass(frozen=True)
class CuratedPuzzle:
    """Puzzle conceptual con un objetivo de aprendizaje claro.

    A diferencia del banco viejo (25 variantes triviales por categoría
    cambiando solo números), cada `CuratedPuzzle` enseña un concepto
    distinto: comprehensions, slicing, broadcasting, groupby, etc.
    """

    slug_suffix: str
    title: str
    topic: str
    code_snippet: str
    correct_output: str
    explanation: str
    hint: str
    elo_rating: int


# Banco curado conceptual. Cada lista cubre un set de conceptos distintos
# del lenguaje/librería; difficultad sube con el ELO.
CURATED_PYTHON_PUZZLES: list[CuratedPuzzle] = [
    CuratedPuzzle(
        slug_suffix="slicing-strings",
        title="Slicing inverso de string",
        topic="strings",
        code_snippet='s = "Python"\nprint(s[::-1])',
        correct_output="nohtyP",
        explanation="`s[::-1]` recorre la cadena con paso -1, devolviéndola invertida.",
        hint="Recuerda que el tercer valor del slice es el paso.",
        elo_rating=850,
    ),
    CuratedPuzzle(
        slug_suffix="list-comprehension",
        title="List comprehension con filtro",
        topic="comprehensions",
        code_snippet="nums = [1, 2, 3, 4, 5, 6]\npares = [n*n for n in nums if n % 2 == 0]\nprint(pares)",
        correct_output="[4, 16, 36]",
        explanation="La comprehension filtra pares y eleva al cuadrado: 2², 4², 6².",
        hint="¿Qué números pasan el filtro `n % 2 == 0`?",
        elo_rating=900,
    ),
    CuratedPuzzle(
        slug_suffix="dict-get-default",
        title="dict.get con valor por defecto",
        topic="dicts",
        code_snippet='d = {"a": 1, "b": 2}\nprint(d.get("c", 0))\nprint(d.get("a", 0))',
        correct_output="0\n1",
        explanation="`.get(k, default)` retorna `default` si la clave no existe; si existe devuelve su valor.",
        hint="`get` no lanza KeyError.",
        elo_rating=920,
    ),
    CuratedPuzzle(
        slug_suffix="enumerate-zip",
        title="enumerate sobre zip",
        topic="iteration",
        code_snippet='nombres = ["Ana", "Beto"]\nedades = [30, 25]\nfor i, (n, e) in enumerate(zip(nombres, edades)):\n    print(f"{i}:{n}-{e}")',
        correct_output="0:Ana-30\n1:Beto-25",
        explanation="`zip` empareja por posición; `enumerate` añade el índice.",
        hint="`enumerate` devuelve (índice, valor); aquí el valor es la tupla de zip.",
        elo_rating=970,
    ),
    CuratedPuzzle(
        slug_suffix="set-operations",
        title="Operaciones de conjuntos",
        topic="sets",
        code_snippet="a = {1, 2, 3}\nb = {2, 3, 4}\nprint(sorted(a & b))\nprint(sorted(a | b))",
        correct_output="[2, 3]\n[1, 2, 3, 4]",
        explanation="`&` es intersección; `|` es unión. `sorted` los devuelve como lista ordenada.",
        hint="Recuerda: intersección = común a ambos; unión = todos sin repetir.",
        elo_rating=1000,
    ),
    CuratedPuzzle(
        slug_suffix="dict-comprehension",
        title="Dict comprehension desde dos listas",
        topic="comprehensions",
        code_snippet='claves = ["a", "b", "c"]\nvalores = [10, 20, 30]\nd = {k: v*2 for k, v in zip(claves, valores)}\nprint(d)',
        correct_output="{'a': 20, 'b': 40, 'c': 60}",
        explanation="zip empareja claves/valores y la comprehension multiplica cada valor por 2.",
        hint="Igual que list comprehension pero produciendo pares clave:valor.",
        elo_rating=1050,
    ),
    CuratedPuzzle(
        slug_suffix="sorted-key-lambda",
        title="sorted con key=lambda",
        topic="sorting",
        code_snippet='palabras = ["sol", "ave", "casa", "ir"]\nordenadas = sorted(palabras, key=lambda s: len(s))\nprint(ordenadas)',
        correct_output="['ir', 'sol', 'ave', 'casa']",
        explanation="`key` define el criterio: ordena por largo de la palabra. Empates conservan orden de aparición (stable).",
        hint="¿Cuál es la palabra más corta? ¿Y la más larga?",
        elo_rating=1100,
    ),
    CuratedPuzzle(
        slug_suffix="generator-sum",
        title="Generator expression con sum",
        topic="generators",
        code_snippet="total = sum(x*x for x in range(1, 5))\nprint(total)",
        correct_output="30",
        explanation="Suma 1² + 2² + 3² + 4² = 1 + 4 + 9 + 16 = 30.",
        hint="`range(1, 5)` produce 1, 2, 3, 4 (sin incluir 5).",
        elo_rating=1150,
    ),
    CuratedPuzzle(
        slug_suffix="try-except-default",
        title="try/except con default",
        topic="errors",
        code_snippet='def parse_int(s):\n    try:\n        return int(s)\n    except ValueError:\n        return -1\n\nprint(parse_int("42"))\nprint(parse_int("abc"))',
        correct_output="42\n-1",
        explanation="`int('42')` funciona; `int('abc')` lanza ValueError y entra al except devolviendo -1.",
        hint="¿Qué pasa si el string no es convertible a int?",
        elo_rating=1200,
    ),
    CuratedPuzzle(
        slug_suffix="args-kwargs",
        title="*args y **kwargs",
        topic="functions",
        code_snippet='def f(*args, **kwargs):\n    print(sum(args), kwargs.get("k", 0))\n\nf(1, 2, 3, k=10)',
        correct_output="6 10",
        explanation="`args=(1,2,3)`, suma=6. `kwargs={'k':10}`, `.get('k', 0)` devuelve 10.",
        hint="`*args` recoge posicionales en tupla; `**kwargs` recoge nombrados en dict.",
        elo_rating=1250,
    ),
    CuratedPuzzle(
        slug_suffix="ternary-expression",
        title="Operador ternario",
        topic="conditionals",
        code_snippet='x = 7\nlabel = "par" if x % 2 == 0 else "impar"\nprint(label)',
        correct_output="impar",
        explanation='`a if cond else b` evalúa la condición y devuelve `a` o `b`. 7 % 2 = 1, no es 0, así que retorna `"impar"`.',
        hint="¿7 es par o impar?",
        elo_rating=800,
    ),
    CuratedPuzzle(
        slug_suffix="fstring-format",
        title="f-string con formato y alineación",
        topic="strings",
        code_snippet='name = "Ana"\npi = 3.14159\nprint(f"{name:>5} {pi:.2f}")',
        correct_output="  Ana 3.14",
        explanation="`{name:>5}` alinea a la derecha en ancho 5 (rellena con espacios). `{pi:.2f}` redondea a 2 decimales.",
        hint="`>` alinea a la derecha; `.2f` corta a 2 decimales.",
        elo_rating=980,
    ),
    CuratedPuzzle(
        slug_suffix="starred-unpacking",
        title="Unpacking con asterisco",
        topic="unpacking",
        code_snippet="first, *middle, last = [1, 2, 3, 4, 5]\nprint(first, middle, last)",
        correct_output="1 [2, 3, 4] 5",
        explanation="`*middle` captura todos los elementos centrales como lista; `first` y `last` toman los extremos.",
        hint='`*nombre` recoge "el resto" en una lista.',
        elo_rating=1100,
    ),
    CuratedPuzzle(
        slug_suffix="recursion-factorial",
        title="Recursión: factorial",
        topic="recursion",
        code_snippet="def fact(n):\n    return 1 if n <= 1 else n * fact(n-1)\n\nprint(fact(5))",
        correct_output="120",
        explanation="5! = 5·4·3·2·1 = 120. La función se llama con n-1 hasta llegar al caso base.",
        hint="¿Cuánto es 5 × 4 × 3 × 2 × 1?",
        elo_rating=1180,
    ),
    CuratedPuzzle(
        slug_suffix="defaultdict-list",
        title="defaultdict para agrupar",
        topic="collections",
        code_snippet='from collections import defaultdict\nd = defaultdict(list)\nfor k, v in [("a", 1), ("b", 2), ("a", 3)]:\n    d[k].append(v)\nprint(dict(d))',
        correct_output="{'a': [1, 3], 'b': [2]}",
        explanation="`defaultdict(list)` crea una lista vacía la primera vez que se accede a una clave, así `.append` funciona sin chequear.",
        hint="No hace falta `if k not in d: d[k] = []`.",
        elo_rating=1280,
    ),
    CuratedPuzzle(
        slug_suffix="chained-comparison",
        title="Comparaciones encadenadas",
        topic="conditionals",
        code_snippet="x = 50\nprint(0 < x <= 100, 100 < x)",
        correct_output="True False",
        explanation="`0 < x <= 100` equivale a `0 < x and x <= 100`. La segunda comparación `100 < x` es 100 < 50 → False.",
        hint="Python permite encadenar comparaciones sin repetir x.",
        elo_rating=900,
    ),
    CuratedPuzzle(
        slug_suffix="strip-split-join",
        title="strip + split + join",
        topic="strings",
        code_snippet='s = "  hola, mundo, python  "\nwords = s.strip().split(", ")\nprint("|".join(words))',
        correct_output="hola|mundo|python",
        explanation='`strip()` quita espacios al inicio/fin; `split(", ")` separa por coma+espacio; `"|".join(...)` une con `|`.',
        hint="Tres operaciones encadenadas: limpiar, partir, unir.",
        elo_rating=1020,
    ),
    CuratedPuzzle(
        slug_suffix="any-all-generators",
        title="any y all con generadores",
        topic="functional",
        code_snippet="nums = [2, 4, 6, 8]\nprint(all(n % 2 == 0 for n in nums), any(n > 5 for n in nums))",
        correct_output="True True",
        explanation="`all`: todos pares → True. `any`: existe alguno > 5 (6 y 8) → True.",
        hint="`all` exige todos; `any` exige al menos uno.",
        elo_rating=1130,
    ),
    CuratedPuzzle(
        slug_suffix="property-decorator",
        title="@property como atributo computado",
        topic="oop",
        code_snippet="class Box:\n    def __init__(self, side):\n        self._side = side\n\n    @property\n    def area(self):\n        return self._side ** 2\n\nb = Box(5)\nprint(b.area)",
        correct_output="25",
        explanation="`@property` convierte el método en un atributo de solo lectura: `b.area` (sin paréntesis) llama internamente al método.",
        hint="Sin @property habría que escribir `b.area()`.",
        elo_rating=1320,
    ),
    CuratedPuzzle(
        slug_suffix="context-manager-class",
        title="Context manager con __enter__/__exit__",
        topic="context-managers",
        code_snippet='class Counter:\n    def __enter__(self):\n        self.n = 0\n        return self\n\n    def __exit__(self, *args):\n        print("end", self.n)\n\nwith Counter() as c:\n    c.n += 5\n    c.n += 3',
        correct_output="end 8",
        explanation="`__enter__` corre al entrar al `with`; `__exit__` corre al salir, sin importar si hubo error. Aquí imprime el total acumulado.",
        hint="`__exit__` siempre se ejecuta al salir del bloque.",
        elo_rating=1450,
    ),
    CuratedPuzzle(
        slug_suffix="enumerate-with-start",
        title="enumerate con start=1",
        topic="iteration",
        code_snippet='for i, x in enumerate(["a", "b", "c"], start=1):\n    print(i, x)',
        correct_output="1 a\n2 b\n3 c",
        explanation='`enumerate(iter, start=k)` numera desde `k` en vez de 0. Útil para mostrar listas "1, 2, 3..." al usuario.',
        hint="El segundo parámetro de enumerate es el número inicial.",
        elo_rating=940,
    ),
    CuratedPuzzle(
        slug_suffix="max-key-len",
        title="max con key=len",
        topic="functional",
        code_snippet='words = ["ab", "xyz", "de"]\nprint(max(words, key=len))',
        correct_output="xyz",
        explanation="`max(iter, key=fn)` aplica `fn` a cada elemento y compara los resultados. `len` devuelve 2, 3, 2 → gana 'xyz' con 3.",
        hint="Sin key=len compara strings alfabéticamente.",
        elo_rating=1050,
    ),
    CuratedPuzzle(
        slug_suffix="divmod-builtin",
        title="divmod retorna (cociente, residuo)",
        topic="arithmetic",
        code_snippet="q, r = divmod(17, 5)\nprint(q, r)",
        correct_output="3 2",
        explanation="`divmod(a, b)` devuelve la tupla `(a // b, a % b)`. Combina las dos operaciones en una llamada.",
        hint="Equivale a (17//5, 17%5).",
        elo_rating=1090,
    ),
    CuratedPuzzle(
        slug_suffix="counter-most-common",
        title="Counter.most_common",
        topic="collections",
        code_snippet='from collections import Counter\nc = Counter("mississippi")\nprint(c.most_common(2))',
        correct_output="[('i', 4), ('s', 4)]",
        explanation="`Counter` cuenta letras: i=4, s=4, p=2, m=1. `most_common(2)` devuelve las 2 más frecuentes; en empate respeta orden de aparición.",
        hint='¿Qué letras se repiten más en "mississippi"?',
        elo_rating=1210,
    ),
    CuratedPuzzle(
        slug_suffix="nested-list-comprehension",
        title="Nested list comprehension (matriz)",
        topic="comprehensions",
        code_snippet="m = [[i * j for j in range(3)] for i in range(3)]\nprint(m)",
        correct_output="[[0, 0, 0], [0, 1, 2], [0, 2, 4]]",
        explanation="Genera una matriz 3x3 donde m[i][j] = i*j. La comprehension externa controla i (filas); la interna j (columnas).",
        hint="Fila i = [i*0, i*1, i*2].",
        elo_rating=1340,
    ),
    CuratedPuzzle(
        slug_suffix="dict-merge-operator",
        title="Unión de diccionarios con |",
        topic="dicts",
        code_snippet='a = {"x": 1, "y": 2}\nb = {"y": 9, "z": 3}\nprint(a | b)',
        correct_output="{'x': 1, 'y': 9, 'z': 3}",
        explanation="El operador `|` (Python 3.9+) fusiona dicts; ante claves repetidas gana el de la derecha, por eso `y` queda en 9.",
        hint="¿Qué valor de `y` prevalece, el de la izquierda o el de la derecha?",
        elo_rating=950,
    ),
    CuratedPuzzle(
        slug_suffix="slice-assignment",
        title="Asignación a un slice",
        topic="slicing",
        code_snippet="lst = [1, 2, 3, 4, 5]\nlst[1:4] = [9]\nprint(lst)",
        correct_output="[1, 9, 5]",
        explanation="Asignar a `lst[1:4]` reemplaza esos tres elementos (2,3,4) por el contenido del nuevo iterable `[9]`, encogiendo la lista.",
        hint="El slice 1:4 cubre los índices 1, 2 y 3; se sustituyen por un solo elemento.",
        elo_rating=1000,
    ),
    CuratedPuzzle(
        slug_suffix="zip-star-transpose",
        title="Transponer con zip(*)",
        topic="iterables",
        code_snippet="m = [[1, 2, 3], [4, 5, 6]]\nprint([list(t) for t in zip(*m)])",
        correct_output="[[1, 4], [2, 5], [3, 6]]",
        explanation="`zip(*m)` desempaqueta las filas y las empareja por columna, transponiendo la matriz.",
        hint="zip agrupa el primer elemento de cada fila, luego el segundo, etc.",
        elo_rating=1080,
    ),
    CuratedPuzzle(
        slug_suffix="walrus-while",
        title="Operador morsa en while",
        topic="operadores",
        code_snippet="data = [1, 2, 3]\nout = []\nwhile (n := len(data)) > 0:\n    out.append(n)\n    data.pop()\nprint(out)",
        correct_output="[3, 2, 1]",
        explanation="`:=` asigna y evalúa en la condición: en cada vuelta guarda el largo actual (3, 2, 1) antes de hacer pop.",
        hint="¿Cuánto vale len(data) en cada iteración antes del pop?",
        elo_rating=1150,
    ),
]


CURATED_NUMPY_PUZZLES: list[CuratedPuzzle] = [
    CuratedPuzzle(
        slug_suffix="arange-vs-linspace",
        title="np.arange vs np.linspace",
        topic="creation",
        code_snippet="import numpy as np\nprint(np.arange(0, 10, 3).tolist())\nprint(np.linspace(0, 10, 3).tolist())",
        correct_output="[0, 3, 6, 9]\n[0.0, 5.0, 10.0]",
        explanation="`arange(start, stop, step)` da pasos fijos sin incluir stop. `linspace(start, stop, num)` da `num` puntos equiespaciados incluyendo stop.",
        hint="`arange` toma paso, `linspace` toma cantidad de puntos.",
        elo_rating=1100,
    ),
    CuratedPuzzle(
        slug_suffix="boolean-mask",
        title="Indexado por máscara booleana",
        topic="indexing",
        code_snippet="import numpy as np\narr = np.array([1, 5, 3, 8, 2])\nprint(arr[arr > 3].tolist())",
        correct_output="[5, 8]",
        explanation="`arr > 3` produce un array booleano; al indexar con él filtra solo los True.",
        hint="¿Qué elementos son mayores que 3?",
        elo_rating=1150,
    ),
    CuratedPuzzle(
        slug_suffix="reshape-axis-sum",
        title="reshape y sum por axis",
        topic="reshaping",
        code_snippet="import numpy as np\nm = np.arange(6).reshape(2, 3)\nprint(m.sum(axis=0).tolist())\nprint(m.sum(axis=1).tolist())",
        correct_output="[3, 5, 7]\n[3, 12]",
        explanation="`axis=0` suma columnas (colapsa filas): [0+3, 1+4, 2+5]. `axis=1` suma filas: [0+1+2, 3+4+5].",
        hint="axis=0 colapsa filas, axis=1 colapsa columnas.",
        elo_rating=1250,
    ),
    CuratedPuzzle(
        slug_suffix="broadcasting-vector",
        title="Broadcasting matriz + vector",
        topic="broadcasting",
        code_snippet="import numpy as np\nm = np.array([[1, 2, 3], [4, 5, 6]])\nv = np.array([10, 20, 30])\nprint((m + v).tolist())",
        correct_output="[[11, 22, 33], [14, 25, 36]]",
        explanation="`v` (shape (3,)) se difunde a cada fila de `m` (shape (2,3)).",
        hint="Broadcasting alinea dimensiones a la derecha.",
        elo_rating=1300,
    ),
    CuratedPuzzle(
        slug_suffix="where-conditional",
        title="np.where para reemplazar",
        topic="conditionals",
        code_snippet="import numpy as np\narr = np.array([1, -2, 3, -4])\nprint(np.where(arr < 0, 0, arr).tolist())",
        correct_output="[1, 0, 3, 0]",
        explanation="`np.where(cond, a, b)` selecciona `a` donde cond es True, `b` donde es False. Aquí reemplaza negativos por 0.",
        hint="Como un if vectorizado.",
        elo_rating=1320,
    ),
    CuratedPuzzle(
        slug_suffix="argmax-axis",
        title="argmax por axis",
        topic="reductions",
        code_snippet="import numpy as np\nm = np.array([[1, 5, 3], [4, 2, 6]])\nprint(m.argmax(axis=1).tolist())",
        correct_output="[1, 2]",
        explanation="Por fila: índice del máximo. Fila 0=[1,5,3] → 1; fila 1=[4,2,6] → 2.",
        hint="argmax devuelve índice, no valor.",
        elo_rating=1380,
    ),
    CuratedPuzzle(
        slug_suffix="dot-product",
        title="Producto punto de vectores",
        topic="linalg",
        code_snippet="import numpy as np\na = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\nprint(a @ b)",
        correct_output="32",
        explanation="1·4 + 2·5 + 3·6 = 4 + 10 + 18 = 32.",
        hint="`@` es el operador de producto matricial; sobre vectores 1D es producto punto.",
        elo_rating=1400,
    ),
    CuratedPuzzle(
        slug_suffix="unique-counts",
        title="np.unique con return_counts",
        topic="reductions",
        code_snippet='import numpy as np\narr = np.array(["a", "b", "a", "c", "b", "a"])\nvals, counts = np.unique(arr, return_counts=True)\nprint(vals.tolist())\nprint(counts.tolist())',
        correct_output="['a', 'b', 'c']\n[3, 2, 1]",
        explanation="`unique` ordena alfabéticamente; `return_counts` da la frecuencia de cada uno.",
        hint="¿Cuántas 'a' hay? ¿Y 'b'?",
        elo_rating=1450,
    ),
    CuratedPuzzle(
        slug_suffix="slicing-2d",
        title="Slicing 2D — fila vs columna",
        topic="indexing",
        code_snippet="import numpy as np\nm = np.arange(12).reshape(3, 4)\nprint(m[:, 1].tolist())\nprint(m[1, :].tolist())",
        correct_output="[1, 5, 9]\n[4, 5, 6, 7]",
        explanation="`m[:,1]` es la columna 1 de las 3 filas. `m[1,:]` es la fila 1 entera.",
        hint="`,` separa filas de columnas; `:` significa todo en ese eje.",
        elo_rating=1500,
    ),
    CuratedPuzzle(
        slug_suffix="cumsum",
        title="np.cumsum",
        topic="reductions",
        code_snippet="import numpy as np\narr = np.array([1, 2, 3, 4])\nprint(arr.cumsum().tolist())",
        correct_output="[1, 3, 6, 10]",
        explanation="Suma acumulada: 1, 1+2, 1+2+3, 1+2+3+4.",
        hint="cum = cumulative.",
        elo_rating=1550,
    ),
    CuratedPuzzle(
        slug_suffix="concatenate-1d",
        title="np.concatenate de arrays 1D",
        topic="manipulation",
        code_snippet="import numpy as np\na = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\nprint(np.concatenate([a, b]).tolist())",
        correct_output="[1, 2, 3, 4, 5, 6]",
        explanation="`concatenate` une los arrays a lo largo del eje 0 por defecto.",
        hint="Es como sumar listas, pero produce ndarray.",
        elo_rating=1080,
    ),
    CuratedPuzzle(
        slug_suffix="transpose-shape",
        title="Transpuesta y shape",
        topic="reshaping",
        code_snippet="import numpy as np\nm = np.array([[1, 2], [3, 4], [5, 6]])\nprint(m.T.shape)",
        correct_output="(2, 3)",
        explanation="`m` tiene shape (3,2); su transpuesta intercambia ejes y queda (2,3).",
        hint="`.T` invierte filas y columnas.",
        elo_rating=1130,
    ),
    CuratedPuzzle(
        slug_suffix="clip-bounds",
        title="np.clip recorta a un rango",
        topic="conditionals",
        code_snippet="import numpy as np\narr = np.array([-2, 5, 0, 12, -7])\nprint(np.clip(arr, 0, 10).tolist())",
        correct_output="[0, 5, 0, 10, 0]",
        explanation="`clip(arr, lo, hi)` lleva valores < lo a lo y > hi a hi. Negativos → 0; 12 → 10.",
        hint="Sirve para acotar a un rango sin bucle explícito.",
        elo_rating=1170,
    ),
    CuratedPuzzle(
        slug_suffix="mean-axis",
        title="mean por axis",
        topic="reductions",
        code_snippet="import numpy as np\nm = np.array([[1, 2, 3], [4, 5, 6]])\nprint(m.mean(axis=0).tolist())",
        correct_output="[2.5, 3.5, 4.5]",
        explanation="`axis=0` colapsa las filas: promedio columna a columna [(1+4)/2, (2+5)/2, (3+6)/2].",
        hint="axis=0 = promedios verticales.",
        elo_rating=1220,
    ),
    CuratedPuzzle(
        slug_suffix="astype-int-truncates",
        title=".astype(int) trunca hacia cero",
        topic="dtypes",
        code_snippet="import numpy as np\narr = np.array([1.7, 2.3, 3.9])\nprint(arr.astype(int).tolist())",
        correct_output="[1, 2, 3]",
        explanation="`astype(int)` no redondea: trunca la parte decimal hacia 0 (1.7 → 1, 3.9 → 3).",
        hint="No es lo mismo que round().",
        elo_rating=1050,
    ),
    CuratedPuzzle(
        slug_suffix="sort-axis-rows",
        title="np.sort por axis",
        topic="sorting",
        code_snippet="import numpy as np\nm = np.array([[3, 1], [4, 2]])\nprint(np.sort(m, axis=1).tolist())",
        correct_output="[[1, 3], [2, 4]]",
        explanation="`axis=1` ordena dentro de cada fila: [3,1]→[1,3]; [4,2]→[2,4]. No reordena filas entre sí.",
        hint="axis=1 = ordena dentro de cada fila.",
        elo_rating=1280,
    ),
    CuratedPuzzle(
        slug_suffix="maximum-elementwise",
        title="np.maximum elemento a elemento",
        topic="conditionals",
        code_snippet="import numpy as np\na = np.array([1, 5, 3])\nb = np.array([4, 2, 6])\nprint(np.maximum(a, b).tolist())",
        correct_output="[4, 5, 6]",
        explanation="`np.maximum` compara posición por posición y devuelve el mayor de cada par. Distinto de `np.max(a)` que reduce.",
        hint="Es como un `if a>b else b` vectorizado.",
        elo_rating=1260,
    ),
    CuratedPuzzle(
        slug_suffix="stack-new-axis",
        title="np.stack agrega un eje",
        topic="manipulation",
        code_snippet="import numpy as np\na = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\nprint(np.stack([a, b]).shape)",
        correct_output="(2, 3)",
        explanation="`stack` apila los arrays creando un eje nuevo (a diferencia de `concatenate` que une en un eje existente). Resultado 2D.",
        hint="stack añade dimensión, concatenate no.",
        elo_rating=1370,
    ),
    CuratedPuzzle(
        slug_suffix="zeros-shape",
        title="np.zeros con shape y dtype",
        topic="creation",
        code_snippet="import numpy as np\nz = np.zeros((2, 3), dtype=int)\nprint(z.tolist())",
        correct_output="[[0, 0, 0], [0, 0, 0]]",
        explanation="`np.zeros((m, n))` crea matriz m×n llena de ceros. `dtype=int` evita que sean floats por defecto.",
        hint="Util para inicializar matrices vacías.",
        elo_rating=950,
    ),
    CuratedPuzzle(
        slug_suffix="eye-identity",
        title="np.eye matriz identidad",
        topic="creation",
        code_snippet="import numpy as np\ne = np.eye(3, dtype=int)\nprint(e.tolist())",
        correct_output="[[1, 0, 0], [0, 1, 0], [0, 0, 1]]",
        explanation="`np.eye(n)` crea la matriz identidad n×n: 1s en la diagonal, 0 en el resto.",
        hint="La matriz identidad es el neutro multiplicativo en álgebra lineal.",
        elo_rating=1100,
    ),
    CuratedPuzzle(
        slug_suffix="matrix-multiply",
        title="Multiplicación matricial con @",
        topic="linalg",
        code_snippet="import numpy as np\nA = np.array([[1, 2], [3, 4]])\nB = np.array([[5, 6], [7, 8]])\nprint((A @ B).tolist())",
        correct_output="[[19, 22], [43, 50]]",
        explanation="`A @ B` es producto matricial. Fila por columna: [1·5+2·7, 1·6+2·8; 3·5+4·7, 3·6+4·8] = [[19,22],[43,50]].",
        hint="Sobre 1D `@` es producto punto; sobre 2D es producto matricial.",
        elo_rating=1420,
    ),
    CuratedPuzzle(
        slug_suffix="median-array",
        title="np.median",
        topic="reductions",
        code_snippet="import numpy as np\narr = np.array([1, 3, 5, 7, 9])\nprint(np.median(arr))",
        correct_output="5.0",
        explanation="La mediana del array ordenado [1,3,5,7,9] es el elemento central: 5.",
        hint="Mediana ≠ promedio: aquí coincidirían si la distribución es simétrica.",
        elo_rating=1180,
    ),
    CuratedPuzzle(
        slug_suffix="boolean-sum-count",
        title="Contar con una máscara booleana",
        topic="boolean",
        code_snippet="import numpy as np\na = np.array([1, 5, 2, 8, 3])\nprint(int((a > 3).sum()))",
        correct_output="2",
        explanation="`a > 3` da un array de booleanos; al sumarlo, True cuenta como 1: hay dos valores (5 y 8) mayores a 3.",
        hint="True == 1 al sumar. ¿Cuántos superan 3?",
        elo_rating=1100,
    ),
    CuratedPuzzle(
        slug_suffix="linspace-num",
        title="np.linspace incluye el extremo",
        topic="creation",
        code_snippet="import numpy as np\nprint(np.linspace(0, 1, 5).tolist())",
        correct_output="[0.0, 0.25, 0.5, 0.75, 1.0]",
        explanation="`linspace(0, 1, 5)` reparte 5 puntos equiespaciados incluyendo ambos extremos: paso 0.25.",
        hint="Son 5 valores de 0 a 1 inclusive; ¿cuál es el paso?",
        elo_rating=1150,
    ),
    CuratedPuzzle(
        slug_suffix="reshape-infer",
        title="reshape con dimensión -1",
        topic="shapes",
        code_snippet="import numpy as np\na = np.arange(12).reshape(3, -1)\nprint(a.shape)",
        correct_output="(3, 4)",
        explanation="`-1` le pide a NumPy inferir esa dimensión: 12 elementos en 3 filas ⇒ 4 columnas.",
        hint="12 / 3 = ?",
        elo_rating=1180,
    ),
    CuratedPuzzle(
        slug_suffix="np-diff",
        title="Diferencias consecutivas con np.diff",
        topic="aggregation",
        code_snippet="import numpy as np\na = np.array([1, 4, 9, 16])\nprint(np.diff(a).tolist())",
        correct_output="[3, 5, 7]",
        explanation="`np.diff` resta cada elemento del siguiente: 4-1, 9-4, 16-9. El resultado tiene un elemento menos.",
        hint="Resta cada par consecutivo.",
        elo_rating=1250,
    ),
    CuratedPuzzle(
        slug_suffix="fancy-index-rows",
        title="Fancy indexing de filas",
        topic="indexing",
        code_snippet="import numpy as np\na = np.arange(1, 10).reshape(3, 3)\nprint(a[[0, 2]].tolist())",
        correct_output="[[1, 2, 3], [7, 8, 9]]",
        explanation="Indexar con una lista `[0, 2]` selecciona esas filas en ese orden: la 0 y la 2.",
        hint="¿Qué filas son la 0 y la 2 de la matriz 3x3?",
        elo_rating=1300,
    ),
    CuratedPuzzle(
        slug_suffix="round-half-even",
        title="np.round usa redondeo bancario",
        topic="gotchas",
        code_snippet="import numpy as np\nprint(np.round(np.array([0.5, 1.5, 2.5, 3.5])).tolist())",
        correct_output="[0.0, 2.0, 2.0, 4.0]",
        explanation="NumPy redondea al par más cercano (banker's rounding): 0.5→0, 1.5→2, 2.5→2, 3.5→4. No es el redondeo 'siempre hacia arriba'.",
        hint="Los .5 van al entero PAR más cercano, no siempre hacia arriba.",
        elo_rating=1420,
    ),
]


CURATED_PANDAS_PUZZLES: list[CuratedPuzzle] = [
    CuratedPuzzle(
        slug_suffix="dataframe-creation",
        title="DataFrame desde dict de listas",
        topic="creation",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"a": [1, 2], "b": [3, 4]})\nprint(df.shape)',
        correct_output="(2, 2)",
        explanation="2 filas, 2 columnas → `(2, 2)`.",
        hint="`shape` es (n_filas, n_columnas).",
        elo_rating=1100,
    ),
    CuratedPuzzle(
        slug_suffix="filter-rows-mask",
        title="Filtrar filas con máscara booleana",
        topic="filtering",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"x": [1, 2, 3, 4]})\nprint(df[df["x"] > 2]["x"].tolist())',
        correct_output="[3, 4]",
        explanation="`df['x'] > 2` produce máscara booleana; al indexar `df[mask]` filtra esas filas.",
        hint="Solo las filas donde x es estrictamente mayor que 2.",
        elo_rating=1150,
    ),
    CuratedPuzzle(
        slug_suffix="value-counts",
        title="value_counts ordenado por frecuencia",
        topic="aggregation",
        code_snippet='import pandas as pd\ns = pd.Series(["x", "y", "x", "z", "x", "y"])\nprint(s.value_counts().to_dict())',
        correct_output="{'x': 3, 'y': 2, 'z': 1}",
        explanation="`value_counts()` cuenta apariciones y ordena descendente.",
        hint="¿Cuántas 'x' hay?",
        elo_rating=1200,
    ),
    CuratedPuzzle(
        slug_suffix="sort-values-descending",
        title="sort_values descendente",
        topic="sorting",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"name": ["a", "b", "c"], "score": [10, 30, 20]})\nout = df.sort_values("score", ascending=False)["name"].tolist()\nprint(out)',
        correct_output="['b', 'c', 'a']",
        explanation="Ordena por `score` descendente: 30, 20, 10 → b, c, a.",
        hint="ascending=False invierte el orden por defecto.",
        elo_rating=1250,
    ),
    CuratedPuzzle(
        slug_suffix="groupby-mean",
        title="groupby + mean",
        topic="grouping",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"team": ["A", "A", "B", "B"], "pts": [10, 20, 30, 50]})\nres = df.groupby("team")["pts"].mean().to_dict()\nprint(res["A"], res["B"])',
        correct_output="15.0 40.0",
        explanation="A: (10+20)/2 = 15. B: (30+50)/2 = 40.",
        hint="mean = promedio.",
        elo_rating=1300,
    ),
    CuratedPuzzle(
        slug_suffix="apply-row-derived",
        title="apply sobre columna",
        topic="apply",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"x": [1, 2, 3]})\ndf["y"] = df["x"].apply(lambda v: v * v + 1)\nprint(df["y"].tolist())',
        correct_output="[2, 5, 10]",
        explanation="Cada x se mapea a x²+1: 1→2, 2→5, 3→10.",
        hint="apply aplica la función a cada elemento.",
        elo_rating=1330,
    ),
    CuratedPuzzle(
        slug_suffix="dropna",
        title="dropna sobre columnas",
        topic="cleaning",
        code_snippet='import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({"a": [1, 2, np.nan], "b": [4, np.nan, 6]})\nprint(len(df.dropna()))',
        correct_output="1",
        explanation="Solo la primera fila no tiene NaN; las otras dos sí — quedan eliminadas.",
        hint="dropna por defecto borra cualquier fila con al menos un NaN.",
        elo_rating=1380,
    ),
    CuratedPuzzle(
        slug_suffix="merge-on-key",
        title="merge sobre clave común",
        topic="joins",
        code_snippet='import pandas as pd\na = pd.DataFrame({"id": [1, 2, 3], "v": ["x", "y", "z"]})\nb = pd.DataFrame({"id": [2, 3], "w": [10, 20]})\nm = a.merge(b, on="id")\nprint(len(m), m["w"].tolist())',
        correct_output="2 [10, 20]",
        explanation="Inner join por defecto: solo ids 2 y 3 están en ambos. 2 filas resultantes.",
        hint="merge sin `how=` es inner por defecto.",
        elo_rating=1430,
    ),
    CuratedPuzzle(
        slug_suffix="pivot-table",
        title="pivot_table simple",
        topic="reshaping",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"d": ["L", "L", "M", "M"], "t": ["x", "y", "x", "y"], "v": [1, 2, 3, 4]})\np = df.pivot_table(index="d", columns="t", values="v")\nprint(p.loc["L", "x"], p.loc["M", "y"])',
        correct_output="1.0 4.0",
        explanation="Tabla cruzada: fila L+col x → 1; fila M+col y → 4. `pivot_table` agrega con la media por defecto, así que el resultado es float.",
        hint="pivot_table reorganiza filas/columnas según los campos elegidos.",
        elo_rating=1500,
    ),
    CuratedPuzzle(
        slug_suffix="cumsum-by-group",
        title="cumsum dentro de groupby",
        topic="grouping",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"g": ["a", "a", "b", "b"], "x": [1, 2, 10, 20]})\nprint(df.groupby("g")["x"].cumsum().tolist())',
        correct_output="[1, 3, 10, 30]",
        explanation="Cumsum por grupo: a→[1, 1+2]; b→[10, 10+20].",
        hint="El cumsum reinicia en cada grupo.",
        elo_rating=1580,
    ),
    CuratedPuzzle(
        slug_suffix="loc-vs-iloc",
        title="loc vs iloc",
        topic="indexing",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"x": [10, 20, 30]}, index=["a", "b", "c"])\nprint(df.loc["b", "x"], df.iloc[2, 0])',
        correct_output="20 30",
        explanation="`loc` indexa por etiqueta (`b` → fila 2da); `iloc` por posición (índice 2 → 3ra fila).",
        hint="loc = label, iloc = integer position.",
        elo_rating=1180,
    ),
    CuratedPuzzle(
        slug_suffix="fillna-default",
        title="fillna con valor por defecto",
        topic="cleaning",
        code_snippet="import pandas as pd\nimport numpy as np\ns = pd.Series([1.0, np.nan, 3.0, np.nan])\nprint(s.fillna(0).tolist())",
        correct_output="[1.0, 0.0, 3.0, 0.0]",
        explanation="`fillna(v)` reemplaza cada NaN por `v` sin alterar los valores existentes.",
        hint="No confundir con dropna: aquí mantenemos todas las filas.",
        elo_rating=1230,
    ),
    CuratedPuzzle(
        slug_suffix="nlargest-by-column",
        title="nlargest por columna",
        topic="sorting",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"name": ["a", "b", "c", "d"], "score": [10, 50, 30, 20]})\nprint(df.nlargest(2, "score")["name"].tolist())',
        correct_output="['b', 'c']",
        explanation="`nlargest(2, 'score')` toma las 2 filas con mayor `score`: b (50) y c (30).",
        hint="Equivalente a sort_values(...ascending=False).head(2).",
        elo_rating=1350,
    ),
    CuratedPuzzle(
        slug_suffix="assign-derived-column",
        title="assign para crear columna derivada",
        topic="creation",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"x": [1, 2, 3]})\ndf = df.assign(y=df["x"] * 10)\nprint(df["y"].tolist())',
        correct_output="[10, 20, 30]",
        explanation="`assign(name=expr)` retorna un DataFrame nuevo con la columna agregada. Pipeline-friendly: encadena bien con otros métodos.",
        hint="No muta in-place; devuelve copia con la nueva columna.",
        elo_rating=1240,
    ),
    CuratedPuzzle(
        slug_suffix="isin-multi-filter",
        title="Filtrar con isin",
        topic="filtering",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"name": ["a", "b", "c", "d"], "v": [1, 2, 3, 4]})\nprint(df[df["name"].isin(["b", "d"])]["v"].tolist())',
        correct_output="[2, 4]",
        explanation="`isin([...])` produce máscara booleana True en filas cuyo valor está en el conjunto. Limpio para múltiples categorías.",
        hint="Más legible que `(df.name == 'b') | (df.name == 'd')`.",
        elo_rating=1280,
    ),
    CuratedPuzzle(
        slug_suffix="str-contains-accessor",
        title="str.contains para filtrar texto",
        topic="strings",
        code_snippet='import pandas as pd\ns = pd.Series(["python", "pandas", "numpy", "javascript"])\nprint(s[s.str.contains("py")].tolist())',
        correct_output="['python', 'numpy']",
        explanation="`s.str` da acceso a métodos de string sobre toda la Serie. `contains('py')` busca el substring; matches: 'python' y 'numpy'.",
        hint="¿Qué strings tienen el substring 'py'? Pandas no, numpy sí.",
        elo_rating=1340,
    ),
    CuratedPuzzle(
        slug_suffix="rename-columns",
        title="rename de columnas",
        topic="cleaning",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"a": [1, 2], "b": [3, 4]})\nprint(df.rename(columns={"a": "x"}).columns.tolist())',
        correct_output="['x', 'b']",
        explanation="`rename(columns={old: new})` retorna un DataFrame con columnas renombradas; las no listadas se mantienen.",
        hint="Sólo lo que está en el dict cambia.",
        elo_rating=1100,
    ),
    CuratedPuzzle(
        slug_suffix="groupby-agg-multi",
        title="groupby + agg con varias métricas",
        topic="grouping",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"g": ["a", "a", "b", "b"], "v": [1, 2, 10, 20]})\nres = df.groupby("g")["v"].agg(["sum", "mean"])\nprint(res.loc["a", "sum"], res.loc["b", "mean"])',
        correct_output="3 15.0",
        explanation='`agg(["sum", "mean"])` aplica varias reducciones a la vez. a→suma=3, b→promedio=(10+20)/2=15.0.',
        hint="agg recibe lista de funciones o nombres.",
        elo_rating=1390,
    ),
    CuratedPuzzle(
        slug_suffix="drop-duplicates-default",
        title="drop_duplicates por defecto",
        topic="cleaning",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"x": [1, 2, 2, 3, 3, 3]})\nprint(df.drop_duplicates()["x"].tolist())',
        correct_output="[1, 2, 3]",
        explanation="Sin args, `drop_duplicates` mantiene la primera aparición y elimina las repetidas.",
        hint="Conserva el orden original; sólo borra repetidos.",
        elo_rating=1190,
    ),
    CuratedPuzzle(
        slug_suffix="concat-rows",
        title="Concatenar DataFrames por filas",
        topic="combine",
        code_snippet='import pandas as pd\na = pd.DataFrame({"x": [1, 2]})\nb = pd.DataFrame({"x": [3]})\nprint(len(pd.concat([a, b])))',
        correct_output="3",
        explanation="`pd.concat` apila por filas (axis=0 por defecto): 2 + 1 = 3 filas.",
        hint="Suma las filas de ambos DataFrames.",
        elo_rating=1150,
    ),
    CuratedPuzzle(
        slug_suffix="nunique-count",
        title="Contar valores distintos con nunique",
        topic="aggregation",
        code_snippet="import pandas as pd\ns = pd.Series([1, 1, 2, 3, 3, 3])\nprint(int(s.nunique()))",
        correct_output="3",
        explanation="`nunique()` cuenta cuántos valores únicos hay: 1, 2 y 3 ⇒ 3.",
        hint="¿Cuántos valores diferentes aparecen, sin contar repeticiones?",
        elo_rating=1160,
    ),
    CuratedPuzzle(
        slug_suffix="groupby-size",
        title="Tamaño de cada grupo con groupby.size",
        topic="grouping",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"g": ["a", "a", "b"], "v": [1, 2, 3]})\nprint(df.groupby("g").size().to_dict())',
        correct_output="{'a': 2, 'b': 1}",
        explanation="`size()` cuenta filas por grupo: 'a' aparece 2 veces, 'b' una.",
        hint="Cuenta cuántas filas tiene cada valor de la columna g.",
        elo_rating=1240,
    ),
    CuratedPuzzle(
        slug_suffix="query-filter",
        title="Filtrar filas con query",
        topic="filtering",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"x": [1, 2, 3, 4]})\nprint(df.query("x % 2 == 0")["x"].tolist())',
        correct_output="[2, 4]",
        explanation="`query` evalúa la expresión como filtro: deja las filas con x par.",
        hint="¿Qué valores cumplen x % 2 == 0?",
        elo_rating=1260,
    ),
    CuratedPuzzle(
        slug_suffix="idxmax-label",
        title="Etiqueta del máximo con idxmax",
        topic="aggregation",
        code_snippet='import pandas as pd\ns = pd.Series([3, 9, 4], index=["a", "b", "c"])\nprint(s.idxmax())',
        correct_output="b",
        explanation="`idxmax()` devuelve la etiqueta del índice (no la posición) donde está el valor máximo: 9 está en 'b'.",
        hint="Devuelve el índice, no el valor. ¿Dónde está el 9?",
        elo_rating=1280,
    ),
    CuratedPuzzle(
        slug_suffix="cut-bins",
        title="Discretizar en rangos con pd.cut",
        topic="binning",
        code_snippet='import pandas as pd\nedades = pd.Series([5, 18, 45, 70])\nbins = pd.cut(edades, [0, 12, 18, 65, 120], labels=["nino", "adolescente", "adulto", "mayor"])\nprint(bins.tolist())',
        correct_output="['nino', 'adolescente', 'adulto', 'mayor']",
        explanation="`pd.cut` asigna cada valor a su intervalo (cerrado por la derecha): 5∈(0,12], 18∈(12,18], 45∈(18,65], 70∈(65,120].",
        hint="Los intervalos son cerrados por la derecha: 18 cae en (12, 18].",
        elo_rating=1390,
    ),
    CuratedPuzzle(
        slug_suffix="melt-wide-long",
        title="De ancho a largo con melt",
        topic="reshape",
        code_snippet='import pandas as pd\ndf = pd.DataFrame({"id": [1], "a": [10], "b": [20]})\nm = df.melt(id_vars="id", var_name="k", value_name="v")\nprint(m["v"].tolist())',
        correct_output="[10, 20]",
        explanation="`melt` pasa de formato ancho a largo: las columnas a y b se vuelven filas; sus valores 10 y 20 quedan en la columna `v`.",
        hint="Cada columna no-id se convierte en una fila con su valor.",
        elo_rating=1410,
    ),
]


CURATED_INTERVIEW_PUZZLES: list[CuratedPuzzle] = [
    CuratedPuzzle(
        slug_suffix="two-sum-hashmap",
        title="Two Sum con hashmap",
        topic="two-sum",
        code_snippet="nums = [2, 7, 11, 15]\ntarget = 9\nseen = {}\nfor i, n in enumerate(nums):\n    if target - n in seen:\n        print(seen[target - n], i)\n        break\n    seen[n] = i",
        correct_output="0 1",
        explanation="2 + 7 = 9. Cuando i=1 (n=7), `target-n = 2` ya está en seen con índice 0.",
        hint="El hashmap permite verificar el complemento en O(1).",
        elo_rating=1400,
    ),
    CuratedPuzzle(
        slug_suffix="reverse-linked-iterative",
        title="Suma de dígitos iterativa",
        topic="loops",
        code_snippet="n = 1234\ntotal = 0\nwhile n:\n    total += n % 10\n    n //= 10\nprint(total)",
        correct_output="10",
        explanation="1+2+3+4 = 10. `% 10` extrae último dígito; `// 10` lo descarta.",
        hint="Modulo y división entera son la herramienta clásica.",
        elo_rating=1430,
    ),
    CuratedPuzzle(
        slug_suffix="binary-search",
        title="Búsqueda binaria",
        topic="search",
        code_snippet="arr = [1, 3, 5, 7, 9, 11]\ntarget = 7\nlo, hi = 0, len(arr) - 1\nidx = -1\nwhile lo <= hi:\n    mid = (lo + hi) // 2\n    if arr[mid] == target:\n        idx = mid\n        break\n    if arr[mid] < target:\n        lo = mid + 1\n    else:\n        hi = mid - 1\nprint(idx)",
        correct_output="3",
        explanation="7 está en índice 3. Búsqueda binaria converge en O(log n).",
        hint="Compara el valor del medio con el target.",
        elo_rating=1500,
    ),
    CuratedPuzzle(
        slug_suffix="fibonacci-memo",
        title="Fibonacci con memoización",
        topic="dp",
        code_snippet="memo = {0: 0, 1: 1}\ndef fib(n):\n    if n not in memo:\n        memo[n] = fib(n-1) + fib(n-2)\n    return memo[n]\n\nprint(fib(10))",
        correct_output="55",
        explanation="fib(10) = 55. La memoización evita recalcular subproblemas.",
        hint="Sin memo, fib(10) tarda mucho. Con memo, es O(n).",
        elo_rating=1550,
    ),
    CuratedPuzzle(
        slug_suffix="anagrams-counter",
        title="Detectar anagramas con Counter",
        topic="strings",
        code_snippet='from collections import Counter\na, b = "listen", "silent"\nprint(Counter(a) == Counter(b))',
        correct_output="True",
        explanation="`Counter` cuenta apariciones; dos anagramas tienen el mismo conteo de letras.",
        hint="Es O(n) sin necesidad de ordenar.",
        elo_rating=1600,
    ),
    CuratedPuzzle(
        slug_suffix="reverse-two-pointers",
        title="Invertir string in-place con dos punteros",
        topic="two-pointers",
        code_snippet='s = list("hola")\nl, r = 0, len(s) - 1\nwhile l < r:\n    s[l], s[r] = s[r], s[l]\n    l += 1\n    r -= 1\nprint("".join(s))',
        correct_output="aloh",
        explanation="Dos punteros se acercan intercambiando extremos; en O(n/2) la cadena queda invertida sin copia auxiliar.",
        hint="Swap simétrico mientras `l < r`.",
        elo_rating=1380,
    ),
    CuratedPuzzle(
        slug_suffix="climbing-stairs-dp",
        title="Climbing Stairs (DP iterativa)",
        topic="dp",
        code_snippet="n = 5\na, b = 1, 1\nfor _ in range(n):\n    a, b = b, a + b\nprint(a)",
        correct_output="8",
        explanation="ways(n) = ways(n-1) + ways(n-2). Para 5 escalones hay 8 combinaciones (1/2 a la vez).",
        hint="Es Fibonacci con índices corridos.",
        elo_rating=1450,
    ),
    CuratedPuzzle(
        slug_suffix="kadane-max-subarray",
        title="Kadane: máxima suma de subarreglo",
        topic="dp",
        code_snippet="nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]\nbest = cur = nums[0]\nfor n in nums[1:]:\n    cur = max(n, cur + n)\n    best = max(best, cur)\nprint(best)",
        correct_output="6",
        explanation="La mejor ventana contigua es [4, -1, 2, 1] con suma 6. Kadane decide en cada paso si extiende o reinicia.",
        hint="`cur = max(n, cur+n)` decide reiniciar o extender.",
        elo_rating=1530,
    ),
    CuratedPuzzle(
        slug_suffix="contains-duplicate-set",
        title="Contains Duplicate con set",
        topic="hashing",
        code_snippet="nums = [1, 2, 3, 1, 4]\nprint(len(set(nums)) != len(nums))",
        correct_output="True",
        explanation="`set(nums)` deduplica; si su tamaño es menor que la lista original, hay al menos un duplicado.",
        hint="Comparar tamaños es O(n) sin hash table manual.",
        elo_rating=1320,
    ),
    CuratedPuzzle(
        slug_suffix="merge-two-sorted",
        title="Merge de dos listas ordenadas",
        topic="two-pointers",
        code_snippet="a = [1, 3, 5]\nb = [2, 4, 6]\ni = j = 0\nout = []\nwhile i < len(a) and j < len(b):\n    if a[i] <= b[j]:\n        out.append(a[i])\n        i += 1\n    else:\n        out.append(b[j])\n        j += 1\nout.extend(a[i:])\nout.extend(b[j:])\nprint(out)",
        correct_output="[1, 2, 3, 4, 5, 6]",
        explanation="Dos punteros avanzan al menor entre `a[i]` y `b[j]`. Los restos se concatenan al final. O(n+m).",
        hint="Es el `merge` del merge sort.",
        elo_rating=1480,
    ),
    CuratedPuzzle(
        slug_suffix="valid-palindrome-alnum",
        title="Palindrome ignorando no-alfanuméricos",
        topic="two-pointers",
        code_snippet='s = "A man, a plan, a canal: Panama"\nfiltered = [c.lower() for c in s if c.isalnum()]\nprint(filtered == filtered[::-1])',
        correct_output="True",
        explanation="Filtra letras y dígitos en minúscula → 'amanaplanacanalpanama' que se lee igual al revés.",
        hint="`isalnum()` filtra; `[::-1]` invierte.",
        elo_rating=1500,
    ),
    CuratedPuzzle(
        slug_suffix="first-non-repeating-char",
        title="Primer carácter no repetido",
        topic="hashing",
        code_snippet='from collections import Counter\ns = "leetcode"\nc = Counter(s)\nfor ch in s:\n    if c[ch] == 1:\n        print(ch)\n        break',
        correct_output="l",
        explanation="Counter cuenta apariciones; recorremos `s` en orden y devolvemos el primero con count 1. En \"leetcode\", la 'l' aparece sólo una vez y va primera.",
        hint="Pasa 1: contar. Pasa 2: encontrar.",
        elo_rating=1410,
    ),
    CuratedPuzzle(
        slug_suffix="rotate-array-slice",
        title="Rotar array a la derecha con slicing",
        topic="arrays",
        code_snippet="nums = [1, 2, 3, 4, 5]\nk = 2\nn = len(nums)\nk = k % n\nprint(nums[-k:] + nums[:-k])",
        correct_output="[4, 5, 1, 2, 3]",
        explanation="Toma los últimos `k` elementos y los coloca al frente. `k % n` evita rotaciones redundantes cuando k > n.",
        hint="Pythonic: dos slices y una suma.",
        elo_rating=1460,
    ),
    CuratedPuzzle(
        slug_suffix="product-except-self",
        title="Product of Array Except Self (sin división)",
        topic="arrays",
        code_snippet="nums = [1, 2, 3, 4]\nn = len(nums)\nout = [1] * n\nleft = 1\nfor i in range(n):\n    out[i] = left\n    left *= nums[i]\nright = 1\nfor i in range(n - 1, -1, -1):\n    out[i] *= right\n    right *= nums[i]\nprint(out)",
        correct_output="[24, 12, 8, 6]",
        explanation="Dos pasadas: izquierda guarda producto de prefijos, derecha multiplica por el sufijo. O(n) tiempo, O(1) extra (sin contar `out`).",
        hint="No uses división — fallaría con ceros.",
        elo_rating=1620,
    ),
    CuratedPuzzle(
        slug_suffix="gcd-euclid",
        title="MCD con el algoritmo de Euclides",
        topic="matematicas",
        code_snippet="def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\nprint(gcd(48, 36))",
        correct_output="12",
        explanation="Euclides: reemplaza (a, b) por (b, a%b) hasta que b sea 0. 48,36 → 36,12 → 12,0 ⇒ 12.",
        hint="En cada paso b pasa a ser el resto a % b.",
        elo_rating=1240,
    ),
    CuratedPuzzle(
        slug_suffix="valid-parentheses-stack",
        title="Paréntesis balanceados con pila",
        topic="stacks",
        code_snippet='def valida(s):\n    pares = {")": "(", "]": "[", "}": "{"}\n    pila = []\n    for c in s:\n        if c in "([{":\n            pila.append(c)\n        elif not pila or pila.pop() != pares[c]:\n            return False\n    return not pila\nprint(valida("([]{})"))',
        correct_output="True",
        explanation="Cada apertura se apila; cada cierre debe coincidir con el tope. Al final la pila queda vacía ⇒ balanceado.",
        hint="Una pila vacía al terminar significa que todo cerró bien.",
        elo_rating=1320,
    ),
    CuratedPuzzle(
        slug_suffix="single-number-xor",
        title="El número único con XOR",
        topic="bits",
        code_snippet="from functools import reduce\nnums = [4, 1, 2, 1, 2]\nprint(reduce(lambda a, b: a ^ b, nums))",
        correct_output="4",
        explanation="XOR es conmutativo y x^x=0: los pares se anulan (1^1, 2^2) y sobrevive el único sin pareja, 4.",
        hint="a ^ a = 0. ¿Qué número no tiene pareja?",
        elo_rating=1360,
    ),
]


_PUZZLE_CATALOG: list[tuple[str, list[CuratedPuzzle]]] = [
    ("python", CURATED_PYTHON_PUZZLES),
    ("numpy", CURATED_NUMPY_PUZZLES),
    ("pandas", CURATED_PANDAS_PUZZLES),
    ("interview", CURATED_INTERVIEW_PUZZLES),
]


async def _deactivate_legacy_generated_puzzles(db: AsyncSession) -> int:
    """Marca como inactivos los puzzles del banco viejo (variantes con seed).

    Los slugs viejos siguen el patrón
    `pycode-curated-open-{cat}-{prefix}-{N}` donde prefix era 'pandas-group',
    'py-arithmetic', 'py-strings', 'py-lists', 'numpy-vector' o
    'interview-pattern'. Los desactivamos para que no aparezcan más en la
    lista pública.
    """
    legacy_prefixes = [
        "pandas-group",
        "py-arithmetic",
        "py-strings",
        "py-lists",
        "numpy-vector",
        "interview-pattern",
    ]
    affected = 0
    for prefix in legacy_prefixes:
        result = await db.execute(
            select(Puzzle).where(
                Puzzle.slug.like(f"{CURATED_SOURCE}-%-{prefix}-%"),
                Puzzle.is_active.is_(True),
            )
        )
        for puzzle in result.scalars().all():
            puzzle.is_active = False
            affected += 1
    if affected:
        await db.commit()
    return affected


async def seed_generated_puzzles(db: AsyncSession) -> int:
    """Insert curated conceptual puzzles across categories.

    Antes de insertar, desactiva los puzzles del banco viejo (variantes
    con seed) para que la lista solo muestre los curados.
    """
    await _deactivate_legacy_generated_puzzles(db)

    inserted = 0
    for category, puzzles in _PUZZLE_CATALOG:
        for puzzle in puzzles:
            slug = f"{CURATED_SOURCE}-{category}-{puzzle.slug_suffix}"
            existing = await db.execute(select(Puzzle.id).where(Puzzle.slug == slug))
            if existing.scalar_one_or_none() is not None:
                continue

            row = Puzzle(
                title=puzzle.title,
                slug=slug,
                category=category,
                topic=puzzle.topic,
                code_snippet=puzzle.code_snippet,
                correct_output=puzzle.correct_output,
                explanation=puzzle.explanation,
                hint=puzzle.hint,
                elo_rating=puzzle.elo_rating,
                elo_initial=puzzle.elo_rating,
                is_advanced=puzzle.elo_rating >= 1450,
                is_active=True,
                source_book="Curated Conceptual Bank",
            )
            db.add(row)
            inserted += 1

    if inserted:
        await db.commit()

    return inserted
