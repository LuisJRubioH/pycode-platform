"""
Import coding challenges from local repositories while hiding solutions from students.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.challenge import CodingChallenge


CHALLENGE_SOURCES = [
    ("Retos/Nivel-1-facil", "easy", "retos-python-core"),
    ("Retos/Nivel-2-medio", "medium", "retos-python-core"),
    ("Retos/Nivel-3-dificil", "hard", "retos-python-core"),
    ("Retos_101_ejercicios/facil", "easy", "retos-python-101"),
    ("Retos_101_ejercicios/medio", "medium", "retos-python-101"),
    ("Retos_101_ejercicios/dificil", "hard", "retos-python-101"),
    ("Retos_21_dias_de_python", "easy", "retos-python-21-dias"),
]


def _challenge_root() -> Path:
    return settings.project_root / "external" / "Retos_Python"


def _read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="ignore")


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def _clean_title(path: Path, prompt: str) -> str:
    first_line = next(
        (line.strip(" \"'#/") for line in prompt.splitlines() if line.strip()), ""
    )
    if first_line:
        return first_line[:120]
    return path.stem.replace("_", " ").replace("-", " ").title()


def _extract_prompt_and_solution(source_code: str) -> tuple[str, str]:
    prompt_parts: list[str] = []

    try:
        module = ast.parse(source_code)
        docstring = ast.get_docstring(module)
        if docstring:
            prompt_parts.append(docstring.strip())
    except SyntaxError:
        module = None

    if not prompt_parts:
        leading_lines = []
        for line in source_code.splitlines():
            stripped = line.strip()
            if not stripped:
                if leading_lines:
                    break
                continue
            if stripped.startswith(
                ("def ", "class ", "import ", "from ", "print(", "if __name__")
            ):
                break
            leading_lines.append(stripped.strip('"'))
        if leading_lines:
            prompt_parts.append("\n".join(leading_lines).strip())

    prompt = "\n\n".join(part for part in prompt_parts if part).strip()
    if not prompt:
        prompt = "Resuelve este reto de programacion en Python."

    return prompt, source_code.strip()


def _infer_topic(path: Path) -> str:
    stem = path.stem.lower()
    for topic in (
        "fibonacci",
        "primos",
        "palindromo",
        "anagrama",
        "morse",
        "factorial",
        "strings",
        "listas",
        "matematicas",
        "logica",
        "password",
    ):
        if topic in stem:
            return topic
    return "logic"


def _recommended_starter_code(title: str) -> str:
    return f"# Reto: {title}\n# Escribe tu solucion aqui\n"


async def import_external_challenges(db: AsyncSession) -> int:
    """Import challenges from the downloaded repo if they are not already present."""
    root = _challenge_root()
    if not root.exists():
        return 0

    inserted = 0
    order_index = 1

    for relative_dir, difficulty, source_name in CHALLENGE_SOURCES:
        source_dir = root / relative_dir
        if not source_dir.exists():
            continue

        for path in sorted(source_dir.glob("*.py")):
            slug = _slugify(f"{source_name}-{path.stem}")
            existing = await db.execute(
                select(CodingChallenge.id).where(CodingChallenge.slug == slug)
            )
            if existing.scalar_one_or_none() is not None:
                order_index += 1
                continue

            source_code = _read_text(path)
            prompt, solution = _extract_prompt_and_solution(source_code)
            title = _clean_title(path, prompt)

            challenge = CodingChallenge(
                title=title,
                slug=slug,
                source=source_name,
                source_path=str(path.relative_to(root)),
                difficulty=difficulty,
                topic=_infer_topic(path),
                prompt=prompt,
                starter_code=_recommended_starter_code(title),
                reference_solution=solution,
                order_index=order_index,
            )
            db.add(challenge)
            inserted += 1
            order_index += 1

    if inserted:
        await db.commit()

    return inserted


def recommended_difficulty_for_elo(elo_rating: int) -> str:
    if elo_rating < 1100:
        return "easy"
    if elo_rating < 1500:
        return "medium"
    return "hard"
