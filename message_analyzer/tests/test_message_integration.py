"""Integration tests for the message receiving endpoint."""

import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from database import initialize_database
from main import app


class MessageEndpointIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.database_path = Path(self.temporary_directory.name) / "messages.db"
        initialize_database(self.database_path)

        self.database_path_patcher = patch("database.DATABASE_PATH", self.database_path)
        self.database_path_patcher.start()
        self.addCleanup(self.database_path_patcher.stop)

        self.client = TestClient(app)
        self.valid_message = {
            "message_id": "b76674b0-a19b-4aa9-9d15-09ac4cf31871",
            "received_at": "2026-09-22T10:00:00Z",
            "session_id": "3885c57d-28c0-4777-92e2-cd293c4cac08",
            "house_id": "01f92a4a-bc7c-4e2a-919d-02c4e9ac1b52",
            "guest_message": "チェックイン方法を教えてください。",
        }

    def test_valid_message_is_saved(self) -> None:
        response = self.client.post("/messages", json=self.valid_message)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"status": "saved"})

        with closing(sqlite3.connect(self.database_path)) as connection:
            stored_message = connection.execute(
                "SELECT message_id FROM messages"
            ).fetchone()

        self.assertEqual(stored_message, (self.valid_message["message_id"],))

    def test_duplicate_message_is_not_saved_twice(self) -> None:
        self.client.post("/messages", json=self.valid_message)

        response = self.client.post("/messages", json=self.valid_message)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "duplicate"})

        with closing(sqlite3.connect(self.database_path)) as connection:
            message_count = connection.execute("SELECT COUNT(*) FROM messages").fetchone()[0]

        self.assertEqual(message_count, 1)

    def test_invalid_message_returns_unprocessable_entity(self) -> None:
        self.valid_message["message_id"] = "not-a-uuid"

        response = self.client.post("/messages", json=self.valid_message)

        self.assertEqual(response.status_code, 422)

    def test_invalid_json_returns_unprocessable_entity(self) -> None:
        response = self.client.post(
            "/messages",
            content="{",
            headers={"content-type": "application/json"},
        )

        self.assertEqual(response.status_code, 422)
