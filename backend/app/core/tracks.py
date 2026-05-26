"""
Metadatos de los Tracks de la plataforma.

Centraliza los títulos legibles de cada Track para que el endpoint de
progreso, los certificados y futuras features no dupliquen el diccionario.
"""

# Títulos legibles por Track. Track 1 está activo; 2-6 son el roadmap
# ML/DL/AI Engineering (ver `project_norte_ml_ai`).
TRACK_TITLES: dict[str, str] = {
    "track-1": "Track 1 · Python",
    "track-2": "Track 2 · Data Science",
    "track-3": "Track 3 · ML Clasico",
    "track-4": "Track 4 · Deep Learning",
    "track-5": "Track 5 · AI Engineering",
    "track-6": "Track 6 · MLOps",
}


def track_title(track: str) -> str:
    """Título legible del track, con fallback al propio identificador."""
    return TRACK_TITLES.get(track, track)
