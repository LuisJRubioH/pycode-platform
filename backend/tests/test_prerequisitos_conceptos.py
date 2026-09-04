"""Regla de contenido: nada se pide antes de haberse enseñado.

Un ejercicio no puede exigir un concepto que su lección —o una anterior del
temario— no haya mostrado **dentro de un bloque de código ejecutable**. La
prosa no cuenta: "Usa `__init__` para estado inicial" en una viñeta no enseña
a escribir un método.

Por qué esto es un test y no una buena intención: en la auditoría de contenido
(``docs/AUDITORIA_CONTENIDO.md``) se encontró que ``def`` no aparece en NINGUNA
lección de Track 1, y aun así cinco ejercicios lo exigen desde la lección 5. El
alumno escribe su primera función sin haber visto nunca una definición.

## Cómo se maneja mientras Track 1 siga vacío

En vez de marcar el test como ``xfail`` —que lo dejaría dormido y sin proteger
nada— se congela la lista exacta de huecos conocidos en ``HUECOS_CONOCIDOS`` y
se compara por igualdad. Así el test está **activo desde hoy**:

- si aparece un hueco nuevo, falla (protege contra regresiones ya);
- si se cierra uno de los conocidos, también falla, pidiendo que se borre de la
  lista (impide que la deuda se quede escrita para siempre).

Cuando se reescriba Track 1, la lista se vacía y el test queda como guard rail
permanente sin tocar una línea de lógica.

## Límite conocido

El detector busca *tokens de Python*, no paráfrasis en español. "Cuenta
bancaria" pide "lanza ValueError" sin escribir ``raise`` en el enunciado ni en
el starter, así que ese hueco NO se detecta aquí aunque sea real. El detector
es un suelo, no un techo.
"""

import re

from app.services.lesson_seed import LESSON_TEMPLATES

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


# Deuda de contenido viva. Se encoge segun avanza la reescritura de Track 1
# (plan en docs/PLANTILLA_LECCION.md): 13 huecos el 2026-09-03, 8 tras
# "Funciones y Parametros" y 6 tras "Comprensiones y Manejo de Errores",
# que cerro el `raise` de AI 2 y el `with` del ejercicio de pytest.
HUECOS_CONOCIDOS: set[tuple[str, str, str]] = {
    # Los 5 huecos de `def` se cerraron el 2026-09-03 al reescribir
    # "Funciones y Parametros", que ahora lo ensena con ejemplos ejecutables.
    # POO: el starter trae la clase hecha, pero la lección no muestra
    # ni `class`, ni `self`, ni `__init__` en un bloque de código. Se cierra
    # al reescribirla (paso 3 del plan de Track 1).
    ("POO en Python", "Clase Producto", "class"),
    ("POO en Python", "Clase Producto", "self"),
    ("POO en Python", "Clase Producto", "__init__"),
    ("POO en Python", "Cuenta bancaria", "class"),
    ("POO en Python", "Cuenta bancaria", "self"),
    ("POO en Python", "Cuenta bancaria", "__init__"),
}


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


def test_el_detector_no_es_vacuo():
    """Si HUECOS_CONOCIDOS se vacía por accidente, este test lo delata.

    Mientras Track 1 siga sin contenido tiene que haber huecos: un detector que
    hoy no encuentre nada está roto, no es que el temario esté sano.
    """
    assert detectar_huecos(), (
        "El detector no encuentra ningún hueco. O se reescribió Track 1 (en "
        "cuyo caso borra este test), o el detector dejó de funcionar."
    )
