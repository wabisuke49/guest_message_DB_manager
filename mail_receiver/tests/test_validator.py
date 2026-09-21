"""Tests for send-side message validation."""

import unittest

from src.validator import validate_message_data


class ValidateMessageDataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.message = {
            "message_id": "8be737ce-03c4-4a2c-a07d-0a732a85e111",
            "received_at": "2026-09-21T00:00:00Z",
            "session_id": "ec8a514e-f1f2-4065-896d-6af7d40d8b22",
            "house_id": "ed0a4093-9e61-4f91-8dbf-7663d72a6c33",
            "guest_message": "チェックイン前に荷物を預けられますか？",
        }

    def test_returns_message_when_all_fields_are_valid(self) -> None:
        self.assertEqual(validate_message_data(self.message), self.message)
    
