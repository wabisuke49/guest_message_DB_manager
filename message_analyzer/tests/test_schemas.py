"""Unit tests for message request validation."""

import unittest

from pydantic import ValidationError

from schemas import MessageRequest


class MessageRequestValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_message = {
            "message_id": "b76674b0-a19b-4aa9-9d15-09ac4cf31871",
            "received_at": "2026-09-22T10:00:00Z",
            "session_id": "3885c57d-28c0-4777-92e2-cd293c4cac08",
            "house_id": "01f92a4a-bc7c-4e2a-919d-02c4e9ac1b52",
            "guest_message": "チェックイン方法を教えてください。",
        }

    def test_accepts_z_utc_datetime(self) -> None:
        message = MessageRequest(**self.valid_message)

        self.assertEqual(message.received_at.isoformat(), "2026-09-22T10:00:00+00:00")

    def test_accepts_plus_zero_zero_utc_datetime(self) -> None:
        self.valid_message["received_at"] = "2026-09-22T10:00:00+00:00"

        message = MessageRequest(**self.valid_message)

        self.assertEqual(message.received_at.isoformat(), "2026-09-22T10:00:00+00:00")

    def test_rejects_invalid_uuid(self) -> None:
        self.valid_message["message_id"] = "not-a-uuid"
        self.valid_message["session_id"] = "not-a-uuid"
        self.valid_message["house_id"] = "not-a-uuid"

        with self.assertRaises(ValidationError):
            MessageRequest(**self.valid_message)

    def test_rejects_non_utc_datetime(self) -> None:
        self.valid_message["received_at"] = "2026-09-22T19:00:00+09:00"

        with self.assertRaises(ValidationError):
            MessageRequest(**self.valid_message)

    def test_rejects_unexisting_date(self) -> None:
        self.valid_message["received_at"] = "2026-02-30T10:00:00Z"

        with self.assertRaises(ValidationError):
            MessageRequest(**self.valid_message)

    def test_rejects_zero_character_guest_message(self) -> None:
        self.valid_message["guest_message"] = ""

        with self.assertRaises(ValidationError):
            MessageRequest(**self.valid_message)

    def test_rejects_blank_guest_message(self) -> None:
        self.valid_message["guest_message"] = " \t\n　 "

        with self.assertRaises(ValidationError):
            MessageRequest(**self.valid_message)

    def test_rejects_missing_required_field(self) -> None:
        del self.valid_message["session_id"]

        with self.assertRaises(ValidationError):
            MessageRequest(**self.valid_message)
