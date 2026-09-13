"""Guard rail: ningun hidden_test aprueba con el starter intacto, y los de los
retos aprueban con su solucion de referencia.

Un test que pasa sin que el alumno escriba nada da el ejercicio por hecho, y
con el sus puntos. El barrido vive en `scripts/check_hidden_tests_triviales.py`
(se puede correr a mano) y aqui se ejecuta en un subproceso: ejecuta codigo de
los ejercicios, cambia de directorio y toca `sys.modules`, y nada de eso debe
ensuciar el proceso de pytest.

Si falla: al test que aparece en la lista le falta la comprobacion positiva
(que el resultado exista y valga lo que debe). Anadela sin quitar la negativa;
ver docs/PLANTILLA_LECCION.md.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1] / "scripts" / "check_hidden_tests_triviales.py"
)


def test_ningun_hidden_test_aprueba_con_el_starter():
    proceso = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=600,
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    assert (
        proceso.stdout.strip()
    ), f"el barrido no produjo salida:\n{proceso.stderr[-2000:]}"
    resultados = json.loads(proceso.stdout.strip().splitlines()[-1])

    # Si el barrido no recorre nada, el guard rail no protege: que se note.
    assert len(resultados) > 300, f"solo se barrieron {len(resultados)} tests"

    triviales = [
        f"[{r['track']}] {r['leccion']} / {r['ejercicio']} / {r['test']}"
        for r in resultados
        if r["aprueba_con_starter"]
    ]
    assert (
        not triviales
    ), "hidden_tests que aprueban con el starter intacto:\n" + "\n".join(triviales)

    rotos = [
        f"[{r['track']}] {r['leccion']} / {r['ejercicio']} / {r['test']}"
        for r in resultados
        if r["aprueba_con_solucion"] is False
    ]
    assert not rotos, "tests de retos que fallan con su solucion:\n" + "\n".join(rotos)
