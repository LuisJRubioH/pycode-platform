"""Regresión del banco curado de puzzles (Pieza G).

Garantiza que:
- el banco tiene exactamente 100 puzzles conceptuales
- los `slug_suffix` son únicos (el slug final debe ser único en la tabla)
- TODO `code_snippet` produce EXACTAMENTE su `correct_output` al ejecutarse

Lo último es el guard rail clave: si un puzzle quedara con la respuesta mal
fijada (p. ej. drift de versión de numpy/pandas), sería imposible de resolver.
Ejecutamos cada snippet en un namespace limpio y comparamos su stdout.
"""

import contextlib
import io

from app.services.generated_bank import _PUZZLE_CATALOG


def _run_snippet(code: str) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {})  # noqa: S102 - contenido curado del propio repo
    out = buf.getvalue()
    return out[:-1] if out.endswith("\n") else out


def test_bank_has_100_puzzles():
    total = sum(len(puzzles) for _, puzzles in _PUZZLE_CATALOG)
    assert total == 100


def test_slug_suffixes_are_unique():
    suffixes = [p.slug_suffix for _, puzzles in _PUZZLE_CATALOG for p in puzzles]
    assert len(suffixes) == len(set(suffixes))


def test_every_snippet_matches_its_correct_output():
    mismatches = []
    for category, puzzles in _PUZZLE_CATALOG:
        for p in puzzles:
            try:
                actual = _run_snippet(p.code_snippet)
            except Exception as exc:  # noqa: BLE001
                mismatches.append(
                    f"{category}/{p.slug_suffix}: EXC {type(exc).__name__}: {exc}"
                )
                continue
            if actual != p.correct_output:
                mismatches.append(
                    f"{category}/{p.slug_suffix}: got {actual!r} "
                    f"expected {p.correct_output!r}"
                )
    assert not mismatches, "Puzzles con salida incorrecta:\n" + "\n".join(mismatches)
