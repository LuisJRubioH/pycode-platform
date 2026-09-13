"""
Validacion de los retos: tests ocultos y soluciones de referencia.

Vive aparte de los enunciados (`generated_bank.py`, `curated_retos.py`) para
que se pueda revisar el contenido sin el ruido de los tests, y al reves.

Los tests siguen el formato de los ejercicios de las lecciones: cada uno se
ejecuta en Pyodide en un namespace nuevo, concatenado detras del codigo del
alumno; "no lanza" = aprobado. Dos guard rails los vigilan en CI
(`scripts/check_hidden_tests_triviales.py`):

- ningun test aprueba con el starter intacto;
- todos los tests aprueban con la solucion de referencia.

La solucion de referencia NUNCA sale por la API (ver `CodingChallengeDetail`).
"""

# flake8: noqa: E501 -- contenido: tests y soluciones con lineas largas.

from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent


def _t(nombre: str, codigo: str) -> dict:
    return {"name": nombre, "code": dedent(codigo).strip() + "\n"}


def _s(codigo: str) -> str:
    return dedent(codigo).lstrip("\n")


@dataclass(frozen=True)
class ValidacionReto:
    reference_solution: str
    hidden_tests: list[dict]


# (slug_base, dificultad) -> validacion de ese nivel
VALIDACION_GENERADOS: dict[tuple[str, str], ValidacionReto] = {
    # ------------------------------------------------------------------ strings
    ("strings-anagrama", "easy"): ValidacionReto(
        _s("""
            def son_anagramas(a: str, b: str) -> bool:
                return sorted(a.lower()) == sorted(b.lower())
        """),
        [
            _t(
                "detecta anagramas sin importar mayusculas",
                """
                assert son_anagramas('Roma', 'amor') is True
                assert son_anagramas('Listen', 'Silent') is True
            """,
            ),
            _t(
                "distingue los que no lo son",
                """
                assert son_anagramas('hola', 'hoja') is False
                assert son_anagramas('abc', 'abcc') is False, 'mismas letras pero distinta cantidad'
            """,
            ),
        ],
    ),
    ("strings-anagrama", "medium"): ValidacionReto(
        _s("""
            import unicodedata
            from collections import Counter


            def _limpia(texto):
                return Counter(
                    unicodedata.normalize('NFD', c)[0]
                    for c in texto.lower()
                    if not c.isspace()
                )


            def son_anagramas_frase(a: str, b: str) -> bool:
                return _limpia(a) == _limpia(b)
        """),
        [
            _t(
                "ignora espacios y tildes",
                """
                assert son_anagramas_frase('Mónica', 'Camión') is True
                assert son_anagramas_frase('La ropa', 'Parola') is True
            """,
            ),
            _t(
                "sigue distinguiendo cantidades",
                """
                assert son_anagramas_frase('sal', 'las s') is False
            """,
            ),
            _t(
                "quitar la tilde no borra la letra",
                """
                assert son_anagramas_frase('Cámara', 'cara') is False, 'la a con tilde sigue contando como a'
                assert son_anagramas_frase('Él', 'le') is True
            """,
            ),
        ],
    ),
    ("strings-anagrama", "hard"): ValidacionReto(
        _s("""
            import unicodedata


            def _clave(palabra):
                letras = (
                    unicodedata.normalize('NFD', c)[0]
                    for c in palabra.lower()
                    if c.isalnum()
                )
                return ''.join(sorted(letras))


            def agrupar_anagramas(palabras: list[str]) -> list[list[str]]:
                grupos = {}
                for p in palabras:
                    grupos.setdefault(_clave(p), []).append(p)
                return list(grupos.values())
        """),
        [
            _t(
                "agrupa en orden de aparicion",
                """
                obtenido = agrupar_anagramas(['Roma', 'amor', 'sol', 'mora', '¡los!'])
                assert obtenido == [['Roma', 'amor', 'mora'], ['sol', '¡los!']], f'devolvio {obtenido}'
            """,
            ),
            _t(
                "ignora tildes al comparar",
                """
                assert agrupar_anagramas(['camión', 'Mónica', 'mar']) == [['camión', 'Mónica'], ['mar']]
            """,
            ),
            _t(
                "una palabra sin pareja forma su propio grupo",
                """
                assert agrupar_anagramas(['uno']) == [['uno']]
                assert agrupar_anagramas([]) == []
            """,
            ),
        ],
    ),
    ("strings-palindromo", "easy"): ValidacionReto(
        _s("""
            def es_palindromo(texto: str) -> bool:
                t = texto.lower()
                return t == t[::-1]
        """),
        [
            _t(
                "reconoce palindromos con mayusculas",
                """
                assert es_palindromo('Ana') is True
                assert es_palindromo('Reconocer') is True
            """,
            ),
            _t(
                "rechaza los que no lo son",
                """
                assert es_palindromo('Hola') is False
            """,
            ),
        ],
    ),
    ("strings-palindromo", "medium"): ValidacionReto(
        _s("""
            def es_palindromo_frase(texto: str) -> bool:
                i, j = 0, len(texto) - 1
                while i < j:
                    if not texto[i].isalnum():
                        i += 1
                    elif not texto[j].isalnum():
                        j -= 1
                    elif texto[i].lower() != texto[j].lower():
                        return False
                    else:
                        i += 1
                        j -= 1
                return True
        """),
        [
            _t(
                "ignora espacios y signos",
                """
                assert es_palindromo_frase('Anita lava la tina.') is True
                assert es_palindromo_frase('Hola, aloh?') is True
            """,
            ),
            _t(
                "rechaza los que no lo son",
                """
                assert es_palindromo_frase('No es, no.') is False
            """,
            ),
            _t(
                "un texto sin letras cuenta como palindromo",
                """
                assert es_palindromo_frase('¡!') is True
            """,
            ),
        ],
    ),
    ("strings-palindromo", "hard"): ValidacionReto(
        _s("""
            import unicodedata


            def _base(c):
                return unicodedata.normalize('NFD', c)[0].lower()


            def es_palindromo_unicode(texto: str) -> bool:
                i, j = 0, len(texto) - 1
                while i < j:
                    if not texto[i].isalnum():
                        i += 1
                    elif not texto[j].isalnum():
                        j -= 1
                    elif _base(texto[i]) != _base(texto[j]):
                        return False
                    else:
                        i += 1
                        j -= 1
                return True
        """),
        [
            _t(
                "trata igual las letras con y sin tilde",
                """
                assert es_palindromo_unicode('¡Sé verlas al revés!') is True
                assert es_palindromo_unicode('Dábale arroz a la zorra el abad') is True
            """,
            ),
            _t(
                "rechaza los que no lo son",
                """
                assert es_palindromo_unicode('Árbol') is False
            """,
            ),
        ],
    ),
    # ------------------------------------------------------------------- arrays
    ("arrays-two-sum", "easy"): ValidacionReto(
        _s("""
            def two_sum(nums: list[int], target: int) -> tuple[int, int]:
                for i in range(len(nums)):
                    for j in range(i + 1, len(nums)):
                        if nums[i] + nums[j] == target:
                            return (i, j)
        """),
        [
            _t(
                "encuentra la pareja",
                """
                assert two_sum([2, 7, 11, 15], 9) == (0, 1)
                assert two_sum([3, 2, 4], 6) == (1, 2)
            """,
            ),
            _t(
                "no usa dos veces el mismo elemento",
                """
                assert two_sum([3, 3], 6) == (0, 1), 'dos posiciones distintas'
                assert two_sum([4, 1, 4], 8) == (0, 2), 'el 4 de la posicion 0 no puede sumarse consigo mismo'
            """,
            ),
        ],
    ),
    ("arrays-two-sum", "medium"): ValidacionReto(
        _s("""
            def two_sum_rapido(nums: list[int], target: int):
                vistos = {}
                for j, x in enumerate(nums):
                    if target - x in vistos:
                        return (vistos[target - x], j)
                    vistos.setdefault(x, j)
                return None
        """),
        [
            _t(
                "encuentra la pareja",
                """
                assert two_sum_rapido([3, 2, 4], 6) == (1, 2)
                assert two_sum_rapido([3, 3], 6) == (0, 1)
            """,
            ),
            _t(
                "devuelve None si no hay pareja",
                """
                assert two_sum_rapido([1, 9], 10) == (0, 1), 'primero tiene que encontrar las que si existen'
                assert two_sum_rapido([1, 2], 10) is None
            """,
            ),
            _t(
                "con varias parejas, la del j mas pequeno",
                """
                assert two_sum_rapido([1, 3, 2, 2], 4) == (0, 1)
            """,
            ),
            _t(
                "es lineal: resuelve 200.000 numeros al instante",
                """
                import time
                nums = list(range(200_000))
                t0 = time.perf_counter()
                assert two_sum_rapido(nums, 399_997) == (199_998, 199_999)
                assert time.perf_counter() - t0 < 2, 'demasiado lento: usa un diccionario'
            """,
            ),
        ],
    ),
    ("arrays-two-sum", "hard"): ValidacionReto(
        _s("""
            def two_sum_todos(nums: list[int], target: int) -> list[tuple[int, int]]:
                indices = {}
                parejas = []
                for j, x in enumerate(nums):
                    for i in indices.get(target - x, []):
                        parejas.append((i, j))
                    indices.setdefault(x, []).append(j)
                return sorted(parejas)
        """),
        [
            _t(
                "todas las parejas, ordenadas",
                """
                obtenido = two_sum_todos([1, 5, 3, 3, 1], 4)
                assert obtenido == [(0, 2), (0, 3), (2, 4), (3, 4)], f'devolvio {obtenido}'
            """,
            ),
            _t(
                "sin parejas devuelve lista vacia",
                """
                assert two_sum_todos([1, 2, 3], 100) == []
            """,
            ),
            _t(
                "no empareja un indice consigo mismo",
                """
                assert two_sum_todos([2, 2, 2], 4) == [(0, 1), (0, 2), (1, 2)]
            """,
            ),
        ],
    ),
    ("arrays-rotacion", "easy"): ValidacionReto(
        _s("""
            def rotar(nums: list[int], k: int) -> list[int]:
                if not nums:
                    return []
                k %= len(nums)
                return nums[-k:] + nums[:-k] if k else list(nums)
        """),
        [
            _t(
                "rota a la derecha",
                """
                assert rotar([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
            """,
            ),
            _t(
                "k mayor que el largo da la vuelta",
                """
                assert rotar([1, 2, 3], 4) == [3, 1, 2]
                assert rotar([1, 2, 3], 3) == [1, 2, 3]
            """,
            ),
            _t(
                "devuelve una lista nueva sin tocar la original",
                """
                original = [1, 2, 3]
                nueva = rotar(original, 1)
                assert nueva == [3, 1, 2]
                assert original == [1, 2, 3], 'modificaste la lista original'
            """,
            ),
        ],
    ),
    ("arrays-rotacion", "medium"): ValidacionReto(
        _s("""
            def _invertir(nums, i, j):
                while i < j:
                    nums[i], nums[j] = nums[j], nums[i]
                    i += 1
                    j -= 1


            def rotar_en_sitio(nums: list[int], k: int) -> None:
                if not nums:
                    return None
                k %= len(nums)
                _invertir(nums, 0, len(nums) - 1)
                _invertir(nums, 0, k - 1)
                _invertir(nums, k, len(nums) - 1)
                return None
        """),
        [
            _t(
                "rota el mismo objeto",
                """
                nums = [1, 2, 3, 4, 5]
                mismo = nums
                resultado = rotar_en_sitio(nums, 2)
                assert nums == [4, 5, 1, 2, 3], f'nums quedo {nums}'
                assert nums is mismo
                assert resultado is None, 'en sitio: devuelve None'
            """,
            ),
            _t(
                "k mayor que el largo",
                """
                nums = [1, 2, 3]
                rotar_en_sitio(nums, 5)
                assert nums == [2, 3, 1]
            """,
            ),
        ],
    ),
    ("arrays-rotacion", "hard"): ValidacionReto(
        _s("""
            def rotar_segmento(nums: list[int], k: int, inicio: int, fin: int) -> None:
                if not (0 <= inicio <= fin < len(nums)):
                    raise ValueError('segmento fuera de la lista')
                largo = fin - inicio + 1
                k %= largo
                if k:
                    nums[inicio:fin + 1] = nums[fin + 1 - k:fin + 1] + nums[inicio:fin + 1 - k]
        """),
        [
            _t(
                "rota solo el tramo",
                """
                nums = [1, 2, 3, 4, 5, 6]
                rotar_segmento(nums, 1, 1, 4)
                assert nums == [1, 5, 2, 3, 4, 6], f'nums quedo {nums}'
            """,
            ),
            _t(
                "k mayor que el tramo",
                """
                nums = [0, 1, 2, 3, 9]
                rotar_segmento(nums, 4, 1, 3)
                assert nums == [0, 3, 1, 2, 9]
            """,
            ),
            _t(
                "indices invalidos lanzan ValueError sin tocar nada",
                """
                nums = [1, 2, 3]
                for inicio, fin in ((2, 1), (-1, 1), (0, 3)):
                    try:
                        rotar_segmento(nums, 1, inicio, fin)
                    except ValueError:
                        pass
                    else:
                        raise AssertionError(f'({inicio}, {fin}) deberia lanzar ValueError')
                assert nums == [1, 2, 3]
            """,
            ),
        ],
    ),
    # -------------------------------------------------------------------- dicts
    ("dicts-frecuencia", "easy"): ValidacionReto(
        _s("""
            def contar_tokens(texto: str) -> dict[str, int]:
                conteo = {}
                for token in texto.split():
                    conteo[token] = conteo.get(token, 0) + 1
                return conteo
        """),
        [
            _t(
                "cuenta cada token",
                """
                assert contar_tokens('el gato y el perro') == {'el': 2, 'gato': 1, 'y': 1, 'perro': 1}
            """,
            ),
            _t(
                "distingue mayusculas y aguanta texto vacio",
                """
                assert contar_tokens('Hola hola') == {'Hola': 1, 'hola': 1}
                assert contar_tokens('') == {}
            """,
            ),
        ],
    ),
    ("dicts-frecuencia", "medium"): ValidacionReto(
        _s("""
            import re


            def contar_tokens_limpios(texto: str) -> dict[str, int]:
                conteo = {}
                for token in re.sub(r'[.,;:!?¡¿]', '', texto.lower()).split():
                    conteo[token] = conteo.get(token, 0) + 1
                return conteo
        """),
        [
            _t(
                "minusculas y sin signos",
                """
                obtenido = contar_tokens_limpios('Hola, hola. ¿Qué tal?')
                assert obtenido == {'hola': 2, 'qué': 1, 'tal': 1}, f'devolvio {obtenido}'
            """,
            ),
            _t(
                "los signos pegados no crean tokens distintos",
                """
                assert contar_tokens_limpios('¡Si! si; SI:') == {'si': 3}
            """,
            ),
        ],
    ),
    ("dicts-frecuencia", "hard"): ValidacionReto(
        _s("""
            import re
            from collections import Counter


            def top_k_tokens(texto: str, k: int) -> list[tuple[str, int]]:
                tokens = re.sub(r'[.,;:!?¡¿]', '', texto.lower()).split()
                return sorted(Counter(tokens).items(), key=lambda par: (-par[1], par[0]))[:k]
        """),
        [
            _t(
                "desempata alfabeticamente",
                """
                assert top_k_tokens('b a c b a d', 2) == [('a', 2), ('b', 2)]
            """,
            ),
            _t(
                "limpia antes de contar",
                """
                assert top_k_tokens('Sol, sol. Luna', 1) == [('sol', 2)]
            """,
            ),
            _t(
                "k mayor que los tokens devuelve todos",
                """
                assert top_k_tokens('x y', 5) == [('x', 1), ('y', 1)]
            """,
            ),
        ],
    ),
    # --------------------------------------------------------------------- sets
    ("sets-diferencia", "easy"): ValidacionReto(
        _s("""
            def faltantes(requeridos: set[str], presentes: set[str]) -> set[str]:
                return requeridos - presentes
        """),
        [
            _t(
                "devuelve lo que falta",
                """
                assert faltantes({'casco', 'guantes', 'botas'}, {'guantes'}) == {'casco', 'botas'}
            """,
            ),
            _t(
                "sin faltantes, conjunto vacio",
                """
                assert faltantes({'a'}, {'a', 'b'}) == set()
            """,
            ),
        ],
    ),
    ("sets-diferencia", "medium"): ValidacionReto(
        _s("""
            def delta_inventario(antes: set[str], despues: set[str]) -> dict[str, set[str]]:
                return {'agregados': despues - antes, 'removidos': antes - despues}
        """),
        [
            _t(
                "agregados y removidos",
                """
                assert delta_inventario({'a', 'b'}, {'b', 'c'}) == {'agregados': {'c'}, 'removidos': {'a'}}
            """,
            ),
            _t(
                "sin cambios, dos conjuntos vacios",
                """
                assert delta_inventario({'x'}, {'x'}) == {'agregados': set(), 'removidos': set()}
            """,
            ),
        ],
    ),
    ("sets-diferencia", "hard"): ValidacionReto(
        _s("""
            from collections import Counter


            def diferencias_con_conteo(antes: list[str], despues: list[str]) -> dict[str, int]:
                cambio = Counter(despues)
                cambio.subtract(Counter(antes))
                return {articulo: n for articulo, n in cambio.items() if n != 0}
        """),
        [
            _t(
                "cuenta los cambios con repetidos",
                """
                obtenido = diferencias_con_conteo(['tornillo', 'tornillo', 'tuerca'], ['tornillo', 'clavo'])
                assert obtenido == {'tornillo': -1, 'tuerca': -1, 'clavo': 1}, f'devolvio {obtenido}'
            """,
            ),
            _t(
                "omite los que no cambian",
                """
                assert diferencias_con_conteo(['a', 'b'], ['b', 'a']) == {}
            """,
            ),
        ],
    ),
    # ------------------------------------------------------------------ sorting
    ("sorting-custom", "easy"): ValidacionReto(
        _s("""
            def ordenar_por_edad(personas):
                return sorted(personas, key=lambda p: p[1])
        """),
        [
            _t(
                "ordena por edad",
                """
                assert ordenar_por_edad([('Ana', 30), ('Beto', 25), ('Cris', 40)]) == [('Beto', 25), ('Ana', 30), ('Cris', 40)]
            """,
            ),
            _t(
                "devuelve una lista nueva",
                """
                original = [('Ana', 30), ('Beto', 25)]
                nueva = ordenar_por_edad(original)
                assert nueva == [('Beto', 25), ('Ana', 30)] and nueva is not original, 'tiene que devolver una lista nueva ordenada'
                assert original == [('Ana', 30), ('Beto', 25)], 'modificaste la lista original'
            """,
            ),
        ],
    ),
    ("sorting-custom", "medium"): ValidacionReto(
        _s("""
            def ordenar_empleados(empleados):
                return sorted(empleados, key=lambda e: (-e['salario'], e['nombre']))
        """),
        [
            _t(
                "salario desc y nombre asc en empate",
                """
                obtenido = ordenar_empleados([
                    {'nombre': 'Luz', 'salario': 900},
                    {'nombre': 'Ana', 'salario': 900},
                    {'nombre': 'Eva', 'salario': 1200},
                ])
                assert [e['nombre'] for e in obtenido] == ['Eva', 'Ana', 'Luz'], f'orden {[e["nombre"] for e in obtenido]}'
            """,
            ),
        ],
    ),
    ("sorting-custom", "hard"): ValidacionReto(
        _s("""
            def ordenar_por_campos(registros, campos):
                resultado = list(registros)
                for campo, sentido in reversed(campos):
                    resultado.sort(key=lambda r: r[campo], reverse=(sentido == 'desc'))
                return resultado
        """),
        [
            _t(
                "mezcla asc y desc con textos",
                """
                regs = [
                    {'ciudad': 'Lima', 'edad': 30, 'nombre': 'a'},
                    {'ciudad': 'Cusco', 'edad': 25, 'nombre': 'b'},
                    {'ciudad': 'Lima', 'edad': 41, 'nombre': 'c'},
                    {'ciudad': 'Cusco', 'edad': 33, 'nombre': 'd'},
                ]
                obtenido = ordenar_por_campos(regs, [('ciudad', 'asc'), ('edad', 'desc')])
                assert [r['nombre'] for r in obtenido] == ['d', 'b', 'c', 'a'], f'orden {[r["nombre"] for r in obtenido]}'
            """,
            ),
            _t(
                "texto descendente como prioridad",
                """
                regs = [{'n': 'b', 'x': 1}, {'n': 'a', 'x': 2}, {'n': 'b', 'x': 0}]
                obtenido = ordenar_por_campos(regs, [('n', 'desc'), ('x', 'asc')])
                assert obtenido == [{'n': 'b', 'x': 0}, {'n': 'b', 'x': 1}, {'n': 'a', 'x': 2}]
            """,
            ),
            _t(
                "no toca la lista original",
                """
                regs = [{'n': 2}, {'n': 1}]
                nueva = ordenar_por_campos(regs, [('n', 'asc')])
                assert nueva == [{'n': 1}, {'n': 2}], 'tiene que devolver la lista ordenada'
                assert regs == [{'n': 2}, {'n': 1}]
            """,
            ),
        ],
    ),
    # ------------------------------------------------------------------- search
    ("search-binary", "easy"): ValidacionReto(
        _s("""
            def binary_search(nums: list[int], target: int) -> int:
                lo, hi = 0, len(nums) - 1
                while lo <= hi:
                    mid = (lo + hi) // 2
                    if nums[mid] == target:
                        return mid
                    if nums[mid] < target:
                        lo = mid + 1
                    else:
                        hi = mid - 1
                return -1
        """),
        [
            _t(
                "encuentra el indice",
                """
                assert binary_search([1, 3, 5, 7, 9], 7) == 3
                assert binary_search([1, 3, 5, 7, 9], 1) == 0
            """,
            ),
            _t(
                "devuelve -1 si no esta",
                """
                assert binary_search([1, 3, 5], 4) == -1
                assert binary_search([], 4) == -1
            """,
            ),
        ],
    ),
    ("search-binary", "medium"): ValidacionReto(
        _s("""
            def primera_ocurrencia(nums: list[int], target: int) -> int:
                lo, hi, res = 0, len(nums) - 1, -1
                while lo <= hi:
                    mid = (lo + hi) // 2
                    if nums[mid] >= target:
                        if nums[mid] == target:
                            res = mid
                        hi = mid - 1
                    else:
                        lo = mid + 1
                return res
        """),
        [
            _t(
                "la primera de varias",
                """
                assert primera_ocurrencia([1, 2, 2, 2, 3], 2) == 1
                assert primera_ocurrencia([2, 2, 2], 2) == 0
            """,
            ),
            _t(
                "-1 si no esta",
                """
                assert primera_ocurrencia([1, 3], 2) == -1
            """,
            ),
        ],
    ),
    ("search-binary", "hard"): ValidacionReto(
        _s("""
            def _borde(nums, target, izquierda):
                lo, hi, res = 0, len(nums) - 1, -1
                while lo <= hi:
                    mid = (lo + hi) // 2
                    if nums[mid] == target:
                        res = mid
                        if izquierda:
                            hi = mid - 1
                        else:
                            lo = mid + 1
                    elif nums[mid] < target:
                        lo = mid + 1
                    else:
                        hi = mid - 1
                return res


            def rango_ocurrencias(nums: list[int], target: int) -> list[int]:
                return [_borde(nums, target, True), _borde(nums, target, False)]
        """),
        [
            _t(
                "primera y ultima posicion",
                """
                assert rango_ocurrencias([5, 7, 7, 8, 8, 10], 8) == [3, 4]
                assert rango_ocurrencias([5, 7, 7, 8, 8, 10], 10) == [5, 5]
            """,
            ),
            _t(
                "[-1, -1] si no esta",
                """
                assert rango_ocurrencias([5, 7], 6) == [-1, -1]
                assert rango_ocurrencias([], 6) == [-1, -1]
            """,
            ),
        ],
    ),
    # ---------------------------------------------------------------- recursion
    ("recursion-factorial", "easy"): ValidacionReto(
        _s("""
            def factorial(n: int) -> int:
                return 1 if n == 0 else n * factorial(n - 1)
        """),
        [
            _t(
                "calcula el factorial",
                """
                assert factorial(5) == 120
                assert factorial(1) == 1
            """,
            ),
            _t(
                "el caso base es 0! = 1",
                """
                assert factorial(0) == 1
            """,
            ),
        ],
    ),
    ("recursion-factorial", "medium"): ValidacionReto(
        _s("""
            def factorial_iterativo(n: int) -> int:
                if n < 0:
                    raise ValueError('n no puede ser negativo')
                resultado = 1
                for i in range(2, n + 1):
                    resultado *= i
                return resultado
        """),
        [
            _t(
                "calcula el factorial",
                """
                assert factorial_iterativo(5) == 120
                assert factorial_iterativo(0) == 1
            """,
            ),
            _t(
                "aguanta n grande sin recursion",
                """
                import math
                assert factorial_iterativo(3000) == math.factorial(3000)
            """,
            ),
            _t(
                "negativo lanza ValueError",
                """
                try:
                    factorial_iterativo(-1)
                except ValueError:
                    pass
                else:
                    raise AssertionError('factorial_iterativo(-1) deberia lanzar ValueError')
            """,
            ),
        ],
    ),
    ("recursion-factorial", "hard"): ValidacionReto(
        _s("""
            def factoriales(consultas: list[int]) -> list[int]:
                if not consultas:
                    return []
                tabla = [1]
                for i in range(1, max(consultas) + 1):
                    tabla.append(tabla[-1] * i)
                return [tabla[n] for n in consultas]
        """),
        [
            _t(
                "mismo orden, con repetidos",
                """
                assert factoriales([5, 3, 6, 3]) == [120, 6, 720, 6]
            """,
            ),
            _t(
                "lista vacia",
                """
                assert factoriales([]) == []
            """,
            ),
            _t(
                "miles de consultas sin recalcular",
                """
                import math, time
                consultas = list(range(2000, 0, -1)) * 3
                t0 = time.perf_counter()
                obtenido = factoriales(consultas)
                assert obtenido[0] == math.factorial(2000) and obtenido[-1] == 1
                assert time.perf_counter() - t0 < 3, 'demasiado lento: reutiliza los factoriales ya calculados'
            """,
            ),
        ],
    ),
    ("recursion-fibonacci", "easy"): ValidacionReto(
        _s("""
            def fib(n: int) -> int:
                a, b = 0, 1
                for _ in range(n):
                    a, b = b, a + b
                return a
        """),
        [
            _t(
                "valores conocidos",
                """
                assert [fib(i) for i in range(8)] == [0, 1, 1, 2, 3, 5, 8, 13]
                assert fib(10) == 55
            """,
            ),
        ],
    ),
    ("recursion-fibonacci", "medium"): ValidacionReto(
        _s("""
            from functools import lru_cache


            @lru_cache(maxsize=None)
            def _fib(n):
                return n if n < 2 else _fib(n - 1) + _fib(n - 2)


            def fib_memo(n: int) -> int:
                if n < 0:
                    raise ValueError('n no puede ser negativo')
                return _fib(n)
        """),
        [
            _t(
                "rapido gracias a la memoria",
                """
                assert fib_memo(80) == 23416728348467685
            """,
            ),
            _t(
                "negativo lanza ValueError",
                """
                try:
                    fib_memo(-3)
                except ValueError:
                    pass
                else:
                    raise AssertionError('fib_memo(-3) deberia lanzar ValueError')
            """,
            ),
        ],
    ),
    ("recursion-fibonacci", "hard"): ValidacionReto(
        _s("""
            def _doubling(n):
                if n == 0:
                    return (0, 1)
                a, b = _doubling(n >> 1)
                c = a * (2 * b - a)
                d = a * a + b * b
                return (d, c + d) if n & 1 else (c, d)


            def fib_rapido(n: int) -> int:
                return _doubling(n)[0]
        """),
        [
            _t(
                "valores conocidos",
                """
                assert fib_rapido(0) == 0 and fib_rapido(1) == 1
                assert fib_rapido(100) == 354224848179261915075
            """,
            ),
            _t(
                "n muy grande en poco tiempo",
                """
                import time
                t0 = time.perf_counter()
                valor = fib_rapido(100_000)
                assert time.perf_counter() - t0 < 2, 'demasiado lento: usa fast doubling'
                # Sin str(): Python no convierte a texto enteros de mas de 4300 digitos.
                assert valor % 10**20 == 49895374653428746875, 'valor incorrecto'
                assert 10**20898 <= valor < 10**20899, 'valor incorrecto: deberia tener 20899 digitos'
            """,
            ),
        ],
    ),
    # ------------------------------------------------------------ sliding-window
    ("window-max-sum", "easy"): ValidacionReto(
        _s("""
            def max_suma_ventana(nums: list[int], k: int) -> int:
                return max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1))
        """),
        [
            _t(
                "mayor suma de k seguidos",
                """
                assert max_suma_ventana([2, 1, 5, 1, 3, 2], 3) == 9
                assert max_suma_ventana([4, -1, 2], 1) == 4
            """,
            ),
            _t(
                "funciona con negativos",
                """
                assert max_suma_ventana([-5, -2, -3], 2) == -5
            """,
            ),
        ],
    ),
    ("window-max-sum", "medium"): ValidacionReto(
        _s("""
            def mejor_ventana(nums: list[int], k: int) -> tuple[int, int, int]:
                suma = sum(nums[:k])
                mejor = (suma, 0, k - 1)
                for i in range(k, len(nums)):
                    suma += nums[i] - nums[i - k]
                    if suma > mejor[0]:
                        mejor = (suma, i - k + 1, i)
                return mejor
        """),
        [
            _t(
                "suma e indices",
                """
                assert mejor_ventana([2, 1, 5, 1, 3, 2], 3) == (9, 2, 4)
            """,
            ),
            _t(
                "en empate, la primera",
                """
                assert mejor_ventana([1, 2, 1, 2], 2) == (3, 0, 1)
            """,
            ),
            _t(
                "lineal con listas grandes",
                """
                import time
                nums = list(range(300_000))
                t0 = time.perf_counter()
                assert mejor_ventana(nums, 1000)[1] == 299_000
                assert time.perf_counter() - t0 < 3, 'demasiado lento: no vuelvas a sumar la ventana entera'
            """,
            ),
        ],
    ),
    ("window-max-sum", "hard"): ValidacionReto(
        _s("""
            def ventana_minima(nums: list[int], umbral: int) -> int:
                i = suma = 0
                mejor = 0
                for j, x in enumerate(nums):
                    suma += x
                    while suma >= umbral:
                        largo = j - i + 1
                        mejor = largo if mejor == 0 else min(mejor, largo)
                        suma -= nums[i]
                        i += 1
                return mejor
        """),
        [
            _t(
                "el tramo mas corto",
                """
                assert ventana_minima([2, 3, 1, 2, 4, 3], 7) == 2
                assert ventana_minima([1, 4, 4], 4) == 1
            """,
            ),
            _t(
                "0 si ningun tramo llega",
                """
                assert ventana_minima([1, 1, 1], 10) == 0
            """,
            ),
        ],
    ),
    # ------------------------------------------------------------------- stacks
    ("stack-parentesis", "easy"): ValidacionReto(
        _s("""
            def balanceado(texto: str) -> bool:
                abiertos = 0
                for c in texto:
                    if c == '(':
                        abiertos += 1
                    elif c == ')':
                        abiertos -= 1
                        if abiertos < 0:
                            return False
                return abiertos == 0
        """),
        [
            _t(
                "reconoce los balanceados",
                """
                assert balanceado('(())()') is True
                assert balanceado('') is True
            """,
            ),
            _t(
                "rechaza aperturas sin cerrar y cierres de mas",
                """
                assert balanceado('(()') is False
                assert balanceado(')(') is False, 'mismo numero pero en mal orden'
            """,
            ),
        ],
    ),
    ("stack-parentesis", "medium"): ValidacionReto(
        _s("""
            def balanceado_mixto(texto: str) -> bool:
                pares = {')': '(', ']': '[', '}': '{'}
                pila = []
                for c in texto:
                    if c in '([{':
                        pila.append(c)
                    elif c in pares:
                        if not pila or pila.pop() != pares[c]:
                            return False
                return not pila
        """),
        [
            _t(
                "tres tipos e ignora el resto",
                """
                assert balanceado_mixto('{[a(b)]}') is True
            """,
            ),
            _t(
                "cruzados no valen",
                """
                assert balanceado_mixto('([)]') is False
                assert balanceado_mixto('((') is False
                assert balanceado_mixto(']') is False
            """,
            ),
        ],
    ),
    ("stack-parentesis", "hard"): ValidacionReto(
        _s("""
            def primer_error(texto: str) -> int:
                pares = {')': '(', ']': '[', '}': '{'}
                pila = []
                for i, c in enumerate(texto):
                    if c in '([{':
                        pila.append((c, i))
                    elif c in pares:
                        if not pila or pila[-1][0] != pares[c]:
                            return i
                        pila.pop()
                return pila[0][1] if pila else -1
        """),
        [
            _t(
                "cierre que no corresponde",
                """
                assert primer_error('(a[b)c]') == 4
                assert primer_error('x)') == 1
            """,
            ),
            _t(
                "aperturas sin cerrar: la primera",
                """
                assert primer_error('((x)') == 0
                assert primer_error('ok[(') == 2
            """,
            ),
            _t(
                "todo bien, -1",
                """
                assert primer_error('(ok)') == -1
            """,
            ),
        ],
    ),
    # ------------------------------------------------------------------- queues
    ("queue-scheduler", "easy"): ValidacionReto(
        _s("""
            from collections import deque


            def simular_cola(operaciones: list[tuple]) -> list[str]:
                cola = deque()
                salidas = []
                for op in operaciones:
                    if op[0] == 'entra':
                        cola.append(op[1])
                    elif cola:
                        salidas.append(cola.popleft())
                return salidas
        """),
        [
            _t(
                "sale en orden de llegada",
                """
                ops = [('entra', 'Ana'), ('entra', 'Beto'), ('sale',), ('entra', 'Cris'), ('sale',), ('sale',)]
                assert simular_cola(ops) == ['Ana', 'Beto', 'Cris']
            """,
            ),
            _t(
                "sacar de una cola vacia no hace nada",
                """
                assert simular_cola([('sale',), ('entra', 'A'), ('sale',), ('sale',)]) == ['A']
            """,
            ),
        ],
    ),
    ("queue-scheduler", "medium"): ValidacionReto(
        _s("""
            import heapq


            def simular_cola_prioridad(operaciones: list[tuple]) -> list[str]:
                heap = []
                llegada = 0
                salidas = []
                for op in operaciones:
                    if op[0] == 'entra':
                        heapq.heappush(heap, (op[2], llegada, op[1]))
                        llegada += 1
                    elif heap:
                        salidas.append(heapq.heappop(heap)[2])
                return salidas
        """),
        [
            _t(
                "prioridad mas baja primero y FIFO en empate",
                """
                ops = [('entra', 'A', 2), ('entra', 'B', 1), ('entra', 'C', 2), ('sale',), ('sale',), ('sale',)]
                assert simular_cola_prioridad(ops) == ['B', 'A', 'C']
            """,
            ),
            _t(
                "sacar de vacia no hace nada",
                """
                assert simular_cola_prioridad([('sale',)]) == []
            """,
            ),
        ],
    ),
    ("queue-scheduler", "hard"): ValidacionReto(
        _s("""
            from collections import deque


            def round_robin(procesos, quantum):
                cola = deque(procesos)
                duracion = dict(procesos)
                t = 0
                fin = {}
                while cola:
                    nombre, resta = cola.popleft()
                    uso = min(quantum, resta)
                    t += uso
                    if resta > uso:
                        cola.append((nombre, resta - uso))
                    else:
                        fin[nombre] = t
                return {nombre: fin[nombre] - duracion[nombre] for nombre in duracion}
        """),
        [
            _t(
                "tiempos de espera del ejemplo",
                """
                assert round_robin([('A', 5), ('B', 3)], 2) == {'A': 3, 'B': 4}
            """,
            ),
            _t(
                "quantum grande es FIFO",
                """
                assert round_robin([('A', 2), ('B', 3), ('C', 1)], 10) == {'A': 0, 'B': 2, 'C': 5}
            """,
            ),
        ],
    ),
    # -------------------------------------------------------------------- regex
    ("regex-validacion", "easy"): ValidacionReto(
        _s("""
            import re


            def es_correo(valor: str) -> bool:
                return re.fullmatch(r'[^\\s@]+@[^\\s@.]+(\\.[^\\s@.]+)*\\.[A-Za-z]{2,}', valor) is not None
        """),
        [
            _t(
                "acepta correos simples",
                """
                assert es_correo('ana@mail.com') is True
                assert es_correo('ana.lopez@correo.edu.pe') is True
            """,
            ),
            _t(
                "rechaza los invalidos",
                """
                for malo in ('ana@mail', 'ana lopez@mail.com', 'ana@@mail.com', '@mail.com', 'ana@mail.c'):
                    assert es_correo(malo) is False, f'{malo!r} no es un correo valido'
            """,
            ),
        ],
    ),
    ("regex-validacion", "medium"): ValidacionReto(
        _s("""
            import re


            def extraer_hashtags(texto: str) -> list[str]:
                return re.findall(r'(?<![\\w#])#([A-Za-z][A-Za-z0-9_]*)', texto)
        """),
        [
            _t(
                "extrae los validos en orden",
                """
                assert extraer_hashtags('Aprendo #Python y #ML_101, no #123') == ['Python', 'ML_101']
            """,
            ),
            _t(
                "sin hashtags, lista vacia",
                """
                assert extraer_hashtags('nada que ver # aqui') == []
            """,
            ),
        ],
    ),
    ("regex-validacion", "hard"): ValidacionReto(
        _s("""
            import re

            _PATRON = re.compile(r'(?P<categoria>[A-Z]{3})-(?P<fecha>\\d{4}-\\d{2}-\\d{2})-(?P<numero>\\d{4})')


            def parsear_codigo(valor: str):
                m = _PATRON.fullmatch(valor)
                if m is None:
                    return None
                return {'categoria': m['categoria'], 'fecha': m['fecha'], 'numero': int(m['numero'])}
        """),
        [
            _t(
                "descompone el codigo",
                """
                assert parsear_codigo('PRD-2026-06-14-0042') == {'categoria': 'PRD', 'fecha': '2026-06-14', 'numero': 42}
            """,
            ),
            _t(
                "None si no encaja",
                """
                assert parsear_codigo('ABC-2025-01-31-9999') == {'categoria': 'ABC', 'fecha': '2025-01-31', 'numero': 9999}
                for malo in ('prd-2026-06-14-0042', 'PRD-2026-6-14-0042', 'PRD-2026-06-14-42', 'PRD-2026-06-14-0042x'):
                    assert parsear_codigo(malo) is None, f'{malo!r} no deberia encajar'
            """,
            ),
        ],
    ),
    # --------------------------------------------------------------------- logs
    ("files-logs", "easy"): ValidacionReto(
        _s("""
            def contar_niveles(lineas: list[str]) -> dict[str, int]:
                conteo = {}
                for linea in lineas:
                    nivel = linea.split()[2]
                    conteo[nivel] = conteo.get(nivel, 0) + 1
                return conteo
        """),
        [
            _t(
                "cuenta por nivel",
                """
                lineas = [
                    '2026-06-14 10:00:01 INFO /api/login ok',
                    '2026-06-14 10:00:02 ERROR /api/pagos timeout',
                    '2026-06-14 10:00:03 INFO /api/home ok',
                ]
                assert contar_niveles(lineas) == {'INFO': 2, 'ERROR': 1}
            """,
            ),
            _t(
                "sin lineas, diccionario vacio",
                """
                assert contar_niveles([]) == {}
            """,
            ),
        ],
    ),
    ("files-logs", "medium"): ValidacionReto(
        _s("""
            from collections import Counter


            def top_endpoints_con_error(lineas: list[str], k: int) -> list[tuple[str, int]]:
                errores = Counter(l.split()[3] for l in lineas if l.split()[2] == 'ERROR')
                return sorted(errores.items(), key=lambda par: (-par[1], par[0]))[:k]
        """),
        [
            _t(
                "ranking de endpoints con error",
                """
                lineas = [
                    '2026-06-14 10:00:01 ERROR /api/pagos timeout',
                    '2026-06-14 10:00:02 ERROR /api/login denegado',
                    '2026-06-14 10:00:03 INFO /api/pagos ok',
                    '2026-06-14 10:00:04 ERROR /api/pagos timeout',
                    '2026-06-14 10:00:05 ERROR /api/busqueda lento',
                ]
                assert top_endpoints_con_error(lineas, 2) == [('/api/pagos', 2), ('/api/busqueda', 1)]
            """,
            ),
            _t(
                "solo cuenta ERROR",
                """
                assert top_endpoints_con_error(['2026-06-14 10:00:01 WARN /x lento'], 3) == []
            """,
            ),
        ],
    ),
    ("files-logs", "hard"): ValidacionReto(
        _s("""
            NIVELES = {'INFO', 'WARN', 'ERROR'}


            def resumir_log(lineas: list[str]) -> dict:
                niveles = {}
                corruptas = 0
                primer_error = None
                for linea in lineas:
                    campos = linea.split()
                    if len(campos) < 4 or campos[2] not in NIVELES:
                        corruptas += 1
                        continue
                    niveles[campos[2]] = niveles.get(campos[2], 0) + 1
                    if campos[2] == 'ERROR' and primer_error is None:
                        primer_error = f'{campos[0]} {campos[1]}'
                return {'niveles': niveles, 'corruptas': corruptas, 'primer_error': primer_error}
        """),
        [
            _t(
                "resume y aparta las corruptas",
                """
                lineas = [
                    '2026-06-14 10:00:01 INFO /api/login ok',
                    'basura',
                    '2026-06-14 10:00:02 ERROR /api/pagos timeout',
                    '2026-06-14 10:00:03 DEBUG /api/x algo',
                    '2026-06-14 10:00:04 ERROR /api/login denegado',
                ]
                obtenido = resumir_log(lineas)
                assert obtenido == {
                    'niveles': {'INFO': 1, 'ERROR': 2},
                    'corruptas': 2,
                    'primer_error': '2026-06-14 10:00:02',
                }, f'devolvio {obtenido}'
            """,
            ),
            _t(
                "sin errores, primer_error es None y se serializa",
                """
                import json
                obtenido = resumir_log(['2026-06-14 10:00:01 INFO /a ok'])
                assert obtenido['primer_error'] is None
                json.dumps(obtenido)
            """,
            ),
        ],
    ),
    # ----------------------------------------------------------------- datetime
    ("datetime-reportes", "easy"): ValidacionReto(
        _s("""
            from datetime import datetime


            def eventos_por_dia(fechas: list[str]) -> dict[str, int]:
                conteo = {}
                for f in fechas:
                    dia = datetime.fromisoformat(f).date().isoformat()
                    conteo[dia] = conteo.get(dia, 0) + 1
                return conteo
        """),
        [
            _t(
                "agrupa por dia",
                """
                fechas = ['2026-06-14T10:30:00', '2026-06-14T23:59:59', '2026-06-15T00:00:00']
                assert eventos_por_dia(fechas) == {'2026-06-14': 2, '2026-06-15': 1}
            """,
            ),
        ],
    ),
    ("datetime-reportes", "medium"): ValidacionReto(
        _s("""
            from datetime import datetime, timedelta


            def racha_maxima(fechas: list[str]) -> int:
                dias = sorted({datetime.fromisoformat(f).date() for f in fechas})
                mejor = actual = 0
                anterior = None
                for d in dias:
                    actual = actual + 1 if anterior and d - anterior == timedelta(days=1) else 1
                    mejor = max(mejor, actual)
                    anterior = d
                return mejor
        """),
        [
            _t(
                "racha con un hueco",
                """
                fechas = ['2026-06-05T09:00:00', '2026-06-01T08:00:00', '2026-06-02T08:00:00', '2026-06-02T20:00:00', '2026-06-03T07:00:00']
                assert racha_maxima(fechas) == 3
            """,
            ),
            _t(
                "cruza de mes",
                """
                assert racha_maxima(['2026-05-31T10:00:00', '2026-06-01T10:00:00']) == 2
            """,
            ),
            _t(
                "sin fechas, 0",
                """
                assert racha_maxima([]) == 0
            """,
            ),
        ],
    ),
    ("datetime-reportes", "hard"): ValidacionReto(
        _s("""
            from datetime import datetime, timezone


            def eventos_por_semana_iso(fechas: list[str]) -> dict[str, int]:
                conteo = {}
                for f in fechas:
                    anio, semana, _ = datetime.fromisoformat(f).astimezone(timezone.utc).isocalendar()
                    clave = f'{anio}-W{semana:02d}'
                    conteo[clave] = conteo.get(clave, 0) + 1
                return conteo
        """),
        [
            _t(
                "convierte a UTC antes de agrupar",
                """
                fechas = ['2026-06-15T01:00:00+02:00', '2026-06-15T10:00:00+02:00']
                assert eventos_por_semana_iso(fechas) == {'2026-W24': 1, '2026-W25': 1}
            """,
            ),
            _t(
                "semana con dos digitos y cambio de anio ISO",
                """
                assert eventos_por_semana_iso(['2027-01-01T12:00:00+00:00']) == {'2026-W53': 1}
                assert eventos_por_semana_iso(['2026-01-05T12:00:00+00:00']) == {'2026-W02': 1}
            """,
            ),
        ],
    ),
    # ---------------------------------------------------------------------- oop
    ("oop-bank-account", "easy"): ValidacionReto(
        _s("""
            class Cuenta:
                def __init__(self, saldo: float = 0):
                    self.saldo = saldo

                def depositar(self, monto: float) -> None:
                    self.saldo += monto

                def retirar(self, monto: float) -> None:
                    if monto > self.saldo:
                        raise ValueError('saldo insuficiente')
                    self.saldo -= monto
        """),
        [
            _t(
                "deposita y retira",
                """
                c = Cuenta()
                c.depositar(100)
                c.retirar(30)
                assert c.saldo == 70, f'saldo {c.saldo}'
            """,
            ),
            _t(
                "no deja retirar mas de lo que hay",
                """
                c = Cuenta(50)
                try:
                    c.retirar(80)
                except ValueError:
                    pass
                else:
                    raise AssertionError('retirar mas del saldo deberia lanzar ValueError')
                assert c.saldo == 50, 'el saldo cambio aunque la operacion fallo'
            """,
            ),
        ],
    ),
    ("oop-bank-account", "medium"): ValidacionReto(
        _s("""
            class SaldoInsuficiente(Exception):
                pass


            class CuentaConHistorial:
                def __init__(self, saldo: float = 0):
                    self.saldo = saldo
                    self.historial = []

                def _validar(self, monto):
                    if monto <= 0:
                        raise ValueError('el monto tiene que ser positivo')

                def depositar(self, monto: float) -> None:
                    self._validar(monto)
                    self.saldo += monto
                    self.historial.append(('deposito', monto))

                def retirar(self, monto: float) -> None:
                    self._validar(monto)
                    if monto > self.saldo:
                        raise SaldoInsuficiente(f'saldo {self.saldo}, pediste {monto}')
                    self.saldo -= monto
                    self.historial.append(('retiro', monto))
        """),
        [
            _t(
                "anota las operaciones que salen bien",
                """
                c = CuentaConHistorial()
                c.depositar(100)
                c.retirar(40)
                assert c.saldo == 60
                assert c.historial == [('deposito', 100), ('retiro', 40)], f'historial {c.historial}'
            """,
            ),
            _t(
                "excepcion propia y sin anotar lo que falla",
                """
                assert issubclass(SaldoInsuficiente, Exception)
                c = CuentaConHistorial(10)
                try:
                    c.retirar(50)
                except SaldoInsuficiente:
                    pass
                else:
                    raise AssertionError('retirar de mas deberia lanzar SaldoInsuficiente')
                assert c.historial == [] and c.saldo == 10
            """,
            ),
            _t(
                "montos no positivos lanzan ValueError",
                """
                c = CuentaConHistorial(10)
                for metodo in (c.depositar, c.retirar):
                    try:
                        metodo(0)
                    except ValueError:
                        pass
                    else:
                        raise AssertionError(f'{metodo.__name__}(0) deberia lanzar ValueError')
                assert c.historial == []
            """,
            ),
        ],
    ),
    ("oop-bank-account", "hard"): ValidacionReto(
        _s("""
            auditoria = []


            class Cuenta:
                def __init__(self, titular: str, saldo: float = 0, activa: bool = True):
                    self.titular = titular
                    self.saldo = saldo
                    self.activa = activa

                def depositar(self, monto: float) -> None:
                    if not self.activa:
                        raise ValueError(f'la cuenta de {self.titular} esta inactiva')
                    self.saldo += monto

                def retirar(self, monto: float) -> None:
                    if monto > self.saldo:
                        raise ValueError('saldo insuficiente')
                    self.saldo -= monto


            def transferir(origen: Cuenta, destino: Cuenta, monto: float) -> None:
                origen.retirar(monto)
                try:
                    destino.depositar(monto)
                except Exception:
                    origen.saldo += monto
                    raise
                auditoria.append((origen.titular, destino.titular, monto))
        """),
        [
            _t(
                "transfiere y anota",
                """
                auditoria.clear()
                a, b = Cuenta('Ana', 100), Cuenta('Beto', 5)
                transferir(a, b, 30)
                assert (a.saldo, b.saldo) == (70, 35)
                assert auditoria == [('Ana', 'Beto', 30)], f'auditoria {auditoria}'
            """,
            ),
            _t(
                "destino inactivo: nadie pierde dinero",
                """
                auditoria.clear()
                a, b = Cuenta('Ana', 100), Cuenta('Beto', 5, activa=False)
                try:
                    transferir(a, b, 30)
                except ValueError:
                    pass
                else:
                    raise AssertionError('transferir a una cuenta inactiva deberia relanzar el error')
                assert (a.saldo, b.saldo) == (100, 5), f'saldos {a.saldo}, {b.saldo}: el dinero desaparecio'
                assert auditoria == []
            """,
            ),
            _t(
                "sin saldo no se mueve nada",
                """
                auditoria.clear()
                a, b = Cuenta('Ana', 10), Cuenta('Beto')
                try:
                    transferir(a, b, 50)
                except ValueError:
                    pass
                else:
                    raise AssertionError('sin saldo deberia lanzar ValueError')
                assert (a.saldo, b.saldo) == (10, 0) and auditoria == []
            """,
            ),
        ],
    ),
    # ------------------------------------------------------------------ testing
    ("testing-pytest", "easy"): ValidacionReto(
        _s("""
            def calcular_descuento(total: float, porcentaje: float) -> float:
                return total - (total * porcentaje / 100)


            def test_descuento_basico():
                assert calcular_descuento(200, 10) == 180
                assert calcular_descuento(100, 0) == 100
                assert calcular_descuento(50, 50) == 25
        """),
        [
            _t(
                "tu test detecta un signo cambiado",
                """
                test_descuento_basico()  # con la funcion correcta tiene que pasar
                def calcular_descuento(total, porcentaje):
                    return total + (total * porcentaje / 100)
                try:
                    test_descuento_basico()
                except AssertionError:
                    pass
                else:
                    raise AssertionError('rompimos la funcion (+ en vez de -) y tu test no se entero')
            """,
            ),
            _t(
                "tu test detecta que se ignora el porcentaje",
                """
                test_descuento_basico()  # con la funcion correcta tiene que pasar
                def calcular_descuento(total, porcentaje):
                    return total
                try:
                    test_descuento_basico()
                except AssertionError:
                    pass
                else:
                    raise AssertionError('rompimos la funcion (no descuenta nada) y tu test no se entero')
            """,
            ),
        ],
    ),
    ("testing-pytest", "medium"): ValidacionReto(
        _s("""
            def calcular_descuento(total: float, porcentaje: float) -> float:
                if not 0 <= porcentaje <= 100:
                    raise ValueError('porcentaje fuera de rango')
                return total - (total * porcentaje / 100)


            def test_casos_borde():
                casos = [(80, 0, 80), (80, 100, 0), (200, 25, 150)]
                for total, porcentaje, esperado in casos:
                    assert calcular_descuento(total, porcentaje) == esperado
                try:
                    calcular_descuento(10, 150)
                except ValueError:
                    pass
                else:
                    raise AssertionError('150% deberia lanzar ValueError')
        """),
        [
            _t(
                "tu test detecta que el 100% no deja en 0",
                """
                test_casos_borde()  # con la funcion correcta tiene que pasar
                def calcular_descuento(total, porcentaje):
                    if not 0 <= porcentaje <= 100:
                        raise ValueError('fuera')
                    return total - (total * min(porcentaje, 99) / 100)
                try:
                    test_casos_borde()
                except AssertionError:
                    pass
                else:
                    raise AssertionError('rompimos el caso del 100% y tu test no se entero')
            """,
            ),
            _t(
                "tu test detecta que falta la validacion",
                """
                test_casos_borde()  # con la funcion correcta tiene que pasar
                def calcular_descuento(total, porcentaje):
                    return total - (total * porcentaje / 100)
                try:
                    test_casos_borde()
                except AssertionError:
                    pass
                else:
                    raise AssertionError('quitamos el ValueError y tu test no se entero')
            """,
            ),
        ],
    ),
    ("testing-pytest", "hard"): ValidacionReto(
        _s("""
            def subtotal(items):
                return sum(item['precio'] * item['cantidad'] for item in items)


            def aplicar_cupon(importe, cupon):
                if cupon == 'DESC10':
                    return importe - importe * 0.10
                if cupon == 'MENOS5' and importe > 5:
                    return importe - 5
                return importe


            def coste_envio(importe):
                return 4.99 if importe < 50 else 0


            def precio_final(items, cupon=None):
                importe = aplicar_cupon(subtotal(items), cupon)
                return round(importe + coste_envio(importe), 2)


            def test_precio_final():
                caro = [{'precio': 30, 'cantidad': 2}]
                barato = [{'precio': 10, 'cantidad': 1}]
                assert precio_final(caro) == 60
                assert precio_final(barato) == 14.99
                assert precio_final(caro, 'DESC10') == 54
                assert precio_final(barato, 'MENOS5') == 9.99
        """),
        [
            _t(
                "refactorizado sin cambiar el resultado",
                """
                for nombre in ('subtotal', 'aplicar_cupon', 'coste_envio'):
                    assert callable(globals().get(nombre)), f'falta extraer {nombre}'
                casos = [
                    ([{'precio': 30, 'cantidad': 2}], None, 60),
                    ([{'precio': 10, 'cantidad': 1}], None, 14.99),
                    ([{'precio': 30, 'cantidad': 2}], 'DESC10', 54.0),
                    ([{'precio': 50, 'cantidad': 1}], 'DESC10', 49.99),
                    ([{'precio': 10, 'cantidad': 1}], 'MENOS5', 9.99),
                    ([{'precio': 4, 'cantidad': 1}], 'MENOS5', 8.99),
                ]
                for items, cupon, esperado in casos:
                    obtenido = precio_final(items, cupon)
                    assert obtenido == esperado, f'precio_final({items}, {cupon!r}) = {obtenido}, antes daba {esperado}'
            """,
            ),
            _t(
                "las tres funciones extraidas existen y funcionan",
                """
                assert subtotal([{'precio': 2, 'cantidad': 3}, {'precio': 1, 'cantidad': 1}]) == 7
                assert aplicar_cupon(100, 'DESC10') == 90 and aplicar_cupon(100, None) == 100
                assert coste_envio(10) == 4.99 and coste_envio(80) == 0
            """,
            ),
            _t(
                "precio_final usa coste_envio",
                """
                def coste_envio(importe):
                    return 1000
                assert precio_final([{'precio': 80, 'cantidad': 1}]) == 1080, 'precio_final no llama a coste_envio'
            """,
            ),
            _t(
                "tu test detecta un precio_final roto",
                """
                test_precio_final()  # con el codigo correcto tiene que pasar
                def precio_final(items, cupon=None):
                    return 0
                try:
                    test_precio_final()
                except AssertionError:
                    pass
                else:
                    raise AssertionError('rompimos precio_final y tu test no se entero')
            """,
            ),
        ],
    ),
    # ------------------------------------------------------------------- pandas
    ("pandas-aggregations", "easy"): ValidacionReto(
        _s("""
            import pandas as pd


            def total_por_producto(df: pd.DataFrame) -> dict:
                importe = df['cantidad'] * df['precio']
                return importe.groupby(df['producto']).sum().to_dict()
        """),
        [
            _t(
                "suma cantidad por precio por producto",
                """
                import pandas as pd
                df = pd.DataFrame({'producto': ['cafe', 'te', 'cafe'], 'cantidad': [2, 1, 3], 'precio': [5, 4, 5]})
                obtenido = total_por_producto(df)
                assert {k: float(v) for k, v in obtenido.items()} == {'cafe': 25.0, 'te': 4.0}, f'devolvio {obtenido}'
            """,
            ),
            _t(
                "devuelve un diccionario",
                """
                import pandas as pd
                df = pd.DataFrame({'producto': ['x'], 'cantidad': [1], 'precio': [2]})
                assert isinstance(total_por_producto(df), dict)
            """,
            ),
        ],
    ),
    ("pandas-aggregations", "medium"): ValidacionReto(
        _s("""
            import pandas as pd


            def ticket_promedio_por_ciudad(df: pd.DataFrame) -> pd.Series:
                por_ticket = df.groupby(['ciudad', 'ticket_id'])['importe'].sum()
                return por_ticket.groupby(level='ciudad').mean().sort_values(ascending=False)
        """),
        [
            _t(
                "promedia por ticket, no por fila",
                """
                import pandas as pd
                df = pd.DataFrame({
                    'ciudad': ['Lima', 'Lima', 'Lima', 'Cusco'],
                    'ticket_id': [1, 1, 2, 3],
                    'importe': [10, 30, 20, 25],
                })
                obtenido = ticket_promedio_por_ciudad(df)
                assert isinstance(obtenido, pd.Series)
                assert abs(obtenido['Lima'] - 30) < 1e-9, f'Lima deberia ser 30 (tickets de 40 y 20), dio {obtenido["Lima"]}'
                assert abs(obtenido['Cusco'] - 25) < 1e-9
            """,
            ),
            _t(
                "ordenada de mayor a menor",
                """
                import pandas as pd
                df = pd.DataFrame({'ciudad': ['A', 'B', 'C'], 'ticket_id': [1, 2, 3], 'importe': [5, 50, 20]})
                assert list(ticket_promedio_por_ciudad(df).index) == ['B', 'C', 'A']
            """,
            ),
        ],
    ),
    ("pandas-aggregations", "hard"): ValidacionReto(
        _s("""
            import pandas as pd


            def reporte_mensual(df: pd.DataFrame) -> pd.DataFrame:
                meses = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m')
                total = df.groupby(meses)['importe'].sum().sort_index()
                out = pd.DataFrame({'mes': total.index, 'total': total.values})
                out['variacion_pct'] = out['total'].pct_change() * 100
                out['ranking'] = out['total'].rank(ascending=False, method='min').astype(int)
                return out
        """),
        [
            _t(
                "una fila por mes con total, variacion y ranking",
                """
                import math
                import pandas as pd
                df = pd.DataFrame({
                    'fecha': ['2026-02-10', '2026-01-05', '2026-01-20', '2026-03-01'],
                    'importe': [150, 60, 40, 75],
                })
                r = reporte_mensual(df).reset_index(drop=True)
                assert list(r['mes']) == ['2026-01', '2026-02', '2026-03'], f'meses {list(r["mes"])}'
                assert [float(x) for x in r['total']] == [100.0, 150.0, 75.0]
                assert math.isnan(r['variacion_pct'][0])
                assert abs(r['variacion_pct'][1] - 50) < 1e-9 and abs(r['variacion_pct'][2] + 50) < 1e-9
                assert [int(x) for x in r['ranking']] == [2, 1, 3]
            """,
            ),
        ],
    ),
    # -------------------------------------------------------------------- numpy
    ("numpy-vectorization", "easy"): ValidacionReto(
        _s("""
            import numpy as np


            def media_y_desviacion(a: np.ndarray) -> tuple[float, float]:
                return (float(np.mean(a)), float(np.std(a)))
        """),
        [
            _t(
                "media y desviacion poblacional",
                """
                import numpy as np
                media, desv = media_y_desviacion(np.array([2, 4, 4, 4, 5, 5, 7, 9]))
                assert (media, desv) == (5.0, 2.0), f'devolvio {(media, desv)}'
                assert type(media) is float and type(desv) is float, 'devuelve float de Python, no np.float64'
            """,
            ),
        ],
    ),
    ("numpy-vectorization", "medium"): ValidacionReto(
        _s("""
            import numpy as np


            def normalizar_columnas(m: np.ndarray) -> np.ndarray:
                m = m.astype(float)
                minimo = m.min(axis=0)
                rango = m.max(axis=0) - minimo
                return np.divide(m - minimo, rango, out=np.zeros_like(m), where=rango != 0)
        """),
        [
            _t(
                "cada columna entre 0 y 1",
                """
                import numpy as np
                m = np.array([[1, 10], [3, 30], [2, 20]])
                obtenido = normalizar_columnas(m)
                assert np.allclose(obtenido, [[0, 0], [1, 1], [0.5, 0.5]]), f'devolvio {obtenido}'
            """,
            ),
            _t(
                "columna constante queda en 0 sin avisos de division",
                """
                import numpy as np, warnings
                with warnings.catch_warnings():
                    warnings.simplefilter('error')
                    obtenido = normalizar_columnas(np.array([[5, 1], [5, 2]]))
                assert np.allclose(obtenido[:, 0], 0) and not np.isnan(obtenido).any()
            """,
            ),
        ],
    ),
    ("numpy-vectorization", "hard"): ValidacionReto(
        _s("""
            import numpy as np


            def distancia_coseno_filas(a: np.ndarray, b: np.ndarray) -> np.ndarray:
                a = a.astype(float)
                b = b.astype(float)
                producto = (a * b).sum(axis=1)
                normas = np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1)
                similitud = np.divide(producto, normas, out=np.zeros(len(a)), where=normas != 0)
                return 1 - similitud
        """),
        [
            _t(
                "distancia por filas",
                """
                import numpy as np
                a = np.array([[1, 0], [1, 1], [1, 0]])
                b = np.array([[1, 0], [-1, -1], [0, 1]])
                obtenido = distancia_coseno_filas(a, b)
                assert obtenido.shape == (3,)
                assert np.allclose(obtenido, [0, 2, 1]), f'devolvio {obtenido}'
            """,
            ),
            _t(
                "fila de ceros vale 1",
                """
                import numpy as np, warnings
                with warnings.catch_warnings():
                    warnings.simplefilter('error')
                    obtenido = distancia_coseno_filas(np.array([[0, 0]]), np.array([[3, 4]]))
                assert np.allclose(obtenido, [1.0])
            """,
            ),
        ],
    ),
}


