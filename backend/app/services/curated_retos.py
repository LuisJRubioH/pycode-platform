"""
Retos de programación curados (Pieza H).

Colección plana de 10 retos originales recreados a partir de los temas del
material externo de PARA_INTEGRAR (estilo MoureDev/Platzi) — reescritos, no
copiados — y orientados a rampar de Python base hacia Data Science / ML
(media móvil, IQR, min-max, one-hot, matriz de confusión, TF), acorde al
norte de la plataforma.

A diferencia de `seed_generated_challenges` (que explota plantillas en
3 dificultades × 3 variantes), aquí cada reto es único y autocontenido.

Se evalúan por auto-marcado (`/challenges/{id}/complete`); no hay grading
automático. Cada reto guarda una `reference_solution` correcta que el
endpoint de detalle NUNCA sirve (ver `CodingChallengeDetail`), reservada
para un futuro "ver solución".
"""

# flake8: noqa: E501 -- contenido curado: enunciados largos en español.

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import CodingChallenge

RETOS_SOURCE = "pycode-retos-curados"


@dataclass(frozen=True)
class CuratedReto:
    slug_suffix: str
    title: str
    difficulty: str  # easy | medium | hard
    topic: str
    prompt: str
    starter_code: str
    reference_solution: str


CURATED_RETOS: list[CuratedReto] = [
    CuratedReto(
        slug_suffix="fizzbuzz-lista",
        title="FizzBuzz como lista",
        difficulty="easy",
        topic="control-flow",
        prompt=(
            "Implementa `fizzbuzz(n)` que devuelva una lista con los números del 1 "
            "al `n` (inclusive) convertidos a `str`, salvo que:\n\n"
            "- los múltiplos de 3 se reemplazan por `'Fizz'`,\n"
            "- los múltiplos de 5 por `'Buzz'`,\n"
            "- los múltiplos de ambos (15) por `'FizzBuzz'`.\n\n"
            "Ejemplo: `fizzbuzz(5)` → `['1', '2', 'Fizz', '4', 'Buzz']`."
        ),
        starter_code="def fizzbuzz(n: int) -> list[str]:\n    # TODO\n    pass\n",
        reference_solution=(
            "def fizzbuzz(n: int) -> list[str]:\n"
            "    out = []\n"
            "    for i in range(1, n + 1):\n"
            "        if i % 15 == 0:\n"
            '            out.append("FizzBuzz")\n'
            "        elif i % 3 == 0:\n"
            '            out.append("Fizz")\n'
            "        elif i % 5 == 0:\n"
            '            out.append("Buzz")\n'
            "        else:\n"
            "            out.append(str(i))\n"
            "    return out\n"
        ),
    ),
    CuratedReto(
        slug_suffix="validador-password",
        title="Validador de contraseña",
        difficulty="easy",
        topic="strings",
        prompt=(
            "Implementa `es_segura(pwd)` que retorne `True` solo si la contraseña "
            "cumple TODO lo siguiente: al menos 8 caracteres, al menos una "
            "mayúscula, al menos una minúscula y al menos un dígito.\n\n"
            "Ejemplos: `es_segura('Abc12345')` → `True`; `es_segura('abc')` → `False`."
        ),
        starter_code="def es_segura(pwd: str) -> bool:\n    # TODO\n    pass\n",
        reference_solution=(
            "def es_segura(pwd: str) -> bool:\n"
            "    return (\n"
            "        len(pwd) >= 8\n"
            "        and any(c.isupper() for c in pwd)\n"
            "        and any(c.islower() for c in pwd)\n"
            "        and any(c.isdigit() for c in pwd)\n"
            "    )\n"
        ),
    ),
    CuratedReto(
        slug_suffix="conteo-palabras",
        title="Conteo de palabras",
        difficulty="easy",
        topic="dicts",
        prompt=(
            "Primer paso de cualquier pipeline de texto. Implementa "
            "`contar_palabras(texto)` que devuelva un `dict` `{palabra: frecuencia}`, "
            "pasando todo a minúsculas y separando por espacios.\n\n"
            "Ejemplo: `contar_palabras('hola Hola mundo')` → `{'hola': 2, 'mundo': 1}`."
        ),
        starter_code="def contar_palabras(texto: str) -> dict[str, int]:\n    # TODO\n    pass\n",
        reference_solution=(
            "def contar_palabras(texto: str) -> dict[str, int]:\n"
            "    conteo: dict[str, int] = {}\n"
            "    for palabra in texto.lower().split():\n"
            "        conteo[palabra] = conteo.get(palabra, 0) + 1\n"
            "    return conteo\n"
        ),
    ),
    CuratedReto(
        slug_suffix="media-movil",
        title="Media móvil",
        difficulty="medium",
        topic="series-temporales",
        prompt=(
            "Suaviza una serie temporal. Implementa `media_movil(serie, k)` que "
            "devuelva la lista de promedios de cada ventana contigua de tamaño `k`. "
            "Para una serie de largo `n` hay `n - k + 1` ventanas. Si `k` es <= 0 o "
            "mayor que el largo de la serie, devuelve `[]`.\n\n"
            "Ejemplo: `media_movil([1, 2, 3, 4], 2)` → `[1.5, 2.5, 3.5]`."
        ),
        starter_code="def media_movil(serie: list[float], k: int) -> list[float]:\n    # TODO\n    pass\n",
        reference_solution=(
            "def media_movil(serie: list[float], k: int) -> list[float]:\n"
            "    if k <= 0 or k > len(serie):\n"
            "        return []\n"
            "    return [\n"
            "        sum(serie[i:i + k]) / k\n"
            "        for i in range(len(serie) - k + 1)\n"
            "    ]\n"
        ),
    ),
    CuratedReto(
        slug_suffix="total-por-categoria",
        title="Total por categoría",
        difficulty="medium",
        topic="agregacion",
        prompt=(
            "Dada una lista de transacciones (cada una un `dict` con claves "
            "`'categoria'` y `'monto'`), implementa `total_por_categoria(transacciones)` "
            "que devuelva un `dict` `{categoria: suma_de_montos}`.\n\n"
            "Ejemplo: `total_por_categoria([{'categoria': 'a', 'monto': 10}, "
            "{'categoria': 'a', 'monto': 5}])` → `{'a': 15}`."
        ),
        starter_code="def total_por_categoria(transacciones: list[dict]) -> dict:\n    # TODO\n    pass\n",
        reference_solution=(
            "def total_por_categoria(transacciones: list[dict]) -> dict:\n"
            "    totales: dict = {}\n"
            "    for t in transacciones:\n"
            '        totales[t["categoria"]] = totales.get(t["categoria"], 0) + t["monto"]\n'
            "    return totales\n"
        ),
    ),
    CuratedReto(
        slug_suffix="outliers-iqr",
        title="Detección de outliers (IQR)",
        difficulty="medium",
        topic="estadistica",
        prompt=(
            "Implementa `outliers(datos)` que devuelva los valores fuera del rango "
            "`[Q1 - 1.5·IQR, Q3 + 1.5·IQR]`, donde `IQR = Q3 - Q1` y los cuartiles se "
            "calculan por interpolación lineal (como `numpy.percentile`). Conserva el "
            "orden original de los outliers.\n\n"
            "Ejemplo: `outliers([10, 12, 11, 13, 12, 100])` → `[100]`."
        ),
        starter_code="import numpy as np\n\n\ndef outliers(datos: list[float]) -> list[float]:\n    # TODO\n    pass\n",
        reference_solution=(
            "import numpy as np\n\n\n"
            "def outliers(datos: list[float]) -> list[float]:\n"
            "    q1, q3 = np.percentile(datos, [25, 75])\n"
            "    iqr = q3 - q1\n"
            "    bajo, alto = q1 - 1.5 * iqr, q3 + 1.5 * iqr\n"
            "    return [x for x in datos if x < bajo or x > alto]\n"
        ),
    ),
    CuratedReto(
        slug_suffix="normalizacion-minmax",
        title="Normalización min-max",
        difficulty="medium",
        topic="feature-scaling",
        prompt=(
            "Escala de features clásico en ML. Implementa `normaliza(valores)` que "
            "lleve la lista al rango `[0, 1]` con `(x - min) / (max - min)`. Si todos "
            "los valores son iguales, devuelve una lista de `0.0` del mismo largo.\n\n"
            "Ejemplo: `normaliza([10, 20, 30])` → `[0.0, 0.5, 1.0]`."
        ),
        starter_code="def normaliza(valores: list[float]) -> list[float]:\n    # TODO\n    pass\n",
        reference_solution=(
            "def normaliza(valores: list[float]) -> list[float]:\n"
            "    lo, hi = min(valores), max(valores)\n"
            "    if hi == lo:\n"
            "        return [0.0 for _ in valores]\n"
            "    return [(x - lo) / (hi - lo) for x in valores]\n"
        ),
    ),
    CuratedReto(
        slug_suffix="one-hot-encoding",
        title="One-hot encoding",
        difficulty="hard",
        topic="encoding",
        prompt=(
            "Codifica variables categóricas para un modelo. Implementa "
            "`one_hot(categorias)` que, dada una lista de etiquetas, devuelva una lista "
            "de vectores one-hot (listas de 0/1). Las columnas son las categorías "
            "únicas ordenadas alfabéticamente.\n\n"
            "Ejemplo: `one_hot(['rojo', 'verde', 'rojo'])` → `[[1, 0], [0, 1], [1, 0]]` "
            "(columnas: `['rojo', 'verde']`)."
        ),
        starter_code="def one_hot(categorias: list[str]) -> list[list[int]]:\n    # TODO\n    pass\n",
        reference_solution=(
            "def one_hot(categorias: list[str]) -> list[list[int]]:\n"
            "    clases = sorted(set(categorias))\n"
            "    indice = {c: i for i, c in enumerate(clases)}\n"
            "    out = []\n"
            "    for c in categorias:\n"
            "        fila = [0] * len(clases)\n"
            "        fila[indice[c]] = 1\n"
            "        out.append(fila)\n"
            "    return out\n"
        ),
    ),
    CuratedReto(
        slug_suffix="matriz-confusion",
        title="Matriz de confusión binaria",
        difficulty="hard",
        topic="ml-metrics",
        prompt=(
            "Base de toda métrica de clasificación. Implementa "
            "`matriz_confusion(y_true, y_pred)` para clasificación binaria (etiquetas "
            "`0`/`1`) que devuelva un `dict` con las claves `'tp'`, `'fp'`, `'fn'`, "
            "`'tn'`.\n\n"
            "Ejemplo: `matriz_confusion([1, 0, 1, 1], [1, 0, 0, 1])` → "
            "`{'tp': 2, 'fp': 0, 'fn': 1, 'tn': 1}`."
        ),
        starter_code="def matriz_confusion(y_true: list[int], y_pred: list[int]) -> dict:\n    # TODO\n    pass\n",
        reference_solution=(
            "def matriz_confusion(y_true: list[int], y_pred: list[int]) -> dict:\n"
            "    tp = fp = fn = tn = 0\n"
            "    for real, pred in zip(y_true, y_pred):\n"
            "        if real == 1 and pred == 1:\n"
            "            tp += 1\n"
            "        elif real == 0 and pred == 1:\n"
            "            fp += 1\n"
            "        elif real == 1 and pred == 0:\n"
            "            fn += 1\n"
            "        else:\n"
            "            tn += 1\n"
            '    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}\n'
        ),
    ),
    CuratedReto(
        slug_suffix="tf-term-frequency",
        title="Term Frequency (TF)",
        difficulty="hard",
        topic="nlp",
        prompt=(
            "Primer ingrediente de TF-IDF. Implementa `tf(documento)` que calcule la "
            "frecuencia de término normalizada: para cada palabra (en minúsculas, "
            "separadas por espacios), su conteo dividido por el total de palabras del "
            "documento. Devuelve un `dict` `{palabra: frecuencia}`.\n\n"
            "Ejemplo: `tf('a b a')` → `{'a': 0.6666666666666666, 'b': 0.3333333333333333}`."
        ),
        starter_code="def tf(documento: str) -> dict[str, float]:\n    # TODO\n    pass\n",
        reference_solution=(
            "def tf(documento: str) -> dict[str, float]:\n"
            "    palabras = documento.lower().split()\n"
            "    total = len(palabras)\n"
            "    conteo: dict[str, int] = {}\n"
            "    for p in palabras:\n"
            "        conteo[p] = conteo.get(p, 0) + 1\n"
            "    return {p: c / total for p, c in conteo.items()}\n"
        ),
    ),
]


async def seed_curated_retos(db: AsyncSession) -> int:
    """Inserta los retos curados que falten (idempotente por slug)."""
    max_order = await db.execute(select(func.max(CodingChallenge.order_index)))
    order_index = (max_order.scalar_one_or_none() or 0) + 1

    inserted = 0
    for reto in CURATED_RETOS:
        slug = f"{RETOS_SOURCE}-{reto.slug_suffix}"
        existing = await db.execute(
            select(CodingChallenge.id).where(CodingChallenge.slug == slug)
        )
        if existing.scalar_one_or_none() is not None:
            continue

        db.add(
            CodingChallenge(
                title=reto.title,
                slug=slug,
                source=RETOS_SOURCE,
                source_path=f"retos-curados/{reto.topic}/{reto.slug_suffix}.md",
                difficulty=reto.difficulty,
                topic=reto.topic,
                prompt=reto.prompt,
                starter_code=reto.starter_code,
                reference_solution=reto.reference_solution,
                order_index=order_index,
            )
        )
        order_index += 1
        inserted += 1

    if inserted:
        await db.commit()

    return inserted
