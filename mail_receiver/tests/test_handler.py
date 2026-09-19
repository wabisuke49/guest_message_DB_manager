from __future__ import annotations

import unittest
from types import SimpleNamespace

from src.handler import SMTPReceiveHandler


class SMTPReceiveHandlerTest(unittest.IsolatedAsyncioTestCase):
    async def test_passes_envelope_values_to_application_callback(self) -> None:
        received: list[tuple[str, list[str], bytes]] = []
        handler = SMTPReceiveHandler(
            lambda mail_from, rcpt_tos, content: received.append(
                (mail_from, rcpt_tos, content)
            )
        )
        envelope = SimpleNamespace(
            mail_from="sender@example.test",
            rcpt_tos=["first@example.test", "second@example.test"],
            content=b"Subject: test\r\n\r\nHello.\r\n",
        )

        response = await handler.handle_DATA(None, None, envelope)

        self.assertEqual("250 Message accepted for delivery", response)
        self.assertEqual(
            [("sender@example.test", ["first@example.test", "second@example.test"], envelope.content)],
            received,
        )

    async def test_callback_failure_returns_temporary_smtp_error(self) -> None:
        def fail(*_args: object) -> None:
            raise RuntimeError("downstream unavailable")

        handler = SMTPReceiveHandler(fail)
        envelope = SimpleNamespace(
            mail_from="sender@example.test",
            rcpt_tos=["recipient@example.test"],
            content=b"test",
        )

        with self.assertLogs("src.handler", level="ERROR"):
            response = await handler.handle_DATA(None, None, envelope)

        self.assertTrue(response.startswith("451"))


if __name__ == "__main__":
    unittest.main()