# slug_suffix del reto curado -> tests (la solucion ya vive en curated_retos.py)
TESTS_CURADOS: dict[str, list[dict]] = {
    "fizzbuzz-lista": [
        _t(
            "el ejemplo del enunciado",
            """
            assert fizzbuzz(5) == ['1', '2', 'Fizz', '4', 'Buzz']
        """,
        ),
        _t(
            "el 15 es FizzBuzz y el resto son str",
            """
            obtenido = fizzbuzz(15)
            assert obtenido[14] == 'FizzBuzz' and obtenido[9] == 'Buzz' and obtenido[5] == 'Fizz'
            assert obtenido[0] == '1', 'los numeros van como str'
            assert len(fizzbuzz(0)) == 0
        """,
        ),
    ],
    "validador-password": [
        _t(
            "acepta una contrasena que cumple todo",
            """
            assert es_segura('Abc12345') is True
        """,
        ),
        _t(
            "rechaza si falta cualquier requisito",
            """
            for mala in ('abc', 'abcdefg1', 'ABCDEFG1', 'Abcdefgh', 'Ab1'):
                assert es_segura(mala) is False, f'{mala!r} no deberia ser segura'
        """,
        ),
    ],
    "conteo-palabras": [
        _t(
            "minusculas y por espacios",
            """
            assert contar_palabras('hola Hola mundo') == {'hola': 2, 'mundo': 1}
        """,
        ),
        _t(
            "varios espacios y texto vacio",
            """
            assert contar_palabras('a   b a') == {'a': 2, 'b': 1}
            assert contar_palabras('') == {}
        """,
        ),
    ],
    "media-movil": [
        _t(
            "promedios de cada ventana",
            """
            assert media_movil([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]
            assert media_movil([5, 5, 5], 3) == [5.0]
        """,
        ),
        _t(
            "k invalido devuelve lista vacia",
            """
            assert media_movil([1, 2], 0) == []
            assert media_movil([1, 2], 3) == []
        """,
        ),
    ],
    "total-por-categoria": [
        _t(
            "suma por categoria",
            """
            obtenido = total_por_categoria([
                {'categoria': 'a', 'monto': 10},
                {'categoria': 'b', 'monto': 3},
                {'categoria': 'a', 'monto': 5},
            ])
            assert obtenido == {'a': 15, 'b': 3}, f'devolvio {obtenido}'
        """,
        ),
        _t(
            "sin transacciones, diccionario vacio",
            """
            assert total_por_categoria([]) == {}
        """,
        ),
    ],
    "outliers-iqr": [
        _t(
            "detecta el valor extremo",
            """
            assert [float(x) for x in outliers([10, 12, 11, 13, 12, 100])] == [100.0]
        """,
        ),
        _t(
            "conserva el orden y detecta por abajo",
            """
            assert [float(x) for x in outliers([-50, 10, 11, 12, 13, 90])] == [-50.0, 90.0]
        """,
        ),
        _t(
            "sin outliers, lista vacia",
            """
            assert list(outliers([1, 2, 3, 4, 5])) == []
        """,
        ),
    ],
    "normalizacion-minmax": [
        _t(
            "lleva a [0, 1]",
            """
            assert normaliza([10, 20, 30]) == [0.0, 0.5, 1.0]
        """,
        ),
        _t(
            "valores iguales dan ceros",
            """
            assert normaliza([7, 7, 7]) == [0.0, 0.0, 0.0]
        """,
        ),
    ],
    "one-hot-encoding": [
        _t(
            "columnas en orden alfabetico",
            """
            assert one_hot(['rojo', 'verde', 'rojo']) == [[1, 0], [0, 1], [1, 0]]
            assert one_hot(['b', 'a', 'c']) == [[0, 1, 0], [1, 0, 0], [0, 0, 1]]
        """,
        ),
        _t(
            "una sola categoria",
            """
            assert one_hot(['x', 'x']) == [[1], [1]]
        """,
        ),
    ],
    "matriz-confusion": [
        _t(
            "el ejemplo del enunciado",
            """
            assert matriz_confusion([1, 0, 1, 1], [1, 0, 0, 1]) == {'tp': 2, 'fp': 0, 'fn': 1, 'tn': 1}
        """,
        ),
        _t(
            "cuenta falsos positivos",
            """
            assert matriz_confusion([0, 0, 1], [1, 1, 1]) == {'tp': 1, 'fp': 2, 'fn': 0, 'tn': 0}
        """,
        ),
    ],
    "tf-term-frequency": [
        _t(
            "frecuencia normalizada",
            """
            obtenido = tf('a b a')
            assert set(obtenido) == {'a', 'b'}
            assert abs(obtenido['a'] - 2 / 3) < 1e-9 and abs(obtenido['b'] - 1 / 3) < 1e-9
        """,
        ),
        _t(
            "minusculas y suma 1",
            """
            obtenido = tf('Hola hola mundo')
            assert set(obtenido) == {'hola', 'mundo'}
            assert abs(sum(obtenido.values()) - 1) < 1e-9
        """,
        ),
    ],
}
