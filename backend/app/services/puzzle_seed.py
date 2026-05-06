"""
Initial puzzle seed data and seeding helpers for the ELO system.
"""

# flake8: noqa: E501 -- archivo de contenido curado: enunciados de puzzles ELO en espanol.

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.elo_models import Puzzle


CORE_PUZZLES = [
    {
        "title": "Hello World",
        "slug": "hello-world",
        "category": "python",
        "topic": "basics",
        "code_snippet": 'print("Hello World!")',
        "correct_output": "Hello World!",
        "explanation": "print() muestra el string en pantalla sin las comillas.",
        "hint": "Piensa en lo que hace print() con un string literal.",
        "elo_rating": 600,
        "elo_initial": 600,
        "source_book": "Coffee Break Python",
    },
    {
        "title": "Variables and Float Division",
        "slug": "variables-float-division",
        "category": "python",
        "topic": "variables",
        "code_snippet": "x = 55 / 11\nprint(x)",
        "correct_output": "5.0",
        "explanation": "En Python 3 el operador / siempre devuelve float.",
        "hint": "Que tipo devuelve / en Python 3: int o float?",
        "elo_rating": 625,
        "elo_initial": 625,
        "source_book": "Coffee Break Python",
    },
    {
        "title": "Integer Division",
        "slug": "integer-division",
        "category": "python",
        "topic": "arithmetic",
        "code_snippet": "print(13 // 4)\nprint(13 % 4)",
        "correct_output": "3\n1",
        "explanation": "// devuelve la division entera y % devuelve el residuo.",
        "hint": "Cuantas veces cabe 4 en 13 y cuanto sobra?",
        "elo_rating": 800,
        "elo_initial": 800,
        "source_book": "Coffee Break Python",
    },
    {
        "title": "List Indexing",
        "slug": "list-indexing",
        "category": "python",
        "topic": "lists",
        "code_snippet": "lst = [1, 2, 3, 4, 5]\nprint(lst[1])\nprint(lst[-1])",
        "correct_output": "2\n5",
        "explanation": "Los indices empiezan en 0 y -1 es el ultimo elemento.",
        "hint": "Python indexa desde 0. Que representa -1?",
        "elo_rating": 900,
        "elo_initial": 900,
        "source_book": "Coffee Break Python",
    },
    {
        "title": "For Loop",
        "slug": "for-loop",
        "category": "python",
        "topic": "loops",
        "code_snippet": "for i in range(3):\n    print(i * 2)",
        "correct_output": "0\n2\n4",
        "explanation": "range(3) produce 0, 1 y 2; luego cada valor se multiplica por 2.",
        "hint": "Enumera manualmente los valores de range(3).",
        "elo_rating": 1000,
        "elo_initial": 1000,
        "source_book": "Coffee Break Python",
    },
    {
        "title": "Default Arguments",
        "slug": "default-arguments",
        "category": "python",
        "topic": "functions",
        "code_snippet": "def greet(name, msg='Hello'):\n    print(msg, name)\n\ngreet('Alice')\ngreet('Bob', 'Hi')",
        "correct_output": "Hello Alice\nHi Bob",
        "explanation": "Si no se pasa msg, la funcion usa el valor por defecto Hello.",
        "hint": "Que parametro recibe un valor por defecto?",
        "elo_rating": 1200,
        "elo_initial": 1200,
        "source_book": "Coffee Break Python",
    },
    {
        "title": "Lambda Function",
        "slug": "lambda-function",
        "category": "python",
        "topic": "functions",
        "code_snippet": "square = lambda x: x ** 2\nprint(square(4))\nprint(square(3) + square(4))",
        "correct_output": "16\n25",
        "explanation": "square devuelve el cuadrado del numero; 3**2 + 4**2 es 25.",
        "hint": "Calcula primero square(3) y square(4).",
        "elo_rating": 1300,
        "elo_initial": 1300,
        "source_book": "Coffee Break Python",
    },
    {
        "title": "Boolean Indexing",
        "slug": "numpy-boolean-indexing",
        "category": "numpy",
        "topic": "indexing",
        "code_snippet": "import numpy as np\na = np.array([10, 20, 30, 40, 50])\nprint(a[a > 25])",
        "correct_output": "[30 40 50]",
        "explanation": "La expresion a > 25 crea una mascara booleana que filtra el array.",
        "hint": "Que elementos del array cumplen la condicion > 25?",
        "elo_rating": 1350,
        "elo_initial": 1350,
        "is_advanced": True,
        "source_book": "Coffee Break NumPy",
    },
]


