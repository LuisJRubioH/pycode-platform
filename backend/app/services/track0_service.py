"""Corrección de los ejercicios que no se ejecutan (Track 0).

El resto de la plataforma valida con `hidden_tests` corridos en Pyodide, pero
el pseudocódigo y los diagramas de flujo de Track 0 no se ejecutan. Estos
ejercicios se corrigen **aquí, en el backend**, de forma determinista: sin
Pyodide y sin LLM.

Por qué en el backend y no en el cliente: la regla 3 de `docs/TRACK_0.md` pide
que la solución correcta no viaje al cliente (mismo guard rail de no-leak que
`hidden_tests`). Un validador de cliente necesita la respuesta para comparar, y
mandarla hasheada no salva nada cuando el valor de una celda es "3": se saca
por fuerza bruta en el navegador. Así que el cliente manda lo que escribió el
alumno y el backend contesta si está bien.

El feedback dice **dónde** falla, nunca cuál era el valor correcto: es la mitad
de la ayuda que hace que el alumno vuelva a trazar el bucle en vez de copiar.

Añadir un tipo nuevo = una función `_validar_<tipo>` y su entrada en
`VALIDADORES`; ni el endpoint ni el modelo cambian.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


class EjercicioInvalido(ValueError):
    """El ejercicio está mal seedeado (tipo desconocido o answer_key vacía)."""


@dataclass
class Veredicto:
    """Resultado de corregir una respuesta.

    `feedback` señala el primer punto que falla sin revelar el valor esperado.
    `detalle` es opcional y solo se rellena cuando ayuda a la UI a marcar el
    sitio exacto (p. ej. la celda de la traza que hay que repasar).
    """

    passed: bool
    feedback: str | None = None
    detalle: dict[str, Any] = field(default_factory=dict)


def _texto(valor: Any) -> str:
    """Normaliza una celda o una opción: str, sin espacios sobrantes."""
    return " ".join(str(valor if valor is not None else "").split())


def _normalizar_salida(valor: Any) -> list[str]:
    """Salida de pantalla -> lista de líneas comparables.

    Se ignoran los espacios de sobra y las líneas vacías del final, que es lo
    que pide el doc ("comparación normalizada"). Las mayúsculas **sí** cuentan:
    el alumno está copiando lo que escribiría el algoritmo.
    """
    lineas = [" ".join(linea.split()) for linea in str(valor or "").splitlines()]
    while lineas and not lineas[-1]:
        lineas.pop()
    return lineas


def _validar_trace_table(clave: dict, respuesta: dict) -> Veredicto:
    """Tabla de traza: se compara celda a celda, en orden de lectura.

    El tipo central del track. `clave['celdas']` es una lista de filas y cada
    fila una lista de valores, en el orden de `spec['columnas']`.
    """
    esperadas = clave.get("celdas")
    if not esperadas:
        raise EjercicioInvalido("la answer_key no trae celdas")
    dadas = respuesta.get("celdas")
    if not isinstance(dadas, list):
        return Veredicto(False, "Completa la tabla antes de comprobarla.")
    if len(dadas) != len(esperadas):
        return Veredicto(
            False,
            f"La tabla tiene {len(esperadas)} filas y enviaste {len(dadas)}.",
        )

    etiquetas = clave.get("etiquetas_filas") or []
    columnas = clave.get("columnas") or []
    for f, (fila_ok, fila_dada) in enumerate(zip(esperadas, dadas)):
        if not isinstance(fila_dada, list) or len(fila_dada) != len(fila_ok):
            return Veredicto(False, f"La fila {f + 1} está incompleta.")
        for c, (celda_ok, celda_dada) in enumerate(zip(fila_ok, fila_dada)):
            if _texto(celda_ok) != _texto(celda_dada):
                fila = etiquetas[f] if f < len(etiquetas) else f"fila {f + 1}"
                columna = columnas[c] if c < len(columnas) else f"columna {c + 1}"
                return Veredicto(
                    False,
                    f"Repasa «{fila}», columna «{columna}»: vuelve a seguir "
                    "el algoritmo hasta ahí.",
                    {"fila": f, "columna": c},
                )
    return Veredicto(True, "Traza correcta: seguiste el algoritmo paso a paso.")


def _validar_predict_output(clave: dict, respuesta: dict) -> Veredicto:
    """Qué escribe el algoritmo: se comparan las líneas normalizadas."""
    if "salida" not in clave:
        raise EjercicioInvalido("la answer_key no trae salida")
    esperada = _normalizar_salida(clave["salida"])
    dada = _normalizar_salida(respuesta.get("salida"))
    if not dada:
        return Veredicto(False, "Escribe la salida antes de comprobarla.")
    if len(dada) != len(esperada):
        return Veredicto(
            False,
            f"Tu respuesta tiene {len(dada)} líneas y el algoritmo escribe "
            f"{len(esperada)}. Cuenta cuántas veces se ejecuta el Escribir.",
        )
    for i, (linea_ok, linea_dada) in enumerate(zip(esperada, dada)):
        if linea_ok != linea_dada:
            return Veredicto(
                False,
                f"La línea {i + 1} no coincide. Traza el algoritmo hasta ese "
                "Escribir y comprueba el valor de cada variable.",
                {"linea": i},
            )
    return Veredicto(True, "Correcto: eso es exactamente lo que escribe.")


def _validar_mcq(clave: dict, respuesta: dict) -> Veredicto:
    """Opción múltiple: índice exacto.

    Al acertar se devuelve el `motivo` como explicación. Al fallar no se dice
    cuál era: los distractores son errores reales y el alumno tiene que volver
    al enunciado.
    """
    if "correcta" not in clave:
        raise EjercicioInvalido("la answer_key no trae la opción correcta")
    dada = respuesta.get("opcion")
    if dada is None:
        return Veredicto(False, "Elige una opción.")
    if not isinstance(dada, int) or isinstance(dada, bool):
        return Veredicto(False, "La opción tiene que ser un número.")
    if dada != clave["correcta"]:
        return Veredicto(
            False,
            clave.get("pista") or "No es esa. Vuelve al enunciado y descarta.",
        )
    return Veredicto(True, clave.get("motivo") or "Correcto.")


def _validar_por_posiciones(clave, respuesta, campo, etiquetas, singular):
    """Comun a los dos tipos de diagrama: una eleccion por hueco o fragmento.

    La respuesta es una lista de indices (que opcion se eligio para cada
    posicion), asi que corregir es compararla posicion a posicion. El feedback
    nombra el primero que falla usando su etiqueta, sin decir cual era.
    """
    esperadas = clave.get(campo)
    if not esperadas:
        raise EjercicioInvalido(f"la answer_key no trae {campo}")
    dadas = respuesta.get(campo)
    if not isinstance(dadas, list) or len(dadas) != len(esperadas):
        return Veredicto(False, f"Contesta {singular} antes de comprobar.")
    nombres = clave.get(etiquetas) or []
    for i, (ok, dada) in enumerate(zip(esperadas, dadas)):
        if dada is None:
            nombre = nombres[i] if i < len(nombres) else f"el numero {i + 1}"
            return Veredicto(False, f"Te falta «{nombre}».", {"posicion": i})
        if not isinstance(dada, int) or isinstance(dada, bool) or dada != ok:
            nombre = nombres[i] if i < len(nombres) else f"el numero {i + 1}"
            return Veredicto(
                False,
                f"Repasa «{nombre}»: compara el diagrama con el pseudocodigo "
                "linea a linea.",
                {"posicion": i},
            )
    return Veredicto(True, "Correcto: el diagrama y el pseudocodigo dicen lo mismo.")


def _validar_flowchart_match(clave: dict, respuesta: dict) -> Veredicto:
    """Emparejar cada fragmento de pseudocodigo con su diagrama."""
    return _validar_por_posiciones(
        clave, respuesta, "asignaciones", "etiquetas_fragmentos", "todos los fragmentos"
    )


def _validar_flowchart_fill(clave: dict, respuesta: dict) -> Veredicto:
    """Rellenar los nodos vacios de un diagrama desde un banco de opciones."""
    return _validar_por_posiciones(
        clave, respuesta, "huecos", "etiquetas_huecos", "todos los huecos"
    )


VALIDADORES: dict[str, Callable[[dict, dict], Veredicto]] = {
    "trace_table": _validar_trace_table,
    "predict_output": _validar_predict_output,
    "mcq": _validar_mcq,
    "flowchart_match": _validar_flowchart_match,
    "flowchart_fill": _validar_flowchart_fill,
}

# Tipos que corrige el backend. "code" no está: ese sigue yendo por Pyodide y
# `POST /exercises/{id}/submit`.
TIPOS_VALIDABLES = frozenset(VALIDADORES)


def validar(exercise_type: str, answer_key: Any, respuesta: Any) -> Veredicto:
    """Corrige `respuesta` contra `answer_key` según el tipo del ejercicio."""
    validador = VALIDADORES.get(exercise_type)
    if validador is None:
        raise EjercicioInvalido(f"tipo de ejercicio no validable: {exercise_type}")
    if not isinstance(answer_key, dict) or not answer_key:
        raise EjercicioInvalido("el ejercicio no tiene answer_key")
    if not isinstance(respuesta, dict):
        return Veredicto(False, "No recibí ninguna respuesta.")
    return validador(answer_key, respuesta)
