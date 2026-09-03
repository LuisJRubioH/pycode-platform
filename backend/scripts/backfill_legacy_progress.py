"""Backfill de las filas ``UserProgress`` con el progreso legacy clavado.

Antes del fix del Bloque 1, abrir una lección escribía un ``progress`` fijo
(el sentinel ``5``) que nunca se recalculaba a partir de los ejercicios
hechos. Esas filas siguen en la base con el valor viejo hasta que el usuario
vuelve a entrar a la lección (``GET /lessons/{id}`` ya llama a
``recompute_lesson_progress``). Este script las recalcula de una vez.

Uso::

    # 1. Solo mirar: cuántas filas hay y qué pasaría con ellas (por defecto).
    python scripts/backfill_legacy_progress.py

    # 2. Aplicar de verdad (pide confirmación explícita).
    python scripts/backfill_legacy_progress.py --apply

Sin ``--apply`` **no escribe nada**: abre la transacción, calcula y hace
rollback. Es idempotente: recalcula desde las ``CodeSubmission``, así que
correrlo N veces deja el mismo estado.
"""

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import func, select  # noqa: E402

from app.core.database import async_session_maker  # noqa: E402
from app.models.learning import Lesson, UserProgress  # noqa: E402
from app.services.progress_service import (  # noqa: E402
    recompute_lesson_progress,
)

# Valor que escribía el código viejo al abrir una lección, sin relación con
# los ejercicios resueltos.
LEGACY_SENTINEL = 5


async def report(apply: bool) -> int:
    async with async_session_maker() as session:
        total_rows = (
            await session.execute(select(func.count(UserProgress.id)))
        ).scalar_one()

        candidates = (
            (
                await session.execute(
                    select(UserProgress).where(UserProgress.progress == LEGACY_SENTINEL)
                )
            )
            .scalars()
            .all()
        )

        print(f"Filas UserProgress totales:            {total_rows}")
        print(
            f"Filas con progress == {LEGACY_SENTINEL} (sentinel legacy):"
            f" {len(candidates)}"
        )

        if not candidates:
            print("\nNada que hacer.")
            return 0

        titles = {
            row[0]: row[1]
            for row in (await session.execute(select(Lesson.id, Lesson.title))).all()
        }

        print("\nRecálculo propuesto (usuario, lección, antes -> después):")
        changed = 0
        for progress in candidates:
            before_pct, before_status = progress.progress, progress.status
            recomputed = await recompute_lesson_progress(
                session, progress.user_id, progress.lesson_id
            )
            after_pct, after_status = recomputed.progress, recomputed.status
            if (before_pct, before_status) != (after_pct, after_status):
                changed += 1
            title = titles.get(progress.lesson_id, "?")
            print(
                f"  user={progress.user_id:<5} lesson={progress.lesson_id:<5}"
                f" {title[:38]:<40}"
                f" {before_pct}% {before_status} -> {after_pct}% {after_status}"
            )

        print(f"\nFilas que cambiarían de verdad: {changed} de {len(candidates)}")

        if apply:
            await session.commit()
            print("\nAPLICADO: cambios commiteados.")
        else:
            await session.rollback()
            print("\nSIMULACIÓN: rollback, no se escribió nada.")
            print("Para aplicarlo: python scripts/backfill_legacy_progress.py --apply")
        return len(candidates)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Escribe los cambios. Sin este flag el script es de solo lectura.",
    )
    args = parser.parse_args()
    asyncio.run(report(args.apply))


if __name__ == "__main__":
    main()
