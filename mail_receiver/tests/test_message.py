"""Tests for MVP message data extraction."""

import unittest

from src.message import extract_message_data


class ExtractMessageDataTests(unittest.TestCase):
    def test_extracts_mvp_message_data(self) -> None:
        message_id = "8be737ce-03c4-4a2c-a07d-0a732a85e111"
        session_id = "ec8a514e-f1f2-4065-896d-6af7d40d8b22"
        house_id = "ed0a4093-9e61-4f91-8dbf-7663d72a6c33"
        received_at = "2026-09-21T00:00:00Z"
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

        result = extract_message_data(body, message_id, received_at)

        self.assertEqual(
            result,
            {
                "message_id": message_id,
                "received_at": received_at,
                "session_id": session_id,
                "house_id": house_id,
                "guest_message": "チェックイン前に荷物を預けられますか？",
            },
        )
