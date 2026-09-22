"""Tests for SQLite database initialization."""

import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from database import check_duplication, initialize_database, save_message
from schemas import MessageRequest


class DatabaseInitializationTests(unittest.TestCase):
    def test_initializes_database(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "messages.db"

            initialize_database(database_path)

            with closing(sqlite3.connect(database_path)) as connection:
                result = connection.execute("SELECT 1").fetchone()

        self.assertEqual(result, (1,))

    def test_can_initialize_the_same_database_twice(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "messages.db"

            initialize_database(database_path)
            initialize_database(database_path)


class MessagePersistenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.database_path = Path(self.temporary_directory.name) / "messages.db"
        initialize_database(self.database_path)
        self.message = MessageRequest(
            message_id="b76674b0-a19b-4aa9-9d15-09ac4cf31871",
            received_at="2026-09-22T10:00:00Z",
            session_id="3885c57d-28c0-4777-92e2-cd293c4cac08",
            house_id="01f92a4a-bc7c-4e2a-919d-02c4e9ac1b52",
            guest_message="チェックイン方法を教えてください。",
        )

    def test_saves_message(self) -> None:
        was_saved = save_message(self.message, self.database_path)

        self.assertTrue(was_saved)
        with closing(sqlite3.connect(self.database_path)) as connection:
            saved_message = connection.execute(
                """
                SELECT message_id, received_at, session_id, house_id, guest_message
                FROM messages
                """
            ).fetchone()

        self.assertEqual(
            saved_message,
            (
                "b76674b0-a19b-4aa9-9d15-09ac4cf31871",
                "2026-09-22T10:00:00+00:00",
                "3885c57d-28c0-4777-92e2-cd293c4cac08",
                "01f92a4a-bc7c-4e2a-919d-02c4e9ac1b52",
                "チェックイン方法を教えてください。",
            ),
        )

    def test_detects_duplicate_message(self) -> None:
        self.assertFalse(check_duplication(self.message, self.database_path))

        save_message(self.message, self.database_path)

        self.assertTrue(check_duplication(self.message, self.database_path))
