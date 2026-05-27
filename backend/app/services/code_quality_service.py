"""
Análisis estático de código del alumno (Pieza L).

Calcula métricas de calidad SIN ejecutar el código: solo `ast.parse` (igual
que `/execute/validate`), por lo que es seguro en el backend. Produce un
`static_score` 0-100 determinista a partir de heurísticas objetivas
(complejidad, longitud de funciones, anidamiento, docstrings, líneas largas).

Complementa los `logic_score`/`general_score` del evaluador LLM: el LLM juzga
la lógica/enfoque; esto mide la forma del código de manera reproducible.
"""

import ast
from dataclasses import dataclass, field

_COMPOUND = (
    ast.If,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
)
_BRANCH = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler)
_FUNC = (ast.FunctionDef, ast.AsyncFunctionDef)


@dataclass
class AnalysisResult:
    static_score: int
    metrics: dict = field(default_factory=dict)


def _max_nesting(node: ast.AST, depth: int = 0) -> int:
    best = depth
    for child in ast.iter_child_nodes(node):
        child_depth = depth + (1 if isinstance(child, _COMPOUND) else 0)
        best = max(best, _max_nesting(child, child_depth))
    return best


def _cyclomatic(tree: ast.AST) -> int:
    complexity = 1
    for node in ast.walk(tree):
        if isinstance(node, _BRANCH):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
        elif isinstance(node, ast.comprehension):
            complexity += 1 + len(node.ifs)
    return complexity


def analyze_code(code: str) -> AnalysisResult:
    """Analiza `code` y devuelve un `static_score` 0-100 + métricas crudas."""
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return AnalysisResult(
            static_score=0,
            metrics={"syntax_ok": False, "error": str(exc)},
        )

    funcs = [n for n in ast.walk(tree) if isinstance(n, _FUNC)]
    n_functions = len(funcs)
    n_classes = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])

    func_lengths = [getattr(f, "end_lineno", f.lineno) - f.lineno + 1 for f in funcs]
    max_func_len = max(func_lengths) if func_lengths else 0
    avg_func_len = (
        round(sum(func_lengths) / len(func_lengths), 1) if func_lengths else 0.0
    )

    complexity = _cyclomatic(tree)
    max_nesting = _max_nesting(tree)

    documented = sum(1 for f in funcs if ast.get_docstring(f))
    docstring_ratio = round(documented / n_functions, 2) if n_functions else 1.0

    lines = code.splitlines()
    long_lines = sum(1 for ln in lines if len(ln) > 100)

    # Score determinista: arranca en 100 y resta penalizaciones acotadas.
    score = 100
    if max_func_len > 30:
        score -= min(25, max_func_len - 30)
    if complexity > 10:
        score -= min(25, (complexity - 10) * 2)
    if max_nesting > 4:
        score -= min(20, (max_nesting - 4) * 5)
    if n_functions and docstring_ratio < 1.0:
        score -= round((1.0 - docstring_ratio) * 10)
    score -= min(10, long_lines * 2)
    score = max(0, min(100, score))

    return AnalysisResult(
        static_score=score,
        metrics={
            "syntax_ok": True,
            "n_lines": len(lines),
            "n_functions": n_functions,
            "n_classes": n_classes,
            "max_func_len": max_func_len,
            "avg_func_len": avg_func_len,
            "cyclomatic_complexity": complexity,
            "max_nesting": max_nesting,
            "docstring_ratio": docstring_ratio,
            "long_lines": long_lines,
        },
    )
