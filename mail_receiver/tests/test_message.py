"""Tests for MVP message data generation."""

import os
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from src.message import extract_message_data, get_message_data


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "normal_message.eml"
MESSAGE_ID = "8be737ce-03c4-4a2c-a07d-0a732a85e111"
RECEIVED_AT = datetime(2026, 9, 22, tzinfo=timezone.utc)


class ExtractMessageDataTests(unittest.TestCase):
    def test_extracts_message_data_from_body(self) -> None:
        session_id = "ec8a514e-f1f2-4065-896d-6af7d40d8b22"
        house_id = "ed0a4093-9e61-4f91-8dbf-7663d72a6c33"
        body = f"""担当者 様、

このメールには返信しないでください。
Booking.comからの問い合わせを確認してください：

チェックイン前に荷物を預けられますか？

詳細を見る: https://pms.airhost.co/messages?houseId={house_id}&ticketId={session_id}

ご注文について

発注元: Booking.com
注文番号: TEST-RESERVATION-ID
物件名: テスト物件
"""

        result = extract_message_data(body)

        self.assertEqual(
            result,
            {
                "session_id": session_id,
                "house_id": house_id,
                "guest_message": "チェックイン前に荷物を預けられますか？",
            },
        )

    def test_builds_message_data_from_saved_eml(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            eml_path = Path(temporary_directory) / f"{MESSAGE_ID}.eml"
            shutil.copy(FIXTURE_PATH, eml_path)
            os.utime(eml_path, (RECEIVED_AT.timestamp(), RECEIVED_AT.timestamp()))

            result = get_message_data(eml_path)

        self.assertEqual(
            result,
            {
                "message_id": MESSAGE_ID,
                "received_at": "2026-09-22T00:00:00Z",
                "session_id": "ec8a514e-f1f2-4065-896d-6af7d40d8b22",
                "house_id": "ed0a4093-9e61-4f91-8dbf-7663d72a6c33",
                "guest_message": "チェックイン前に荷物を預けられますか？",
            },
        )
