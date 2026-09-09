"""Regla de contenido: nada se pide antes de haberse enseñado.

Un ejercicio no puede exigir un concepto que su lección —o una anterior del
temario— no haya mostrado **dentro de un bloque de código ejecutable**. La
prosa no cuenta: "Usa `__init__` para estado inicial" en una viñeta no enseña
a escribir un método.

Por qué esto es un test y no una buena intención: en la auditoría de contenido
(``docs/AUDITORIA_CONTENIDO.md``) se encontró que ``def`` no aparece en NINGUNA
lección de Track 1, y aun así cinco ejercicios lo exigen desde la lección 5. El
alumno escribe su primera función sin haber visto nunca una definición.

## Cómo se manejó la deuda

En vez de marcar el test como ``xfail`` —que lo dejaría dormido y sin proteger
nada— se congeló la lista exacta de huecos conocidos en ``HUECOS_CONOCIDOS`` y
se comparó por igualdad. Así el test estuvo **activo desde el primer día**:

- si aparece un hueco nuevo, falla (protege contra regresiones ya);
- si se cierra uno de los conocidos, también falla, pidiendo que se borre de la
  lista (impide que la deuda se quede escrita para siempre).

Los 13 huecos se cerraron entre el 2026-09-03 y el 2026-09-09 reescribiendo
"Funciones y Parametros", "Comprensiones y Manejo de Errores" y "POO en
Python". La lista está vacía y el test es ya un guard rail permanente, sin
haber tocado una línea de su lógica.

## Límite conocido

El detector busca *tokens de Python*, no paráfrasis en español. "Cuenta
bancaria" pide "lanza ValueError" sin escribir ``raise`` en el enunciado ni en
el starter, así que ese hueco NO se detecta aquí aunque sea real. El detector
es un suelo, no un techo.
"""

import re
import sys

from app.services.lesson_seed import (
    LESSON_TEMPLATES,
    ExerciseTemplate,
    LessonTemplate,
)

# Tokens que un principiante no puede deducir: o los ha visto escritos, o no.
CONCEPTOS = {
    "def": r"\bdef\s+\w+\s*\(",
    "class": r"\bclass\s+\w+",
    "self": r"\bself\b",
    "raise": r"\braise\b",
    "break": r"\bbreak\b",
    "continue": r"\bcontinue\b",
    "lambda": r"\blambda\b",
    "yield": r"\byield\b",
    "try/except": r"\bexcept\b",
    "with": r"\bwith\s+\w",
    "__init__": r"__init__",
    "decorador": r"^\s*@\w+",
}

_FENCE = re.compile(r"```.*?\n(.*?)```", re.S)


def ejemplos_ejecutables(content: str | None) -> str:
    """Solo el código dentro de bloques ```. La prosa explicativa no enseña sintaxis."""
    return "\n".join(_FENCE.findall(content or ""))


def _conceptos_en(texto: str) -> set[str]:
    return {
        nombre for nombre, patron in CONCEPTOS.items() if re.search(patron, texto, re.M)
    }


def detectar_huecos() -> set[tuple[str, str, str]]:
    """(lección, ejercicio, concepto) de todo lo que se pide sin haberse enseñado.

    Recorre el temario en su orden real (track, luego ``order``) acumulando lo
    que ya se mostró: una lección de Track 3 puede apoyarse en algo que enseñó
    Track 1, igual que hace el alumno.
    """
    vistos: set[str] = set()
    huecos: set[tuple[str, str, str]] = set()

    for leccion in sorted(LESSON_TEMPLATES, key=lambda t: (t.track, t.order)):
        # Lo que enseña ESTA lección ya está disponible para sus propios
        # ejercicios: el alumno lee la teoría antes de resolverlos.
        disponibles = vistos | _conceptos_en(ejemplos_ejecutables(leccion.content))

        for ejercicio in leccion.exercises:
            # Solo lo que el alumno ve: enunciado y starter code. Los
            # hidden_tests los escribe el autor y no enseñan nada.
            expuesto = (
                (ejercicio.instructions or "") + "\n" + (ejercicio.starter_code or "")
            )
            for concepto in _conceptos_en(expuesto) - disponibles:
                huecos.add((leccion.title, ejercicio.title, concepto))

        vistos = disponibles

    return huecos


