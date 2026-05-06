"""
Small schema bootstrap helpers for environments that still rely on create_all().
"""

from sqlalchemy import inspect, text


USER_PROFILE_ELO_COLUMNS = {
    "elo_rating": "INTEGER NOT NULL DEFAULT 1000",
    "elo_peak": "INTEGER NOT NULL DEFAULT 1000",
    "rank": "VARCHAR(50) NOT NULL DEFAULT 'Beginner'",
    "puzzles_attempted": "INTEGER NOT NULL DEFAULT 0",
    "puzzles_correct": "INTEGER NOT NULL DEFAULT 0",
    "streak_current": "INTEGER NOT NULL DEFAULT 0",
    "streak_best": "INTEGER NOT NULL DEFAULT 0",
    "last_activity": "DATETIME",
}

USER_PROGRESS_COLUMNS = {
    "progress": "INTEGER NOT NULL DEFAULT 0",
}


def bootstrap_elo_schema(sync_connection) -> None:
    """Add missing ELO columns to user_profiles when the table already exists."""
    inspector = inspect(sync_connection)
    if "user_profiles" not in inspector.get_table_names():
        return

    existing_columns = {
        column["name"] for column in inspector.get_columns("user_profiles")
    }
    for column_name, ddl in USER_PROFILE_ELO_COLUMNS.items():
        if column_name in existing_columns:
            continue
        sync_connection.execute(
            text(f"ALTER TABLE user_profiles ADD COLUMN {column_name} {ddl}")
        )

    if "user_progress" in inspector.get_table_names():
        progress_columns = {
            column["name"] for column in inspector.get_columns("user_progress")
        }
        for column_name, ddl in USER_PROGRESS_COLUMNS.items():
            if column_name in progress_columns:
                continue
            sync_connection.execute(
                text(f"ALTER TABLE user_progress ADD COLUMN {column_name} {ddl}")
            )
