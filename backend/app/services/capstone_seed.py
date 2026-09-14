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
    {
        "slug": "track-4-mlp-desde-cero",
        "track": "track-4",
        "title": "Red neuronal desde cero: tu propia mini-libreria de deep learning",
        "short_description": (
            "Construye una red neuronal completa con numpy puro: "
            "inicializacion, forward, perdida, backprop encadenado, "
            "descenso de gradiente y un bucle de entrenamiento que "
            "resuelve un problema no lineal. Cierra el Track 4 de Deep "
            "Learning."
        ),
        "description": (
            "## Contexto\n\n"
            "A lo largo del Track 4 construiste cada pieza de una red "
            "neuronal (neurona, perdida, backprop, training loop, MLP). "
            "Ahora las juntas en una **mini-libreria** coherente: un "
            "modulo `red.py` con funciones puras que, combinadas, "
            "entrenan un perceptron multicapa de 2 capas para clasificar "
            "datos **no linealmente separables** — todo con numpy, sin "
            "PyTorch ni sklearn.\n\n"
            "## Que integra este capstone\n\n"
            "- **DL 1** — forward de una capa (`X @ W + b`) y "
            "activaciones (relu, sigmoid).\n"
            "- **DL 2** — perdida BCE con clip.\n"
            "- **DL 3** — backprop encadenado por 2 capas (verificado con "
            "gradient checking).\n"
            "- **DL 4** — descenso de gradiente y bucle de "
            "entrenamiento.\n"
            "- **DL 5** — arquitectura MLP (capa oculta relu + salida "
            "sigmoid) que resuelve lo no lineal.\n\n"
            "## Arquitectura\n\n"
            "```\n"
            "X --[W1,b1]--> relu --[W2,b2]--> sigmoid --> p (probabilidad)\n"
            "```\n\n"
            "Los pesos viven en un dict `params = {'W1','b1','W2','b2'}`. "
            "El `forward` devuelve tambien un `cache` con los valores "
            "intermedios que el `backward` necesita.\n\n"
            "## Estructura\n\n"
            "```\n"
            "mlp/\n"
            "  red.py       # La mini-libreria: las 8 funciones que se evaluan\n"
            "  demo.py      # Script libre para experimentar (no se evalua)\n"
            "```\n\n"
            "## Como se evalua\n\n"
            "Al pulsar **Enviar capstone**, la plataforma corre 8 tests "
            "ocultos: verifican cada funcion por separado, hacen "
            "**gradient checking** de tu backprop contra el gradiente "
            "numerico, y al final entrenan tu red sobre un dataset no "
            "lineal comprobando que alcanza **mas del 95% de "
            "accuracy**. Necesitas pasar al menos **7 de 8** para "
            "completar el capstone y desbloquear el certificado del "
            "Track 4."
        ),
        "requirements": [
            {
                "id": "R1",
                "text": (
                    "`inicializar_pesos(d_in, d_hidden, seed=0) -> dict` "
                    "devuelve `{'W1','b1','W2','b2'}` con `W1` shape "
                    "`(d_in, d_hidden)` y `W2` shape `(d_hidden, 1)` "
                    "inicializados al azar (usa "
                    "`np.random.default_rng(seed)`), y los bias en cero. "
                    "No inicialices W en ceros (symmetry breaking)."
                ),
            },
            {
                "id": "R2",
                "text": (
                    "`forward(X, params) -> (p, cache)` calcula "
                    "`z1 = X@W1+b1`, `h = relu(z1)`, `z2 = h@W2+b2`, "
                    "`p = sigmoid(z2)`, y devuelve las probabilidades `p` "
                    "junto a un `cache` (dict) con al menos `z1` y `h` "
                    "para el backward."
                ),
            },
            {
                "id": "R3",
                "text": (
                    "`bce(y, p) -> float` calcula la binary cross-entropy "
                    "media, recortando `p` a `[1e-12, 1-1e-12]` para "
                    "evitar `log(0)`."
                ),
            },
            {
                "id": "R4",
                "text": (
                    "`backward(y, params, cache) -> dict` devuelve "
                    "`{'dW1','db1','dW2','db2'}` con el backprop "
                    "encadenado: `dz2=(p-y)/N`, `dW2=h.T@dz2`, "
                    "`dh=dz2@W2.T`, `dz1=dh*(z1>0)`, `dW1=X.T@dz1`. Debe "
                    "coincidir con el gradiente numerico."
                ),
            },
            {
                "id": "R5",
                "text": (
                    "`actualizar(params, grads, lr) -> dict` devuelve los "
                    "pesos actualizados: cada `param - lr * grad` "
                    "correspondiente (W1 con dW1, etc.)."
                ),
            },
            {
                "id": "R6",
                "text": (
                    "`entrenar(X, y, d_hidden=8, lr=0.5, epocas=3000, "
                    "seed=0) -> (params, historial)` inicializa los "
                    "pesos y en cada epoca hace forward, guarda la BCE, "
                    "backward y actualiza. Devuelve los pesos finales y "
                    "la lista de perdidas."
                ),
            },
            {
                "id": "R7",
                "text": (
                    "`predecir(X, params) -> np.ndarray` devuelve las "
                    "etiquetas 0/1 (probabilidad `> 0.5`) con shape "
                    "`(N, 1)`."
                ),
            },
            {
                "id": "R8",
                "text": (
                    "`accuracy(y, pred) -> float` devuelve la fraccion de "
                    "aciertos entre etiquetas verdaderas y predichas."
                ),
            },
        ],
        "starter_files": [
            {
                "path": "red.py",
                "editable": True,
                "content": (
                    '"""Mini-libreria de red neuronal (MLP de 2 capas) con numpy."""\n'
                    "\n"
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def sigmoid(z):\n"
                    "    return 1.0 / (1.0 + np.exp(-np.asarray(z, float)))\n"
                    "\n"
                    "\n"
                    "def relu(z):\n"
                    "    return np.maximum(0.0, np.asarray(z, float))\n"
                    "\n"
                    "\n"
                    "def inicializar_pesos(d_in, d_hidden, seed=0):\n"
                    '    """Pesos al azar (symmetry breaking) y bias en cero."""\n'
                    "    rng = np.random.default_rng(seed)\n"
                    "    # TODO: return {'W1': rng.normal(size=(d_in, d_hidden)) * 0.5,\n"
                    "    #   'b1': np.zeros(d_hidden),\n"
                    "    #   'W2': rng.normal(size=(d_hidden, 1)) * 0.5,\n"
                    "    #   'b2': np.zeros(1)}\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def forward(X, params):\n"
                    '    """Devuelve (p, cache). cache guarda z1 y h para el backward."""\n'
                    "    # TODO: z1 = X @ params['W1'] + params['b1']; h = relu(z1)\n"
                    "    # TODO: p = sigmoid(h @ params['W2'] + params['b2'])\n"
                    "    # TODO: return p, {'X': np.asarray(X, float), 'z1': z1, 'h': h, 'p': p}\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def bce(y, p):\n"
                    '    """Binary cross-entropy media, con clip."""\n'
                    "    # TODO: y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    # TODO: pc = np.clip(np.asarray(p, float).reshape(-1, 1), 1e-12, 1 - 1e-12)\n"
                    "    # TODO: return float(-np.mean(y*np.log(pc) + (1-y)*np.log(1-pc)))\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def backward(y, params, cache):\n"
                    '    """Backprop encadenado. Devuelve {dW1, db1, dW2, db2}."""\n'
                    "    # TODO: y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    # TODO: X, z1, h, p = cache['X'], cache['z1'], cache['h'], cache['p']\n"
                    "    # TODO: N = X.shape[0]; dz2 = (p - y) / N\n"
                    "    # TODO: dW2 = h.T @ dz2; db2 = dz2.sum(axis=0)\n"
                    "    # TODO: dh = dz2 @ params['W2'].T; dz1 = dh * (z1 > 0)\n"
                    "    # TODO: dW1 = X.T @ dz1; db1 = dz1.sum(axis=0)\n"
                    "    # TODO: return {'dW1': dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def actualizar(params, grads, lr):\n"
                    '    """params - lr * grad, para cada peso."""\n'
                    "    # TODO: return {k: params[k] - lr * grads['d' + k] for k in params}\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def entrenar(X, y, d_hidden=8, lr=0.5, epocas=3000, seed=0):\n"
                    '    """Bucle de entrenamiento. Devuelve (params, historial)."""\n'
                    "    X = np.asarray(X, float)\n"
                    "    y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    params = inicializar_pesos(X.shape[1], d_hidden, seed)\n"
                    "    historial = []\n"
                    "    # TODO: for _ in range(epocas):\n"
                    "    #   p, cache = forward(X, params); historial.append(bce(y, p))\n"
                    "    #   grads = backward(y, params, cache); params = actualizar(params, grads, lr)\n"
                    "    return params, historial\n"
                    "\n"
                    "\n"
                    "def predecir(X, params):\n"
                    '    """Etiquetas 0/1 (p > 0.5), shape (N, 1)."""\n'
                    "    # TODO: p, _ = forward(X, params); return (p > 0.5).astype(int)\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def accuracy(y, pred):\n"
                    '    """Fraccion de aciertos."""\n'
                    "    # TODO: y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    # TODO: pred = np.asarray(pred, float).reshape(-1, 1)\n"
                    "    # TODO: return float(np.mean(pred == y))\n"
                    "    raise NotImplementedError\n"
                ),
            },
            {
                "path": "demo.py",
                "editable": True,
                "content": (
                    '"""Experimenta libremente (no se evalua).\n'
                    "\n"
                    "Genera un dataset no lineal y entrena tu red.\n"
                    '"""\n'
                    "\n"
                    "import numpy as np\n"
                    "\n"
                    "from red import entrenar, predecir, accuracy\n"
                    "\n"
                    "rng = np.random.default_rng(42)\n"
                    "n = 30\n"
                    "\n"
                    "\n"
                    "def blob(cx, cy):\n"
                    "    return rng.normal([cx, cy], 0.15, size=(n, 2))\n"
                    "\n"
                    "\n"
                    "X = np.vstack([blob(0, 0), blob(1, 1), blob(0, 1), blob(1, 0)])\n"
                    "y = np.concatenate([np.zeros(2 * n), np.ones(2 * n)]).reshape(-1, 1)\n"
                    "params, hist = entrenar(X, y, d_hidden=8, lr=0.5, epocas=3000, seed=0)\n"
                    "print('perdida inicial->final:', hist[0], hist[-1])\n"
                    "print('accuracy:', accuracy(y, predecir(X, params)))\n"
                ),
            },
        ],
        "hidden_tests": [
            {
                "name": "inicializar_pesos: shapes + symmetry breaking",
                "code": (
                    "from red import inicializar_pesos\n"
                    "import numpy as np\n"
                    "p = inicializar_pesos(2, 8, seed=0)\n"
                    "assert p['W1'].shape == (2, 8), p['W1'].shape\n"
                    "assert p['W2'].shape == (8, 1), p['W2'].shape\n"
                    "assert np.asarray(p['b1']).shape == (8,)\n"
                    "assert not np.allclose(p['W1'], 0), 'W1 no debe ser todo ceros'"
                ),
            },
            {
                "name": "forward: (p, cache), p en (0,1)",
                "code": (
                    "from red import inicializar_pesos, forward\n"
                    "import numpy as np\n"
                    "X = np.random.default_rng(1).normal(size=(5, 2))\n"
                    "params = inicializar_pesos(2, 8, seed=0)\n"
                    "p, cache = forward(X, params)\n"
                    "p = np.asarray(p)\n"
                    "assert p.shape == (5, 1), p.shape\n"
                    "assert np.all((p > 0) & (p < 1))\n"
                    "for k in ('z1', 'h'):\n"
                    "    assert k in cache, k"
                ),
            },
            {
                "name": "bce: valores conocidos y clip finito",
                "code": (
                    "from red import bce\n"
                    "import numpy as np\n"
                    "assert abs(bce([1], [0.9]) - 0.105360516) < 1e-5, bce([1], [0.9])\n"
                    "assert bce([1], [0.01]) > bce([1], [0.99])\n"
                    "assert np.isfinite(bce([1], [1.0]))"
                ),
            },
            {
                "name": "backward: gradient checking en dW1",
                "code": (
                    "from red import inicializar_pesos, forward, backward, bce\n"
                    "import numpy as np\n"
                    "rng = np.random.default_rng(0)\n"
                    "X = rng.normal(size=(6, 2))\n"
                    "y = (rng.normal(size=(6, 1)) > 0).astype(float)\n"
                    "params = inicializar_pesos(2, 5, seed=2)\n"
                    "p, cache = forward(X, params)\n"
                    "grads = backward(y, params, cache)\n"
                    "dW1 = np.asarray(grads['dW1'])\n"
                    "assert dW1.shape == params['W1'].shape\n"
                    "def loss(W1):\n"
                    "    q = dict(params); q['W1'] = W1\n"
                    "    pp, _ = forward(X, q)\n"
                    "    return bce(y, pp)\n"
                    "h = 1e-5\n"
                    "num = np.zeros_like(params['W1'])\n"
                    "for i in range(params['W1'].shape[0]):\n"
                    "    for j in range(params['W1'].shape[1]):\n"
                    "        Wp = params['W1'].copy(); Wp[i, j] += h\n"
                    "        Wm = params['W1'].copy(); Wm[i, j] -= h\n"
                    "        num[i, j] = (loss(Wp) - loss(Wm)) / (2 * h)\n"
                    "assert np.allclose(dW1, num, atol=1e-4), (dW1.ravel()[:3], num.ravel()[:3])"
                ),
            },
            {
                "name": "actualizar: params -= lr*grad",
                "code": (
                    "from red import actualizar\n"
                    "import numpy as np\n"
                    "params = {'W1': np.ones((2, 2)), 'b1': np.zeros(2), 'W2': np.ones((2, 1)), 'b2': np.zeros(1)}\n"
                    "grads = {'dW1': np.ones((2, 2)), 'db1': np.ones(2), 'dW2': np.ones((2, 1)), 'db2': np.ones(1)}\n"
                    "out = actualizar(params, grads, 0.1)\n"
                    "assert np.allclose(out['W1'], 0.9), out['W1']\n"
                    "assert np.allclose(out['b1'], -0.1)"
                ),
            },
            {
                "name": "predecir: 0/1 shape (N,1)",
                "code": (
                    "from red import inicializar_pesos, predecir\n"
                    "import numpy as np\n"
                    "X = np.random.default_rng(3).normal(size=(7, 2))\n"
                    "params = inicializar_pesos(2, 8, seed=0)\n"
                    "pred = np.asarray(predecir(X, params))\n"
                    "assert pred.shape == (7, 1), pred.shape\n"
                    "assert set(np.unique(pred)).issubset({0, 1})"
                ),
            },
            {
                "name": "accuracy: fraccion correcta",
                "code": (
                    "from red import accuracy\n"
                    "assert accuracy([1, 0, 1, 0], [[1], [0], [0], [0]]) == 0.75\n"
                    "assert accuracy([[1], [1]], [[1], [1]]) == 1.0"
                ),
            },
            {
                "name": "entrenar: resuelve dataset no lineal (acc > 0.95)",
                "code": (
                    "from red import entrenar, predecir, accuracy\n"
                    "import numpy as np\n"
                    "rng = np.random.default_rng(42)\n"
                    "n = 30\n"
                    "def blob(cx, cy):\n"
                    "    return rng.normal([cx, cy], 0.15, size=(n, 2))\n"
                    "X = np.vstack([blob(0, 0), blob(1, 1), blob(0, 1), blob(1, 0)])\n"
                    "y = np.concatenate([np.zeros(2 * n), np.ones(2 * n)]).reshape(-1, 1)\n"
                    "params, hist = entrenar(X, y, d_hidden=8, lr=0.5, epocas=3000, seed=0)\n"
                    "assert hist[-1] < hist[0], (hist[0], hist[-1])\n"
                    "acc = accuracy(y, predecir(X, params))\n"
                    "assert acc > 0.95, acc"
                ),
            },
        ],
        "estimated_hours": 12,
        "difficulty": "advanced",
        "order_index": 4,
    },
    {
        "slug": "track-5-nebula-rag",
        "track": "track-5",
        "title": "Nebula RAG: el asistente completo",
        "short_description": (
            "Construye el asistente de atencion al cliente de Nebula en cinco modulos: recuperacion con umbral y citas, un agente que consulta pedidos, un router que decide entre los dos y una evaluacion automatica. Se corrige con un LLM falso; el LLM real queda como paso opcional."
        ),
        "description": (
            "## Contexto\n"
            "\n"
            'Nebula, la tienda online de las lecciones AI 4-6, quiere poner su asistente delante de clientes reales. Tiene dos tipos de preguntas: las que se responden con sus **documentos** ("¿cuanto tarda el envio?") y las que necesitan **datos vivos** ("¿donde esta mi pedido 1001?"). Y antes de publicarlo quiere una **evaluacion** que diga, con numeros, si funciona.\n'
            "\n"
            "Vas a construir el sistema entero, separado en modulos como se haria en un proyecto real.\n"
            "\n"
            "## Que integra este capstone\n"
            "\n"
            "- **AI 1-2**: embeddings de bolsa de palabras y similitud coseno para recuperar.\n"
            '- **AI 3-4**: prompt con fuentes numeradas, umbral de relevancia ("no lo se" sin llamar al LLM) y citas verificables.\n'
            "- **AI 5**: un agente con una herramienta, que valida los argumentos, captura los errores y no entra en bucle.\n"
            "- **AI 6**: una evaluacion con metricas automaticas (cobertura de datos clave, recall de fuentes) y un LLM juez cuyo veredicto se valida.\n"
            "\n"
            "## Arquitectura\n"
            "\n"
            "```\n"
            "pregunta ──> nebula.atender ──┬── ¿numero de pedido? ──> herramientas.ejecutar_agente ──> consultar_pedido\n"
            "                              │\n"
            "                              └── si no ──> asistente.responder ──> recuperacion.recuperar\n"
            "                                                                └──> llm_fn (con fuentes numeradas)\n"
            "\n"
            "evaluacion.evaluar(casos, sistema_fn, juez_fn) ──> tasa de aprobados + casos sin veredicto\n"
            "```\n"
            "\n"
            "Ninguna funcion llama al LLM por su cuenta: **todas reciben `llm_fn`**, una funcion `async` que toma un prompt y devuelve texto. Esa inyeccion es lo que permite corregir el proyecto con un LLM falso (determinista y gratis) y usar el real sin cambiar una linea.\n"
            "\n"
            "## Estructura\n"
            "\n"
            "```\n"
            "recuperacion.py   tokenizar, embed_bow, construir_indice, recuperar      (R1-R2)\n"
            "asistente.py      prompt_con_fuentes, extraer_citas, responder           (R3-R4)\n"
            "herramientas.py   crear_herramientas, parsear_accion,\n"
            "                  ejecutar_herramienta, ejecutar_agente                  (R5-R7)\n"
            "nebula.py         atender: el router                                     (R8)\n"
            "evaluacion.py     contiene_datos, puntuar_fuentes,\n"
            "                  parsear_veredicto, evaluar                             (R9-R10)\n"
            "datos.py          documentos, pedidos y casos de Nebula (ya escrito)\n"
            "demo.py           paso opcional con el LLM real (no se evalua)\n"
            "```\n"
            "\n"
            "Las funciones que ya vienen escritas (`describir_herramientas`, `construir_prompt`, `prompt_juez`) no hace falta tocarlas.\n"
            "\n"
            "## Como se evalua\n"
            "\n"
            'Al pulsar "Enviar capstone" corren **10 tests ocultos**, uno por requisito, en tu navegador. Cada test importa tus modulos desde cero y usa **sus propios datos** y un **LLM falso** que devuelve respuestas guionizadas y anota los prompts que recibe: asi comprueba, por ejemplo, que no se llama al LLM cuando nada supera el umbral, o que el agente le pasa la observacion del paso anterior. Para aprobar hay que pasar **los 10**.\n'
            "\n"
            "Los tests son `async`: tus funciones `responder`, `ejecutar_agente`, `atender` y `evaluar` deben ser `async def` y hacer `await` de `llm_fn`, `sistema_fn` y `juez_fn`.\n"
            "\n"
            "## Paso opcional: el LLM real\n"
            "\n"
            "No cuenta para aprobar. En el editor de PyCode existe `pycode.llm_complete(prompt)`, que llama al modelo real a traves del backend. `demo.py` muestra como envolverlo en un `llm_fn` y lanzar la evaluacion con los casos de `datos.py`. Como el editor trabaja con un solo archivo, pega alli tus cinco modulos seguidos del contenido de `demo.py` (quitando los `from ... import` entre modulos), o ejecutalo en local con tu propio `llm_fn`. Con un modelo real las respuestas cambian de una ejecucion a otra: por eso la nota se pone con el LLM falso y el real sirve para ver la tasa de aprobados de verdad.\n"
            "\n"
            'Fijate tambien en las fuentes que recupera: con bolsa de palabras, las palabras vacias pesan tanto como las importantes, y "¿tienen tienda fisica en Madrid?" puede recuperar un documento solo porque comparte "en". Filtrarlas, o cambiar a embeddings de verdad, es la primera mejora que la evaluacion te dejaria medir.\n'
        ),
        "requirements": [
            {
                "id": "R1",
                "text": "`recuperacion.py`: `tokenizar(texto)` pasa a minusculas, quita las tildes (`unicodedata.normalize('NFD', ...)` + `encode('ascii', 'ignore')`) y devuelve `re.findall(r'\\w+', ...)`. `embed_bow(texto, vocab)` devuelve un vector numpy con cuantas veces aparece cada palabra del vocabulario (las que no estan no cuentan). `construir_indice(textos)` devuelve `{'textos', 'vocab', 'matriz'}`: el vocabulario ordenado sin repetidos y una matriz `(N, V)` con un embedding por fila.",
            },
            {
                "id": "R2",
                "text": "`recuperar(pregunta, indice, k=3, umbral=0.2)` devuelve una lista de tuplas `(indice_del_texto, similitud)` con la similitud coseno entre la pregunta y cada fila: solo las que llegan al umbral (`>=`), de mayor a menor (en empate, el indice menor primero), como mucho `k`. Un vector de ceros tiene similitud 0, sin dividir entre cero. Los indices son `int` y las similitudes `float`.",
            },
            {
                "id": "R3",
                "text": "`asistente.py`: `prompt_con_fuentes(pregunta, fragmentos)` incluye la pregunta y cada fragmento en su propia linea como `[1] texto`, `[2] texto`... en orden, e instruye al modelo a citar con esos numeros. `extraer_citas(respuesta, n_fuentes)` devuelve los numeros citados entre corchetes (`[2]`, `[1, 3]`) en orden de aparicion, sin repetidos y descartando los que no estan entre 1 y `n_fuentes`.",
            },
            {
                "id": "R4",
                "text": "`async responder(pregunta, indice, llm_fn, k=3, umbral=0.2)` recupera los fragmentos; si ninguno supera el umbral devuelve `{'respuesta': NO_SE, 'fuentes': []}` **sin llamar al LLM**. Si hay fragmentos, llama a `llm_fn` una vez con `prompt_con_fuentes` y devuelve `{'respuesta': texto_del_llm, 'fuentes': [...]}`, donde las fuentes son los textos de los fragmentos citados, en el orden de las citas.",
            },
            {
                "id": "R5",
                "text": "`herramientas.py`: `crear_herramientas(pedidos)` devuelve `{'consultar_pedido': {'descripcion', 'parametros', 'funcion'}}` con `parametros == ['numero']`. La funcion busca `str(numero)` en el diccionario **recibido** y devuelve `'Pedido 1001: en camino, entrega estimada 2026-09-20'`; si el pedido no existe lanza `KeyError`.",
            },
            {
                "id": "R6",
                "text": "`parsear_accion(texto)` acepta JSON suelto o dentro de una cerca de codigo y devuelve `{'tipo': 'herramienta', 'nombre', 'argumentos'}`, `{'tipo': 'respuesta', 'texto'}` o `{'tipo': 'error', 'detalle'}`. `ejecutar_herramienta(accion, herramientas)` nunca lanza: devuelve `'Resultado: <valor>'`, o `'Error: la herramienta X no existe'`, `'Error: falta el argumento a'` / `'Error: argumento no permitido: c'` (unidos con `'; '`, faltan primero, cada grupo en orden alfabetico), o `'Error: <Excepcion>: <mensaje>'` si la funcion falla.",
            },
            {
                "id": "R7",
                "text": "`async ejecutar_agente(pregunta, herramientas, llm_fn, max_pasos=4)` repite: prompt con `construir_prompt`, llamada al LLM, `parsear_accion`. Si es una respuesta, termina con `{'respuesta': texto, 'pasos': pasos, 'motivo': 'respuesta'}`. Si no, anade `{'llm': texto, 'observacion': ...}` a `pasos` (el resultado de la herramienta, o un texto que empieza por `'Error'` si el formato era invalido) y sigue. Tras `max_pasos` llamadas devuelve `{'respuesta': None, 'pasos': pasos, 'motivo': 'max_pasos'}`.",
            },
            {
                "id": "R8",
                "text": "`nebula.py`: `async atender(pregunta, indice, herramientas, llm_fn)` es el router. Si la pregunta contiene un numero de 4 o mas cifras, usa el agente y devuelve `{'modo': 'agente', 'respuesta': ..., 'fuentes': []}` (con `SIN_RESPUESTA` si el agente agoto los pasos). Si no, usa `responder` y devuelve `{'modo': 'rag', 'respuesta': ..., 'fuentes': ...}`.",
            },
            {
                "id": "R9",
                "text": "`evaluacion.py`: `contiene_datos(respuesta, datos_clave)` devuelve la fraccion de datos clave que aparecen en la respuesta, comparando ambos normalizados (minusculas, sin tildes, signos como espacios, espacios colapsados); sin datos clave vale `1.0`. `puntuar_fuentes(citadas, esperadas)` devuelve `{'precision', 'recall'}` como conjuntos: precision `0.0` sin citadas y recall `1.0` sin esperadas.",
            },
            {
                "id": "R10",
                "text": "`parsear_veredicto(texto)` lee `{\"puntuacion\": 1-5, \"motivo\": ...}` (suelto o en cerca de codigo) y devuelve `{'puntuacion', 'motivo'}` o `None` si no es un entero (ni `bool`) entre 1 y 5. `async evaluar(casos, sistema_fn, juez_fn, nota_minima=4)` ejecuta cada caso y devuelve `{'casos': [{'id', 'aprobado', 'cobertura', 'recall', 'puntuacion'}], 'tasa_aprobados', 'sin_veredicto'}`. Un caso aprueba con cobertura 1.0, recall 1.0 y nota del juez `>= nota_minima`; sin veredicto no aprueba y su id va a `sin_veredicto`.",
            },
        ],
        "starter_files": [
            {
                "path": "recuperacion.py",
                "editable": True,
                "content": (
                    '"""Recuperacion: tokenizar, indexar y buscar lo relevante (R1-R2)."""\n'
                    "\n"
                    "import re\n"
                    "import unicodedata\n"
                    "\n"
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def tokenizar(texto):\n"
                    "    \"\"\"'¿Cuanto tarda el ENVIO?' -> ['cuanto', 'tarda', 'el', 'envio'].\"\"\"\n"
                    "    # TODO: minusculas, quitar tildes (NFD + encode('ascii', 'ignore')) y re.findall(r'\\w+', ...)\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def embed_bow(texto, vocab):\n"
                    '    """Vector numpy de conteos: una posicion por palabra del vocabulario."""\n'
                    "    # TODO: palabra -> columna; suma 1 por cada palabra del texto que este en vocab\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def construir_indice(textos):\n"
                    "    \"\"\"{'textos': textos, 'vocab': vocabulario ordenado, 'matriz': (N, V)}.\"\"\"\n"
                    "    # TODO: vocabulario = palabras de todos los textos, sin repetir y ordenadas\n"
                    "    # TODO: matriz con embed_bow de cada texto (cuidado con la shape si V == 0)\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def recuperar(pregunta, indice, k=3, umbral=0.2):\n"
                    '    """[(i, similitud), ...] con similitud >= umbral, de mayor a menor, como mucho k."""\n'
                    "    # TODO: embedding de la pregunta con el vocabulario del indice\n"
                    "    # TODO: similitud coseno contra cada fila (0 si alguna norma es 0)\n"
                    "    # TODO: ordenar de forma estable (np.argsort(-sims, kind='stable')), filtrar y cortar en k\n"
                    "    raise NotImplementedError\n"
                ),
            },
            {
                "path": "asistente.py",
                "editable": True,
                "content": (
                    '"""Asistente RAG: prompt con fuentes, citas y respuesta (R3-R4)."""\n'
                    "\n"
                    "import re\n"
                    "\n"
                    "from recuperacion import recuperar\n"
                    "\n"
                    "NO_SE = 'No lo se: no encontre informacion sobre eso en los documentos.'\n"
                    "\n"
                    "\n"
                    "def prompt_con_fuentes(pregunta, fragmentos):\n"
                    '    """Instrucciones + fuentes numeradas \'[1] texto\' (una por linea) + pregunta."""\n'
                    "    # TODO: numera desde 1 con enumerate(fragmentos, start=1)\n"
                    "    # TODO: pide responder solo con las fuentes, citar con [n] y decir que no lo sabe si no bastan\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def extraer_citas(respuesta, n_fuentes):\n"
                    '    """\'Tarda 3 dias [2]. Gratis [1, 2] y [7].\' con n_fuentes=2 -> [2, 1]."""\n'
                    "    # TODO: re.findall(r'\\[([\\d,\\s]+)\\]', respuesta) da el interior de cada corchete\n"
                    "    # TODO: sin repetidos, en orden de aparicion, solo 1..n_fuentes\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "async def responder(pregunta, indice, llm_fn, k=3, umbral=0.2):\n"
                    '    """{\'respuesta\': texto, \'fuentes\': [textos citados]}; NO_SE sin llamar al LLM."""\n'
                    "    # TODO: recuperar(pregunta, indice, k, umbral); si esta vacio -> NO_SE y fuentes []\n"
                    "    # TODO: fragmentos = textos recuperados; texto = await llm_fn(prompt_con_fuentes(...))\n"
                    "    # TODO: fuentes = fragmentos citados segun extraer_citas\n"
                    "    raise NotImplementedError\n"
                ),
            },
            {
                "path": "herramientas.py",
                "editable": True,
                "content": (
                    '"""Agente con herramientas: consulta de pedidos (R5-R7)."""\n'
                    "\n"
                    "import json\n"
                    "\n"
                    "CERCA = '`' * 3  # tres acentos graves: la cerca de un bloque de codigo\n"
                    "\n"
                    "\n"
                    "def describir_herramientas(herramientas):\n"
                    '    """Ya escrita: una linea por herramienta, en orden alfabetico."""\n'
                    "    return '\\n'.join(\n"
                    "        f\"- {nombre}({', '.join(herramientas[nombre]['parametros'])}): \"\n"
                    "        f\"{herramientas[nombre]['descripcion']}\"\n"
                    "        for nombre in sorted(herramientas)\n"
                    "    )\n"
                    "\n"
                    "\n"
                    "def construir_prompt(pregunta, herramientas, pasos):\n"
                    '    """Ya escrita: herramientas + formato de salida + pregunta + historial."""\n'
                    "    historial = '\\n'.join(\n"
                    "        f\"Accion: {paso['llm']}\\nObservacion: {paso['observacion']}\" for paso in pasos\n"
                    "    )\n"
                    "    return (\n"
                    "        'Eres el asistente de Nebula. Herramientas disponibles:\\n'\n"
                    "        f'{describir_herramientas(herramientas)}\\n\\n'\n"
                    '        \'Responde SOLO con JSON: {"herramienta": nombre, "argumentos": {...}} \'\n'
                    "        'o {\"respuesta\": texto}.\\n\\n'\n"
                    "        f'Pregunta: {pregunta}\\n{historial}'\n"
                    "    )\n"
                    "\n"
                    "\n"
                    "def crear_herramientas(pedidos):\n"
                    "    \"\"\"{'consultar_pedido': {'descripcion', 'parametros': ['numero'], 'funcion'}}.\"\"\"\n"
                    "\n"
                    "    def consultar_pedido(numero):\n"
                    "        # TODO: busca str(numero) en `pedidos` (el diccionario recibido)\n"
                    "        # TODO: si no existe -> raise KeyError(f'el pedido {numero} no existe')\n"
                    '        # TODO: return f"Pedido {numero}: {estado}, entrega estimada {entrega}"\n'
                    "        raise NotImplementedError\n"
                    "\n"
                    "    # TODO: devuelve la ficha con descripcion, parametros y funcion\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def parsear_accion(texto):\n"
                    "    \"\"\"Texto del LLM -> {'tipo': 'herramienta'|'respuesta'|'error', ...}.\"\"\"\n"
                    "    # TODO: si hay CERCA, quedate con lo de dentro (y quita el 'json' inicial)\n"
                    "    # TODO: json.loads con try/except json.JSONDecodeError -> tipo 'error'\n"
                    "    # TODO: 'herramienta' en el dict -> tipo 'herramienta'; 'respuesta' -> tipo 'respuesta'\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def ejecutar_herramienta(accion, herramientas):\n"
                    '    """Nunca lanza: \'Resultado: ...\' o \'Error: ...\'."""\n'
                    "    # TODO: herramienta desconocida -> 'Error: la herramienta X no existe'\n"
                    "    # TODO: faltan / sobran argumentos -> 'Error: falta el argumento a; argumento no permitido: c'\n"
                    "    # TODO: llama a la funcion con **argumentos dentro de try/except Exception\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "async def ejecutar_agente(pregunta, herramientas, llm_fn, max_pasos=4):\n"
                    "    \"\"\"Bucle del agente: {'respuesta', 'pasos', 'motivo'}.\"\"\"\n"
                    "    pasos = []\n"
                    "    # TODO: for _ in range(max_pasos): prompt -> await llm_fn -> parsear_accion\n"
                    "    # TODO: respuesta -> return {'respuesta': ..., 'pasos': pasos, 'motivo': 'respuesta'}\n"
                    "    # TODO: herramienta -> observacion = ejecutar_herramienta(...)\n"
                    "    # TODO: error de formato -> observacion = 'Error de formato: ' + detalle\n"
                    "    # TODO: pasos.append({'llm': texto, 'observacion': observacion})\n"
                    "    raise NotImplementedError\n"
                ),
            },
            {
                "path": "nebula.py",
                "editable": True,
                "content": (
                    '"""El asistente de Nebula: decide entre documentos y pedidos (R8)."""\n'
                    "\n"
                    "import re\n"
                    "\n"
                    "from asistente import responder\n"
                    "from herramientas import ejecutar_agente\n"
                    "\n"
                    "SIN_RESPUESTA = 'No pude completar la consulta. Un companero de soporte te escribira pronto.'\n"
                    "\n"
                    "\n"
                    "async def atender(pregunta, indice, herramientas, llm_fn):\n"
                    "    \"\"\"{'modo': 'agente'|'rag', 'respuesta': ..., 'fuentes': [...]}.\"\"\"\n"
                    "    # TODO: re.search(r'\\d{4,}', pregunta) -> hay numero de pedido -> agente\n"
                    "    # TODO: agente: respuesta None (agoto los pasos) -> SIN_RESPUESTA; fuentes []\n"
                    "    # TODO: si no: resultado = await responder(pregunta, indice, llm_fn)\n"
                    "    raise NotImplementedError\n"
                ),
            },
            {
                "path": "evaluacion.py",
                "editable": True,
                "content": (
                    '"""Evaluacion: metricas automaticas y LLM juez (R9-R10)."""\n'
                    "\n"
                    "import json\n"
                    "import re\n"
                    "import unicodedata\n"
                    "\n"
                    "CERCA = '`' * 3\n"
                    "\n"
                    "\n"
                    "def prompt_juez(pregunta, respuesta):\n"
                    '    """Ya escrita: pide al juez una nota de 1 a 5 en JSON."""\n'
                    "    return (\n"
                    "        'Evalua la respuesta de un asistente de atencion al cliente.\\n'\n"
                    "        'Puntua de 1 a 5: 5 = correcta, completa y clara; 1 = incorrecta o no contesta.\\n'\n"
                    '        \'Responde SOLO con JSON: {"puntuacion": entero, "motivo": texto breve}.\\n\\n\'\n'
                    "        f'Pregunta: {pregunta}\\nRespuesta: {respuesta}'\n"
                    "    )\n"
                    "\n"
                    "\n"
                    "def normalizar(texto):\n"
                    '    """\'¡Llega en 3 DIAS!\' -> \'llega en 3 dias\'."""\n'
                    "    # TODO: minusculas, sin tildes, signos -> espacios (re.sub(r'[^\\w\\s]', ' ', ...)), espacios colapsados\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def contiene_datos(respuesta, datos_clave):\n"
                    '    """Fraccion de datos clave presentes (normalizados). Sin datos clave: 1.0."""\n'
                    "    # TODO\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def puntuar_fuentes(citadas, esperadas):\n"
                    '    """{\'precision\', \'recall\'} como conjuntos."""\n'
                    "    # TODO: precision 0.0 si no hay citadas; recall 1.0 si no hay esperadas\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "def parsear_veredicto(texto):\n"
                    '    """{\'puntuacion\': 1-5, \'motivo\': str} o None si el veredicto no es valido."""\n'
                    "    # TODO: como parsear_accion; puntuacion debe cumplir type(p) is int y 1 <= p <= 5\n"
                    "    raise NotImplementedError\n"
                    "\n"
                    "\n"
                    "async def evaluar(casos, sistema_fn, juez_fn, nota_minima=4):\n"
                    "    \"\"\"{'casos': [...], 'tasa_aprobados': float, 'sin_veredicto': [ids]}.\"\"\"\n"
                    "    # TODO: por caso: resultado = await sistema_fn(pregunta); cobertura; recall de fuentes\n"
                    "    # TODO: veredicto = parsear_veredicto(await juez_fn(prompt_juez(pregunta, respuesta)))\n"
                    "    # TODO: aprobado = cobertura == 1.0 and recall == 1.0 and nota >= nota_minima\n"
                    "    raise NotImplementedError\n"
                ),
            },
            {
                "path": "datos.py",
                "editable": False,
                "content": (
                    '"""Datos de Nebula (ya escrito: no hace falta tocarlo)."""\n'
                    "\n"
                    "DOCUMENTOS = [\n"
                    "    'El envio estandar tarda de 3 a 5 dias habiles y es gratis desde 50 euros.',\n"
                    "    'El envio express llega en 24 horas y cuesta 6 euros.',\n"
                    "    'Puedes devolver cualquier producto durante 30 dias desde que lo recibes.',\n"
                    "    'Las devoluciones son gratis si el producto llega danado.',\n"
                    "    'Aceptamos pago con tarjeta, transferencia bancaria y PayPal.',\n"
                    "    'El reembolso de una devolucion tarda hasta 10 dias en aparecer en tu cuenta.',\n"
                    "    'La garantia de los productos electronicos es de 2 anos.',\n"
                    "    'Para cambiar la direccion de un pedido escribe a soporte antes de que salga del almacen.',\n"
                    "]\n"
                    "\n"
                    "PEDIDOS = {\n"
                    "    '1001': {'estado': 'en camino', 'entrega': '2026-09-20'},\n"
                    "    '1002': {'estado': 'entregado', 'entrega': '2026-09-02'},\n"
                    "    '1003': {'estado': 'preparando', 'entrega': '2026-09-25'},\n"
                    "}\n"
                    "\n"
                    "CASOS = [\n"
                    "    {\n"
                    "        'id': 'envio-estandar',\n"
                    "        'pregunta': 'Cuanto tarda el envio estandar?',\n"
                    "        'datos_clave': ['3 a 5 dias'],\n"
                    "        'fuentes_esperadas': [DOCUMENTOS[0]],\n"
                    "    },\n"
                    "    {\n"
                    "        'id': 'formas-de-pago',\n"
                    "        'pregunta': 'Puedo pagar con PayPal?',\n"
                    "        'datos_clave': ['PayPal'],\n"
                    "        'fuentes_esperadas': [DOCUMENTOS[4]],\n"
                    "    },\n"
                    "    {\n"
                    "        'id': 'plazo-devolucion',\n"
                    "        'pregunta': 'Cuantos dias tengo para devolver un producto?',\n"
                    "        'datos_clave': ['30 dias'],\n"
                    "        'fuentes_esperadas': [DOCUMENTOS[2]],\n"
                    "    },\n"
                    "    {\n"
                    "        'id': 'pedido-en-camino',\n"
                    "        'pregunta': 'Donde esta mi pedido 1001?',\n"
                    "        'datos_clave': ['en camino'],\n"
                    "        'fuentes_esperadas': [],\n"
                    "    },\n"
                    "]\n"
                ),
            },
            {
                "path": "demo.py",
                "editable": True,
                "content": (
                    '"""Paso opcional con el LLM real (no se evalua).\n'
                    "\n"
                    "En el editor de PyCode, `pycode.llm_complete` llama al modelo real. Pega tus\n"
                    "modulos en un solo archivo seguidos de este codigo (sin los imports entre\n"
                    "modulos) o ejecutalo en local con tu propio `llm_fn`.\n"
                    '"""\n'
                    "\n"
                    "import pycode\n"
                    "\n"
                    "from datos import CASOS, DOCUMENTOS, PEDIDOS\n"
                    "from evaluacion import evaluar\n"
                    "from herramientas import crear_herramientas\n"
                    "from nebula import atender\n"
                    "from recuperacion import construir_indice\n"
                    "\n"
                    "\n"
                    "async def llm_real(prompt):\n"
                    "    return await pycode.llm_complete(prompt, max_tokens=300, temperature=0.2)\n"
                    "\n"
                    "\n"
                    "indice = construir_indice(DOCUMENTOS)\n"
                    "herramientas = crear_herramientas(PEDIDOS)\n"
                    "\n"
                    "respuesta = await atender('Cuanto tarda el envio express?', indice, herramientas, llm_real)\n"
                    "print(respuesta)\n"
                    "\n"
                    "\n"
                    "async def sistema(pregunta):\n"
                    "    return await atender(pregunta, indice, herramientas, llm_real)\n"
                    "\n"
                    "\n"
                    "informe = await evaluar(CASOS, sistema, llm_real)\n"
                    "for caso in informe['casos']:\n"
                    "    print(caso)\n"
                    "print('tasa de aprobados:', informe['tasa_aprobados'])\n"
                    "print('sin veredicto:', informe['sin_veredicto'])\n"
                ),
            },
        ],
        "hidden_tests": [
            {
                "name": "R1 · tokenizar, embed_bow y construir_indice",
                "code": (
                    "from recuperacion import tokenizar, embed_bow, construir_indice\n"
                    "import numpy as np\n"
                    "t = tokenizar('¿Cuánto tarda el ENVÍO?')\n"
                    "assert t == ['cuanto', 'tarda', 'el', 'envio'], t\n"
                    "textos = ['Envío gratis desde 50 euros', 'El envío tarda 3 días']\n"
                    "indice = construir_indice(textos)\n"
                    "assert list(indice['textos']) == textos\n"
                    "assert list(indice['vocab']) == ['3', '50', 'desde', 'dias', 'el', 'envio', 'euros', 'gratis', 'tarda'], indice['vocab']\n"
                    "m = np.asarray(indice['matriz'], float)\n"
                    "assert m.shape == (2, 9), m.shape\n"
                    "assert m[1].tolist() == [1, 0, 0, 1, 1, 1, 0, 0, 1], m[1]\n"
                    "v = np.asarray(embed_bow('envio ENVÍO pingüino', indice['vocab']), float)\n"
                    "assert v.tolist() == [0, 0, 0, 0, 0, 2, 0, 0, 0], v"
                ),
            },
            {
                "name": "R2 · recuperar con umbral, orden y k",
                "code": (
                    "from recuperacion import construir_indice, recuperar\n"
                    "docs = ['el envio tarda 3 dias', 'devoluciones gratis en 30 dias', 'pago con tarjeta o transferencia']\n"
                    "indice = construir_indice(docs)\n"
                    "r = recuperar('envio gratis en dias', indice, k=3, umbral=0.2)\n"
                    "assert [i for i, _ in r] == [1, 0], r\n"
                    "assert all(type(i) is int for i, _ in r), r\n"
                    "assert abs(r[0][1] - 3 / (5 ** 0.5 * 2)) < 1e-9, r[0]\n"
                    "assert abs(r[1][1] - 2 / (5 ** 0.5 * 2)) < 1e-9, r[1]\n"
                    "assert [i for i, _ in recuperar('envio gratis en dias', indice, k=1, umbral=0.2)] == [1]\n"
                    "assert [i for i, _ in recuperar('envio gratis en dias', indice, k=3, umbral=0.5)] == [1]\n"
                    "assert recuperar('horario de la tienda', indice) == []\n"
                    "empate = construir_indice(['tarjeta roja', 'tarjeta azul'])\n"
                    "assert [i for i, _ in recuperar('tarjeta', empate)] == [0, 1], 'en empate va primero el indice menor'"
                ),
            },
            {
                "name": "R3 · prompt con fuentes numeradas y extraer_citas",
                "code": (
                    "from asistente import prompt_con_fuentes, extraer_citas\n"
                    "p = prompt_con_fuentes('¿Cuanto tarda?', ['El envio tarda 3 dias', 'Pago con tarjeta'])\n"
                    "lineas = p.splitlines()\n"
                    "assert '[1] El envio tarda 3 dias' in lineas, p\n"
                    "assert '[2] Pago con tarjeta' in lineas, p\n"
                    "assert lineas.index('[1] El envio tarda 3 dias') < lineas.index('[2] Pago con tarjeta')\n"
                    "assert '¿Cuanto tarda?' in p\n"
                    "c = extraer_citas('Tarda 3 dias [2]. Gratis [1, 2] y [7].', 2)\n"
                    "assert c == [2, 1], c\n"
                    "assert extraer_citas('Sin citas por aqui', 3) == []\n"
                    "assert extraer_citas('[3][1,3] [0]', 3) == [3, 1]"
                ),
            },
            {
                "name": "R4 · responder: citas a fuentes y no llama al LLM sin contexto",
                "code": (
                    "from recuperacion import construir_indice\n"
                    "from asistente import responder, NO_SE\n"
                    "docs = ['el envio estandar tarda 3 dias habiles', 'las devoluciones son gratis durante 30 dias', 'aceptamos pago con tarjeta']\n"
                    "indice = construir_indice(docs)\n"
                    "prompts = []\n"
                    "guion = []\n"
                    "async def llm_falso(prompt):\n"
                    "    prompts.append(prompt)\n"
                    "    return guion.pop(0)\n"
                    "guion.append('Aceptamos tarjeta [1].')\n"
                    "r = await responder('¿puedo hacer el pago con tarjeta?', indice, llm_falso)\n"
                    "assert len(prompts) == 1, prompts\n"
                    "assert '[1] aceptamos pago con tarjeta' in prompts[0], prompts[0]\n"
                    "assert 'el envio tarda' not in prompts[0], 'solo deben ir los fragmentos que superan el umbral'\n"
                    "assert r == {'respuesta': 'Aceptamos tarjeta [1].', 'fuentes': ['aceptamos pago con tarjeta']}, r\n"
                    "guion.append('Tienes 30 dias [2] y el envio [1].')\n"
                    "r = await responder('devoluciones gratis 30 dias envio', indice, llm_falso)\n"
                    "assert r['fuentes'] == ['el envio estandar tarda 3 dias habiles', 'las devoluciones son gratis durante 30 dias'], r\n"
                    "r = await responder('horario de la tienda fisica', indice, llm_falso)\n"
                    "assert len(prompts) == 2, 'no se debe llamar al LLM si nada supera el umbral'\n"
                    "assert r == {'respuesta': NO_SE, 'fuentes': []}, r"
                ),
            },
            {
                "name": "R5 · crear_herramientas: consultar_pedido",
                "code": (
                    "from herramientas import crear_herramientas\n"
                    "pedidos = {'2001': {'estado': 'en camino', 'entrega': '2026-10-02'}}\n"
                    "h = crear_herramientas(pedidos)\n"
                    "ficha = h['consultar_pedido']\n"
                    "assert list(ficha['parametros']) == ['numero'], ficha['parametros']\n"
                    "assert isinstance(ficha['descripcion'], str) and ficha['descripcion'].strip()\n"
                    "esperado = 'Pedido 2001: en camino, entrega estimada 2026-10-02'\n"
                    "assert ficha['funcion'](numero='2001') == esperado, ficha['funcion'](numero='2001')\n"
                    "assert ficha['funcion'](numero=2001) == esperado, ficha['funcion'](numero=2001)\n"
                    "try:\n"
                    "    ficha['funcion'](numero='9999')\n"
                    "except KeyError:\n"
                    "    pass\n"
                    "else:\n"
                    "    raise AssertionError('un pedido inexistente debe lanzar KeyError')"
                ),
            },
            {
                "name": "R6 · parsear_accion y ejecutar_herramienta sin lanzar",
                "code": (
                    "from herramientas import parsear_accion, ejecutar_herramienta\n"
                    "CERCA = '`' * 3\n"
                    'a = parsear_accion(\'{"herramienta": "consultar_pedido", "argumentos": {"numero": "1"}}\')\n'
                    "assert a == {'tipo': 'herramienta', 'nombre': 'consultar_pedido', 'argumentos': {'numero': '1'}}, a\n"
                    'a = parsear_accion(CERCA + \'json\\n{"respuesta": "Hola"}\\n\' + CERCA)\n'
                    "assert a == {'tipo': 'respuesta', 'texto': 'Hola'}, a\n"
                    "assert parsear_accion('no es json')['tipo'] == 'error'\n"
                    "assert parsear_accion('{\"otra\": 1}')['tipo'] == 'error'\n"
                    "def dividir(a, b):\n"
                    "    return a / b\n"
                    "h = {'dividir': {'descripcion': 'divide a entre b', 'parametros': ['a', 'b'], 'funcion': dividir}}\n"
                    "def accion(nombre, argumentos):\n"
                    "    return {'tipo': 'herramienta', 'nombre': nombre, 'argumentos': argumentos}\n"
                    "r = ejecutar_herramienta(accion('dividir', {'a': 6, 'b': 3}), h)\n"
                    "assert r == 'Resultado: 2.0', r\n"
                    "r = ejecutar_herramienta(accion('borrar', {}), h)\n"
                    "assert r == 'Error: la herramienta borrar no existe', r\n"
                    "r = ejecutar_herramienta(accion('dividir', {'a': 1}), h)\n"
                    "assert r == 'Error: falta el argumento b', r\n"
                    "r = ejecutar_herramienta(accion('dividir', {'c': 3}), h)\n"
                    "assert r == 'Error: falta el argumento a; falta el argumento b; argumento no permitido: c', r\n"
                    "r = ejecutar_herramienta(accion('dividir', {'a': 1, 'b': 0}), h)\n"
                    "assert r.startswith('Error: ZeroDivisionError'), r"
                ),
            },
            {
                "name": "R7 · ejecutar_agente: observaciones y limite de pasos",
                "code": (
                    "from herramientas import ejecutar_agente, crear_herramientas\n"
                    "h = crear_herramientas({'1001': {'estado': 'en camino', 'entrega': '2026-09-20'}})\n"
                    "guion = [\n"
                    '    \'{"herramienta": "consultar_pedido", "argumentos": {"numero": "1001"}}\',\n'
                    "    'esto no es json',\n"
                    '    \'{"respuesta": "Tu pedido llega el 20 de septiembre."}\',\n'
                    "]\n"
                    "prompts = []\n"
                    "async def llm_falso(prompt):\n"
                    "    prompts.append(prompt)\n"
                    "    return guion[len(prompts) - 1]\n"
                    "r = await ejecutar_agente('¿Donde esta mi pedido 1001?', h, llm_falso)\n"
                    "assert r['motivo'] == 'respuesta', r\n"
                    "assert r['respuesta'] == 'Tu pedido llega el 20 de septiembre.', r\n"
                    "assert len(r['pasos']) == 2, r['pasos']\n"
                    "assert r['pasos'][0]['observacion'] == 'Resultado: Pedido 1001: en camino, entrega estimada 2026-09-20', r['pasos'][0]\n"
                    "assert r['pasos'][1]['observacion'].startswith('Error'), r['pasos'][1]\n"
                    "assert 'Resultado: Pedido 1001' in prompts[1], 'el LLM debe ver la observacion del paso anterior'\n"
                    "assert len(prompts) == 3\n"
                    "llamadas = []\n"
                    "async def llm_terco(prompt):\n"
                    "    llamadas.append(prompt)\n"
                    "    return guion[0]\n"
                    "r = await ejecutar_agente('pedido 1001', h, llm_terco, max_pasos=3)\n"
                    "assert r['motivo'] == 'max_pasos' and r['respuesta'] is None, r\n"
                    "assert len(r['pasos']) == 3 and len(llamadas) == 3, (len(r['pasos']), len(llamadas))"
                ),
            },
            {
                "name": "R8 · atender: el router entre agente y RAG",
                "code": (
                    "from recuperacion import construir_indice\n"
                    "from herramientas import crear_herramientas\n"
                    "from nebula import atender, SIN_RESPUESTA\n"
                    "indice = construir_indice(['el envio tarda 3 dias habiles', 'aceptamos pago con tarjeta'])\n"
                    "h = crear_herramientas({'1001': {'estado': 'entregado', 'entrega': '2026-09-10'}})\n"
                    "guion = []\n"
                    "prompts = []\n"
                    "async def llm_falso(prompt):\n"
                    "    prompts.append(prompt)\n"
                    "    return guion.pop(0)\n"
                    'guion[:] = [\'{"herramienta": "consultar_pedido", "argumentos": {"numero": "1001"}}\', \'{"respuesta": "Tu pedido 1001 ya fue entregado."}\']\n'
                    "r = await atender('¿Y mi pedido 1001?', indice, h, llm_falso)\n"
                    "assert r == {'modo': 'agente', 'respuesta': 'Tu pedido 1001 ya fue entregado.', 'fuentes': []}, r\n"
                    "assert 'Resultado: Pedido 1001: entregado' in prompts[-1], prompts[-1]\n"
                    "guion[:] = ['Tarda 3 dias habiles [1].']\n"
                    "r = await atender('¿cuanto tarda el envio?', indice, h, llm_falso)\n"
                    "assert r == {'modo': 'rag', 'respuesta': 'Tarda 3 dias habiles [1].', 'fuentes': ['el envio tarda 3 dias habiles']}, r\n"
                    'guion[:] = [\'{"herramienta": "consultar_pedido", "argumentos": {"numero": "1001"}}\'] * 20\n'
                    "r = await atender('pedido 1001 otra vez', indice, h, llm_falso)\n"
                    "assert r['modo'] == 'agente' and r['respuesta'] == SIN_RESPUESTA and r['fuentes'] == [], r"
                ),
            },
            {
                "name": "R9 · contiene_datos y puntuar_fuentes",
                "code": (
                    "from evaluacion import contiene_datos, puntuar_fuentes\n"
                    "assert contiene_datos('Llega en 3 DÍAS hábiles, gratis.', ['3 dias habiles', 'gratis']) == 1.0\n"
                    "assert contiene_datos('Llega pronto.', ['3 dias', 'gratis']) == 0.0\n"
                    "assert contiene_datos('¡Es gratis!', ['3 días', 'Gratis']) == 0.5\n"
                    "assert contiene_datos('Tarda 3-5  dias', ['3 5 dias']) == 1.0\n"
                    "assert contiene_datos('lo que sea', []) == 1.0\n"
                    "assert puntuar_fuentes(['a', 'b'], ['a']) == {'precision': 0.5, 'recall': 1.0}\n"
                    "assert puntuar_fuentes(['a', 'a'], ['a', 'c']) == {'precision': 1.0, 'recall': 0.5}\n"
                    "assert puntuar_fuentes([], ['a']) == {'precision': 0.0, 'recall': 0.0}\n"
                    "assert puntuar_fuentes(['a'], []) == {'precision': 0.0, 'recall': 1.0}"
                ),
            },
            {
                "name": "R10 · parsear_veredicto y evaluar con juez falso",
                "code": (
                    "from evaluacion import parsear_veredicto, evaluar\n"
                    "CERCA = '`' * 3\n"
                    "assert parsear_veredicto('{\"puntuacion\": 5, \"motivo\": \"ok\"}') == {'puntuacion': 5, 'motivo': 'ok'}\n"
                    "assert parsear_veredicto(CERCA + 'json\\n{\"puntuacion\": 2}\\n' + CERCA) == {'puntuacion': 2, 'motivo': ''}\n"
                    "for malo in ['no se', '{\"puntuacion\": 9}', '{\"puntuacion\": \"5\"}', '[5]', '{\"puntuacion\": true}']:\n"
                    "    assert parsear_veredicto(malo) is None, malo\n"
                    "casos = [\n"
                    "    {'id': 'envio', 'pregunta': 'cuanto tarda', 'datos_clave': ['3 dias'], 'fuentes_esperadas': ['doc envio']},\n"
                    "    {'id': 'pago', 'pregunta': 'como pago', 'datos_clave': ['tarjeta'], 'fuentes_esperadas': ['doc pago']},\n"
                    "    {'id': 'juez-roto', 'pregunta': 'devoluciones', 'datos_clave': ['30 dias'], 'fuentes_esperadas': ['doc dev']},\n"
                    "    {'id': 'nota-baja', 'pregunta': 'garantia', 'datos_clave': [], 'fuentes_esperadas': []},\n"
                    "]\n"
                    "respuestas = {\n"
                    "    'cuanto tarda': {'respuesta': 'Tarda 3 días [1].', 'fuentes': ['doc envio']},\n"
                    "    'como pago': {'respuesta': 'Con tarjeta [1].', 'fuentes': ['doc envio']},\n"
                    "    'devoluciones': {'respuesta': 'Tienes 30 dias [1].', 'fuentes': ['doc dev']},\n"
                    "    'garantia': {'respuesta': 'Ni idea.', 'fuentes': []},\n"
                    "}\n"
                    "async def sistema(pregunta):\n"
                    "    return respuestas[pregunta]\n"
                    "juicios = []\n"
                    "async def juez(prompt):\n"
                    "    juicios.append(prompt)\n"
                    "    if 'devoluciones' in prompt:\n"
                    "        return 'no tengo opinion'\n"
                    "    if 'garantia' in prompt:\n"
                    '        return \'{"puntuacion": 3, "motivo": "vaga"}\'\n'
                    '    return \'{"puntuacion": 5, "motivo": "bien"}\'\n'
                    "r = await evaluar(casos, sistema, juez)\n"
                    "assert len(juicios) == 4, len(juicios)\n"
                    "assert [c['id'] for c in r['casos']] == ['envio', 'pago', 'juez-roto', 'nota-baja'], r['casos']\n"
                    "assert [c['aprobado'] for c in r['casos']] == [True, False, False, False], r['casos']\n"
                    "assert r['casos'][1]['recall'] == 0.0 and r['casos'][1]['cobertura'] == 1.0, r['casos'][1]\n"
                    "assert r['casos'][2]['puntuacion'] is None, r['casos'][2]\n"
                    "assert r['casos'][3]['puntuacion'] == 3, r['casos'][3]\n"
                    "assert r['sin_veredicto'] == ['juez-roto'], r['sin_veredicto']\n"
                    "assert abs(r['tasa_aprobados'] - 0.25) < 1e-9, r['tasa_aprobados']\n"
                    "r = await evaluar(casos, sistema, juez, nota_minima=3)\n"
                    "assert [c['aprobado'] for c in r['casos']] == [True, False, False, True], r['casos']"
                ),
            },
        ],
        "estimated_hours": 14,
        "difficulty": "advanced",
        "order_index": 5,
    },
    {
        "slug": "track-6-pipeline-produccion",
        "track": "track-6",
        "title": "Pipeline de produccion: del experimento al despliegue",
        "short_description": (
            "Monta el pipeline completo de Nebula en cinco modulos: experimentos reproducibles, registro de modelos con checksum, un servicio con contrato de entrada, monitoreo de drift sobre su log y un despliegue con puerta de calidad, rollout y rollback."
        ),
        "description": (
            "## Contexto\n"
            "\n"
            "El modelo de devoluciones de Nebula ya existe: predice si un pedido acabara devuelto. Lo que no existe es **todo lo que hay alrededor**, que es lo que separa un cuaderno de un sistema en produccion. Hoy nadie sabe con que datos se entreno el que esta sirviendo, el artefacto es un `.pkl` sin firma, el servicio revienta con una peticion rara, nadie mira si los datos han cambiado y desplegar consiste en que alguien copie un archivo un viernes.\n"
            "\n"
            "Vas a construir ese alrededor entero, separado en modulos como se haria en un proyecto real.\n"
            "\n"
            "## Que integra este capstone\n"
            "\n"
            "- **MLOps 1**: semillas, division reproducible, huellas SHA-256 y manifiesto del experimento.\n"
            "- **MLOps 2**: runs con metricas, eleccion del mejor, artefacto con checksum y registro de versiones con etapas.\n"
            "- **MLOps 3**: contrato de entrada, validacion que acumula errores, vector de caracteristicas y respuestas 200/422/500/503.\n"
            "- **MLOps 4**: histogramas con bordes fijos, PSI y alertas de drift sobre el log del servicio.\n"
            "- **MLOps 5**: puerta de calidad, champion contra challenger, reparto de trafico y los cuatro finales de un despliegue.\n"
            "\n"
            "## Arquitectura\n"
            "\n"
            "```\n"
            "datos ──> reproducibilidad.manifiesto ──> registro.mejor_run ──> registro.guardar_modelo (+checksum)\n"
            "                                                                      │\n"
            "                                                                      v\n"
            "peticion ──> servicio.servir ──> 200/422/500/503 + log ──> monitoreo.monitorear ──> alertas\n"
            "                                                                      │\n"
            "candidato ──> despliegue.desplegar ──> puerta ──> champion/challenger ──> rollout ──> promovido\n"
            "                                                                                      rechazado\n"
            "                                                                                      rollback\n"
            "                                                                                      pausado\n"
            "```\n"
            "\n"
            "Cada pieza recibe lo que necesita como argumento: el modelo entra en el servicio como `modelo_fn`, y el despliegue mide cada paso del rollout con un `medir_fn`. Esa inyeccion es lo que permite corregir el proyecto entero con datos de juguete, deterministas y sin entrenar nada de verdad.\n"
            "\n"
            "## Estructura\n"
            "\n"
            "```\n"
            "reproducibilidad.py   huella, huella_config, huella_datos,\n"
            "                      dividir, manifiesto                              (R1-R2)\n"
            "registro.py           nuevo_run, registrar_metrica, mejor_run,\n"
            "                      guardar_modelo, cargar_modelo,\n"
            "                      registrar_version, promover                      (R3-R4)\n"
            "servicio.py           validar, vector, servir                          (R5-R6)\n"
            "monitoreo.py          histograma, psi, monitorear                      (R7-R8)\n"
            "despliegue.py         puerta_de_calidad, comparar_modelos,\n"
            "                      asignar_variante, evaluar_rollout, desplegar     (R9-R10)\n"
            "datos.py              pedidos, esquema y referencias de Nebula (ya escrito)\n"
            "demo.py               el pipeline de punta a punta (no se evalua)\n"
            "```\n"
            "\n"
            "Las funciones que ya vienen escritas (`coaccionar`, `severidad`, `tasa_error`, `revisar_requisitos`) no hace falta tocarlas: son las de las lecciones, puestas ahi para que te centres en el resto.\n"
            "\n"
            "## Como se evalua\n"
            "\n"
            'Al pulsar "Enviar capstone" corren **10 tests ocultos**, uno por requisito, en tu navegador. Cada test importa tus modulos desde cero y usa **sus propios datos**, nunca los de `datos.py`: un manifiesto se comprueba con otras filas, el servicio con otro esquema y el despliegue con un `medir_fn` de juguete. Para aprobar hay que pasar **los 10**.\n'
            "\n"
            "Ninguna funcion entrena un modelo de verdad ni llama a la red: donde hace falta un modelo se inyecta una funcion, igual que en las lecciones.\n"
            "\n"
            "## Paso opcional: el pipeline entero\n"
            "\n"
            "No cuenta para aprobar. `demo.py` encadena las cinco piezas con los datos de `datos.py`: divide, entrena un modelo de umbral, registra el run, guarda el artefacto con su checksum, atiende un puñado de peticiones, monitorea el log resultante y decide si el candidato se despliega. Como el editor de PyCode trabaja con un solo archivo, pega alli tus cinco modulos seguidos del contenido de `demo.py` (quitando los `from ... import` entre modulos). Es la forma de ver que las piezas encajan de verdad y no solo pasan los tests por separado.\n"
        ),
        "requirements": [
            {
                "id": "R1",
                "text": "`reproducibilidad.py`: `huella(texto, n=12)` devuelve los primeros `n` caracteres del SHA-256 del texto en UTF-8. `huella_config(config)` aplica `huella` a `json.dumps(config, sort_keys=True, separators=(',', ':'))`, de modo que el orden de las claves no cambie el resultado. `huella_datos(filas)` es la huella de la concatenacion de las huellas de cada fila (`json.dumps(fila, sort_keys=True)`), asi que el orden de las filas **si** cuenta. `dividir(filas, fraccion_test, semilla)` copia la lista, la baraja con `random.Random(semilla)`, parte por `round(len(filas) * fraccion_test)` y devuelve `(train, test)` con el test **primero** en la lista barajada.",
            },
            {
                "id": "R2",
                "text": "`manifiesto(filas, config, semilla, entorno, metricas)` devuelve `{'datos': {'huella', 'filas'}, 'config': {'huella', 'valores'}, 'semilla', 'entorno', 'metricas', 'id'}`. `entorno` se copia (quien llame despues no puede cambiarlo). El `'id'` es la `huella_config` de un diccionario con **solo** `datos`, `config`, `semilla` y `entorno`: dos ejecuciones con la misma receta comparten id aunque las metricas cambien.",
            },
            {
                "id": "R3",
                "text": "`registro.py`: `nuevo_run(run_id, params)` devuelve `{'id', 'params': <copia>, 'metricas': {}, 'historial': {}, 'estado': 'en_curso'}`. `registrar_metrica(run, nombre, valor, paso)` anade `[paso, valor]` (una **lista**) al historial y guarda el ultimo valor en `metricas`. `mejor_run(runs, metrica, mayor_es_mejor=True)` devuelve el mejor run entre los que tienen `estado == 'terminado'` **y** esa metrica; en empate gana el primero, y sin candidatos devuelve `None`.",
            },
            {
                "id": "R4",
                "text": "`guardar_modelo(modelo, ruta)` escribe `pickle.dumps(modelo)` y devuelve su SHA-256 completo. `cargar_modelo(ruta, checksum)` compara el checksum del archivo **antes** de `pickle.loads` y lanza `ValueError` si no coincide. `registrar_version(registro, nombre, run_id, checksum)` anade `{'version': <len+1>, 'run_id', 'checksum', 'etapa': 'ninguna'}` y la devuelve. `promover(registro, nombre, version, etapa)` pone esa etapa y, si es `'production'`, archiva la que estuviera en produccion.",
            },
            {
                "id": "R5",
                "text": "`servicio.py`: `validar(peticion, esquema)` devuelve `(datos, errores)` recorriendo el esquema en su orden: ausente con `'por_defecto'` se rellena, ausente sin el da `f'{nombre}: requerido'`; el valor se convierte con `coaccionar` (ya escrita) y si falla da `f\"{nombre}: se esperaba {tipo}\"`; despues, **solo el primer limite que falle** entre `'min'`, `'max'` y `'opciones'`. Al final, los campos que no estan en el esquema dan `f'{nombre}: campo desconocido'` en orden alfabetico. `vector(datos, orden, mapas)` recorre `orden` y devuelve `float`s, mapeando las categorias y lanzando `ValueError` si un nombre falta (`f'{nombre}: ausente'`) o la categoria no esta en el mapa (`f'{nombre}: categoria desconocida'`).",
            },
            {
                "id": "R6",
                "text": "`servir(peticion, servicio, peticion_id)` devuelve siempre `{'codigo', 'peticion_id', 'version', 'cuerpo'}`: **503** con `{'error': 'modelo no cargado'}` y `version` `None` si `servicio['modelo_fn']` es `None`; **422** con `{'errores': [...]}` si la validacion o el vector fallan; **500** con `{'error': 'error interno'}` si `modelo_fn` lanza (el mensaje real no sale en la respuesta); **200** con `{'prediccion': valor}`. Salvo el 503, anade al log `{'id', 'codigo'}` mas `'errores'` (422), `'detalle'` con `str(e)` (500) o `'entrada'` y `'prediccion'` (200).",
            },
            {
                "id": "R7",
                "text": "`monitoreo.py`: `histograma(valores, bordes)` cuenta por tramos con los bordes dados, metiendo lo que se sale por los extremos en el primer o ultimo tramo (asi `sum(conteos) == len(valores)`), y lanza `ValueError` con menos de dos bordes. `psi(referencia, actual)` devuelve el PSI de dos listas de conteos: proporciones con suelo `1e-6` y suma de `(pa - pe) * ln(pa / pe)`; `ValueError` si las longitudes no coinciden o alguna suma 0.",
            },
            {
                "id": "R8",
                "text": "`monitorear(log, referencia, config)` devuelve `{'resumen': {'peticiones', 'por_codigo', 'tasa_error'}, 'alertas': [...]}`. Si la tasa de error (codigos `>= 400`, redondeada a 4 decimales) supera `config['tasa_error_maxima']`, anade `{'tipo': 'errores', 'valor', 'severidad': 'critico'}`. Con menos de `config['minimo']` peticiones de codigo 200 anade `{'tipo': 'muestra', 'valor', 'severidad': 'aviso'}` y **no** revisa drift. Si hay muestra, revisa cada columna de `config['orden']` que este en `referencia['columnas']` y despues la prediccion, anadiendo `{'tipo': 'drift', 'columna', 'psi', 'severidad'}` cuando `severidad` (ya escrita) del PSI no es `None`; el `psi` va redondeado a 4 decimales. Las criticas van delante, sin alterar el orden dentro de cada severidad.",
            },
            {
                "id": "R9",
                "text": "`despliegue.py`: `puerta_de_calidad(candidato, requisitos, minimo_casos)` devuelve `{'pasa', 'motivos'}` juntando los motivos de `revisar_requisitos` (ya escrita) y, al final, `f\"casos: {casos} < {minimo}\"` si el candidato se midio con pocos casos. `comparar_modelos(campeon, retador, metrica, margen, mayor_es_mejor=True)` devuelve `{'delta': <redondeado a 4>, 'gana': delta >= margen}` y lanza `ValueError` si la metrica falta en alguno. `asignar_variante(peticion_id, porcentaje)` reparte con `int(sha256(id), 16) % 100 < porcentaje`, y lanza `ValueError` fuera de 0..100.",
            },
            {
                "id": "R10",
                "text": "`evaluar_rollout(log_champion, log_challenger, minimo, tolerancia)` devuelve `'sin datos'` si alguno de los dos logs no llega al minimo, `'rollback'` si la tasa de error del challenger supera la del champion mas la tolerancia, y `'seguir'` si no. `desplegar(candidato, campeon, config, medir_fn)` devuelve `{'estado', 'motivos', 'historial'}`: `'rechazado'` con los motivos de la puerta (historial vacio); `'rechazado'` con `[f\"no mejora al campeon: delta {delta}\"]` si hay campeon y no gana; y si no, recorre `config['pasos']` llamando a `medir_fn(porcentaje)` (devuelve `{'champion', 'challenger'}`), anotando `{'porcentaje', 'decision'}` y parando en `'rollback'` (estado `'rollback'`) o `'sin datos'` (estado `'pausado'`). Si todos siguen, `'promovido'`.",
            },
        ],
        "starter_files": [
            {
                "path": "reproducibilidad.py",
                "editable": True,
                "content": (
                    '"""Reproducibilidad: huellas, division y manifiesto (R1-R2)."""\n'
                    "import hashlib\n"
                    "import json\n"
                    "import random\n"
                    "\n"
                    "\n"
                    "def huella(texto, n=12):\n"
                    "    # TODO: sha256 del texto en utf-8, recortado a n caracteres\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def huella_config(config):\n"
                    "    # TODO: huella del json canonico (sort_keys y separators)\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def huella_datos(filas):\n"
                    "    # TODO: huella de la concatenacion de las huellas de cada fila\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def dividir(filas, fraccion_test, semilla):\n"
                    "    # TODO: copiar, barajar con la semilla y partir; el test va primero\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def manifiesto(filas, config, semilla, entorno, metricas):\n"
                    "    # TODO: datos, config, semilla, entorno (copiado), metricas\n"
                    "    # TODO: id = huella_config de la receta, sin las metricas\n"
                    "    pass\n"
                ),
            },
            {
                "path": "registro.py",
                "editable": True,
                "content": (
                    '"""Registro de experimentos y de modelos (R3-R4)."""\n'
                    "import hashlib\n"
                    "import pickle\n"
                    "from pathlib import Path\n"
                    "\n"
                    "\n"
                    "def nuevo_run(run_id, params):\n"
                    "    # TODO: id, params copiados, metricas, historial y estado 'en_curso'\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def registrar_metrica(run, nombre, valor, paso):\n"
                    "    # TODO: [paso, valor] al historial y el ultimo valor en metricas\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def mejor_run(runs, metrica, mayor_es_mejor=True):\n"
                    "    # TODO: solo los terminados que midieron la metrica; empate, el primero\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def guardar_modelo(modelo, ruta):\n"
                    "    # TODO: pickle.dumps -> archivo, y devolver el sha256 de esos bytes\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def cargar_modelo(ruta, checksum):\n"
                    "    # TODO: comprobar el checksum ANTES de pickle.loads\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def registrar_version(registro, nombre, run_id, checksum):\n"
                    "    # TODO: version numerada desde 1, etapa 'ninguna', y devolverla\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def promover(registro, nombre, version, etapa):\n"
                    "    # TODO: una sola version en production; la anterior se archiva\n"
                    "    pass\n"
                ),
            },
            {
                "path": "servicio.py",
                "editable": True,
                "content": (
                    '"""El servicio: contrato de entrada, vector y respuesta (R5-R6)."""\n'
                    "\n"
                    "def coaccionar(valor, tipo):\n"
                    '    """Ya escrito: convierte lo inequivoco y lanza ValueError con el resto."""\n'
                    "    if tipo == 'numero':\n"
                    "        if isinstance(valor, bool):\n"
                    "            raise ValueError('booleano no es numero')\n"
                    "        if isinstance(valor, (int, float)):\n"
                    "            return float(valor)\n"
                    "        if isinstance(valor, str):\n"
                    "            return float(valor.strip())\n"
                    "        raise ValueError('no es numero')\n"
                    "    if tipo == 'texto':\n"
                    "        if isinstance(valor, str):\n"
                    "            return valor.strip()\n"
                    "        raise ValueError('no es texto')\n"
                    "    if tipo == 'booleano':\n"
                    "        if isinstance(valor, bool):\n"
                    "            return valor\n"
                    "        if isinstance(valor, str) and valor.strip().lower() in ('true', 'false'):\n"
                    "            return valor.strip().lower() == 'true'\n"
                    "        raise ValueError('no es booleano')\n"
                    "    raise ValueError('tipo desconocido')\n"
                    "\n"
                    "\n"
                    "def validar(peticion, esquema):\n"
                    "    # TODO: recorrer el esquema; ausentes, coaccion y limites\n"
                    "    # TODO: campos desconocidos al final, ordenados\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def vector(datos, orden, mapas):\n"
                    "    # TODO: recorrer orden (no el diccionario), mapear categorias y float\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def servir(peticion, servicio, peticion_id):\n"
                    "    # TODO: 503 sin modelo, 422 con errores, 500 generico, 200 con prediccion\n"
                    "    # TODO: y cada peticion atendida al log\n"
                    "    pass\n"
                ),
            },
            {
                "path": "monitoreo.py",
                "editable": True,
                "content": (
                    '"""Monitoreo: histogramas, PSI y alertas de drift (R7-R8)."""\n'
                    "import math\n"
                    "\n"
                    "def severidad(valor):\n"
                    '    """Ya escrito: los umbrales estandar del PSI."""\n'
                    "    if valor >= 0.25:\n"
                    "        return 'critico'\n"
                    "    if valor >= 0.1:\n"
                    "        return 'aviso'\n"
                    "    return None\n"
                    "\n"
                    "\n"
                    "def tasa_error(log):\n"
                    '    """Ya escrito: proporcion de peticiones con codigo >= 400."""\n'
                    "    if not log:\n"
                    "        return 0.0\n"
                    "    return sum(1 for r in log if r['codigo'] >= 400) / len(log)\n"
                    "\n"
                    "\n"
                    "def histograma(valores, bordes):\n"
                    "    # TODO: ValueError con menos de dos bordes\n"
                    "    # TODO: un conteo por tramo; los extremos al primero y al ultimo\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def psi(referencia, actual):\n"
                    "    # TODO: validar longitudes y totales\n"
                    "    # TODO: proporciones con suelo 1e-6 y suma de (pa - pe) * log(pa / pe)\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def monitorear(log, referencia, config):\n"
                    "    # TODO: resumen del servicio y alerta de tasa de error\n"
                    "    # TODO: los 200; si no llegan al minimo, alerta de muestra y parar\n"
                    "    # TODO: columnas del orden, prediccion, y lo critico delante\n"
                    "    pass\n"
                ),
            },
            {
                "path": "despliegue.py",
                "editable": True,
                "content": (
                    '"""Despliegue: puerta, champion/challenger, rollout y rollback (R9-R10)."""\n'
                    "import hashlib\n"
                    "\n"
                    "from monitoreo import tasa_error\n"
                    "\n"
                    "def revisar_requisitos(metricas, requisitos):\n"
                    '    """Ya escrito: todos los motivos por los que un candidato no pasa."""\n'
                    "    motivos = []\n"
                    "    for nombre, regla in requisitos.items():\n"
                    "        if nombre not in metricas:\n"
                    "            motivos.append(f'{nombre}: no medida')\n"
                    "        elif 'minimo' in regla and metricas[nombre] < regla['minimo']:\n"
                    "            motivos.append(f\"{nombre}: {metricas[nombre]} < {regla['minimo']}\")\n"
                    "        elif 'maximo' in regla and metricas[nombre] > regla['maximo']:\n"
                    "            motivos.append(f\"{nombre}: {metricas[nombre]} > {regla['maximo']}\")\n"
                    "    return motivos\n"
                    "\n"
                    "\n"
                    "def puerta_de_calidad(candidato, requisitos, minimo_casos):\n"
                    "    # TODO: los motivos de los requisitos y, al final, el de los casos\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def comparar_modelos(campeon, retador, metrica, margen, mayor_es_mejor=True):\n"
                    "    # TODO: ValueError si la metrica no esta en los dos\n"
                    "    # TODO: delta (invertido si menor es mejor) y el veredicto con el margen\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def asignar_variante(peticion_id, porcentaje):\n"
                    "    # TODO: ValueError fuera de 0..100; huella -> cubo 0..99 -> variante\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def evaluar_rollout(log_champion, log_challenger, minimo, tolerancia):\n"
                    "    # TODO: 'sin datos' / 'rollback' / 'seguir'\n"
                    "    pass\n"
                    "\n"
                    "\n"
                    "def desplegar(candidato, campeon, config, medir_fn):\n"
                    "    # TODO: puerta -> rechazado; comparacion -> rechazado\n"
                    "    # TODO: recorrer los pasos con medir_fn y anotar el historial\n"
                    "    # TODO: rollback / pausado / promovido\n"
                    "    pass\n"
                ),
            },
            {
                "path": "datos.py",
                "editable": False,
                "content": (
                    '"""Datos del pipeline de Nebula (ya escrito: no hace falta tocarlo)."""\n'
                    "\n"
                    "# 200 pedidos historicos: importe, pais, urgencia y si acabaron devueltos.\n"
                    "FILAS = [\n"
                    "    {\n"
                    "        'importe': float(20 + (i * 37) % 280),\n"
                    "        'pais': ['ES', 'PT', 'FR'][i % 3],\n"
                    "        'urgente': i % 5 == 0,\n"
                    "        'devuelto': ((i * 37) % 280 > 150) != (i % 11 == 0),  # ~9% de ruido\n"
                    "    }\n"
                    "    for i in range(200)\n"
                    "]\n"
                    "\n"
                    "CONFIG = {'modelo': 'umbral', 'umbral': 170.0, 'fraccion_test': 0.25}\n"
                    "ENTORNO = {'python': '3.11', 'numpy': '2.0.2'}\n"
                    "SEMILLA = 7\n"
                    "\n"
                    "# El contrato de entrada del servicio y el vector con el que se entreno.\n"
                    "ESQUEMA = {\n"
                    "    'importe': {'tipo': 'numero', 'min': 0, 'max': 10000},\n"
                    "    'pais': {'tipo': 'texto', 'opciones': ['ES', 'PT', 'FR']},\n"
                    "    'urgente': {'tipo': 'booleano', 'por_defecto': False},\n"
                    "}\n"
                    "ORDEN = ['importe', 'pais', 'urgente']\n"
                    "MAPAS = {'pais': {'ES': 0, 'PT': 1, 'FR': 2}}\n"
                    "\n"
                    "# Histogramas del entrenamiento: los bordes se fijan aqui y no se recalculan.\n"
                    "REFERENCIA = {\n"
                    "    'columnas': {\n"
                    "        'importe': {'bordes': [0, 100, 200, 300], 'conteos': [58, 71, 71]},\n"
                    "        'pais': {'bordes': [0, 1, 2, 3], 'conteos': [67, 67, 66]},\n"
                    "    },\n"
                    "    'prediccion': {'bordes': [0, 0.5, 1], 'conteos': [110, 90]},\n"
                    "}\n"
                    "\n"
                    "CONFIG_MONITOREO = {'orden': ORDEN, 'minimo': 20, 'tasa_error_maxima': 0.1}\n"
                    "\n"
                    "CONFIG_DESPLIEGUE = {\n"
                    "    'requisitos': {'acierto': {'minimo': 0.80}, 'latencia_ms': {'maximo': 200}},\n"
                    "    'minimo_casos': 50,\n"
                    "    'metrica': 'acierto',\n"
                    "    'margen': 0.02,\n"
                    "    'pasos': [1, 10, 50],\n"
                    "    'minimo_peticiones': 20,\n"
                    "    'tolerancia': 0.02,\n"
                    "}\n"
                ),
            },
            {
                "path": "demo.py",
                "editable": True,
                "content": (
                    '"""El pipeline entero, de punta a punta (paso opcional: no se evalua).\n'
                    "\n"
                    "Pega en el editor tus cinco modulos seguidos de este archivo, quitando los\n"
                    "`from ... import` de abajo, y ejecuta. Deberia imprimir el manifiesto, la\n"
                    "version registrada, el resultado del monitoreo y el final del despliegue.\n"
                    '"""\n'
                    "from datos import (CONFIG, CONFIG_DESPLIEGUE, CONFIG_MONITOREO, ENTORNO,\n"
                    "                   ESQUEMA, FILAS, MAPAS, ORDEN, REFERENCIA, SEMILLA)\n"
                    "from reproducibilidad import dividir, manifiesto\n"
                    "from registro import (cargar_modelo, guardar_modelo, mejor_run, nuevo_run,\n"
                    "                      promover, registrar_metrica, registrar_version)\n"
                    "from servicio import servir\n"
                    "from monitoreo import monitorear\n"
                    "from despliegue import desplegar\n"
                    "\n"
                    "# 1. Un experimento reproducible: mismas filas y misma semilla, mismo id.\n"
                    "train, test = dividir(FILAS, CONFIG['fraccion_test'], SEMILLA)\n"
                    "\n"
                    "\n"
                    "def entrenar(train, umbral):\n"
                    '    """Un "modelo" de una sola regla: importe por encima del umbral, devuelto."""\n'
                    "    return {'umbral': umbral}\n"
                    "\n"
                    "\n"
                    "def acierto(modelo, filas):\n"
                    "    aciertos = sum(1 for f in filas\n"
                    "                   if (f['importe'] > modelo['umbral']) == f['devuelto'])\n"
                    "    return aciertos / len(filas)\n"
                    "\n"
                    "\n"
                    "runs = []\n"
                    "modelos = {}\n"
                    "for i, umbral in enumerate([140.0, 170.0, 200.0], start=1):\n"
                    "    run = nuevo_run(f'run-{i}', {**CONFIG, 'umbral': umbral})\n"
                    "    modelo = entrenar(train, umbral)\n"
                    "    registrar_metrica(run, 'acierto', round(acierto(modelo, test), 4), 0)\n"
                    "    run['estado'] = 'terminado'\n"
                    "    runs.append(run)\n"
                    "    modelos[run['id']] = modelo\n"
                    "\n"
                    "mejor = mejor_run(runs, 'acierto')\n"
                    "m = manifiesto(FILAS, CONFIG, SEMILLA, ENTORNO, mejor['metricas'])\n"
                    "print('experimento', m['id'], '| mejor', mejor['id'], mejor['metricas'])\n"
                    "\n"
                    "# 2. El artefacto, con su checksum, y una version en el registro.\n"
                    "checksum = guardar_modelo(modelos[mejor['id']], 'modelo.pkl')\n"
                    "registro = {}\n"
                    "entrada = registrar_version(registro, 'devoluciones', mejor['id'], checksum)\n"
                    "promover(registro, 'devoluciones', entrada['version'], 'production')\n"
                    "modelo = cargar_modelo('modelo.pkl', checksum)\n"
                    "print('version', entrada['version'], entrada['etapa'], '| checksum', checksum[:12])\n"
                    "\n"
                    "# 3. El servicio atiende peticiones y deja su log.\n"
                    "servicio = {'esquema': ESQUEMA, 'orden': ORDEN, 'mapas': MAPAS,\n"
                    "            'version': entrada['version'], 'log': [],\n"
                    "            'modelo_fn': lambda fila: 1.0 if fila[0] > modelo['umbral'] else 0.0}\n"
                    "for i, fila in enumerate(FILAS[:60]):\n"
                    "    peticion = {'importe': fila['importe'], 'pais': fila['pais'], 'urgente': fila['urgente']}\n"
                    "    servir(peticion, servicio, f'p-{i}')\n"
                    "servir({'pais': 'DE'}, servicio, 'p-mala')\n"
                    "print('peticiones', len(servicio['log']))\n"
                    "\n"
                    "# 4. El monitoreo mira ese log.\n"
                    "informe = monitorear(servicio['log'], REFERENCIA, CONFIG_MONITOREO)\n"
                    "print('resumen', informe['resumen'])\n"
                    "print('alertas', informe['alertas'])\n"
                    "\n"
                    "# 5. Y el despliegue decide si el candidato sustituye al campeon.\n"
                    "sano = [{'codigo': 200}] * 95 + [{'codigo': 500}] * 5\n"
                    "candidato = {'metricas': {**mejor['metricas'], 'latencia_ms': 90}, 'casos': len(test)}\n"
                    "campeon = {'metricas': {'acierto': 0.80, 'latencia_ms': 95}, 'casos': len(test)}\n"
                    "resultado = desplegar(candidato, campeon, CONFIG_DESPLIEGUE,\n"
                    "                      lambda p: {'champion': sano, 'challenger': sano})\n"
                    "print('despliegue', resultado['estado'], resultado['historial'])\n"
                ),
            },
        ],
        "hidden_tests": [
            {
                "name": "R1 · huellas y division reproducible",
                "code": (
                    "from reproducibilidad import huella, huella_config, huella_datos, dividir\n"
                    "h = huella('hola')\n"
                    "assert isinstance(h, str) and len(h) == 12, h\n"
                    "assert h == huella('hola') and h != huella('hola ')\n"
                    "assert len(huella('hola', 8)) == 8\n"
                    "assert huella_config({'a': 1, 'b': 2}) == huella_config({'b': 2, 'a': 1}), 'el orden de claves no cuenta'\n"
                    "assert huella_config({'a': 1}) != huella_config({'a': 1.5})\n"
                    "filas = [{'x': 1, 'y': 'a'}, {'x': 2, 'y': 'b'}, {'x': 3, 'y': 'c'}]\n"
                    "assert huella_datos(filas) == huella_datos(list(filas))\n"
                    "assert huella_datos(filas) != huella_datos(filas[::-1]), 'el orden de las filas si cuenta'\n"
                    "assert huella_datos(filas) != huella_datos(filas + filas[:1])\n"
                    "todos = [{'i': i} for i in range(12)]\n"
                    "train, test = dividir(todos, 0.25, 5)\n"
                    "assert len(test) == 3 and len(train) == 9\n"
                    "assert (train, test) == dividir(todos, 0.25, 5), 'misma semilla, misma division'\n"
                    "assert dividir(todos, 0.25, 6) != (train, test), 'otra semilla, otra division'\n"
                    "assert sorted(x['i'] for x in train + test) == list(range(12)), 'no se pierde ni se repite nada'\n"
                    "assert todos == [{'i': i} for i in range(12)], 'no se toca la lista original'\n"
                ),
            },
            {
                "name": "R2 · manifiesto con id de la receta",
                "code": (
                    "from reproducibilidad import manifiesto, huella_config, huella_datos\n"
                    "filas = [{'a': 1}, {'a': 2}]\n"
                    "config = {'modelo': 'umbral', 'umbral': 3.0}\n"
                    "entorno = {'python': '3.11'}\n"
                    "m = manifiesto(filas, config, 7, entorno, {'auc': 0.9})\n"
                    "assert m['datos'] == {'huella': huella_datos(filas), 'filas': 2}, m['datos']\n"
                    "assert m['config'] == {'huella': huella_config(config), 'valores': config}, m['config']\n"
                    "assert m['semilla'] == 7 and m['entorno'] == {'python': '3.11'} and m['metricas'] == {'auc': 0.9}\n"
                    "entorno['python'] = '3.12'\n"
                    "assert m['entorno'] == {'python': '3.11'}, 'el entorno se copia'\n"
                    "otro = manifiesto(filas, config, 7, {'python': '3.11'}, {'auc': 0.1})\n"
                    "assert otro['id'] == m['id'], 'las metricas no forman parte del id'\n"
                    "assert manifiesto(filas, config, 8, {'python': '3.11'}, {})['id'] != m['id'], 'la semilla si'\n"
                    "assert manifiesto(filas[::-1], config, 7, {'python': '3.11'}, {})['id'] != m['id'], 'los datos si'\n"
                    "esperado = huella_config({k: m[k] for k in ('datos', 'config', 'semilla', 'entorno')})\n"
                    "assert m['id'] == esperado, m['id']\n"
                ),
            },
            {
                "name": "R3 · runs, metricas y el mejor",
                "code": (
                    "from registro import nuevo_run, registrar_metrica, mejor_run\n"
                    "import json\n"
                    "params = {'umbral': 3}\n"
                    "run = nuevo_run('run-1', params)\n"
                    "assert run == {'id': 'run-1', 'params': {'umbral': 3}, 'metricas': {}, 'historial': {}, 'estado': 'en_curso'}, run\n"
                    "params['umbral'] = 99\n"
                    "assert run['params'] == {'umbral': 3}, 'los params se copian'\n"
                    "for paso, v in enumerate([0.9, 0.6, 0.45]):\n"
                    "    registrar_metrica(run, 'perdida', v, paso)\n"
                    "assert run['historial'] == {'perdida': [[0, 0.9], [1, 0.6], [2, 0.45]]}, run['historial']\n"
                    "assert run['metricas'] == {'perdida': 0.45}\n"
                    "assert json.loads(json.dumps(run)) == run, 'usa listas, no tuplas'\n"
                    "runs = [\n"
                    "    {'id': 'a', 'estado': 'terminado', 'metricas': {'auc': 0.81}},\n"
                    "    {'id': 'b', 'estado': 'fallido', 'metricas': {'auc': 0.99}},\n"
                    "    {'id': 'c', 'estado': 'terminado', 'metricas': {'perdida': 0.2}},\n"
                    "    {'id': 'd', 'estado': 'terminado', 'metricas': {'auc': 0.86}},\n"
                    "    {'id': 'e', 'estado': 'terminado', 'metricas': {'auc': 0.86}},\n"
                    "]\n"
                    "assert mejor_run(runs, 'auc')['id'] == 'd', 'en empate gana el primero'\n"
                    "assert mejor_run(runs, 'perdida', mayor_es_mejor=False)['id'] == 'c'\n"
                    "assert mejor_run(runs, 'f1') is None\n"
                    "assert mejor_run([], 'auc') is None\n"
                ),
            },
            {
                "name": "R4 · artefacto con checksum y versiones",
                "code": (
                    "from registro import guardar_modelo, cargar_modelo, registrar_version, promover\n"
                    "import hashlib, pickle, tempfile\n"
                    "from pathlib import Path\n"
                    "carpeta = Path(tempfile.mkdtemp())\n"
                    "modelo = {'tipo': 'umbral', 'umbral': 120.0}\n"
                    "ruta = carpeta / 'm.pkl'\n"
                    "checksum = guardar_modelo(modelo, ruta)\n"
                    "assert isinstance(checksum, str) and len(checksum) == 64, checksum\n"
                    "assert checksum == hashlib.sha256(ruta.read_bytes()).hexdigest()\n"
                    "assert pickle.loads(ruta.read_bytes()) == modelo\n"
                    "assert cargar_modelo(ruta, checksum) == modelo\n"
                    "ruta.write_bytes(ruta.read_bytes()[:-1] + b'!')\n"
                    "try:\n"
                    "    cargar_modelo(ruta, checksum)\n"
                    "    raise AssertionError('un artefacto alterado no se carga')\n"
                    "except ValueError:\n"
                    "    pass\n"
                    "registro = {}\n"
                    "v1 = registrar_version(registro, 'dev', 'run-1', 'aa')\n"
                    "v2 = registrar_version(registro, 'dev', 'run-3', 'bb')\n"
                    "assert v1 == {'version': 1, 'run_id': 'run-1', 'checksum': 'aa', 'etapa': 'ninguna'}, v1\n"
                    "assert v2['version'] == 2 and len(registro['dev']) == 2\n"
                    "promover(registro, 'dev', 1, 'production')\n"
                    "promover(registro, 'dev', 2, 'production')\n"
                    "assert [(v['version'], v['etapa']) for v in registro['dev']] == [(1, 'archivado'), (2, 'production')]\n"
                    "promover(registro, 'dev', 1, 'production')\n"
                    "assert [(v['version'], v['etapa']) for v in registro['dev']] == [(1, 'production'), (2, 'archivado')], 'rollback'\n"
                ),
            },
            {
                "name": "R5 · validar y vector de caracteristicas",
                "code": (
                    "from servicio import validar, vector\n"
                    "esquema = {\n"
                    "    'importe': {'tipo': 'numero', 'min': 0, 'max': 1000},\n"
                    "    'canal': {'tipo': 'texto', 'opciones': ['web', 'app']},\n"
                    "    'vip': {'tipo': 'booleano', 'por_defecto': False},\n"
                    "}\n"
                    "datos, errores = validar({'importe': '120.5', 'canal': ' web '}, esquema)\n"
                    "assert errores == [] and datos == {'importe': 120.5, 'canal': 'web', 'vip': False}, (datos, errores)\n"
                    "datos, errores = validar({'canal': 'fax', 'vip': 1, 'zona': 3, 'Canal': 'web'}, esquema)\n"
                    "assert errores == ['importe: requerido', 'canal: valor no permitido', 'vip: se esperaba booleano',\n"
                    "                   'Canal: campo desconocido', 'zona: campo desconocido'], errores\n"
                    "assert datos == {}, datos\n"
                    "assert validar({'importe': True, 'canal': 'web'}, esquema)[1] == ['importe: se esperaba numero']\n"
                    "assert validar({'importe': -1, 'canal': 'web'}, esquema)[1] == ['importe: minimo 0']\n"
                    "assert validar({'importe': 1001, 'canal': 'web'}, esquema)[1] == ['importe: maximo 1000']\n"
                    "orden = ['importe', 'canal', 'vip']\n"
                    "mapas = {'canal': {'web': 0, 'app': 1}}\n"
                    "f = vector({'vip': True, 'importe': 120.5, 'canal': 'app'}, orden, mapas)\n"
                    "assert f == [120.5, 1.0, 1.0] and all(isinstance(x, float) for x in f), f\n"
                    "for datos, mensaje in ([{'importe': 1, 'canal': 'fax', 'vip': False}, 'canal: categoria desconocida'],\n"
                    "                       [{'importe': 1, 'vip': False}, 'canal: ausente']):\n"
                    "    try:\n"
                    "        vector(datos, orden, mapas)\n"
                    "        raise AssertionError(mensaje)\n"
                    "    except ValueError as e:\n"
                    "        assert str(e) == mensaje, str(e)\n"
                ),
            },
            {
                "name": "R6 · servir con sus cuatro codigos",
                "code": (
                    "from servicio import servir\n"
                    "esquema = {'importe': {'tipo': 'numero', 'min': 0}, 'canal': {'tipo': 'texto', 'opciones': ['web']}}\n"
                    "base = {'esquema': esquema, 'orden': ['importe', 'canal'], 'mapas': {'canal': {'web': 0}}, 'version': 4}\n"
                    "s = {**base, 'log': [], 'modelo_fn': lambda f: round(f[0] / 1000, 4)}\n"
                    "r = servir({'importe': '120.5', 'canal': 'web'}, s, 'p-1')\n"
                    "assert r == {'codigo': 200, 'peticion_id': 'p-1', 'version': 4, 'cuerpo': {'prediccion': 0.1205}}, r\n"
                    "assert s['log'] == [{'id': 'p-1', 'codigo': 200, 'entrada': [120.5, 0.0], 'prediccion': 0.1205}], s['log']\n"
                    "r = servir({'canal': 'otro', 'zona': 1}, s, 'p-2')\n"
                    "assert r['codigo'] == 422 and r['version'] == 4, r\n"
                    "assert r['cuerpo'] == {'errores': ['importe: requerido', 'canal: valor no permitido',\n"
                    "                                   'zona: campo desconocido']}, r['cuerpo']\n"
                    "assert s['log'][1] == {'id': 'p-2', 'codigo': 422, 'errores': r['cuerpo']['errores']}, s['log'][1]\n"
                    "def rompe(fila):\n"
                    "    raise RuntimeError('ruta /srv/v4.pkl corrupta')\n"
                    "s2 = {**base, 'log': [], 'modelo_fn': rompe}\n"
                    "r = servir({'importe': 10, 'canal': 'web'}, s2, 'p-3')\n"
                    "assert r == {'codigo': 500, 'peticion_id': 'p-3', 'version': 4, 'cuerpo': {'error': 'error interno'}}, r\n"
                    "assert 'v4.pkl' not in str(r), 'el detalle no sale en la respuesta'\n"
                    "assert s2['log'] == [{'id': 'p-3', 'codigo': 500, 'detalle': 'ruta /srv/v4.pkl corrupta'}], s2['log']\n"
                    "s3 = {**base, 'log': [], 'modelo_fn': None}\n"
                    "r = servir({'importe': 10, 'canal': 'web'}, s3, 'p-4')\n"
                    "assert r == {'codigo': 503, 'peticion_id': 'p-4', 'version': None,\n"
                    "             'cuerpo': {'error': 'modelo no cargado'}}, r\n"
                    "assert s3['log'] == [], 'el 503 no se registra'\n"
                ),
            },
            {
                "name": "R7 · histograma y PSI",
                "code": (
                    "from monitoreo import histograma, psi\n"
                    "bordes = [0, 50, 100, 200]\n"
                    "assert histograma([10, 60, 70, 120, 999], bordes) == [1, 2, 2]\n"
                    "assert histograma([-5, 0, 49.9], bordes) == [3, 0, 0]\n"
                    "assert histograma([], bordes) == [0, 0, 0]\n"
                    "assert histograma([50, 99.99], bordes) == [0, 2, 0]\n"
                    "valores = [-100, 0, 5, 10, 19, 20, 29, 30, 39, 40, 1000]\n"
                    "c = histograma(valores, [0, 10, 20, 30, 40])\n"
                    "assert c == [3, 2, 2, 4] and sum(c) == len(valores), c\n"
                    "for malos in ([], [0]):\n"
                    "    try:\n"
                    "        histograma([1], malos)\n"
                    "        raise AssertionError('con menos de dos bordes no hay tramos')\n"
                    "    except ValueError:\n"
                    "        pass\n"
                    "ref = [10, 40, 30, 20]\n"
                    "assert psi(ref, ref) == 0.0\n"
                    "assert abs(psi(ref, [20, 80, 60, 40])) < 1e-9, 'la misma forma con mas datos no es drift'\n"
                    "assert round(psi(ref, [12, 38, 32, 18]), 4) == 0.0081\n"
                    "assert round(psi(ref, [25, 35, 25, 15]), 4) == 0.1676\n"
                    "assert round(psi(ref, [40, 30, 20, 10]), 4) == 0.5545\n"
                    "assert round(psi(ref, [0, 40, 30, 30]), 4) == 1.1918, 'el suelo evita el infinito'\n"
                    "for a, b in ([[1, 2], [1, 2, 3]], [[0, 0], [1, 2]], [[1, 2], [0, 0]]):\n"
                    "    try:\n"
                    "        psi(a, b)\n"
                    "        raise AssertionError(f'{a} vs {b} deberia lanzar ValueError')\n"
                    "    except ValueError:\n"
                    "        pass\n"
                ),
            },
            {
                "name": "R8 · monitorear el log del servicio",
                "code": (
                    "from monitoreo import monitorear\n"
                    "referencia = {\n"
                    "    'columnas': {'importe': {'bordes': [0, 50, 100, 200], 'conteos': [10, 40, 30]},\n"
                    "                 'canal': {'bordes': [0, 1, 2, 3], 'conteos': [10, 40, 30]}},\n"
                    "    'prediccion': {'bordes': [0, 0.25, 0.5, 1], 'conteos': [10, 40, 30]},\n"
                    "}\n"
                    "config = {'orden': ['importe', 'canal'], 'minimo': 4, 'tasa_error_maxima': 0.2}\n"
                    "log = [{'codigo': 200, 'entrada': [10.0, 0.0], 'prediccion': 0.1} for _ in range(10)]\n"
                    "log += [{'codigo': 200, 'entrada': [60.0, 1.0], 'prediccion': 0.3} for _ in range(40)]\n"
                    "log += [{'codigo': 200, 'entrada': [150.0, 2.0], 'prediccion': 0.8} for _ in range(30)]\n"
                    "r = monitorear(log, referencia, config)\n"
                    "assert r['resumen'] == {'peticiones': 80, 'por_codigo': {200: 80}, 'tasa_error': 0.0}, r['resumen']\n"
                    "assert r['alertas'] == [], r['alertas']\n"
                    "r = monitorear([{'codigo': 200, 'entrada': [10.0, 0.0], 'prediccion': 0.1}] * 3, referencia, config)\n"
                    "assert r['alertas'] == [{'tipo': 'muestra', 'valor': 3, 'severidad': 'aviso'}], r['alertas']\n"
                    "r = monitorear([], referencia, config)\n"
                    "assert r['resumen'] == {'peticiones': 0, 'por_codigo': {}, 'tasa_error': 0.0}, r['resumen']\n"
                    "assert r['alertas'] == [{'tipo': 'muestra', 'valor': 0, 'severidad': 'aviso'}], r['alertas']\n"
                    "malo = log + [{'codigo': 422, 'errores': ['importe: requerido']} for _ in range(40)]\n"
                    "r = monitorear(malo, referencia, config)\n"
                    "assert r['alertas'][0] == {'tipo': 'errores', 'valor': 0.3333, 'severidad': 'critico'}, r['alertas']\n"
                    "assert r['resumen']['por_codigo'] == {200: 80, 422: 40}, r['resumen']\n"
                    "movido = [{'codigo': 200, 'entrada': [10.0, 0.0], 'prediccion': 0.1} for _ in range(60)]\n"
                    "movido += [{'codigo': 200, 'entrada': [60.0, 1.0], 'prediccion': 0.3} for _ in range(20)]\n"
                    "r = monitorear(movido, referencia, config)\n"
                    "tipos = [(a['tipo'], a.get('columna'), a['severidad']) for a in r['alertas']]\n"
                    "assert ('drift', 'importe', 'critico') in tipos and ('drift', 'prediccion', 'critico') in tipos, tipos\n"
                    "assert all(a['psi'] == round(a['psi'], 4) for a in r['alertas'] if a['tipo'] == 'drift')\n"
                    "mezcla = [{'codigo': 200, 'entrada': [10.0, 0.0], 'prediccion': 0.1} for _ in range(25)]\n"
                    "mezcla += [{'codigo': 200, 'entrada': [60.0, 1.0], 'prediccion': 0.3} for _ in range(45)]\n"
                    "mezcla += [{'codigo': 200, 'entrada': [150.0, 2.0], 'prediccion': 0.8} for _ in range(30)]\n"
                    "r = monitorear(mezcla, referencia, config)\n"
                    "sev = [a['severidad'] for a in r['alertas']]\n"
                    "assert sev == sorted(sev, key=lambda s: 0 if s == 'critico' else 1), sev\n"
                ),
            },
            {
                "name": "R9 · puerta, comparacion y reparto",
                "code": (
                    "from despliegue import puerta_de_calidad, comparar_modelos, asignar_variante\n"
                    "requisitos = {'auc': {'minimo': 0.85}, 'latencia_ms': {'maximo': 200}}\n"
                    "bueno = {'metricas': {'auc': 0.9, 'latencia_ms': 120}, 'casos': 400}\n"
                    "assert puerta_de_calidad(bueno, requisitos, 100) == {'pasa': True, 'motivos': []}\n"
                    "pocos = {'metricas': {'auc': 0.99, 'latencia_ms': 10}, 'casos': 7}\n"
                    "assert puerta_de_calidad(pocos, requisitos, 100) == {'pasa': False, 'motivos': ['casos: 7 < 100']}\n"
                    "malo = {'metricas': {'auc': 0.5}, 'casos': 10}\n"
                    "r = puerta_de_calidad(malo, requisitos, 100)\n"
                    "assert r['motivos'] == ['auc: 0.5 < 0.85', 'latencia_ms: no medida', 'casos: 10 < 100'], r['motivos']\n"
                    "assert comparar_modelos({'auc': 0.86}, {'auc': 0.87}, 'auc', 0.02) == {'delta': 0.01, 'gana': False}\n"
                    "assert comparar_modelos({'auc': 0.86}, {'auc': 0.88}, 'auc', 0.02)['gana'] is True, 'el margen justo gana'\n"
                    "r = comparar_modelos({'perdida': 0.30}, {'perdida': 0.22}, 'perdida', 0.05, mayor_es_mejor=False)\n"
                    "assert r == {'delta': 0.08, 'gana': True}, r\n"
                    "try:\n"
                    "    comparar_modelos({'auc': 0.8}, {}, 'auc', 0.01)\n"
                    "    raise AssertionError('sin la metrica en los dos no hay comparacion')\n"
                    "except ValueError:\n"
                    "    pass\n"
                    "ids = [f'p-{i}' for i in range(2000)]\n"
                    "assert all(asignar_variante(i, 0) == 'champion' for i in ids)\n"
                    "assert all(asignar_variante(i, 100) == 'challenger' for i in ids)\n"
                    "diez = {i for i in ids if asignar_variante(i, 10) == 'challenger'}\n"
                    "cincuenta = {i for i in ids if asignar_variante(i, 50) == 'challenger'}\n"
                    "assert diez <= cincuenta and len(diez) < len(cincuenta), 'estable y monotono'\n"
                    "assert abs(len(diez) / len(ids) * 100 - 10) < 3, len(diez)\n"
                    "for p in (-1, 101):\n"
                    "    try:\n"
                    "        asignar_variante('p-1', p)\n"
                    "        raise AssertionError('porcentaje invalido')\n"
                    "    except ValueError:\n"
                    "        pass\n"
                ),
            },
            {
                "name": "R10 · rollout y los cuatro finales",
                "code": (
                    "from despliegue import evaluar_rollout, desplegar\n"
                    "sano = [{'codigo': 200}] * 95 + [{'codigo': 500}] * 5\n"
                    "roto = [{'codigo': 200}] * 80 + [{'codigo': 500}] * 20\n"
                    "assert evaluar_rollout(sano, roto, 50, 0.02) == 'rollback'\n"
                    "assert evaluar_rollout(sano, sano, 50, 0.02) == 'seguir'\n"
                    "assert evaluar_rollout(sano, roto, 500, 0.02) == 'sin datos'\n"
                    "assert evaluar_rollout(sano, roto, 50, 0.2) == 'seguir', 'con mas tolerancia aguanta'\n"
                    "config = {'requisitos': {'auc': {'minimo': 0.85}}, 'minimo_casos': 100, 'metrica': 'auc',\n"
                    "          'margen': 0.02, 'pasos': [1, 10, 50], 'minimo_peticiones': 50, 'tolerancia': 0.02}\n"
                    "candidato = {'metricas': {'auc': 0.90}, 'casos': 400}\n"
                    "campeon = {'metricas': {'auc': 0.86}, 'casos': 400}\n"
                    "llamadas = []\n"
                    "def medir(p):\n"
                    "    llamadas.append(p)\n"
                    "    return {'champion': sano, 'challenger': sano}\n"
                    "r = desplegar(candidato, campeon, config, medir)\n"
                    "assert r['estado'] == 'promovido' and r['motivos'] == [], r\n"
                    "assert llamadas == [1, 10, 50] and [h['porcentaje'] for h in r['historial']] == [1, 10, 50], r['historial']\n"
                    "assert all(h['decision'] == 'seguir' for h in r['historial'])\n"
                    "llamadas.clear()\n"
                    "r = desplegar({'metricas': {'auc': 0.5}, 'casos': 10}, campeon, config, medir)\n"
                    "assert r['estado'] == 'rechazado' and r['historial'] == [] and llamadas == [], r\n"
                    "assert r['motivos'] == ['auc: 0.5 < 0.85', 'casos: 10 < 100'], r['motivos']\n"
                    "r = desplegar({'metricas': {'auc': 0.87}, 'casos': 400}, campeon, config, medir)\n"
                    "assert r['estado'] == 'rechazado' and r['motivos'] == ['no mejora al campeon: delta 0.01'], r\n"
                    "assert desplegar({'metricas': {'auc': 0.87}, 'casos': 400}, None, config, medir)['estado'] == 'promovido'\n"
                    "r = desplegar(candidato, campeon, config,\n"
                    "              lambda p: {'champion': sano, 'challenger': sano if p == 1 else roto})\n"
                    "assert r['estado'] == 'rollback', r\n"
                    "assert r['historial'] == [{'porcentaje': 1, 'decision': 'seguir'},\n"
                    "                          {'porcentaje': 10, 'decision': 'rollback'}], r['historial']\n"
                    "r = desplegar(candidato, campeon, config, lambda p: {'champion': sano[:10], 'challenger': sano[:10]})\n"
                    "assert r['estado'] == 'pausado', r\n"
                    "assert r['historial'] == [{'porcentaje': 1, 'decision': 'sin datos'}], r['historial']\n"
                ),
            },
        ],
        "estimated_hours": 16,
        "difficulty": "advanced",
        "order_index": 6,
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
