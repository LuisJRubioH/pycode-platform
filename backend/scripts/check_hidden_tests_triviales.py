"""
Falla si algun `hidden_test` aprueba con el starter intacto.

Un test que pasa sin que el alumno escriba una linea no comprueba nada: da el
ejercicio por hecho (y suma sus puntos) con el codigo vacio. Paso a paso:

1. Recorre los `LESSON_TEMPLATES` de `lesson_seed.py` (lo que se seedea).
2. Ejecuta cada `hidden_test` contra el `starter_code` de SU ejercicio,
   imitando al worker de Pyodide (`frontend/src/sandbox/pyodideWorker.ts`):
   namespace fresco por test, stdout del alumno capturado en `_salida`,
   `await` de nivel superior permitido y un modulo `pycode` con
   `load_dataset`.
3. En los retos, que guardan solucion de referencia, comprueba ademas que
   todos sus tests aprueban con ella.
4. Si algo falla, lo lista y sale con codigo 1.

Es una **cota inferior**: CPython no es Pyodide (versiones de numpy/pandas
distintas, sin paquetes que Pyodide carga solo), y un test que aqui falla por un
import que falta cuenta como no trivial aunque en el navegador pasara.

Uso:
    cd backend && python scripts/check_hidden_tests_triviales.py
    cd backend && python scripts/check_hidden_tests_triviales.py --json
"""

from __future__ import annotations

import ast
import asyncio
import contextlib
import io
import json
import os
import sys
import tempfile
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Sin display: matplotlib no debe intentar abrir ventanas.
os.environ.setdefault("MPLBACKEND", "Agg")


def _modulo_pycode() -> types.ModuleType:
    """Imitacion minima del modulo `pycode` que registra el worker."""
    from app.services.dataset_seed import _build_templates

    csv_por_slug = {t.slug: t.csv_content for t in _build_templates()}
    mod = types.ModuleType("pycode")

    async def load_dataset(slug):
        import pandas as pd

        if slug not in csv_por_slug:
            raise FileNotFoundError(f"Dataset no encontrado: {slug!r}")
        return pd.read_csv(io.StringIO(csv_por_slug[slug]))

    async def llm_complete(prompt, system="", max_tokens=256, temperature=0.4):
        return "respuesta de prueba"

    mod.load_dataset = load_dataset
    mod.llm_complete = llm_complete
    return mod


# Mismo envoltorio que `Kernel.runTests` en el worker.
PLANTILLA = (
    "import sys as _sys, io as _io\n_sys.stdout = _io.StringIO()\n"
    "{starter}\n"
    "_salida = _sys.stdout.getvalue()\n_sys.stdout = _sys.__stdout__\n\n"
    "{test}\n"
)


def _aprueba(starter: str, test: str) -> bool:
    programa = PLANTILLA.format(starter=starter, test=test)
    cwd_real = os.getcwd()
    stdout_real, stdin_real = sys.stdout, sys.stdin
    # Directorio nuevo por test: si no, un archivo que dejo un test anterior
    # puede hacer aprobar al siguiente sin que el codigo escriba nada.
    with tempfile.TemporaryDirectory(prefix="hidden_test_") as tmp:
        os.chdir(tmp)
        # En Pyodide el directorio de trabajo esta en sys.path: un test puede
        # escribir `saludos.py` e importarlo. Aqui hay que ponerlo a mano.
        sys.path.insert(0, tmp)
        modulos_antes = set(sys.modules)
        # stdin vacio: un `input()` en el starter falla en vez de colgar.
        sys.stdin = io.StringIO("")
        try:
            codigo = compile(
                programa,
                "<hidden_test>",
                "exec",
                flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT,
            )
            with contextlib.redirect_stderr(io.StringIO()):
                resultado = eval(codigo, {})  # noqa: S307 - contenido del repo
                if asyncio.iscoroutine(resultado):
                    asyncio.run(resultado)
            return True
        except KeyboardInterrupt:
            raise
        except BaseException:  # noqa: BLE001 - SystemExit tambien es "falla"
            return False
        finally:
            sys.stdout, sys.stdin = stdout_real, stdin_real
            # Los modulos que el test escribio e importo (p.ej. `saludos.py`)
            # quedarian cacheados y el siguiente test los veria sin crearlos.
            sys.path.remove(tmp)
            # Solo los modulos que aparecieron durante este test: mirar todo
            # sys.modules con realpath en cada test multiplicaba el tiempo.
            raiz = os.path.normcase(os.path.realpath(tmp))
            for nombre in set(sys.modules) - modulos_antes:
                archivo = getattr(sys.modules[nombre], "__file__", None)
                if archivo and os.path.normcase(os.path.realpath(archivo)).startswith(
                    raiz
                ):
                    del sys.modules[nombre]
            # Windows no borra el directorio en uso: salir antes de limpiarlo.
            os.chdir(cwd_real)
            try:
                import matplotlib.pyplot as plt

                plt.close("all")
            except Exception:  # noqa: BLE001
                pass