# Deuda de contenido saldada. Empezo con 13 huecos el 2026-09-03 y se fue
# encogiendo con la reescritura de Track 1 (plan en docs/PLANTILLA_LECCION.md):
# 8 tras "Funciones y Parametros" (cerro los 5 de `def`), 6 tras "Comprensiones
# y Manejo de Errores" (`raise` de AI 2 y `with` del ejercicio de pytest) y 0
# tras "POO en Python" (`class`, `self` e `__init__`, que hasta entonces solo
# aparecian en la prosa y en el starter).
#
# Vacio no significa muerto: el test deja de proteger deuda y pasa a ser un
# guard rail puro. Si al escribir una leccion nueva sale un hueco, la respuesta
# por defecto es ensenar el concepto con un ejemplo, no anotarlo aqui.
HUECOS_CONOCIDOS: set[tuple[str, str, str]] = set()


def test_la_prosa_no_cuenta_como_ejemplo():
    """El corazón de la regla: solo enseña lo que está en un bloque de código."""
    solo_prosa = "## Clases\n- Usa `__init__` para el estado inicial.\n"
    con_ejemplo = (
        "## Clases\n"
        "```python\n"
        "class Producto:\n"
        "    def __init__(self, nombre):\n"
        "        self.nombre = nombre\n"
        "```\n"
    )
    assert _conceptos_en(ejemplos_ejecutables(solo_prosa)) == set()
    assert {"class", "def", "self", "__init__"} <= _conceptos_en(
        ejemplos_ejecutables(con_ejemplo)
    )


def test_ningun_ejercicio_pide_lo_que_no_se_ha_ensenado():
    """Compara los huecos reales contra la lista congelada, en los dos sentidos."""
    detectados = detectar_huecos()

    nuevos = detectados - HUECOS_CONOCIDOS
    assert not nuevos, (
        "Hueco de concepto NUEVO: estos ejercicios piden algo que ninguna "
        "lección anterior muestra en un bloque de código ejecutable. Enseña el "
        "concepto con un ejemplo, o cambia el enunciado:\n  "
        + "\n  ".join(f"{lec} -> {ej}: {c}" for lec, ej, c in sorted(nuevos))
    )

    cerrados = HUECOS_CONOCIDOS - detectados
    assert not cerrados, (
        "Estos huecos ya están cerrados: bórralos de HUECOS_CONOCIDOS para que "
        "el test los proteja de verdad:\n  "
        + "\n  ".join(f"{lec} -> {ej}: {c}" for lec, ej, c in sorted(cerrados))
    )


def test_el_detector_no_es_vacuo(monkeypatch):
    """Un detector que nunca encuentra nada aprueba cualquier temario.

    Antes esto se comprobaba contra el temario real ("si no ve huecos es que
    está roto"), que valía mientras Track 1 estuviera sin contenido. Cerrados
    los 13, se le da un temario de mentira con un hueco evidente: una lección
    que explica `__init__` **solo en prosa** y un ejercicio que pide escribir
    una clase. Si tampoco lo ve, el guard rail no protege nada.
    """
    temario_con_hueco = [
        LessonTemplate(
            title="Clases sin ejemplos",
            description="",
            content="## Clases\n- Usa `__init__` para el estado inicial.\n",
            difficulty="beginner",
            category="fundamentos",
            order=1,
            estimated_duration=10,
            exercises=[
                ExerciseTemplate(
                    title="Pide una clase",
                    description="",
                    instructions="Define `class Punto` con su `__init__`.",
                    starter_code="",
                )
            ],
        )
    ]
    monkeypatch.setattr(sys.modules[__name__], "LESSON_TEMPLATES", temario_con_hueco)

    assert detectar_huecos() == {
        ("Clases sin ejemplos", "Pide una clase", "class"),
        ("Clases sin ejemplos", "Pide una clase", "__init__"),
    }
