"""
Falla si encuentra SQL construido por interpolación de strings.
Permitido: text("SELECT ... :param") con bindeo, text(\""" SQL literal \""")
Prohibido: text(f"..."), text("..." + var), execute(f"...")
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "app", ROOT / "alembic"]

# Patrón 1: text(f"...
PAT_FSTRING = re.compile(r"\btext\s*\(\s*f['\"]")
# Patrón 2: text("..." + ...) o text(... + ...)
PAT_CONCAT = re.compile(r"\btext\s*\([^)]*\+[^)]*\)")
# Patrón 3: execute(f"...
PAT_EXECUTE_FSTRING = re.compile(r"\bexecute\s*\(\s*f['\"]")

violations: list[str] = []

for base in TARGETS:
    if not base.exists():
        continue
    for py_file in base.rglob("*.py"):
        if "__pycache__" in py_file.parts:
            continue
        text = py_file.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for pat in (PAT_FSTRING, PAT_CONCAT, PAT_EXECUTE_FSTRING):
                if pat.search(line):
                    violations.append(
                        f"{py_file.relative_to(ROOT)}:{lineno}: {line.strip()}"
                    )

if violations:
    print(
        "SQLi risk: queries con interpolación de strings detectadas:\n",
        file=sys.stderr,
    )
    for v in violations:
        print(f"  {v}", file=sys.stderr)
    print(
        '\nUsar text("... :param") con parámetros bindeados o pasar al ORM.',
        file=sys.stderr,
    )
    sys.exit(1)

print("OK: sin riesgos de SQL injection detectados.")
