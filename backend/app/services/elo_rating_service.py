"""
Gestión de ratings ELO multidominio.

Cada *(usuario, dominio, scope)* lleva su propio ELO. `process_attempt`
(en `elo_service`) sigue siendo la función pura que calcula deltas; aquí solo
resolvemos *qué* rating leer/escribir y aplicamos el resultado.

Lazy-init: la primera vez que un usuario toca una track, su rating hereda el
ELO global (`UserProfile.elo_rating`) para no resetear su progreso.
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.elo_models import EloRating
from app.services.elo_service import EloResult, get_rank

DOMAIN_PUZZLE = "puzzle"
DOMAIN_CHALLENGE = "challenge"

# ELO nominal de un reto según su dificultad: se usa como "elo del rival" al
# otorgar ELO por completar un reto (la completación cuenta como acierto).
CHALLENGE_DIFFICULTY_ELO = {"easy": 850, "medium": 1200, "hard": 1550}


def nominal_elo_for_difficulty(difficulty: str) -> int:
    return CHALLENGE_DIFFICULTY_ELO.get(difficulty, 1200)


async def get_or_init_rating(
    db: AsyncSession,
    user_id: int,
    domain: str,
    scope: str,
    *,
    fallback_elo: int = 1000,
) -> EloRating:
    """Devuelve el rating de la track, creándolo (heredando `fallback_elo`) si
    aún no existe. El caller es responsable del commit."""
    row = await db.execute(
        select(EloRating).where(
            EloRating.user_id == user_id,
            EloRating.domain == domain,
            EloRating.scope == scope,
        )
    )
    rating = row.scalar_one_or_none()
    if rating is None:
        rating = EloRating(
            user_id=user_id,
            domain=domain,
            scope=scope,
            elo_rating=fallback_elo,
            elo_peak=fallback_elo,
            rank=get_rank(fallback_elo).value,
        )
        db.add(rating)
        await db.flush()
    return rating


def apply_result_to_rating(rating: EloRating, result: EloResult) -> None:
    """Aplica el resultado de un intento al rating (in-place)."""
    rating.elo_rating = result.user_elo_after
    rating.elo_peak = max(rating.elo_peak, result.user_elo_after)
    rating.rank = result.rank_after.value
    rating.attempts += 1
    rating.last_activity = datetime.utcnow()
    if result.correct:
        rating.correct += 1
        rating.streak_current += 1
        rating.streak_best = max(rating.streak_best, rating.streak_current)
    else:
        rating.streak_current = 0