def _casos_retos():
    """(problema, nivel, starter, solucion, tests) de cada reto."""
    from app.services.curated_retos import CURATED_RETOS
    from app.services.generated_bank import CHALLENGE_TEMPLATES, NIVELES
    from app.services.retos_validacion import TESTS_CURADOS, VALIDACION_GENERADOS

    for template in CHALLENGE_TEMPLATES:
        for difficulty, _, nivel in NIVELES:
            validacion = VALIDACION_GENERADOS[(template.slug_base, difficulty)]
            yield (
                template.title,
                f"nivel {nivel} ({difficulty})",
                getattr(template, difficulty).starter_code,
                validacion.reference_solution,
                validacion.hidden_tests,
            )
    for reto in CURATED_RETOS:
        yield (
            reto.title,
            reto.difficulty,
            reto.starter_code,
            reto.reference_solution,
            TESTS_CURADOS[reto.slug_suffix],
        )


def barrer() -> list[dict]:
    from app.services.lesson_seed import LESSON_TEMPLATES

    sys.modules["pycode"] = _modulo_pycode()
    resultados = []
    for leccion in LESSON_TEMPLATES:
        for ejercicio in leccion.exercises:
            for test in ejercicio.hidden_tests:
                resultados.append(
                    {
                        "track": leccion.track,
                        "leccion": leccion.title,
                        "ejercicio": ejercicio.title,
                        "test": test["name"],
                        "aprueba_con_starter": _aprueba(
                            ejercicio.starter_code, test["code"]
                        ),
                        # Las lecciones no guardan solucion de referencia.
                        "aprueba_con_solucion": None,
                    }
                )
    # Los retos si la guardan: ademas de "no aprueba con el starter" se
    # comprueba la otra mitad, "aprueba con una solucion correcta".
    for problema, nivel, starter, solucion, tests in _casos_retos():
        for test in tests:
            resultados.append(
                {
                    "track": "retos",
                    "leccion": problema,
                    "ejercicio": nivel,
                    "test": test["name"],
                    "aprueba_con_starter": _aprueba(starter, test["code"]),
                    "aprueba_con_solucion": _aprueba(solucion, test["code"]),
                }
            )
    return resultados


def main() -> int:
    resultados = barrer()
    triviales = [r for r in resultados if r["aprueba_con_starter"]]
    rotos = [r for r in resultados if r["aprueba_con_solucion"] is False]
    fallo = bool(triviales or rotos)

    if "--json" in sys.argv:
        print(json.dumps(resultados, ensure_ascii=False))
        return 1 if fallo else 0

    por_track: dict[str, list[int]] = {}
    for r in resultados:
        cuenta = por_track.setdefault(r["track"], [0, 0])
        cuenta[0] += 1
        cuenta[1] += r["aprueba_con_starter"]
    print("track   | tests | pasan con el starter")
    for track in sorted(por_track):
        total, pasan = por_track[track]
        print(f"{track:7} | {total:5d} | {pasan:2d}")

    def _linea(r):
        return f"  [{r['track']}] {r['leccion']} / {r['ejercicio']} / {r['test']}"

    if triviales:
        print(f"\n{len(triviales)} hidden_tests aprueban con el starter intacto:")
        print("\n".join(_linea(r) for r in triviales))
    if rotos:
        print(f"\n{len(rotos)} tests de retos FALLAN con la solucion de referencia:")
        print("\n".join(_linea(r) for r in rotos))
    if not fallo:
        print(
            "\nOK: ningun hidden_test aprueba con el starter, y los de retos "
            "aprueban con su solucion."
        )
    return 1 if fallo else 0


if __name__ == "__main__":
    sys.exit(main())
