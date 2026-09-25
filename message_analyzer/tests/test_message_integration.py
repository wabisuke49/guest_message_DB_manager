"""Integration tests for the message validation endpoint."""

import unittest

from fastapi.testclient import TestClient

from main import app


class MessageEndpointIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.valid_message = {
            "message_id": "b76674b0-a19b-4aa9-9d15-09ac4cf31871",
            "received_at": "2026-09-22T10:00:00Z",
            "session_id": "3885c57d-28c0-4777-92e2-cd293c4cac08",
            "house_id": "01f92a4a-bc7c-4e2a-919d-02c4e9ac1b52",
            "guest_message": "チェックイン方法を教えてください。",
        }

    def test_valid_message_returns_validated_status(self) -> None:
        response = self.client.post("/messages", json=self.valid_message)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "validated"})

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
