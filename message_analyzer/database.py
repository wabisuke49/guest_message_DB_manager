"""SQLite database setup for the message analysis service."""

import sqlite3
from contextlib import closing
from pathlib import Path


SERVICE_DIRECTORY = Path(__file__).resolve().parent
DATABASE_PATH = SERVICE_DIRECTORY / "data" / "messages.db"
SCHEMA_PATH = SERVICE_DIRECTORY / "schema.sql"


def initialize_database(database_path: Path = DATABASE_PATH) -> None:
    """Create the SQLite database and apply the initial schema."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with closing(sqlite3.connect(database_path)) as connection:
        connection.executescript(schema)
