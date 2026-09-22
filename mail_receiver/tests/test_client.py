"""Tests for the Phase 2 API client."""

import unittest
from unittest.mock import MagicMock, patch

from src.client import API_URL, send_message_data


class SendMessageDataTests(unittest.TestCase):
    
    def test_posts_message_data_as_json(self) -> None:
        message_data = {
            "message_id": "8be737ce-03c4-4a2c-a07d-0a732a85e111",
            "received_at": "2026-09-21T00:00:00Z",
            "session_id": "ec8a514e-f1f2-4065-896d-6af7d40d8b22",
            "house_id": "ed0a4093-9e61-4f91-8dbf-7663d72a6c33",
            "guest_message": "チェックイン前に荷物を預けられますか？",
        }
        response = MagicMock(status_code=200)

        with patch("src.client.requests.post") as mock_post:
            mock_post.return_value = response

            status = send_message_data(message_data)

        self.assertEqual(status, 200)
        mock_post.assert_called_once_with(API_URL, json=message_data)
