"""Integration tests for saved EML processing."""

import os
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import requests_mock

from src.client import API_URL
from src.processor import process_eml


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "normal_message.eml"
MESSAGE_ID = "8be737ce-03c4-4a2c-a07d-0a732a85e111"
RECEIVED_AT = datetime(2026, 9, 22, tzinfo=timezone.utc)


class ProcessEmlTests(unittest.TestCase):
    def test_extracts_validates_and_sends_message_data(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            eml_path = Path(temporary_directory) / f"{MESSAGE_ID}.eml"
            shutil.copy(FIXTURE_PATH, eml_path)
            os.utime(eml_path, (RECEIVED_AT.timestamp(), RECEIVED_AT.timestamp()))

            with requests_mock.Mocker() as mock_api:
                mock_api.post(API_URL, status_code=200)

                status = process_eml(eml_path)

        self.assertEqual(status, 200)
        self.assertEqual(
            mock_api.last_request.json(),
            {
                "message_id": MESSAGE_ID,
                "received_at": "2026-09-22T00:00:00Z",
                "session_id": "ec8a514e-f1f2-4065-896d-6af7d40d8b22",
                "house_id": "ed0a4093-9e61-4f91-8dbf-7663d72a6c33",
                "guest_message": "チェックイン前に荷物を預けられますか？",
            },
        )
