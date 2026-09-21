"""Tests for SQLite database initialization."""

import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from database import initialize_database


class DatabaseInitializationTests(unittest.TestCase):
    def test_creates_messages_table(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "messages.db"

            initialize_database(database_path)

            self.assertTrue(database_path.exists())
            with closing(sqlite3.connect(database_path)) as connection:
                columns = connection.execute("PRAGMA table_info(messages)").fetchall()

        self.assertEqual(
            [column[1] for column in columns],
            ["message_id", "received_at", "session_id", "house_id", "guest_message"],
        )

    def test_can_initialize_the_same_database_twice(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "messages.db"

            initialize_database(database_path)
            initialize_database(database_path)
