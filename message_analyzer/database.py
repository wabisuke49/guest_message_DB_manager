"""SQLite database setup for the message analysis service."""

import sqlite3
from contextlib import closing
from pathlib import Path

from schemas import MessageRequest

SERVICE_DIRECTORY = Path(__file__).resolve().parent
DATABASE_PATH = SERVICE_DIRECTORY / "data" / "messages.db"
SCHEMA_PATH = SERVICE_DIRECTORY / "schema.sql"


def initialize_database(database_path: Path = DATABASE_PATH) -> None:
    """Create the SQLite database and apply the initial schema."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    cur.execute(schema)

    conn.commit()
    conn.close()

def check_duplication(message:MessageRequest, database_path: Path | None = None) -> bool:
    """Check if a message is duplicated in the database."""
    target_path = DATABASE_PATH if database_path is None else database_path

    with closing(sqlite3.connect(target_path)) as connection:
        result = connection.execute(
            """
            SELECT EXISTS(
                SELECT 1
                FROM messages
                WHERE message_id = ?
            )
            """,
            (str(message.message_id),)
        ).fetchone()[0]

    return bool(result)


def save_message(message: MessageRequest, database_path: Path | None = None) -> bool:
    """Save a message and return whether it was newly created."""
    target_path = DATABASE_PATH if database_path is None else database_path

    with closing(sqlite3.connect(target_path)) as connection:
        connection.execute(
            """
            INSERT INTO messages (
                message_id,
                received_at,
                session_id,
                house_id,
                guest_message
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(message.message_id),
                message.received_at.isoformat(),
                str(message.session_id),
                str(message.house_id),
                message.guest_message,
            ),
        )
        connection.commit()

    return True