INTERVIEW_PUZZLES = [
    {
        "title": "Two Sum Candidate",
        "slug": "interview-two-sum-candidate",
        "category": "interview",
        "topic": "arrays",
        "code_snippet": "nums = [2, 7, 11, 15]\ntarget = 9\nseen = {}\nfor i, n in enumerate(nums):\n    if target - n in seen:\n        print(seen[target - n], i)\n        break\n    seen[n] = i",
        "correct_output": "0 1",
        "explanation": "El complemento de 7 es 2, que ya estaba en el diccionario con indice 0.",
        "hint": "Piensa en complemento = target - n.",
        "elo_rating": 1450,
        "elo_initial": 1450,
        "is_advanced": True,
        "source_book": "Interview Patterns",
    },
    {
        "title": "Valid Parentheses",
        "slug": "interview-valid-parentheses",
        "category": "interview",
        "topic": "stacks",
        "code_snippet": "s = '([]{})'\nstack = []\npairs = {')': '(', ']': '[', '}': '{'}\nfor ch in s:\n    if ch in '([{':\n        stack.append(ch)\n    else:\n        if not stack or stack.pop() != pairs[ch]:\n            print(False)\n            break\nelse:\n    print(len(stack) == 0)",
        "correct_output": "True",
        "explanation": "Cada cierre coincide con el ultimo simbolo abierto.",
        "hint": "Usa una pila LIFO.",
        "elo_rating": 1500,
        "elo_initial": 1500,
        "is_advanced": True,
        "source_book": "Interview Patterns",
    },
    {
        "title": "Merge Intervals Count",
        "slug": "interview-merge-intervals-count",
        "category": "interview",
        "topic": "intervals",
        "code_snippet": "intervals = [[1,3],[2,6],[8,10],[15,18]]\nintervals.sort()\nmerged = [intervals[0]]\nfor start, end in intervals[1:]:\n    last = merged[-1]\n    if start <= last[1]:\n        last[1] = max(last[1], end)\n    else:\n        merged.append([start, end])\nprint(len(merged))",
        "correct_output": "3",
        "explanation": "Los dos primeros intervalos se fusionan, los otros dos quedan separados.",
        "hint": "Ordena por inicio antes de fusionar.",
        "elo_rating": 1550,
        "elo_initial": 1550,
        "is_advanced": True,
        "source_book": "Interview Patterns",
    },
    {
        "title": "Sliding Window Max Sum k=3",
        "slug": "interview-sliding-window-max-sum",
        "category": "interview",
        "topic": "sliding-window",
        "code_snippet": "nums = [2, 1, 5, 1, 3, 2]\nk = 3\nwindow = sum(nums[:k])\nbest = window\nfor i in range(k, len(nums)):\n    window += nums[i] - nums[i-k]\n    best = max(best, window)\nprint(best)",
        "correct_output": "9",
        "explanation": "La mejor ventana de longitud 3 es [5,1,3], suma 9.",
        "hint": "Actualiza la ventana restando el elemento que sale.",
        "elo_rating": 1500,
        "elo_initial": 1500,
        "is_advanced": True,
        "source_book": "Interview Patterns",
    },
    {
        "title": "Binary Search Mid Value",
        "slug": "interview-binary-search-mid-value",
        "category": "interview",
        "topic": "binary-search",
        "code_snippet": "arr = [1, 3, 5, 7, 9, 11, 13]\nleft, right = 0, len(arr)-1\nwhile left <= right:\n    mid = (left + right) // 2\n    if arr[mid] == 9:\n        print(mid)\n        break\n    if arr[mid] < 9:\n        left = mid + 1\n    else:\n        right = mid - 1",
        "correct_output": "4",
        "explanation": "El valor 9 esta en el indice 4.",
        "hint": "Busca el indice, no el valor.",
        "elo_rating": 1475,
        "elo_initial": 1475,
        "is_advanced": True,
        "source_book": "Interview Patterns",
    },
    {
        "title": "Pandas GroupBy Mean",
        "slug": "interview-pandas-groupby-mean",
        "category": "interview",
        "topic": "pandas",
        "code_snippet": "import pandas as pd\ndf = pd.DataFrame({'team':['A','A','B','B'],'score':[10,20,30,50]})\nres = df.groupby('team')['score'].mean().to_dict()\nprint(res['A'], res['B'])",
        "correct_output": "15.0 40.0",
        "explanation": "Promedio de A: (10+20)/2; promedio de B: (30+50)/2.",
        "hint": "groupby + mean por columna.",
        "elo_rating": 1600,
        "elo_initial": 1600,
        "is_advanced": True,
        "source_book": "Pandas Interview",
    },
    {
        "title": "NumPy Broadcast Sum",
        "slug": "interview-numpy-broadcast-sum",
        "category": "interview",
        "topic": "numpy",
        "code_snippet": "import numpy as np\na = np.array([[1],[2],[3]])\nb = np.array([10,20,30])\nprint((a + b).shape[0], (a + b).shape[1])",
        "correct_output": "3 3",
        "explanation": "Broadcasting expande a una matriz 3x3.",
        "hint": "Analiza dimensiones (3,1) + (3,).",
        "elo_rating": 1650,
        "elo_initial": 1650,
        "is_advanced": True,
        "source_book": "NumPy Interview",
    },
]


async def seed_puzzles_if_empty(db: AsyncSession) -> int:
    """Insert initial puzzles only when the table is empty."""
    result = await db.execute(select(Puzzle.id).limit(1))
    existing_id = result.scalar_one_or_none()
    if existing_id is not None:
        return 0

    for puzzle_data in CORE_PUZZLES:
        db.add(Puzzle(**puzzle_data))

    await db.commit()
    return len(CORE_PUZZLES)


async def seed_interview_puzzles(db: AsyncSession) -> int:
    """Insert interview puzzles that are missing by slug."""
    inserted = 0

    for puzzle_data in INTERVIEW_PUZZLES:
        existing = await db.execute(
            select(Puzzle.id).where(Puzzle.slug == puzzle_data["slug"])
        )
        if existing.scalar_one_or_none() is not None:
            continue
        db.add(Puzzle(**puzzle_data))
        inserted += 1

    if inserted:
        await db.commit()

    return inserted
