"""
Seed de capstones por Track.

Cada capstone es un proyecto guiado: descripcion + requisitos + archivos
starter + tests ocultos. El seeder es idempotente por slug (no sobrescribe
submissions existentes; solo inserta capstones que falten).

Patron replicable: los capstones de Tracks 2-6 se anaden a `CAPSTONES`
con el mismo schema. El evaluador (D.3) corre los hidden_tests en Pyodide
para Track 1; en Tracks 2-6 reutilizara el mismo runner con assertions
de Pandas/sklearn/PyTorch.
"""

# flake8: noqa: E501 -- contenido curado del capstone, enunciados largos en espanol.

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.capstone import Capstone

CAPSTONES: list[dict] = [
    {
        "slug": "track-1-cli-ventas",
        "track": "track-1",
        "title": "CLI de gestion de ventas",
        "short_description": (
            "Construye una aplicacion de linea de comandos para registrar "
            "ventas, calcular totales y generar reportes. Combina argparse, "
            "persistencia JSON y funciones puras."
        ),
        "description": (
            "## Contexto\n\n"
            "Una panaderia local lleva las ventas en una hoja de calculo y "
            "necesita una herramienta mas simple. Vas a construir una CLI en "
            "Python que registre ventas, las persista en un archivo JSON y "
            "genere reportes basicos.\n\n"
            "## Que aprendes con este capstone\n\n"
            "- Disenar un proyecto multimodulo (separar logica de IO).\n"
            "- Persistir datos en JSON con `json.load` / `json.dump`.\n"
            "- Validar entradas y lanzar excepciones con mensaje claro.\n"
            "- Escribir funciones puras (sin efectos) faciles de testear.\n\n"
            "## Estructura sugerida\n\n"
            "```\n"
            "ventas_cli/\n"
            "  store.py       # Clase SalesStore: load/save/add/remove\n"
            "  reports.py     # Funciones puras: totales y rankings\n"
            "  cli.py         # Entry point con argparse\n"
            "```\n\n"
            "## Como se evalua\n\n"
            "Cuando pulses **Enviar capstone**, la plataforma corre un set "
            "de tests ocultos sobre tu codigo (mismo patron que los tests "
            "ocultos de los ejercicios). No veras los tests, pero veras "
            "cuantos pasaron y el mensaje de error de los que fallaron.\n\n"
            "Necesitas pasar al menos 7 de 8 tests para que el capstone "
            "cuente como completado y desbloquee el certificado del Track 1."
        ),
        "requirements": [
            {
                "id": "R1",
                "text": (
                    "`SalesStore.add_venta(producto, cantidad, precio_unitario)` "
                    "registra una venta en memoria. Acepta strings para producto "
                    "y enteros/floats positivos para cantidad y precio_unitario."
                ),
            },
            {
                "id": "R2",
                "text": (
                    "`SalesStore.add_venta` lanza `ValueError` con mensaje claro "
                    "si cantidad <= 0 o precio_unitario <= 0."
                ),
            },
            {
                "id": "R3",
                "text": (
                    "`SalesStore.list_ventas()` retorna la lista de ventas en "
                    "orden de insercion. Cada venta es un dict con claves "
                    "`producto`, `cantidad` y `precio_unitario`."
                ),
            },
            {
                "id": "R4",
                "text": (
                    "`SalesStore.remove_producto(producto)` elimina todas las "
                    "ventas de ese producto. Retorna el numero de ventas "
                    "eliminadas (0 si no habia ninguna)."
                ),
            },
            {
                "id": "R5",
                "text": (
                    "`reports.total_ventas(ventas)` retorna la suma total de "
                    "`cantidad * precio_unitario` sobre la lista. Funciona con "
                    "lista vacia (retorna 0)."
                ),
            },
            {
                "id": "R6",
                "text": (
                    "`reports.ventas_por_producto(ventas)` retorna un dict "
                    "`producto -> total_ingresos` agrupando por producto."
                ),
            },
            {
                "id": "R7",
                "text": (
                    "`reports.top_n_productos(ventas, n)` retorna una lista de "
                    "tuplas `(producto, total)` ordenadas por total descendente, "
                    "con un maximo de `n` elementos."
                ),
            },
            {
                "id": "R8",
                "text": (
                    "Todos los reportes deben funcionar con lista vacia sin "
                    "lanzar excepciones (`total_ventas([]) == 0`, "
                    "`ventas_por_producto([]) == {}`, etc.)."
                ),
            },
        ],
        "starter_files": [
            {
                "path": "store.py",
                "editable": True,
                "content": (
                    '"""Modulo de persistencia y CRUD de ventas."""\n'
                    "\n"
                    "import json\n"
                    "from pathlib import Path\n"
                    "\n"
                    "\n"
                    "class SalesStore:\n"
                    '    """Gestiona la lista de ventas y su persistencia en JSON."""\n'
                    "\n"
                    "    def __init__(self, ruta_archivo: str | None = None):\n"
                    "        self.ruta_archivo = ruta_archivo\n"
                    "        self._ventas: list[dict] = []\n"
                    "\n"
                    "    def add_venta(self, producto: str, cantidad, precio_unitario) -> None:\n"
                    "        # TODO: validar cantidad > 0 y precio_unitario > 0\n"
                    "        # TODO: si no, lanzar ValueError con mensaje claro\n"
                    "        # TODO: anadir un dict {producto, cantidad, precio_unitario} a self._ventas\n"
                    "        raise NotImplementedError\n"
                    "\n"
                    "    def list_ventas(self) -> list[dict]:\n"
                    "        # TODO: retornar self._ventas (o una copia)\n"
                    "        raise NotImplementedError\n"
                    "\n"
                    "    def remove_producto(self, producto: str) -> int:\n"
                    "        # TODO: eliminar todas las ventas cuyo producto coincida\n"
                    "        # TODO: retornar el numero de ventas eliminadas\n"
                    "        raise NotImplementedError\n"
                    "\n"
                    "    def save(self) -> None:\n"
                    "        # OPCIONAL: persiste self._ventas a self.ruta_archivo en JSON\n"
                    "        if not self.ruta_archivo:\n"
                    "            return\n"
                    "        Path(self.ruta_archivo).write_text(\n"
                    "            json.dumps(self._ventas, ensure_ascii=False, indent=2),\n"
                    '            encoding="utf-8",\n'
                    "        )\n"
                    "\n"
                    "    def load(self) -> None:\n"
                    "        # OPCIONAL: carga self._ventas desde self.ruta_archivo si existe\n"
                    "        if not self.ruta_archivo:\n"
                    "            return\n"
                    "        path = Path(self.ruta_archivo)\n"
                    "        if not path.exists():\n"
                    "            return\n"
                    '        self._ventas = json.loads(path.read_text(encoding="utf-8"))\n'
                ),
            },
            {
                "path": "reports.py",
                "editable": True,
                "content": (
                    '"""Funciones puras para calcular reportes sobre una lista de ventas."""\n'
                    "\n"
                    "\n"
                    "def total_ventas(ventas: list[dict]) -> float:\n"
                    '    """Suma total de cantidad * precio_unitario sobre todas las ventas."""\n'
                    "    # TODO: recorrer ventas y sumar cantidad * precio_unitario\n"
                    "    # TODO: si la lista esta vacia, retornar 0\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def ventas_por_producto(ventas: list[dict]) -> dict:\n"
                    '    """Retorna {producto: total_ingresos} agrupando por producto."""\n'
                    "    # TODO: usar un dict acumulador\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def top_n_productos(ventas: list[dict], n: int) -> list[tuple]:\n"
                    '    """Top n productos por total de ingresos, descendente."""\n'
                    "    # TODO: reutilizar ventas_por_producto y ordenar\n"
                    "    raise NotImplementedError\n"
                ),
            },
            {
                "path": "cli.py",
                "editable": True,
                "content": (
                    '"""Entry point CLI con argparse (opcional para los tests, pero recomendable)."""\n'
                    "\n"
                    "import argparse\n"
                    "from store import SalesStore\n"
                    "from reports import total_ventas, ventas_por_producto, top_n_productos\n"
                    "\n"
                    "\n"
                    "def build_parser() -> argparse.ArgumentParser:\n"
                    '    parser = argparse.ArgumentParser(description="Gestion de ventas")\n'
                    '    subparsers = parser.add_subparsers(dest="comando")\n'
                    "\n"
                    '    add = subparsers.add_parser("add")\n'
                    '    add.add_argument("producto")\n'
                    '    add.add_argument("cantidad", type=int)\n'
                    '    add.add_argument("precio", type=float)\n'
                    "\n"
                    '    subparsers.add_parser("listar")\n'
                    '    subparsers.add_parser("total")\n'
                    '    subparsers.add_parser("top")\n'
                    "\n"
                    "    return parser\n"
                    "\n"
                    "\n"
                    'if __name__ == "__main__":\n'
                    "    parser = build_parser()\n"
                    "    args = parser.parse_args()\n"
                    '    print("Comando:", args.comando)\n'
                ),
            },
        ],
        "hidden_tests": [
            {
                "name": "add_venta agrega una venta",
                "code": (
                    "from store import SalesStore\n"
                    "store = SalesStore()\n"
                    "store.add_venta('pan', 5, 2.0)\n"
                    "ventas = store.list_ventas()\n"
                    "assert len(ventas) == 1\n"
                    "assert ventas[0]['producto'] == 'pan'\n"
                    "assert ventas[0]['cantidad'] == 5\n"
                    "assert ventas[0]['precio_unitario'] == 2.0"
                ),
            },
            {
                "name": "add_venta rechaza cantidad cero o negativa",
                "code": (
                    "from store import SalesStore\n"
                    "store = SalesStore()\n"
                    "try:\n"
                    "    store.add_venta('pan', 0, 2.0)\n"
                    "    raise AssertionError('debio lanzar ValueError con cantidad 0')\n"
                    "except ValueError:\n"
                    "    pass\n"
                    "try:\n"
                    "    store.add_venta('pan', -3, 2.0)\n"
                    "    raise AssertionError('debio lanzar ValueError con cantidad negativa')\n"
                    "except ValueError:\n"
                    "    pass"
                ),
            },
            {
                "name": "add_venta rechaza precio cero o negativo",
                "code": (
                    "from store import SalesStore\n"
                    "store = SalesStore()\n"
                    "try:\n"
                    "    store.add_venta('pan', 5, 0)\n"
                    "    raise AssertionError('debio lanzar ValueError con precio 0')\n"
                    "except ValueError:\n"
                    "    pass\n"
                    "try:\n"
                    "    store.add_venta('pan', 5, -2.0)\n"
                    "    raise AssertionError('debio lanzar ValueError con precio negativo')\n"
                    "except ValueError:\n"
                    "    pass"
                ),
            },
            {
                "name": "remove_producto retorna cuenta correcta",
                "code": (
                    "from store import SalesStore\n"
                    "store = SalesStore()\n"
                    "store.add_venta('pan', 5, 2.0)\n"
                    "store.add_venta('cafe', 3, 4.0)\n"
                    "store.add_venta('pan', 2, 2.0)\n"
                    "n = store.remove_producto('pan')\n"
                    "assert n == 2, f'esperaba 2 ventas removidas, obtuve {n}'\n"
                    "assert len(store.list_ventas()) == 1\n"
                    "assert store.list_ventas()[0]['producto'] == 'cafe'"
                ),
            },
            {
                "name": "total_ventas suma correctamente",
                "code": (
                    "from reports import total_ventas\n"
                    "ventas = [\n"
                    "    {'producto': 'pan', 'cantidad': 5, 'precio_unitario': 2.0},\n"
                    "    {'producto': 'cafe', 'cantidad': 3, 'precio_unitario': 4.0},\n"
                    "]\n"
                    "assert total_ventas(ventas) == 22.0"
                ),
            },
            {
                "name": "total_ventas con lista vacia retorna 0",
                "code": (
                    "from reports import total_ventas\n" "assert total_ventas([]) == 0"
                ),
            },
            {
                "name": "ventas_por_producto agrupa correctamente",
                "code": (
                    "from reports import ventas_por_producto\n"
                    "ventas = [\n"
                    "    {'producto': 'pan', 'cantidad': 5, 'precio_unitario': 2.0},\n"
                    "    {'producto': 'pan', 'cantidad': 2, 'precio_unitario': 2.0},\n"
                    "    {'producto': 'cafe', 'cantidad': 3, 'precio_unitario': 4.0},\n"
                    "]\n"
                    "resultado = ventas_por_producto(ventas)\n"
                    "assert resultado == {'pan': 14.0, 'cafe': 12.0}, resultado"
                ),
            },
            {
                "name": "top_n_productos ordena descendente",
                "code": (
                    "from reports import top_n_productos\n"
                    "ventas = [\n"
                    "    {'producto': 'pan', 'cantidad': 5, 'precio_unitario': 2.0},\n"
                    "    {'producto': 'cafe', 'cantidad': 3, 'precio_unitario': 4.0},\n"
                    "    {'producto': 'leche', 'cantidad': 10, 'precio_unitario': 1.5},\n"
                    "]\n"
                    "top = top_n_productos(ventas, 2)\n"
                    "assert top[0] == ('leche', 15.0), top\n"
                    "assert top[1] == ('cafe', 12.0), top\n"
                    "assert len(top) == 2"
                ),
            },
        ],
        "estimated_hours": 8,
        "difficulty": "intermediate",
        "order_index": 1,
    },
    {
        "slug": "track-2-eda-cafecito",
        "track": "track-2",
        "title": "EDA del cafecito: ventas, sucursales y productos",
        "short_description": (
            "Analiza el dataset ventas-pyme con pandas. Construye un modulo "
            "de funciones puras que calcule KPIs, ranking de sucursales, "
            "serie temporal de unidades y correlacion. Cierra el Track 2 "
            "de Data Science."
        ),
        "description": (
            "## Contexto\n\n"
            "La cafeteria del Track 1 (la que registraba ventas con la CLI) "
            "ya tiene 60 dias de datos consolidados en un CSV. La duena te "
            "pide un analisis exploratorio: que sucursal vende mas, cual es "
            "el producto estrella, si hay tendencia diaria y si las unidades "
            "vendidas explican el ingreso.\n\n"
            "## Que aprendes con este capstone\n\n"
            "- Cargar y parsear un CSV real con `pd.read_csv` + `parse_dates`.\n"
            "- Componer `groupby + sum + sort_values + idxmax` como bloques.\n"
            "- Trabajar con `DatetimeIndex` para series temporales.\n"
            "- Calcular correlacion de Pearson con `.corr()`.\n"
            "- Mantener funciones **puras** (sin efectos, sin prints) faciles "
            "de testear.\n\n"
            "## Estructura sugerida\n\n"
            "```\n"
            "eda_cafecito/\n"
            "  analisis.py    # Funciones puras: parsear, KPIs, agrupaciones\n"
            "  notebook.py    # Script de exploracion (opcional, no testeado)\n"
            "```\n\n"
            "El dataset esta disponible via la helper de la plataforma:\n\n"
            "```python\n"
            "import pycode\n"
            "csv_text = await pycode.fetch_dataset_csv('ventas-pyme')\n"
            "df = parsear_ventas(csv_text)\n"
            "```\n\n"
            "Pero **los tests** te van a pasar su propio CSV pequeno (6 filas) "
            "para que las funciones sean reproducibles; no asumas el dataset "
            "real en tu logica.\n\n"
            "## Como se evalua\n\n"
            "Cuando pulses **Enviar capstone**, la plataforma corre 8 tests "
            "ocultos que invocan cada funcion con datos sinteticos y comparan "
            "el resultado contra valores fijos. Necesitas pasar al menos 7 de "
            "8 para que el capstone cuente como completado y desbloquee el "
            "certificado del Track 2."
        ),
        "requirements": [
            {
                "id": "R1",
                "text": (
                    "`parsear_ventas(csv_text: str) -> pd.DataFrame` lee el CSV "
                    "(via `pd.read_csv` + `StringIO`) y devuelve un DataFrame "
                    "con columnas `fecha, sucursal, producto, categoria, "
                    "unidades, precio_unit, ingreso`. La columna `fecha` debe "
                    "quedar como `datetime64` (usa `parse_dates`)."
                ),
            },
            {
                "id": "R2",
                "text": (
                    "`ingreso_total(df) -> float` retorna la suma de la columna "
                    "`ingreso`. Para un DataFrame vacio retorna `0.0` (no "
                    "lanza excepcion)."
                ),
            },
            {
                "id": "R3",
                "text": (
                    "`ranking_sucursales(df) -> pd.DataFrame` agrupa por "
                    "`sucursal`, suma `ingreso` y devuelve un DataFrame con "
                    "indice `sucursal` y columna `ingreso`, ordenado "
                    "descendente."
                ),
            },
            {
                "id": "R4",
                "text": (
                    "`top_producto(df) -> str` agrupa por `producto`, suma "
                    "`ingreso` y devuelve el nombre del producto que mas "
                    "ingreso genero (idxmax)."
                ),
            },
            {
                "id": "R5",
                "text": (
                    "`ingreso_por_categoria(df) -> dict` agrupa por `categoria`, "
                    "suma `ingreso` y devuelve un `dict` `categoria -> total`."
                ),
            },
            {
                "id": "R6",
                "text": (
                    "`unidades_por_dia(df) -> pd.Series` agrupa por `fecha`, "
                    "suma `unidades` y devuelve una Serie con `DatetimeIndex` "
                    "ordenado ascendente."
                ),
            },
            {
                "id": "R7",
                "text": (
                    "`dia_pico_unidades(df) -> pd.Timestamp` retorna la fecha "
                    "(Timestamp) con mas unidades vendidas (idxmax sobre "
                    "`unidades_por_dia`)."
                ),
            },
            {
                "id": "R8",
                "text": (
                    "`correlacion_unidades_ingreso(df) -> float` calcula la "
                    "correlacion de Pearson entre `unidades` e `ingreso`. "
                    "Devuelve un float en el rango [-1, 1]."
                ),
            },
        ],
        "starter_files": [
            {
                "path": "analisis.py",
                "editable": True,
                "content": (
                    '"""Funciones puras de analisis EDA sobre ventas-pyme."""\n'
                    "\n"
                    "import io\n"
                    "\n"
                    "import pandas as pd\n"
                    "\n"
                    "\n"
                    "def parsear_ventas(csv_text: str) -> pd.DataFrame:\n"
                    '    """Lee el CSV de ventas y devuelve un DataFrame.\n'
                    "\n"
                    "    La columna `fecha` debe quedar como datetime64.\n"
                    '    """\n'
                    "    # TODO: usa pd.read_csv con io.StringIO(csv_text) y\n"
                    "    # parse_dates=['fecha'] para obtener fechas tipadas.\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def ingreso_total(df: pd.DataFrame) -> float:\n"
                    '    """Suma de la columna ingreso. 0.0 si esta vacio."""\n'
                    "    # TODO: devolver float(df['ingreso'].sum()).\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def ranking_sucursales(df: pd.DataFrame) -> pd.DataFrame:\n"
                    '    """DataFrame con indice sucursal y col ingreso, desc."""\n'
                    "    # TODO: groupby('sucursal')['ingreso'].sum().sort_values\n"
                    "    # (ascending=False).to_frame()\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def top_producto(df: pd.DataFrame) -> str:\n"
                    '    """Producto con mayor ingreso total."""\n'
                    "    # TODO: groupby('producto')['ingreso'].sum().idxmax()\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def ingreso_por_categoria(df: pd.DataFrame) -> dict:\n"
                    '    """dict {categoria: total_ingreso}."""\n'
                    "    # TODO: groupby('categoria')['ingreso'].sum().to_dict()\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def unidades_por_dia(df: pd.DataFrame) -> pd.Series:\n"
                    '    """Serie con DatetimeIndex (asc) sumando unidades por fecha."""\n'
                    "    # TODO: groupby('fecha')['unidades'].sum().sort_index()\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def dia_pico_unidades(df: pd.DataFrame) -> pd.Timestamp:\n"
                    '    """Fecha (Timestamp) con mas unidades vendidas."""\n'
                    "    # TODO: unidades_por_dia(df).idxmax()\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def correlacion_unidades_ingreso(df: pd.DataFrame) -> float:\n"
                    '    """Pearson entre columnas unidades e ingreso."""\n'
                    "    # TODO: float(df['unidades'].corr(df['ingreso']))\n"
                    "    raise NotImplementedError\n"
                ),
            },
            {
                "path": "notebook.py",
                "editable": True,
                "content": (
                    '"""Script de exploracion libre (no se evalua).\n'
                    "\n"
                    "Usa este archivo para cargar el dataset real y probar las\n"
                    "funciones de analisis.py contra los 60 dias de ventas.\n"
                    '"""\n'
                    "\n"
                    "import asyncio\n"
                    "\n"
                    "import pycode\n"
                    "\n"
                    "from analisis import (\n"
                    "    parsear_ventas,\n"
                    "    ingreso_total,\n"
                    "    ranking_sucursales,\n"
                    "    top_producto,\n"
                    "    ingreso_por_categoria,\n"
                    "    unidades_por_dia,\n"
                    "    dia_pico_unidades,\n"
                    "    correlacion_unidades_ingreso,\n"
                    ")\n"
                    "\n"
                    "\n"
                    "async def main() -> None:\n"
                    '    csv_text = await pycode.fetch_dataset_csv("ventas-pyme")\n'
                    "    df = parsear_ventas(csv_text)\n"
                    '    print("ingreso total =", ingreso_total(df))\n'
                    '    print("top producto =", top_producto(df))\n'
                    '    print("dia pico =", dia_pico_unidades(df))\n'
                    '    print("correlacion =", correlacion_unidades_ingreso(df))\n'
                    "\n"
                    "\n"
                    'if __name__ == "__main__":\n'
                    "    asyncio.run(main())\n"
                ),
            },
        ],
        "hidden_tests": [
            {
                "name": "parsear_ventas retorna DataFrame con fecha datetime64",
                "code": (
                    "from analisis import parsear_ventas\n"
                    "import pandas as pd\n"
                    "csv = (\n"
                    '    "fecha,sucursal,producto,categoria,unidades,precio_unit,ingreso\\n"\n'
                    '    "2026-01-01,centro,cafe,bebida,5,3.5,17.5\\n"\n'
                    '    "2026-01-02,norte,torta,comida,2,4.5,9.0\\n"\n'
                    ")\n"
                    "df = parsear_ventas(csv)\n"
                    "assert isinstance(df, pd.DataFrame)\n"
                    "assert list(df.columns) == ['fecha','sucursal','producto','categoria','unidades','precio_unit','ingreso']\n"
                    "assert str(df['fecha'].dtype).startswith('datetime64'), df.dtypes\n"
                    "assert len(df) == 2"
                ),
            },
            {
                "name": "ingreso_total suma columna ingreso (y 0 si esta vacio)",
                "code": (
                    "from analisis import parsear_ventas, ingreso_total\n"
                    "import math\n"
                    "csv = (\n"
                    '    "fecha,sucursal,producto,categoria,unidades,precio_unit,ingreso\\n"\n'
                    '    "2026-01-01,centro,cafe,bebida,5,3.5,17.5\\n"\n'
                    '    "2026-01-01,norte,torta,comida,2,4.5,9.0\\n"\n'
                    '    "2026-01-02,centro,cafe,bebida,3,3.5,10.5\\n"\n'
                    '    "2026-01-02,sur,sandwich,comida,4,6.0,24.0\\n"\n'
                    '    "2026-01-03,centro,te,bebida,2,2.5,5.0\\n"\n'
                    '    "2026-01-03,norte,galletas,comida,6,1.8,10.8\\n"\n'
                    ")\n"
                    "df = parsear_ventas(csv)\n"
                    "assert math.isclose(ingreso_total(df), 76.8, abs_tol=1e-6)\n"
                    'vacio = parsear_ventas("fecha,sucursal,producto,categoria,unidades,precio_unit,ingreso\\n")\n'
                    "assert math.isclose(ingreso_total(vacio), 0.0, abs_tol=1e-6)"
                ),
            },
            {
                "name": "ranking_sucursales ordena descendente por ingreso",
                "code": (
                    "from analisis import parsear_ventas, ranking_sucursales\n"
                    "import math\n"
                    "csv = (\n"
                    '    "fecha,sucursal,producto,categoria,unidades,precio_unit,ingreso\\n"\n'
                    '    "2026-01-01,centro,cafe,bebida,5,3.5,17.5\\n"\n'
                    '    "2026-01-01,norte,torta,comida,2,4.5,9.0\\n"\n'
                    '    "2026-01-02,centro,cafe,bebida,3,3.5,10.5\\n"\n'
                    '    "2026-01-02,sur,sandwich,comida,4,6.0,24.0\\n"\n'
                    '    "2026-01-03,centro,te,bebida,2,2.5,5.0\\n"\n'
                    '    "2026-01-03,norte,galletas,comida,6,1.8,10.8\\n"\n'
                    ")\n"
                    "df = parsear_ventas(csv)\n"
                    "rs = ranking_sucursales(df)\n"
                    "assert list(rs.index) == ['centro','sur','norte'], rs.index.tolist()\n"
                    "assert math.isclose(rs.loc['centro','ingreso'], 33.0)\n"
                    "assert math.isclose(rs.loc['sur','ingreso'], 24.0)\n"
                    "assert math.isclose(rs.loc['norte','ingreso'], 19.8)"
                ),
            },
            {
                "name": "top_producto devuelve cafe (mayor ingreso acumulado)",
                "code": (
                    "from analisis import parsear_ventas, top_producto\n"
                    "csv = (\n"
                    '    "fecha,sucursal,producto,categoria,unidades,precio_unit,ingreso\\n"\n'
                    '    "2026-01-01,centro,cafe,bebida,5,3.5,17.5\\n"\n'
                    '    "2026-01-01,norte,torta,comida,2,4.5,9.0\\n"\n'
                    '    "2026-01-02,centro,cafe,bebida,3,3.5,10.5\\n"\n'
                    '    "2026-01-02,sur,sandwich,comida,4,6.0,24.0\\n"\n'
                    '    "2026-01-03,centro,te,bebida,2,2.5,5.0\\n"\n'
                    '    "2026-01-03,norte,galletas,comida,6,1.8,10.8\\n"\n'
                    ")\n"
                    "df = parsear_ventas(csv)\n"
                    "tp = top_producto(df)\n"
                    "assert tp == 'cafe', tp"
                ),
            },
            {
                "name": "ingreso_por_categoria agrupa bebida y comida",
                "code": (
                    "from analisis import parsear_ventas, ingreso_por_categoria\n"
                    "import math\n"
                    "csv = (\n"
                    '    "fecha,sucursal,producto,categoria,unidades,precio_unit,ingreso\\n"\n'
                    '    "2026-01-01,centro,cafe,bebida,5,3.5,17.5\\n"\n'
                    '    "2026-01-01,norte,torta,comida,2,4.5,9.0\\n"\n'
                    '    "2026-01-02,centro,cafe,bebida,3,3.5,10.5\\n"\n'
                    '    "2026-01-02,sur,sandwich,comida,4,6.0,24.0\\n"\n'
                    '    "2026-01-03,centro,te,bebida,2,2.5,5.0\\n"\n'
                    '    "2026-01-03,norte,galletas,comida,6,1.8,10.8\\n"\n'
                    ")\n"
                    "df = parsear_ventas(csv)\n"
                    "ipc = ingreso_por_categoria(df)\n"
                    "assert isinstance(ipc, dict)\n"
                    "assert set(ipc.keys()) == {'bebida','comida'}, ipc\n"
                    "assert math.isclose(ipc['bebida'], 33.0)\n"
                    "assert math.isclose(ipc['comida'], 43.8)"
                ),
            },
            {
                "name": "unidades_por_dia tiene DatetimeIndex y suma por fecha",
                "code": (
                    "from analisis import parsear_ventas, unidades_por_dia\n"
                    "import pandas as pd\n"
                    "csv = (\n"
                    '    "fecha,sucursal,producto,categoria,unidades,precio_unit,ingreso\\n"\n'
                    '    "2026-01-01,centro,cafe,bebida,5,3.5,17.5\\n"\n'
                    '    "2026-01-01,norte,torta,comida,2,4.5,9.0\\n"\n'
                    '    "2026-01-02,centro,cafe,bebida,3,3.5,10.5\\n"\n'
                    '    "2026-01-02,sur,sandwich,comida,4,6.0,24.0\\n"\n'
                    '    "2026-01-03,centro,te,bebida,2,2.5,5.0\\n"\n'
                    '    "2026-01-03,norte,galletas,comida,6,1.8,10.8\\n"\n'
                    ")\n"
                    "df = parsear_ventas(csv)\n"
                    "upd = unidades_por_dia(df)\n"
                    "assert isinstance(upd, pd.Series), type(upd)\n"
                    "esperado_idx = list(pd.to_datetime(['2026-01-01','2026-01-02','2026-01-03']))\n"
                    "assert list(upd.index) == esperado_idx, upd.index.tolist()\n"
                    "assert int(upd.iloc[0]) == 7\n"
                    "assert int(upd.iloc[1]) == 7\n"
                    "assert int(upd.iloc[2]) == 8"
                ),
            },
            {
                "name": "dia_pico_unidades es 2026-01-03",
                "code": (
                    "from analisis import parsear_ventas, dia_pico_unidades\n"
                    "import pandas as pd\n"
                    "csv = (\n"
                    '    "fecha,sucursal,producto,categoria,unidades,precio_unit,ingreso\\n"\n'
                    '    "2026-01-01,centro,cafe,bebida,5,3.5,17.5\\n"\n'
                    '    "2026-01-01,norte,torta,comida,2,4.5,9.0\\n"\n'
                    '    "2026-01-02,centro,cafe,bebida,3,3.5,10.5\\n"\n'
                    '    "2026-01-02,sur,sandwich,comida,4,6.0,24.0\\n"\n'
                    '    "2026-01-03,centro,te,bebida,2,2.5,5.0\\n"\n'
                    '    "2026-01-03,norte,galletas,comida,6,1.8,10.8\\n"\n'
                    ")\n"
                    "df = parsear_ventas(csv)\n"
                    "dp = dia_pico_unidades(df)\n"
                    "assert dp == pd.Timestamp('2026-01-03'), dp"
                ),
            },
            {
                "name": "correlacion_unidades_ingreso es positiva en rango",
                "code": (
                    "from analisis import parsear_ventas, correlacion_unidades_ingreso\n"
                    "csv = (\n"
                    '    "fecha,sucursal,producto,categoria,unidades,precio_unit,ingreso\\n"\n'
                    '    "2026-01-01,centro,cafe,bebida,5,3.5,17.5\\n"\n'
                    '    "2026-01-01,norte,torta,comida,2,4.5,9.0\\n"\n'
                    '    "2026-01-02,centro,cafe,bebida,3,3.5,10.5\\n"\n'
                    '    "2026-01-02,sur,sandwich,comida,4,6.0,24.0\\n"\n'
                    '    "2026-01-03,centro,te,bebida,2,2.5,5.0\\n"\n'
                    '    "2026-01-03,norte,galletas,comida,6,1.8,10.8\\n"\n'
                    ")\n"
                    "df = parsear_ventas(csv)\n"
                    "c = correlacion_unidades_ingreso(df)\n"
                    "assert isinstance(c, float), type(c)\n"
                    "assert -1.0 <= c <= 1.0, c\n"
                    "assert 0.3 < c < 0.7, c"
                ),
            },
        ],
        "estimated_hours": 10,
        "difficulty": "intermediate",
        "order_index": 2,
    },
    {
        "slug": "track-3-diagnostico-ml",
        "track": "track-3",
        "title": "Diagnostico asistido: clasificador de tumores end-to-end",
        "short_description": (
            "Construye un pipeline de ML completo sobre el dataset breast "
            "cancer: split estratificado, escalado, LogisticRegression, "
            "metricas honestas, cross-validation, tuning de regularizacion, "
            "umbral de decision e interpretabilidad. Cierra el Track 3 de "
            "ML Clasico."
        ),
        "description": (
            "## Contexto\n\n"
            "Un hospital tiene mediciones de nucleos celulares (radio, "
            "textura, perimetro, area, ...) extraidas de imagenes de "
            "biopsias, y una etiqueta: tumor **maligno** (0) o **benigno** "
            "(1). Te piden un clasificador que ayude al equipo medico, pero "
            "**hecho bien**: sin data leakage, evaluado con metricas que "
            "importan en salud (no solo accuracy), con la regularizacion "
            "ajustada y con el umbral de decision bajo control.\n\n"
            "Usaras el dataset `breast_cancer` que trae sklearn "
            "(`load_breast_cancer`, 569 muestras x 30 features). Es el "
            "mismo que corre dentro de Pyodide, sin descargas externas.\n\n"
            "## Que integra este capstone\n\n"
            "Una funcion por cada idea del Track 3:\n\n"
            "- **ML 1** — split estratificado train/test.\n"
            "- **ML 3** — `StandardScaler` + `Pipeline` (escalado sin "
            "leakage).\n"
            "- **ML 2** — precision, recall, f1 y matriz de confusion.\n"
            "- **ML 6** — cross-validation y comparacion de "
            "hiperparametros (`C`).\n"
            "- **ML 8 / regresion logistica** — probabilidades, umbral de "
            "decision e interpretacion de coeficientes.\n\n"
            "## Estructura\n\n"
            "```\n"
            "diagnostico/\n"
            "  modelo.py      # Las 8 funciones puras que se evaluan\n"
            "  explora.py     # Script libre para experimentar (no se evalua)\n"
            "```\n\n"
            "## Reglas de oro (te las repetimos porque cuentan)\n\n"
            "- **Nunca** ajustes el `StandardScaler` con el test: va dentro "
            "del `Pipeline` para que `fit` toque solo train.\n"
            "- En salud, **recall** (no perder un maligno) suele pesar mas "
            "que accuracy. Reporta las cuatro metricas.\n"
            "- El umbral 0.5 no es sagrado: bajarlo captura mas positivos "
            "(mas recall, menos precision).\n\n"
            "## Como se evalua\n\n"
            "Al pulsar **Enviar capstone**, la plataforma corre 8 tests "
            "ocultos que invocan cada funcion con el dataset real y "
            "comparan contra rangos esperados (no floats exactos, para no "
            "romperse entre versiones de sklearn). No veras los tests, pero "
            "si cuantos pasaron y el error de los que fallen. Necesitas al "
            "menos **7 de 8** para completar el capstone y desbloquear el "
            "certificado del Track 3."
        ),
        "requirements": [
            {
                "id": "R1",
                "text": (
                    "`dividir_datos(X, y, test_size=0.2, seed=42) -> tuple` "
                    "hace un split **estratificado** (`stratify=y`, "
                    "`random_state=seed`) y devuelve "
                    "`(X_train, X_test, y_train, y_test)`."
                ),
            },
            {
                "id": "R2",
                "text": (
                    "`construir_pipeline(C=1.0) -> Pipeline` devuelve un "
                    "`Pipeline` con `StandardScaler` seguido de "
                    "`LogisticRegression(C=C, max_iter=5000, "
                    "random_state=42)` como ultimo paso."
                ),
            },
            {
                "id": "R3",
                "text": (
                    "`entrenar_evaluar(pipe, X_train, y_train, X_test, "
                    "y_test) -> dict` entrena el pipeline con train y "
                    "devuelve un dict con `accuracy`, `precision`, `recall` "
                    "y `f1` calculados sobre test."
                ),
            },
            {
                "id": "R4",
                "text": (
                    "`matriz_confusion(pipe, X_test, y_test) -> np.ndarray` "
                    "devuelve la matriz de confusion 2x2 "
                    "(`confusion_matrix`) del pipeline ya entrenado sobre "
                    "el test."
                ),
            },
            {
                "id": "R5",
                "text": (
                    "`cv_media(pipe, X, y, folds=5) -> float` devuelve la "
                    "media de `cross_val_score(pipe, X, y, cv=folds)`."
                ),
            },
            {
                "id": "R6",
                "text": (
                    "`comparar_C(X, y, valores_C, folds=5) -> dict` devuelve "
                    "`{C: cv_media}` para cada `C` en `valores_C` "
                    "(reutiliza `construir_pipeline` y `cv_media`)."
                ),
            },
            {
                "id": "R7",
                "text": (
                    "`predecir_con_umbral(pipe, X, umbral) -> np.ndarray` "
                    "devuelve un array de 0/1 marcando positivo (1) cuando "
                    "`predict_proba` de la clase 1 es `>= umbral`. El "
                    "pipeline ya viene entrenado."
                ),
            },
            {
                "id": "R8",
                "text": (
                    "`ranking_coeficientes(pipe, nombres) -> list` devuelve "
                    "una lista de tuplas `(nombre, magnitud)` con el valor "
                    "absoluto del coeficiente de cada feature, ordenada de "
                    "mayor a menor magnitud. El ultimo paso del pipeline es "
                    "la regresion logistica."
                ),
            },
        ],
        "starter_files": [
            {
                "path": "modelo.py",
                "editable": True,
                "content": (
                    '"""Clasificador de diagnostico end-to-end (Track 3).\n'
                    "\n"
                    "Implementa las 8 funciones puras. Cada una reutiliza la\n"
                    "API de sklearn que viste en las lecciones ML 1-8.\n"
                    '"""\n'
                    "\n"
                    "import numpy as np\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.metrics import (\n"
                    "    accuracy_score,\n"
                    "    confusion_matrix,\n"
                    "    f1_score,\n"
                    "    precision_score,\n"
                    "    recall_score,\n"
                    ")\n"
                    "from sklearn.model_selection import cross_val_score, train_test_split\n"
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "\n"
                    "\n"
                    "def dividir_datos(X, y, test_size=0.2, seed=42):\n"
                    '    """Split estratificado -> (X_train, X_test, y_train, y_test)."""\n'
                    "    # TODO: return train_test_split(X, y, test_size=test_size,\n"
                    "    #     random_state=seed, stratify=y)\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def construir_pipeline(C=1.0):\n"
                    '    """StandardScaler + LogisticRegression en un Pipeline."""\n'
                    "    # TODO: Pipeline([('sc', StandardScaler()),\n"
                    "    #     ('clf', LogisticRegression(C=C, max_iter=5000,\n"
                    "    #     random_state=42))])\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def entrenar_evaluar(pipe, X_train, y_train, X_test, y_test):\n"
                    '    """Entrena en train y devuelve dict de metricas en test."""\n'
                    "    # TODO: pipe.fit(X_train, y_train); pred = pipe.predict(X_test)\n"
                    "    # TODO: return {'accuracy': ..., 'precision': ...,\n"
                    "    #     'recall': ..., 'f1': ...} con floats\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def matriz_confusion(pipe, X_test, y_test):\n"
                    '    """Matriz de confusion 2x2 del pipeline ya entrenado."""\n'
                    "    # TODO: return confusion_matrix(y_test, pipe.predict(X_test))\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def cv_media(pipe, X, y, folds=5):\n"
                    '    """Media de cross_val_score con cv=folds."""\n'
                    "    # TODO: return float(cross_val_score(pipe, X, y, cv=folds).mean())\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def comparar_C(X, y, valores_C, folds=5):\n"
                    '    """dict {C: cv_media} probando cada C."""\n'
                    "    # TODO: return {C: cv_media(construir_pipeline(C=C), X, y, folds)\n"
                    "    #     for C in valores_C}\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def predecir_con_umbral(pipe, X, umbral):\n"
                    '    """Array 0/1: positivo si predict_proba clase 1 >= umbral."""\n'
                    "    # TODO: proba = pipe.predict_proba(X)[:, 1]\n"
                    "    # TODO: return (proba >= umbral).astype(int)\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def ranking_coeficientes(pipe, nombres):\n"
                    '    """[(nombre, |coef|)] ordenado desc por magnitud."""\n'
                    "    # TODO: modelo = pipe.steps[-1][1]; coefs = modelo.coef_[0]\n"
                    "    # TODO: pares = [(n, abs(float(c))) for n, c in zip(nombres, coefs)]\n"
                    "    # TODO: return sorted(pares, key=lambda t: t[1], reverse=True)\n"
                    "    raise NotImplementedError\n"
                ),
            },
            {
                "path": "explora.py",
                "editable": True,
                "content": (
                    '"""Script de exploracion libre (no se evalua).\n'
                    "\n"
                    "Carga el dataset real y prueba tus funciones de modelo.py.\n"
                    '"""\n'
                    "\n"
                    "from sklearn.datasets import load_breast_cancer\n"
                    "\n"
                    "from modelo import (\n"
                    "    comparar_C,\n"
                    "    construir_pipeline,\n"
                    "    cv_media,\n"
                    "    dividir_datos,\n"
                    "    entrenar_evaluar,\n"
                    "    matriz_confusion,\n"
                    "    predecir_con_umbral,\n"
                    "    ranking_coeficientes,\n"
                    ")\n"
                    "\n"
                    "data = load_breast_cancer()\n"
                    "X, y = data.data, data.target\n"
                    "nombres = list(data.feature_names)\n"
                    "\n"
                    "X_tr, X_te, y_tr, y_te = dividir_datos(X, y)\n"
                    "pipe = construir_pipeline()\n"
                    "print(entrenar_evaluar(pipe, X_tr, y_tr, X_te, y_te))\n"
                    "print(matriz_confusion(pipe, X_te, y_te))\n"
                    "print('CV:', cv_media(construir_pipeline(), X, y))\n"
                    "print('C:', comparar_C(X, y, [0.01, 0.1, 1.0, 10.0]))\n"
                    "print('top features:', ranking_coeficientes(pipe, nombres)[:5])\n"
                ),
            },
        ],
        "hidden_tests": [
            {
                "name": "dividir_datos: shapes 455/114 y estratificacion",
                "code": (
                    "from sklearn.datasets import load_breast_cancer\n"
                    "from modelo import dividir_datos\n"
                    "X, y = load_breast_cancer(return_X_y=True)\n"
                    "Xtr, Xte, ytr, yte = dividir_datos(X, y)\n"
                    "assert Xtr.shape == (455, 30), Xtr.shape\n"
                    "assert Xte.shape == (114, 30), Xte.shape\n"
                    "assert len(ytr) == 455 and len(yte) == 114\n"
                    "assert abs(ytr.mean() - yte.mean()) < 0.02, (ytr.mean(), yte.mean())"
                ),
            },
            {
                "name": "construir_pipeline: Pipeline con scaler + logreg",
                "code": (
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from modelo import construir_pipeline\n"
                    "pipe = construir_pipeline()\n"
                    "assert isinstance(pipe, Pipeline), type(pipe)\n"
                    "pasos = [s for _, s in pipe.steps]\n"
                    "assert any(isinstance(s, StandardScaler) for s in pasos), pipe.steps\n"
                    "assert isinstance(pipe.steps[-1][1], LogisticRegression), pipe.steps"
                ),
            },
            {
                "name": "entrenar_evaluar: 4 metricas > 0.90",
                "code": (
                    "from sklearn.datasets import load_breast_cancer\n"
                    "from modelo import dividir_datos, construir_pipeline, entrenar_evaluar\n"
                    "X, y = load_breast_cancer(return_X_y=True)\n"
                    "Xtr, Xte, ytr, yte = dividir_datos(X, y)\n"
                    "m = entrenar_evaluar(construir_pipeline(), Xtr, ytr, Xte, yte)\n"
                    "assert isinstance(m, dict), type(m)\n"
                    "for k in ('accuracy', 'precision', 'recall', 'f1'):\n"
                    "    assert k in m, k\n"
                    "    assert 0.90 < float(m[k]) <= 1.0, (k, m[k])"
                ),
            },
            {
                "name": "matriz_confusion: 2x2, suma 114, diagonal domina",
                "code": (
                    "import numpy as np\n"
                    "from sklearn.datasets import load_breast_cancer\n"
                    "from modelo import dividir_datos, construir_pipeline, matriz_confusion\n"
                    "X, y = load_breast_cancer(return_X_y=True)\n"
                    "Xtr, Xte, ytr, yte = dividir_datos(X, y)\n"
                    "pipe = construir_pipeline().fit(Xtr, ytr)\n"
                    "cm = np.asarray(matriz_confusion(pipe, Xte, yte))\n"
                    "assert cm.shape == (2, 2), cm.shape\n"
                    "assert cm.sum() == 114, cm.sum()\n"
                    "assert cm[0, 0] + cm[1, 1] > 100, cm"
                ),
            },
            {
                "name": "cv_media: float en (0.95, 1.0]",
                "code": (
                    "from sklearn.datasets import load_breast_cancer\n"
                    "from modelo import construir_pipeline, cv_media\n"
                    "X, y = load_breast_cancer(return_X_y=True)\n"
                    "val = cv_media(construir_pipeline(), X, y, folds=5)\n"
                    "assert isinstance(val, float), type(val)\n"
                    "assert 0.95 < val <= 1.0, val"
                ),
            },
            {
                "name": "comparar_C: dict, C sobre-regularizado rinde peor",
                "code": (
                    "from sklearn.datasets import load_breast_cancer\n"
                    "from modelo import comparar_C\n"
                    "X, y = load_breast_cancer(return_X_y=True)\n"
                    "res = comparar_C(X, y, [0.01, 1.0], folds=5)\n"
                    "assert isinstance(res, dict), type(res)\n"
                    "assert set(res.keys()) == {0.01, 1.0}, list(res.keys())\n"
                    "assert res[0.01] < res[1.0], res\n"
                    "assert res[1.0] > 0.95, res[1.0]"
                ),
            },
            {
                "name": "predecir_con_umbral: monotono, 0->todo, 1->nada",
                "code": (
                    "import numpy as np\n"
                    "from sklearn.datasets import load_breast_cancer\n"
                    "from modelo import dividir_datos, construir_pipeline, predecir_con_umbral\n"
                    "X, y = load_breast_cancer(return_X_y=True)\n"
                    "Xtr, Xte, ytr, yte = dividir_datos(X, y)\n"
                    "pipe = construir_pipeline().fit(Xtr, ytr)\n"
                    "bajo = np.asarray(predecir_con_umbral(pipe, Xte, 0.0))\n"
                    "medio = np.asarray(predecir_con_umbral(pipe, Xte, 0.5))\n"
                    "alto = np.asarray(predecir_con_umbral(pipe, Xte, 1.0))\n"
                    "assert set(np.unique(bajo)).issubset({0, 1})\n"
                    "assert int(bajo.sum()) == 114, bajo.sum()\n"
                    "assert int(alto.sum()) == 0, alto.sum()\n"
                    "assert alto.sum() <= medio.sum() <= bajo.sum()"
                ),
            },
            {
                "name": "ranking_coeficientes: 30 pares ordenados desc",
                "code": (
                    "from sklearn.datasets import load_breast_cancer\n"
                    "from modelo import dividir_datos, construir_pipeline, ranking_coeficientes\n"
                    "data = load_breast_cancer()\n"
                    "X, y = data.data, data.target\n"
                    "nombres = list(data.feature_names)\n"
                    "Xtr, Xte, ytr, yte = dividir_datos(X, y)\n"
                    "pipe = construir_pipeline().fit(Xtr, ytr)\n"
                    "rank = ranking_coeficientes(pipe, nombres)\n"
                    "assert len(rank) == 30, len(rank)\n"
                    "assert all(isinstance(n, str) for n, _ in rank)\n"
                    "mags = [float(m) for _, m in rank]\n"
                    "assert mags == sorted(mags, reverse=True), mags[:5]\n"
                    "assert mags[0] > 0"
                ),
            },
        ],
        "estimated_hours": 10,
        "difficulty": "advanced",
        "order_index": 3,
    },
]


async def seed_capstones_if_empty(db: AsyncSession) -> int:
    """Inserta capstones que falten (idempotente por slug)."""
    inserted = 0
    for data in CAPSTONES:
        existing = await db.execute(
            select(Capstone.id).where(Capstone.slug == data["slug"])
        )
        if existing.scalar_one_or_none() is not None:
            continue
        db.add(Capstone(**data))
        inserted += 1

    if inserted:
        await db.commit()
    return inserted
