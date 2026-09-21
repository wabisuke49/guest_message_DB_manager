"""Tests for SQLite database initialization."""

import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from database import initialize_database


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
