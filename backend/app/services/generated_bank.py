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


def _python_puzzle_snippet(seed: int) -> tuple[str, str, str]:
    a = seed + 2
    b = seed * 3
    snippet = f"x = {a}\n" f"y = {b}\n" "print(x + y)\n" "print((x * y) % 7)"
    out_1 = a + b
    out_2 = (a * b) % 7
    return snippet, f"{out_1}\n{out_2}", "arithmetic"


def _string_puzzle_snippet(seed: int) -> tuple[str, str, str]:
    word = f"python{seed}"
    snippet = f"s = '{word}'\nprint(s[::-1])\nprint(s.upper().count('O'))"
    result = f"{word[::-1]}\n{word.upper().count('O')}"
    return snippet, result, "strings"


def _list_puzzle_snippet(seed: int) -> tuple[str, str, str]:
    base = [seed, seed + 1, seed + 2, seed + 3]
    snippet = (
        f"nums = {base}\n"
        "print(sum(nums[1:3]))\n"
        "nums.append(nums[0] * 2)\n"
        "print(nums[-1])"
    )
    return snippet, f"{sum(base[1:3])}\n{base[0] * 2}", "lists"


def _interview_puzzle_snippet(seed: int) -> tuple[str, str, str]:
    target = seed + 10
    nums = [seed, seed + 1, seed + 4, seed + 9]
    snippet = (
        f"nums = {nums}\n"
        f"target = {target}\n"
        "seen = set()\n"
        "ok = False\n"
        "for n in nums:\n"
        "    if target - n in seen:\n"
        "        ok = True\n"
        "        break\n"
        "    seen.add(n)\n"
        "print(ok)"
    )
    values = set(nums)
    ok = any(
        (target - n) in values and (target - n != n or nums.count(n) > 1) for n in nums
    )
    return snippet, str(ok), "two-sum"


def _numpy_puzzle_snippet(seed: int) -> tuple[str, str, str]:
    a = [seed, seed + 1, seed + 2]
    b = [seed * 2, seed * 3, seed * 4]
    snippet = (
        "import numpy as np\n"
        f"a = np.array({a})\n"
        f"b = np.array({b})\n"
        "print(int((a + b).sum()))\n"
        "print(int((a * b).max()))"
    )
    out_1 = sum(x + y for x, y in zip(a, b))
    out_2 = max(x * y for x, y in zip(a, b))
    return snippet, f"{out_1}\n{out_2}", "numpy"


def _pandas_puzzle_snippet(seed: int) -> tuple[str, str, str]:
    s1 = seed * 10
    s2 = seed * 10 + 5
    s3 = seed * 10 + 20
    snippet = (
        "import pandas as pd\n"
        f"df = pd.DataFrame({{'team': ['A','A','B'], 'score': [{s1}, {s2}, {s3}]}})\n"
        "res = df.groupby('team')['score'].mean().to_dict()\n"
        "print(res['A'])\n"
        "print(res['B'])"
    )
    out_a = (s1 + s2) / 2
    out_b = float(s3)
    return snippet, f"{out_a}\n{out_b}", "pandas"


async def seed_generated_puzzles(db: AsyncSession) -> int:
    """Insert a large generated puzzle set across categories."""
    inserted = 0
    generators = [
        ("python", "Py Arithmetic", _python_puzzle_snippet, 900),
        ("python", "Py Strings", _string_puzzle_snippet, 980),
        ("python", "Py Lists", _list_puzzle_snippet, 1040),
        ("numpy", "NumPy Vector", _numpy_puzzle_snippet, 1300),
        ("pandas", "Pandas Group", _pandas_puzzle_snippet, 1350),
        ("interview", "Interview Pattern", _interview_puzzle_snippet, 1400),
    ]

    for category, title_prefix, builder, base_elo in generators:
        for seed in range(1, 26):
            slug = f"{CURATED_SOURCE}-{category}-{title_prefix.lower().replace(' ', '-')}-{seed}"
            existing = await db.execute(select(Puzzle.id).where(Puzzle.slug == slug))
            if existing.scalar_one_or_none() is not None:
                continue

            code_snippet, correct_output, topic = builder(seed)
            difficulty = "easy" if seed <= 8 else "medium" if seed <= 17 else "hard"
            elo = _difficulty_elo(difficulty, (seed % 7) * 10) + (base_elo - 900)

            puzzle = Puzzle(
                title=f"{title_prefix} #{seed}",
                slug=slug,
                category=category,
                topic=topic,
                code_snippet=code_snippet,
                correct_output=correct_output,
                explanation="Analiza el flujo del codigo paso a paso y verifica cada print.",
                hint="Traza manualmente variables clave antes de responder.",
                elo_rating=elo,
                elo_initial=elo,
                is_advanced=elo >= 1450,
                is_active=True,
                source_book="Curated Open Practice Bank",
            )
            db.add(puzzle)
            inserted += 1

    if inserted:
        await db.commit()

    return inserted
